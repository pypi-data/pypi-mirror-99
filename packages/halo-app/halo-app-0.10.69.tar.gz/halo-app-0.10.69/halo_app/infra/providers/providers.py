from __future__ import print_function

import configparser
import datetime
import json
import logging
import os
import time
import uuid
import abc

#@ TODO put_parameter should be activated only is current value is different then the existing one
#@ TODO perf activation will reload SSM if needed and refresh API table


from .ssm.onprem_ssm  import set_app_param_config as set_app_param_config_onprem,get_app_param_config as get_app_param_config_onprem
from .ssm.onprem_ssm import get_config as get_config_onprem
from .ssm.onprem_ssm import get_app_config as get_app_config_onprem
from halo_app.settingsx import settingsx
from halo_app.infra.providers.exceptions import ProviderException,NoONPREMProviderClassException,NoONPREMProviderModuleException,ProviderInitException
from halo_app.classes import AbsBaseClass
from halo_app.logs import log_json
from halo_app.sys_util import SysUtil
from halo_app.reflect import Reflect
from ...app.exceptions import HaloMethodNotImplementedException

settings = settingsx()
#current_milli_time = lambda: int(round(time.time() * 1000))

logger = logging.getLogger(__name__)

AWS = 'AWS'
AZURE = 'AZURE'
GCP = 'GCP'
KUBELESS = 'KUBELESS'
ONPREM = 'ONPREM'
PROVIDERS = [AWS,AZURE,GCP,KUBELESS]


def get_provider_name():
    if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
        return AWS
    if 'KUBELESS_FUNCTION_NAME' in os.environ:
        return KUBELESS
    if settings.PROVIDER and settings.PROVIDER in PROVIDERS:
        return settings.PROVIDER
    return ONPREM



LATEST = None

class IProvider(AbsBaseClass,abc.ABC) :

    PROVIDER_NAME = None

    def show(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_context(self):
        pass

    def get_header_name(self, request, name):
        pass

    def get_request_id(self, request):
        pass

    def send_event(self,ctx,messageDict,service_name,version=LATEST,capture_response=None):
        pass

    def get_topic_name(self,lambda_name):
        pass

    def publish(self,ctx, messageDict, arn=None,capture_response=False,lambda_function_name=None):
        pass

    def invoke_sync(self,ctx, messageDict, lambda_function_name,version=LATEST):
        pass

    def send_mail(self,req_context, vars, from1=None, to=None):
        pass

    def get_timeout(self,request):
        pass

    def get_func_name(self):
        pass

    def upload_file(self,file,file_name, bucket_name, object_name=None):
        pass

    def create_presigned_url(self,bucket_name, object_name, expiration=3600):
        pass

    def get_path(url):
        pass

    def get_params(url):
        pass

class ONPREMProvider(IProvider):

    PROVIDER_NAME = ONPREM

    def __init__(self):
        pass

    def show(self):
        raise HaloMethodNotImplementedException("")

    @staticmethod
    def get_context():
        return {"stage": SysUtil.get_stage()}

    def get_header_name(self,request,name):
        return name

    def get_request_id(self,request):
        return uuid.uuid4().__str__()


def get_onprem_provider():
    if settings.ONPREM_PROVIDER_CLASS_NAME:
        class_name = settings.ONPREM_PROVIDER_CLASS_NAME
    else:
        raise NoONPREMProviderClassException("no ONPREM_PROVIDER_CLASS_NAME")
    if settings.ONPREM_PROVIDER_MODULE_NAME:
        module = settings.ONPREM_PROVIDER_MODULE_NAME
    else:
        raise NoONPREMProviderModuleException("no ONPREM_PROVIDER_MODULE_NAME")
    return Reflect.do_instantiate(module,class_name, None)

provider = None
def get_provider()->IProvider:
    global provider
    if provider:
        return provider
    provider_name = get_provider_name()
    logger.info("provider_name:"+str(provider_name))
    if  provider_name == AWS:
        try:
            from halo_aws.providers.cloud.aws.aws import AWSProvider
            provider = AWSProvider()
        except Exception as e:
            raise ProviderInitException("failed to get provider "+provider_name,e)
    else:
        if provider_name == ONPREM:
            try:
                provider = get_onprem_provider()
            except Exception as e:
                raise ProviderInitException("failed to get provider " + provider_name, e)
    return provider


################## ssm ###########################

def get_app_param_config(ssm_type, service_name,var_name):
    """

    :param region_name:
    :param host:
    :return:
    """
    if ssm_type == AWS:
        try:
            from .ssm.aws_ssm import get_app_param_config as get_app_param_config_cld
            return get_app_param_config_cld(service_name,var_name)
        except Exception as e:
            raise ProviderException("failed to get ssm: "+str(e),e)
    return get_app_param_config_onprem(service_name,var_name)

def set_app_param_config(ssm_type, params):
    """

    :param region_name:
    :param host:
    :return:
    """
    if ssm_type == AWS:
        try:
            from .ssm.aws_ssm import set_app_param_config as set_app_param_config_cld
            return set_app_param_config_cld(params)
        except Exception as e:
            raise ProviderException("failed to get ssm: "+str(e),e)
    return set_app_param_config_onprem(params)

def get_config(ssm_type):
    """

    :param region_name:
    :return:
    """
    # Initialize app if it doesn't yet exist
    if ssm_type == AWS:
        try:
            from .ssm.aws_ssm import get_config as get_config_cld
            return get_config_cld()
        except ProviderInitException as e:
            raise e
        except Exception as e:
            raise ProviderException("failed to get ssm type "+ssm_type,e)
    return get_config_onprem()


def get_app_config(ssm_type):
    """

    :param ssm_type: [None,ONPREM,AWS]
    :return:
    """
    # Initialize app if it doesn't yet exist
    if ssm_type == AWS:
        try:
            from .ssm.aws_ssm import get_app_config as get_app_config_cld
            return get_app_config_cld()
        except Exception as e:
            raise ProviderException("failed to get ssm type "+ssm_type,e)
    return get_app_config_onprem()

