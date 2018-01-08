import random
import sys
import os
import math
import string
from decimal import *


#########################################################################################################################
############################################## S H I T ## D O N E #######################################################
#########################################################################################################################

### New ideas ###

# Read the entire document, make a list of rounds.
# put every element of the list(round) to tests
# update all dictionaries with



#########################################################################################################################
############################################## AUXILIARY ## FUNCTIONS ###################################################
#########################################################################################################################

#Returns a reversed list
def reverselist(list):
	iterator = len(list)-1
	index = 0
	dic = {}
	reversedlist = []
	for element in list:
		dic[index] = element
		index +=1
	for key in dic:
		reversedelement = dic.get(iterator)
		reversedlist.append(reversedelement)
		iterator -=1
	return reversedlist


#Returns an integer from a float
def intvalue(floatnum):
	intvalue = floatnum%1
	value = floatnum - intvalue
	value = int(value)
	return value


#########################################################################################################################
#################################### AUXILIARY ## IN-GAME ##FUNCTIONS ###################################################
#########################################################################################################################

#Returns list of roundevents
def findpreviousround(list):
	roundevents = []
	firstelement = True
	for element in list:
		if firstelement:
			firstelement = False
		else:
			roundevents.append(element)
			if "round_start" in element:
				return roundevents
	return roundevents

def findlastround(list):
	roundevents = []
	endofround = True
	for element in list:
		if endofround:
			if "round_start" in element:
				endofround = False
		else:
			roundevents.append(element)
			if "round_start" in element:
				return roundevents
	return roundevents


#Case where bomb doesn't decide who won the round
def eliminationdecider(list,team1,team2):
	team1members = 0
	team2members = 0
	for element in list:
		if "killed" in element:
			prekilled = element.strip().split("killed")
			if "with" in element:
				prekilled2 = prekilled[1].split("with")
				killed = prekilled2[0].strip()
			else:
				prekilled2 = prekilled[1].split("using")
				killed = prekilled2[0].strip()
			if killed in team1[1]:
				team1members +=1
			else:
				team2members +=1
		else:
			continue
	if team1members == 5:
		return True
	else:
		return False
	return True

#Algorithm to determine the round winner
def registerscore(templist,team1,team2):
	roundlist = []
	for element in templist:
		#print(element)
		pre_element = element.split("Tick: ")
		pre_element2 = pre_element[1].split(": ")
		new_element = pre_element2[1].strip()
		roundlist.append(new_element)
	
	kill = False
	for element in roundlist:
		if "killed" in element:
			kill = True
			break
		else:
			continue
	if not kill:
		return 0

	if "bomb_exploded" in roundlist:
		team2[0] +=1
		#print("\n1\n")
		return 0
	if "bomb_defused" in roundlist:
		team1[0] +=1
		#print("\n2\n")
		return 0
	if "bomb_planted" not in roundlist:
		if eliminationdecider(templist,team1,team2):
			team2[0] +=1
			#print("\n3\n")
			return 0
	
	if "bomb_planted" in roundlist:
		index = roundlist.index("round_end")
		index2 = roundlist.index("bomb_planted")
		#print("\n",index,index2,"\n")
		if index<index2:
			team1[0] +=1
			#print("\n4\n")
			return 0

	if "bomb_planted" in roundlist:
		if "bomb_defused" not in roundlist:
			team2[0] +=1
			#print("\n5\n")
			return 0
	#print("\n6\n")
	team1[0] +=1
	return 0

#Check for overtime
def existsovertime(list):
	counter = 0
	for element in list:
		if "round_start" in element:
			counter +=1 
	if counter >=4:
		return True
	return False

