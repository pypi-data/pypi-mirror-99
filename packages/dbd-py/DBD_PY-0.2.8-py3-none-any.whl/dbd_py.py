functions = {"functions":{"$eval":"noarg","$title[":"arg","$description[":"arg","$color[":"arg","$addField[":"arg","$thumbnail[":"arg","$image[":"arg","$footer[":"arg","$author[":"arg","$authorIcon[":"arg","$footerIcon[":"arg","$deletecommand":"noarg","$addReactions[":"arg","$addCmdReactions[":"arg","$addTimestamp":"noarg","$authorURL[":"arg","$suppressErrors[":"arg","$embedSuppressErrors[":"arg","$textSplit[":"arg","$useChannel[":"arg","$replyIn[":"arg","$nomention":"noarg", "$allowMention":"noarg","$blackListIDs[":"arg","$blackListServers[":"arg","$blackListUsers[":"arg","$blackListRoles[":"arg","$blackListRolesIDs[":"arg","$channelSendMessage[":"arg","$onlyIf[":"arg","$if[":"arg","$else":"noarg","$endIf":"noarg","$botLeave[":"arg","$dm[":"arg","$ban[":"arg","$kick[":"arg","$unban[":"arg","$setVar[":"arg","$setServerVar[":"arg","$setChannelVar[":"arg","$setUserVar[":"arg","$ignoreTriggerCase":"noarg","$onlyForServers[":"arg","$onlyForUsers[":"arg","$onlyForRoles[":"arg","$onlyForIDs[":"arg","$onlyForChannels[":"arg","$onlyIfMessageContains[":"arg","$onlyNSFW[":"arg","$pyEval[":"arg","$reactionCollector[":"arg", "$reactionPages[":"arg", "$reactionPage[":"arg", "$print[":"arg", "$editIn[":"arg", "$editEmbedIn[":"arg", "$status[":"arg", "$cooldown[":"arg", "$setLocalVar[":"arg", "$getReactions[":"arg", "$end":"noarg"},"adds":{"$message":"noarg","$splitText[":"arg","$math[":"arg","$authorID":"noarg","$authorAvatar":"noarg","$allMembersCount":"noarg","$argCount[":"arg","$message[":"arg","$mentioned[":"arg","$noMentionMessage[":"arg","$noMentionMessage":"noarg","$getTextSplitLength":"noarg","$replaceText[":"arg","$authorOfMessage[":"arg","$guildID":"noarg","$isBot[":"arg","$isAdmin[":"arg","$isNumber[":"arg","$joinSplitText[":"arg","$serverCount":"noarg","$ping":"noarg","$channelID":"noarg","$channelName[":"arg","$channelID[":"arg","$serverIcon":"noarg","$mentionedChannels[":"arg","$mentionedRoles[":"arg","$uptime":"noarg","$userAvatar[":"arg","$getVar[":"arg","$getServerVar[":"arg","$getUserVar[":"arg","$getChannelVar[":"arg","$leaderboard[":"arg","$guildID[":"arg","$getBotInvite":"noarg","$random":"noarg","$random[":"arg","$randomMention":"noarg","$randomUserID":"noarg","$randomUser":"noarg","$botID":"noarg","$commandsCount":"noarg","$collector[":"arg", "$username[":"arg", "$username":"noarg", "$nickname[":"arg", "$nickname":"noarg", "$getLocalVar[":"arg", "$emoji":"noarg", "$randomText[":"arg", "$emoteUrl[":"arg", "$tag[":"arg", "$tag":"noarg"}}
import time as _time
import sqlite3 as _sql
_startTime=_time.time()
def _syntax(code):
	func = []
	funstr=""
	skob=0
	linec=0
	for fun in code:
		linec+=1
		if any(fun.startswith(func) for func in functions["functions"]):
			if skob>0:
				skob-=1
				func.append(funstr)
			if linec==len(code):
				func.append(fun)
			else:
				try:
					if functions["functions"][fun]=="noarg":
						func.append(fun)
					else:
						if fun.endswith("\]"):
							funstr=fun[:-2]+"]"
							skob+=1
						elif fun.endswith("]"):
							func.append(fun)
						else:
							funstr=fun
							skob+=1
				except:
					if fun.endswith("\]"):
						funstr=fun[:-2]+"]"
						skob+=1
					elif fun.endswith("]"):
						func.append(fun)
					else:
						funstr=fun
						skob+=1
		elif fun.endswith("\]") and skob>0:
			funstr+="/n"+fun[:-2]+"]"
		elif fun.endswith("]") and skob>0:
			funstr+="/n"+fun
			func.append(funstr)
			funstr=""
			skob-=1
		else:
			if skob>0:
				funstr+="/n"+fun
			else:
				func.append(fun)
	return func
class _variables():
	def __init__(self,conn,values):
		if conn:
			self._conn=conn
			self._cursor=conn.cursor()
		else:
			self._conn=False
		self._values=values
		self._valstr="id INT"
		for var in values:
			self._valstr+=",\n	var"+var+" TEXT"
		self._adds=""
		for v in values:
			self._adds+=f",'{values[v]}'"
	def get(self,thing,type,where='11'):
		if self._conn:
			if self._cursor.execute(f"SELECT id FROM {type} WHERE {where[0]} LIKE '{where[1]}'").fetchone() is None:
				self._cursor.execute(f"INSERT INTO {type} VALUES('{where[1]}'{self._adds})")
			if self._cursor.execute(f"SELECT var{thing} FROM {type} WHERE {where[0]} = '{where[1]}'").fetchone()[0] is None:
				self._cursor.execute(f'UPDATE {type} SET var{thing}="{self._values[thing]}" WHERE {where[0]}="{where[1]}"')
			self._conn.commit()
			return self._cursor.execute(f"SELECT var{thing} FROM {type} WHERE {where[0]} LIKE '{where[1]}'").fetchone()[0]
		else:
			return "null"
	def set(self,things,type,where="11"):
		if self._conn:
			if self._cursor.execute(f"SELECT var{things[0]} FROM {type} WHERE {where[0]} LIKE '{where[1]}'").fetchone() is None:
				self._cursor.execute(f"INSERT INTO {type} VALUES('{where[1]}'{self._adds})")
			self._cursor.execute(f"UPDATE {type} SET var{things[0]}='{things[1]}' WHERE {where[0]} == {where[1]}")
			self._conn.commit()

