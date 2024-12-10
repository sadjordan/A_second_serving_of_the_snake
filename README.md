sneakies V1.2
by Jordan

"To exist is to survive unfair choices"
- Khatun (The OA)


Some features:
- Auto fill your CLiC username and password (you will need to manually enter the OTP, I couldn't 
get the email thing to work)
- Auto sign in for your attendance
- It works by reading messages from a discord server
- Helps you maintain an unconventional sleep schedule
- Does not save you from those lecturers who do things manually
- Does not help you attend class
- QR code detection (in development)
- Malaysia recorded 1087 deaths by suicide in 2023
- If you would like to help, consider donating to Befrienders at https://www.befrienders.org.my/donate
- Lots of random quotes if you type in certain keywords

How to run:
- Download necessary modules and prepare the stuff needed.
- Create a discord server (or use an existing one)
- Designate a channel for the sending of the attendance qr code link
- Place the requested info into the json file (id, password, api token, channel id)
- Run
- Paste link into the designated channel
- Watch as magic happens (or sleep, but even I wouldn't trust my programs)

Notes:
- Won't stay online if the computer goes to sleep
- Channel ID is a number

Modules:
selenium
webdriver
discord.py
imaplib
email
audioop-lts

(I think that's it)

Currently runs on python 3.13

A couple things needed:
- The above modules
- A discord bot must have the permissions necessary to view messages on the discord server where the 
attendance qr will be sent (look up a quick tutorial on how to make one, it is really easy!)
- The API token as well
- Your student id and password (it's all stored locally, I'm not phishing you I promise)
- The discord channel where the links are being sent
- Active and stable internet connection
- Decent amount of ram because we are using chrome
- Python virtual environment if you can't download modules globally
- Oh and since this uses a json file, you need to cd into the folder where it is located

Special thanks to Yen Hong for spreading the amazing Selenium to me and Izzmin from MMU for his 
JSON file inspiration.
