from db.db_operations import fetchall_from_single_table, update_single_table
from db.models.table_model import TableModel
import logging

logger = logging.getLogger(__name__)

table_name = "vip_users"

class VipUsersService:
    @staticmethod
    def get_user_by_user_id(user_id):
        """
        通过user_id查找用户数据
        :param user_id:
        :return: Optional[TableModel]
        """
        users_data_list = fetchall_from_single_table(table_name, selected_columns=["tag"], user_id=user_id)

        if not users_data_list:
            logger.error(f"没有找到用户数据：user_id={user_id}")
            return None
        elif len(users_data_list) != 1:
            logger.error(f"找到多条用户数据：user_id={user_id}")
            return None

        # 转换为VipUser对象
        return TableModel.from_dict(users_data_list[0])


    @staticmethod
    def set_user_tag_by_user_id(user_id, tag) -> int:
        """
        修改user_id用户的tag值，应该只有1条数据！
        :param user_id:
        :param tag:
        :return: int
        """
        updated_count = update_single_table(table_name, columns_to_update={"tag": tag}, user_id=user_id)

        if updated_count != 1:
            logger.warning(f"更新{updated_count}条用户数据: user_id={user_id}")
        else:
            logger.info(f"更新1条用户数据: user_id={user_id}")

        return updated_count