#Check clutch
def clutchcalculator(list,team1,team2):
	team1members = team1[1]
	team2members = team2[1]
	killedlist = []
	#print(list, "\n")
	clutcher = ""
	for element in list:
		if "killed" in element:
			prekilled = element.strip().split("killed")
			if "with" in element:
				prekilled2 = prekilled[1].split("with")
				killed = prekilled2[0].strip()
			else:
				prekilled2 = prekilled[1].split("using")
				killed = prekilled2[0].strip()
			killedlist.append(killed)
			if killed in team1[1]:
				team1members.remove(killed)
			if killed in team2[1]:
				team2members.remove(killed)
			elif len(team1members) == 1 and len(team2members)>1:
				clutcher = team1members[0]
			elif len(team2members) == 1 and len(team1members)>1:
				clutcher = team2members[0]
	if clutcher not in killedlist:
		#print(killedlist)
		#print(clutcher)
		return clutcher
	#print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
	return 0
#check for k's
def mostroundkills(list):
	killers = {}
	for element in list:
		if "killed" in element:
			prekiller = element.strip().split("killed")
			killer = prekiller[0].strip()
			if killer in killers:
				killers[killer] +=1
			else:
				killers[killer] = 1
	mostroundkill = max(killers, key=killers.get)
	return mostroundkill

#need a better algorithm
def mvpawardsingle(totalscores):
	mvpscores = {}
	for key in totalscores[0]:
		killnumber = totalscores[0].get(key)
		deaths = totalscores[1].get(key)
		entrykills = totalscores[3].get(key)
		mvpscores[key] = (killnumber - entrykills)*10 + entrykills*15 - deaths
	mvp = max(mvpscores, key = mvpscores.get)
	mvpscore = mvpscores.get(mvp)
	return mvp

def setwinner(team1,team2,team1tag,team2tag):
	mostrounds = max(team1[0],team2[0])
	#print(team1,team2)
	if mostrounds == team1[0]:
		winner = [team1tag]
		loser = [team2tag]
		winner.append(team1[1])
		loser.append(team2[1])
	else:
		winner = [team2tag]
		loser = [team1tag]
		winner.append(team2[1])
		loser.append(team1[1])
	#print(winner,loser)
	return [winner,loser]

def setteams(teams,team1tag,team2tag):
	team1 = [0]
	team2 = [0]
	for key in teams:
		if key == team1tag:
			team1.append(teams.get(key))
		if key == team2tag:
			team2.append(teams.get(key))
	return [team1,team2]

#########################################################################################################################
############################################## PRE-GAME ## FUNCTIONS ####################################################
#########################################################################################################################

#find the exact moment where the game starts aka Live on 3
def findlo3(list):
	live = 0
	if len(list)>=18:
		if "round_freeze_end" in list[-1]:
			templist = list[-18:]
			for element in templist:
				if "Event: round_start" in element:
					live +=1  
			if live >=3:
				return True
	return False

#parse the textfile to eliminate warmups at the beggining of the match and halftime
def gamestart(logfile):
	lock = 0
	listlo3 = []
	game = []
	for line in logfile:
		if lock == 1:
			game.append(line.strip())
		if findlo3(listlo3):
			lock=1
		if lock == 0:
			listlo3.append(line.strip())
		else:
			continue
	if len(game) == 0:
		return listlo3
	return game

#import teams and players
def getteams(filename):
	f = open(filename,'r')
	tag = True
	teamdic = {}
	counter = 0
	team = []
	for line in f:
		if tag:
			teamtag = line.strip()
			tag = False
			team = []
		else:
			if counter<5:
				team.append(line.strip())
				counter +=1
			else:
				tag = True
				teamdic[teamtag] = team
				counter = 0
	f.close()
	return teamdic

