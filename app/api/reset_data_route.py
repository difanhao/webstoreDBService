from flask import Blueprint, jsonify

from services.user_activity_data_table_service import UserActivityDataTableService
from services.user_mission_table_service import UserMissionTableService
from services.vip_user_bindings_table_service import VipUserBindingsTableService

reset_data_bp = Blueprint("reset_data", __name__)

@reset_data_bp.route("/autumn_activity/<open_id>/<user_id>/<activity_id>/", methods=["GET"])
def reset_data_autumn_activity(open_id, user_id, activity_id):
    """
    重置用户的中秋活动的数据
    :param open_id:
    :param user_id:
    :param activity_id:
    :return:
    """
    deleted_rows_in_user_mission = UserMissionTableService.delete_data(open_id=open_id, user_id=user_id, activity_id=activity_id)
    deleted_rows_in_user_mission = UserActivityDataTableService.delete_data(open_id=open_id, user_id=user_id, activity_id=activity_id)
    deleted_rows_in_vip_user_bindings = VipUserBindingsTableService.delete_data(open_id=open_id)



    message = f"删除{deleted_rows_in_user_mission}条订单数据"
    return jsonify({"message": message,
                    "re": True})