class dbot():
	def __init__(self, info):
		import os
		try:
			import discord
			from discord.ext import commands
		except:
			print("Нет модуля discord, начинаем установку!")
			os.system("pip install discord")
		try:
			import asyncio
		except:
			print("Нет модуля asyncio, начинаем установку!")
			os.system("pip install asyncio")
		import discord
		from discord.ext import commands
		self._prefix=info["prefix"]
		self._token=info["token"]
		self._vars={}
		try:
			if info["self"] in ["true","false"]:
				self._self=info["self"]=="true"
			else:
				print(f"Создание бота\nУкажите true или false в self!")
				self._self=False
		except:
			self._self=False
		try:
			self._path=info["path"][:len(info["path"])-len(os.path.basename(info["path"]))]+"vars.db"
		except Exception as e:
			self._path=False
		self._codes={}
		self._count=0
		self._codes["commands"]={}
		self._codes["events"]={}
		self._codes["wait"]={}
		self._cooldown={}
		self._client=commands.Bot(command_prefix=self._prefix, intents=discord.Intents.all())
		self._client.remove_command(help)

	def var(self, info):
		self._vars[info["name"]]=info["value"]

	def wait(self, info):
		self._codes["wait"][info["name"]]={}
		code=[]
		code=info["code"].split("\n")
		self._codes["wait"][info["name"]]["name"]=info["name"]
		code = _syntax(code)
		try:
			if info["lang"] in ["unstable","classic"]:
				if info["lang"]=="unstable":
					code=code[::-1]
			else:
				print(f"Ожидание: {info['prefix']+info['name']}\nУкажите unstable или classic в lang!")
		except:
			pass
		self._codes["wait"][info["name"]]["code"]=code
		try:
			if info["type"] in ["true","false"]:
				self._codes["wait"][info["name"]]["type"]=info["type"]=="true"
			else:
				print(f"Ожидание: {info['name']}\nУкажите true или false в type!")
				self._codes["wait"][info["name"]]["type"]=False
		except:
			self._codes["wait"][info["name"]]["type"]=False

	def event(self, info):
		self._codes["events"][info["name"]]={}
		code=[]
		code=info["code"].split("\n")
		self._codes["events"][info["name"]]["name"]=info["name"]
		code = _syntax(code)
		try:
			if info["lang"] in ["unstable","classic"]:
				if info["lang"]=="unstable":
					code=code[::-1]
			else:
				print(f"Эвент: {info['prefix']+info['name']}\nУкажите unstable или classic в lang!")
		except:
			pass
		self._codes["events"][info["name"]]["code"]=code
		try:
			if info["type"] in ["true","false"]:
				self._codes["events"][info["name"]]["type"]=info["type"]=="true"
			else:
				print(f"Эвент: {info['name']}\nУкажите true или false в type!")
				self._codes["events"][info["name"]]["type"]=False
		except:
			self._codes["events"][info["name"]]["type"]=False
		try:
			self._codes["events"][info["name"]]["channel"]=info["id"]
		except:
			self._codes["events"][info["name"]]["channel"]=False

	def command(self, info):
		if isinstance(info["name"], list):
			self._count+=1
			self._codes["commands"][self._count]={}
			code=[]
			code=info["code"].split("\n")
			self._codes["commands"][self._count]["name"]=info["name"]
			code = _syntax(code)
			try:
				if info["lang"] in ["unstable","classic"]:
					if info["lang"]=="unstable":
						code=code[::-1]
				else:
					print(f"Комманда: {info['prefix']+info['name']}\nУкажите unstable или classic в lang!")
			except:
				pass
			self._codes["commands"][self._count]["code"]=code
			try:
				self._codes["commands"][self._count]["prefix"]=info["prefix"]
			except:
				self._codes["commands"][self._count]["prefix"]=self._prefix
			try:
				if info["type"] in ["true","false"]:
					self._codes["commands"][self._count]["type"]=info["type"]=="true"
				else:
					print(f"Комманда: {info['prefix']+info['name']}\nУкажите true или false в type!")
					self._codes["commands"][self._count]["type"]=False
			except:
				self._codes["commands"][self._count]["type"]=False
		else:
			print("Тригер должен быть списком!")

	def run(self):
		if self._path:
			self._db=_variables(_sql.connect(self._path),self._vars)
		else:
			self._db=_variables(False,self._vars)
		_start(self._client, self)

def _start(client, info):
	
	@client.event
	async def on_ready():
		import discord
		import asyncio 
		import datetime
		timedelta=datetime.timedelta
		if info._path:
			valstr=info._db._valstr
			adds=info._db._adds
			gs=["servers", "globals", "channels"]
			for g in client.guilds:
				gs.append("server"+str(g.id))
			for n in gs:
				info._db._cursor.execute("""CREATE TABLE IF NOT EXISTS """+str(n)+"""(
			"""+valstr+"""
			)""")
			for var in info._db._values:
				for n in gs:
					try:
						info._db._cursor.execute(f"alter table {n} add column 'var{var}' 'TEXT'")
					except:
						pass
			info._db._conn.commit()
		if "ready" in info._codes["events"]:
			if info._codes["events"]["ready"]["channel"]:
				channel = discord.utils.get(client.get_all_channels(), id=int(info._codes["events"]["ready"]["channel"]))
				message = await channel.fetch_message(list(await channel.history(limit=1).flatten())[0].id)
				await use([message, "ready", "events", "null"],info)
		else:
			print("Бот онлайн!")

	@client.event
	async def on_message(message):
		exe = True
		ex=False
		if exe:
			for cmd in info._codes["commands"]:
				ex=False
				for trig in info._codes["commands"][cmd]["name"]:
					ex=False
					trig = await replaces([info._codes["commands"][cmd]["prefix"]+trig, info, "", [message, cmd, "commands", ""], [], True, {}, {}, "", message])
					if message.content.lower().startswith(str(trig.lower())):
						if "$ignoreTriggerCase" in info._codes["commands"][cmd]["code"]:
							ex=True
						else:
							if message.content.startswith(trig):
								ex=True
					if ex:
						if info._codes["commands"][cmd]["type"]:
							await use([message, cmd, "commands", message.content[len(trig):]],info)
						else:
							if message.author.id!=client.user.id:
								await use([message, cmd, "commands", message.content[len(trig):]],info)
	if info._self:
		client.run(info._token, bot=False)
	else:
		client.run(info._token)

