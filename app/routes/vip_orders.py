from flask import Blueprint, jsonify
from utilities.time_utilities import is_within_timestamp_interval, set_timestamp
from db.vip_orders_table import get_orders_from_db, update_order


vip_orders_bp = Blueprint("vip_orders", __name__)

interval_time = 10

@vip_orders_bp.route("/check_order_by_create_time/<string:open_id>/<int:product_id>/", methods=["GET"])
def check_order_by_create_time(open_id, product_id):
    """
    检查在固定时间（10s）内，是否有对应的支付订单生成
    :param open_id:
    :param product_id:
    :return:
    """
    orders = get_orders_from_db(selected_columns=["id", "create_time"], order_by={"create_time": "DESC"},
                                openid=open_id, product_id=product_id)

    create_time = orders[0].get("create_time")
    res = is_within_timestamp_interval(create_time, interval_time, unit="seconds")

    message = ""
    if res:
        order_id = orders[0].get("id")
        message = f"数据库中成功生成订单数据"
        print(message)
        return jsonify({"message": message,
                        "order_id": order_id,
                        "create_time": create_time,
                        "re": True})
    else:
        message = f"Err，数据库中没有生成订单数据"
        print(message)
        return jsonify({"message": message,
                        "order_id": None,
                        "create_time": None,
                        "re": False})


@vip_orders_bp.route("/set_order_purchased/<int:order_id>/", methods=["GET"])
def set_order_purchased(order_id):
    """
    修改订单为成功支付状态：status=8，pay_status=1
    :param order_id: 订单id
    :return:
    """
    updated_count = update_order(columns_to_update={"status": 8, "pay_status": 1}, id=order_id)

    if updated_count > 0:
        message = f"成功修改{updated_count}条数据"
        print(message)
        return jsonify({"message": message,
                        "re": True})
    else:
        message = f"没有修改任何数据！"
        print(message)
        return jsonify({"message": message,
                        "re": False}), 404

@vip_orders_bp.route("/set_order_available/<int:order_id>/<int:create_time_before>/", methods=["GET"])
def set_order_available(order_id, create_time_before):
    """
    修改订单create_time为为N（7）   天前，模拟每周限购解除
    :param order_id: 订单id
    :param create_time_before: 订单当前create_time
    :return:
    """
    create_time_after = set_timestamp(create_time_before, 7, unit="days", direction="backward")

    updated_count = update_order(columns_to_update={"create_time": create_time_after}, id=order_id)
    if updated_count > 0:
        message = f"成功修改{updated_count}条数据的create_time"
        print(message)
        return jsonify({"message": message,
                        "re": True})
    else:
        message = f"没有修改任何数据的create_time"
        print(message)
        return jsonify({"message": message,
                        "re": False}), 404


# @vip_orders_bp.route("/set_all_orders_purchased/<string:open_id>/", methods=["GET"])
# def set_all_orders_purchased(open_id):
#     re = get_orders_from_db(selected_columns=["id", "create_time"], )



if __name__ == '__main__':
    from run import app

    with app.app_context():
        # check_order_by_create_time("okorF5pMFuTJ3K4Q5IztHeHkxSIg", 418)
        set_order_available(1518, 1692160434)


    # orders = get_orders_from_db(selected_columns=["id"], order_by={"create_time": "DESC"},
    #                             openid="okorF5pMFuTJ3K4Q5IztHeHkxSIg")


