import logging

from services.table_service import TableService

logger = logging.getLogger(__name__)


class UserMissionTableService(TableService):

    table_name = "user_mission"

