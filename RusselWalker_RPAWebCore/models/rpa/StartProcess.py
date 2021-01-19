# -*- encoding=utf-8 -*-
#!/usr/bin/python3
"""
Created on 2020/jan
Update on 2021/jan
@author: Sandro Regis Cardoso
"""
import logging
from time import sleep

#@TODO: Change for import local package i.e firefox.geckodriver
from selenium import webdriver

#from bin.rpa.R2D2 import R2D2
import sys

class StartProcess(object):
    
    def __init__(self):
        logging.info("Criando objeto da StartProcess")
        return
    
    def str_to_class(self, str):
        return getattr(sys.modules[__name__], str)
    
    """def _preencherDados(self, convenio, browser_instance, contratos):
        fingers = R2D2()
        result = fingers._preencherDados(convenio, browser_instance, contratos)
        return result"""
    
    def __obterCaptchaValue(self, convenio, objeto_captcha):
        """
        Metodo com finalidade agilizar o desenvolvimento e testes
        TODO: Substituir por chamada de metodo na classe QuebraNozes
        """
        captcha_val = None
        
        #@TODO: Change CAPTCHA dummy values for nutcracker module processing 
        if convenio == 1:
            captcha_val = 'NJI83H'
        elif convenio == 2:
            captcha_val = '789215'
        elif convenio == 3:
            captcha_val = '9FB34Q'
        return captcha_val
    
    def mostrarApresentacao(self, browser_instance, convenio):
        if convenio == 1:
            sleep(1)
            browser_instance.execute_script('document.getElementById("apresentacao").innerHTML="Minha configuração é para rodar muito rapidamente dentro de uma rede local, onde não existem restrições para minha atuação \
                                e também não exista policiamento da minha operação como robô no preenchimento de dados, coleta e troca de informações.<br /> \
                                Meu processamento é extremamente rápido e provávelmente não será possível sua visão acompanhar."')
            sleep(5)
            browser_instance.find_element_by_xpath('//*[@id="acessar_form2"]').click()
            
        elif convenio == 2:
            sleep(1)
            browser_instance.execute_script("document.getElementById('apresentacao').innerHTML='Minha configuração é para rodar muito similar a um ser humano, porém um pouco mais rápido, justamente para evitar bloqueios em sistemas externos onde existem restrições para minha atuação \
                                ou seja, exista policiamento da minha operação como robô no preenchimento de dados, coleta e troca de informações.<br /> \
                                Meu processamento é em média 50% mais rápido do que a operação de um humano.'")
            sleep(5)
            browser_instance.find_element_by_xpath('//*[@id="acessar_form2"]').click()
            
        else:
            pass
        return
    
    
    def _doLogin(self, _convenio, _browser_instance:webdriver, _autenticacao:dict, _campos:dict):
        try:
            sleep(3)
            operador = _autenticacao['operador']
            senha = _autenticacao['senha']
            _browser_instance.find_element_by_xpath(_campos.get('campo_login')).send_keys(operador)
            _browser_instance.find_element_by_xpath(_campos.get('campo_senha')).send_keys(senha)
            _browser_instance.find_element_by_xpath(_campos.get('campo_captcha')).send_keys(self.__obterCaptchaValue(_convenio, _campos.get('objeto_captcha')))
            _browser_instance.find_element_by_xpath(_campos.get('botao_confirmar')).click()
            valueToConfirmAuthSuccess = _browser_instance.find_element_by_xpath('//*[@id="notificacao_de_login"]')
            
            if valueToConfirmAuthSuccess.text == "Operador autenticado com sucesso.":
                return True
            else:
                return False
        except Exception as ex:
            logging.exception("Authentication error : %s", ex)