# Divide both halves
def sethalves(gamefile):
	count = 1
	lock = 0
	firsthalf = []
	secondhalf = []
	game = []
	for line in gamefile:
		if lock == 1:
			secondhalf.append(line.strip())
		elif lock == 0:
			if count<16:
				if "round_start" in line:
					firsthalf.append(line.strip())
					count +=1
				else:
					firsthalf.append(line.strip())
			else:
				lock = 1
		else:
			continue
	game.append(firsthalf)

	pistols = ["glock","usp_silencer","usp_silencer_not"]
	pistolcount = 0
	pistolround = []
	lock2 = 0
	roundcount = 0
	secondhalf2 = []
	overtime = []
	for line in secondhalf:
		newline = line.strip().split()
		if lock2 == 1:
			secondhalf2.append(line)
			if "round_start" in line:
				roundcount +=1
			continue
		if roundcount>14:
			overtime.append(line)
		if "bomb" in line and lock2 == 0:
			continue
		if "round" in line and lock2 == 0:
			continue
		if newline[-1] in pistols and lock2 == 0:
			pistolcount +=1
			pistolround.append(line)
			if pistolcount >= 5:
				lock2 = 1
				pistolround2 = pistolround[-5]
		else:
			if lock2 == 0:
				pistolcount = 0
				pistolround.clear()
	realsecondhalf = pistolround + secondhalf2
	game.append(realsecondhalf)
	stoppermessage = "Host_WriteConfiguration"
	overtimerounds = 0
	overtime2 = 0
	for line in overtime:
		if stoppermessage in overtime:
			break
		if "round_start" in line:
			overtimerounds +=1
		overtime2.append(line)

	if overtimerounds < 4:
		return game
	else:
		game.append(overtime2)

	return game

#splits halves of a game, also overtime
def splithalves(gamefile):
	count = 1
	lock = 0
	firsthalf = []
	presecondhalf = []
	secondhalf = []
	preovertime = []
	game = []
	for line in gamefile:
		if lock == 1:
			presecondhalf.append(line.strip())
		elif lock == 0:
			if count<16:
				if "round_start" in line:
					firsthalf.append(line.strip())
					count +=1
				else:
					firsthalf.append(line.strip())
			else:
				lock = 1
		else:
			continue
	game.append(firsthalf)

	#input funtion to determine second half, in this case, case of a live on 3, gamestart works
	lock = 0
	count = 1
	#list1 = gamestart(presecondhalf)
	for line in presecondhalf:
		if lock == 1:
			preovertime.append(line.strip())
		elif lock == 0:
			if count<16:
				if "round_start" in line:
					secondhalf.append(line.strip())
					count +=1
				else:
					secondhalf.append(line.strip())
			else:
				lock = 1
		else:
			continue
	game.append(secondhalf)

	lock = 0
	count = 1
	overtimelist = []
	overtime1 = []
	overtime2  = []
	if existsovertime(preovertime):
		list2 = gamestart(preovertime)
		for line in list2:
			if lock == 1:
				overtime1 = []
				overtime2 = []
				lock = 0
				count = 1
			elif lock == 0:
				if count <4:
					if "round_start" in line:
						overtime1.append(line)
						count +=1
					else:
						overtime1.append(line)
				if count>3 and count<7:
					if "round_start" in line:
						overtime2.append(line)
						count +=1
					else:
						overtime2.append(line)
				if count>6:
					overtimelist.append(overtime1)
					overtimelist.append(overtime2)

	game.append(overtimelist)
	return game



#########################################################################################################################
############################################### GAME ## FUNCTIONS #######################################################
#########################################################################################################################

