import random
import sys
import os
import math
import string
from decimal import *

killcount = {}
deathcount = {}
entryfrags = {}
headshots = {}
awpkills = {}
score = {}
#stoppermessage = "Host_WriteConfiguration"


def getroundlist(demo):
	roundlist = []
	auxlist =  []
	for line in demo:
		if "round_end" in line.split(" "):
			auxlist.append(line.strip())
			roundlist.append(cleanround(auxlist))
			auxlist = []
		else:
			auxlist.append(line.strip())
	return roundlist

def getkiller(event):
	list = event.split(':')
	event2 = list[-1].strip()
	namelist = event2.split("killed")
	killer = namelist[0].strip()
	return killer

def getkilled(event):
	list = event.split(':')
	event2 = list[-1].strip()
	namelist = event2.split("killed")
	if "headshot" in event:
		namelist2 = namelist[1].split("with")
		killed = namelist2[0].strip()
	else:
		namelist2 = namelist[1].split("using")
		killed = namelist2[0].strip()
	return killed


def updatedict(dictionary,key):
	if dictionary.get(key) is None:
		dictionary[key] = 1
	else:
		dictionary[key] +=1	

def roundanalyser(round):
	#start parsing the text
	entryfrag = True
	for element in round:
		#check if there was an interaction ( kill ) and parse the killer
		if "killed" in element:
			killer = getkiller(element)
			updatedict(killcount,killer)
			killed = getkilled(element)
			updatedict(deathcount,killed)
			if entryfrag:
				entryfrag = False
				updatedict(entryfrags,killer)
			if "headshot" in element:
				updatedict(headshots,killer)
			if "awp" in element:
				updatedict(awpkills,killer)
	return 0


def clutchsituation(team1,team2,round):
	team1players = list(team1[1])
	team2players = list(team2[1])
	clutchsitch1 = False
	clutchsitch2 = False
	sitstate1 = 0
	sitstate2 = 0
	lock1 = True
	lock2 = True
	for element in round:
		#print(element)
		if "killed" in element:
			killed = getkilled(element)
			if killed in team1players:
				team1players.remove(killed)
			if killed in team2players:
				team2players.remove(killed)
	
		if len(team1players) == 1 and lock1 == True:
			clutchsitch1 = True
			clutchplayer1 = team1players[0]
			sitstate1 = len(team2players)
			lock1 = False

		if len(team2players) == 1 and lock2 == True:
			clutchsitch2 = True
			clutchplayer2 = team2players[0]
			sitstate2 = len(team2players)
			lock1 = False
	
	if clutchsitch1:
		if clutchplayer1 in team1players:
			return clutchplayer1,sitstate1
	if clutchsitch2:
		if clutchplayer2 in team1players:
			return clutchplayer2,sitstate2
	return False

def setteams(teams,team1tag,team2tag):
	team1 = [team1tag]
	team2 = [team2tag]
	for key in teams:
		if key == team1tag:
			team1.append(teams.get(key))
		if key == team2tag:
			team2.append(teams.get(key))
	return [team1,team2]

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


def registerscore(team1,team2,team1tag,team2tag,round):
	if score.get(team1tag) is None:
		score[team1tag] = 0
	if score.get(team2tag) is None:
		score[team2tag] = 0
	winner = getroundwinner(team1,team2,team1tag,team2tag,round)
	score[winner] +=1
	return 0

def cleanround(round):

	cleanedround = []
	round_started_index = 0
	for line in round:
		if "round_start" in line:
			round_started_index = round.index(line)
	return round[round_started_index:]


def getroundwinner(team1,team2,team1tag,team2tag,round):

	bomb_defused = False
	bomb_exploded = False
	bomb_planted = False

	for event in round:
		if "bomb_defused" in event:
			bomb_defused = True
		if "bomb_exploded" in event:
			bomb_exploded = True
		if "bomb_planted" in event:
			bomb_planted = True
			bomb_planted_index = round.index(event)
		if "round_end" in event:
			round_end_index = round.index(event)

	if bomb_defused:
		return team1tag
	if bomb_exploded:
		return team2tag


	if bomb_planted and not bomb_defused:
		if bomb_planted_index<round_end_index:
			return team2tag
	
	if elimination(team1,team2,team1tag,team2tag,round) != "":
		return elimination(team1,team2,team1tag,team2tag,round)

	#print(round)
	return team1tag

