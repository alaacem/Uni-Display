import pip
import imp
from selenium import webdriver
import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from tkinter import messagebox
import time
import copy
from subprocess import run
import signal
import os
import logging
import re
import json
import shutil
import sys
from datetime import datetime, date
#from webdriver_manager.chrome import ChromeDriverManager

abspath = os.path.abspath(__file__)    # To make currently path as default path
dname = os.path.dirname(abspath)
os.chdir(dname)

global dispSpar
global driver
filename='set.json'
linux=True
firth=True


def create_backup(json_file):
    # Create backup folder if it doesn't exist
    backup_dir = 'Allbackup'

    # Get the full path of the file to backup
    file_path = os.path.abspath(json_file)

    # Get the backup file name and path
    backup_filename = os.path.basename(file_path) + '.bak'
    backup_path = os.path.join(backup_dir, backup_filename)

    # Load the JSON data from the original file
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Write the JSON data to the backup file
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    print(f"JSON backup created: {backup_path}")
def copy_file_with_encoding(src_file, dst_file, encoding='utf-8'):
    with open(src_file, encoding=encoding) as fsrc, open(dst_file, mode='w', encoding=encoding) as fdst:
        for line in fsrc:
            fdst.write(line)
def restore_from_backup(filename):
    # Get the full path of the file to restore
    file_path = os.path.abspath(filename)

    # Get the backup file name and path
    backup_dir = 'Allbackup'
    backup_filename = os.path.basename(file_path) + '.bak'
    backup_path = os.path.join(backup_dir, backup_filename)

    # Check if the backup file exists
    if not os.path.exists(backup_path):
        print(f"Backup file {backup_path} does not exist")
        return

    # Restore the file from the backup
    shutil.copyfile(backup_path, file_path)
    print(f"File restored from backup: {file_path}")
def load_variables():
    # Read variables from the JSON file
    #create_backup(filename)
    try:

        with open(filename, 'r+',encoding='utf-8') as f:

            data = json.load(f)
            for key, value in data.items():
                #print('key:',key)
                #print('value:', value)
                globals()[key] = value
    except Exception as e:
        print(f"Error creating backup file: {e}")
        os.remove('set.json')
        restore_from_backup(filename)
        load_variables()
def update_variables(key,value):
    # Read the contents of the file
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updates={}
    updates[key]=value
    data.update(updates)

    # Write the updated data back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    create_backup(filename)





def start_display():
    global driver

    pathrsp = 'file:///home/hiwiadmin/pyDisplay/Site1/index.html'
    pathwind= 'C:/Users/AlaaShaar/Priv/Rasp/pyDisplay/Site1/index.html'
    drivpathwin="pyDisplay/driver/chromedriver.exe"
   # drivpathlin = "driver/chromedriver"
    drivpathlin = "/usr/lib/chromium-browser/chromedriver"
   # os.chmod(drivpathlin, 755)
    #service = ChromeService(executable_path=ChromeDriverManager().install())

    # Set up the Chrome driver with options
    if linux :
        driver_path = drivpathlin   # Path to the Chrome driver executable
    else:
        driver_path = pathwind 
    options = webdriver.ChromeOptions()
    options.add_argument("--kiosk")                           # Enable kiosk mode
    options.add_argument("--window-size=1920,1080")           # Set window size
    options.add_argument("--disable-extensions")              # Disable browser extensions
    options.add_argument("--disable-infobars")                # Disable infobars
    options.add_argument("--no-sandbox")                      # Disable the sandbox
    options.add_argument("--disable-dev-shm-usage")           # Disable shared memory usage
    options.add_experimental_option("excludeSwitches", ['enable-automation']);

    driver = webdriver.Chrome(driver_path, options=options)
    #driver = webdriver.Chrome(service=service,options=options)
    # Set the default zoom level
    driver.get('chrome://settings/')
    driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.67);')
    
    # Load the HTML website and display it in kiosk mode
    driver.get(pathrsp)


