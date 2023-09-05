import logging

from services.table_service import TableService

logger = logging.getLogger(__name__)


class UserActivityDataTableService(TableService):
    table_name = "user_activity_data"