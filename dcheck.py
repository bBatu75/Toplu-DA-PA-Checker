#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cfonts import render, say
from itertools import islice
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as soup
import xlsxwriter
from os import system
from colorama import init, Fore, Back, Style
import getmac
import sys
import time
import requests
import subprocess    

def chunk(it, size):
    it = iter(it)
    return list(iter(lambda: tuple(islice(it, size)), ()))



output = render('DA - PA|CHECKER', colors=['#3D63D5', '#07C8F9'], align='left' )
dosyaokunuyor = render('Dosya|Okunuyor...', colors=['#3D63D5', '#07C8F9'], align='left')
dosyaokaydedildi = render('Dosya|Kaydedildi', colors=['#3D63D5', '#07C8F9'], align='left')
print(output)
print(Fore.CYAN + "R10 = Batu75")
dosyaList=input("Site listesi(ÖRN: liste.txt): ")
try:
    file=open(dosyaList,"r")
    listS=file.read()
    file.close()
except:
    print("Dosya okunurken hata oluştu.")
    system("pause >nul")
    exit()


data = []

listSP=list(set(listS.split("\n")))

for k in chunk(listSP,20):

    listAS=""
    for i in k:
        listAS=listAS+i+"\n"
 
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("disable-crash-reporter")
    options.add_argument("no-sandbox")
    options.add_argument("disable-crash-reporter")
    options.add_argument("disable-extensions")
    options.add_argument("disable-in-process-stack-traces")
    options.add_argument("disable-logging")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("log-level=3")
    options.add_argument("output=/dev/null")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
 
    browser = webdriver.Chrome(chrome_options=options)
    browser.get("https://www.softo.org/tool/domain-authority-checker")
    urlList = browser.find_element("xpath",'//*[@id="urls"]')
    urlList.send_keys(listAS)
    time.sleep(1)
    cAbutton=browser.find_element("xpath",'//*[@id="checkBtnCap"]')
    cAbutton.click()
    time.sleep(10)

    system("cls")

    print(dosyaokunuyor)
    source = soup(browser.page_source,"html5lib")

    browser.close()

    table = source.find('table', attrs={'id':'example'})
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])




xlsxF = xlsxwriter.Workbook('sonuc.xlsx')
xlsxWS = xlsxF.add_worksheet()
xlsxWS.set_column(0, 0, 80)

f1=xlsxF.add_format({'bg_color':'#ffff00', 'font_size':16}) #RENK
f2=xlsxF.add_format({'bg_color':'#ffff00', 'font_size':11}) #renk2

xlsxWS.write('A1', 'Site Adı',f1)
xlsxWS.write('B1', 'DA',f2)
xlsxWS.write('C1', 'PA',f2)
xlsxWS.write('D1', 'SS',f2)
xlsxWS.write('E1', 'MR',f2)






say=2
for i in sorted(data, key=lambda x: int(x[2]), reverse=True):
    xlsxWS.write(f'A{say}', f'{i[1]}')
    xlsxWS.write(f'B{say}', f'{i[2]}')
    xlsxWS.write(f'C{say}', f'{i[3]}')
    xlsxWS.write(f'D{say}', f'{i[4]}')
    xlsxWS.write(f'E{say}', f'{i[5]}')
    say+=1


xlsxF.close()

system("cls")
print(dosyaokaydedildi)

print(Fore.CYAN + "Dosya \"sonuc.xlsx\" adıyla kaydedildi.\nÇıkmak için herhangi bir tuşa basınız.")
print("R10 = Batu75")
system("pause >nul")