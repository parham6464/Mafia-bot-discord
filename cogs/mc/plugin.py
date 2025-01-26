from __future__ import annotations
from http.client import HTTPException
from os import scandir
from urllib import response

from core.bot import Bot
from typing import Any, Optional , Callable , Literal , Union
from datetime import timedelta , datetime
from cogs.cog_config import Plugin
from discord.ext import commands , tasks 
from humanfriendly import parse_timespan , InvalidTimespan
from discord import app_commands , User , utils as Utils , CategoryChannel , ForumChannel , PartialMessageable , Object , TextChannel , Thread , Permissions , StageChannel , VoiceChannel , Role , Attachment , Forbidden , Color
from pytz import UTC
from aiohttp import ClientSession
import aiohttp
import discord
import config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from easy_pil import Editor , Canvas, load_image_async , Font
from config import TOKEN
import requests
from typing import Union 
from datetime import timedelta , datetime
from core.embed import Embed
from core.models import Giveawaymodel
from views.giveaway import GiveawayView
import time
import humanfriendly
import asyncio
from discord import ui
from discord import Colour
import random
import http.client
import json

cluster = MongoClient("mongodb+srv://asj646464:8cdNz0UEamn8I6aV@cluster0.0ss9wqf.mongodb.net/?retryWrites=true&w=majority")
# Send a ping to confirm a successful connection
db = cluster["mafia"]
collection = db["mafia"]
new_GUILD = db['guilds']

########################################## class win shahrvand
class WinShahrvand(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(label='ارسال نتایج' , custom_id='sendresult' , style=discord.ButtonStyle.primary)
    async def sendresult(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                embed=discord.Embed(
                    title='نتایج بازی',
                    description='تیم شهروند برنده بازی شد لیست پلیر ها به شرح زیر است',
                    timestamp=datetime.now(),
                    color= 0x0554FE
                )
                mafia_players = find1['mafia_players']
                shahr_players = find1['shahr_players']
                hazf_mafia = find1['hazf_mafia']
                hazf_shahrvand= find1['hazf_shahrvand']

                for key , value in shahr_players.items():

                    user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key))
                    embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}' , inline=False)

                for key , value in hazf_shahrvand.items():

                    user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key))
                    embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}' , inline=False)


                for key , value in mafia_players.items():
                    
                    user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key))
                    embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}' , inline=False)

                for key , value in hazf_mafia.items():

                    user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key))
                    embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}' , inline=False)
                
                channel_players = find1['channel_players']
                channel_send = discord.utils.get(interaction.guild.text_channels , id=channel_players)
                msg_id = find1['msg_embed']

                if channel_send is not None:
                    await channel_send.send(embed=embed)
                    await interaction.response.send_message('ارسال شد و بازی تمام شد' , ephemeral=True)
                    collection.delete_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3})
                else:
                    await interaction.response.send_message('چنل پلیر ها یافت نشد' , ephemeral=True)
                    collection.delete_one({"server_id":interaction.guild_id , "god":interaction.user.id, 'part':3})
                
            else:
                await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)



########################################### class win Mafia
class WinMafia(ui.View):
    def __init__(self , bot:Bot ):
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(label='ارسال نتایج' , custom_id='sendresult' , style=discord.ButtonStyle.primary)
    async def sendresult(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                embed=discord.Embed(
                    title='نتایج بازی',
                    description='تیم مافیا برنده بازی شد لیست پلیر ها به شرح زیر است',
                    timestamp=datetime.now(),
                    color= 0x0554FE
                )
                mafia_players = find1['mafia_players']
                shahr_players = find1['shahr_players']
                hazf_mafia = find1['hazf_mafia']
                hazf_shahrvand= find1['hazf_shahrvand']

                for key , value in shahr_players.items():

                    user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key) , inline=False)
                    embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}')

                for key , value in hazf_shahrvand.items():

                    user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key) , inline=False)
                    embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}')


                for key , value in mafia_players.items():
                    
                    user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key) , inline=False)
                    embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}')

                for key , value in hazf_mafia.items():

                    user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key) , inline=False)
                    embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}')
                
                channel_players = find1['channel_players']
                channel_send = discord.utils.get(interaction.guild.text_channels , id=channel_players)
                msg_id = find1['msg_embed']

                if channel_send is not None:
                    await channel_send.send(embed=embed)
                    await interaction.response.send_message('ارسال شد و بازی تمام شد' , ephemeral=True)
                    collection.delete_one({"server_id":interaction.guild_id , "god":interaction.user.id, 'part':3})
                else:
                    await interaction.response.send_message('چنل پلیر ها یافت نشد' , ephemeral=True)
                    collection.delete_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3})
                
            else:
                await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

#############################################################ray giri mojadad
class RayGiriMojadad(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(label='رای گیری مجدد' , custom_id='revote' , style=discord.ButtonStyle.primary)
    async def revote(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):

                total_players  = find1['total_players']
                shahrhvand_players = find1['shahr_players']
                mafia_players = find1['mafia_players']
                raygiri = find1['raygiri']
                channel_players = find1['channel_players']
                msg_raygiri = find1['msg_raygiri']
                hazf_mafia = find1['hazf_mafia']
                hazf_shahrvand = find1['hazf_shahrvand']
                tedade_ray = find1['tedade_ray']
                reply_count = find1['reply_count']
                reply_players = find1['reply_players']
                reply_players=[]
                print (f'22222 {tedade_ray}')

                channel_send = discord.utils.get(interaction.guild.text_channels , id=channel_players)

                msg = ''
                async for messager in channel_send.history(limit=None):
                    if messager.id == msg_raygiri:
                        msg = messager
                
                if len(raygiri) == (len(shahrhvand_players) + len(mafia_players)):
                    all_scores = []
                    for i in tedade_ray.values():
                        all_scores.append(i)
                    
                    if len(tedade_ray)!=0:
                        max_score = max(all_scores)
                        counter = all_scores.count(max_score)
                    else:
                        max_score = 0
                        counter = all_scores.count(max_score)


                    raygiri_counter = 0

                    raygiri=[]
                    for key ,value in tedade_ray.items():
                        if value == max_score:
                            reply_players.append(int(key))
                            if raygiri_counter ==0:
                                raygiri.append(int(key))
                                raygiri_counter+=1
                    
                    print(f'11111 {reply_players}')
                    embed = discord.Embed(
                        title= 'رای خروج',
                        description= f'رای گیری دوباره برای خروج',
                    )

                    
                    for i in reply_players:
                        if str(i) in shahrhvand_players or str(i) in mafia_players:
                            user = discord.utils.get(interaction.guild.members , id=i)
                            if user is not None:
                                embed.add_field(name=f'{user.name}' ,value='' , inline=False)
                                break
                                

                    msg=await msg.edit(embed=embed , view=RayGiri(self.bot , interaction.user.id))
                    await interaction.response.send_message('انجام شد' , ephemeral=True)

                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3} , {'$set':{'msg_raygiri':msg.id,'reply_count':1 , 'tedade_ray':{} , 'reply_players':reply_players ,'raygiri':raygiri}})

            else:
                await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

    @ui.button(label='لغو رای گیری' , custom_id='endvote' , style=discord.ButtonStyle.primary)
    async def endvote(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3} , {'$set':{'msg_raygiri':None,'reply_count':None , 'tedade_ray':{} , 'reply_players':None ,'raygiri':None , 'player_cart':None}})
                await interaction.response.send_message('رای گیری اتمام یافت' ,ephemeral=True)
                await interaction.message.delete()

            else:
                await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

############################################ ray khoroje nahayi baraye hazf va cart keshidane player

class RayGiriPart2(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(label='خارج کردن پلیر' , custom_id='kickplayer' , style=discord.ButtonStyle.primary)
    async def kickplayer(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                total_players  = find1['total_players']
                shahrhvand_players = find1['shahr_players']
                mafia_players = find1['mafia_players']
                raygiri = find1['raygiri']
                channel_players = find1['channel_players']
                msg_raygiri = find1['msg_raygiri']
                hazf_mafia = find1['hazf_mafia']
                hazf_shahrvand = find1['hazf_shahrvand']
                tedade_ray = find1['tedade_ray']

                channel_send = discord.utils.get(interaction.guild.text_channels , id=channel_players)

                msg = ''
                async for messager in channel_send.history(limit=None):
                    if messager.id == msg_raygiri:
                        msg = messager
                
                if len(raygiri) == (len(shahrhvand_players) + len(mafia_players)):
                    all_scores = []
                    for i in tedade_ray.values():
                        all_scores.append(i)
                    
                    max_score = max(all_scores)
                    for key , value in tedade_ray.items():
                        if value == max_score:
                            key = int(key)
                            user = discord.utils.get(interaction.guild.members , id=key)
                            if user is not None:
                                if str(user.id) in mafia_players:
                                    hazf_mafia[f'{user.id}'] = value
                                    del mafia_players[f'{user.id}']
                                    embed=discord.Embed(
                                        title='حذف پلیر',
                                        description=f'{user.mention} از بازی حذف شد'
                                    )
                                    await msg.edit(embed=embed)
                                    await interaction.response.send_message('پلیر از بازی حذف شد' , ephemeral=True)
                                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3} , {"$set":{"mafia_players":mafia_players ,'hazf_mafia':hazf_mafia,'msg_raygiri':None , 'raygiri':[] ,'tedade_ray':{}}})
                                    break
                                elif str(user.id) in shahrhvand_players:
                                    hazf_shahrvand[f'{user.id}'] = value
                                    del shahrhvand_players[f'{user.id}']
                                    embed=discord.Embed(
                                        title='حذف پلیر',
                                        description=f'{user.mention} از بازی حذف شد'
                                    )
                                    await msg.edit(embed=embed)
                                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3} , {"$set":{"shahr_players":mafia_players ,'hazf_shahrvand':hazf_mafia,'msg_raygiri':None , 'raygiri':[] ,'tedade_ray':{}}})
                                    await interaction.response.send_message('پلیر از بازی حذف شد' , ephemeral=True)
                                    break
                    
                    channel_embed = find1['channel_embed']
                    msg_embed = find1['msg_embed']

                    channel_send = discord.utils.get(interaction.guild.text_channels ,id=channel_embed)


                    embed = discord.Embed(
                        title = f'قسمت سوم تنظیمات',
                        description=f'به فرم مدیریتی پیشرفته بات مافیا خوش آمدید',
                        timestamp=datetime.now(),
                        color= 0x0554FE
                    )
                    embed.add_field(name='لیست پلیرها :', value='' , inline=False)
                    embed.add_field(name='نقش های شهروند:' , value='' , inline=False)
                    for key , value in shahrhvand_players.items():
                        users = discord.utils.get(interaction.guild.members , id=int(key))
                        if users is not None:
                            embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 

                    embed.add_field(name='نقش های مافیا:' ,value='' , inline=False)

                    for key , value in mafia_players.items():
                        users = discord.utils.get(interaction.guild.members , id=int(key))
                        if users is not None:
                            embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                    
                    embed.add_field(name='پلیر های حذف شده تیم مافیا' , value='' , inline=False)
                    if len(hazf_mafia) !=0:
                        for key , value in hazf_mafia.items():
                            users = discord.utils.get(interaction.guild.members , id=int(key))
                            if users is not None:
                                embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                    else:
                        embed.add_field(name='پلیری حذف نشده از تیم مافیا' , value='' , inline=False)
                    
                    embed.add_field(name='پلیر های حذف شده تیم شهروند' , value='' , inline=False)
                    if len(hazf_shahrvand) !=0:
                        for key , value in hazf_shahrvand.items():
                            users = discord.utils.get(interaction.guild.members , id=int(key))
                            if users is not None:
                                embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                    else:
                        embed.add_field(name='پلیری حذف نشده از تیم شهروند' , value='' , inline=False)


                    embed.add_field(name='دستورات مدیریتی' , value='' , inline=False)
                    embed.add_field(name='/switchin' , value='جا به جایی نقش دو پلیر داخل بازی' , inline=False)
                    embed.add_field(name='/kharidari' , value='تغییر نقش پلیر داخل بازی' , inline=False)
                    embed.add_field(name='/hazfplayer' , value='پلیر به لیست کشته شده ها می رود یا همان حذف می شود',inline=True)
                    embed.add_field(name='/show' , value='نشان دادن نقش پلیر' , inline=True)
                    embed.add_field(name='/estelam' , value='استعلام ارسال می شود' , inline=True)
                    embed.add_field(name='/setvoice' , value='وویس جنل پلیر ها ست می شود' , inline=False)

                    msg = ''
                    async for messager in channel_send.history(limit=None):
                        if messager.id == msg_embed:
                            msg = messager

                    msg=await msg.edit(embed=embed , view=Part3Panel(self.bot))
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{"msg_embed":msg.id}})

            else:
                await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

    @ui.button(label='کشیدن کارت' , custom_id='usecart' , style=discord.ButtonStyle.primary)
    async def usecart(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                total_players  = find1['total_players']
                shahrhvand_players = find1['shahr_players']
                mafia_players = find1['mafia_players']
                raygiri = find1['raygiri']
                channel_players = find1['channel_players']
                msg_raygiri = find1['msg_raygiri']
                hazf_mafia = find1['hazf_mafia']
                hazf_shahrvand = find1['hazf_shahrvand']
                tedade_ray = find1['tedade_ray']
                cart_player = find1['player_cart']
                carts = find1['carts']
                
                if carts is None:
                    return await interaction.response.send_message('کارتی به این بازی ادد نشده است' , ephemeral=True)
                
                if len(carts) ==0:
                    return await interaction.response.send_message('کارت ها تمام شده است' , ephemeral=True)

                if interaction.user.id == cart_player:
                    choosen_one=random.choice(carts)
                    carts.remove(choosen_one)
                    await interaction.response.send_message(f'{choosen_one}')
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3} , {'$set':{"cart_player":None , 'carts':carts}})
                else:
                    await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)
            else:
                await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

    @ui.button(label='تایید اجازه کشیدن کارت توسط گاد' , custom_id='cartpermission' , style=discord.ButtonStyle.primary)
    async def cartpermission(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                total_players  = find1['total_players']
                shahrhvand_players = find1['shahr_players']
                mafia_players = find1['mafia_players']
                raygiri = find1['raygiri']
                channel_players = find1['channel_players']
                msg_raygiri = find1['msg_raygiri']
                hazf_mafia = find1['hazf_mafia']
                hazf_shahrvand = find1['hazf_shahrvand']
                tedade_ray = find1['tedade_ray']
                cart_player = find1['player_cart']
                carts = find1['carts']

                if len(raygiri) == (len(shahrhvand_players) + len(mafia_players)):
                    all_scores = []
                    for i in tedade_ray.values():
                        all_scores.append(i)
                    
                    max_score = max(all_scores)
                    for key , value in tedade_ray.items():
                        if value == max_score:
                            key = int(key)
                            user = discord.utils.get(interaction.guild.members , id=key)
                            if user is not None:
                                collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3} , {'$set':{'player_cart':user.id}})
                                await interaction.response.send_message('اجازه داده شد' , ephemeral=True)
                                break

            else:
                await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

