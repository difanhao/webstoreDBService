from db.vip_orders_table import get_orders_from_db, update_order
from db.models.vip_order_model import VipOrder
from utilities.time_utilities import is_within_timestamp_interval, set_timestamp
import logging
import time

logger = logging.getLogger(__name__)

interval_time = 10000

class VipOrdersService:
    @staticmethod
    def check_order_in_interval_time(open_id, product_id):
        """
        检查在固定时间（10s）内，是否有对应的支付订单生成
        通过openid、product_id查找订单数据，应该只有一条数据！
        :param open_id:
        :param product_id:
        :return: VipOrder or None
        """
        orders_data = get_orders_from_db(selected_columns=["id", "create_time"], order_by={"create_time": "DESC"},
                                openid=open_id, product_id=product_id)

        if not orders_data:
            logger.warning(f"没有找到订单数据：openid={open_id}, product_id:{product_id}")
            return None
        elif len(orders_data) != 1:
            logger.error(f"找到多条订单数据：openid={open_id}, product_id:{product_id}")
            return None

        order_dict = orders_data[0]
        create_time = order_dict.get("create_time")

        result = is_within_timestamp_interval(create_time, interval_time, unit="seconds")
        if result:
            return VipOrder.from_dict(order_dict)
        else:
            logger.warning(f"订单(openid={open_id}, product_id:{product_id})"
                           f"的create_time据当前时间>{interval_time}秒")
            return None


    @staticmethod
    def set_purchased(order_id) -> int:
        """
        设置订单为成功支付状态，status=8，pay_status=1，应该只有1条
        :param order_id:
        :return: int
        """
        updated_count = update_order(columns_to_update={"status": 8, "pay_status": 1}, id=order_id)

        if updated_count != 1:
            logger.warning(f"更新{updated_count}条订单数据: id={order_id}")
        else:
            logger.info(f"更新1条订单数据: id={order_id}")

        return updated_count

    @staticmethod
    def unfreeze_purchase(order_id, create_time_before) -> int:
        """
        tab商品的每周限购解：create_time改为7天前，应该只有1条
        :param order_id:
        :param create_time_before:
        :return: int
        """
        create_time_after = set_timestamp(create_time_before, 7, unit="days", direction="backward")

        updated_count = update_order(columns_to_update={"create_time": create_time_after}, id=order_id)
        if updated_count != 1:
            logger.warning(f"更新{updated_count}条订单数据: id={order_id}")
        else:
            logger.info(f"更新1条订单数据: id={order_id}")

        return updated_count

    @staticmethod
    def unfreeze_purchase2(open_id) -> int:
        """
        标签（tab）商品的每周限购解：create_time改为7天前
        :param open_id:
        :return: int
        """

        orders = get_orders_from_db(selected_columns=["id", "create_time"], order_by={"create_time": "DESC"}, openid=open_id, status=8, pay_status=1)

        # 把当前时间向前推7天
        time_stamp_7_days_before = set_timestamp(time.time(), 7, unit="days", direction="backward")
        filtered_orders = [order for order in orders if order.get("create_time") > time_stamp_7_days_before]

        try:
            for order in filtered_orders:
                id = order.get("id")
                updated_count = update_order(columns_to_update={"create_time": time_stamp_7_days_before}, id=id)

                if updated_count != 1:
                    logger.warning(f"更新{updated_count}条订单数据: id={id}")
                else:
                    logger.info(f"更新1条订单数据: id={id}")
        except Exception as e:
            # TODO:添加异常处理
            raise e

        return True