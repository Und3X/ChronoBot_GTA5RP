import os
from datetime import datetime as dt
import discord
from discord.ext import commands
from discord.colour import Colour as DiscordColour
from table2ascii import table2ascii as t2a, PresetStyle

TOKEN = os.getenv('TOKEN')
GUILD = "💊🔞"#os.getenv('DISCORD_GUILD')
ADMIN_ROLE_NAME = "Chief"


class MyClient(discord.Client):     
    async def on_ready(self):
        
        self.CHANNEL_ID = 0
        self.GUILD_ID = 0
        self.TIME_SK = dt.now()
        self.TIME_SH = dt.now()
        self.TIME_ORG = dt.now()
        
        global ADMIN_ROLE_NAME
        self.NOTIFY_ROLE_NAME = 'TimeNotify'
        
        print('Logged on as', self.user)
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name} (id: {guild.id})'
        )
        self.GUILD_ID = guild.id
        self.ADMIN_ROLE = discord.utils.get(self.get_guild(guild.id).roles,name=ADMIN_ROLE_NAME)
        self.NOTIFY_ROLE = discord.utils.get(self.get_guild(guild.id).roles,name=self.NOTIFY_ROLE_NAME)

    async def on_message(self, message:discord.message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if self.user in message.mentions:
            if '!set_info_channel' in message.content and message.author.get_role(self.ADMIN_ROLE.id)!=None:
                self.CHANNEL_ID = message.channel.id
                await message.channel.send(embed=self.alert_generate("Информация", "Канал для информирования установлен, как текущий.", discord.Color.green()))
            
            if '!get_info_channel' in message.content and message.author.get_role(self.ADMIN_ROLE.id)!=None:
                channel = self.get_channel(self.CHANNEL_ID)
                await message.channel.send(embed=self.alert_generate("Информация", f"Канал для информирования на данный момент установлен, как {channel.name}.", discord.Color.blue()))
                
            if '!set_notify_role_name' in message.content and message.author.get_role(self.ADMIN_ROLE.id)!=None:
                try:
                    name = str(message.content).split(" ")[1].strip()
                    self.NOTIFY_ROLE_NAME = name
                    self.NOTIFY_ROLE = discord.utils.get(self.get_guild(self.GUILD_ID).roles,name=name)
                    await message.channel.send(embed=self.alert_generate("Информация", f"Роль для уведомлений установлена как {name}.", discord.Color.green()))
                except:
                    await message.channel.send(embed=self.alert_generate("Информация", f"Введите корректное значение, имя роли не может содержать пробелов.", discord.Color.red()))
                                
            if '!get_notify_role_name' in message.content and message.author.get_role(self.ADMIN_ROLE.id)!=None:
                await message.channel.send(embed=self.alert_generate("Информация", f"Роль для уведомлений установлена как {self.NOTIFY_ROLE.name}.", discord.Color.blue()))
                
        if message.content.startswith('+ск') and message.author.get_role(self.NOTIFY_ROLE.id)!=None:
            self.TIME_SK = dt.Now.AddHours(3)
            await message.channel.send(embed=self.alert_generate("Информация", f"СК время обновлено.\nСледующий СК: {name}.", discord.Color.green()))
            
        if message.content.startswith('+сх') and message.author.get_role(self.NOTIFY_ROLE.id)!=None:
            self.TIME_SH = dt.Now.AddHours(4)
            await message.channel.send(embed=self.alert_generate("Информация", f"СХ время обновлено.\nСледующий СХ: {name}.", discord.Color.green()))
            
        if message.content.startswith('+о') and message.author.get_role(self.NOTIFY_ROLE.id)!=None:
            self.TIME_ORG = dt.Now.AddHours(2)
            await message.channel.send(embed=self.alert_generate("Информация", f"'Организация' время обновлено.\nСледующая 'Организация': {name}.", discord.Color.green()))
        
        if message.content.startswith("???") and message.author.get_role(self.NOTIFY_ROLE.id)!=None:
                await message.channel.send(f'```{self.generate_table_result()}```')
            
        if message.content == 'ping':
            await message.channel.send(f'pong. ```Channel ID: {message.channel.id}```')
            
        date = dt.now().strftime("%d/%m/%y %H:%M:%S")
        roles = ", ".join([x.name for x in message.author.roles])
        print(f"[{date}] [DEBUG] MSG: {message.content} | From: {message.author} ({roles}) | Channel: {message.channel.name} ({message.channel.id})")
            
    def alert_generate(self, title:str ,text:str, color:DiscordColour):
        embed = discord.Embed(
            title=title,
            description=text,
            color=color
        )
        return embed
    
    def generate_table_result(self):
        # In your command:
        output = t2a(
            header=["Огра", "Схемы", "Скользкая"],
            body=[[self.TIME_ORG.strftime("%H:%M:%S"),self.TIME_SH.strftime("%H:%M:%S"),self.TIME_SK.strftime("%H:%M:%S")]],
            style=PresetStyle.thin_compact
        )
        return output

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
    
    
client.run(TOKEN)