########################################### ray khoroj
class RayGiri(ui.View):
    def __init__(self , bot:Bot , god):
        super().__init__(timeout=None)
        self.bot = bot
        self.god = god

    @ui.button(label='رای' , custom_id='vote' , style=discord.ButtonStyle.primary)
    async def vote(self, interaction:discord.Interaction,_):
        if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":self.god , 'part':3})):
            total_players  = find1['total_players']
            shahrhvand_players = find1['shahr_players']
            mafia_players = find1['mafia_players']
            raygiri = find1['raygiri']
            channel_players = find1['channel_players']
            tedad_ray = find1['tedade_ray']
            tedad_ray= {}
            voters = find1['voters']

            if interaction.user.id in voters:
                return await interaction.response.send_message('شما قبلا رای داده اید' , ephemeral=True)
            channel_send = discord.utils.get(interaction.guild.text_channels , id=channel_players)

            if raygiri[-1] not in tedad_ray:
                tedad_ray[f'{raygiri[-1]}'] = 1
            else:
                tedad_ray[f'{raygiri[-1]}'] +=1
            
            voters.append(interaction.user.id)
            
            collection.update_one({"server_id":interaction.guild_id , "god":self.god , 'part':3} , {"$set":{"tedade_ray":tedad_ray ,'voters':voters}})

            await interaction.response.send_message('رای داده شد' , ephemeral=True)
        else:
            await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)
            
    @ui.button(label='قسمت بعد' , custom_id='nextpart' , style=discord.ButtonStyle.primary)
    async def nextpart(self, interaction:discord.Interaction,_):
        if self.god != interaction.user.id:
            return await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

        if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":self.god , 'part':3})):
            total_players  = find1['total_players']
            shahrhvand_players = find1['shahr_players']
            mafia_players = find1['mafia_players']
            raygiri = find1['raygiri']
            channel_players = find1['channel_players']
            msg_raygiri = find1['msg_raygiri']
            reply_count = find1['reply_count']
            reply_players = find1['reply_players']
            tedad_ray = find1['tedade_ray']
            print(reply_count)
            
            if str(raygiri[-1]) not in tedad_ray:
                print(2)
                print(reply_players)
                tedad_ray[f'{raygiri[-1]}'] = 0
            
            channel_send = discord.utils.get(interaction.guild.text_channels , id=channel_players)

            if reply_count is None:
                if len(raygiri) == (len(shahrhvand_players) + len(mafia_players)):
                    return await interaction.response.send_message('قسمت بعدی دیگر وجود ندارد رای گیری را پایان دهید' , ephemeral=True)  
            else:
                if len(raygiri) == len(reply_players):
                    return await interaction.response.send_message('قسمت بعدی دیگر وجود ندارد رای گیری را پایان دهید' , ephemeral=True)  

            if reply_count is None:
                for i in total_players:
                    for j in raygiri:
                        if i==j:
                            total_players.remove(i)
            else:
                print(reply_players)
                print(raygiri)
                for i in reply_players:
                    for j in raygiri:
                        if i==j:
                            reply_players.remove(i)


            if reply_count is None:
                msg = ''
                if len(total_players)!=0:
                    option = random.choice(total_players)
                    option=str(option)
                    if option in mafia_players or option in shahrhvand_players:
                        print('1')
                        async for messager in channel_send.history(limit=None):
                            if messager.id == msg_raygiri:
                                raygiri.append(int(option))
                                msg = messager
                else:
                    return await interaction.response.send_message('قسمت بعدی وجود ندارد' , ephemeral=True)
                                    
                                    
            else:
                msg = ''
                if len(reply_players)!=0:
                    print('85')
                    option = random.choice(reply_players)
                    option=str(option)
                    if option in mafia_players or option in shahrhvand_players:
                        print('95')
                        async for messager in channel_send.history(limit=None):
                            if messager.id == msg_raygiri:
                                raygiri.append(int(option))
                                msg = messager
                else:
                    return await interaction.response.send_message('قسمت بعدی وجود ندارد' , ephemeral=True)
                                                    
            
            print(raygiri)
            user = discord.utils.get(interaction.guild.members , id=raygiri[-1])
            embed = discord.Embed(
                title= 'رای خروج',
                description= f'رای خروج برای ممبر زیر وارد کنید',
            )
            embed.add_field(name=f'{user.name}' , value='' , inline=False)
            msg=await msg.edit(embed=embed , view=RayGiri(self.bot , self.god))
            await interaction.response.defer()
            
            collection.update_one({"server_id":interaction.guild_id , "god":self.god , 'part':3} , {"$set":{"msg_raygiri":msg.id , 'raygiri':raygiri , 'tedade_ray':tedad_ray}})

        else:
            await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)


    @ui.button(label='اتمام رای گیری' , custom_id='endvote' , style=discord.ButtonStyle.primary)
    async def endvote(self, interaction:discord.Interaction,_):
        
        if self.god != interaction.user.id:
            return await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

        if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":self.god , 'part':3})):
            total_players  = find1['total_players']
            shahrhvand_players = find1['shahr_players']
            mafia_players = find1['mafia_players']
            raygiri = find1['raygiri']
            channel_players = find1['channel_players']
            msg_raygiri = find1['msg_raygiri']
            tedade_ray = find1['tedade_ray']
            reply_count = find1['reply_count']
            reply_players = find1['reply_players']

            if str(raygiri[-1]) not in tedade_ray:
                tedade_ray[f'{raygiri[-1]}'] = 0

            print(tedade_ray)


            channel_send = discord.utils.get(interaction.guild.text_channels , id=channel_players)

            msg = ''
            async for messager in channel_send.history(limit=None):
                if messager.id == msg_raygiri:
                    msg = messager

            embed=discord.Embed(
                title='حذف پلیر',
                description='پلیر به رای نهایی رسیده و با اجازه ی گاد حذف می شود'
            )

            embed1=discord.Embed(
                title='حذف پلیر',
                description='پلیر های زیر رای مساوی آورده اند'
            )

            if reply_count is None:
                if len(raygiri) == (len(shahrhvand_players) + len(mafia_players)):
                    all_scores = []
                    for i in tedade_ray.values():
                        all_scores.append(i)
                else:
                    return await interaction.response.send_message('تا آخر لیست را باید بروید برای اتمام' , ephemeral=True)
                
                if len(all_scores) !=0:
                    max_score = max(all_scores)
                    count_max = all_scores.count(max_score)
                else:
                    max_score = 0
                    count_max = all_scores.count(max_score)


                if count_max >1:

                    for key,values in tedade_ray.items():
                        if values == max_score:
                            user=discord.utils.get(interaction.guild.members , id = int(key))
                            embed1.add_field(name=f'{user.name}' , value='')
                            

                    await msg.edit(embed=embed1 ,view=RayGiriMojadad(self.bot))
                    await interaction.response.send_message(f'رای گیری اتمام یافت' , ephemeral=True)
                    collection.update_one({"server_id":interaction.guild_id , "god":self.god , 'part':3} , {'$set':{"msg_raygiri":msg.id , 'tedade_ray':tedade_ray, 'voters':[]}})

                else:
                    for key,values in tedade_ray.items():
                        if values == max_score:
                            user=discord.utils.get(interaction.guild.members , id = int(key))                    
                            embed.add_field(name=f'{user.name}' , value='')
                            break

                    await msg.edit(embed=embed ,view=RayGiriPart2(self.bot))
                    await interaction.response.send_message(f'رای گیری اتمام یافت' , ephemeral=True)
                    collection.update_one({"server_id":interaction.guild_id , "god":self.god , 'part':3} , {'$set':{"msg_raygiri":msg.id , 'tedade_ray':tedade_ray, 'voters':[]}})

            else:
                if len(raygiri) == len(reply_players):
                    all_scores = []
                    for i in tedade_ray.values():
                        all_scores.append(i)
                else:
                    return await interaction.response.send_message('تا آخر لیست را باید بروید برای اتمام' , ephemeral=True)
                
                max_score = max(all_scores)
                count_max = all_scores.count(max_score)
                if count_max >1:

                    for key,values in tedade_ray.items():
                        if values == max_score:
                            user=discord.utils.get(interaction.guild.members , id = int(key))
                            embed1.add_field(name=f'{user.name}' , value='')

                    await msg.edit(embed=embed1 ,view=RayGiriMojadad(self.bot))
                    await interaction.response.send_message(f'رای گیری اتمام یافت' , ephemeral=True)
                    collection.update_one({"server_id":interaction.guild_id , "god":self.god , 'part':3} , {'$set':{"msg_raygiri":msg.id , 'tedade_ray':tedade_ray, 'voters':[]}})


                else:
                    for key,values in tedade_ray.items():
                        if values == max_score:
                            user=discord.utils.get(interaction.guild.members , id = int(key))
                    
                    embed.add_field(name=f'{user.name}' , value='')
                    
                    await msg.edit(embed=embed ,view=RayGiriPart2(self.bot))
                    await interaction.response.send_message(f'رای گیری اتمام یافت' , ephemeral=True)
                    collection.update_one({"server_id":interaction.guild_id , "god":self.god , 'part':3} , {'$set':{"msg_raygiri":msg.id , 'tedade_ray':tedade_ray , 'voters':[]}})


        else:
            await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

