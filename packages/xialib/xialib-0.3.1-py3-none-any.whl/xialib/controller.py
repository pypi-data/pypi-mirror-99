import abc
import logging
from datetime import datetime
from typing import List

__all__ = ['Controller']


class Controller():
    """XIA Controller

    Aim to provide a general solution to handle meta-data, field-data, age data flow

    Attributes:
        ctrl_key (:obj:`int`): The control information will be saved in this document
        min_frame_length (:obj:`int`): Minimum possible frame lenght.

    Notes:
        Normally, each Agent should have its dedicated controller

    Notes:
        Each document should has its own target table id, segment id and start seq
    """
    def __init__(self, ctrl_key: str = '_XIA', min_frame_length: int = 0):
        self.logger = logging.getLogger("XIA.Controller")
        self.log_context = {'context': ''}
        if len(self.logger.handlers) == 0:
            formatter = logging.Formatter('%(asctime)s-%(process)d-%(thread)d-%(module)s-%(funcName)s-%(levelname)s-'
                                          '%(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        self.ctrl_key = ctrl_key
        self.min_fram_length = min_frame_length

    @classmethod
    def age_list_add_item(cls, age_list: List[list], item: list) -> List[list]:
        new_age_list, cur_item, start_point = list(), item.copy(), None
        for list_item in age_list:
            # <List Item> --- <New Item>
            if list_item[1] + 1 < cur_item[0]:
                new_age_list.append(list_item)
            # <New Item> --- <List Item>
            elif cur_item[1] + 1 < list_item[0]:
                new_age_list.append(cur_item)
                cur_item = list_item.copy()
            # <New Item && List Item>
            else:
                cur_item = [min(cur_item[0], list_item[0]), max(cur_item[1], list_item[1])]
        new_age_list.append(cur_item)
        return new_age_list

    @classmethod
    def get_frame_id(cls, frame_length: int = 0, ts: int = 0):
        """Get the current frame_id

        Attributes:
            frame_length (:obj:`int`): Length of frame (seconds)

        Note:
            frame_id is the last timestamp of frame
        """
        ts = ts if ts else int(datetime.timestamp(datetime.now()))
        if frame_length <= 1:
            return datetime.fromtimestamp(ts).strftime("%Y%m%d%H%M%S")
        frame_ts = (((ts - 1) // frame_length) + 1) * frame_length
        return datetime.fromtimestamp(frame_ts).strftime("%Y%m%d%H%M%S")

    @abc.abstractmethod
    def key_init(self, key: str, ctrl_info: dict, frame_length: int = 0):
        """Creating Ager Object for requested keys

        Args:
            key (:obj:`str`): object key (key should unique per Target Table, Segment ID and Start Seq)
            ctrl (:obj:`dict`): Should contains all ctrl infomation: target table id, segment id, source id,
            start seq, log table id, table meta data and field list
            frame_length (:obj:`int`): Data should be update every x seconds. Default 0 = Realtime
        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def get_table_info_all(self, table_id: str):
        """Get All activate table information

        Args:
            table_id (:obj:`str`): Table ID

        Return:
            (:obj:`dict`): {segment_id: ctrl_info}
        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def get_ready_task(self, key: str, start_key: int = 0, end_key: int = 0) -> str:
        """Adding age range and get the last ready key

        Attributes:
            key (:obj:`str`): object key (key should contains Target Topic, Target Table, Segment ID)
            start_key (:obj:`int`): new input start merge key
            end_key (:obj:`int`): new input end merge key

        Notes:
            If start_key == end_key == 0 : Just return the last ready key

        Return:
            :obj:`dict`: task which is ready to be loaded (No GAP from beginning).
                Key list: start_key, end_key, log_table_id, table_id, field_list

        Notes:
            All operations must be multi-process safe (Increment for No-SQL or Transactional)
        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def get_update_tasks(self, start_frame: int = 0, end_frame: int = 0) -> dict:
        """Get keys to be updated after the last update time

        Attributes:
            start_frame (:obj:`int`): by default is the last loaded frame
            end_frame (:obj:`int`): by default is the current timestamp

        Return:
            :obj:`dict`: key: Dict with: start_key, end_key, log_table_id, table_id, field_list

        Notes:
            The operation of the control needn't to be multi-processing safe.
            The uniqueness of global update task run will be controlled by scheduler
        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def get_ctrl_info(self, key: str):
        """Get Control information from given key

        Attributes:
            key (:obj:`str`): object key (key should contains Target Topic, Target Table, Segment ID)
        """
        raise NotImplementedError  # pragma: no cover