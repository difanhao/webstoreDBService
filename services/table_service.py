import logging

from db.db_operations import delete_from_single_table

logger = logging.getLogger(__name__)

class TableService:

    table_name = None

    @classmethod
    def delete_data(cls, **filters):
        if cls.table_name is None:
            raise ValueError("子类中必须定义table_name!")

        deleted_rows = delete_from_single_table(cls.table_name, **filters)
        logger.info(f"删除{deleted_rows}行数据")
        return deleted_rows