########################################### day time view
class NightTime(ui.View):
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot
        
    @ui.button(label='ارسال فرم پیشفرض' , custom_id='defaultformnight' , style=discord.ButtonStyle.primary)
    async def defaultformnight(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                channel_players  = find1['channel_players']
                embed=discord.Embed(
                    title='شب مافیا',
                    description='شهر شب میشه و تیم مافیا دست به کار میشه آیا امشب کسی حذف میشه؟',
                    timestamp=datetime.now(),
                    color= 0x0554FE
                )
                channel_send = discord.utils.get(interaction.guild.text_channels , id= channel_players)
                if channel_send is not None:
                    await channel_send.send(embed=embed)
                    await interaction.response.send_message('پیام ارسال شد', ephemeral=True)
                else:
                    await interaction.response.send_message('چنل پلیرها به نظر پاک شده است یا من دسترسی ندارم')
            else:
                await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

    @ui.button(label='وارد کردن متن دلخواه شب' , custom_id='nighttext' , style=discord.ButtonStyle.primary)
    async def nighttext(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                async def on_submit(ctx):
                    embed=discord.Embed(
                        title='روز مافیا',
                        description=f'{self.rolename.value}',
                        timestamp=datetime.now(),
                        color= 0x0554FE
                    )

                    channel_players  = find1['channel_players']
                    channel_send = discord.utils.get(interaction.guild.text_channels , id= channel_players)
                    if channel_send is not None:
                        await channel_send.send(embed=embed)
                        await ctx.response.send_message('پیام ارسال شد')
                    else:
                        await ctx.response.send_message('چنل پلیرها به نظر پاک شده است یا من دسترسی ندارم', ephemeral=True)

                delete_form = discord.ui.Modal(title='فرم واردن کردن متن شب')
                self.rolename = discord.ui.TextInput(label='متن شب:' , style=discord.TextStyle.long , required=True)
                delete_form.add_item(self.rolename)
                delete_form.on_submit = on_submit
                await interaction.response.send_modal(delete_form)
            else:
                await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)


class DayTime(ui.View):

    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(label='ارسال فرم پیشفرض' , custom_id='defaultform' , style=discord.ButtonStyle.primary)
    async def defaultform(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                channel_players  = find1['channel_players']
                embed=discord.Embed(
                    title='روز مافیا',
                    description='شهر روز میشه و تیم شهروند همچنان شانس خود را برای پیدا کردن مافیا از دست نداده است',
                    timestamp=datetime.now(),
                    color= 0x0554FE
                )
                channel_send = discord.utils.get(interaction.guild.text_channels , id= channel_players)
                if channel_send is not None:
                    await channel_send.send(embed=embed)
                    await interaction.response.send_message('پیام ارسال شد' , ephemeral=True)
                else:
                    await interaction.response.send_message('چنل پلیرها به نظر پاک شده است یا من دسترسی ندارم')
            else:
                await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

    @ui.button(label='وارد کردن متن دلخواه روز' , custom_id='daytext' , style=discord.ButtonStyle.primary)
    async def daytext(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):

                async def on_submit(ctx):
                    embed=discord.Embed(
                        title='روز مافیا',
                        description=f'{self.rolename.value}',
                        timestamp=datetime.now(),
                        color= 0x0554FE
                    )

                    channel_players  = find1['channel_players']
                    channel_send = discord.utils.get(interaction.guild.text_channels , id= channel_players)
                    if channel_send is not None:
                        await channel_send.send(embed=embed)
                        await ctx.response.send_message('پیام ارسال شد')
                    else:
                        await ctx.response.send_message('چنل پلیرها به نظر پاک شده است یا من دسترسی ندارم', ephemeral=True)

                delete_form = discord.ui.Modal(title='فرم واردن کردن متن روز')
                self.rolename = discord.ui.TextInput(label='متن روز:' , style=discord.TextStyle.long , required=True)
                delete_form.add_item(self.rolename)
                delete_form.on_submit = on_submit
                await interaction.response.send_modal(delete_form)
            else:
                await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

##########################################part 3 view
class Part3Panel(ui.View):

    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(label='ََشروع بازی' , custom_id='startgame' , style=discord.ButtonStyle.primary)
    async def startgame(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'moarefe':True})):
                moarefe=find1['moarefe']
                total_players  = find1['total_players']
                shahrhvand_players = find1['shahr_players']
                mafia_players = find1['mafia_players']

                if moarefe == True:
                    channel_players = find1['channel_players']
                    
                    if channel_players is None:
                        return await interaction.response.send_message('چنل پلیر را تنظیم کنید' , ephemeral=True)
                    
                    channel_send  = discord.utils.get(interaction.guild.text_channels , id=channel_players)

                    if channel_send is None:
                        return await interaction.response.send_message('چنل پلیرها یافت نشد' , ephemeral=True)
                    
                    time = find1['time']

                    if time is None:
                        return await interaction.response.send_message('زمان را تنظیم کنید' , ephemeral = True)
                    
                    embed=discord.Embed(
                        title='شروع بازی',
                        description='در نوبت معارفه بازی هستیم پلیرها خیلی کوتاه خود را معرفی کنند'
                    )
                    embed.add_field(name='لیست پلیر ها' , value='' , inline=False)
                    for i in total_players:
                        user = discord.utils.get(interaction.guild.members , id=i)
                        if user is not None:
                            embed.add_field(name=f'{user.name}' , value='' , inline=False)
                    
                    await channel_send.send(embed=embed)
                    await interaction.response.send_message('بازی شروع شد' , ephemeral=True)

                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3} , {'$set':{'moarefe':False}})

            else:
                await interaction.response.send_message('یا دسترسی ندارید یا بازی از قبل شروع شده است' , ephemeral=True)


    @ui.button(label='تغییر به روز' , custom_id='turnday' , style=discord.ButtonStyle.primary)
    async def turnday(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'moarefe':False})):

                state=find1['night_time']
                if state == True:
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3} , {'$set':{'day_time':True , 'night_time':False}})
                    await interaction.response.send_message('به روز تغییر بافت', view= DayTime(self.bot) , ephemeral=True)
                    

                else:
                    await interaction.response.send_message('قبلا روز شروع شده است' , ephemeral=True)
            else:
                await interaction.response.send_message('اول بازی را شروع کنید و بعد از اتمام معارفه و یک بار شب کردن بازی از این دکمه استفاده کنید به صورت اتوماتیک بازی از روز شروع می شود',ephemeral=True)

    @ui.button(label='تغییر به شب' , custom_id='turnnight' , style=discord.ButtonStyle.primary)
    async def turnnight(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'moarefe':False})):
                state=find1['day_time']

                if state == True:
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3} , {'$set':{'night_time':True , 'day_time':False}})
                    await interaction.response.send_message('به َشب تغییر بافت', view= NightTime(self.bot) , ephemeral=True)
                else:
                    return await interaction.response.send_message('شب قبلا شروع شده است' , ephemeral=True)

                turn = find1['turn']
                if turn ==1 :
                    ct_tozih = find1['ct_tozih']
                    tr_tozih = find1['tr_tozih']
                    ct_roles = find1['ct_roles']
                    tr_roles = find1['tr_roles']

                    shahr_players = find1['shahr_players']
                    mafia_players = find1['mafia_players']

                    for key , value in shahr_players.items():
                        if value[0] in ct_roles:
                            user= discord.utils.get(interaction.guild.members , id=int(key))
                            indexer=ct_roles.index(value[0])
                            tozih = ct_tozih[indexer]
                            embed=discord.Embed(
                                title='توضیح نقش شما',
                                description=tozih
                            )
                            await user.send(embed=embed)
                            await asyncio.sleep(2)

                    for key , value in mafia_players.items():
                        if value[0] in ct_roles:
                            user= discord.utils.get(interaction.guild.members , id=int(key))
                            indexer=tr_roles.index(value[0])
                            tozih = tr_tozih[indexer]
                            embed=discord.Embed(
                                title='توضیح نقش شما',
                                description=tozih
                            )
                            await user.send(embed=embed)
                            await asyncio.sleep(2)

                    turn+=1
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3} , {'$set':{'turn':turn}})

            
            else:
                await interaction.response.send_message('اول بازی را شروع کنید و بعد از اتمام معارفه و یک بار شب کردن بازی از این دکمه استفاده کنید به صورت اتوماتیک بازی از روز شروع می شود' , ephemeral=True)

    @ui.button(label='تغییر اسم' , custom_id='changename' , style=discord.ButtonStyle.primary)
    async def changename(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):

                async def on_submit(ctx):
                    total_players = find1['total_players']
                    real_names = find1['real_names']
                    for i in total_players:
                        user = discord.utils.get(interaction.guild.members , id=i)
                        if user is not None:
                            name=user.name
                            real_names[user.id] = user.name
                            tmp = str(self.rolename.value)
                            tmp+=name
                            try:
                                await user.edit(nick=tmp)
                            except:
                                pass

                    await ctx.response.send_message('انجام شد' , ephemeral=True)
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3 } , {'$set':{'real_names':real_names}})


                change_name_form = discord.ui.Modal(title='فرم وارد کردن تغییر اسم')
                self.rolename = discord.ui.TextInput(label='چه چیزی دوست دارید به اول اسمشان اضافه شود' , style=discord.TextStyle.short , required=True)
                change_name_form.add_item(self.rolename)
                change_name_form.on_submit=on_submit
                await interaction.response.send_modal(change_name_form)
                
            
            else:
                await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

    @ui.button(label='میوت کردن همه' , custom_id='muteall' , style=discord.ButtonStyle.primary)
    async def muteall(self, interaction:discord.Interaction,_):
        
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'moarefe':False})):
                channel_game = find1['channel_game']
                if channel_game is None:
                    return await interaction.response.send_message('اول با استفاده از دستور /setvoice چنل گیم را ست کنید' , ephemeral=True)
                
                channel_voice = discord.utils.get(interaction.guild.voice_channels , id=channel_game)

                if channel_voice is None:
                    return await interaction.response.send_message('چنل شما در سرور وجود ندارد' , ephemeral=True)
                
                await interaction.response.defer()
                total_players = find1['total_players']
                for member in channel_voice.members:
                    if member.id in total_players:
                        await member.edit(mute=True)
                


            else:
                await interaction.response.send_message('اول بازی را شروع کنید و بعد از اتمام معارفه و یک بار شب کردن بازی از این دکمه استفاده کنید به صورت اتوماتیک بازی از روز شروع می شود' , ephemeral=True)

    @ui.button(label='زمان صحبت' , custom_id='time' , style=discord.ButtonStyle.primary)
    async def timer(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                async def on_submit(ctx):
                    timer = self.rolename.value
                    try:
                        timer = int(timer)
                    except:
                        await ctx.response.send_message('زمان را عددی وارد کنید' , ephemeral=True)
                    
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3 } , {'$set':{'time':timer}})
                    await ctx.response.send_message('زمان وارد شد')

                time_form = discord.ui.Modal(title='فرم وارد کردن زمان صحبت')
                self.rolename = discord.ui.TextInput(label='زمان را به ثانیه وارد کنید' , style=discord.TextStyle.short , required=True)
                time_form.add_item(self.rolename)
                time_form.on_submit=on_submit
                await interaction.response.send_modal(time_form)
            else:
                await interaction.response.send_message('شما دسترسی ندارید' , ephemeral=True)

    @ui.button(label='مدیریت خودکار وویس' , custom_id='automod' , style=discord.ButtonStyle.primary)
    async def automod(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'moarefe':False})):
                moarefe=find1['moarefe']
                if moarefe == True:
                    return await interaction.response.send_message('اول بازی را شروع کنید' , ephemeral=True)

                night_time= find1['night_time']
                if night_time == True:
                    return await interaction.response.send_message('در شب صحبتی صورت نمیگیرد' , ephemeral=True)


                channel_game = find1['channel_game']
                channel_players =find1['channel_players']
                if channel_game is None:
                    return await interaction.response.send_message('اول با استفاده از دستور /setvoice چنل گیم را ست کنید' , ephemeral=True)
                
                channel_voice = discord.utils.get(interaction.guild.voice_channels , id=channel_game)

                if channel_voice is None:
                    return await interaction.response.send_message('چنل شما در سرور وجود ندارد' , ephemeral=True)
                
                if channel_players is None:
                    return await interaction.response.send_message('چنل پلیر ها یافت نشد' , ephemeral=True)
                
                channel_send= discord.utils.get(interaction.guild.text_channels , id = channel_players)

                if channel_send is None:
                    return await interaction.response.send_message('چنل پلیر ها یافت نشد' , ephemeral=True)

                await interaction.response.defer()
                turn = 1
                total_players = find1['total_players']
                for member in channel_voice.members:
                    if member.id in total_players:
                        await member.edit(mute=True)

                timer = find1['time']
                timer1=f'{timer}s'
                msg=''
                for member in channel_voice.members:
                    ends_at = humanfriendly.parse_timespan(timer1) + time.time()
                    if member.id in total_players:
                        embed=discord.Embed(
                            title='نوبت صحبت خودکار',
                            description = f'{member.mention}',
                        )
                        embed.add_field(name='زمان شما' , value=f"{discord.utils.format_dt(datetime.fromtimestamp(ends_at),'R')}")
                        if turn ==1:
                            await member.edit(mute=False)
                            msg=await channel_send.send(embed=embed)
                            turn+=1
                        else:
                            await member.edit(mute=False)
                            await msg.edit(embed=embed)
                        

                        await asyncio.sleep(timer)
                        await member.edit(mute=True)

                embed=discord.Embed(
                    title='اتمام گفتگو',
                    description = f'همه صحبت کردند',
                )
                await msg.edit(embed=embed)


            else:
                await interaction.response.send_message('اول بازی را شروع کنید و بعد از اتمام معارفه و یک بار شب کردن بازی از این دکمه استفاده کنید به صورت اتوماتیک بازی از روز شروع می شود' , ephemeral=True)


    @ui.button(label='از میوت بیرون آوردن' , custom_id='unmute' , style=discord.ButtonStyle.primary)
    async def unmute(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'moarefe':False})):
                channel_game = find1['channel_game']
                if channel_game is None:
                    return await interaction.response.send_message('اول با استفاده از دستور /setvoice چنل گیم را ست کنید' , ephemeral=True)
                
                channel_voice = discord.utils.get(interaction.guild.voice_channels , id=channel_game)

                if channel_voice is None:
                    return await interaction.response.send_message('چنل شما در سرور وجود ندارد' , ephemeral=True)
                
                total_players = find1['total_players']
                for member in channel_voice.members:
                    if member.id in total_players:
                        await member.edit(mute=False)
                
                await interaction.response.send_message('انجام شد' , ephemeral=True)


            else:
                await interaction.response.send_message('اول بازی را شروع کنید و بعد از اتمام معارفه و یک بار شب کردن بازی از این دکمه استفاده کنید به صورت اتوماتیک بازی از روز شروع می شود' , ephemeral=True)


    @ui.button(label='ارسال فرم رای خروح' , custom_id='sendvote' , style=discord.ButtonStyle.primary)
    async def sendvote(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                moarefe=find1['moarefe']
                if moarefe == True:
                    return await interaction.response.send_message('اول بازی را شروع کنید' , ephemeral=True)

                night_time= find1['night_time']
                if night_time == True:
                    return await interaction.response.send_message('در شب رای گیری نمی توانید بکنید' , ephemeral=True)

                total_players  = find1['total_players']
                shahrhvand_players = find1['shahr_players']
                mafia_players = find1['mafia_players']
                raygiri = find1['raygiri']
                channel_players = find1['channel_players']
                reply_counter = find1['reply_count']
                voter = find1['voters']
                voter = []
                reply_counter = None
                raygiri=[]

                if channel_players is None:
                    return await interaction.response.send_message('چنل پلیرها ست نشده است' , ephemeral=True)
                
                channel_send = discord.utils.get(interaction.guild.text_channels , id=channel_players)

                if channel_send is None:
                    return await interaction.response.send_message('چنل پلیرها وجود ندارد یا من دسترسی ندارم' , ephemeral=True)

                embed = discord.Embed(
                    title= 'رای خروج',
                    description= f'رای گیری از بین ممبر های پایین است',
                )


                for i in total_players:
                    if str(i) in shahrhvand_players or str(i) in mafia_players:
                        user = discord.utils.get(interaction.guild.members , id=i)
                        if user is not None:
                            embed.add_field(name=f'{user.name}' ,value='' , inline=False)
                            raygiri.append(i)
                            break

                msg=await channel_send.send(embed=embed , view=RayGiri(self.bot,interaction.user.id ))
                collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':3} , {"$set":{"raygiri":raygiri , 'msg_raygiri':msg.id , 'tedade_ray':{} , 'reply_players':[] , 'reply_count':None ,'voters':voter}})
                await interaction.response.send_message('ارسال شد' , ephemeral=True)
                        

    @ui.button(label='اتمام بازی' , custom_id='endgame' , style=discord.ButtonStyle.primary)
    async def endgame(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                moarefe=find1['moarefe']
                if moarefe == True:
                    return await interaction.response.send_message('اول بازی را شروع کنید' , ephemeral=True)

                night_time= find1['night_time']
                if night_time == True:
                    return await interaction.response.send_message('اول بازی را روز کنید و بعد اتمام بدهید' , ephemeral=True)

                total_players  = find1['total_players']
                shahrhvand_players = find1['shahr_players']
                mafia_players = find1['mafia_players']
                raygiri = find1['raygiri']
                channel_players = find1['channel_players']
                msg_raygiri = find1['msg_raygiri']
                tedade_ray = find1['tedade_ray']
                reply_count = find1['reply_count']
                hazf_mafia = find1['hazf_mafia']
                hazf_shahrvand = find1['hazf_shahrvand']

                channel_send= discord.utils.get(interaction.guild.text_channels , id = channel_players)

                if channel_send is None:
                    return await interaction.response.send_message('چنل پلیرهارا تنظیم کنید' , ephemeral=True)
                
                god = discord.utils.get(interaction.guild.members , id= interaction.user.id )
                embed=discord.Embed(
                    title= 'نتایج بازی',
                    description='بازی به اتمام رسیده است'
                )
                if len(mafia_players) ==0:

                    embed.add_field(name='تیم برنده:', value='شهروند' , inline=False)
                    embed.add_field(name='گاد بازی:' , value=f'{god.name}', inline=False)
                    embed.add_field(name='لیست پلیرها' ,value='', inline=False)
                    for key , value in shahrhvand_players.items():

                        user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key))
                        embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}')

                    for key , value in hazf_shahrvand.items():

                        user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key))
                        embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}')


                    for key , value in mafia_players.items():
                        
                        user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key))
                        embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}')

                    for key , value in hazf_mafia.items():

                        user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key))
                        embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}')


                    await channel_send.send(embed=embed)
                    await interaction.response.send_messages('بازی تمام شد' , ephemeral=True)
                    collection.delete_one({"server_id":interaction.guild_id , "god":interaction.user.id  , 'part':3})




                elif len(shahrhvand_players) == 0 or len(shahrhvand_players) == len(mafia_players):

                    embed.add_field(name='تیم برنده:', value='مافیا' , inline=False)
                    embed.add_field(name='گاد بازی:' , value=f'{god.name}', inline=False)
                    embed.add_field(name='لیست پلیرها' ,value='', inline=False)

                    for key , value in mafia_players.items():
                        
                        user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key))
                        embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}')

                    for key , value in hazf_mafia.items():

                        user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key))
                        embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}')


                    for key , value in shahrhvand_players.items():

                        user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key))
                        embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}')

                    for key , value in hazf_shahrvand.items():

                        user_shahrvand = discord.utils.get(interaction.guild.members , id= int(key))
                        embed.add_field(name=f'{user_shahrvand.name}' , value=f'نقش : {value}')


                    await channel_send.send(embed=embed)
                    await interaction.response.send_message('بازی تمام شد' , ephemeral=True)
                    collection.delete_one({"server_id":interaction.guild_id , "god":interaction.user.id  , 'part':3})

            else:
                await interaction.response.send_message('شما دسترسی نداری' , ephemeral=True)

