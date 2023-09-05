from flask import Blueprint, jsonify
from services.vip_users_table_service import VipUsersService


vip_users_bp = Blueprint("vip_users", __name__)

@vip_users_bp.route("/edit_tag/<int:user_id>/<string:tag>/", methods=["GET"])
def edit_tag(user_id, tag):
    """
    设置user_id用户的tag值
    :param user_id:
    :param tag:
    :return:
    """
    user = VipUsersService.get_user_by_user_id(user_id)

    if not user:
        message = "Error 用户数据错误！"
        return jsonify({"message": message,
                        "re": False})

    if user.tag == tag:
        message = f"OK 用户(user_id={user_id})的tag值已经是{tag}，无需修改"
        return jsonify({"message": message,
                        "re": True})

    else:  # 修改tag值
        set_count = VipUsersService.set_user_tag_by_user_id(user_id, tag)
        if set_count == 1:
            message = f"OK 用户(user_id={user_id})的tag值已被修改为{tag}"
            return jsonify({"message": message,
                            "re": True})
        else:
            message = f"Error 修改数据时发生错误"
            return jsonify({"message": message,
                            "re": False})


