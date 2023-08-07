import logging
from halo_app.classes import AbsBaseClass
from halo_app.app.context import HaloContext, InitCtxFactory
from halo_app.infra.providers.providers import get_provider,ONPREM
from .exceptions import ProviderException
from halo_app.entrypoints.client_type import ClientType
from halo_app.infra.exceptions import CacheException
from halo_app.reflect import Reflect
from halo_app.settingsx import settingsx

settings = settingsx()

logger = logging.getLogger(__name__)

class ProviderUtil(AbsBaseClass):

    @staticmethod
    def get_func_region():
        """

        :return:
        """
        provider = get_provider()
        if provider.PROVIDER_NAME != ONPREM:
            return provider.get_func_region()
        raise ProviderException("no region defined")

    @staticmethod
    def get_debug_param():
        """

        :return:
        """
        # check if env var for sampled debug logs is on and activate for percentage in settings (5%)
        dbg = 'false'
        if settings.SSM_CONFIG is None:
            return dbg
        try:
            DEBUG_LOG = settings.SSM_CONFIG.get_param('DEBUG_LOG')
            dbg = DEBUG_LOG["val"]
            logger.debug("get_debug_param=" + dbg)
        except CacheException as e:
            pass
        return dbg