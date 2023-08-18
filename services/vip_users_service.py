from db.vip_users_table import get_users_from_db, update_user
from db.models.vip_user_model import VipUser
import logging

logger = logging.getLogger(__name__)

class VipUsersService:
    @staticmethod
    def get_user_by_user_id(user_id) -> VipUser:
        """
        通过user_id查找订单数据，应该只有一条数据！
        :param user_id:
        :return: VipUser or None
        """
        users_data = get_users_from_db(selected_columns=["tag"], user_id=user_id)

        if not users_data:
            logger.warning(f"没有找到订单数据：user_id={user_id}")
            return None
        elif len(users_data) != 1:
            logger.error(f"找到多条订单数据：user_id={user_id}")
            return None

        # 转换为VipUser对象
        return VipUser.from_dict(users_data[0])


    @staticmethod
    def set_user_tag_by_user_id(user_id, tag) -> int:
        """
        修改user_id用户的tag值，应该只有1条数据！
        :param user_id:
        :param tag:
        :return: int
        """
        updated_count = update_user(columns_to_update={"tag": tag}, user_id=user_id)

        if updated_count != 1:
            logger.warning(f"更新{updated_count}条用户数据: user_id={user_id}")
        else:
            logger.info(f"更新1条用户数据: user_id={user_id}")

        return updated_count