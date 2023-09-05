import logging

from services.table_service import TableService

logger = logging.getLogger(__name__)


class VipUserBindingsTableService(TableService):

    table_name = "vip_user_bindings"