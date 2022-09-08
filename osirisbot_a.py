# osirisbot_a.py
#Arthur Lee 9/8/22


#importing libraries
import os
import discord
import random
import smtplib
from email.message import EmailMessage
import secrets

###defining global variables###
TOKEN = "FILLER" #token for bot used
GUILD = 12345 #change guild ID to guild ID of server

Femail='FILLER' #dm aRsin#000 for this
password='FILLER' #dm aRsin#000 for this

###important discord connection info###
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)
authtokens = {}

###events###

#connected
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#runs every time a user joins
@client.event
async def on_member_join(member):
    CHANNEL = client.get_channel("FILLER")#channel id
    await CHANNEL.send(get_welcome_message("<@!"+str(member.id)+">"))
    print(f'{member.name} has joined the server!')

#runs when a message is sent
@client.event
async def on_message(message: discord.Message):
    print("recieved a message!")
    if message.guild is None:#if message is a dm:
        print("recieved a dm!")
        if(message.content[-8:]=="@nyu.edu"):#if message is an nyu email
            print("recieved email")
            authtokens[str(message.author.id)]= sendSecToken(message.content)#emails security token and adds token to security token array
            await message.author.send("Sent an authentication token to your NYU email! Send me the code to get verified as an NYU Student!")
            print(message.content)
        if(str(message.author.id) in authtokens.keys() and authtokens[str(message.author.id)] == message.content):#if message is an authentication token
            print("recieved an authentication token")
            authtokens.pop(str(message.author.id))#removes token from array
            guild = client.get_guild(GUILD)#creates guild object
            member = guild.get_member(message.author.id)#creates member object using user id
            roletoadd = discord.utils.get(guild.roles, name="NYU Student")#gets role object
            await member.add_roles(roletoadd)#adds role to member
            print(message.content)
            await message.author.send("You have been verified as an NYU Student!")
        else: 
            return

def get_welcome_message(name):
    return message_start["Welcome "+name+"! DM me your NYU Email to get verified!"]

def sendSecToken(Temail):
    token = generateToken()#gets token
    msg = EmailMessage() #generates email object
    msg['Subject'] = "Osiris Discord Verification"
    msg['From'] = Femail
    msg['To'] =Temail
    msg.set_content(token)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:#sends email
        smtp.login(Femail, password)
        smtp.send_message(msg)
    return token

def generateToken():
    token = secrets.token_hex(16)
    return token


client.run(TOKEN)