#This is the main algorithm. It finds markers in the description of the demo and records every useful information
def buildscores(list,team1,team2):

	#initializing all dictionaries and variables
	killdict = {}
	deathdict = {}
	hsdict = {}
	awpkillsdict = {}
	entryfragdict = {}
	nround = 0
	listofdictionaries = []
	entryfragger = True
	firstround = True
	templist = []
	team1score = 0
	team2score = 0
	stoppermessage = "Host_WriteConfiguration"
	#start parsing the text
	for element in list:
		templist.append(element)
		if stoppermessage in element:
			break

		#check if there was an interaction ( kill ) and parse the killer
		if "killed" in element:
			list = element.split(':')
			event = list[-1].strip()
			namelist = event.split("killed")
			killer = namelist[0].strip()

			#check for a headshot and parse the killed		
			if "headshot" in event:
				namelist2 = namelist[1].split("with")
				killed = namelist2[0].strip()

				#Record headshot event
				if killer in hsdict:
					hsdict[killer] +=1
				else:
					hsdict[killer] = 1
			else:
				namelist2 = namelist[1].split("using")
				killed = namelist2[0].strip()

			#Record the information in the dictionaries
			if killer in killdict:
				killdict[killer] +=1
			else:
				killdict[killer] = 1
			if killed in deathdict:
				deathdict[killed] +=1
			else:
				deathdict[killed] = 1

			#Check if it was an entryfrag
			if entryfragger == True:
				if killer in entryfragdict:
					entryfragdict[killer] +=1
					entryfragger = False
				else:
					entryfragdict[killer] = 1
					entryfragger = False

			#Record all awp kills 
			newnamelist = namelist2[1].split(' ')
			weapon = newnamelist[-1].strip()
			if weapon == 'awp':
				if killer in awpkillsdict:
					awpkillsdict[killer] +=1
				else:
					awpkillsdict[killer] = 1

		#Count the round number, reset the entryfragger for the next round
		if "round_start" in element:
			nround +=1
			entryfragger = True
			previousround = findpreviousround(reverselist(templist))
			score = registerscore(reverselist(previousround),team1,team2)
			#clutchcalculator(reverselist(previousround),team1,team2)
			#if x != 0:
		#		print(reverselist(previousround))
		#		print("\n")
		#		print(x,"\n\n")
		else:
			continue

	#Determine the winner
	#Populating dicitonaries to avoid null types in case they didn't get a kill or an awp kill or didn' get a single headshot
	for key in deathdict:
		if killdict.get(key) is None:
			killdict[key] = 0
		else:
			continue
	for key in killdict:
		if deathdict.get(key) is None:
			deathdict[key] = 0
		else:
			continue
			
	for key in deathdict:
		if awpkillsdict.get(key) is None:
			awpkillsdict[key] = 0
		else:
			continue

	for key in deathdict:
		if entryfragdict.get(key) is None:
			entryfragdict[key] = 0
		else:
			continue
	for key in deathdict:
		if hsdict.get(key) is None:
			hsdict[key] = 0
		else:
			continue
	#All info will be appended in dictionary form to the list, we just have to manipulate the list to get what we want
	listofdictionaries.append(killdict)
	listofdictionaries.append(deathdict)
	listofdictionaries.append(hsdict)
	listofdictionaries.append(entryfragdict)
	listofdictionaries.append(awpkillsdict)
	listofdictionaries.append([team1score,team2score])
	
	return listofdictionaries


def thescript(filenamelist):
	for filename in filenamelist:
		logfile = open(filename, 'r')
		
		#extracting information from file
		prename = filename.strip().split('_')
		team1tag = prename[0]
		team2tag = prename[1]
		pre_gamemap = prename[2].split(".txt")
		gamemap = pre_gamemap[0]
		#print(gamemap)

		#find liveon3 and eliminate warmup
		gamefile = gamestart(logfile)
		
		#got all the information i need, close the file
		logfile.close()

		#setup teams
		teams = getteams("teams.txt")
		lineups = setteams(teams,team1tag,team2tag)
		team1 = lineups[0]
		team2 = lineups[1]
		#print(team1,team2)
		#get both halves scores and maybe overtime
		game = splithalves(gamefile)
		firsthalf = buildscores(game[0],team1,team2)
		secondhalf = buildscores(game[1],team2,team1)
		if len(game) > 2:
			overtime = buildscores(game[2],team1,team2)
		
		#merge the scores
		totalscores = []
		killcount = {}
		for key in firsthalf[0]:
			killcount[key] = firsthalf[0].get(key)+secondhalf[0].get(key)
		deathcount = {}
		for key in firsthalf[1]:
			deathcount[key] = firsthalf[1].get(key)+secondhalf[1].get(key)
		hspercentage = {}
		numberhs = {}
		for key in firsthalf[2]:
			numberhs[key] = (firsthalf[2].get(key) + secondhalf[2].get(key))
		"""
		for key in firsthalf[2]:
			hspercentage[key] = (firsthalf[2].get(key)+secondhalf[2].get(key))/killcount.get(key)
			hspercentage[key] = intvalue((hspercentage.get(key))*100)

		"""
		entryfrag = {}
		for key in firsthalf[3]:
			entryfrag[key] = firsthalf[3].get(key) + secondhalf[3].get(key)
		awpkills = {}
		for key in firsthalf[4]:
			awpkills[key] = firsthalf[4].get(key) + secondhalf[4].get(key)

		score = (team1[0],team2[0])
		
		#save all data from the match
		totalscores.append(killcount)
		totalscores.append(deathcount)
		totalscores.append(numberhs)
		totalscores.append(entryfrag)
		totalscores.append(awpkills)
		totalscores.append(score)
		totalscores.append((team1tag,team2tag))
		prewinner = setwinner(team1,team2,team1tag,team2tag)
		winner = prewinner[0]
		loser = prewinner[1]

		#record everything on a file
		recorddata(totalscores,team1tag,team2tag,gamemap,winner,loser)

	return totalscores



