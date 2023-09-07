from db.db_operations import fetchall_from_single_table, update_single_table, direct_fetchall
from db.models.table_model import TableModel
from utilities.time_utilities import is_within_timestamp_interval, set_timestamp
import logging
import time

logger = logging.getLogger(__name__)


interval_time = 10000  # 毫秒

class VipOrdersTableService:
    table_name = "vip_orders"

    @classmethod
    def check_order_in_interval_time(cls, open_id, product_id):
        """
        检查在固定时间（10s）内，是否有对应的支付订单生成
        通过openid、product_id查找订单数据，应该只有一条数据！
        :param open_id:
        :param product_id:
        :return: Optional[TableModel]
        """
        orders_data = fetchall_from_single_table(cls.table_name, selected_columns=["id", "create_time"], order_by={"create_time": "DESC"},
                                openid=open_id, product_id=product_id)

        if not orders_data:
            logger.warning(f"没有找到订单数据：openid={open_id}, product_id={product_id}")
            return None
        elif len(orders_data) != 1:
            logger.error(f"找到多条订单数据：openid={open_id}, product_id={product_id}")
            return None

        order_dict = orders_data[0]
        create_time = order_dict.get("create_time")

        result = is_within_timestamp_interval(create_time, interval_time, unit="seconds")
        if result:
            return TableModel.from_dict(order_dict)
        else:
            logger.warning(f"订单(openid={open_id}, product_id={product_id})"
                           f"的create_time据当前时间>{interval_time}秒")
            return None


    @classmethod
    def set_purchased(cls, order_id) -> int:
        """
        设置订单为成功支付状态，status=8，pay_status=1，应该只有1条
        :param order_id:
        :return: int
        """
        updated_count = update_single_table(cls.table_name, columns_to_update={"status": 8, "pay_status": 1}, id=order_id)

        if updated_count != 1:
            logger.warning(f"更新{updated_count}条订单数据: id={order_id}")
        else:
            logger.info(f"更新1条订单数据: id={order_id}")

        return updated_count

    @classmethod
    def unfreeze_purchase(cls, open_id) -> int:
        """
        标签（tab）商品的每周限购解：create_time改为7天前
        :param open_id:
        :return: int
        """

        orders = fetchall_from_single_table(cls.table_name, selected_columns=["id", "create_time"], order_by={"create_time": "DESC"}, openid=open_id, status=8, pay_status=1)

        # 把当前时间向前推7天
        time_stamp_7_days_before = set_timestamp(time.time(), 7, unit="days", direction="backward")
        filtered_orders = [order for order in orders if order.get("create_time") > time_stamp_7_days_before]

        try:
            for order in filtered_orders:
                id = order.get("id")
                updated_count = update_single_table(cls.table_name, columns_to_update={"create_time": time_stamp_7_days_before}, id=id)

                if updated_count != 1:
                    logger.warning(f"更新{updated_count}条订单数据: id={id}")
                else:
                    logger.info(f"更新1条订单数据: id={id}")
        except Exception as e:
            # TODO:添加异常处理
            raise e

        return True


    @classmethod
    def advance_create_time_of_successful_order(cls, open_id, start_timestamp, end_timestamp):
        """
        将某用户的create_time值在timestamp之后的成功订单的create_time提前为timestamp之前
        :param end_timestamp:
        :param open_id:
        :param start_timestamp:
        :return:
        """
        # TODO
        query = f"SELECT id FROM {cls.table_name} where openid='{open_id}' and status=8 and pay_status=1 " \
                f"and create_time>={start_timestamp} and create_time<={end_timestamp} order by id desc"
        # [{'id': 1581}, ]
        order_data = direct_fetchall(query)

        if not order_data:
            logger.warning(f"没有找到订单数据")
            return

        advanced_timestamp = set_timestamp(start_timestamp, 1, unit="days", direction="backward")

        # TODO
        for i in range(len(order_data)):
            update_single_table(cls.table_name, columns_to_update={"create_time": advanced_timestamp}, id=order_data[i]["id"])

    @classmethod
    def set_real_price_of_successful_order_during_activity_time(cls, open_id, start_timestamp, end_timestamp, price):
        """
        将某用户的create_time值在timestamp之后的成功订单的create_time提前为timestamp之前
        :param end_timestamp:
        :param price:
        :param open_id:
        :param start_timestamp:
        :return:
        """
        # TODO create_time大于等于活动开始时间，小于等于活动结束时间
        # TODO 对sql返回的处理 如打印日志
        # 1 先找有没有活动期间内的成功订单
        query = f"SELECT id FROM {cls.table_name} where openid='{open_id}' and status=8 and pay_status=1 " \
                f"and create_time>={start_timestamp} and create_time<={end_timestamp} order by id desc"
        # [{'id': 1581}, ]
        orders = direct_fetchall(query)

        if orders:
            # 取最近的订单，修改其real_price
            target_order_id = orders[0]["id"]
            update_single_table(cls.table_name, columns_to_update={"real_price": price}, id=target_order_id)
            # TODO return
            return

        logger.warning(f"1 没有找到活动期内的成功订单数据")

        new_create_time = set_timestamp(start_timestamp, 1, unit="days", direction="forward")

        # 2 再找最近的一次成功订单
        orders_data = fetchall_from_single_table(cls.table_name, selected_columns=["id", ], order_by={"id": "DESC"},
                                                 openid=open_id, status=8, pay_status=1)

        if orders_data:
            targ_order_id = orders_data[0]["id"]
            update_single_table(cls.table_name, columns_to_update={"create_time": new_create_time, "real_price": price}, id=targ_order_id)
            # TODO return
            return

        logger.warning(f"2 没有找到任何成功订单数据")

        # 3 将最近一笔的订单，进行修改
        orders_data_list = fetchall_from_single_table(cls.table_name, selected_columns=["id", ], order_by={"id": "DESC"}, openid=open_id)
        tar_order_id = orders_data_list[0]["id"]
        update_single_table(cls.table_name, columns_to_update={"status": 8, "pay_status": 1, "create_time": new_create_time, "real_price": price}, id=tar_order_id)




