# -*- encoding: utf-8 -*-
#!/usr/bin/python3
"""
Created on 20200125
Updated on 2021/jan
@author: Sandro Regis Cardoso
"""
import logging
from bin.rpa.System import BootStrap as System
from redis.exceptions import RedisError
import time as __timer
from utils.WebDriverSingleton import WebBrowser as __WEBBROWSER

#from pexecute.process import ProcessLoom

"""
import importlib
import json
from time import sleep
import urllib3
"""

def main():
    """
    @TODO: Doc String
    """
    
    _name                       = "main"
    __redisQueueServIsActive    = False
    __CURRENT_QUEUE_SIZE        = 0
    _browser_instance           = object
    
    try:
        __system                = System()
        __tmr                   = 0
        __tmr_limit             = 5
        __redisQueueServIsActive= __system._REDIS_SERVICE.ping()
        
        """
        runForms = ProcessLoom(max_runner_cap=8)
        workload = []
        """
        while __redisQueueServIsActive == True:
            #bloco de test para verificar a inclusão de um novo registro na fila
            #melhorar esta chamada futuramente
            #https://www.geeksforgeeks.org/timer-objects-python/
            if __tmr == __tmr_limit:
                logging.info("Checking for new contracts in the Redis Queue")
                __system._verifyContractQuee()
                
                logging.info("Checking for news data forms done.")
                #reset var
                __tmr = 0
            
            #Evaluate condition to process queue
            if len(__system._CONTRACTS) > __CURRENT_QUEUE_SIZE:
                #List to store form input values
                input_values    =  []
                
                #Update queue site
                __CURRENT_QUEUE_SIZE    =   len(__system._CONTRACTS)
                
                #PREPARE LIST OF CONTRACTS DO PROCESS
                #__cq2p : contract queue to process
                __cq2p  =   __system._prepareContractQueueToProcess()
                logging.info(__cq2p)
                
                #__s2o : site to open
                __s2o   =   __system._prepareSitesToLoad()
                logging.info(__s2o)
                
                #Run loop to open browsers and do processes
                for __sites in __s2o:
                    #if __sites.get('site') is not None and __sites.get('site') != "":
                    #Try open browser and load url
                    _browser_instance   =   __WEBBROWSER()._openBrowser(__sites.get('browser_distro'), __sites.get('site'))
                    
                    #Se o site não estiver aberto o Singleton retorna um objeto de browser para preenchimento dos dados
                    if _browser_instance is not None:
                        
                        __system._LOADED_BROWSERS.append(
                            {'convenio': __sites.get('convenio'),
                             'browser_inst': _browser_instance
                            })
                        
                        #Registra o log do site que foi aberto
                        logging.info("Site : %s %s", __sites.get('site'), "carregado e aguardando autenticacao....")
                        
                        #@Desc:    If the agreement is not in the list of logged agreements \
                        #          read the created dictionary data and authenticates
                        #@NOTE:    This process must be performed by Nutcracker
                        #@TODO:    Create method to perform this task
                        if __sites.get('convenio') not in __system._LOGGED_SITES:
                            logging.info("Try to Log in to the site : %s", __sites.get('site'))
                            __logged    =   __system._tryLogin(__sites.get('convenio'), _browser_instance, __sites.get('auth'), __sites.get('login_page'))
                            
                            if __logged == True:
                                logging.info("Successfully logged on site : %s", __sites.get('site'))
                                __system._LOGGED_SITES.append({"site": __sites.get('site'), "convenio": __sites.get('convenio'), "browser_inst": _browser_instance})
                            else:
                                #TODO: Register error to login and send email;
                                pass
                    else:
                        #@Desc: RECUPERA O OBJETO DA LISTA RUNNING_SITES E RETORNA PARA EXECUCAO DO PROCESSO
                        for itens in __system._LOGGED_SITES:
                            if __sites.get('convenio') == itens.get('convenio'):
                                _browser_instance   =   itens.get('browser_inst')
                                logging.info("Site %s already loaded.", __sites.get('site'))
                                logging.info("Returning existing browser instance : %s", _browser_instance)
                    
                    for ix, val in enumerate(__system._CONTRACTS):
                        #if int(val['data']['header']['exec_id']) not in __system._EXECUTED_CONTRACTS:
                        #Monta chamada PPP
                        eval1 = (int(val['data']['dados']['numeroconvenio']['valor']) == int(__sites.get('convenio')))
                        eval2 = (int(val['data']['header']['exec_id']) not in __system._EXECUTED_CONTRACTS)
                        if eval1 == True and eval2 == True:
                            input_values.append(val['data'])
                            #uso temporario desta global_var
                            __system._EXECUTED_CONTRACTS.append(int(val['data']['header']['exec_id']))
                        
                        #destroy loop vars
                        del(ix); del(val);
                
                #Perform parallel execution
                #Fill form as many records has in json file
                __system._callTypist(input_values)
                """workload.append((__system._callTypist, [_browser_instance], {'contratos': input_values, 'wait':1.5}))
                runForms.add_work(workload)
                result = runForms.execute()
                
                for res in result.items():
                    logging.info(res)"""
            
            #RUN TIMER FOR CHECK CONTRACT QUEUE
            __timer.sleep(2)
            __tmr += 1
            print("TIMER : %s" %__tmr)
            if __tmr == __tmr_limit:
                if __system._checkRedisServiceStatus() == False:
                    if _browser_instance != None:
                        _browser_instance.close()
                    raise RedisError("Redis Service is down")
                else:
                    continue
    except BaseException as ex:
        raise BaseException("Russel module main program Fatal Error : %s" %ex)
    
if __name__ == "__main__":
    main()