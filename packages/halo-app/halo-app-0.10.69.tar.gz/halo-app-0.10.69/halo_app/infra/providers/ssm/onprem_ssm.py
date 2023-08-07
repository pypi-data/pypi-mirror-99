from __future__ import print_function

import configparser
import datetime
import json
import logging
import os
import time
from environs import Env
from abc import ABCMeta,abstractmethod

from halo_app.app.exceptions import HaloMethodNotImplementedException
from halo_app.infra.exceptions import CacheKeyException, CacheExpireException, AbsHaloException
from halo_app.infra.providers.exceptions import  NoLocalSSMClassException, NoLocalSSMModuleException, SSMException
from halo_app.classes import AbsBaseClass
from halo_app.logs import log_json
from halo_app.base_util import BaseUtil
from halo_app.reflect import Reflect
from halo_app.settingsx import settingsx
settings = settingsx()

current_milli_time = lambda: int(round(time.time() * 1000))

logger = logging.getLogger(__name__)

client = None


class AbsOnPremClient(AbsBaseClass):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_parameters_by_path(self,Path,Recursive,WithDecryption):
        raise HaloMethodNotImplementedException("NotImplemented get_parameters_by_path in OnPremClient")

    @abstractmethod
    def put_parameter(self,Name,Value,Type,Overwrite):
        raise HaloMethodNotImplementedException("NotImplemented put_parameter in OnPremClient")

def get_onprem_client()->AbsOnPremClient:
    if settings.ONPREM_SSM_CLASS_NAME:
        class_name = settings.ONPREM_SSM_CLASS_NAME
    else:
        raise NoLocalSSMClassException("no ONPREM_SSM_CLASS_NAME")
    if settings.ONPREM_SSM_MODULE_NAME:
        module = settings.ONPREM_SSM_MODULE_NAME
    else:
        raise NoLocalSSMModuleException("no ONPREM_SSM_MODULE_NAME")
    return Reflect.do_instantiate(module,class_name, None)

def get_onprem_client1()->AbsOnPremClient:
    if settings.ONPREM_SSM_CLASS_NAME:
        class_name = settings.ONPREM_SSM_CLASS_NAME
    else:
        raise NoLocalSSMClassException("no ONPREM_SSM_CLASS_NAME")
    if settings.ONPREM_SSM_MODULE_NAME:
        module = settings.ONPREM_SSM_MODULE_NAME
    else:
        raise NoLocalSSMModuleException("no ONPREM_SSM_MODULE_NAME")
    import importlib
    module = importlib.import_module(module)
    class_ = getattr(module, class_name)
    instance = class_()
    return instance

def get_client():
    """

    :param region_name:
    :return:
    """
    logger.debug("get_client")
    global client
    if not client:
        client = get_onprem_client()
    return client



# ALWAYS use json value in parameter store!!!

class Cache(AbsBaseClass):
    expiration = 0
    items = None


DEFAULT_EXPIRY = 3 * 60 * 1000;  # default expiry is 3 mins


def load_cache(config, expiryMs=DEFAULT_EXPIRY):
    """

    :param config:
    :param expiryMs:
    :return:
    """
    if config is None:
        raise SSMException('you need to provide a non-empty config')

    if (expiryMs <= 0):
        raise SSMException('you need to specify an expiry (ms) greater than 0, or leave it undefined')

    # the below uses the captured closure to return an object with a gettable
    # property per config key that on invoke:
    #  * fetch the config values and cache them the first time
    #  * thereafter, use cached values until they expire
    #  * otherwise, try fetching from SSM parameter store again and cache them

    now = datetime.datetime.now()
    cache = Cache()
    cache.expiration = current_milli_time() + expiryMs
    cache.items = config

    logger.debug('refreshed cache')
    return cache


class MyConfig(AbsBaseClass):
    def __init__(self, cache, path):
        """
        Construct new MyApp with configuration
        :param config: application configuration
        """
        self.cache = cache
        self.path = path

    def get_param(self, key):
        """

        :param key:
        :return:
        """
        now = current_milli_time()
        if now <= self.cache.expiration:
            for key in self.cache.items:
                logger.debug("key=" + str(key))
            if key in self.cache.items:
                return self.cache.items[key]
            else:
                raise CacheKeyException("no key in cache:" + key)
        else:
            self.cache = get_cache(self.region_name, self.path)
            if key in self.cache.items:
                return self.cache.items[key]
        raise CacheExpireException("cache expired")