async def use(need, info):
	import discord
	import random
	import ast
	import json
	import time 
	import asyncio
	import datetime
	timedelta=datetime.timedelta
	global _startTime
	binstr = ""
	collector = {}
	go=None
	pages=[]
	edits=[]
	msg = ""
	vars={}
	content = need[3]
	try:
		emoji=need[4]
	except:
		emoji=""
	emb = [False, discord.Embed()]
	lines=eval(str(list(info._codes[need[2]][need[1]]["code"])))
	reactions = []
	linec = 0
	error = [True,""]
	br = True
	split = []
	est = False
	ctx = need[0].channel
	if "$ignoreTriggerCase" in lines:
		lines.remove("$ignoreTriggerCase")
	if "$eval" in lines:
		rel=lines[lines.index("$eval")+1:]
		lines=lines[:lines.index("$eval")]
		lines=lines + _syntax(content.split("\n")) + rel
	linec=0
	allow=True
	ment=""
	if "$mention" in lines:
		lines.remove("$mention")
		ment=str(need[0].author.mention)+"\n"
	if "$allowMention" in lines:
		lines.remove("$allowMention")
		allow=False
	if allow:
		for m in need[0].mentions:
			content=content.replace(str(m.mention).replace("!",""), str(m.display_name))
	for line in lines:
		linec+=1
		reline = line
		if go==True:
			if line.startswith("$else"):
				go=False
				continue
			elif line.startswith("$endIf"):
				go=None
				continue
			else:
				continue
		elif go==False:
			if line.startswith("$endIf"):
				go=None
				continue
		elif go=="null":
			if line.startswith("$endIf"):
				go=None
				continue
			else:
				continue
		else:
			if line.startswith("$else"):
				go="null"
				continue
			elif line.startswith("$endIf"):
				go=None
				continue
		def remember(text):
			global function
			function = text
			return True
		if any(line.startswith(func) and remember(func) for func in functions["functions"]):
			if functions["functions"][function]=="arg":
				if line.endswith("]"):
					line=line[:-1]
			try:
				line = await replaces([line, info, content.replace("[","⦍").replace("]","⦎"), need, split, allow, collector, vars, emoji, msg])
				line=line.replace("/n","\n")
				if line.startswith("$title["):
					emb[1].title=line[len("$title["):]
					emb[0]=True
				elif line.startswith("$description["):
					emb[1].description=line[len("$description["):]
					emb[0]=True
				elif line.startswith("$color["):
					try:
						rgb=list(int(line[len("$color["):][i:i+2], 16) for i in (0, 2, 4))
						emb[1].color=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2])
						emb[0]=True
					except:
						raise TypeError("Неправильный HEX в $color")
				elif line.startswith("$addField["):
					emb[1].add_field(name=line[len("$addField["):].split(";")[0], value=line[len("$addField["):].split(";")[1], inline=True)
					emb[0]=True
				elif line.startswith("$thumbnail["):
					emb[1].set_thumbnail(url=line[len("$thumbnail["):])
					emb[0]=True
				elif line.startswith("$image["):
					emb[1].set_image(url=line[len("$image["):])
					emb[0]=True
				elif line.startswith("$footer["):
					emb[1].set_footer(text=line[len("$footer["):])
					emb[0]=True
				elif line.startswith("$author["):
					emb[1].set_author(name=line[len("$author["):])
					emb[0]=True
				elif line.startswith("$footerIcon["):
					if not isinstance(emb[1].footer.text, str):
						emb[1].set_footer(text="", icon_url=line[len("$footerIcon["):])
					else:
						emb[1].set_footer(text=emb[1].footer.text, icon_url=line[len("$footerIcon["):])
					emb[0]=True
				elif line.startswith("$authorIcon["):
					if not isinstance(emb[1].author.name, str):
						emb[1].set_author(name="", icon_url=line[len("$authorIcon["):])
					else:
						emb[1].set_author(name=emb[1].author.name, icon_url=line[len("$authorIcon["):])
					emb[0]=True
				elif line.startswith("$deletecommand"):
					await need[0].delete()
				elif line.startswith("$addReactions["):
					reactions = line[len("$addReactions["):].split(";")
				elif line.startswith("$addCmdReactions["):
					for react in line[len("$addCmdReactions["):].split(";"):
						await need[0].add_reaction(react)
				elif line.startswith("$addTimestamp"):
					emb[1].timestamp = datetime.datetime.utcnow()
					emb[0]=True
				elif line.startswith("$authorURL["):
					if not isinstance(emb[1].author.name, str):
						if not isinstance(emb[1].author.icon_url, str):
							emb[1].set_author(name="", url=line[len("$authorURL["):])
						else:
							emb[1].set_author(name="", icon_url=emb[1].author.icon_url, url=line[len("$authorURL["):])
					else:
						emb[1].set_author(name=emb[1].author.name, icon_url=emb[1].author.icon_url, url=line[len("$authorURL["):])
					emb[0]=True
				elif line.startswith("$suppressErrors["):
					error[1]=line[len("$suppressErrors["):]
					error[0]=False
				elif line.startswith("$embedSuppressErrors["):
					line = line[len("$embedSuppressErrors["):]
					error[0]="Embed"
					error[1]=line
				elif line.startswith("$replyIn["):
					line = line[len("$replyIn["):]
					if line.endswith("s"):
						line=line.rstrip("s")
					elif line.endswith("m"):
						line=line.rstrip("m")
						line=int(line)*60
					elif line.endswith("h"):
						line=line.rstrip("h")
						line=int(line)*60*60
					elif line.endswith("d"):
						line=line.rstrip("d")
						line=int(line)*60*60*24
					await asyncio.sleep(int(line))
				elif line.startswith("$textSplit["):
					split = str(line[len("$textSplit["):].split(";")[0]).split(line[len("$textSplit["):].split(";")[1])
				elif line.startswith("$useChannel["):
					channel = discord.utils.get(info._client.get_all_channels(), id = int(line[len("$useChannel["):]))
					if channel:
						ctx = channel
				elif line.startswith("$blackListServers["):
					if str(need[0].guild.id) in line[len("$blackListServers["):].split(";")[:-1]:
						raise TypeError(line[len("$blackListServers["):].split(";")[-1])
				elif line.startswith("$blackListUsers["):
					if str(need[0].author.name) in line[len("$blackListUsers["):].split(";")[:-1]:
						raise TypeError(line[len("$blackListUsers["):].split(";")[-1])
				elif line.startswith("$blackListRoles["):
					for role in line[len("$blackListRoles["):].split(";")[:-1]:
						if discord.utils.get(need[0].author.roles, name=role):
							raise TypeError(line[len("$blackListRoles["):].split(";")[-1])
				elif line.startswith("$blackListRolesIDs["):
					for role in line[len("$blackListRolesIDs["):].split(";")[:-1]:
						if discord.utils.get(need[0].author.roles, id=int(role)):
							raise TypeError(line[len("$blackListRolesIDs["):].split(";")[-1])
				elif line.startswith("$channelSendMessage["):
					msg=await discord.utils.get(info._client.get_all_channels(), id = int(line[len("$channelSendMessage["):].split(";")[0])).send(line[len("$channelSendMessage["):].split(";")[1])
				elif line.startswith("$onlyIf["):
					t=True
					ret=line[len("$onlyIf["):][:len(line[len("$onlyIf["):])-len(";"+line[len("$onlyIf["):].split(";")[-1])]
					if "==" in ret:
						t=ret.split("==")
						if t[0]==t[1]:
							t=True
						else:
							t=False
					elif "!=" in ret:
						t=ret.split("!=")
						if t[0]!=t[1]:
							t=True
						else:
							t=False
					elif ">=" in ret:
						t=ret.split(">=")
						if int(t[0])>=int(t[1]):
							t=True
						else:
							t=False
					elif "<=" in ret:
						t=ret.split("<=")
						if int(t[0])<=int(t[1]):
							t=True
						else:
							t=False
					elif ">" in ret:
						t=ret.split(">")
						if int(t[0])>int(t[1]):
							t=True
						else:
							t=False
					elif "<" in ret:
						t=ret.split("<")
						if int(t[0])<int(t[1]):
							t=True
						else:
							t=False
					if t==False:
						raise TypeError(line[len("$onlyIf["):].split(";")[-1])
				elif line.startswith("$if["):
					t=True
					ret=line[len("$if["):]
					if "==" in ret:
						t=ret.split("==")
						if t[0]==t[1]:
							t=True
						else:
							t=False
					elif "!=" in ret:
						t=ret.split("!=")
						if t[0]!=t[1]:
							t=True
						else:
							t=False
					elif ">=" in ret:
						t=ret.split(">=")
						if int(t[0])>=int(t[1]):
							t=True
						else:
							t=False
					elif "<=" in ret:
						t=ret.split("<=")
						if int(t[0])<=int(t[1]):
							t=True
						else:
							t=False
					elif ">" in ret:
						t=ret.split(">")
						if int(t[0])>int(t[1]):
							t=True
						else:
							t=False
					elif "<" in ret:
						t=ret.split("<")
						if int(t[0])<int(t[1]):
							t=True
						else:
							t=False
					if t==False:
						go=True
				elif line.startswith("$botLeave["):
					await discord.utils.get(client.guilds, id=int(line[len("$botLeave["):])).leave()
				elif line.startswith("$dm["):
					if discord.utils.get(info._client.get_all_members(), id=int(line[len("$dm["):])):
						ctx=discord.utils.get(info._client.get_all_members(), id=int(line[len("$dm["):]))
				elif line.startswith("$ban["):
					if discord.utils.get(info._client.get_all_members(), id=int(line[len("$ban["):])):
						try:
							await discord.utils.get(info._client.get_all_members(), id=int(line[len("$ban["):].split(";")[0])).ban(reason=line[len("$ban["):].split(";")[1])
						except:
							await discord.utils.get(info._client.get_all_members(), id=int(line[len("$ban["):].split(";")[0])).ban(reason="")
				elif line.startswith("$kick["):
					if discord.utils.get(info._client.get_all_members(), id=int(line[len("$kick["):])):
						try:
							await discord.utils.get(info._client.get_all_members(), id=int(line[len("$kick["):].split(";")[0])).kick(reason=line[len("$kick["):].split(";")[1])
						except:
							await discord.utils.get(info._client.get_all_members(), id=int(line[len("$kick["):].split(";")[0])).kick(reason="")
				elif line.startswith("$unban["):
					banned_users = await need[0].guild.bans()
					for ban_entry in banned_users:
						user = ban_entry.user
						if user.id==int(line[len("$unban["):]):
							await user.unban(user)
				elif line.startswith("$setVar["):
					n=line[len("$setVar["):].split(";")
					if 0 <= 2 < len(n):
						info._db.set([n[0],n[1]],"globals",where=["id",n[2]])
					else:
						info._db._values[n[0]]=n[1]
				elif line.startswith("$setServerVar["):
					n=line[len("$setServerVar["):].split(";")
					if 0 <= 2 < len(n):
						info._db.set([n[0],n[1]],"servers",where=["id",n[2]])
					else:
						info._db.set([n[0],n[1]],"servers",where=["id",str(need[0].guild.id)])
				elif line.startswith("$setChannelVar["):
					n=line[len("$setChannelVar["):].split(";")
					if 0 <= 2 < len(n):
						info._db.set([n[0],n[1]],"channels",where=["id",n[2]])
					else:
						info._db.set([n[0],n[1]],"channels",where=["id",str(need[0].channel.id)])
				elif line.startswith("$setUserVar["):
					n=line[len("$setUserVar["):].split(";")
					if 0 <= 3 < len(n):
						info._db.set([n[0],n[1]],"server"+str(n[3]),where=["id",n[2]])
					elif 0 <= 2 < len(n):
						info._db.set([n[0],n[1]],"server"+str(need[0].guild.id),where=["id",n[2]])
					else:
						info._db.set([n[0],n[1]],"server"+str(need[0].guild.id),where=["id",str(need[0].author.id)])
				elif line.startswith("$onlyForServers["):
					if not str(need[0].guild.id) in line[len("$onlyForServers["):].split(";")[:-1]:
						raise TypeError(line[len("$onlyForServers["):].split(";")[-1])
				elif line.startswith("$onlyForUsers["):
					if not str(need[0].author.name) in line[len("$onlyForUsers["):].split(";")[:-1]:
						raise TypeError(line[len("$onlyForUsers["):].split(";")[-1])
				elif line.startswith("$onlyForRoles["):
					for role in line[len("$onlyForRoles["):].split(";")[:-1]:
						if not discord.utils.get(need[0].author.roles, name=role):
							raise TypeError(line[len("$onlyForRoles["):].split(";")[-1])
				elif line.startswith("$onlyForIDs["):
					if not str(need[0].author.id) in line[len("$onlyForIDs["):].split(";")[:-1]:
						raise TypeError(line[len("$onlyForIDs["):].split(";")[-1])
				elif line.startswith("$onlyForChannels["):
					if not str(need[0].channel.id) in line[len("$onlyForChannels["):].split(";")[:-1]:
						raise TypeError(line[len("$onlyForChannels["):].split(";")[-1])
				elif line.startswith("$onlyIfMessageContains["):
					for word in line[len("$onlyIfMessageContains["):].split(";")[:-1]:
						if not word in content:
							raise TypeError(line[len("$onlyIfMessageContains["):].split(";")[-1])
				elif line.startswith("$onlyNSFW["):
					if not need[0].channel.is_nsfw():
						raise TypeError(line[len("$onlyNSFW["):])
				elif line.startswith("$pyEval["):
					from discord.ext import commands
					def insert_returns(body):
						if isinstance(body[-1], ast.Expr):
							body[-1] = ast.Return(body[-1].value)
							ast.fix_missing_locations(body[-1])
						if isinstance(body[-1], ast.If):
							insert_returns(body[-1].body)
							insert_returns(body[-1].orelse)
						if isinstance(body[-1], ast.With):
							insert_returns(body[-1].body)
						return body
					fn_name = "_eval_expr"
					n=line[len("$pyEval["):]
					d=""
					for t in n.split("\n"):
						d+="\n	"+t
					body = f"async def {fn_name}():{d}"
					parsed = ast.parse(body)
					body = parsed.body[0].body
					body = insert_returns(body)
					env = { "message":need[0], "client":info._client, "discord":discord, "commands":commands, "ctx": ctx, "__import__": __import__ }
					exec(compile(parsed, filename="<ast>", mode="exec"), env)
					result = str((await eval(f"{fn_name}()", env)))
					if line[len("$pyEval["):].split(";")[-1]=="yes":
						binstr += result
				elif line.startswith("$reactionCollector["):
					vote_msg = await ctx.send(line[len("$reactionCollector["):].split(";")[0])
					rs = []
					for r in line[len("$reactionCollector["):].split(";")[2:]:
						await vote_msg.add_reaction(r)
						rs.append(r)
					await asyncio.sleep(int(line[len("$reactionCollector["):].split(";")[1]))
					vote_msg = await vote_msg.channel.fetch_message(vote_msg.id)
					for r in rs:
						for n in vote_msg.reactions:
							if n.emoji==r:
								collector[r] = n.count - 1
				elif line.startswith("$reactionPage["):
					e = line[len("$reactionPage["):].split(";")
					eemb = discord.Embed(title=e[0], description=e[1])
					if e[2]!="":
						rgb=list(int(e[2][i:i+2], 16) for i in (0, 2, 4))
						eemb.color=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2])
					if e[3]!="":
						eemb.set_author(name=e[3])
					if e[4]!="":
						eemb.set_footer(text=e[4], icon_url=e[5])
					pages.append(eemb)
				elif line.startswith("$reactionPages["):
					userid = str(need[0].author.id)
					line=line[len("$reactionPages["):].split(";")
					previuspage = line[0]
					nextpage = line[1]
					page = 0
					zeropage=pages[0]
					mesg = await ctx.send(embed=zeropage)
					await mesg.add_reaction(previuspage)
					await mesg.add_reaction(nextpage)
					def checkforreaction(reaction, user):
						return str(user.id) == userid and str(reaction.emoji) in [previuspage,nextpage] and reaction.message.id==mesg.id
					loopclose = 0
					while loopclose == 0:
						try:
							reaction, user = await info._client.wait_for('reaction_add', timeout=8,check = checkforreaction)
							if reaction.emoji == nextpage:
								if page+1<=len(pages)-1:
									page=page+1
								r=nextpage
							elif reaction.emoji == previuspage:
								if page-1>=0:
									page-=1
								r=previuspage
							nowpage=pages[page]
							await mesg.remove_reaction(r,need[0].author)
							await mesg.edit(embed=nowpage)
						except asyncio.TimeoutError:
							try:
								await mesg.remove_reaction(previuspage,client.user)
							except:
								pass
							try:
								await mesg.remove_reaction(nextpage,client.user)
							except:
								pass
							loopclose = 1
				elif line.startswith("$print["):
					print(line[len("$print["):])
				elif line.startswith("$editIn["):
					line=line[len("$editIn["):]
					s=line.split(";")[0]
					line=line[len(s+";"):]
					if s.endswith("s"):
						s=s.rstrip("s")
					elif s.endswith("m"):
						s=s.rstrip("m")
						s=int(s)*60
					elif s.endswith("h"):
						s=s.rstrip("h")
						s=int(s)*60*60
					elif s.endswith("d"):
						s=s.rstrip("d")
						s=int(s)*60*60*24
					edits.append(["str", s, line])
				elif line.startswith("$editEmbedIn["):
					line=line[len("$editEmbedIn["):]
					s=line.split(";")[0]
					line=line[len(s+";"):].split(";")
					eemb = discord.Embed(title=line[0], description=line[1])
					if line[2]!="":
						rgb=list(int(line[2][i:i+2], 16) for i in (0, 2, 4))
						eemb.color=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2])
					if line[3]!="":
						eemb.set_author(name=line[3])
					if line[4]!="":
						if line[5]!="": 
							eemb.set_footer(text=line[4], icon_url=line[5])
						else:
							eemb.set_footer(text=line[4])
					if s.endswith("s"):
						s=s.rstrip("s")
					elif s.endswith("m"):
						s=s.rstrip("m")
						s=int(s)*60
					elif s.endswith("h"):
						s=s.rstrip("h")
						s=int(s)*60*60
					elif s.endswith("d"):
						s=s.rstrip("d")
						s=int(s)*60*60*24
					edits.append(["emb", s, eemb])
				elif line.startswith("$status["):
					line=line[len("$status["):].split(";")
					act=None
					if len(line)>2:
						if line[1]=="play":
							act=discord.Activity(type=discord.ActivityType.playing,name=line[2])
						elif line[1]=="watch":
							act=discord.Activity(type=discord.ActivityType.watching,name=line[2])
						elif line[1]=="listen":
							act=discord.Activity(type=discord.ActivityType.listening,name=line[2])
						elif line[1]=="stream":
							act=discord.Activity(type=discord.ActivityType.streaming,name=line[2])
					if line[0]=="online":
						await info._client.change_presence(activity=act, status=discord.Status.online)
					elif line[0]=="idle":
						await info._client.change_presence(activity=act, status=discord.Status.idle)
					elif line[0]=="dnd":
						await info._client.change_presence(activity=act, status=discord.Status.dnd)
					elif line[0]=="offline":
						await info._client.change_presence(status=discord.Status.invisible)
				elif line.startswith("$cooldown["):
					line=line[len("$cooldown["):]
					n=line[len(line.split(";")[0]+";"):]
					line=line.split(";")[0]
					if not need[1] in info._cooldown:
						info._cooldown[need[1]]={"user":{},"server":{}, "global":0}
					if not str(need[0].author.id) in info._cooldown[need[1]]["user"]:
						info._cooldown[need[1]]["user"][str(need[0].author.id)]=0
					if not str(need[0].guild.id) in info._cooldown[need[1]]["server"]:
						info._cooldown[need[1]]["server"][str(need[0].guild.id)]=0
					try:
						if info._cooldown[need[1]]["user"][str(need[0].author.id)]-int(time.time() - _startTime)<0:
							timerep="0"
						else:
							timerep=str(info._cooldown[need[1]]["user"][str(need[0].author.id)]-int(time.time() - _startTime))
					except Exception as e:
						timerep="0"
					if info._cooldown[need[1]]["user"][str(need[0].author.id)]>int(time.time() - _startTime):
						dt=str(timedelta(seconds=round(int(timerep)))).split(":")
						raise TypeError(n.replace("$second", str(dt[2])).replace("$minute", str(dt[1])).replace("$hour", str(dt[0])))
					else:
						if line.endswith("s"):
							line=line.rstrip("s")
						elif line.endswith("m"):
							line=line.rstrip("m")
							line=int(line)*60
						elif line.endswith("h"):
							line=line.rstrip("h")
							line=int(line)*60*60
						elif line.endswith("d"):
							line=line.rstrip("d")
							line=int(line)*60*60*24
						info._cooldown[need[1]]["user"][str(need[0].author.id)]=int(time.time() - _startTime)+int(line)
				elif line.startswith("$setLocalVar["):
					n=line[len("$setLocalVar["):].split(";")
					vars[n[0]]=n[1]
				elif line.startswith("$end"):
					if emb[0]:
						if str(ment+binstr).replace(" ","")!="":
							msg = await ctx.send(content=ment+binstr,embed=emb[1])
						else:
							msg = await ctx.send(embed=emb[1])
					else:
						if str(ment+binstr).replace(" ","")!="":
							msg = await ctx.send(ment+binstr)
					for react in reactions:
						try:
							await msg.add_reaction(react)
						except Exception as e:
							pass
					for edit in edits:
						await asyncio.sleep(int(edit[1]))
						if isinstance(msg, str):
							if edit[0]=="str":
								await ctx.send(edit[2])
							elif edit[0]=="emb":
								await ctx.send(embed=edit[2])
						else:
							if edit[0]=="str":
								await msg.edit(content=edit[2])
							elif edit[0]=="emb":
								await msg.edit(embed=edit[2])
					emb = [False, discord.Embed()]
					binstr = ""
					edits=[]
					reactions = []
				elif line.startswith("$getReactions["):
					line=line[len("$getReactions["):].split(";")
					r={}
					if line[2].endswith("s"):
						line[2]=line[2].rstrip("s")
					elif line.endswith("m"):
						line[2]=line[2].rstrip("m")
						line[2]=int(line[2])*60
					elif line[2].endswith("h"):
						line[2]=line[2].rstrip("h")
						line[2]=int(line[2])*60*60
					elif line[2].endswith("d"):
						line[2]=line[2].rstrip("d")
						line[2]=int(line[2])*60*60*24
					m=await ctx.fetch_message(int(line[1]))
					for rec in line[4:]:
						await m.add_reaction(rec.split("|")[0])
						r[rec.split("|")[0]]=rec.split("|")[1]
					def checkforreaction(reaction, user):
						if line[0]=="everyone":
							return str(user.id) != str(info._client.user.id) and str(reaction.emoji) in r and reaction.message.id==m.id
						else:
							return str(user.id) == line[0] and str(reaction.emoji) in r and reaction.message.id==m.id
					t=0
					while t<int(line[3]):
						t+=1
						try:
							reaction, user = await info._client.wait_for("reaction_add", timeout=int(line[2]), check = checkforreaction)
							n=need[0]
							n.author=user
							await use([n, r[str(reaction.emoji)], "wait", content, str(reaction.emoji)],info)
						except asyncio.TimeoutError:
							pass
				else:
					if binstr == "":
						binstr += reline
					else:
						binstr += "\n"+reline
			except Exception as e:
				if error[0]==True:
					print(f"❌Ошибка: `{e}`\nСтрока: {linec}\nЛиния: "+reline.replace("/n","\n"))
				else:
					if error[0]=="Embed":
						line = error[1].replace("%error%",str(e)).replace("%line%",str(linec)).replace("%text%",str(reline)).split(";")
						erremb = discord.Embed(title=line[0], description=line[1])
						if line[2]!="":
							rgb=list(int(line[2][i:i+2], 16) for i in (0, 2, 4))
							erremb.color=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2])
						if line[3]!="":
							erremb.set_author(name=line[3])
						if line[4]!="":
							erremb.set_footer(text=line[4], icon_url=line[5])
						await ctx.send(embed=erremb)
					else:
						if error[1]!="":
							await ctx.send(error[1].replace("%error%",str(e)).replace("%line%",str(linec)).replace("%text%",str(reline)))
				br=False
				break
		else:
			reline = await replaces([reline, info, content.replace("[","⦍").replace("]","⦎"), need, split, allow, collector, vars, emoji, msg])
			if binstr == "":
				binstr += reline
			else:
				binstr += "\n"+reline
	binstr=binstr.replace("/n","\n")
	if br:
		if emb[0]:
			if str(ment+binstr).replace(" ","")!="":
				msg = await ctx.send(content=ment+binstr,embed=emb[1])
			else:
				msg = await ctx.send(embed=emb[1])
		else:
			if str(ment+binstr).replace(" ","")!="":
				msg = await ctx.send(ment+binstr)
		for react in reactions:
			try:
				await msg.add_reaction(react)
			except Exception as e:
				pass
		for edit in edits:
			await asyncio.sleep(int(edit[1]))
			if isinstance(msg, str):
				if edit[0]=="str":
					await ctx.send(edit[2])
				elif edit[0]=="emb":
					await ctx.send(embed=edit[2])
			else:
				if edit[0]=="str":
					await msg.edit(content=edit[2])
				elif edit[0]=="emb":
					await msg.edit(embed=edit[2])