"""
Woche ist a List contains 5 Element. and every one contains 3 element :
1. Day Name
2. The first Colum on The Table
3. The Second Coum on The Table
for Example : ["Montag","09:30 - 13:00","14:00 - 16:30"]

Functions List:

- webFramer() :
1.Take the HTML form URL and take the table from the spicel ID
2.Split the table to days and Time and with divide to multiple times
3.Save all Times to woche List
4. Send the List to compareJson(tab) to compare the current Time and The Time on the Page
5. if Times has been changed, WebFrame send the woche list to updateLocal1(woche) and refresh the driver

- status(newStat)
1. Take the new Statu (Geschlossen , Gleich Züruck , Geöffnet ) as Parameter
2. take the Backup Website and changed the HTML TEXT in the Local Website to the new Statu and save it

- css(farbe)

1. Take the new Color (rot , Green , Gelb ) as Parameter
2. take the Backup CSS file from theWebsite and changed the CSS TEXT in the Local Website to the new Color and save it


- schlies()
- gleich()
- geoff()
1. Send new statu and color and refresh

- updateLocal1()
Take the table from the local Website and changed to current Times
- anzeig()
1.Main function
2. Has the Loop for Tastaur function and webFramer and Display Sparmodus
- timetst()
1. refresh the current Time and run a current script to power on or off the display
- tastatur()
1 Read the text File that connect with the Neu.py and py2.py and changed the statu depend on the number in that txt file
('2','3','4')
- json_d(wochetab,filename)
save the current Table to a json file
- compareJson(tab)
compare current table with the old one
- backup()
if shit habend backup take the backups file and replace it with the current files
- in_between(now, start, end)
check if time in_between power on and off time

"""


def webFramer():
    import requests
    global frame_id
    from bs4 import BeautifulSoup
#     url = 'https://www.hs-kl.de/hochschule/servicestellen/rechenzentrum/servicepoints-und-hilfe'
# 
#     try:
#         Error=False
#         while 1:
#             try:
#                 page = requests.get(url)
#             except :#(requests.exceptions.ConnectTimeout,requests.exceptions.ConnectionError):
#                    print("requests.exceptions.ConnectTimeout")
#                    continue
#             break
#         divide = '&'
# 
#         brk = False
#         ####______________
#         soup = BeautifulSoup(page.text, 'html.parser')
#         #table = soup.find('div', attrs={'class': 'table-responsive'})
# 
#         table = soup.find('div', attrs={'id': frame_id})
#        
#         gdd = table.find('p')
# 
#         for gdds in gdd:
#             #print(gdds)
#             if gdds.text.__contains__('vom') or gdds.text.__contains__('Vom') or gdds.text.__contains__('öffnungszeiten')or gdds.text.__contains__('Öffnungszeiten'):
#                     exGD(gdd.text)
#                     break
#         #exGD(gdd.text) # Extract 5555555555555555555555555
# 
#         table_body = table.find('tbody')
#         rows = table_body.find_all('tr')
#     except Exception as e:
#         print("An unexpected error occurred: ", e)
#         Error=True
#         pass
# 
#     if Error==False:
#         next = False
#         index = 0
#         wochetemp =copy.deepcopy(woche)
# 
#         for row in rows:
#             cols = row.find_all('td')
# 
#             #print("_______8")
#             for col in cols:
#                 cols1 = col.find('td')
#                 text_temp = col.get_text(strip=True)
#                 if text_temp.__contains__('Uhr'):
#                     #print("YES")
#                     text_temp = text_temp.replace('Uhr', '')
#                     #print(type(text_temp))
#                 if next == True:
#                     if divide in text_temp:
#                         x = text_temp.split(divide)
#                         woche[index][1] = x[0]
#                         woche[index][2] = x[1]
#                         print(f'x[1,2] mit\n{text_temp}')
#                     else:
#                         woche[index][1] = text_temp
#                         woche[index][2]=""
#                         print(f'x[1,2] Ohne\n{text_temp}')
# 
#                     next = False
#                 else:
#                     for i in range(0, 5):
#                         if text_temp in woche[i]:
#                             print(f"Tag {text_temp}")
#                             index = i
#                             #print(text_temp, index)
#                             next = True
    #nG=exGD(gdd.text)
   # print("gdd.text",gdd.text)
    #print("Ng",nG)
   # if nG != 0:

      #  datum(nG)                        
    if faei or is_weekend() or man:
        
        if compareJson(woche):
             updateLocal1(woche)
             
             #log(woche, 'woche')
             update_variables("woche",woche)
             driver.refresh()
             #print("JAAAA")