#########################################################################################################################
############################################### OUTPUT ## FUNCTIONS #####################################################
#########################################################################################################################

#Record Data
def recorddata(totalscores,team1tag,team2tag,gamemap,winner,loser):
	filename = team1tag + "_" + team2tag + "_" + gamemap + "_output.txt"
	f = open(filename,'w')
	f.write("MATCH: " + team1tag + "-" + team2tag + "\n")
	f.write("MAP: " + gamemap+"\n")
	f.write("WINNER: " + winner[0]+"\n")
	f.write("LOSER: " + loser[0]+"\n")
	score = totalscores[5]
	score1 = score[0]
	score2 = score[1]
	#print(winner)
	#print(loser)
	f.write("SCORE: " + str(score1) + "-" + str(score2) +"\n")
	f.write("Player stats\n")
	f.write(winner[0] + "\n")
	for key in winner[1]:
		f.write(key + ": " + str(totalscores[0].get(key)) + " - " + str(totalscores[1].get(key)) + " - " + str(totalscores[2].get(key)) + " - " + str(totalscores[3].get(key)) + " - " + str(totalscores[4].get(key))+"\n")
	#f.write("\n-----\n")
	f.write(loser[0]+"\n")
	for key in loser[1]:
		f.write(key + ": " + str(totalscores[0].get(key)) + " - " + str(totalscores[1].get(key)) + " - " + str(totalscores[2].get(key)) + " - " + str(totalscores[3].get(key)) + " - " + str(totalscores[4].get(key))+"\n")
	f.close()
	return 0

#Output Score to Console
def outputtotalscores(totalscores):
	for key in totalscores[0]:
		print(key)
		print("kills  - ",totalscores[0].get(key),"---",totalscores[1].get(key)) 
		print("Deaths  - ",totalscores[1].get(key))
		print("Headshots  - ",(totalscores[2].get(key)))
		print("entry frags  - ", totalscores[3].get(key))
		print("awp kills  - ",totalscores[4].get(key))
		print("---------------------------------------------\n\n")
	print("TEAMS",totalscores[6])
	print("SCORE", totalscores[5])
	return 0


