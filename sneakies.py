from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import discord
import json

with open('sneakies_info.json', 'r') as file:
    data = json.load(file)

Student_ID = data['Student_ID']
Password = data['Password']
API_TOKEN = data['API_TOKEN']
Attendance_QR_Channel = data['Attendance_QR_Channel']

def attendance(Student_ID, Password, Link, Channel_ID):
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    #Make sure it is the right channel
    
    if Channel_ID != Attendance_QR_Channel:
        return 0
    
    #URL checking before opening
    
    if Link[0:85] == "https://osc.mmu.edu.my/psc/csprd/EMPLOYEE/SA/c/N_PUBLIC.N_CLASS_QRSTUD_ATT.GBL?&GUID=":
        print('Attendance QR code')
    elif Link == "https://clic.mmu.edu.my/psp/csprd/?cmd=login&languageCd=ENG&":
        print('CLiC')
    elif Link == "https://online.mmu.edu.my/":
        print("MMU Online Portal")
        #remnant of a failed feature
        return 0
    else:
        print(f"{Link} is an Invalid URL!")
        return 0
    
    driver = webdriver.Chrome(options=options)
    

    title = driver.title

    #assert "CLiC Sign-In" in title
    
    if title == "CLiC Sign-In":
        driver.get(Link)
        sleep(3)
        
        driver.find_element(By.ID, "userid").send_keys(Student_ID)
        driver.find_element(By.ID, "pwd").send_keys(Password)
        driver.find_element(By.ID, "ps_submit_button").click()
        
        sleep(200)
        driver.quit()
        
    elif title == "Attendance Signin":
        print("In progress")
        
        guid = Link[85:122]
        
        
        driver.get(f"https://osc.mmu.edu.my/psc/csprd/EMPLOYEE/SA/c/N_PUBLIC.N_CLASS_QRSTUD_ATT.GBL?&GUID={guid}")
        sleep(3)
        
    
        driver.find_element(By.ID, "N_QRCODE_DRV_USERID").send_keys(Student_ID)
        driver.find_element(By.ID, "N_QRCODE_DRV_PASSWORD").send_keys(Password)
        driver.find_element(By.ID, "N_QRCODE_DRV_BUTTON1").click()
        
        sleep(60)
        driver.quit()
        
        print("Window Closed")
        
    else:
        print("Invalid URL: Exiting Webpage")
        driver.quit()
        print("Window Closed")

    '''if input() == "end":
        driver.quit() '''
    #sleep(45)

    #driver.quit()
#####################################################################################

intents = discord.Intents.default()
intents.message_content = True  # Allows your bot to read message content (use with caution)

client = discord.Client(intents=intents)

guild = discord.Guild

@client.event
async def on_message(message):
    message_content = message.content
    channel_id = message.channel.id
    attendance(Student_ID, Password, message_content, channel_id)

if __name__ == "__main__":
    client.run(API_TOKEN)
    
#Many gracious thanks to Boulama Kandine: https://blog.tinq.ai/read-discord-chats-with-python/ for 
#the discord bot tutorial
#My most appreciative thanks to Diego Molina at Sauce Labs for the Selenium guide: (link below)
#https://saucelabs.com/resources/blog/selenium-with-python-for-automated-testing