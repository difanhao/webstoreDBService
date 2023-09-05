from flask import Blueprint, jsonify
from services.vip_orders_table_service import VipOrdersService


vip_orders_bp = Blueprint("vip_orders", __name__)

@vip_orders_bp.route("/check_order_generation/<string:open_id>/<int:product_id>/", methods=["GET"])
def check_order_generation(open_id, product_id):
    """
    检查是否有对应的支付订单生成
    :param open_id:
    :param product_id:
    :return: order_id
    """
    vip_order_obj = VipOrdersService.check_order_in_interval_time(open_id, product_id)

    if vip_order_obj is None:
        message = f"Error 订单数据错误！"
        return jsonify({"message": message,
                        "order_id": None,
                        "create_time": None,
                        "re": False})

    message = f"OK 成功生成订单数据"
    return jsonify({"message": message,
                    "order_id": vip_order_obj.id,
                    "create_time": vip_order_obj.create_time,
                    "re": True})


@vip_orders_bp.route("/set_order_purchased/<int:order_id>/", methods=["GET"])
def set_order_purchased(order_id):
    """
    修改订单为成功支付状态
    :param order_id: 订单id
    :return:
    """
    set_count = VipOrdersService.set_purchased(order_id)

    if set_count == 1:
        message = f"OK 成功修改订单(order_id={order_id})为 成功支付 状态"
        return jsonify({"message": message,
                        "re": True})
    else:
        message = f"Error 修改数据时发生错误"
        return jsonify({"message": message,
                        "re": False})


@vip_orders_bp.route("/set_order_available/<string:open_id>/", methods=["GET"])
def set_order_available(open_id):
    """
    解除微信open_id用户 对标签商品的购买限制
    :param open_id:
    :return:
    """
    re = VipOrdersService.unfreeze_purchase(open_id)
    if re:
        message = f"OK 成功解除用户(open_id={open_id})的标签商品购买限制"
        return jsonify({"message": message,
                        "re": True})
    else:
        message = f"Error 修改数据时发生错误"
        return jsonify({"message": message,
                        "re": False})



if __name__ == '__main__':
    from run import app

    with app.app_context():
        # check_order_by_create_time("okorF5pMFuTJ3K4Q5IztHeHkxSIg", 418)
        set_order_available(1518, 1692160434)


    # orders = get_orders_from_db(selected_columns=["id"], order_by={"create_time": "DESC"},
    #                             openid="okorF5pMFuTJ3K4Q5IztHeHkxSIg")


