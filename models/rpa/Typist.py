# -*- encoding=utf-8 -*-
#!/usr/bin/python3
"""
Created on 2020/jan
Update on 2021/jan
@author: Sandro Regis Cardoso
"""

import logging
from selenium import webdriver
from time import sleep

class _Typist(object):
    
    def __init__(self):
        logging.info("Typist in action")
        return
    
    def __tasksOnSite1(self, browser_instance:webdriver, contratos:list, wait=0) -> bool:
        
        try:
            #browser_instance.find_element_by_xpath('//*[@id="acessar_form2"]').click()
            for dados_de_input in contratos:
                
                browser_instance.find_element_by_xpath('//*[@id="c1"]').clear; sleep(wait)
                browser_instance.find_element_by_xpath('//*[@id="c1"]').send_keys(str(dados_de_input['c1'].get('valor')));
                
                browser_instance.find_element_by_xpath('//*[@id="c2"]').clear(); sleep(wait)
                browser_instance.find_element_by_xpath('//*[@id="c2"]').send_keys(str(dados_de_input['c2'].get('valor')));
                
                browser_instance.find_element_by_xpath('//*[@id="c3"]').clear(); sleep(wait)
                browser_instance.find_element_by_xpath('//*[@id="c3"]').send_keys(str(dados_de_input['c3'].get('valor')));
                
                browser_instance.find_element_by_xpath('//*[@id="c4"]').clear(); sleep(wait)
                browser_instance.find_element_by_xpath('//*[@id="c4"]').send_keys(str(dados_de_input['c4'].get('valor')));
                
                browser_instance.find_element_by_xpath('//*[@id="c5"]').clear(); sleep(wait)
                browser_instance.find_element_by_xpath('//*[@id="c5"]').send_keys(str(dados_de_input['c5'].get('valor')));
                
                
                browser_instance.find_element_by_xpath('//*[@id="c6"]').clear(); sleep(wait)
                browser_instance.find_element_by_xpath('//*[@id="c6"]').send_keys(str(dados_de_input['c6'].get('valor')));
                
                
                browser_instance.find_element_by_xpath('//*[@id="c7"]').clear(); sleep(wait)
                browser_instance.find_element_by_xpath('//*[@id="c7"]').send_keys(str(dados_de_input['c7'].get('valor')));
                
                browser_instance.find_element_by_xpath('//*[@id="c8"]').clear(); sleep(wait)
                browser_instance.find_element_by_xpath('//*[@id="c8"]').send_keys(str(dados_de_input['c8'].get('valor')));
                
                browser_instance.find_element_by_xpath('//*[@id="c9"]').clear(); sleep(wait)
                browser_instance.find_element_by_xpath('//*[@id="c9"]').send_keys(str(dados_de_input['c9'].get('valor')));
                
                browser_instance.find_element_by_xpath('//*[@id="c10"]').clear(); sleep(wait)
                browser_instance.find_element_by_xpath('//*[@id="c10"]').send_keys(str(dados_de_input['c10'].get('valor')));
                #registra o contrato executado
                #TODO: Verificar retorno da execucao
                #Boot._CONTRATOS_EXECUTADOS.append(exec_id)
                #print("R2D2->CONTRATOS EXECUTADOS: ", Boot._CONTRATOS_EXECUTADOS)
                #send form
                browser_instance.find_element_by_xpath('//*[@id="submeter"]').click()
                sleep(wait)
                browser_instance.find_element_by_xpath('//*[@id="continue"]').click()
        except Exception as excpt:
            raise excpt
    
    def _tasksOnSite1_v2(self, browser_instance:webdriver, contratos:list, wait=0):
        """
        Dummy method should be eliminated on test case development
        @TODO: delete after test case
        """
        try:
            sleep(1.25)
            for dados in contratos:
                c1 = browser_instance.find_element_by_xpath('//*[@id="c1"]')
                c1.clear(); sleep(wait)
                c1.send_keys(str(dados['c1']['valor'])); 
                
                c2 = browser_instance.find_element_by_xpath('//*[@id="c2"]')
                c2.clear(); sleep(wait)
                c2.send_keys(str(dados['c2']['valor']));
                
                c3 = browser_instance.find_element_by_xpath('//*[@id="c3"]')
                c3.clear(); sleep(wait)
                c3.send_keys(str(dados['c3']['valor']));
                
                c4 = browser_instance.find_element_by_xpath('//*[@id="c4"]')
                c4.clear(); sleep(wait)
                c4.send_keys(str(dados['c4']['valor']));
                
                c5 = browser_instance.find_element_by_xpath('//*[@id="c5"]')
                c5.clear(); sleep(wait)
                c5.send_keys(str(dados['c5']['valor']));
                
                c6 = browser_instance.find_element_by_xpath('//*[@id="c6"]')
                c6.clear(); sleep(wait)
                c6.send_keys(str(dados['c6']['valor']));
                
                c7 = browser_instance.find_element_by_xpath('//*[@id="c7"]')
                c7.clear(); sleep(wait)
                c7.send_keys(str(dados['c7']['valor']));
                
                c8 = browser_instance.find_element_by_xpath('//*[@id="c8"]')
                c8.clear(); sleep(wait)
                c8.send_keys(str(dados['c8']['valor']));
                
                c9 = browser_instance.find_element_by_xpath('//*[@id="c9"]')
                c9.clear(); sleep(wait)
                c9.send_keys(str(dados['c9']['valor']));
                
                c10 = browser_instance.find_element_by_xpath('//*[@id="c10"]')
                c10.clear(); sleep(wait)
                c10.send_keys(str(dados['c10']['valor']));
                
                #send form
                browser_instance.find_element_by_xpath('//*[@id="submeter"]').click()
                browser_instance.find_element_by_xpath('//*[@id="continue"]').click()
        except Exception as excpt:
            raise excpt

