#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
Created on 20200125
Update on 2021/jan
@author: Sandro Regis Cardoso
"""
 
import os
from time import sleep
import speech_recognition as sr


class Nutcracker(object):
    """
    @NOTE: Important keep in mind that Google Speech is build on Sphinx project
    @TODO: Work on Sphinx Voice to Text trainning to avoid Google service contracts;
           Build programming Test Case;
           Create design pattern for production deploy;
    """
    _name = "nutcracker"
    
    # __SPEECH_SERVICE_RUNNING = False
    
    def __init__(self):
        try:
            print("Criando objeto da ClasseA2")
            return
        except:
            raise Exception
     
    def __recarregarCaptcha(self, browserObject):
        browserObject.execute_script("javascript:location.reload();")
        sleep(5)
        return
     
    def __abrirMicrofone(self, objMic, objectRecognizer, browserObject, playerPath):
        with objMic as source:
            # Flag Global var
            self.__SPEECH_SERVICE_RUNNING = True
            print("Ajustando o tratamento de ruidos....")
            objectRecognizer.adjust_for_ambient_noise(source, duration=5)
            print("Ajustes concluidos....")
            player = browserObject.find_element_by_xpath(playerPath)
            player.click()
            print("Iniciando captura de audio....")
            rec = objectRecognizer.listen(source, phrase_time_limit=8)
        return rec
     
    def executarProcessamento(self, convenio, browserObject):
        try:
            if convenio == '2':
                captchaSize = 6
                inputCaptcha = '//*[@id="captcha"]'
                inputLogin = '//*[@id="usuario"]'
                inputSenha = '//*[@id="senha"]'
                playerLocation = '/html/body/div/div[1]/div[3]/form/div[3]/div[2]/a'
                btnEntrar = ''
            elif convenio == '1':
                captchaSize = 4
                self.__recarregarCaptcha(browserObject)
                inputCaptcha = '//*[@id="ctl00$body$ccCodigo"]'
                inputLogin = '//*[@id="ctl00_body_tbCpfCnpj"]'
                inputSenha = '//*[@id="ctl00_body_tbSenha"]'
                playerLocation = '//*[@id="linkOuvirAudio"]'
                captchaErrorLocation = '//*[@id="ctl00_body_cvCodigo"]'
                captchaErrorMessage = 'Código da imagem incorreto'
                btnEntrar = '//*[@id="ctl00_body_btEntrar"]'
            else:
                pass
            # Record Audio
            print("Carregando módulo de reconhecimento Voz....")
            recognizer = sr.Recognizer()
             
            # Call Speech recognition
            print("Iniciando o processamento do áudio....")
            self.__converterAudio(recognizer, playerLocation, captchaSize, browserObject, captchaErrorMessage,
                                  captchaErrorLocation, inputCaptcha, btnEntrar, inputLogin, inputSenha)
             
            # Set Free to new serv
            # self.__SPEECH_SERVICE_RUNNING = False
        except Exception as ex:
            raise ex
     
    def __obterChave(self):
        chave = '../gcp/SpeechRecognition-7dbbbb70a02d.json'
        return chave
     
    def __obterLoginSenha(self, convenio):
        dados = {}
        if convenio == '1':
            dados['login'] = '11580536000140'
            dados['senha'] = '186073'
        elif convenio == '2':
            dados['login'] = 'SANDRO_REGIS_CARDOSO'
            dados['senha'] = '186073'
        return dados
         
    def __converterAudio(self, objectRecognizer, playerLocation, captchaSize, browserObject, captchaErrorMessage,
                         captchaErrorLocation, inputCaptcha, btnEntrar, inputLogin, inputSenha):
        try:
            if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.__obterChave()
                 
            print("Reconhecimento de voz carregado....")
            audio = self.__abrirMicrofone(sr.Microphone(device_index=0), objectRecognizer, browserObject, playerLocation)
             
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            captchaValue = objectRecognizer.recognize_google(audio, language="pt-BR")
             
            if captchaValue.__contains__(' '):
                captchaValue = captchaValue.replace(' ', '')
             
            print(captchaValue)
                 
            if len(captchaValue) != captchaSize:
                self.__recarregarCaptcha(browserObject)
                self.__converterAudio(objectRecognizer, playerLocation, captchaSize, browserObject, captchaErrorMessage,
                                      captchaErrorLocation, inputCaptcha, btnEntrar, inputLogin, inputSenha)
            elif len(captchaValue) == captchaSize:
                loginSenha = self.__obterLoginSenha('1')
                 
                browserObject.find_element_by_xpath(inputLogin).send_keys(loginSenha.get('login'))
                browserObject.find_element_by_xpath(inputSenha).send_keys(loginSenha.get('senha'))
                browserObject.find_element_by_xpath(inputCaptcha).send_keys(captchaValue)
                browserObject.find_element_by_xpath(btnEntrar).click()
                try:
                    if browserObject.find_element_by_xpath(captchaErrorLocation).text == captchaErrorMessage:
                        self.__recarregarCaptcha(browserObject)
                        self.__converterAudio(objectRecognizer, playerLocation, captchaSize, browserObject, captchaErrorMessage,
                                              captchaErrorLocation, inputCaptcha, btnEntrar, inputLogin, inputSenha)
                    else:
                        print("Autenticacao concluída!")
                        del loginSenha
                        del audio
                        del captchaValue
                except ReferenceError:
                    pass
        except sr.UnknownValueError as uve:
            print("Desculpe, mas não consegui entender o seu áudio")
            self.__recarregarCaptcha(browserObject)
            self.__converterAudio(objectRecognizer, playerLocation, captchaSize, browserObject, captchaErrorMessage,
                                  captchaErrorLocation, inputCaptcha, btnEntrar, inputLogin, inputSenha)
            # raise uve
        except sr.RequestError as rerr:
            print("Houve um erro no sistema de processamento da sua voz. Comunique o meu mestre por favor!")
            raise rerr
    
    
    def __executarQuebraNozes(self):
        try:
            captcha = self.obterCaptcha(timewait=5)
            return captcha
        except Exception as ex:
            raise ex