#########################################################

class joinvoteer(ui.View):

    def __init__(self , bot:Bot ,god):
        super().__init__(timeout=None)
        self.bot = bot
        self.god=god
        
    @ui.button(label='ورود' , custom_id='join_button' , style=discord.ButtonStyle.primary)
    async def vorod(self, interaction:discord.Interaction,_):

        if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":self.god , 'part':2})):

            max_players = len(find1['ct_roles'])
            len2 = len(find1['tr_roles'])
            total_players = find1['total_players']
            if interaction.user.id in total_players:
                return await interaction.response.send_message('شما قبلا عضو شده اید' ,  ephemeral=True)
            total_players.append(interaction.user.id)
            max_players+=len2
            if len(total_players)>max_players:
                return await interaction.response.send_message('ظرفیت تکمیل است')
            else: 
                collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{"total_players":total_players}})
                self.status.label = f'تعداد پلیرهای اضافه شده : {len(total_players)}'
                await interaction.response.send_message('وارد شدید' , ephemeral=True)
                await interaction.message.edit(view=self)
                
                
        
        
                            

        else:
            return await interaction.response.send_message('این بازی تمام شده است' , ephemeral=True)


    @ui.button(label='خروج' , custom_id='exit_button' , style=discord.ButtonStyle.primary)
    async def exit1(self, interaction:discord.Interaction,_):

        if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":self.god , 'part':2})):
                max_players = len(find1['ct_roles'])
                len2 = len(find1['tr_roles'])
                total_players = find1['total_players']
                max_players+=len2
                if interaction.user.id in total_players :
                    total_players.remove(interaction.user.id)
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{"total_players":total_players}})
                    await interaction.response.send_message('خارج شدید' , ephemeral=True)
                    self.status.label = f'تعداد پلیرهای اضافه شده : {len(total_players)}'
                    await interaction.message.edit(view=self)
                else:
                    await interaction.response.send_message('شما اصلا در رای گیری وارد نشده اید' , ephemeral=True)
                            

        else:
            await interaction.response.send_message('این بازی تمام شده است' , ephemeral=True)

    @ui.button(label='تعداد پلیرهای اضافه شده:0' , custom_id='status' , style=discord.ButtonStyle.primary , disabled=True)
    async def status(self, interaction:discord.Interaction,_):
        ...

    @ui.button(label='اتمام' , custom_id='end_button' , style=discord.ButtonStyle.primary)
    async def ended(self, interaction:discord.Interaction,_):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                self.vorod.disabled=True
                self.exit1.disabled=True
                await interaction.message.edit(view=self)
                await interaction.response.send_message('اتمام یافت' , ephemeral=True)
            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    



class addroles(ui.View):

    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot
        
    @ui.button(label='نقش های شهروند' , custom_id='shahrvand_role' , style=discord.ButtonStyle.primary)
    async def subject1(self, interaction:discord.Interaction,_):
        async def sumbit(ctx):
            await ctx.response.defer()
            user_roles = interaction.user.roles
            roler = ''
            flag = False
            for role in user_roles:
                if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                    roler = role
                    flag=True
                    break
            if flag == True:
                if (find1:=collection.find_one({"server_id":ctx.guild_id,"god":ctx.user.id })):
                    tmp_list = find1['ct_roles']
                    list_tozih = find1['ct_tozih']
                    rolename = str(self.rolename.value)
                    role_explaination = str(self.role_explaination.value)
                    tmp_list.append(rolename)
                    list_tozih.append(role_explaination)
                    collection.update_one({"server_id":ctx.guild_id,"god":ctx.user.id } , {"$set":{'ct_roles':tmp_list , "ct_tozih":list_tozih}})
                else:
                    await ctx.followup.send('به نظر بازی تمام شده است')    
            else:
                await ctx.followup.send('گاد بازی شخص دیگریست')        

        shahrvand_form = discord.ui.Modal(title='فرم وارد کردن رول های شهروند')
        self.rolename = discord.ui.TextInput(label='اسم رول شهروند' , style=discord.TextStyle.short , required=True)
        self.role_explaination = discord.ui.TextInput(label='پیام ارسالی به این رول در شب ' , style=discord.TextStyle.long , required=True)
        shahrvand_form.add_item(self.rolename)
        shahrvand_form.add_item(self.role_explaination)
        shahrvand_form.on_submit = sumbit
        await interaction.response.send_modal(shahrvand_form)


    @ui.button(label='نقش های مافیا' , custom_id='mafia_role' , style=discord.ButtonStyle.primary)
    async def subject2(self, interaction:discord.Interaction,_):
        async def sumbit(ctx):
            await ctx.response.defer()
            user_roles = interaction.user.roles
            roler = ''
            flag = False
            for role in user_roles:
                if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                    roler = role
                    flag=True
                    break
            if flag == True:
                if (find1:=collection.find_one({"server_id":ctx.guild_id,"god":ctx.user.id })):
                    tmp_list = find1['tr_roles']
                    list_tozih = find1['tr_tozih']
                    rolename = str(self.rolename.value)
                    role_explaination = str(self.role_explaination.value)
                    tmp_list.append(rolename)
                    list_tozih.append(role_explaination)
                    collection.update_one({"server_id":ctx.guild_id,"god":ctx.user.id } , {"$set":{'tr_roles':tmp_list , 'tr_tozih':list_tozih}})
                else:
                    await ctx.followup.send('به نظر بازی تمام شده است')    
            else:
                await ctx.followup.send('گاد بازی شخص دیگریست')     

        self.mafia_form = discord.ui.Modal(title='فرم واردن کردن نقش های مافیا')
        self.rolename = discord.ui.TextInput(label='اسم رول مافیا' , style=discord.TextStyle.short , required=True)
        self.role_explaination = discord.ui.TextInput(label='پیام ارسالی به این رول در شب' , style=discord.TextStyle.long , required=True)
        self.mafia_form.add_item(self.rolename)
        self.mafia_form.add_item(self.role_explaination)
        self.mafia_form.on_submit = sumbit
        await interaction.response.send_modal(self.mafia_form)

    @ui.button(label='نشان دادن لیست نقش ها' , custom_id='show_roles' , style=discord.ButtonStyle.primary)
    async def subject3(self, interaction:discord.Interaction,_):
            user_roles = interaction.user.roles
            roler = ''
            flag = False
            for role in user_roles:
                if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                    roler = role
                    flag=True
                    break
            if flag == True:
                if (find1:=collection.find_one({"server_id":interaction.guild_id,"god":interaction.user.id })):
                    mafia_roles = find1['tr_roles']
                    mafia_exp = find1["tr_tozih"]
                    shahrvand_roles = find1['ct_roles']
                    shahrvand_exp = find1['ct_tozih']

                    embed=discord.Embed(
                    title=f"لیست نقش ها:",
                    description=f'گاد بازی {interaction.user.name}',
                    timestamp=datetime.now(),
                    color= 0xF6F6F6
                    )
                    for i in range(len(mafia_roles)):
                        embed.add_field(name=mafia_roles[i] , value=mafia_exp[i] , inline=False)
                    for i in range(len(shahrvand_roles)):
                        embed.add_field(name=shahrvand_roles[i] , value=shahrvand_exp[i] , inline=False)

                    await interaction.response.send_message(embed=embed , ephemeral=True)
                else:
                    await interaction.response.send_message('به نظر بازی تمام شده است' , ephemeral=True)    
            else:
                await interaction.response.send_message('گاد بازی شخص دیگریست' , ephemeral=True)     

    @ui.button(label='پاک کردن نقش' , custom_id='delete_roles' , style=discord.ButtonStyle.red)
    async def subject4(self, interaction:discord.Interaction,_):
            user_roles = interaction.user.roles
            roler = ''
            flag = False
            for role in user_roles:
                if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                    roler = role
                    flag=True
                    break
            if flag == True:
                if (find1:=collection.find_one({"server_id":interaction.guild_id,"god":interaction.user.id })):
                    mafia_roles = find1['tr_roles']
                    mafia_exp = find1["tr_tozih"]
                    shahrvand_roles = find1['ct_roles']
                    shahrvand_exp = find1['ct_tozih']

                    total_roles = list(mafia_roles)
                    for i in shahrvand_roles:
                        total_roles.append(i)
                    count = len(total_roles)
                    embed=discord.Embed(
                    title=f"لیست نقش ها:",
                    description=f'آیدی نقشی که می خواهید پاک کنید را بخاطر بسپارید و بر روی دکمه وارد کردن آیدی بزنید و آیدی را وارد کنید تا نقش پاک شود',
                    timestamp=datetime.now(),
                    color= 0xF6F6F6
                    )
                    for i in range(len(total_roles)):
                        embed.add_field(name=f'{total_roles[i]}\t\t ID:{i}' , value='' , inline=False)
                        
                    async def sumbit(ctx):
                        if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":roler.id})):
                            if (find1:=collection.find_one({"server_id":interaction.guild_id,"god":interaction.user.id })):
                                try:
                                    count = len(total_roles)
                                    rolename=str(self.rolename.value)
                                    rolename = int(rolename)
                                    if total_roles[rolename] in mafia_roles:
                                        del mafia_roles[rolename]
                                        del mafia_exp[rolename]
                                        collection.update_one({"server_id":interaction.guild_id,"god":interaction.user.id } , {"$set":{"tr_roles":mafia_roles , "tr_tozih":mafia_exp}})
                                        await ctx.response.send_message('انجام شد')
                                    elif total_roles[rolename] in shahrvand_roles:
                                        rolename = rolename - len(mafia_roles)
                                        del shahrvand_roles[rolename]
                                        del shahrvand_exp[rolename]
                                        collection.update_one({"server_id":interaction.guild_id,"god":interaction.user.id } , {"$set":{"ct_roles":shahrvand_roles , "ct_tozih":shahrvand_exp}})
                                        await ctx.response.send_message('انجام شد')
                                except:
                                    await ctx.response.send_message("آیدی انتخابی وجود ندارد")

                    async def on_sumbit(ctx):
                        if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":roler.id})):
                            if (find1:=collection.find_one({"server_id":interaction.guild_id,"god":interaction.user.id })):
                                await ctx.response.send_modal(delete_form)

        
                    button_delete_form = discord.ui.Button(label='وارد کردن آیدی')
                    button_delete_form.callback = on_sumbit
                    button_delete_view = discord.ui.View(timeout=None)
                    button_delete_view.add_item(button_delete_form)
                    delete_form = discord.ui.Modal(title='فرم واردن کردن آیدی')
                    self.rolename = discord.ui.TextInput(label='آیدی رول:' , style=discord.TextStyle.short , required=True)
                    delete_form.add_item(self.rolename)
                    delete_form.on_submit = sumbit


                    await interaction.response.send_message(embed=embed , view=button_delete_view , ephemeral=True)
                else:
                    await interaction.response.send_message('به نظر بازی تمام شده است' , ephemeral=True)    
            else:
                await interaction.response.send_message('گاد بازی شخص دیگریست' , ephemeral=True)    

    @ui.button(label='پاک کردن همه نقش ها' , custom_id='reset_roles' , style=discord.ButtonStyle.primary)
    async def subject5(self, interaction:discord.Interaction,_):
            user_roles = interaction.user.roles
            roler = ''
            flag = False
            for role in user_roles:
                if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                    roler = role
                    flag=True
                    break
            if flag == True:
                if (find1:=collection.find_one({"server_id":interaction.guild_id,"god":interaction.user.id })):
                    collection.update_one({"server_id":interaction.guild_id,"god":interaction.user.id } , {"$set":{"ct_roles":[] , "tr_roles":[] , "ct_tozih":[] , 'tr_tozih':[]}})
                    await interaction.response.send_message('همه نقش ها پاک شدند', ephemeral=True)
                else:
                    await interaction.response.send_message('به نظر بازی تمام شده است' , ephemeral=True)    
            else:
                await interaction.response.send_message('گاد بازی شخص دیگریست' , ephemeral=True)     

    @ui.button(label='پاک کردن بازی' , custom_id='delete_game' , style=discord.ButtonStyle.primary)
    async def subject6(self, interaction:discord.Interaction,_):
            user_roles = interaction.user.roles
            roler = ''
            flag = False
            for role in user_roles:
                if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                    roler = role
                    flag=True
                    break
            if flag == True:
                if (find1:=collection.find_one({"server_id":interaction.guild_id,"god":interaction.user.id })):
                    collection.delete_one({"server_id":interaction.guild_id,"god":interaction.user.id })
                    await interaction.response.send_message('بازی پاک شد و شما دیگر گاد نیستید و می توانید بعدا بازی دیگری را ایجاد کنید', ephemeral=True)
                else:
                    await interaction.response.send_message('به نظر بازی تمام شده است' , ephemeral=True)    
            else:
                await interaction.response.send_message('گاد بازی شخص دیگریست' , ephemeral=True)     


