"""EFD client class
"""

import aiohttp
import aioinflux
from astropy.time import Time, TimeDelta
import astropy.units as u
from functools import partial
from kafkit.registry.aiohttp import RegistryApi
import logging
import pandas as pd
import requests

from .auth_helper import NotebookAuth
from .efd_utils import merge_packed_time_series


class EfdClient:
    """Class to handle connections and basic queries

    Parameters
    ----------
    efd_name : `str`
        Name of the EFD instance for which to retrieve credentials.
    db_name : `str`, optional
        Name of the database within influxDB to query ('efd' by default).
    port : `str`, optional
        Port to use when querying the database ('443' by default).
    internal_scale : `str`, optional
        Time scale to use when converting times to internal formats
        ('tai' by default).
    path_to_creds : `str`, optional
        Absolute path to use when reading credentials from disk
        ('~/.lsst/notebook_auth.yaml' by default).
    client : `object`, optional
        An instance of a class that ducktypes as `aioinflux.InfluxDBClient`.
        The intent is to be able to substitute a mocked client for testing.
    """

    influx_client = None
    """The `aioinflux.client.InfluxDBClient` used for queries.

    This should be used to execute queries not wrapped by this class.
    """

    subclasses = {}
    deployment = ''

    def __init__(self, efd_name, db_name='efd', port='443',
                 internal_scale='tai', creds_service='https://roundtable.lsst.codes/segwarides/',
                 client=None):
        self.db_name = db_name
        self.internal_scale = internal_scale
        self.auth = NotebookAuth(service_endpoint=creds_service)
        host, schema_registry, user, password = self.auth.get_auth(efd_name)
        self.schema_registry = schema_registry
        if client is None:
            health_url = f'https://{host}/health'
            response = requests.get(health_url)
            if response.status_code != 200:
                raise RuntimeError(f'InfluxDB server, {host}, does not appear ready to '
                                   f'recieve queries.  Recieved code:{response.status_code} '
                                   'when attempting the health check.')
            self.influx_client = aioinflux.InfluxDBClient(host=host,
                                                          port=port,
                                                          ssl=True,
                                                          username=user,
                                                          password=password,
                                                          db=db_name,
                                                          mode='async')  # mode='blocking')
            self.influx_client.output = 'dataframe'
        else:
            self.influx_client = client
        self.query_history = []

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """Register subclasses with the abstract base class.
        """
        super().__init_subclass__(**kwargs)
        if cls.mode in EfdClient.subclasses:
            raise ValueError(f'Class for mode, {cls.mode}, already defined')
        EfdClient.subclasses[cls.deployment] = cls

    @classmethod
    def list_efd_names(cls, creds_service='https://roundtable.lsst.codes/segwarides/'):
        return NotebookAuth(service_endpoint=creds_service).list_auth()

    def from_name(self, efd_name, *args, **kwargs):
        """Construct a client for the specific named subclass.

        Parameters
        ----------
        efd_name : `str`
            Name of the EFD instance for which to construct a client.
        *args
            Extra arguments to pass to the subclass constructor.
        **kwargs
            Extra keyword arguments to pass to the subclass constructor.

        Raises
        ------
        NotImpementedError
            Raised if there is no subclass corresponding to the name.
        """
        if efd_name not in self. subclasses:
            raise NotImplementedError(f'There is no EFD client class implemented for {efd_name}.')
        return self.subclasses[efd_name](efd_name, *args, **kwargs)

    async def _do_query(self, query):
        """Query the influxDB and return results

        Parameters
        ----------
        query : `str`
            Query string to execute.

        Returns
        -------
        results : `pandas.DataFrame`
            Results of the query in a `pandas.DataFrame`.
        """
        self.query_history.append(query)
        result = await self.influx_client.query(query)
        return result

    async def get_topics(self):
        """Query the list of possible topics.

        Returns
        -------
        results : `list`
            List of valid topics in the database.
        """
        topics = await self._do_query('SHOW MEASUREMENTS')
        return topics['name'].tolist()

    async def get_fields(self, topic_name):
        """Query the list of field names for a topic.

        Parameters
        ----------
        topic_name : `str`
            Name of topic to query for field names.

        Returns
        -------
        results : `list`
            List of field names in specified topic.
        """
        fields = await self._do_query(f'SHOW FIELD KEYS FROM "{self.db_name}"."autogen"."{topic_name}"')
        return fields['fieldKey'].tolist()

    def build_time_range_query(self, topic_name, fields, start, end, is_window=False, index=None):
        """Build a query based on a time range.

        Parameters
        ----------
        topic_name : `str`
            Name of topic for which to build a query.
        fields :  `str` or `list`
            Name of field(s) to query.
        start : `astropy.time.Time`
            Start time of the time range, if ``is_window`` is specified,
            this will be the midpoint of the range.
        end : `astropy.time.Time` or `astropy.time.TimeDelta`
            End time of the range either as an absolute time or
            a time offset from the start time.
        is_window : `bool`, optional
            If set and the end time is specified as a
            `~astropy.time.TimeDelta`, compute a range centered on the start
            time (default is `False`).
        index : `int`, optional
            For indexed topics set this to the index of the topic to query
            (default is `None`).

        Returns
        -------
        query : `str`
            A string containing the constructed query statement.
        """
        if not isinstance(start, Time):
            raise TypeError('The first time argument must be a time stamp')

        if not start.scale == self.internal_scale:
            logging.warn(f'Timestamps must be in {self.internal_scale.upper()}.  Converting...')
            start = getattr(start, self.internal_scale)

        if isinstance(end, TimeDelta):
            if is_window:
                start_str = (start - end/2).isot
                end_str = (start + end/2).isot
            else:
                start_str = start.isot
                end_str = (start + end).isot
        elif isinstance(end, Time):
            end = getattr(end, self.internal_scale)
            start_str = start.isot
            end_str = end.isot
        else:
            raise TypeError('The second time argument must be the time stamp for the end ' +
                            'or a time delta.')
        index_str = ''
        if index:
            parts = topic_name.split('.')
            index_str = f' AND {parts[-2]}ID = {index}'  # The CSC name is always the penultimate
        timespan = f"time >= '{start_str}Z' AND time <= '{end_str}Z'{index_str}"  # influxdb demands last Z

        if isinstance(fields, str):
            fields = [fields, ]
        elif isinstance(fields, bytes):
            fields = fields.decode()
            fields = [fields, ]

        # Build query here
        return f'SELECT {", ".join(fields)} FROM "{self.db_name}"."autogen"."{topic_name}" WHERE {timespan}'

    async def select_time_series(self, topic_name, fields, start, end, is_window=False, index=None):
        """Select a time series for a set of topics in a single subsystem

        Parameters
        ----------
        topic_name : `str`
            Name of topic to query.
        fields :  `str` or `list`
            Name of field(s) to query.
        start : `astropy.time.Time`
            Start time of the time range, if ``is_window`` is specified,
            this will be the midpoint of the range.
        end : `astropy.time.Time` or `astropy.time.TimeDelta`
            End time of the range either as an absolute time or
            a time offset from the start time.
        is_window : `bool`, optional
            If set and the end time is specified as a
            `~astropy.time.TimeDelta`, compute a range centered on the start
            time (default is `False`).
        index : `int`, optional
            For indexed topics set this to the index of the topic to query
            (default is `None`).

        Returns
        -------
        result : `pandas.DataFrame`
            A `pandas.DataFrame` containing the results of the query.
        """
        query = self.build_time_range_query(topic_name, fields, start, end, is_window, index)
        # Do query
        ret = await self._do_query(query)
        if not isinstance(ret, pd.DataFrame) and not ret:
            # aioinflux returns an empty dict for an empty query
            ret = pd.DataFrame()
        return ret

    async def select_top_n(self, topic_name, fields, num, index=None):
        """Select the most recent N samples from a set of topics in a single subsystem.
        This method does not guarantee sort direction of the returned rows.

        Parameters
        ----------
        topic_name : `str`
            Name of topic to query.
        fields : `str` or `list`
            Name of field(s) to query.
        num : `int`
            Number of rows to return.
        index : `int`, optional
            For indexed topics set this to the index of the topic to query
            (default is `None`)

        Returns
        -------
        result : `pandas.DataFrame`
            A `pandas.DataFrame` containing teh results of the query.
        """

        # The "GROUP BY" is necessary to return the tags
        limit = f"GROUP BY * ORDER BY DESC LIMIT {num}"

        # Deal with index
        istr = ''
        if index:
            parts = topic_name.split('.')
            istr = f' WHERE {parts[-2]}ID = {index}'  # The CSC name is always the penultimate

        if isinstance(fields, str):
            fields = [fields, ]
        elif isinstance(fields, bytes):
            fields = fields.decode()
            fields = [fields, ]

        # Build query here
        query = f'SELECT {", ".join(fields)} FROM "{self.db_name}"."autogen"."{topic_name}"{istr} {limit}'

        # Do query
        ret = await self._do_query(query)
        if not isinstance(ret, pd.DataFrame) and not ret:
            # aioinflux returns an empty dict for an empty query
            ret = pd.DataFrame()
        return ret

    def _make_fields(self, fields, base_fields):
        """Construct the list of fields for a field that
        is the result of ingesting vector data.

        Parameters
        ----------
        fields : `list`
            List of field names to search for vector field names.
        base_fields : `list`
            List of base field names to search the fields list for.

        Returns
        -------
        fields : `tuple`
            Tuple containing a dictionary keyed by the base field
            names with lists of resulting fields from the fields list
            and a single `int` representing number of entries in each
            vector (they must be the same for all base fields).
        """
        ret = {}
        n = None
        for bfield in base_fields:
            for f in fields:
                if f.startswith(bfield) and f[len(bfield):].isdigit():  # Check prefix is complete
                    ret.setdefault(bfield, []).append(f)
            if n is None:
                n = len(ret[bfield])
            if n != len(ret[bfield]):
                raise ValueError(f'Field lengths do not agree for {bfield}: {n} vs. {len(ret[bfield])}')

            def sorter(prefix, val):
                return int(val[len(prefix):])

            part = partial(sorter, bfield)
            ret[bfield].sort(key=part)
        return ret, n

    async def select_packed_time_series(self, topic_name, base_fields, start, end,
                                        is_window=False, index=None, ref_timestamp_col="cRIO_timestamp"):
        """Select fields that are time samples and unpack them into a dataframe.

        Parameters
        ----------
        topic_name : `str`
            Name of topic to query.
        base_fields :  `str` or `list`
            Base field name(s) that will be expanded to query all
            vector entries.
        start : `astropy.time.Time`
            Start time of the time range, if ``is_window`` is specified,
            this will be the midpoint of the range.
        end : `astropy.time.Time` or `astropy.time.TimeDelta`
            End time of the range either as an absolute time or
            a time offset from the start time.
        is_window : `bool`, optional
            If set and the end time is specified as a
            `~astropy.time.TimeDelta`, compute a range centered on the start
            time (default is `False`).
        index : `int`, optional
            For indexed topics set this to the index of the topic to query
            (default is `False`).
        ref_timestamp_col : `str`, optional
            Name of the field name to use to assign timestamps to unpacked
            vector fields (default is 'cRIO_timestamp').

        Returns
        -------
        result : `pandas.DataFrame`
            A `pandas.DataFrame` containing the results of the query.
        """
        fields = await self.get_fields(topic_name)
        if isinstance(base_fields, str):
            base_fields = [base_fields, ]
        elif isinstance(base_fields, bytes):
            base_fields = base_fields.decode()
            base_fields = [base_fields, ]
        qfields, els = self._make_fields(fields, base_fields)
        field_list = []
        for k in qfields:
            field_list += qfields[k]
        result = await self.select_time_series(topic_name, field_list+[ref_timestamp_col, ],
                                               start, end, is_window=is_window, index=index)
        vals = {}
        for f in base_fields:
            df = merge_packed_time_series(result, f, ref_timestamp_col=ref_timestamp_col,
                                          internal_time_scale=self.internal_scale)
            vals[f] = df[f]
        vals.update({'times': df['times']})
        return pd.DataFrame(vals, index=df.index)

    async def get_schema(self, topic):
        """Givent a topic, get a list of dictionaries describing the fields

        Parameters
        ----------
        topic : `str`
            The name of the topic to query.  A full list of valid topic names
            can be obtained using ``get_schema_topics``.

        Returns
        -------
        result : `Pandas.DataFrame`
            A dataframe with the schema information for the topic.  One row per field.
        """
        async with aiohttp.ClientSession() as http_session:
            registry_api = RegistryApi(
                session=http_session, url=self.schema_registry
            )
            schema = await registry_api.get_schema_by_subject(f'{topic}-value')
            return self._parse_schema(topic, schema)

    @staticmethod
    def _parse_schema(topic, schema):
        # A helper function so we can test our parsing
        fields = schema['schema']['fields']
        vals = {'name': [], 'description': [], 'units': [], 'aunits': []}
        for f in fields:
            vals['name'].append(f['name'])
            vals['description'].append(f['description'])
            vals['units'].append(f['units'])
            try:
                if vals['units'][-1] == 'unitless':  # Special case not having units
                    vals['aunits'].append(u.dimensionless_unscaled)
                else:
                    vals['aunits'].append(u.Unit(vals['units'][-1]))
            except (ValueError, TypeError) as e:
                logging.warning(f'Could not construct unist: {e.args[0]}')
                vals['aunits'].append(None)
        return pd.DataFrame(vals)