def load_config(ssm_parameter_path):
    """
    Load configparser from config stored in SSM Parameter Store
    :param ssm_parameter_path: Path to app config in SSM Parameter Store
    :return: ConfigParser holding loaded config
    """
    configuration = configparser.ConfigParser()
    logger.debug("ssm_parameter_path=" + str(ssm_parameter_path) )
    try:
        # Get all parameters for this app
        param_details = get_client().get_parameters_by_path(
            Path=ssm_parameter_path,
            Recursive=False,
            WithDecryption=True
        )

        logger.debug("config="+str(ssm_parameter_path) + "=" + str(param_details))
        # Loop through the returned parameters and populate the ConfigParser
        if 'Parameters' in param_details and len(param_details.get('Parameters')) > 0:
            for param in param_details.get('Parameters'):
                param_path_array = param.get('Name').split("/")
                section_position = len(param_path_array) - 1
                section_name = param_path_array[section_position]
                config_values = json.loads(param.get('Value'))
                config_dict = {section_name: config_values}
                logger.debug("Found configuration: " + str(config_dict))
                configuration.read_dict(config_dict)

    except AbsHaloException as e:
        logger.error("Encountered a client Exception loading config from SSM:" + str(e))
    except json.decoder.JSONDecodeException as e:
        logger.error("Encountered a json Exception loading config from SSM:" + str(e))
    except Exception as e:
        logger.error("Encountered an Exception loading config from SSM:" + str(e))
    finally:
        return configuration


def set_param_config(region_name, key, value):
    """

    :param region_name:
    :param key:
    :param value:
    :return:
    """
    full_config_path,short_config_path = BaseUtil.get_env()
    ssm_parameter_path = full_config_path + '/' + key
    return set_config(region_name, ssm_parameter_path, value)

def get_app_param_config(service_name,var_name):
    """

    :param region_name:
    :param host:
    :return:
    """
    return None

def set_app_param_config(params):
    """

    :param region_name:
    :param host:
    :return:
    """
    full_config_path,short_config_path = BaseUtil.get_env()
    ssm_parameter_path = short_config_path + '/' + BaseUtil.get_func()
    value = '{'
    for var_name in params.keys():
        value = value + '"' + str(var_name) + '":"' + str(params[var_name]) + '",'
    value = value[:-1]
    value = value + '}'
    return set_config(ssm_parameter_path, value)


def set_config(ssm_parameter_path, value):
    """
    Load configparser from config stored in SSM Parameter Store
    :param ssm_parameter_path: Path to app config in SSM Parameter Store
    :return: ConfigParser holding loaded config
    """
    try:
        # set parameters for this app

        json.loads(value)
        ret = get_client().put_parameter(
            Name=ssm_parameter_path,
            Value=value,
            Type='String',
            Overwrite=True
        )
        full_config_path,short_config_path = BaseUtil.get_env()
        logger.debug(str(full_config_path) + "=" + str(ret))
        return True
    except AbsHaloException as e:
        msg = "Encountered a client Exception setting config from SSM"
        logger.error(msg)
        raise SSMException(msg,e)
    except json.decoder.JSONDecodeException as e:
        msg = "Encountered a json Exception setting config from SSM"
        logger.error(msg)
        raise SSMException(msg,e)
    except Exception as e:
        msg = "Encountered an Exception setting config from SSM"
        logger.error(msg)
        raise SSMException(msg,e)


def get_cache(path):
    """

    :param region_name:
    :param path:
    :return:
    """
    logger.debug("get_cache")
    config = load_config(path)
    cache = load_cache(config)
    return cache


def get_config():
    """

    :param region_name:
    :return:
    """
    # Initialize app if it doesn't yet exist
    full_config_path,short_config_path = BaseUtil.get_env()
    logger.debug("Loading config and creating new MyConfig..." + full_config_path)
    cache = get_cache(full_config_path)
    myconfig = MyConfig(cache, full_config_path)
    logger.debug("MyConfig is " + str(cache.items._sections))
    return myconfig


def get_app_config():
    """

    :param region_name:
    :return:
    """
    # Initialize app if it doesn't yet exist
    full_config_path,short_config_path = BaseUtil.get_env()
    logger.debug("Loading app config and creating new AppConfig..." + short_config_path)
    cache = get_cache(short_config_path)
    appconfig = MyConfig(cache, short_config_path)
    logger.debug("AppConfig is " + str(cache.items._sections))
    return appconfig