class Part2Panel(ui.View):
    
    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(label='مشاهده افراد عضو شده' , custom_id='total_players' , style=discord.ButtonStyle.primary)
    async def subject4(self, interaction:discord.Interaction,_):
        if (find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':2})):
            total_players = find1['total_players']
            embed = discord.Embed(
                title='پلیرهای عضو شده به بازی',
                description="لیست پلیرها را به ترتیب می توانید مشاهده کنید",
                timestamp=datetime.now(),
                color= 0x0554FE
            )
            tmp_remove = 0
            for i in total_players:
                user = discord.utils.get(interaction.guild.members , id=i)
                if user is not None:
                    embed.add_field(name=user.name ,value='' , inline=False)
                else:
                    tmp_remove+=1
                    total_players.remove(i)
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id , 'part':2} , {"$set":{"total_players":total_players}})

            if tmp_remove != 0:
                await interaction.response.send_message(f'به اطلاع می رسانیم تعداد {tmp_remove} یوزر دیگر در سرور نیستند و از لیست بازیکنان حذف شده اند اقدام به اضافه کردن پلیر جدید کنید' ,ephemeral=True)
                await interaction.followup.send(embed=embed)
            else:
                await interaction.response.send_message(embed=embed , ephemeral=True)


    @ui.button(label='قسمت بعد' , custom_id='start_game' , style=discord.ButtonStyle.primary)
    async def subject3(self, interaction:discord.Interaction,_):


        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if (find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                channel_id = find1['channel_embed']
                msg_id = find1['msg_embed']
                scenario = find1['scenario']
                ct_roles = find1['ct_roles']
                tr_roles = find1['tr_roles']
                channel_god = find1['channel_god']
                channel = discord.utils.get(interaction.guild.text_channels , id =channel_id )
                msg = ''
                if channel is not None:
                    async for messager in channel.history(limit=None):
                        if messager.id == msg_id:
                            msg = messager
                            break
                    if msg is not None:
                        if scenario is not None:
                            if len(ct_roles) !=0:
                                if len(tr_roles) !=0:
                                    if channel_god is not None:
                                        total_players = find1['total_players']
                                        if len(total_players) == (len(ct_roles)+len(tr_roles)):
                                            shahr_players = find1['shahr_players']
                                            mafia_players = find1['mafia_players']

                                            for i in range(len(total_players)):
                                                if len(ct_roles)!=0:
                                                    choice1=random.choice(ct_roles)
                                                    ct_roles.remove(choice1)
                                                    choice_player = random.choice(total_players)
                                                    total_players.remove(choice_player)
                                                    choice_player= str(choice_player)
                                                    shahr_players[f'{choice_player}'] = [f'{choice1}']

                                                elif len(tr_roles)!=0:
                                                    choice1=random.choice(tr_roles)
                                                    tr_roles.remove(choice1)
                                                    choice_player = random.choice(total_players)
                                                    total_players.remove(choice_player)
                                                    choice_player= str(choice_player)
                                                    mafia_players[f'{choice_player}'] = [f'{choice1}']
                                                


                                            embed = discord.Embed(
                                                title = f'قسمت سوم تنظیمات',
                                                description=f'به فرم مدیریتی پیشرفته بات مافیا خوش آمدید',
                                                timestamp=datetime.now(),
                                                color= 0x0554FE
                                            )
                                            embed.add_field(name='لیست پلیرها :', value='' , inline=False)
                                            embed.add_field(name='نقش های شهروند:' , value='' , inline=False)
                                            for key , value in shahr_players.items():
                                                users = discord.utils.get(interaction.guild.members , id=int(key))
                                                if users is not None:
                                                    embed.add_field(name=f'{users.name}' , value=f'نقش: {value[0]}', inline=False) 

                                            embed.add_field(name='نقش های مافیا:' ,value='' , inline=False)

                                            for key , value in mafia_players.items():
                                                users = discord.utils.get(interaction.guild.members , id=int(key))
                                                if users is not None:
                                                    embed.add_field(name=f'{users.name}' , value=f'نقش: {value[0]}', inline=False) 
                                            

                                            embed.add_field(name='دستورات مدیریتی' , value='' , inline=False)
                                            embed.add_field(name='/switchin' , value='جا به جایی نقش دو پلیر داخل بازی' , inline=False)
                                            embed.add_field(name='/kharidari' , value='تغییر نقش پلیر داخل بازی' , inline=False)
                                            embed.add_field(name='/hazfplayer' , value='پلیر به لیست کشته شده ها می رود یا همان حذف می شود',inline=True)
                                            embed.add_field(name='/show' , value='نشان دادن نقش پلیر' , inline=True)
                                            embed.add_field(name='/estelam' , value='استعلام ارسال می شود' , inline=True)
                                            embed.add_field(name='/setvoice' , value='وویس جنل پلیر ها ست می شود' , inline=False)

                                            msg=await msg.edit(embed=embed , view=Part3Panel(self.bot))
                                            collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{"part":3 , 'msg_embed':msg.id, 'mafia_players':mafia_players , "shahr_players":shahr_players}})
                                            await interaction.response.send_message('به قسمت سوم رفتید' , ephemeral=True)
                                        else:
                                            await interaction.response.send_message('به تعداد نقش ها کاربر عضو نشده است لطفا یا به صورت دستی یا رای گیری کاربرانی را وارد کنید' , ephemeral=True)
                                    else:
                                        await interaction.response.send_message('لطفا چنل گاد را نیز وارد کنید' , ephemeral=True)
                                else:
                                    await interaction.response.send_message('لطفا اول سناریو را ادد کنید' , ephemeral=True)                
                            else:
                                await interaction.response.send_message('لطفا نقش شهروند اضافه کنید' , ephemeral=True)                

                        else:
                            await interaction.response.send_message('لطفا نقش مافیا اضافه کنید' , ephemeral=True)                


            else:
                await interaction.response.send_message('یا بازی تمام شده است یا شما گاد این بازی نیستید' , ephemeral=True)                
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    



class MafiaPanel(ui.View):

    def __init__(self , bot:Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(label='اضافه/حذف نقش ها' , custom_id='add_roless' , style=discord.ButtonStyle.primary)
    async def subject1(self, interaction:discord.Interaction,_):

        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
                await interaction.response.send_message(view=addroles(self.bot) , ephemeral=True)
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    


    @ui.button(label='اضافه کردن سناریو' , custom_id='add_scenario' , style=discord.ButtonStyle.primary)
    async def subject2(self, interaction:discord.Interaction,_):

        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if (find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                    
                async def sumbit(x):
                    await x.response.defer()
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {'$set':{'scenario':scenario.value}})

                scenario_form = discord.ui.Modal(title='فرم واردن کردن آیدی')
                scenario = discord.ui.TextInput(label='سناریو بازی را وارد کنید:' , style=discord.TextStyle.long , required=True)
                scenario_form.add_item(scenario)
                scenario_form.on_submit = sumbit
                await interaction.response.send_modal(scenario_form)
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)  

    @ui.button(label='اضافه کردن کارت های حرکت آخر' , custom_id='add_carts' , style=discord.ButtonStyle.primary)
    async def subject4(self, interaction:discord.Interaction,_):

        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if (find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                    
                async def sumbit(x):
                    await x.response.defer()
                    carts = scenario.value.split(',')
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {'$set':{'carts':carts}})

                scenario_form = discord.ui.Modal(title='فرم واردن کردن آیدی')
                scenario = discord.ui.TextInput(label='کلمات را با ,  از هم جدا کنید' , style=discord.TextStyle.long , required=True)
                scenario_form.add_item(scenario)
                scenario_form.on_submit = sumbit
                await interaction.response.send_modal(scenario_form)
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    
  
    @ui.button(label='قسمت بعد' , custom_id='next' , style=discord.ButtonStyle.primary)
    async def subject3(self, interaction:discord.Interaction,_):


        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if (find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                channel_id = find1['channel_embed']
                msg_id = find1['msg_embed']
                scenario = find1['scenario']
                ct_roles = find1['ct_roles']
                tr_roles = find1['tr_roles']
                channel_god = find1['channel_god']
                channel = discord.utils.get(interaction.guild.text_channels , id =channel_id )
                msg = ''
                if channel is not None:
                    async for messager in channel.history(limit=None):
                        if messager.id == msg_id:
                            msg = messager
                            break
                    if msg is not None:
                        if scenario is not None:
                            if len(ct_roles) !=0:
                                if len(tr_roles) !=0:
                                    if channel_god is not None:
                                        embed = discord.Embed(
                                            title = f'قسمت دوم تنظیمات',
                                            description=f'از دستورات  از زیر استفاده کنید و بعد از تکمیل کردن به قسمت بعد بروید',
                                            timestamp=datetime.now(),
                                            color= 0x0554FE
                                        )
                                        embed.add_field(name='وارد کردن دستی پلیر ها' ,value='/addplayer' , inline=False)
                                        embed.add_field(name='ارسال فرم ورود' ,value='/joinvote', inline=False)
                                        msg=await msg.edit(embed=embed , view=Part2Panel(self.bot))
                                        await interaction.response.send_message(f'به قسمت دوم خوش آمدید' , ephemeral=True)
                                        collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{"part":2 , 'msg_embed':msg.id}})
                                    else:
                                        await interaction.response.send_message('لطفا چنل گاد را نیز وارد کنید' , ephemeral=True)
                                else:
                                    await interaction.response.send_message('لطفا نقش مافیا اضافه کنید' , ephemeral=True)                
                            else:
                                await interaction.response.send_message('لطفا نقش شهروند اضافه کنید' , ephemeral=True)                

                        else:
                            await interaction.response.send_message('لطفا سناریو اضافه کنید', ephemeral=True)      


            else:
                await interaction.response.send_message('یا بازی تمام شده است یا شما گاد این بازی نیستید' , ephemeral=True)                
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    