def exGD(gdatum):
    global GString , firth
    # gDat: Öffnungszeiten vom 27.02. - 03.03.2023:
    # GString 27.02. - 03.03.2023:
    # gdatum ['27.02. ', ' 03.03.2023']
    # gdatum1 27.02.
    # gdatum2 03.03.2023
    # match1 27.02.
    # match2 03.03.2023
    m = re.search(r"\d", gdatum)

    tempGst=gdatum[m.start():]
  
  #  print("tempGst",tempGst)
    if GString != tempGst or firth == True:
        firth = False
        GString = tempGst
        update_variables("GString",GString)
        print("GString=",GString)

        
        tempgdatum = str(GString.replace(':', ''))
        gdatum = tempgdatum.split('-')
        gdatum1 = gdatum[0]
        gdatum2 = gdatum[1]

        pattern = r"\d{2}\.\d{2}"

        match1 = re.search(pattern, gdatum1).string
        match2 = re.search(pattern, gdatum2).string
        print("match2:",match2)
        print("match1:",match1)
        if match1 and match2:
            # print(match1)
            pas=extract(match1,match2)
            print("pas=",pas)
            if faei or is_weekend():
                print("match found.",GString)
                datum(GString)
        else:
            print("No match found.")
            return 0
            #print("ab_date", ab_date)
            #print("bis_date", bis_date)
            #print("cur", current_date)
def extract(match1,match2):
    global faei
    #errordate = False
    gt = match1.split('.')
    bt = match2.split('.')

    gtd = int(gt[0])
    gtm = int(gt[1])
    gty = int(gt[2])

    btd = int(bt[0])
    btm = int(bt[1])
    bty = int(bt[2])
    try:
        ab_date = datetime(gty, gtm, gtd)
        bis_date = datetime(bty, btm, btd)
        errordate = True
        print("start:",ab_date,"end:",bis_date)
        update_variables("gty", gty)
        update_variables("gtm", gtm)
        update_variables("gtd", gtd)
        update_variables("bty", bty)
        update_variables("btm", btm)
        update_variables("btd", btd)





    except Exception as e:
        errordate = False

        print("An unexpected error occurred: extract(match1,match2)", e)

    if errordate:
        xbol=compare_date(ab_date, bis_date)
        if xbol != faei :
            faei=xbol
            update_variables("faei",faei)
            print("faei:",faei)
            return faei
    else:
            return 2
def compare_date(start_date, end_date):
    current_date = date.today()
    #print("start:",start_date,"cur:",current_date,"end:",end_date)
    if start_date.date() <= current_date <= end_date.date():

        return True
    else:
        return False
def datum(NDat):
    print("Ndat",NDat)
    global act_date
    if NDat != act_date:
        print("Ndat",NDat)
        print("act_date",act_date)

        try:
            # Open the file for reading and writing
            with open('Site1/index.html', 'r+', encoding='utf-8') as my_file:
                # Read the file contents and create a soup object
                soup = BeautifulSoup(my_file.read(), 'html.parser')

                # Find the h1 element with class 'gd' and modify its content
                h1 = soup.find('h1', attrs={'class': 'gd'})
                h1.string = NDat

                # Move the file pointer to the beginning of the file and write the modified soup object
                my_file.seek(0)
                my_file.write(str(soup))

            # Close the file
            with open('Site1/index1.html', 'r+', encoding='utf-8') as my_file2:
                # Read the file contents and create a soup object
                soup = BeautifulSoup(my_file2.read(), 'html.parser')

                # Find the h1 element with class 'gd' and modify its content
                h1 = soup.find('h1', attrs={'class': 'gd'})
                h1.string = NDat

                # Move the file pointer to the beginning of the file and write the modified soup object
                my_file2.seek(0)
                my_file2.write(str(soup))

            # Close the file
        except IOError as e:
            print("An error occurred while reading or writing the file: datum(NDat) ", e)

        except Exception as e:
            print("An unexpected error occurred: datum(NDat)", e)


        
        act_date =NDat
        update_variables("act_date",act_date)
        driver.refresh()