def buildtournamentscores():
	teams = getteams("teams.txt")
	teamtags = []
	for key in teams:
		teamtags.append(key)
	teamtournamentscores = {}
	teamtournamentratio = {}   #wins or losses, not actual score
	teamtournamentmaps = {}		#maps they played go throughout the tournament
	playertournamentscores = {}
	teamscore = {}
	team1score = {}
	team2score = {}
	directory = []
	count = 0
	for filename in os.listdir():	
		if filename.endswith("_output.txt"):
			directory.append(filename)
	for file in directory:
		f = open(file,'r')
		for line in f:
			if "MATCH:" in line:
				#print(line)
				match = line.split(":")
				localteams = match[1].strip().split("-")
				team1 = localteams[0]
				team2 = localteams[1] 
				continue
			if "MAP:" in line:
				aux = line.strip().split(":")
				gamemap = aux[1].strip()
				#print(gamemap)
				if teamtournamentmaps.get(team1) == None:
					teamtournamentmaps[team1] = [gamemap]
				else:
					teamtournamentmaps[team1].append(gamemap)
				if teamtournamentmaps.get(team2) == None:
					teamtournamentmaps[team2] = [gamemap]
					continue
				else:
					teamtournamentmaps[team2].append(gamemap)
					continue
			if "WINNER: " in line:
				aux = line.strip().split(":")
				winner = aux[1].strip()
				if teamtournamentratio.get(winner) == None:
					teamtournamentratio[winner] = ["W"]
					continue
				else:
					teamtournamentratio[winner].append("W")
					continue
			if "LOSER: " in line:
				aux = line.strip().split(":")
				loser = aux[1].strip()
				if teamtournamentratio.get(loser) == None:
					teamtournamentratio[loser] = ["L"]
					continue
				else:
					teamtournamentratio[loser].append("L")
					continue
			if "SCORE: " in line:
				continue
			if "Player stats" in line:
				continue
			if line.strip() == "":
				continue
			if line.strip() in teamtags:
				count = 0
				scoringteam = line.strip()
				teamscore = {}
				continue
			playerstats = line.strip().split(":")
			playername = playerstats[0]
			stats = playerstats[1].strip().split("-")
			teamscore[playername] = []
			for element in stats:
				teamscore[playername].append(element)
			count+=1

			if count==4:
				if 	teamtournamentscores.get(scoringteam) == None:
					teamtournamentscores[scoringteam] = [teamscore]
				else:
					teamtournamentscores[scoringteam].append(teamscore)
			else:
				continue
	for key in teamtournamentscores:
		teamtournamentscores[key] = [outputtournamentscores(key,teamtournamentscores)]
	datalist = ["kills","deaths","headshots","entryfrags","awpkills","kdr","hspercentage"]
	f = open("tournamentstats.txt",'w')
	f.write("TOURNAMENT STATS\n")
	f.write("------------------------------------\n")
	for key in teamtournamentscores:
		#print(key)
		f.write(key + "\n")
		f.write("------------------------------------\n")
		f.write("MAP RECORD\n")
		for element in teamtournamentmaps.get(key):
			index2 = teamtournamentmaps.get(key).index(element)
			l = teamtournamentratio.get(key)
			#print(element, l[index2])
			f.write(element + " - " + l[index2] + "\n")
		for dic in teamtournamentscores[key]:
			#print("PLAYER PERFORMANCES")
			f.write("PLAYER PERFORMANCES\n")
			f.write("--------------------\n")
			for key2 in dic:
				iterator = 0
				stats = dic.get(key2)
				#print(key2)
				kdr = stats[0]/stats[1]
				kdr2 = 	format(kdr,'.2f')
				stats.append(kdr2)
				format('.2f')
				hspercentage = stats[2]/stats[0]
				f.write(key2 + "\n")
				hspercentage2 = format(hspercentage, '.2f')
				stats.append(hspercentage2)
				for stat in stats:
					#print(stat, datalist[iterator])
					f.write(datalist[iterator] + " - " + str(stat) + "\n")
					iterator +=1
				f.write("----------------------------\n")
	return 0

def sumlists(list1,list2):
	sumlist = []
	iterator = 0
	for element in list1:
		sumlist.append(intvalue(float(list1[iterator])) + intvalue(float(list2[iterator])))
		iterator +=1
	return sumlist


def outputtournamentscores(dickey,teamtournamentscores):
	tempdic = {}
	for dic in teamtournamentscores[dickey]:
		for key in dic:
			if tempdic.get(key) == None:
				tempdic[key] = dic.get(key)	
			else:
				tempdic[key] = sumlists(dic.get(key),tempdic.get(key))
	return tempdic


#########################################################################################################################
##################################################### MAIN ##############################################################
#########################################################################################################################


def main():
	
	print("Welcome to CSGOSTATS")

	
	filenames = ["alientech_hexagone_cache.txt"]
	outputscores = thescript(filenames)
	#outputtotalscores(outputscores)
	buildtournamentscores()
	print("A script developed by BLACKi")
	
	return 0

################################################ S H I T ## T O ## BE ## D O N E ##########################################

# Test overtime situation

# Reformulate mvp algorithm, mvpround, etc. just find a better rating system

# Make calculations between output files


if __name__ == "__main__":
    main()