class Gif(Plugin):
    def __init__(self , bot:Bot):
        self.bot = bot
    
    async def cog_load(self):
        await super().cog_load()
        self.bot.add_view(addroles(self.bot))
        self.bot.add_view(MafiaPanel(self.bot))
        self.bot.add_view(Part2Panel(self.bot))
        self.bot.add_view(Part3Panel(self.bot))

        


    @commands.Cog.listener() #join to sv jadid
    async def on_guild_join(self,guild):
        try:
            flag=False
            if (find:= new_GUILD.find_one({"owner":guild.owner_id})):
                general = guild.text_channels
                if general is not None:
                    for i in general:
                        if i.permissions_for(guild.me).send_messages:
                            embed=discord.Embed(
                            title=f"Mafia",
                            description= f"🤖thanks for inviting me\n\n🌀 The Best Mafia Bot",
                            timestamp=datetime.now(),
                            color= 0xF6F6F6
                            )
                            embed.set_footer(text='Developed by APA team with ❤' , icon_url=None)
                            embed.set_image(url='https://media.discordapp.net/attachments/1135103098805817477/1201102084464971836/74pZ.gif?ex=65c8987c&is=65b6237c&hm=97a892033c4ac4d1b6706527e2cfa9bbb224a1fec52719ffa227da02ac0b5018&=&width=893&height=670')
                            await i.send(embed=embed)
                            await guild.leave()
                            break
            else:
                new_GUILD.insert_one({'_id':guild.id ,'owner':guild.owner_id , 'server':guild.id ,'key':True})
                general = guild.text_channels
                if general is not None:
                    for i in general:
                        if i.permissions_for(guild.me).send_messages:
                            embed=discord.Embed(
                            title=f"Mafia",
                            description= f"🤖thanks for inviting me\n\n🌀 The Best Mafia Bot ",
                            timestamp=datetime.now(),
                            color= 0xF6F6F6
                            )
                            embed.set_footer(text='Developed by APA team with ❤' , icon_url=None)
                            embed.set_image(url='https://media.discordapp.net/attachments/1135103098805817477/1201102084464971836/74pZ.gif?ex=65c8987c&is=65b6237c&hm=97a892033c4ac4d1b6706527e2cfa9bbb224a1fec52719ffa227da02ac0b5018&=&width=893&height=670')
                            await i.send(embed=embed)
                            flag=True
                            break
            
            if flag==True:
                if (find1:= new_GUILD.find_one({"_id":1})):
                    counter = find1['count_guilds']
                    counter+=1
                    new_GUILD.update_one({'_id':1} ,{"$set":{'count_guilds':counter}})
                else:
                    new_GUILD.insert_one({'_id':1 ,'count_guilds':1})

        except:
            pass

      
        return

    @commands.Cog.listener() #join to sv jadid
    async def on_guild_remove(self,guild):
        try:
            if (find1:= new_GUILD.find_one({"_id":1})):
                counter = find1['count_guilds']
                counter-=1
                new_GUILD.update_one({'_id':1} ,{"$set":{'count_guilds':counter}})
                new_GUILD.delete_one({'_id':guild.id})
        except:
            pass


    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"{ctx.author.mention} command is cooldown wait for {round(error.retry_after)} seconds")

        elif isinstance(error,commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention} you dont have permission')
        elif isinstance(error,commands.CheckFailure):
            pass
        elif isinstance(error ,commands.ArgumentParsingError) :
            pass
        elif isinstance(error,commands.BadArgument):
            pass   
        # elif isinstance(error , commands.BadBoolArgument):
        #     pass
        # elif isinstance(error ,commands.BadInviteArgument ):
        #     pass
        elif isinstance(error ,commands.BadLiteralArgument ):
            pass
        elif isinstance(error , commands.BadUnionArgument):
            pass
        elif isinstance(error,commands.BotMissingRole):
            await ctx.send('bot missing role!')
        elif isinstance(error,commands.BotMissingPermissions ):
            await ctx.send('bot permission is not enough')
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send('channel not found')
        # elif isinstance(error,commands.ChannelNotFound):
        #     pass
        elif isinstance(error ,commands.CommandInvokeError ):
            pass
        elif isinstance(error ,commands.ChannelNotReadable ):
            pass
        elif isinstance(error , commands.CommandError):
            pass


        elif isinstance(error ,commands.MissingPermissions ):
            await ctx.send(f'you dont have permission , for using this bot you better have administrator')



