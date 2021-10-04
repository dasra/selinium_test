import pickle
import smtplib
import re 
from datetime import date
import datefinder
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from selenium.webdriver.chrome.options import Options

import pandas as pd
from pandas import DataFrame
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException



#class for email alerts

class UscisOp1:
    def __init__(self,url_nm):
        path = r'./chromedriver' 
        extenpath1= r'./cfhdojbkjhnklbpkdaibdccddilifddb-3.9.5-Crx4Chrome.com.crx'
        #self.extenpath= extenpath
        options = Options()
        options.add_argument("--headless") #, "--disable-gpu", "--window-size=1920,1200","--ignore-certificate-errors","--disable-extensions","--no-sandbox","--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--no-sandbox')  
        # options.add_extension(extenpath1)
        self.driver = webdriver.Chrome(executable_path = path,options=options)
        #self.driver = webdriver.Chrome(executable_path=path,options=options)   
        self.url_nm=url_nm     
        self.driver.get(url_nm)
        #self.driver.maximize_window()
        #self.driver.implicitly_wait(45) 
        # self.driver.get("http://www.jonessoda.com/contests/back2school")
        #self.driver.find_elements_by_css_selector("receipt_number")
        
    def en_n_clk_1(self,rec_num):
        
        
        element1= self.driver.find_element_by_xpath('//*[@id="receipt_number"]')
        element1.send_keys(rec_num)        
        button=self.driver.find_element_by_xpath('//*[@id="landingForm"]/div/div[1]/div/div[1]/fieldset/div[2]/div[2]/input')
        button.click()          
        #first = False 
        #return (first)       
    def close_error(self):      
        button_cls=self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/button')
        button_cls.click()  
          
        
    def en_n_clk_2(self,rec_num):
        try:
            element1= self.driver.find_element_by_xpath('//*[@id="receipt_number"]')
            element1.send_keys(rec_num)       
            button=self.driver.find_element_by_xpath('//*[@id="caseStatusSearchBtn"]')
            button.click()
        except (NoSuchElementException):
            button=self.driver.find_element_by_xpath('//*[@id="landingForm"]/div/div[1]/div/div[1]/fieldset/div[2]/div[2]/input')
            button.click()
        #//*[@id="landingForm"]/div/div[1]/div/div[1]/fieldset/div[2]/div[2]/input
        

   
    def get_status(self):     
        try:
            status_txt=self.driver.find_element_by_xpath('/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/h1').text
            return(status_txt)
        except (NoSuchElementException):
            
            status_txt="no case found"
            return(status_txt)    
    def get_case(self):
        try:
            case_text=self.driver.find_element_by_xpath('/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/p').text
            return (case_text)  
        except (NoSuchElementException):
            case_text="no text found"  
            return (case_text) 
        #print(case_type)
    def close_conn(self):
        self.driver.close()
        self.driver.quit()    

    def send_email(self,gmailUser, gmailPassword, recipient, text,files,sub):
        msg = MIMEMultipart()
        msg['From'] = f'"USCIS 1 scan report " <{gmailUser}>'
        msg['To'] = recipient
        msg['Subject'] = sub
        msg.attach(MIMEText(text))
        
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(files, "rb").read())
        encoders.encode_base64(part)
        filename=files
        part.add_header('Content-Disposition', 'attachment; filename="uscisscan_10k.xlsx"')
        msg.attach(part)


        try:
            mailServer = smtplib.SMTP('smtp.gmail.com', 587)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(gmailUser, gmailPassword)
            mailServer.sendmail(gmailUser, recipient, msg.as_string())
            mailServer.close()
            print ('Email sent!')
        except:
            print ('Something went wrong...')
            
    r'''
    class UscisOp2:
        def __init__(self,url_nm,rec_num):
            status_list=[]
            path = r'C:\Users\dasra\Documents\python_projects\webscrap\chromedriver.exe'  
            extenpath1= r'C:\Users\dasra\Documents\python_projects\webscrap\server_file\stock_prediction\cfhdojbkjhnklbpkdaibdccddilifddb-3.9.5-Crx4Chrome.com.crx'
            #self.extenpath= extenpath
            options = Options()
            options.add_argument("--headless")
            options.add_argument('--no-sandbox')  
            # options.add_extension(extenpath1)
            self.driver = webdriver.Chrome(executable_path = path,options=options)
            #self.driver = webdriver.Chrome(executable_path=path,options=options)   
            self.url_nm=url_nm     
            self.driver.get(url_nm)
            #self.driver.maximize_window()
            #self.driver.implicitly_wait(45) 
            # self.driver.get("http://www.jonessoda.com/contests/back2school")
            #self.driver.find_elements_by_css_selector("receipt_number")
            element1= self.driver.find_element_by_xpath('//*[@id="receipt_number"]')
            element1.send_keys(rec_num) 
            button=self.driver.find_element_by_xpath('//*[@id="landingForm"]/div/div[1]/div/div[1]/fieldset/div[2]/div[2]/input')
            button.click()

            
        def get_status(self):     
            try:
                status_txt=self.driver.find_element_by_xpath('/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/h1').text
                return(status_txt)
            except NoSuchElementException:
                status_txt="no case found" 
                return(status_txt)    
        def get_case(self):
            try:
                case_text=self.driver.find_element_by_xpath('/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/p').text
                return (case_text)  
            except NoSuchElementException:
                case_text="no text found"  
                return (case_text) 
            #print(case_type)
        def close_conn(self):
            self.driver.close()
            self.driver.quit()    
    r'''

def isWordPresent(sentence, word):
      # To break the sentence in words
    s = sentence.split(" ")
 
    for i in s:
 
        # Comparing the current word
        # with the word to be searched
        if (i == word):
            return True
    return False
    
 
    
        
            



#function to return list 

def get_first_row(self,css_sel,selector):
            
    if (selector == 'css'):
        bought_list = self.driver.find_elements_by_css_selector(css_sel)
        bought_list = [link.text for link in bought_list]           
        splitted_0 = bought_list[0].splitlines()           
        return (splitted_0)
    elif (selector == 'path'):
        bought_list = self.driver.find_element_by_xpath(css_sel)
        bought_list = bought_list.get_attribute('innerHTML')
        return (bought_list)
    else:
        print('wrong selector selcted')
        
    
    #print("splitted 0 is", splitted_0)
def close_conn(self):
    self.driver.close()
    self.driver.quit()
    

#message function
def mes_text(self,spl_0,url,bs):
    if (bs == 'buy'):
        message = f"""
        BUY : Alert new insider trading detected   
        %s
        link to url
        %s
        """ % (spl_0, url)
    elif (bs == 'sale'):
        message = f"""
        SALE : Alert new insider trading detected   
        %s
        link to url
        %s
        """ % (spl_0, url)
    else:
        message="no buy or sale maybe option"
    return  (message)

#Email function 
def send_email(self,gmailUser, gmailPassword, recipient, message, sub):
    msg = MIMEMultipart()
    msg['From'] = f'"Inside Stock Analysis" <{gmailUser}>'
    msg['To'] = recipient
    msg['Subject'] = sub
    msg.attach(MIMEText(message))

    try:
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipient, msg.as_string())
        mailServer.close()
        print ('Email sent!')
    except:
        print ('Something went wrong...')

#functions for uscis


            

    