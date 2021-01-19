# -*- encoding: utf-8 -*-
#!/usr/bin/python3
"""
Created on 2020/jan
Update on 2021/jan
@author: Sandro Regis Cardoso
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOpts
from selenium.webdriver.common.keys import Keys
import sys

class WebDriverSingleton(type):
    _instances = {}
    _brwinst = object
    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(WebDriverSingleton, self).__call__(*args, **kwargs)
        return self._instances[self]
    
class WebBrowser(metaclass=WebDriverSingleton):
    _name="WebBrowser"
    
    _brwinst = object
    _webdriverInst = []
    __site_aberto = []
    __browserInstance = None
    
    def _openBrowser(self, browser_distro:str, url2open:str, recreate_instance=False)->object:
        
        try:
            if recreate_instance == True:
                self.__site_aberto.remove(url2open)
                
            if  url2open not in self.__site_aberto:
                self.__site_aberto.append(url2open)
                
                if browser_distro.upper() == 'FIREFOX':
                    opts = FirefoxOpts()
                    #opts.headless = True
                    #caps = webdriver.DesiredCapabilities().FIREFOX
                    #caps['marionette'] = True
                    exec_path='../firefox/geckodriver'
                    #self.self.__browserInstance = webdriver.Firefox(capabilities=caps, executable_path=exec_path, options=opts, desired_capabilities=caps, log_path='./firefox/')
                    self.__browserInstance = webdriver.Firefox(executable_path=exec_path, options=opts)
                elif browser_distro.upper() == 'CHROME':
                    chrome_options = ChromeOptions()
                    #chrome_options.add_argument("--headless")
                    self.__browserInstance = webdriver.Chrome(executable_path='../chrome/chromedriver', options=chrome_options)
                
                self.__browserInstance.get(url2open)
                return self.__browserInstance
        except Exception:
            pass

    def str_to_class(self, str):
        return getattr(sys.modules[__name__], str)
    