#####################################
    @app_commands.command(
        name='setrole-god',
        description='start mafia bot'
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def setrole(self , interaction:discord.Interaction , role:discord.Role):
        # Your existing code for querying the Minecraft server status here
        collection.insert_one({"server_id":interaction.guild_id , "role_id":role.id})  
        await interaction.response.send_message('role added',ephemeral=True) 

    @app_commands.command(
        name='delrole-god',
        description='start mafia bot'
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def delrolegod(self , interaction:discord.Interaction , role:discord.Role):
        # Your existing code for querying the Minecraft server status here
        collection.delete_one({"server_id":interaction.guild_id , "role_id":role.id})  
        await interaction.response.send_message('role removed',ephemeral=True) 


    @app_commands.command(
        name='switchdeath',
        description='dadane naghshe playere birone bazi be shakhsi dakhele bazi'
    )
    @app_commands.choices(player_role=[
    app_commands.Choice(name='shahrvand' , value=1),
    app_commands.Choice(name='mafia' , value=2),
    ])
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def switchdeath(self , interaction:discord.Interaction ,player:discord.User ,player_role:app_commands.Choice[int], target:discord.User):
        # Your existing code for querying the Minecraft server status here
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                part = find1['part']
                if part != 3 :
                    return await interaction.response.send_message('شما این دستور را فقط در مرحله 3 می توانید اجرا کنید' , ephemeral=True)
                mafia_players = find1['mafia_players']
                shahr_players = find1['shahr_players']
                hazf_mafia = find1['hazf_mafia']
                hazf_shahrvand = find1['hazf_shahrvand']
                total_players = find1['total_players']
                channel_embed = find1['channel_embed']
                msg_embed = find1['msg_embed']

                if str(player.id) in mafia_players or str(player.id) in shahr_players:
                    return await interaction.response.send_message('پلیر هنوز زنده است' ,  ephemeral=True)
                
                if str(target.id) in hazf_mafia or str(target.id) in hazf_shahrvand:
                    return await interaction.response.send_message('پلیر تارگت مرده است' ,  ephemeral=True)
                

                if player_role.value == 2:

                    if str(player.id) in hazf_mafia:
                        if str(target.id) in mafia_players:
                            mafia_players[f'{target.id}'] = hazf_mafia[f'{player.id}']
                            collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id},{'$set':{'mafia_players':mafia_players , 'shahr_players':shahr_players}})
                            await interaction.response.send_message('نقش انتقال یافت' , ephemeral=True)

                        elif str(target.id) in shahr_players:
                            mafia_players[f'{target.id}'] = hazf_mafia[f'{player.id}']

                            del shahr_players[f'{target.id}']

                            collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id},{'$set':{'mafia_players':mafia_players , 'shahr_players':shahr_players}})
                            await interaction.response.send_message('نقش انتقال یافت' , ephemeral=True)
                        
                    else:
                        return await interaction.response.send_message('پلیر از حذف شده های تیم مافیا نیست' , ephemeral=True)
                elif player_role.value == 1:

                    if str(player.id) in hazf_shahrvand:
                        if str(target.id) in mafia_players:

                            shahr_players[f'{target.id}'] = hazf_shahrvand[f'{player.id}']
                            del mafia_players[f'{target.id}']
                            collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id},{'$set':{'mafia_players':mafia_players , 'shahr_players':shahr_players}})
                            await interaction.response.send_message('نقش انتقال یافت' , ephemeral=True)

                        elif str(target.id) in shahr_players:
                            shahr_players[f'{target.id}'] = hazf_shahrvand[f'{player.id}']
                            collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id},{'$set':{'mafia_players':mafia_players , 'shahr_players':shahr_players}})
                            await interaction.response.send_message('نقش انتقال یافت' , ephemeral=True)

                    else:
                        return await interaction.response.send_message('پلیر از حذف شده های تیم شهروند نیست' , ephemeral=True)

                channel_embed = find1['channel_embed']
                msg_embed = find1['msg_embed']

                channel_send = discord.utils.get(interaction.interaction.guild.text_channels ,id=channel_embed)


                embed = discord.Embed(
                    title = f'قسمت سوم تنظیمات',
                    description=f'به فرم مدیریتی پیشرفته بات مافیا خوش آمدید',
                    timestamp=datetime.now(),
                    color= 0x0554FE
                )
                embed.add_field(name='لیست پلیرها :', value='' , inline=False)
                embed.add_field(name='نقش های شهروند:' , value='' , inline=False)
                for key , value in shahr_players.items():
                    users = discord.utils.get(interaction.guild.members , id=int(key))
                    if users is not None:
                        embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 

                embed.add_field(name='نقش های مافیا:' ,value='' , inline=False)

                for key , value in mafia_players.items():
                    users = discord.utils.get(interaction.guild.members , id=int(key))
                    if users is not None:
                        embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                
                embed.add_field(name='پلیر های حذف شده تیم مافیا' , value='' , inline=False)
                if len(hazf_mafia) !=0:
                    for key , value in hazf_mafia.items():
                        users = discord.utils.get(interaction.guild.members , id=int(key))
                        if users is not None:
                            embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                else:
                    embed.add_field(name='پلیری حذف نشده از تیم مافیا' , value='' , inline=False)
                
                embed.add_field(name='پلیر های حذف شده تیم شهروند' , value='' , inline=False)
                if len(hazf_shahrvand) !=0:
                    for key , value in hazf_shahrvand.items():
                        users = discord.utils.get(interaction.guild.members , id=int(key))
                        if users is not None:
                            embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                else:
                    embed.add_field(name='پلیری حذف نشده از تیم شهروند' , value='' , inline=False)


                embed.add_field(name='دستورات مدیریتی' , value='' , inline=False)
                embed.add_field(name='/switchin' , value='جا به جایی نقش دو پلیر داخل بازی' , inline=False)
                embed.add_field(name='/kharidari' , value='تغییر نقش پلیر داخل بازی' , inline=False)
                embed.add_field(name='/hazfplayer' , value='پلیر به لیست کشته شده ها می رود یا همان حذف می شود',inline=True)
                embed.add_field(name='/show' , value='نشان دادن نقش پلیر' , inline=True)
                embed.add_field(name='/estelam' , value='استعلام ارسال می شود' , inline=True)
                embed.add_field(name='/setvoice' , value='وویس جنل پلیر ها ست می شود' , inline=False)

                msg = ''
                async for messager in channel_send.history(limit=None):
                    if messager.id == msg_embed:
                        msg = messager

                msg=await msg.edit(embed=embed , view = Part3Panel(self.bot))
                collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{"msg_embed":msg.id}})


            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    


    @app_commands.command(
        name='alive',
        description='zende kardane yek playere birone bazi'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def alive(self , interaction:discord.Interaction ,player:discord.User):
        # Your existing code for querying the Minecraft server status here
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                part = find1['part']
                if part != 3 :
                    return await interaction.response.send_message('شما این دستور را فقط در مرحله 3 می توانید اجرا کنید' , ephemeral=True)
                mafia_players = find1['mafia_players']
                shahr_players = find1['shahr_players']
                hazf_mafia = find1['hazf_mafia']
                hazf_shahrvand = find1['hazf_shahrvand']
                total_players = find1['total_players']
                channel_embed = find1['channel_embed']
                msg_embed = find1['msg_embed']

                if str(player.id) in mafia_players or str(player.id) in shahr_players:
                    return await interaction.response.send_message('پلیر هنوز زنده است' ,  ephemeral=True)
                
                if str(player.id) in hazf_mafia:
                    mafia_players[f'{player.id}'] = hazf_mafia[f'{player.id}']
                    del hazf_mafia[f'{player.id}']
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {'$set':{'hazf_mafia':hazf_mafia , 'mafia_players':mafia_players}})
                    await interaction.response.send_message('پلیر زنده شد' , ephemeral=True)
                
                elif str(player.id) in hazf_shahrvand:
                    shahr_players[f'{player.id}'] = hazf_shahrvand[f'{player.id}']
                    del hazf_shahrvand[f'{player.id}']
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {'$set':{'hazf_shahrvand':hazf_shahrvand , 'shahr_players':shahr_players}})
                    await interaction.response.send_message('پلیر زنده شد' , ephemeral=True)


            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    

    @app_commands.command(
        name='joinvote',
        description='ferestadan forme vorod be bazi'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def joinvote(self , interaction:discord.Interaction ,channel:discord.TextChannel):
        # Your existing code for querying the Minecraft server status here
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                part = find1['part']
                if part != 2 :
                    return await interaction.response.send_message('شما این دستور را فقط در مرحله 2 می توانید اجرا کنید' , ephemeral=True)
                
                
                scenario = find1['scenario']
                ct_roles = find1['ct_roles']
                tr_roles = find1['tr_roles']
                ct_roles.extend(tr_roles)
                total_players = len(ct_roles)
                embed = discord.Embed(

                title=f"فرم ورود به بازی مافیا",
                description= f'برای ورود به بازی بر روی دکمه ورود بزنید تا به بازی وارد شوید.',
                timestamp=datetime.now(),
                color= 0x0554FE
                )
                embed.add_field(name= 'ظرفیقت:' , value = total_players  , inline=False)
                embed.add_field(name = 'گاد بازی:' , value=interaction.user.mention, inline=False)
                embed.add_field(name = "سناریو بازی:" , value = scenario, inline=False)
                await channel.send(embed=embed , view=joinvoteer(self.bot , interaction.user.id))
                await interaction.response.send_message('ارسال شد' ,  ephemeral=True)
            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    


    @app_commands.command(
        name='setvoice',
        description='voice channeli ke bazi dar an anjam mishavad ra set mikonad'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def setvoice(self , interaction:discord.Interaction , voice:discord.VoiceChannel):
        # Your existing code for querying the Minecraft server status here
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                part = find1['part']
                if part != 3:
                    return await interaction.response.send_message('از این دستور فقط وقتی می توانید استفاده کنید که بازی شروع شده باشد',ephemeral=True)
                await interaction.response.send_message('انجام شد', ephemeral=True)
                collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id},{'$set':{'channel_game':voice.id}})
            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    

    @app_commands.command(
        name='switch',
        description='switch kardane yek player dakhele bazi ba playere birone bazi'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def switch(self , interaction:discord.Interaction , player:discord.User , switch:discord.User):
        # Your existing code for querying the Minecraft server status here
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                part = find1['part']
                if part != 3:
                    return await interaction.response.send_message('از این دستور فقط وقتی می توانید استفاده کنید که بازی شروع شده باشد',ephemeral=True)
                
                mafia_players = find1['mafia_players']
                shahr_players = find1['shahr_players']
                hazf_mafia = find1['hazf_mafia']
                hazf_shahrvand = find1['hazf_shahrvand']
                total_players = find1['total_players']
                channel_embed = find1['channel_embed']
                msg_embed = find1['msg_embed']

                channel_send = discord.utils.get(interaction.guild.text_channels ,id=channel_embed)

                flag1= False
                if player.id in total_players:
                    return await interaction.response.send_message('پلیری که می خواهید او را وارد کنید در بازی هست!' , ephemeral=True)
                
                if switch.id not in total_players:
                    return await interaction.response.send_message('پلیری که می خواهید نقشش را بدهد به کس دیگری در بازی اصلا نیست' , ephemeral=True)
                
                if str(switch.id) in mafia_players:
                    temp_role = mafia_players[f'{switch.id}']
                    del mafia_players[f'{switch.id}']
                    mafia_players[f'{player.id}'] = temp_role
                    await interaction.response.send_message(f'پلیر تغییر کرد' , ephemeral=True)


                elif str(switch.id) in shahr_players:
                    temp_role = shahr_players[f'{switch.id}']
                    del shahr_players[f'{switch.id}']
                    shahr_players[f'{player.id}'] = temp_role
                    await interaction.response.send_message(f'پلیر تغییر کرد' , ephemeral=True)


                elif str(switch.id) in hazf_mafia:
                    temp_role = hazf_mafia[f'{switch.id}']
                    del hazf_mafia[f'{switch.id}']
                    hazf_mafia[f'{player.id}'] = temp_role
                    await interaction.response.send_message(f'پلیر تغییر کرد' , ephemeral=True)

                

                elif str(switch.id) in hazf_shahrvand:
                    temp_role = hazf_shahrvand[f'{switch.id}']
                    del hazf_shahrvand[f'{switch.id}']
                    hazf_shahrvand[f'{player.id}'] = temp_role
                    await interaction.response.send_message(f'پلیر تغییر کرد' , ephemeral=True)

                else:
                    return await interaction.response.send_message('اطلاعات ارسالی درست نبوده' , ephemeral=True)
                
                embed = discord.Embed(
                    title = f'قسمت سوم تنظیمات',
                    description=f'به فرم مدیریتی پیشرفته بات مافیا خوش آمدید',
                    timestamp=datetime.now(),
                    color= 0x0554FE
                )
                embed.add_field(name='لیست پلیرها :', value='' , inline=False)
                embed.add_field(name='نقش های شهروند:' , value='' , inline=False)
                for key , value in shahr_players.items():
                    users = discord.utils.get(interaction.guild.members , id=int(key))
                    if users is not None:
                        embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 

                embed.add_field(name='نقش های مافیا:' ,value='' , inline=False)

                for key , value in mafia_players.items():
                    users = discord.utils.get(interaction.guild.members , id=int(key))
                    if users is not None:
                        embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                
                embed.add_field(name='پلیر های حذف شده تیم مافیا' , value='' , inline=False)
                if len(hazf_mafia) !=0:
                    for key , value in hazf_mafia.items():
                        users = discord.utils.get(interaction.guild.members , id=int(key))
                        if users is not None:
                            embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                else:
                    embed.add_field(name='پلیری حذف نشده از تیم مافیا' , value='' , inline=False)
                
                embed.add_field(name='پلیر های حذف شده تیم شهروند' , value='' , inline=False)
                if len(hazf_shahrvand) !=0:
                    for key , value in hazf_shahrvand.items():
                        users = discord.utils.get(interaction.guild.members , id=int(key))
                        if users is not None:
                            embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                else:
                    embed.add_field(name='پلیری حذف نشده از تیم شهروند' , value='' , inline=False)


                embed.add_field(name='دستورات مدیریتی' , value='' , inline=False)
                embed.add_field(name='/switchin' , value='جا به جایی نقش دو پلیر داخل بازی' , inline=False)
                embed.add_field(name='/kharidari' , value='تغییر نقش پلیر داخل بازی' , inline=False)
                embed.add_field(name='/hazfplayer' , value='پلیر به لیست کشته شده ها می رود یا همان حذف می شود',inline=True)
                embed.add_field(name='/show' , value='نشان دادن نقش پلیر' , inline=True)
                embed.add_field(name='/estelam' , value='استعلام ارسال می شود' , inline=True)
                embed.add_field(name='/setvoice' , value='وویس جنل پلیر ها ست می شود' , inline=False)

                msg = ''
                async for messager in channel_send.history(limit=None):
                    if messager.id == msg_embed:
                        msg = messager

                msg=await msg.edit(embed=embed , view=Part3Panel(self.bot))
                collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{"msg_embed":msg.id}})

            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    

    @app_commands.command(
        name='end',
        description='agar baziyi be esme shoma bashad tamam mishavad'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def end(self , interaction:discord.Interaction):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                collection.delete_one({"server_id":interaction.guild_id , "god":interaction.user.id})
                await interaction.response.send_message('بازی های شما از حافظه پاک شد می توانید بازی جدیدی بسازید' , ephemeral=True)

            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    

    @app_commands.command(
        name='estelam',
        description='neshan dadane estelame bazi bedone goftane naghsh haye ashkhas'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def estelam(self , interaction:discord.Interaction):
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                part = find1['part']
                if part != 3:
                    return await interaction.response.send_message('از این دستور فقط وقتی می توانید استفاده کنید که بازی شروع شده باشد',ephemeral=True)
                total_players = find1['total_players']

                hazf_mafia= find1['hazf_mafia']
                hazf_shahrvand = find1['hazf_shahrvand']

                embed = discord.Embed(
                    title= 'استعلام',
                    description='وضعیت شهر به صورت زیر است'
                )
                embed.add_field(name='تعداد شهروندهای بیرون بازی:' , value=len(hazf_shahrvand) , inline=False)
                embed.add_field(name='تعداد مافیاهای بیرون بازی' , value = len(hazf_mafia) , inline=False)

                channel_players= find1['channel_players']

                channel_send=discord.utils.get(interaction.guild.text_channels , id = channel_players)

                if channel_send is None:
                    return await interaction.response.send_message('چنل پلیرها یافت نشد' , ephemeral=True)

                await channel_send.send(embed=embed)
                await interaction.response.send_message('ارسال شد' , ephemeral=True)
            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    


    @app_commands.command(
        name='showrole',
        description='neshan dadane naghshe role entekhabi be hame'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def showrole(self , interaction:discord.Interaction , player:discord.User):
        # Your existing code for querying the Minecraft server status here
        
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                part = find1['part']
                if part != 3:
                    return await interaction.response.send_message('از این دستور فقط وقتی می توانید استفاده کنید که بازی شروع شده باشد',ephemeral=True)
                total_players = find1['total_players']
                if player.id not in total_players:
                    return await interaction.response.send_message('پلیر انتخابی در بازی نیست',ephemeral=True)

                mafia_players = find1['mafia_players']
                shahr_players = find1['shahr_players']
                hazf_mafia = find1['hazf_mafia']
                hazf_shahrvand = find1['hazf_shahrvand']
                channel_players= find1['channel_players']

                channel_send=discord.utils.get(interaction.guild.text_channels , id = channel_players)

                if channel_send is None:
                    return await interaction.response.send_message('چنل پلیرها یافت نشد' , ephemeral=True)

                if str(player.id) in mafia_players:
                    embed = discord.Embed(
                        title='افشای نقش',
                        description=f'{player.name} : {mafia_players[f"{player.id}"][0]}'
                    )

                    await channel_send.send(embed=embed)
                    await interaction.resposne.send_message('پیام ارسال شد')

                if str(player.id) in shahr_players:
                    embed = discord.Embed(
                        title='افشای نقش',
                        description=f'{player.name} : {shahr_players[f"{player.id}"][0]}'
                    )

                    await channel_send.send(embed=embed)
                    await interaction.resposne.send_message('پیام ارسال شد')
                if str(player.id) in hazf_mafia:
                    embed = discord.Embed(
                        title='افشای نقش',
                        description=f'{player.name} : {hazf_mafia[f"{player.id}"][0]}'
                    )

                    await channel_send.send(embed=embed)
                    await interaction.resposne.send_message('پیام ارسال شد')
                if str(player.id) in hazf_shahrvand:
                    embed = discord.Embed(
                        title='افشای نقش',
                        description=f'{player.name} : {hazf_shahrvand[f"{player.id}"][0]}'
                    )

                    await channel_send.send(embed=embed )
                    await interaction.response.send_message('پیام ارسال شد' , ephemeral=True)


            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    



    @app_commands.command(
        name='hazfplayer',
        description='player be liste hazf shode ha ezafe mishavad'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def hazfplayer(self , interaction:discord.Interaction , player:discord.User):
        # Your existing code for querying the Minecraft server status here
        
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                part = find1['part']
                if part != 3:
                    return await interaction.response.send_message('از این دستور فقط وقتی می توانید استفاده کنید که بازی شروع شده باشد',ephemeral=True)
                
                

                total_players = find1['total_players']
                if player.id in total_players:
                    mafia_players = find1['mafia_players']
                    shahr_players = find1['shahr_players']
                    hazf_mafia = find1['hazf_mafia']
                    hazf_shahrvand = find1['hazf_shahrvand']

                    if str(player.id) in hazf_mafia:
                        return await interaction.response.send_message('پلیر قبلا حذف شده است' , ephemeral=True)
                    elif str(player.id) in hazf_shahrvand:
                        return await interaction.response.send_message('پلیر قبلا حذف شده است' , ephemeral=True)

                    await interaction.response.defer(thinking=True)
                    flag1=False
                    flag_win_mafia=False
                    flag_win_shahrvand = False
                    print(mafia_players)
                    for i in mafia_players.keys():
                        print(type(i))
                        if str(player.id) == i:
                            hazf_mafia[f"{player.id}"] = mafia_players[f'{i}']
                            del mafia_players[f'{i}']
                            collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {'$set':{'hazf_mafia':hazf_mafia , 'mafia_players':mafia_players}})
                            flag1 = True
                            break
                            
                    for i in shahr_players.keys():
                        if str(player.id) == i:
                            hazf_shahrvand[f"{player.id}"] = shahr_players[f'{i}']
                            del shahr_players[f'{i}']
                            collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {'$set':{'hazf_shahrvand':hazf_shahrvand , 'shahr_players':shahr_players}})
                            flag1 = True
                            break
                    
                    print('3')
                    if len(mafia_players) >= len(shahr_players):
                        flag_win_mafia=True

                    
                    elif len(mafia_players) == 0:
                        flag_win_shahrvand = True
                    
                    print('4')
                    if flag_win_mafia == False and flag_win_shahrvand==False:
                        if flag1 == True:
                            await interaction.edit_original_response(content=f'پلیر مورد نظر حذف شد' )
                        else:
                            await interaction.edit_original_response(content=f'پلیر مورد نظر در لیست بازیکنان نیست' )

                    elif flag_win_mafia == True and flag_win_shahrvand==False:
                        if flag1 == True:
                            await interaction.edit_original_response(contet=f'پلیر مورد نظر حذف شد' , view=WinMafia(self.bot))
                        else:
                            await interaction.edit_original_response(content=f'پلیر مورد نظر در لیست بازیکنان نیست' )

                    elif flag_win_mafia == False and flag_win_shahrvand==True:
                        print('5')
                        if flag1 == True:
                            print('6')
                            await interaction.edit_original_response(content=f'پلیر مورد نظر حذف شد' ,view=WinShahrvand(self.bot))
                        else:
                            await interaction.edit_original_response(content=f'پلیر مورد نظر در لیست بازیکنان نیست' )

                    channel_embed = find1['channel_embed']
                    msg_embed = find1['msg_embed']

                    channel_send = discord.utils.get(interaction.interaction.guild.text_channels ,id=channel_embed)


                    embed = discord.Embed(
                        title = f'قسمت سوم تنظیمات',
                        description=f'به فرم مدیریتی پیشرفته بات مافیا خوش آمدید',
                        timestamp=datetime.now(),
                        color= 0x0554FE
                    )
                    embed.add_field(name='لیست پلیرها :', value='' , inline=False)
                    embed.add_field(name='نقش های شهروند:' , value='' , inline=False)
                    for key , value in shahr_players.items():
                        users = discord.utils.get(interaction.guild.members , id=int(key))
                        if users is not None:
                            embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 

                    embed.add_field(name='نقش های مافیا:' ,value='' , inline=False)

                    for key , value in mafia_players.items():
                        users = discord.utils.get(interaction.guild.members , id=int(key))
                        if users is not None:
                            embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                    
                    embed.add_field(name='پلیر های حذف شده تیم مافیا' , value='' , inline=False)
                    if len(hazf_mafia) !=0:
                        for key , value in hazf_mafia.items():
                            users = discord.utils.get(interaction.guild.members , id=int(key))
                            if users is not None:
                                embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                    else:
                        embed.add_field(name='پلیری حذف نشده از تیم مافیا' , value='' , inline=False)
                    
                    embed.add_field(name='پلیر های حذف شده تیم شهروند' , value='' , inline=False)
                    if len(hazf_shahrvand) !=0:
                        for key , value in hazf_shahrvand.items():
                            users = discord.utils.get(interaction.guild.members , id=int(key))
                            if users is not None:
                                embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                    else:
                        embed.add_field(name='پلیری حذف نشده از تیم شهروند' , value='' , inline=False)


                    embed.add_field(name='دستورات مدیریتی' , value='' , inline=False)
                    embed.add_field(name='/switchin' , value='جا به جایی نقش دو پلیر داخل بازی' , inline=False)
                    embed.add_field(name='/kharidari' , value='تغییر نقش پلیر داخل بازی' , inline=False)
                    embed.add_field(name='/hazfplayer' , value='پلیر به لیست کشته شده ها می رود یا همان حذف می شود',inline=True)
                    embed.add_field(name='/show' , value='نشان دادن نقش پلیر' , inline=True)
                    embed.add_field(name='/estelam' , value='استعلام ارسال می شود' , inline=True)
                    embed.add_field(name='/setvoice' , value='وویس جنل پلیر ها ست می شود' , inline=False)

                    msg = ''
                    async for messager in channel_send.history(limit=None):
                        if messager.id == msg_embed:
                            msg = messager

                    msg=await msg.edit(embed=embed , view = Part3Panel(self.bot))
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{"msg_embed":msg.id}})

                    
                else:
                    await interaction.response.send_message('پلیر در لیست بازیکنان نیست' , ephemeral=True)

            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    


    @app_commands.command(
        name='deleteplayer',
        description='hazf kardane player be sorate kamel az liste player ha'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def deleteplayer(self , interaction:discord.Interaction , player:discord.User):
        # Your existing code for querying the Minecraft server status here
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                total_players = find1['total_players']
                if player.id in total_players:
                    total_players.remove(player.id)
                    await interaction.response.send_message('پلیر حذف شد', ephemeral=True)
                else:
                    await interaction.response.send_message('پلیر در لیست بازیکنان نیست' , ephemeral=True)

            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    


    @app_commands.command(
        name='addplayer',
        description='ezafe kardan player be bazi'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def addplayer(self , interaction:discord.Interaction , player:discord.User):
        # Your existing code for querying the Minecraft server status here
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                max_players = len(find1['ct_roles'])
                len2 = len(find1['tr_roles'])
                total_players = find1['total_players']
                if player.id in total_players:
                    return await interaction.response.send_message('پلیر قبلا عضو شده است' , ephemeral=True)
                total_players.append(player.id)
                max_players+=len2
                if len(total_players)>max_players:
                    return await interaction.response.send_message('بیشتر از تعداد نقش ها نمی توانید پلیر اضافه کنید')
                else: 
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{"total_players":total_players}})
                    await interaction.response.send_message('پلیر اضافه شد')
            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    


    @app_commands.command(
        name='kharidari',
        description='taghire naghshe player dar bazi'
    )
    @app_commands.choices(target=[
    app_commands.Choice(name='shahrvand' , value=1),
    app_commands.Choice(name='mafia' , value=2),
    ])
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def kharidari(self , interaction:discord.Interaction , player:discord.User , target:app_commands.Choice[int] , naghsh:str):
        # Your existing code for querying the Minecraft server status here
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                part = find1['part']
                if part != 3:
                    return await interaction.response.send_message('از این دستور فقط وقتی می توانید استفاده کنید که بازی شروع شده باشد',ephemeral=True)
                
                mafia_players = find1['mafia_players']
                shahr_players = find1['shahr_players']
                hazf_mafia = find1['hazf_mafia']
                hazf_shahrvand = find1['hazf_shahrvand']
                total_players = find1['total_players']
                flag1= False

                if target.value ==1:
                    if str(player.id) in mafia_players:
                        shahr_players[f'{player.id}'] = naghsh
                        del mafia_players[f'{player.id}']
                        collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{'mafia_players':mafia_players , 'shahr_players' :shahr_players}})
                        await interaction.response.send_message(f'نقش تغییر یافت')
                    else:
                        return await interaction.response.send_message('پلیر در تیم مافیا نیست شاید مرده است توجه داشته باشید باید شخصی که می خواهید تغییر نقش دهید تارگت آن را تیم مقابل انتخاب کنید' , ephemeral=True)     
                elif target.value==2:
                    if str(player.id) in shahr_players:
                        mafia_players[f'{player.id}'] = naghsh
                        del shahr_players[f'{player.id}']
                        collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{'mafia_players':mafia_players , 'shahr_players' :shahr_players}})
                        await interaction.response.send_message(f'نقش تغییر یافت')
                    else:
                        return await interaction.response.send_message('پلیر در تیم مافیا نیست شاید مرده است توجه داشته باشید باید شخصی که می خواهید تغییر نقش دهید تارگت آن را تیم مقابل انتخاب کنید' , ephemeral=True)     

                channel_embed = find1['channel_embed']
                msg_embed = find1['msg_embed']

                channel_send = discord.utils.get(interaction.guild.text_channels ,id=channel_embed)


                embed = discord.Embed(
                    title = f'قسمت سوم تنظیمات',
                    description=f'به فرم مدیریتی پیشرفته بات مافیا خوش آمدید',
                    timestamp=datetime.now(),
                    color= 0x0554FE
                )
                embed.add_field(name='لیست پلیرها :', value='' , inline=False)
                embed.add_field(name='نقش های شهروند:' , value='' , inline=False)
                for key , value in shahr_players.items():
                    users = discord.utils.get(interaction.guild.members , id=int(key))
                    if users is not None:
                        embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 

                embed.add_field(name='نقش های مافیا:' ,value='' , inline=False)

                for key , value in mafia_players.items():
                    users = discord.utils.get(interaction.guild.members , id=int(key))
                    if users is not None:
                        embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                
                embed.add_field(name='پلیر های حذف شده تیم مافیا' , value='' , inline=False)
                if len(hazf_mafia) !=0:
                    for key , value in hazf_mafia.items():
                        users = discord.utils.get(interaction.guild.members , id=int(key))
                        if users is not None:
                            embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                else:
                    embed.add_field(name='پلیری حذف نشده از تیم مافیا' , value='' , inline=False)
                
                embed.add_field(name='پلیر های حذف شده تیم شهروند' , value='' , inline=False)
                if len(hazf_shahrvand) !=0:
                    for key , value in hazf_shahrvand.items():
                        users = discord.utils.get(interaction.guild.members , id=int(key))
                        if users is not None:
                            embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                else:
                    embed.add_field(name='پلیری حذف نشده از تیم شهروند' , value='' , inline=False)


                embed.add_field(name='دستورات مدیریتی' , value='' , inline=False)
                embed.add_field(name='/switchin' , value='جا به جایی نقش دو پلیر داخل بازی' , inline=False)
                embed.add_field(name='/kharidari' , value='تغییر نقش پلیر داخل بازی' , inline=False)
                embed.add_field(name='/hazfplayer' , value='پلیر به لیست کشته شده ها می رود یا همان حذف می شود',inline=True)
                embed.add_field(name='/show' , value='نشان دادن نقش پلیر' , inline=True)
                embed.add_field(name='/estelam' , value='استعلام ارسال می شود' , inline=True)
                embed.add_field(name='/setvoice' , value='وویس جنل پلیر ها ست می شود' , inline=False)

                msg = ''
                async for messager in channel_send.history(limit=None):
                    if messager.id == msg_embed:
                        msg = messager

                msg=await msg.edit(embed=embed , view=Part3Panel(self.bot))
                collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{"msg_embed":msg.id}})


            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    



    @app_commands.command(
        name='switchin',
        description='switch kardane 2 playere dakhele bazi'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def switchin(self , interaction:discord.Interaction , first_player:discord.User , second_player:discord.User):
        # Your existing code for querying the Minecraft server status here
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                part = find1['part']
                if part != 3:
                    return await interaction.response.send_message('از این دستور فقط وقتی می توانید استفاده کنید که بازی شروع شده باشد',ephemeral=True)
                
                mafia_players = find1['mafia_players']
                shahr_players = find1['shahr_players']
                hazf_mafia = find1['hazf_mafia']
                hazf_shahrvand = find1['hazf_shahrvand']
                total_players = find1['total_players']
                flag1= False

                if str(first_player.id) in mafia_players and str(second_player.id) in shahr_players:

                    shahr_players[f'{first_player.id}'] = shahr_players[f'{second_player.id}']
                    mafia_players[f'{second_player.id}'] = mafia_players[f'{first_player.id}']
                    del mafia_players[f'{first_player.id}']
                    del shahr_players[f'{second_player.id}']

                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{'mafia_players':mafia_players , 'shahr_players' :shahr_players}})
                    await interaction.response.send_message(f'نقش های آن ها عوض شد' , ephemeral=True)
                    

                elif str(first_player.id) in shahr_players and str(second_player.id) in mafia_players:

                    shahr_players[f'{second_player.id}'] = shahr_players[f'{first_player.id}']
                    mafia_players[f'{first_player.id}'] = mafia_players[f'{second_player.id}']
                    del mafia_players[f'{second_player.id}']
                    del shahr_players[f'{first_player.id}']
                    
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{'mafia_players':mafia_players , 'shahr_players' :shahr_players}})
                    await interaction.response.send_message(f'نقش های آن ها عوض شد' , ephemeral=True)
                else:
                    return await interaction.response.send_message(f'یا هر دو پلیر در یک تیم هستند یا یافت نشده اند یا در زنده نیستند' , ephemeral=True)
                channel_embed = find1['channel_embed']
                msg_embed = find1['msg_embed']
                channel_send = discord.utils.get(interaction.guild.text_channels ,id=channel_embed)

                embed = discord.Embed(
                    title = f'قسمت سوم تنظیمات',
                    description=f'به فرم مدیریتی پیشرفته بات مافیا خوش آمدید',
                    timestamp=datetime.now(),
                    color= 0x0554FE
                )

                embed.add_field(name='لیست پلیرها :', value='' , inline=False)

                embed.add_field(name='نقش های شهروند:' , value='' , inline=False)

                for key , value in shahr_players.items():
                    users = discord.utils.get(interaction.guild.members , id=int(key))
                    if users is not None:
                        embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 

                embed.add_field(name='نقش های مافیا:' ,value='' , inline=False)

                for key , value in mafia_players.items():
                    users = discord.utils.get(interaction.guild.members , id=int(key))
                    if users is not None:
                        embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 

                embed.add_field(name='پلیر های حذف شده تیم مافیا' , value='' , inline=False)
                if len(hazf_mafia) !=0:
                    for key , value in hazf_mafia.items():
                        users = discord.utils.get(interaction.guild.members , id=int(key))
                        if users is not None:
                            embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 


                else:
                    embed.add_field(name='پلیری حذف نشده از تیم مافیا' , value='' , inline=False)
                
                embed.add_field(name='پلیر های حذف شده تیم شهروند' , value='' , inline=False)
                if len(hazf_shahrvand) !=0:
                    for key , value in hazf_shahrvand.items():
                        users = discord.utils.get(interaction.guild.members , id=int(key))
                        if users is not None:
                            embed.add_field(name=f'{users.name}' , value=f'نقش: {value}', inline=False) 
                else:
                    embed.add_field(name='پلیری حذف نشده از تیم شهروند' , value='' , inline=False)


                embed.add_field(name='دستورات مدیریتی' , value='' , inline=False)
                embed.add_field(name='/switchin' , value='جا به جایی نقش دو پلیر داخل بازی' , inline=False)
                embed.add_field(name='/kharidari' , value='تغییر نقش پلیر داخل بازی' , inline=False)
                embed.add_field(name='/hazfplayer' , value='پلیر به لیست کشته شده ها می رود یا همان حذف می شود',inline=True)
                embed.add_field(name='/show' , value='نشان دادن نقش پلیر' , inline=True)
                embed.add_field(name='/estelam' , value='استعلام ارسال می شود' , inline=True)
                embed.add_field(name='/setvoice' , value='وویس جنل پلیر ها ست می شود' , inline=False)

                msg = ''
                async for messager in channel_send.history(limit=None):
                    if messager.id == msg_embed:
                        msg = messager

                msg=await msg.edit(embed=embed , view=Part3Panel(self.bot))

                collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{"msg_embed":msg.id}})



            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    



    @app_commands.command(
        name='sch',
        description='baraye set kardane tanzimat ersal etelaat bazi be god va player ha'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def sch(self , interaction:discord.Interaction , channel_god:discord.TextChannel , channel_players:discord.TextChannel):
        # Your existing code for querying the Minecraft server status here
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if ( find1:=collection.find_one({"server_id":interaction.guild_id , "god":interaction.user.id})):
                if channel_players is None:
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{"channel_god":channel_god.id}})
                    await interaction.response.send_message("done!",ephemeral=True)
                else:
                    collection.update_one({"server_id":interaction.guild_id , "god":interaction.user.id} , {"$set":{"channel_god":channel_god.id , 'channel_players':channel_players.id}})
                    await interaction.response.send_message("done!",ephemeral=True)
            else:
                await interaction.response.send_message('شما بازی در حال اجرایی ندارید')
                            
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    


    @app_commands.command(
        name='mafiastart',
        description='start mafia bot'
    )
    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def gifgenerate(self , interaction:discord.Interaction , channel:discord.TextChannel):
        # Your existing code for querying the Minecraft server status here
        user_roles = interaction.user.roles
        roler = ''
        flag = False
        for role in user_roles:
            if (find:=collection.find_one({'server_id':interaction.guild_id , "role_id":role.id})):
                roler = role
                flag=True
                break
        if flag == True:
            if (find:=collection.find_one({"server_id":interaction.guild_id,"god":interaction.user.id})):
                return await interaction.response.send_message('شما از قبل بازی ای در حافظه دارید با دستور /end  آن را پاک کنید' , ephemeral=True)

            embed = discord.Embed(

                title=f"پنل تنظیمات بازی مافیا",
                description= f'به بازی مافیا خوش آمدید \nلطفا جهت استفاده از ربات به ترتیت نقش هارا وارد کنید و بعد از آن سناریو و بعد با استفاده از دستور زیر چنل ارسال اطلاعات به گاد را انتخاب کنید و بعد گزینه قسمت بعد را بزنید \n\n',
                timestamp=datetime.now(),
                color= 0x0554FE
            )
            embed.add_field(name='از دستور زیر چنل گاد و پلیر هارا تنظیم کنید' , value='' , inline=False)
            embed.add_field(name='/sch' , value='تنظیم چنل گاد و پلیر' , inline=False)
            try:
                msg=await channel.send(embed=embed , view=MafiaPanel(self.bot))
                collection.insert_one({"server_id":interaction.guild_id,"god":interaction.user.id , "ct_roles":[],'tr_roles':[] , 'ct_tozih':[] , 'tr_tozih':[] , 'total_players':[],'shahr_players':{},"mafia_players":{},'hazf_mafia':{} , 'hazf_shahrvand':{},'scenario':None , 'channel_embed':channel.id , 'msg_embed':msg.id , 'channel_god':None , "channel_players":None ,'embed_players':None , 'part':1 ,'day_time':True, 'night_time':False , 'moarefe':True ,'turn':1 , 'start':False , 'real_names':{} , 'channel_game':None , 'time':None , 'msg_timer':None , 'raygiri':[] , 'tedade_ray':{} , 'msg_raygiri':None , 'player_cart':None ,'carts':None , 'reply_count':None , 'reply_players':None , 'voters':[]})

                
            except:
                await interaction.response.send_message('something went wrong' , ephemeral=True)
        else:
            await interaction.response.send_message('you dont have require role' , ephemeral=True)    


        

async def setup(bot : Bot):
    await bot.add_cog(Gif(bot))
