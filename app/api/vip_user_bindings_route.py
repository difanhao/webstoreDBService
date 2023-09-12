from flask import Blueprint, jsonify
from services.vip_user_bindings_table_service import VipUserBindingsTableService


vip_user_bindings_bp = Blueprint("vip_user_bindings", __name__)

@vip_user_bindings_bp.route("/bind_phone/<open_id>/<phone_number>/", methods=["POST"])
def bind_phone(open_id, phone_number):
    """
    绑定用户手机号
    :param open_id:
    :param phone_number:
    :return:
    """

    VipUserBindingsTableService.create_user_binding(open_id, phone_number)

    message = "OK"
    return jsonify({"message": message,
                    "re": True})


@vip_user_bindings_bp.route("/unbind_phone/<open_id>", methods=["DELETE"])
def unbind_phone(open_id):
    """
    绑定用户手机号
    :param open_id:
    :return:
    """

    VipUserBindingsTableService.cancel_user_binding(open_id)

    message = "OK"
    return jsonify({"message": message,
                    "re": True})




