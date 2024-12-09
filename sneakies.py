from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import discord
import json
from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import os

with open('sneakies_info.json', 'r') as file:
    data = json.load(file)
    
#print(data)

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
        title = "Attendance Signin"
    elif Link == "https://clic.mmu.edu.my/psp/csprd/?cmd=login&languageCd=ENG&":
        print('CLiC')
        title =  "CLiC Sign-In" 
    elif Link == "https://online.mmu.edu.my/":
        print("MMU Online Portal")
        #remnant of a failed feature
        return 0
    else:
        print(f"{Link} is an Invalid URL!")
        return 0
    

    #assert "CLiC Sign-In" in title
    
    if title == "CLiC Sign-In":
        driver = webdriver.Chrome(options=options)
        driver.get(Link)
        sleep(3)
        
        driver.find_element(By.ID, "userid").send_keys(Student_ID)
        driver.find_element(By.ID, "pwd").send_keys(Password)
        driver.find_element(By.ID, "ps_submit_button").click()
        
        sleep(200)
        driver.quit()
        
    elif title == "Attendance Signin":
        print("In progress")
        
        #guid = Link[85:121]
        #print(f'guid: {guid}')
        
        driver = webdriver.Chrome(options=options)
        driver.get(Link)
        sleep(2)
    
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


def qr_code(filename):
    print("In development")
    
    # Load the QR code image
    image_path = f"/Users/jordan/Desktop/The_Grand_Archive/Projects/A_second_serving_of_the_snake/qr_codes/{filename}"
    #/Users/jordan/Desktop/The_Grand_Archive/Projects/A_second_serving_of_the_snake/qr_codes/220px-QR_code_for_mobile_English_Wikipedia.png
    #/Users/jordan/Desktop/The_Grand_Archive/Projects/A_second_serving_of_the_snake/qr_codes/220px-QR_code_for_mobile_English_Wikipedia.png
    
    '''if os.path.exists(image_path):
        print("File exists!")
    else:
        print("File not found!")'''
        
    try:
        image = cv2.imread(image_path)
        #b,g,r = cv2.split(image)
        #cv2.imshow("B", b)
        #cv2.imshow("G", g)
        #cv2.imshow("R", r)
        #cv2.imshow("Image", image)
        #print(image_path)
        if image is None:
            print(f"Image not found: {image_path}")
            return 0
    except Exception as e:
        print(f"Error opening image: {e}")
        return 0
    
    
    #detector = cv2.QRCodeDetector()
    #print (detector)

    #link, trash, moretrash = detector.detectAndDecode(a)
    
    detector = cv2.QRCodeDetector()
    #print (detector)
    link, trash, moretrash = detector.detectAndDecode(image)
    #print(link)
    if link != '':
        print(f"Detected QR Code: {link}")
        return link
    else:
        return 0

intents = discord.Intents.default()
intents.message_content = True  # Allows your bot to read message content (use with caution)

client = discord.Client(intents=intents)

guild = discord.Guild

@client.event
async def on_message(message):
    message_content = message.content
    channel_id = message.channel.id
    attendance(Student_ID, Password, message_content, channel_id)
    
    print("Testing")
    
    if message.attachments:  # If there are attachments
        for attachment in message.attachments:
            if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):  # Check if it's an image
                print(f"Image detected: {attachment.filename} (URL: {attachment.url})")
                # You can download or process the image here if needed
                await attachment.save(f"/Users/jordan/Desktop/The_Grand_Archive/Projects/A_second_serving_of_the_snake/qr_codes/{attachment.filename}")  # Save the attachment locally
                print(f"Image saved as: /Users/jordan/Desktop/The_Grand_Archive/Projects/A_second_serving_of_the_snake/qr_codes/{attachment.filename}")
                
                qr_run = qr_code(attachment.filename)
                channel = client.get_channel(channel_id)
                if qr_run != 0:
                    await channel.send(qr_run)
                else:
                    await channel.send("Link could not be read from QR code")
            else:
                print(f"Non-image attachment detected: {attachment.filename} (URL: {attachment.url})")
    
if __name__ == "__main__":
    client.run(API_TOKEN)
    
#Many gracious thanks to Boulama Kandine: https://blog.tinq.ai/read-discord-chats-with-python/ for 
#the discord bot tutorial
#My most appreciative thanks to Diego Molina at Sauce Labs for the Selenium guide: (link below)
#https://saucelabs.com/resources/blog/selenium-with-python-for-automated-testing