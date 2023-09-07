import logging

from db.db_operations import fetchall_from_single_table
from db.models.table_model import TableModel
from services.table_service import TableService

logger = logging.getLogger(__name__)


class ActivityInfoTableService(TableService):
    table_name = "activity_info"

    @classmethod
    def get_activity_start_time(cls, activity_id):
        """
        获取活动开始时间
        :param activity_id:
        :return: datetime.datetime(2023, 8, 28, 0, 0)
        """
        start_time_list = fetchall_from_single_table(cls.table_name, selected_columns=["start_time", ], id=activity_id)

        if not start_time_list:
            logger.warning(f"没有找到活动数据：id={activity_id}")
            return None
        elif len(start_time_list) != 1:
            logger.error(f"找到多条活动数据：id={activity_id}")
            return None

        return start_time_list[0]["start_time"]

    @classmethod
    def get_activity_end_time(cls, activity_id):
        """
        获取活动结束时间
        :param activity_id:
        :return: datetime.datetime(2023, 8, 28, 0, 0)
        """
        end_time_list = fetchall_from_single_table(cls.table_name, selected_columns=["end_time", ], id=activity_id)

        if not end_time_list:
            logger.warning(f"没有找到活动数据：id={activity_id}")
            return None
        elif len(end_time_list) != 1:
            logger.error(f"找到多条活动数据：id={activity_id}")
            return None

        return end_time_list[0]["end_time"]