def getmatchwinner(score):
	winner = max(score, key = score.get)
	loser = min(score, key = score.get)
	return [winner,loser]


def elimination(team1,team2,team1tag,team2tag,round):
	team1players = list(team1[1])
	team2players = list(team2[1])
	for element in round:
		#print(element)
		if "killed" in element:
			killed = getkilled(element)
			if killed in team1players:
				team1players.remove(killed)
			if killed in team2players:
				team2players.remove(killed)
	#print(team1players,team2players)
	if len(team1players) == 0:
		return team2tag
	if len(team2players) ==0:
		return team1tag
	return ""

def populatedicts(team1,team2,score):
	teams = [team1,team2]
	for team in teams:
		for player in team:
			killcount[player] = 0
			deathcount[player] = 0
			entryfrags[player] = 0
			headshots[player] = 0
			awpkills[player] = 0
	for key in score:
		score[key] = 0
	return 0




def thescript(filenamelist):

	for filename in filenamelist:
		logfile = open(filename, 'r')
		
		#extracting information from file
		prename = filename.strip().split('_')
		team1tag = prename[0]
		team2tag = prename[1]
		pre_gamemap = prename[2].split(".txt")
		gamemap = pre_gamemap[0]
		
		#setup teams
		teams = getteams("teams.txt")
		#print(teams)
		lineups = setteams(teams,team1tag,team2tag)
		team1 = lineups[0]
		team2 = lineups[1]
		#print(team1,team2)
		game = getroundlist(logfile)


		
		populatedicts(team1[1],team2[1],score)

		print(killcount,deathcount,headshots,entryfrags,awpkills)

		round = 1
		# MR3
		ticker = 0
		overtime_aux = 3
		overtimebol = True

		for element in game:
			roundanalyser(element)
			if round >= 31:
				if overtimebol:
					registerscore(team2,team1,team2tag,team1tag,element)
					ticker +=1
					if ticker == overtime_aux:
						ticker == 0
						overtimebol = False
				else:
					registerscore(team1,team2,team1tag,team2tag,element)
					ticker +=1
					if ticker == overtime_aux:
						ticker == 0
						overtimebol = True
				round +=1
				print(score)
				continue
			if round <= 15:
				registerscore(team1,team2,team1tag,team2tag,element)
				round +=1
				print(score)
				continue
			else:
				registerscore(team2,team1,team2tag,team1tag,element)
				round +=1
				print(score)
				continue
			if not clutchsituation(team1,team2,element):
				continue
			else:
				continue
		finalscore =  []
		finalscore.append(killcount)
		finalscore.append(deathcount)
		finalscore.append(headshots)
		finalscore.append(entryfrags)
		finalscore.append(awpkills)

	print(score)
	
	return finalscore

#Record Data
def recorddata(totalscores,team1tag,team2tag,gamemap,winner,loser):
	filename = team1tag + "_" + team2tag + "_" + gamemap + "_output.txt"
	f = open(filename,'w')
	f.write("MATCH: " + team1tag + "-" + team2tag + "\n")
	f.write("MAP: " + gamemap+"\n")
	aux_var = getmatchwinner(score)
	winner = aux_var[0]
	loser = aux_var[1]
	f.write("WINNER: " + winner + "\n")
	f.write("LOSER: " + loser + "\n")
	score1 = score.get(team1tag)
	score2 = score.get(team2tag)
	f.write("SCORE: " + str(score1) + "-" + str(score2) +"\n")
	f.write("Player stats\n")

	#edit more 
	f.write(winner[0] + "\n")
	for key in winner[1]:
		f.write(key + ": " + str(totalscores[0].get(key)) + " - " + str(totalscores[1].get(key)) + " - " + str(totalscores[2].get(key)) + " - " + str(totalscores[3].get(key)) + " - " + str(totalscores[4].get(key))+"\n")
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
	return 0

def main():
	
	print("Welcome to CSGOSTATS")

	
	filenames = ["Astralis_SK_Cache.txt","Astralis_SK_Inferno.txt","SK_Astralis_Mirage.txt"]
	stats = thescript(filenames)
	return 0

if __name__ == "__main__":
    main()