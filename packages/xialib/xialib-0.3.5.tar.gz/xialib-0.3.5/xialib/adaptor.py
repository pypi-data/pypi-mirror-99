import abc
import json
import os
import uuid
import base64
import gzip
import logging
from collections import Counter
from xialib.flowers.segment_flower import SegmentFlower
from xialib.storer import RWStorer
from typing import List, Dict, Tuple, Union

__all__ = ['Adaptor', 'DbapiAdaptor', 'DbapiQmarkAdaptor', 'FileAdaptor']


class Adaptor(metaclass=abc.ABCMeta):
    # Constant Definition
    FLEXIBLE_FIELDS = [{}]

    # Segment Compatibility Configuration
    support_add_column = False
    support_alter_column = False
    log_table_meta = {}

    # Standard field definition
    _age_field = {'field_name': '_AGE', 'key_flag': True, 'type_chain': ['int', 'ui_8'],
                  'format': None, 'encode': None, 'default': 0}
    _seq_field = {'field_name': '_SEQ', 'key_flag': True, 'type_chain': ['char', 'c_20'],
                  'format': None, 'encode': None, 'default': '0'*20}
    _no_field = {'field_name': '_NO', 'key_flag': True, 'type_chain': ['int', 'ui_8'],
                 'format': None, 'encode': None, 'default': 0}
    _op_field = {'field_name': '_OP', 'key_flag': False, 'type_chain': ['char', 'c_1'],
                 'format': None, 'encode': None, 'default': ''}

    table_extension = {
        "raw": [],
        "aged": [_age_field, _no_field, _op_field],
        "normal": [_seq_field, _no_field, _op_field],
    }

    def __init__(self, **kwargs):
        """Adaptor for loading databases

        """
        self.logger = logging.getLogger("XIA.Adaptor")
        self.log_context = {'context': ''}
        if len(self.logger.handlers) == 0:
            formatter = logging.Formatter('%(asctime)s-%(process)d-%(thread)d-%(module)s-%(funcName)s-%(levelname)s-'
                                          '%(context)s:%(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def get_log_table_id(self, table_id: str, segment_id: str):
        """ Get log table id from give table id

        Could be implemented by each adaptor, by default, the log table will be named as:
        XIA_<table_name>_<segment_id>. Table name is the last section separated by "."

        Args:
            table_id (:obj:`str`): Table ID
            segment_id (:obj:`str`): Segment ID

        Return:
            (:obj:`str`): log_table_id
        """
        table_path = table_id.split(".")
        if segment_id:
            table_path[-1] = "XIA_" + table_path[-1] + "_" + segment_id
        else:
            table_path[-1] = "XIA_" + table_path[-1]
        return ".".join(table_path)

    # ===DML Section=========
    @abc.abstractmethod
    def append_log_data(self, table_id: str, field_data: List[dict], data: List[dict], **kwargs) -> bool:
        """ To be implemented Public function

        This function will insert x-i-a spec data into the log area without any modification.

        Args:
            table_id (:obj:`str`): Table ID
            field_data (:obj:`list` of `dict`): Table field description
            data (:obj:`list` of :obj:`dict`): Data in Python dictioany list format (spec x-i-a)

        Return:
            True if successful False in the other case

        Note:
            De-duplication must be done during the log load
        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def load_log_data(self, log_table_id: str, table_id: str, field_data: list, start_age: int, end_age: int) -> bool:
        """ To be implemented Public function

        This function will load the data saved in raw table (log usage) into target table.
        Useful only in strong consistency scenario

        Args:
            log_table_id (:obj:`str`): Log Table ID
            table_id (:obj:`str`): Target Table ID
            field_data (:obj:`list` of `dict`): Table field description
            start_age (:obj:`int`): Start Age
            end_age (:obj:`int`): End Age

        Return:
            True if successful False in the other case

        Notes:
            Each segment should has its own log table.

        Warning:
            The insert and delete operation must be an transaction to avoid data duplication
       """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def append_normal_data(self, table_id: str, field_data: List[dict], data: List[dict], type: str, **kwargs) -> bool:
        """ To be implemented Public function

        This function will insert x-i-a spec data into the database without any modification.
        Should be used in eventually consistent scenario (with loading sequence windows function)

        Args:
            table_id (:obj:`str`): Table ID
            field_data (:obj:`list` of `dict`): Table field description
            data (:obj:`list` of :obj:`dict`): Data in Python dictioany list format (spec x-i-a)
            type (:obj:`str`):
                "raw" : No extra fields
                "aged": (_AGE, _NO, _OP)
                "normal": (_SEQ, _NO, _OP)

        Return:
            True if successful False in the other case

        Notes:
            De-duplication is supported natural in the eventually consistent scenario
        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def upsert_data(self, table_id: str, field_data: List[dict], data: List[dict], **kwargs) -> bool:
        """ To be implemented Public function

        This function will get the pushed data and save it to the target database

        Args:
            table_id (:obj:`str`): Table ID
            field_data (:obj:`list` of `dict`): Table field description
            data (:obj:`list` of :obj:`dict`): Data in Python dictioany list format (spec x-i-a)

        Return:
            True if successful False in the other case

        Warning:
            This function should be used in the manual process to adjust data.
            insert_raw_data and load_log_data has covered all use cases
        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def purge_segment(self, table_id: str, meta_data: dict, segment_config: Union[dict, None]) -> bool:
        """Public Function

        Remove segment data from table

        Args:
            table_id (:obj:`str`): Table ID
            meta_data (:obj:`dict`): Table related meta-data, such as Table description / Partition / Clustering
            segment_config (:obj:`dict`): Table Segment Configuration. Truncate all if None

        Return:
            True if successful False in the other case
       """
        raise NotImplementedError  # pragma: no cover

    # # ===DDL Section=========
    @abc.abstractmethod
    def create_table(self, table_id: str, meta_data: dict, field_data: List[dict], type: str) -> bool:
        """Public Function

        Create a table with information provided by header message with specification x-i-a

        Args:
            table_id (:obj:`str`): Table ID to be created
            meta_data (:obj:`dict`): Table related meta-data, such as Table description / Partition / Clustering
            field_data (:obj:`list` of `dict`): Table field description
            type (:obj:`str`):
                "raw" : No extra fields
                "aged": (_AGE, _NO, _OP)
                "normal": (_SEQ, _NO, _OP)

        Return:
            True if successful False in the other case
        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def drop_table(self, table_id: str) -> bool:
        """Public Function

        Drop table

        Warning:
            Drop Table without ANY Check !!! Only useful in the extreme cases !!!

        Args:
            table_id (:obj:`str`): Table ID with format sysid.dbid.schema.table

        Return:
            True if successful False in the other case
       """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def alter_column(self, table_id: str, old_field_line: dict, new_field_line: dict) -> bool:
        """Public Function

        Changing size of an existed column. (if supported by database)

        Args:
            table_id (:obj:`str`): Table ID
            old_field_line (:obj:`dict`): old field
            new_field_line (:obj:`dict`): new field

        Return:
            True if success False in the other case

        Notes:
            If the database support dynamic column size, just return True
        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def add_column(self, table_id: str, new_field_line: dict) -> bool:
        """Public Function

        Add a column to target database. (if supported by database)

        Args:
            table_id (:obj:`str`): Table ID
            new_field_line (:obj:`dict`): new field

        Return:
            True if success False in the other case

        Notes:
            If the database support dynamic column, just return True
        """
        raise NotImplementedError  # pragma: no cover

class DbapiAdaptor(Adaptor):
    """Adaptor for databases supporting PEP249

    Attributes:
        type_dict (:obj:`dict`): field type translator
        create_sql_template (:obj:`str`): create table
        drop_sql_template (:obj:`str`): drop table
        insert_sql_template (:obj:`str`): insert table
        delete_sql_template (:obj:`str`): delete table
        connection (:obj:`Connection`): Connection object defined in PEP249

    """

    type_dict = {}

    # Variable Name: @table_name@, @field_types@, @key_list@
    create_sql_template = "CREATE TABLE {} ( {}, PRIMARY KEY( {} ))"
    # Variable Name: @table_name@
    drop_sql_template = "DROP TABLE {}"
    # Variable Name: @table_name@, @fields@, @value_holders@
    insert_sql_template = "INSERT INTO {} ({}) VALUES ( {} )"
    # Variable Name: @table_name@, @where_key_holders@
    delete_sql_template = "DELETE FROM {} WHERE {}"
    # Variable Name: @tar_table_name@, @log_table_name@, @key_eq_key@, @age_range
    load_del_sql_template = ("DELETE FROM {} WHERE EXISTS ( "
                             "SELECT * FROM {} WHERE {} AND {} AND _OP in ( 'U', 'D' ) )")
    # Variable Name: @tar_table_name@, @field_list@, @field_list@, @key_list@, @log_table_name@, @age_range
    load_ins_sql_template = ("INSERT INTO {} ({}) "
                             "SELECT {} FROM ( "
                             "SELECT *, ROW_NUMBER() OVER (PARTITION BY {} ORDER BY _AGE DESC, _NO DESC) AS row_nb "
                             "FROM {} WHERE {}) "
                             "WHERE row_nb = 1 AND _OP != 'D'")

    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        # Duck type check for db
        if any([not hasattr(db, method) for method in ['cursor', 'close', 'commit']]):
            self.logger.error("connection must an Connection defined by PEP249", extra=self.log_context)
            raise TypeError("XIA-000019")
        else:
            self.connection = db

    # ===DML Section=========
    def append_log_data(self, table_id: str, field_data: List[dict], data: List[dict], **kwargs):
        field_data = field_data.copy()
        field_data.extend(self.table_extension["aged"])
        return self.append_normal_data(table_id, field_data, data, 'aged')

    def load_log_data(self, log_table_id: str, table_id: str, field_data: list, start_age: int, end_age: int):
        load_del_sql = self._get_load_del_sql(log_table_id, table_id, field_data, start_age, end_age)
        load_ins_sql = self._get_load_ins_sql(log_table_id, table_id, field_data, start_age, end_age)
        remove_old_log_sql = self._get_remove_old_log_sql(log_table_id)
        cur = self.connection.cursor()
        try:
            cur.execute(load_del_sql)
            cur.execute(load_ins_sql)
            cur.execute(remove_old_log_sql, (end_age, ))
            self.connection.commit()
            return True
        except Exception as e:  # pragma: no cover
            self.logger.error("SQL Error: {}".format(e), extra=self.log_context)  # pragma: no cover
            return False  # pragma: no cover

    def append_normal_data(self, table_id: str, field_data: List[dict], data: List[dict], type: str, **kwargs):
        field_list = field_data.copy()
        field_list.extend(self.table_extension.get(type))
        cur = self.connection.cursor()
        ins_sql = self._get_insert_sql(table_id, field_data)
        ins_values = self._get_value_tuples(data, field_data)
        try:
            cur.executemany(ins_sql, ins_values)
            self.connection.commit()
            return True
        except Exception as e:  # pragma: no cover
            self.logger.error("SQL Error: {}".format(e), extra=self.log_context)  # pragma: no cover
            return False  # pragma: no cover

    def upsert_data(self, table_id: str, field_data: List[dict], data: List[dict], **kwargs):
        """
        Notes:
            This is a general implementation with delete all and insert all.
            Not a powerful solution but upsert_data shouldn't be used very often
        """
        cur = self.connection.cursor()
        key_list = [item for item in field_data if item['key_flag']]
        del_sql = self._get_delete_sql(table_id, key_list)
        ins_sql = self._get_insert_sql(table_id, field_data)
        del_data = [item for item in data]
        del_vals = self._get_value_tuples(del_data, key_list)
        cur_del_set = set()
        for line in reversed(data):
            key_tuple = tuple([line.get(field['field_name'], None) for field in key_list])
            if key_tuple in cur_del_set:
                line['_OP'] = 'D'
            elif line.get('_OP', '') in ['U', 'D']:
                cur_del_set.add(key_tuple)
        ins_values = self._get_value_tuples([item for item in data if item.get('_OP', '') != 'D'], field_data)
        try:
            cur.executemany(del_sql, del_vals)
            cur.executemany(ins_sql, ins_values)
            self.connection.commit()
            return True
        except Exception as e:  # pragma: no cover
            self.logger.error("SQL Error: {}".format(e), extra=self.log_context)  # pragma: no cover
            return False  # pragma: no cover

    def purge_segment(self, table_id: str, meta_data: dict, segment_config: Union[dict, None]):
        cur = self.connection.cursor()
        if segment_config is None:
            sql = self._get_purge_all_sql(table_id)
            try:
                cur.execute(sql)
                self.connection.commit()
            except Exception as e:  # pragma: no cover
                self.logger.error("SQL Error: {}".format(e), extra=self.log_context)  # pragma: no cover
                return False  # pragma: no cover
        elif 'null' in segment_config or segment_config.get('default', '') is None:
            sql = self._get_purge_null_sql(table_id, segment_config['field_name'])
            try:
                cur.execute(sql)
                self.connection.commit()
            except Exception as e:  # pragma: no cover
                self.logger.error("SQL Error: {}".format(e), extra=self.log_context)  # pragma: no cover
                return False  # pragma: no cover
        elif segment_config.get('list', None):
            sql = self._get_purge_list_sql(table_id, segment_config['field_name'])
            purge_list = segment_config['list'].copy()
            values = [(value, ) for value in purge_list]
            try:
                cur.executemany(sql, values)
                self.connection.commit()
            except Exception as e:  # pragma: no cover
                self.logger.error("SQL Error: {}".format(e), extra=self.log_context)  # pragma: no cover
                return False  # pragma: no cover
        elif 'min' in segment_config or segment_config.get('default', '') is not None:
            min_value = segment_config['min'] if 'min' in segment_config else segment_config['default']
            max_value = segment_config['max'] if 'max' in segment_config else segment_config['default']
            sql = self._get_purge_range_sql(table_id, segment_config['field_name'])
            try:
                cur.execute(sql, (min_value, max_value))
                self.connection.commit()
            except Exception as e:  # pragma: no cover
                self.logger.error("SQL Error: {}".format(e), extra=self.log_context)  # pragma: no cover
                return False  # pragma: no cover
        return True

    # ===DDL Section=========
    def create_table(self, table_id: str, meta_data: dict, field_data: List[dict], type: str):
        field_list = field_data.copy()
        cur = self.connection.cursor()
        sql = self._get_create_sql(table_id, meta_data, field_list, type)
        try:
            cur.execute(sql)
            return True
        except Exception as e:  # pragma: no cover
            self.logger.error("SQL Error: {}".format(e), extra=self.log_context)  # pragma: no cover
            return False  # pragma: no cover

    def drop_table(self, table_id: str, raw_flag: bool = False):
        cur = self.connection.cursor()
        sql = self._get_drop_sql(table_id)
        try:
            cur.execute(sql)
            return True
        except Exception as e:  # pragma: no cover
            self.logger.error("SQL Error: {}".format(e), extra=self.log_context)  # pragma: no cover
            return False  # pragma: no cover

    # ===Tools=========
    def _sql_safe(self, input: str) -> str:
        return input.replace(';', '')

    def _get_key_list(self, field_data: List[dict]) -> str:
        key_list = ", ".join(['"' + field['field_name'] + '"' for field in field_data if field['key_flag']])
        return key_list

    def _get_field_list(self, field_data: List[dict]) -> str:
        field_list = ", ".join(['"' + field['field_name'] + '"' for field in field_data])
        return field_list

    def _get_table_name(self, table_id: str) -> str:
        sysid, db_name, schema, table_name = table_id.split('.')
        table_name = '"' + schema + '"."' + table_name + '"' if schema else '"' + table_name + '"'
        return table_name

    @abc.abstractmethod
    def _get_field_type(self, type_chain: list):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def _get_field_types(self, field_data: List[dict]) -> str:
        """To be implemented Function

        Create table fields definitions,

        Args:
            field_data (:obj:`list` of `dict`): Table field description

        Returns:
            field defintion string: FIELD_A Integer, FIELD_B String, ...
        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def _get_value_holders(self, field_data: List[dict]):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def _get_where_key_holders(self, field_data: List[dict]):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def _get_key_eq_key(self, field_data: List[dict], alias1: str, alias2: str):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def _get_value_tuples(self, data_list: List[dict], field_data: List[dict]):
        raise NotImplementedError  # pragma: no cover

    def _get_create_sql(self, table_id: str, meta_data: dict, field_data: List[dict], type: str):
        field_list = field_data.copy()
        field_list.extend(self.table_extension.get(type))
        return self.create_sql_template.format(self._sql_safe(self._get_table_name(table_id)),
                                               self._sql_safe(self._get_field_types(field_list)),
                                               self._sql_safe(self._get_key_list(field_list)))

    def _get_drop_sql(self, table_id: str):
        return self.drop_sql_template.format(self._sql_safe(self._get_table_name(table_id)))

    def _get_load_del_sql(self, log_table_id: str, table_id: str, field_data: list, start_age: int, end_age: int):
        log_table_name = self._get_table_name(log_table_id)
        tar_table_name = self._get_table_name(table_id)
        age_condition = "_AGE >= {} AND _AGE <= {}".format(start_age, end_age)
        return self.load_del_sql_template.format(self._sql_safe(tar_table_name),
                                                 self._sql_safe(log_table_name),
                                                 self._sql_safe(self._get_key_eq_key(field_data,
                                                                                     tar_table_name,
                                                                                     log_table_name)),
                                                 self._sql_safe(age_condition))

    def _get_load_ins_sql(self, log_table_id: str, table_id: str, field_data: list, start_age: int, end_age: int):
        log_table_name = self._get_table_name(log_table_id)
        tar_table_name = self._get_table_name(table_id)
        age_condition = "_AGE >= {} AND _AGE <= {}".format(start_age, end_age)
        return self.load_ins_sql_template.format(self._sql_safe(tar_table_name),
                                                 self._sql_safe(self._get_field_list(field_data)),
                                                 self._sql_safe(self._get_field_list(field_data)),
                                                 self._sql_safe(self._get_key_list(field_data)),
                                                 self._sql_safe(log_table_name),
                                                 self._sql_safe(age_condition))

    @abc.abstractmethod
    def _get_insert_sql(self, table_id: str, field_data: List[dict]):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def _get_delete_sql(self, table_id: str, key_field_data: List[dict]):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def _get_purge_all_sql(self, table_id: str):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def _get_purge_null_sql(self, table_id: str, field_name: str):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def _get_purge_list_sql(self, table_id: str, field_name: str):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def _get_purge_range_sql(self, table_id: str, field_name: str):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def _get_remove_old_log_sql(self, log_table_id: str):
        raise NotImplementedError  # pragma: no cover


class DbapiQmarkAdaptor(DbapiAdaptor):
    """Adaptor for databases supporting PEP 249 with paramstyple qmark

    """
    def _get_value_holders(self, field_data: List[dict]):
        value_holders = ', '.join(['?' for field in field_data])
        return value_holders

    def _get_where_key_holders(self, field_data: List[dict]):
        where_key_holders = ' AND '.join(['"' + field['field_name'] + '" = ?' for field in field_data])
        return where_key_holders

    def _get_key_eq_key(self, field_data: List[dict], alias1: str, alias2: str):
        where_key_holders = ' AND '.join([alias1 + '."' + field['field_name'] + '" = ' +
                                          alias2 + '."' + field['field_name'] + '"'
                                            for field in field_data if field['key_flag']])
        return where_key_holders

    def _get_value_tuples(self, data_list: List[dict], field_data: List[dict]):
        value_tuples = list()
        for line in data_list:
            value_tuples.append(tuple([line.get(field['field_name'], field.get('default', None))
                                       for field in field_data]))
        return value_tuples

    def _get_insert_sql(self, table_id: str, field_data: List[dict]):
        return self.insert_sql_template.format(self._sql_safe(self._get_table_name(table_id)),
                                               self._sql_safe(self._get_field_list(field_data)),
                                               self._sql_safe(self._get_value_holders(field_data)))

    def _get_delete_sql(self, table_id: str, key_field_data: List[dict]):
        return self.delete_sql_template.format(self._sql_safe(self._get_table_name(table_id)),
                                               self._sql_safe(self._get_where_key_holders(key_field_data)))

    def _get_purge_all_sql(self, table_id: str):
        return self.delete_sql_template.format(self._sql_safe(self._get_table_name(table_id)),
                                               '1=1')

    def _get_purge_null_sql(self, table_id: str, field_name: str):
        return self.delete_sql_template.format(self._sql_safe(self._get_table_name(table_id)),
                                               self._sql_safe(field_name + ' IS NULL'))

    def _get_purge_list_sql(self, table_id: str, field_name: str):
        return self.delete_sql_template.format(self._sql_safe(self._get_table_name(table_id)),
                                               self._sql_safe(field_name + ' = ?'))

    def _get_purge_range_sql(self, table_id: str, field_name: str):
        return self.delete_sql_template.format(self._sql_safe(self._get_table_name(table_id)),
                                               self._sql_safe(field_name + ' >= ?' + ' AND ' +
                                                              field_name + ' <= ?'))

    def _get_remove_old_log_sql(self, log_table_id: str):
        return self.delete_sql_template.format(self._sql_safe(self._get_table_name(log_table_id)),
                                               self._sql_safe('_AGE <= ?'))


class FileAdaptor(Adaptor):
    """Adaptor for exporting data to files

    No predefined structure, each message will be translated into two file: Insert File and Delete File
    """
    def __init__(self, fs: RWStorer, location: str, **kwargs):
        super().__init__(**kwargs)
        if not isinstance(fs, RWStorer):
            self.logger.error("File Adapter needs a RWStorer", extra=self.log_context)
            raise TypeError("XIA-000030")
        if not fs.exists(location):
            self.logger.error("Location {} does not exists".format(location), extra=self.log_context)
            raise TypeError("XIA-000031")
        else:
            self.storer = fs
            self.location = location

    @abc.abstractmethod
    def _write_content(self, file_path: str, data: List[dict]):
        """Write Data to file

        Args:
            file_path (:obj:`str`): File Path to Write Data
            data (:obj:`list` of :obj:`dict`): Data in Python dictioany list format (spec x-i-a)
        """
        raise NotImplementedError  # pragma: no cover

    def append_log_data(self, table_id: str, field_data: List[dict], data: List[dict], **kwargs):
        check_d, check_i = dict(), dict()
        file_name = self._get_file_name(data)
        table_path = [i if i else "default" for i in table_id.split(".")]
        data = sorted(data, key=lambda k: (k.get('_AGE', None), k.get('_NO', None)), reverse=True)
        key_list = [item['field_name'] for item in field_data if item['key_flag']]
        for i in range(len(data)):
            line = data.pop()
            key_descr = self._get_key_from_line(key_list, line)
            if line.get('_OP', 'I') == 'I':
                line.pop('_OP', None)
                line.pop('_AGE', None)
                line.pop('_NO', None)
                check_i[key_descr] = line
                check_d.pop(key_descr, None)
            elif line.get('_OP', 'I') == 'D':
                check_d[key_descr] = ''
                check_i.pop(key_descr, None)
            elif line.get('_OP', 'I') == 'U':
                line.pop('_OP', None)
                line.pop('_AGE', None)
                line.pop('_NO', None)
                check_i[key_descr] = line
                check_d[key_descr] = ''
        if check_d:
            d_file_name = self.storer.join(self.location, *table_path, file_name + '-D')
            d_content = [{key: value for key, value in zip(key_list, line)} for line in check_d]
            self._write_content(d_file_name, d_content)
        if check_i:
            i_file_name = self.storer.join(self.location, *table_path, file_name + '-I')
            i_content = [value for key, value in check_i.items()]
            self._write_content(i_file_name, i_content)
        return True

    def load_log_data(self, log_table_id: str, table_id: str, field_data: list, start_age: int, end_age: int):
        """Copying files from log table location into table location
        """
        log_table_path = [i if i else "default" for i in log_table_id.split(".")]
        table_path = [i if i else "default" for i in table_id.split(".")]
        start_file_name = str(start_age).zfill(20)
        end_file_name = str(end_age).zfill(20)
        for full_path in self.storer.walk_file(self.storer.join(self.location, *log_table_path)):
            file_name = full_path.split(self.storer.path_separator)[-1]
            file_prefix = file_name[:20]
            if start_file_name <= file_prefix <= end_file_name:
                for data_io in self.storer.get_io_stream(full_path):
                    self.storer.write(data_io, self.storer.join(self.location, *table_path, file_name))
        return True  # pragma: no cover

    def append_normal_data(self, table_id: str, field_data: List[dict], data: List[dict], type: str, **kwargs):
        table_path = [i if i else "default" for i in table_id.split(".")]
        file_name = self._get_file_name(data)
        file_path = self.storer.join(self.location, *table_path, file_name)
        self._write_content(file_path, data)
        return True

    def upsert_data(self, table_id: str, field_data: List[dict], data: List[dict], **kwargs):
        return self.append_normal_data(table_id, field_data, data, "raw")

    def purge_segment(self, table_id: str, meta_data: dict, segment_config: Union[dict, None]):
        table_path = [i if i else "default" for i in table_id.split(".")]
        for file_path in self.storer.walk_file(self.storer.join(self.location, *table_path)):
            self.storer.remove(file_path)
        return True

    def create_table(self, table_id: str, meta_data: dict, field_data: List[dict], type: str):
        table_path = [i if i else "default" for i in table_id.split(".")]
        if not self.storer.exists(self.storer.join(self.location, *table_path)):
            self.storer.mkdir(self.storer.join(self.location, *table_path))  # pragma: no cover
        return True

    def drop_table(self, table_id: str):
        self.purge_segment(table_id, {}, None)
        return True

    def alter_column(self, table_id: str, old_field_line: dict, new_field_line: dict):
        return True  # pragma: no cover

    def add_column(self, table_id: str, new_field_line: dict):
        return True  # pragma: no cover

    def _get_file_name(self, data: List[dict]):
        min_age, min_seq = min([(int(line.get('_AGE', 0)), line.get('_SEQ', '')) for line in data])
        return str(min_age).zfill(20) if min_age > 0 else min_seq

    def _get_key_from_line(self, field_list: List[str], line: dict) -> Tuple:
        return_list = list()
        for key in field_list:
            if key in line:
                return_list.append(line[key])
            else:  # pragma: no cover
                return_list.append(None)  # pragma: no cover
        return tuple(return_list)