def status(newStat):
    import os

    pathhtml = 'Site1/index.html'
    pathhtml1 = 'Site1/index1.html'
    my_file = open('Site1/index1.html', 'r+', encoding='utf-8')

    string_list = my_file.readlines()
    #print(string_list[10])
    stringS="u-text-4"
    statu=["Geschlossen","Geöffnet","gleich zurück"]

    for line in string_list:
        if stringS in line:
            for txt in statu:
                if txt in line:
                    #print(txt)
                    index = string_list.index(line)
                    string_list[index]=line.replace(txt,newStat)
                    #print(index)
    my_file.close()
    time.sleep(1)
    with open(pathhtml,'w', encoding='utf-8') as f:
        f.writelines(string_list)
        
        f.close()
    with open(pathhtml1,'w', encoding='utf-8') as f:
        f.writelines(string_list)
        f.close()
    
    
    log(newStat, 'Statu')
def css(farbe):
    import sys
    import os

    stringS = "--red"

    pathCss1 = 'Site1/Home1.css'
    pathCss = 'Site1/Home.css'

    my_file = open(pathCss1, 'r+', encoding='utf-8')

    string_list = my_file.readlines()


    statu = ["Geschlossen", "Geöffnet", "gleich zurück"]

    for line in string_list:
        if line.__contains__(stringS):
            index = string_list.index(line)

            print("--red:"+farbe)
            string_list[index] ="--red:"+farbe
            break

    my_file.close()


    with open(pathCss, 'w',encoding='utf-8') as f:
        f.writelines(string_list)
        f.close()


    with open(pathCss1, 'w',encoding='utf-8') as f:
        f.writelines(string_list)
        f.close()
def schlies():
    global jetztstatu
    status(statu[0])
    css(rot)
    driver.refresh()
    #messagebox.showinfo("Gleich")
    jetztstatu=statu[0]
def gleich():
    global jetztstatu
    status(statu[2])
    css(gelb)
    driver.refresh()
    jetztstatu=statu[2]
def geoff():
    global jetztstatu
    status(statu[1])
    css(green)
    driver.refresh()
    jetztstatu=statu[1]
def updateLocal1(woche):
    #woche = [["Montag", "", ""], ["Dienstag", "", ""], ["Mittwoch", "", ""], ["Donnerstag", "", ""],["Freitag", "", ""]]
    from bs4 import BeautifulSoup
    import os
    import requests
    #print(woche[0][1])

    try:
        print("Update")
        #base = os..pathdirname(os.path.abspath(__file__))
        html1 = open('Site1/index1.html','r+', encoding='utf-8')
        html = 'Site1/index.html'
        html1PATH ='Site1/index1.html'
        soup = BeautifulSoup(html1, 'html.parser')
        soup.find("td", class_="T1").string = woche[0][1]
        soup.find("td", class_="T2").string = woche[1][1]
        soup.find("td", class_="T3").string = woche[2][1]
        soup.find("td", class_="T4").string = woche[3][1]
        soup.find("td", class_="T5").string = woche[4][1]

        soup.find("td", class_="T01").string = woche[0][2]
        soup.find("td", class_="T02").string = woche[1][2]
        soup.find("td", class_="T03").string = woche[2][2]
        soup.find("td", class_="T04").string = woche[3][2]
        soup.find("td", class_="T05").string = woche[4][2]
        html1.close()

        with open(html1PATH, 'w', encoding='utf-8') as f:
            soup = str(soup)
            f.write(soup)
            f.close()
        with open(html, 'w', encoding='utf-8') as f:
            soup = str(soup)
            f.write(soup)
            f.close()

    except AttributeError:
        print("AttributeError ERROR Cannot get Data")
        backup()
        pass
