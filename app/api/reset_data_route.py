from flask import Blueprint, jsonify

from services.user_activity_data_table_service import UserActivityDataTableService
from services.user_mission_table_service import UserMissionTableService
from services.vip_orders_table_service import VipOrdersTableService
from services.vip_user_bindings_table_service import VipUserBindingsTableService
from services.activity_info_table_service import ActivityInfoTableService

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

    # 获取中秋活动开始和结束时间
    start_time_datatime_obj = ActivityInfoTableService.get_activity_start_time(activity_id)
    start_time_timestamp = int(start_time_datatime_obj.timestamp())
    end_time_datatime_obj = ActivityInfoTableService.get_activity_end_time(activity_id)
    end_time_timestamp = int(end_time_datatime_obj.timestamp())

    # TODO 传递时间值和方向
    VipOrdersTableService.advance_create_time_of_successful_order(open_id, start_time_timestamp, end_time_timestamp)


    message = "OK"
    return jsonify({"message": message,
                    "re": True})