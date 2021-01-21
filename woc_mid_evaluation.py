#------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#------------------------------------------------------------------
import sys
import time
import csv
import itertools
#------------------------------------------------------------------
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from base64 import encodebytes
#------------------------------------------------------------------

#taking in email credentials
sender_email = input("Enter sender's email address: ")
password = input("Enter sender's email password: ")
reciver_email = input("Enter reciver's email address: ")


driver = webdriver.Chrome('Z:\chromedriver\chromedriver.exe')
driver.minimize_window()
driver.get("https://summerofcode.withgoogle.com/archive/2020/organizations/")
list_org = WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.XPATH, '/html/body/main/section/div/ul/li/a')))
#fetching data from all organizations

#getting all the links
list_link = []
for link in list_org:
    list_link = list_link + [link.get_attribute("href")]
tech_options = []

#scrapping data
scrp_data = open('scrapped data.csv', 'w', newline="")
writer = csv.writer(scrp_data, delimiter = ",")
for link in list_link:
    driver.get(link)
    org_name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/h3'))).text
    org_tech_stack = WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.XPATH, '/html/body/main/section[1]/div/div/div[2]/md-card/div/div[3]/ul/li')))
    tech_name = []
    for tech in org_tech_stack:
        tech_name = tech_name + [tech.text]
        if tech.text not in tech_options:
            tech_options = tech_options + [tech.text]
    row = [org_name, link , tech_name]
    writer.writerow(row)
scrp_data.seek(0)
scrp_data.close

print("Scrapping complete")
driver.quit()

while True:
    #taking user's input
    inp = []
    while True:
        ch = input("Enter tech stack you know[y-send mail/n-exit code]:- ")
        if ch == 'n':
            sys.exit()
        elif ch in tech_options:
            inp = inp + [ch]
        elif ch == 'y':
            if inp == []:
                print("you have not entered any tech:")
                if input("do you want to exit?[y/n]: ") == "n":
                    sys.exit()
                else :
                    continue 
            else:
                break
        else:
            print('That tech stack is not in any organisation')
    
    #making csv file according to user's input
    with open('Organisation based on your choices.csv','w+',newline = "") as file:
        scrp_data = csv.reader(open('scrapped data.csv','r'), delimiter = ",")
        od = csv.writer(file, delimiter=",")
        for i in inp:
            for r in scrp_data:
                if i in r[2]:
                    od.writerow(r)
        file.close

    #making mail
    m = MIMEMultipart()
    m["Subject"] = "Organisations for you"
    m["From"] = sender_email
    m["To"] = reciver_email
    body = '''<p><span style="color: #0000ff;"> Organisations found for your preferred technologies are in the attached file.</span></p>'''
    m.attach(MIMEText(body, 'html'))
    with open("Organisation based on your choices.csv","rb") as data:
        data.seek(0)
        part = MIMEBase('application', "octet-stream")
        part.set_payload(encodebytes(data.read()).decode())
        data.close()
        part.add_header('Content-Transfer-Encoding', 'base64')
        part.add_header('Content-Disposition', 'attachment; filename="Organisation based on your choices.csv"')
        m.attach(part)

    #sending mail
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    while True:
        try:
            server.login(sender_email, password)
            break
        except:
            print("email address or password is wrong")
            if input("want to change different email?[y/n]: ") == "n":
                sys.exit
            sender_email = input("Email address: ")
            password = input("Password: ")

    server.send_message(m)
    server.quit()
    print("mail sent")
    ch = input("want to check organistion with different technologies?[y/n]: ")
    if ch == 'n':
        sys.exit()
    ch = input("do you want to change email credentials?[y/n]: ")
    if ch == 'y':
        sender_email = input("Enter sender's email address: ")
        password = input("Enter sender's email password: ")
        reciver_email = input("Enter reciver's email address: ")