def timetst():
    global Aus,An,Start,chk
    from time import strftime
    from datetime import datetime
    import os
    from subprocess import run                              #################
    now = datetime.now()  # current date and time
    time = now.strftime("%H:%M:%S")
    #print("time:", time)
    # print(strftime("%H"))
    stunde = int(strftime("%H"))

    if in_between(stunde,Aus,An):
        if chk==True:

            os.system('xrandr -display :0.0 --output HDMI-2 --off')         #################
            print("Aus")
            chk=False
    else:
       if chk==False:
           os.system('xrandr -display :0.0 --output HDMI-2 --mode 1920x1080 --rate 60 --rotate left')       #################
           print("on")
           chk=True
def tastatur():
    global jetztstatu
    with open("keypre.txt",'r+') as f:
        lines=f.readlines()
      #print(lines[0])
        try:
              if lines[0]=="2" and jetztstatu!=statu[1]:
                  geoff()

              if lines[0]=="3" and jetztstatu!=statu[2]:
                  gleich()
              if lines[0]=="4" and jetztstatu!=statu[0]:
                  schlies()
        except IndexError:
                print("File is Empty Tastaur")
                lines.append("4")
                pass
def json_d(wochetab,filename):
    import json

    with open(filename,'r+',encoding='utf-8') as json_file:
        wochedata=json.load(json_file)
        for x in wochetab:
            print(x)
            temp=x[0]
            wochedata[temp][0]=x[1]
            wochedata[temp][1]=x[2]
        json_file.seek(0)
        json.dump(wochedata, json_file ,indent = 4)
        json_file.truncate()
def compareJson(tab):
    import json
    print("::::::::::::::::::::::::")
    print(tab)
    print("::::::::::::::::::::::::")

    temp_name = 'tempwoche'
    ext = 'json'

    jsontemp = f'{temp_name}.{ext}'



    json_file_temp= open('tempwoche.json','r+')
    tempdata=json.load(json_file_temp)
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for x in range(0,5):
       tag=tab[x][0]
       for i in range (0,2):
             #print(tag,"::", "tab::",tab[x][i+1],"temp::",tempdata[tag][i])
            # print("________")
             if tab[x][i+1] != tempdata[tag][i]:
                 json_d(woche, jsontemp)
                 return True
def backup():
    import os
    import shutil
    import time
    root_src_dir = '/home/hiwiadmin/pyDisplay/Site1_v0/Site1'
    root_dst_dir = '/home/hiwiadmin/pyDisplay/Site1'
    import zipfile
    try:
        shutil.rmtree(root_dst_dir)
    except FileNotFoundError:
        print("Backup Org Folder dont found")
    with zipfile.ZipFile('Site1BK.zip','r') as source:
        source.extractall()
    driver.refresh()
def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else: # over midnight e.g., 23:30-04:15
        return start <= now or now < end
def setup_logger(name, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    log_file = name + '.log'
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
def log(msg, typ):

    logger = setup_logger(typ)
    logger.info(msg)
def is_weekend():
    today = datetime.today().weekday() # get the current day of the week as an integer (0 = Monday, 6 = Sunday)
    if today == 5 or today == 6:
        return True # return True if it's Saturday or Sunday
    else:
        return False

if __name__=="__main__":

    

    
    GString=""
    act_date=""
   # update_variables("GString",GString)
   # update_variables("act_date",act_date)
    load_variables()
    
    start_display()

    tastatur()

    while 1:
        webFramer()
        if disSpar:
            timetst()
        tastatur()