async def replaces(info):
	import re
	import time
	import discord
	import requests
	import random
	global _startTime
	reline = info[0]
	content = info[2]
	need = info[3]
	resplit = info[4]
	allow = info[5]
	collector = info[6]
	vars = info[7]
	emoji = info[8]
	msg=info[9]
	info = info[1]
	nowloop = ""
	members = 0
	content = re.sub("\s\s+", " ", content)
	def in_replaces(info):
		global _startTime
		reline = info[0]
		need = info[1]
		members = info[2]
		content = info[3]
		split = info[5]
		allow = info[6]
		collector = info[7]
		emojj = info[8]
		msg=info[9]
		info = info[4]
		recontent=content
		if need[0]!="none":
			reline = reline.replace("$authorID",str(need[0].author.id))
			reline = reline.replace("$authorAvatar",str(need[0].author.avatar_url))
			reline = reline.replace("$serverIcon",str(need[0].guild.icon_url))
			reline = reline.replace("$randomMention",str(random.choice(list(need[0].guild.members)).mention))
			reline = reline.replace("$randomUserID",str(random.choice(list(need[0].guild.members)).id))
			reline = reline.replace("$randomUser",str(random.choice(list(need[0].guild.members)).display_name))
			for m in need[0].mentions:
				recontent=recontent.replace(str(m.mention).replace("!",""),"")
				if allow:
					content=content.replace(str(m.mention).replace("!",""), str(m.display_name))
		if not isinstance(msg, str):
			reline = reline.replace("$messageID",str(msg.id))
		reline = reline.replace("$emoji",str(emoji))
		reline = reline.replace("$getBotInvite",f"https://discord.com/api/oauth2/authorize?client_id={info._client.user.id}&permissions=8&scope=bot")
		reline = reline.replace("$serverCount",str(len(info._client.guilds)))
		reline = reline.replace("$ping",str(round(info._client.latency*1000)))
		reline = reline.replace("$uptime",str(round(time.time()-_startTime)))
		reline = reline.replace("$botID",str(info._client.user.id))
		reline = reline.replace("$allMembersCount",str(members))
		reline = reline.replace("$getTextSplitLength",str(len(split)))
		reline = reline.replace("$commandsCount",str(len(info._codes["commands"])))
		for guild in info._client.guilds:
			members += len(guild.members)
		recontent=recontent.lstrip(" ")
		content=content.lstrip(" ")
		nowloop=""
		while "$collector[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					reline=reline.replace("$collector["+reline.split("$collector[")[-1].split("]")[0]+"]", str(collector[reline.split("$collector[")[-1].split("]")[0]]))
				except Exception as e:
					reline=reline.replace("$collector["+reline.split("$collector[")[-1].split("]")[0]+"]", "none")
		while "$guildID[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					guild = discord.utils.get(info._client.guilds, name = reline.split("$guildID[")[-1].split("]")[0])
					reline=reline.replace("$guildID["+reline.split("$guildID[")[-1].split("]")[0]+"]", str(guild.id))
				except Exception as e:
					reline=reline.replace("$guildID["+reline.split("$guildID[")[-1].split("]")[0]+"]", "none")
		if need[0]!="none":
			reline = reline.replace("$guildID",str(need[0].guild.id))
		while "$channelID[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					channel = discord.utils.get(info._client.get_all_channels(), name = reline.split("$channelID[")[-1].split("]")[0])
					reline=reline.replace("$channelID["+reline.split("$channelID[")[-1].split("]")[0]+"]", str(channel.id))
				except Exception as e:
					reline=reline.replace("$channelID["+reline.split("$channelID[")[-1].split("]")[0]+"]", "none")
		if need[0]!="none":
			reline = reline.replace("$channelID",str(need[0].channel.id))
		
		while "$mentionedChannels[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					reline=reline.replace("$mentionedChannels["+reline.split("$mentionedChannels[")[-1].split("]")[0]+"]", str(need[0].channel_mentions[int(reline.split("$mentionedChannels[")[-1].split("]")[0].split(";")[0])-1].id))
				except Exception as e:
					try:
						if reline.split("$mentionedChannels[")[-1].split("]")[0].split(";")[1]=="yes":
							reline=reline.replace("$mentionedChannels["+reline.split("$mentionedChannels[")[-1].split("]")[0]+"]", str(need[0].channel.id))
						else:
							reline=reline.replace("$mentionedChannels["+reline.split("$mentionedChannels[")[-1].split("]")[0]+"]", "")
					except Exception as e:
						reline=reline.replace("$mentionedChannels["+reline.split("$mentionedChannels[")[-1].split("]")[0]+"]", "")
		while "$channelName[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					channel = discord.utils.get(info._client.get_all_channels(), id = int(reline.split("$channelName[")[-1].split("]")[0]))
					reline=reline.replace("$channelName["+reline.split("$channelName[")[-1].split("]")[0]+"]", str(channel.name))
				except Exception as e:
					reline=reline.replace("$channelName["+reline.split("$channelName[")[-1].split("]")[0]+"]", "none")
		while "$mentionedRoles[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					reline=reline.replace("$mentionedRoles["+reline.split("$mentionedRoles[")[-1].split("]")[0]+"]", str(need[0].role_mentions[int(reline.split("$mentionedRoles[")[-1].split("]")[0].split(";")[0])-1].id))
				except Exception as e:
					reline=reline.replace("$mentionedRoles["+reline.split("$mentionedRoles[")[-1].split("]")[0]+"]", "")
		while "$message[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					reline=reline.replace("$message["+reline.split("$message[")[-1].split("]")[0]+"]", content.split(" ")[int(reline.split("$message[")[-1].split("]")[0])-1])
				except Exception as e:
					reline=reline.replace("$message["+reline.split("$message[")[-1].split("]")[0]+"]", "")
		reline = reline.replace("$message",content)
		while "$noMentionMessage[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					reline=reline.replace("$noMentionMessage["+reline.split("$noMentionMessage[")[-1].split("]")[0]+"]", recontent.split(" ")[int(reline.split("$noMentionMessage[")[-1].split("]")[0])-1])
				except Exception as e:
					reline=reline.replace("$noMentionMessage["+reline.split("$noMentionMessage[")[-1].split("]")[0]+"]", "")
		reline = reline.replace("$noMentionMessage",recontent)
		while "$mentioned[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					reline=reline.replace("$mentioned["+reline.split("$mentioned[")[-1].split("]")[0]+"]", str(need[0].mentions[int(reline.split("$mentioned[")[-1].split("]")[0].split(";")[0])-1].id))
				except Exception as e:
					try:
						if reline.split("$mentioned[")[-1].split("]")[0].split(";")[1]=="yes":
							reline=reline.replace("$mentioned["+reline.split("$mentioned[")[-1].split("]")[0]+"]", str(need[0].author.id))
						else:
							reline=reline.replace("$mentioned["+reline.split("$mentioned[")[-1].split("]")[0]+"]", "")
					except Exception as e:
						reline=reline.replace("$mentioned["+reline.split("$mentioned[")[-1].split("]")[0]+"]", "")
		while "$username[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					user = discord.utils.get(info._client.get_all_members(), id = int(reline.split("$username[")[-1].split("]")[0]))
					reline=reline.replace("$username["+reline.split("$username[")[-1].split("]")[0]+"]", str(user.name))
				except Exception as e:
					reline=reline.replace("$username["+reline.split("$username[")[-1].split("]")[0]+"]", "none")
		if need[0]!="none":
			reline = reline.replace("$username",str(need[0].author.name))
		while "$nickname[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					user = discord.utils.get(info._client.get_all_members(), id = int(reline.split("$nickname[")[-1].split("]")[0]))
					reline=reline.replace("$nickname["+reline.split("$nickname[")[-1].split("]")[0]+"]", str(user.display_name))
				except Exception as e:
					reline=reline.replace("$nickname["+reline.split("$nickname[")[-1].split("]")[0]+"]", "none")
		if need[0]!="none":
			reline = reline.replace("$nickname",str(need[0].author.display_name))
		while "$tag[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					user = discord.utils.get(info._client.get_all_members(), id = int(reline.split("$tag[")[-1].split("]")[0]))
					reline=reline.replace("$tag["+reline.split("$tag[")[-1].split("]")[0]+"]", str(user.discriminator))
				except Exception as e:
					reline=reline.replace("$tag["+reline.split("$tag[")[-1].split("]")[0]+"]", "none")
		if need[0]!="none":
			reline = reline.replace("$tag",str(need[0].author.discriminator))
		while "$randomText[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					nums=reline.split("$randomText[")[-1].split("]")[0].split(";")
					reline=reline.replace("$randomText["+reline.split("$randomText[")[-1].split("]")[0]+"]", str(random.choice(nums)))
				except Exception as e:
					reline=reline.replace("$randomText["+reline.split("$randomText[")[-1].split("]")[0]+"]", "none")
		while "$random[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					nums=reline.split("$random[")[-1].split("]")[0].replace("?",str(random.randint(1,9))).split(";")
					if int(nums[0])>int(nums[1]):
						nums=nums[::-1]
					reline=reline.replace("$random["+reline.split("$random[")[-1].split("]")[0]+"]", str(random.randint(int(nums[0]), int(nums[1]))))
				except Exception as e:
					reline=reline.replace("$random["+reline.split("$random[")[-1].split("]")[0]+"]", "nan")
		reline = reline.replace("$random",str(random.randint(0,9)))
		return reline
	reline=in_replaces([reline, need, members, content, info, resplit, allow, collector, emoji, msg])
	while "$splitText[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				reline=reline.replace("$splitText["+reline.split("$splitText[")[-1].split("]")[0]+"]", str(resplit[int(reline.split("$splitText[")[-1].split("]")[0])-1]))
			except Exception as e:
				reline=reline.replace("$splitText["+reline.split("$splitText[")[-1].split("]")[0]+"]", "")
	while "$joinSplitText[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				reline=reline.replace("$joinSplitText["+reline.split("$joinSplitText[")[-1].split("]")[0]+"]", reline.split("$joinSplitText[")[-1].split("]")[0].join(resplit))
			except Exception as e:
				reline=reline.replace("$joinSplitText["+reline.split("$joinSplitText[")[-1].split("]")[0]+"]", "")
	while "$argCount[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			if reline.split("$argCount[")[-1].split("]")[0].split(" ")[0]!="":
				reline=reline.replace("$argCount["+reline.split("$argCount[")[-1].split("]")[0]+"]", str(len(reline.split("$argCount[")[-1].split("]")[0].split(" "))))
			else:
				reline=reline.replace("$argCount["+reline.split("$argCount[")[-1].split("]")[0]+"]", "0")
	while "$isAdmin[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				user = discord.utils.get(info._client.get_all_members(), id=int(reline.split("$isAdmin[")[-1].split("]")[0]))
				if user.guild_permissions.administrator:
					reline=reline.replace("$isAdmin["+reline.split("$isAdmin[")[-1].split("]")[0]+"]", "true")
				else:
					reline=reline.replace("$isAdmin["+reline.split("$isAdmin[")[-1].split("]")[0]+"]", "false")
			except Exception as e:
				reline=reline.replace("$isAdmin["+reline.split("$isAdmin[")[-1].split("]")[0]+"]", "none")
	while "$isBot[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				user = discord.utils.get(info._client.get_all_members(), id=int(reline.split("$isBot[")[-1].split("]")[0]))
				if user.bot:
					reline=reline.replace("$isBot["+reline.split("$isBot[")[-1].split("]")[0]+"]", "true")
				else:
					reline=reline.replace("$isBot["+reline.split("$isBot[")[-1].split("]")[0]+"]", "false")
			except Exception as e:
				reline=reline.replace("$isBot["+reline.split("$isBot[")[-1].split("]")[0]+"]", "none")
	while "$userAvatar[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				user = discord.utils.get(info._client.get_all_members(), id=int(reline.split("$userAvatar[")[-1].split("]")[0]))
				reline=reline.replace("$userAvatar["+reline.split("$userAvatar[")[-1].split("]")[0]+"]", str(user.avatar_url))
			except Exception as e:
				reline=reline.replace("$userAvatar["+reline.split("$userAvatar[")[-1].split("]")[0]+"]", "none")
	while "$authorOfMessage[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				channel = discord.utils.get(info._client.get_all_channels(), id = int(reline.split("$authorOfMessage[")[-1].split("]")[0].split(";")[0]))
				message = await channel.fetch_message(int(reline.split("$authorOfMessage[")[-1].split("]")[0].split(";")[1]))
				reline=reline.replace("$authorOfMessage["+reline.split("$authorOfMessage[")[-1].split("]")[0]+"]", str(message.author.id))
			except Exception as e:
				reline=reline.replace("$authorOfMessage["+reline.split("$authorOfMessage[")[-1].split("]")[0]+"]", "none")
	while "$isNumber[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				int(reline.split("$isNumber[")[-1].split("]")[0])
				reline=reline.replace("$isNumber["+reline.split("$isNumber[")[-1].split("]")[0]+"]", "true")
			except Exception as e:
				reline=reline.replace("$isNumber["+reline.split("$isNumber[")[-1].split("]")[0]+"]", "false")
	while "$toLowercase[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				reline=reline.replace("$toLowercase["+reline.split("$toLowercase[")[-1].split("]")[0]+"]", reline.split("$toLowercase[")[-1].split("]")[0].lower())
			except Exception as e:
				reline=reline.replace("$toLowercase["+reline.split("$toLowercase[")[-1].split("]")[0]+"]", reline.split("$toLowercase[")[-1].split("]")[0])
	while "$toUppercase[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				reline=reline.replace("$toUppercase["+reline.split("$toUppercase[")[-1].split("]")[0]+"]", reline.split("$toUppercase[")[-1].split("]")[0].upper())
			except Exception as e:
				reline=reline.replace("$toUppercase["+reline.split("$toUppercase[")[-1].split("]")[0]+"]", reline.split("$toUppercase[")[-1].split("]")[0])
	while "$getVar[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			if 0 <= 1 < len(reline.split("$getVar[")[-1].split("]")[0].split(";")):
				try:
					reline=reline.replace("$getVar["+reline.split("$getVar[")[-1].split("]")[0]+"]",str(info._db.get(reline.split("$getVar[")[-1].split("]")[0].split(";")[0],"globals",["id",reline.split("$getVar[")[-1].split("]")[0].split(";")[1]])))
				except Exception as e:
					reline=reline.replace("$getVar["+reline.split("$getVar[")[-1].split("]")[0]+"]","none")
			else:
				try:
					reline=reline.replace("$getVar["+reline.split("$getVar[")[-1].split("]")[0]+"]",str(info._db._values[reline.split("$getVar[")[-1].split("]")[0].split(";")[0]]))
				except:
					reline=reline.replace("$getVar["+reline.split("$getVar[")[-1].split("]")[0]+"]","none")
	while "$getLocalVar[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				reline=reline.replace("$getLocalVar["+reline.split("$getLocalVar[")[-1].split("]")[0]+"]",str(vars[reline.split("$getLocalVar[")[-1].split("]")[0].split(";")[0]]))
			except:
				reline=reline.replace("$getLocalVar["+reline.split("$getLocalVar[")[-1].split("]")[0]+"]","none")
	while "$getServerVar[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			if 0 <= 1 < len(reline.split("$getServerVar[")[-1].split("]")[0].split(";")):
				try:
					reline=reline.replace("$getServerVar["+reline.split("$getServerVar[")[-1].split("]")[0]+"]",str(info._db.get(reline.split("$getServerVar[")[-1].split("]")[0].split(";")[0],"servers",["id",reline.split("$getServerVar[")[-1].split("]")[0].split(";")[1]])))
				except Exception as e:
					reline=reline.replace("$getServerVar["+reline.split("$getServerVar[")[-1].split("]")[0]+"]","none")
			else:
				try:
					reline=reline.replace("$getServerVar["+reline.split("$getServerVar[")[-1].split("]")[0]+"]",str(info._db.get(reline.split("$getServerVar[")[-1].split("]")[0].split(";")[0],"servers",["id",str(need[0].guild.id)])))
				except:
					reline=reline.replace("$getServerVar["+reline.split("$getServerVar[")[-1].split("]")[0]+"]","none")
	while "$getChannelVar[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			if 0 <= 1 < len(reline.split("$getChannelVar[")[-1].split("]")[0].split(";")):
				try:
					reline=reline.replace("$getChannelVar["+reline.split("$getChannelVar[")[-1].split("]")[0]+"]",str(info._db.get(reline.split("$getChannelVar[")[-1].split("]")[0].split(";")[0],"channels",["id",reline.split("$getChannelVar[")[-1].split("]")[0].split(";")[1]])))
				except Exception as e:
					reline=reline.replace("$getChannelVar["+reline.split("$getChannelVar[")[-1].split("]")[0]+"]","none")
			else:
				try:
					reline=reline.replace("$getChannelVar["+reline.split("$getChannelVar[")[-1].split("]")[0]+"]",str(info._db.get(reline.split("$getServerVar[")[-1].split("]")[0].split(";")[0],"channels",["id",str(need[0].channel.id)])))
				except:
					reline=reline.replace("$getChannelVar["+reline.split("$getChannelVar[")[-1].split("]")[0]+"]","none")
	while "$getUserVar[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			if 0 <= 2 < len(reline.split("$getUserVar[")[-1].split("]")[0].split(";")):
				try:
					reline=reline.replace("$getUserVar["+reline.split("$getUserVar[")[-1].split("]")[0]+"]",str(info._db.get(reline.split("$getUserVar[")[-1].split("]")[0].split(";")[0],"server"+str(reline.split("$getUserVar[")[-1].split("]")[0].split(";")[2]),["id",reline.split("$getUserVar[")[-1].split("]")[0].split(";")[1]])))
				except Exception as e:
					reline=reline.replace("$getUserVar["+reline.split("$getUserVar[")[-1].split("]")[0]+"]","none")
			elif 0 <= 1 < len(reline.split("$getUserVar[")[-1].split("]")[0].split(";")):
				try:
					reline=reline.replace("$getUserVar["+reline.split("$getUserVar[")[-1].split("]")[0]+"]",str(info._db.get(reline.split("$getUserVar[")[-1].split("]")[0].split(";")[0],"server"+str(need[0].guild.id),["id",reline.split("$getUserVar[")[-1].split("]")[0].split(";")[1]])))
				except Exception as e:
					reline=reline.replace("$getUserVar["+reline.split("$getUserVar[")[-1].split("]")[0]+"]","none")
			else:
				try:
					reline=reline.replace("$getUserVar["+reline.split("$getUserVar[")[-1].split("]")[0]+"]",str(info._db.get(reline.split("$getUserVar[")[-1].split("]")[0].split(";")[0],"server"+str(need[0].guild.id),["id",str(need[0].author.id)])))
				except Exception as e:
					reline=reline.replace("$getUserVar["+reline.split("$getUserVar[")[-1].split("]")[0]+"]","none")
	while "$math[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				reline=reline.replace("$math["+reline.split("$math[")[-1].split("]")[0]+"]", str(eval(reline.split("$math[")[-1].split("]")[0],{'__builtins__':None})))
			except Exception as e:
				reline=reline.replace("$math["+reline.split("$math[")[-1].split("]")[0]+"]", "nan")
	while "$replaceText[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				if int(reline.split("$replaceText[")[-1].split("]")[0].split(";")[3])<=0:
					reline=reline.replace("$replaceText["+reline.split("$replaceText[")[-1].split("]")[0]+"]", reline.split("$replaceText[")[-1].split("]")[0].split(";")[0].replace(reline.split("$replaceText[")[-1].split("]")[0].split(";")[1], reline.split("$replaceText[")[-1].split("]")[0].split(";")[2]))
				else:
					s=list(reline.split("$replaceText[")[-1].split("]")[0].split(";")[0])
					i=0
					while reline.split("$replaceText[")[-1].split("]")[0].split(";")[1] in s:
						i+=1
						if i<=int(reline.split("$replaceText[")[-1].split("]")[0].split(";")[3]):
							find = s.index(reline.split("$replaceText[")[-1].split("]")[0].split(";")[1])
							s[find]=reline.split("$replaceText[")[-1].split("]")[0].split(";")[2]
						else:
							break
					reline=reline.replace("$replaceText["+reline.split("$replaceText[")[-1].split("]")[0]+"]", "".join(s))
			except Exception as e:
				raise e
	while "$leaderboard[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				if reline.split("$leaderboard[")[-1].split("]")[0].split(";")[0]=="server":
					try:
						top = info._db._cursor.execute(f"SELECT id, var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]} from servers ORDER BY var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]} + 0").fetchall()
					except:
						top = info._db._cursor.execute(f"SELECT id, var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]} from servers ORDER BY var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]}").fetchall()
				elif reline.split("$leaderboard[")[-1].split("]")[0].split(";")[0]=="global":
					try:
						top = info._db._cursor.execute(f"SELECT id, var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]} from globals ORDER BY var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]} + 0").fetchall()
					except:
						top = info._db._cursor.execute(f"SELECT id, var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]} from globals ORDER BY var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]}").fetchall()
				elif reline.split("$leaderboard[")[-1].split("]")[0].split(";")[0]=="channel":
					try:
						top = info._db._cursor.execute(f"SELECT id, var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]} from channels ORDER BY var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]} + 0").fetchall()
					except:
						top = info._db._cursor.execute(f"SELECT id, var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]} from channels ORDER BY var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]}").fetchall()
				else:
					try:
						top = info._db._cursor.execute(f"SELECT id, var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]} from server{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[0]} ORDER BY var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]} + 0").fetchall()
					except:
						top = info._db._cursor.execute(f"SELECT id, var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]} from server{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[0]} ORDER BY var{reline.split('$leaderboard[')[-1].split(']')[0].split(';')[1]}").fetchall()
				topos=0
				tops={}
				topstr=""
				for i, u in top:
					try:
						tops[str(i)]=int(u)
					except Exception as e:
						tops[str(i)]=u
				top=sorted(tops.items(), key=lambda x: x[1], reverse=True)
				for n, u in top:
					try:
						if topos<int(reline.split("$leaderboard[")[-1].split("]")[0].split(";")[2]) and int(reline.split("$leaderboard[")[-1].split("]")[0].split(";")[2])>=0:
							if reline.split("$leaderboard[")[-1].split("]")[0].split(";")[0]=="server":
								t = discord.utils.get(info._client.guilds, id=int(n))
							elif reline.split("$leaderboard[")[-1].split("]")[0].split(";")[0]=="global":
								t = discord.utils.get(info._client.get_all_members(), id=int(n))
							elif reline.split("$leaderboard[")[-1].split("]")[0].split(";")[0]=="channel":
								t = discord.utils.get(info._client.get_all_channels(), id=int(n))
							else:
								t = discord.utils.get(info._client.get_all_members(), id=int(n))
							if t:
								topos+=1
								try:
									topstr+=str(reline.split("$leaderboard[")[-1].split("]")[0].split(";")[3]).replace("%pos%",str(topos)).replace("%name%",str(t.name)).replace("%id%",str(t.id)).replace("%value%",str(u)).replace("%fullname%",str(t)).replace("%discriminator%",str(t.discriminator))+"\n"
								except:
									topstr+=str(topos)+". "+str(t)+" - "+str(u)+"\n"
						elif int(reline.split("$leaderboard[")[-1].split("]")[0].split(";")[2])==-1:
							if reline.split("$leaderboard[")[-1].split("]")[0].split(";")[0]=="server":
								t = discord.utils.get(info._client.guilds, id=int(n))
							elif reline.split("$leaderboard[")[-1].split("]")[0].split(";")[0]=="global":
								t = discord.utils.get(info._client.get_all_members(), id=int(n))
							elif reline.split("$leaderboard[")[-1].split("]")[0].split(";")[0]=="channel":
								t = discord.utils.get(info._client.get_all_channels(), id=int(n))
							else:
								t = discord.utils.get(info._client.get_all_members(), id=int(n))
							if t:
								topos+=1
								try:
									topstr+=str(reline.split("$leaderboard[")[-1].split("]")[0].split(";")[3]).replace("%pos%",str(topos)).replace("%name%",str(t.name)).replace("%id%",str(t.id)).replace("%value%",str(u)).replace("%fullname%",str(t)).replace("%discriminator%",str(t.discriminator))+"\n"
								except:
									topstr+=str(topos)+". "+str(t)+" - "+str(u)+"\n"
						else:
							break
					except Exception as e:
						pass
				while len(topstr)>2000:
					topstr="\n".join(topstr.split("\n")[:-2])
				reline=reline.replace("$leaderboard["+reline.split("$leaderboard[")[-1].split("]")[0]+"]", str(topstr))
			except Exception as e:
				reline=reline.replace("$leaderboard["+reline.split("$leaderboard[")[-1].split("]")[0]+"]", "none")
	while "$emoteUrl[" in reline:
		if nowloop==reline:
			break
		else:
			nowloop=reline
			try:
				reline=reline.replace("$emoteUrl["+reline.split("$emoteUrl[")[-1].split("]")[0]+"]", str(discord.utils.get(need[0].guild.emojis, id=int(reline.split("$emoteUrl[")[-1].split("]")[0])).url))
			except Exception as e:
				reline=reline.replace("$emoteUrl["+reline.split("$emoteUrl[")[-1].split("]")[0]+"]", "none")
	return reline