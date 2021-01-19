#!/usr/bin/python3

"""
Created on 20200125
Update on 
@author: Sandro Regis Cardoso
"""

import argparse
import ast
import json
import logging.config
import yaml
from pexecute.process import ProcessLoom

from models.rpa.RedisSingleton import RedisServer
from models.rpa.WebDriverSingleton import WebBrowser
from models.rpa.StartProcess import StartProcess as _STARTPROCESS
from models.rpa.Typist import _Typist

from models.rpa.__init__ import __data_deploy__ as DATA_DEPLOY
from models.rpa.__init__ import __version__ as VERSION

from argparse import ArgumentError
from selenium import webdriver

class BootStrapSingleton(type):
    _name = "BootStrapSingleton"
    _instances = {}
    
    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(BootStrapSingleton, self).__call__(*args, **kwargs)
        return self._instances[self]
    

class BootStrap(object):
    _name           =   "BootStrap"
    __metaclass__   =   BootStrapSingleton
    
    #Global vars
    #_MAIN_SYS_RPA_OBJECT = None
    #_REDIS_BROWSERS_INSTANCES = object
    #_BROWSERS_INSTANCES = []
    
    _REDIS_SERVICE      =   object
    __SITES             =   {}
    __SITES_TO_LOAD     =   []
    _LOADED_BROWSERS    =   []
    _LOGGED_SITES       =   []
    _CONTRACTS          =   []
    __QUEUE_TO_PROCESS  =   []
    _EXECUTED_CONTRACTS =   []
    
    
    def __init__(self):
        try:
            #self._REDIS_BROWSERS_INSTANCES = self._getRedisBrowserInstances()
            self.__boot_config, __log   =   self.__loadDefaults()
            self.__createRedisService(self.__boot_config['queue_server'])
            self.__SITES    =   self.__loadSites()
            self.__loadContractQuee(self.__boot_config['queue_server']['input'])            
            return
        except Exception as ex:
            raise ex
    
    def __loadDefaults(self):
        try:
            parser_boot =   argparse.ArgumentParser(description="Validando dados de boot do RPA")
            parser_boot.add_argument('-cb', '--config_boot', required = False, 
                                     default = './config/bootstrap.yaml', help = 'Arquivo de conexao com REDIS')
            
            boot_args           =   parser_boot.parse_args()
            boot_config, log    =   self.__load_boot_parameters('Carregando Dados de Boot {0}'.format(VERSION), 'C.A.I.O | RPA', boot_args.config_boot)
            
            log.info('Copyright: Projétaty SCA {0}'.format(DATA_DEPLOY))
            logging.info("RPA.BootStrap loaded.........")
            
            return boot_config, log
        except ArgumentError as parseExc:
            raise parseExc
    
    def __loadSites(self):
        try:
            parser_sites = argparse.ArgumentParser(description="Validando dados de sites do RPA")
            parser_sites.add_argument('-cs',
                                    '--config_sites',
                                    help='Arquivo de configuracaco de Sites para Averbacao',
                                    required=False,
                                    default='./config/sites.yaml')
            site_args = parser_sites.parse_args()
            self.__SITES = self.__set_sites_yaml('Carregando Dados de Sites {0}'.format(VERSION), 'C.A.I.O | RPA', site_args.config_sites)
            logging.info("ACTIVE CUSTOMERS SITES loaded.........")
            return self.__SITES
        except Exception:
            raise ArgumentError
    
    
    def _tryLogin(self, _convenio:int, _browser_instance:webdriver, _auth:dict, _login_page:dict)->bool:
        try:
            __runner    =   _STARTPROCESS()
            result      =   __runner._doLogin(_convenio, _browser_instance, _auth, _login_page)
            '''if result:
                self._LOGGED_SITES.append(_convenio)'''
            return result
        except Exception as ex:
            raise ex
    
    def _callTypist(self, contracts:list):
        try:
            __typist = _Typist()
            runForms = ProcessLoom(max_runner_cap=8)
            workload = []
            
            for loggedSites in self._LOGGED_SITES:
                formData = []
                for cntr in contracts:
                    if int(cntr['dados']['numeroconvenio']['valor']) == loggedSites['convenio']:
                        formData.append(cntr['dados'])
                        browserInstance = [loggedSites.get('browser_inst')]
                    del(cntr)
                workload.append((__typist._tasksOnSite1_v2, browserInstance, {'contratos': formData, 'wait': 0.75}))
                del(browserInstance)
                del(formData)
            
            del(contracts)
            del(loggedSites)
            
            runForms.add_work(workload)
            result = runForms.execute()
            
            for res in result.items():
                logging.info(res)
            
            return result
        except Exception as ex:
            raise ex
    
    """def _callTypist(self, contracts:list):
        try:
            __typist = _Typist()
            runForms = ProcessLoom(max_runner_cap=8)
            workload = []
            formData = []
            browserInstance = None
            for loggedSites in self._LOGGED_SITES:
                for cntr in contracts:
                    if int(cntr['dados']['numeroconvenio']['valor']) == loggedSites['convenio']:
                        formData.append(cntr['dados'])
                        if browserInstance == None:
                            browserInstance = loggedSites['browser_inst']
                            logging.info("Browser %s" %browserInstance)
                    
                            workload.append((__typist._tasksOnSite1_v2, [browserInstance], {'contratos': formData, 'wait':2.5}))
                            runForms.add_work(workload)
                
                        browserInstance = None
            
            result = runForms.execute()
            
            for res in result.items():
                logging.info(res)
            
            #mem relief
            del(contracts)
            del(formData)
            del(workload)
            
            return result
        except Exception as ex:
            raise ex"""
    
    
    def _prepareSitesToLoad(self):
        try:
            #Monta um dicionario de dados relacional entre o convenio, site, browser para ser utilizado, página e dados de login
            #usando not in dic_convenios_e_sites[]
            for yamlkey in self.__SITES:
                for site_config_values in self.__SITES[yamlkey]:
                    if int(site_config_values['convenio']) in self.__QUEUE_TO_PROCESS:
                        self.__SITES_TO_LOAD.append({'convenio': site_config_values['convenio'],
                                                'browser_distro': site_config_values['remote']['browser_config']['browser'],
                                                'site': site_config_values['url'], 'auth': site_config_values['auth'],
                                                'login_page': site_config_values['login_page']})
                #destroy loop vars
                    del(site_config_values)
                del(yamlkey)
                return self.__SITES_TO_LOAD
        except Exception as ex:
            raise ex
    
    def _prepareContractQueueToProcess(self):
        try:
            #Verifica se o convenio não está na fila para abrir o site relacionado
            #Se o convenio já existir na fila não abre duas vezes o mesmo site.
            for indice, val in enumerate(self._CONTRACTS):
                for k, num_conv in val['data']['dados']['numeroconvenio'].items():
                    if k == 'valor':
                        if int(num_conv) not in self.__QUEUE_TO_PROCESS:
                            self.__QUEUE_TO_PROCESS.append(int(num_conv))
                #destroy loop vars
                    del(k); del(num_conv);
                del(indice); del(val);
            return self.__QUEUE_TO_PROCESS
        except Exception as excp:
            raise excp
    
    
    def _checkRedisServiceStatus(self):
        try:
            status = self._REDIS_SERVICE.ping()
            return status
        except Exception as ex:
            raise ex
    
    def _verifyContractQuee(self):
        try:
            result = self.__loadContractQuee(self.__boot_config['queue_server']['input'])
            return result
        except Exception as ex:
            raise ex
        
    def __loadContractQuee(self, param):
        """
        Populate data in Redis Queue
            :var param: list of data loaded from config file
            :author: Sandro Regis Cardoso
            :copyright: Projetaty SCA
            :version: 1.0
            :revision: 1
            :revision_author: Dev 01
        """
        try:
            self._REDIS_SERVICE.flushdb(asynchronous=True) #Usage for dev
            #print(__boot_config['queue_server']['input']['file'])
            with open(param['file'], 'r') as stream:
                #contrato = json.load(stream)
                __CONTRACTS = json.load(stream)
                #contrato['data']['payload']['dados']['terceiros']['dados']
                del(stream)
            
            #'Hash Set value : HSET()
            self._REDIS_SERVICE.hset("hash-redis-quee", "convenios-fila1",   str(__CONTRACTS))
            
            #BLOCO DE TESTES:
            redis_keys = self._REDIS_SERVICE.keys("*")
            #print("redis_keys : ", redis_keys)
            
            subkey_redis_quee = None
            
            for index, hash_name in enumerate(redis_keys):
                #print("Contratos index e hash-name : ", index, hash_name)
                for sbkn, sbk_redis_quee in self._REDIS_SERVICE.hgetall(hash_name).items():
                    #subkey_name = sbkn
                    if type(sbk_redis_quee[index]) != dict:
                        subkey_redis_quee = ast.literal_eval(sbk_redis_quee)
                        #print("Globals : ", globals())
                        self._CONTRACTS = subkey_redis_quee
                        #print("Contratos Subkey name :", sbkn, "-> Redis quee for subkey:", subkey_redis_quee)
                    del(sbkn)
                    del(sbk_redis_quee)
                del(index)
                del(hash_name)
                del(subkey_redis_quee)
                del(redis_keys)
                del(param)
            
            logging.info("CONTRACT's QUEUE CHARGED.........")
            return self._CONTRACTS
            
            """
            @todo: Eval wich parameter has data file or url
            if 'file' in param:
                pass
                
            if 'url' in param:
                #not implemented yet
                pass
            else:
                #TODO: Enviar msg email e WhatsApp para Projétaty SCA comunicando erro grave.
                raise BaseException("Nenhuma fila de dados especificada")"""
        except Exception as ex:
            raise ex
    
    def __createRedisService(self, __boot_config):
        """
        Places Redis Server connection instance
        @author: Sandro Regis Cardoso
        @copyright: Projetaty SCA
        """
        try:
            self._REDIS_SERVICE = RedisServer().setConnection(
                                    __boot_config['host'], 
                                    __boot_config['port'], 
                                    __boot_config['db'], 
                                    __boot_config['password'])
            del(__boot_config)
            logging.info("REDIS SERVICE loaded.........")
            return self._REDIS_SERVICE
        except Exception as ex:
            raise ex
        
    def __createRedisBrowserInstances(self):
        try:
            self._REDIS_BROWSERS_INSTANCES = RedisServer().setConnection('127.0.0.1', '6379', '1', 'AAABBBCCC')
            return self._REDIS_BROWSERS_INSTANCES
        except Exception as ex:
            raise ex
    
    def _getRedisBrowserInstances(self):
        res = self.__createRedisBrowserInstances()
        return res
    
    @staticmethod
    def setGlobalBrwInst(dados:list):
        brwinst = []
        brwinst.append(dados)
        return brwinst
    
    def _openBrowserInstance(self, convenio:int, browser_distro:str, url:str)->object:
        try:
            browser_instance = WebBrowser().openBrowser(browser_distro, url)
            #if len(self._BROWSERS_INSTANCES) == 0:
            """if browser_instance != None:
                self._CONTRACTS = self._CONTRACTS + [{"convenio":convenio,"browser_inst":browser_instance}]
                self._BROWSERS_INSTANCES = self._BROWSERS_INSTANCES.append({'convenio': convenio, 'browser_inst': browser_instance})
                self._REDIS_BROWSERS_INSTANCES.hset("hashset-browser", str(convenio), str([{"convenio": convenio, "browser_inst": str(browser_instance)}]))"""
            
            logging.info("RPA returning Browser instance %s" %browser_distro)
            del(convenio)
            del(browser_distro)
            del(url)
            return browser_instance
        except Exception as brwexcpt:
            raise brwexcpt
    
    def __set_sites_yaml(self, texto:str, app_name:str, site_config_file)->list:
        """
        Carrega arquivo de configuração dos sites (obrigatorio)
            :param texto: Texto a ser exibido primeiro
            :param app_name: nome do logger principal
            :param site_config_file: arquivo formato .yaml a ser carregado
        """
        try:
            with open(site_config_file, 'r') as stream:
                sites_config = yaml.load(stream)
                #logging.config.dictConfig(sites_config['sites'][0])
                #log = logging.getLogger(app_name)
                #log.info('>>>>>> Starting %s, loading setup file: %s', texto, site_config_file)
            del(texto)
            del(app_name)
            del(site_config_file)
            logging.info("SITE's CONFIG loaded.........")
            return sites_config
        except yaml.YAMLError as exc:
            logging.info('Sites Config: {0}, Erro: {0}'.format(site_config_file, repr(exc)))
        except Exception as exp:
            logging.info('Sites Config: {0}, Erro Geral: {0}'.format(site_config_file, repr(exp)))
    
    
    def __load_boot_parameters(self, texto, app_name, boot_config_file):
        """
        Carrega arquivo de configuração e loggin predefinido (obrigatorio)
            :param texto: Texto a ser exibido primeiro
            :param app_name: nome do logger principal
            :param boot_config_file: arquivo formato .yaml a ser carregado
        """
        try:
            with open(boot_config_file, 'r') as stream:
                global_config = yaml.load(stream)
                logging.config.dictConfig(global_config['loggin'])
                log = logging.getLogger(app_name)
                log.info('>>>>>> Inicializando %s, carregando arquivo de configuracao: %s', texto, boot_config_file)
                return global_config, log
        except yaml.YAMLError as exc:
            logging.info('Boot Config: {0}, Erro: {1}'.format(boot_config_file, repr(exc)))
        except Exception as exp:
            logging.info('Boot Config: {0}, Erro Geral: {1}'.format(boot_config_file, repr(exp)))


    def updateContratos(self, idx, browser_inst):
        global _CONTRACTS
        _CONTRACTS = self._CONTRACTS
        del(_CONTRACTS)
        del(self._CONTRACTS)
        #self._CONTRACTS[idx]['data']['header']['browser_inst'] = browser_inst
        return
    
    def registrarContratosProcessados(self, exec_id:int):
        try:
            self.__EXECUTED_CONTRACTS = self.__EXECUTED_CONTRACTS + [exec_id]
            return
        except Exception as ex:
            raise ex