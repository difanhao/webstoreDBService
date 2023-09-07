import logging

from db.db_operations import insert_into_single_table
from services.table_service import TableService

logger = logging.getLogger(__name__)


class VipUserBindingsTableService(TableService):

    table_name = "vip_user_bindings"

    @classmethod
    def create_user_binding(cls, open_id, phone_number):
        rows = insert_into_single_table(cls.table_name, columns_to_insert={"open_id": open_id, "phone": phone_number})
        logger.info(f"插入{rows}行数据")