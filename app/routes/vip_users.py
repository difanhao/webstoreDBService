from flask import Blueprint, jsonify
from db.vip_users_table import get_user_tag_by_user_id, update_user_tag_by_user_id


vip_users_bp = Blueprint("vip_users", __name__)

@vip_users_bp.route("/edit_tag/<int:user_id>/<string:tag>/", methods=["GET"])
def edit_tag(user_id, tag):
    user = get_user_tag_by_user_id(user_id)

    message = ""
    if not user:
        message = f"没有找到user_id为{user_id}的用户"
        print(message)
        return jsonify({"message": message,
                        "re": False}), 404

    if user['tag'] == tag:
        message = f"user_id为{user_id}的用户tag已经是{tag}"
        print(message)
        return jsonify({"message": message,
                        "re": True})
    else:
        updated_count = update_user_tag_by_user_id(user_id, tag)
        if updated_count > 0:
            message = f"成功将{updated_count}条数据的tag改为{tag}"
            print(message)
            return jsonify({"message": message,
                            "re": True})
        else:
            message = f"没有将任何数据的tag改为{tag}"
            print(message)
            return jsonify({"message": message,
                            "re": False}), 404