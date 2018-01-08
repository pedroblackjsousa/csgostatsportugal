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
stoppermessage = "Host_WriteConfiguration"

def getroundlist(demo):
	roundlist = []
	auxlist =  []
	for line in demo:
		if "round_end" in line.split(" "):
			roundlist.append(auxlist)
			auxlist = []
		else:
			auxlist.append(line)
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

def populatedict(dictionary,listofkeys):
	for key in listofkeys:
		if dictionary.get(key) is None:
			dictionary[key] = 0
		else:
			continue


def roundanalyser(round):
	#start parsing the text
	entryfrag = True
	for element in round:
		#check if there was an interaction ( kill ) and parse the killer
		if "killed" in element:
			killer = getkiller(element)
			print(killer)
			updatedict(killcount,killer)
			killed = getkilled(element)
			print(killed)
			updatedict(deathcount,killed)
			if entryfrag:
				entryfrag = False
				updatedict(entryfrags,killer)
			if "headshot" in element:
				updatedict(headshots,killer)
			if "awp" in element:
				updatedict(awpkills,killer)
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
		#teams = getteams("teams.txt")
		#lineups = setteams(teams,team1tag,team2tag)
		#team1 = lineups[0]
		#team2 = lineups[1]

		game = getroundlist(logfile)

		for element in game:
			roundanalyser(element)

		finalscore =  []
		finalscore.append(killcount)
		finalscore.append(deathcount)
		finalscore.append(headshots)
		finalscore.append(entryfrags)
		finalscore.append(awpkills)

		print(finalscore)

	return finalscore



def main():
	
	print("Welcome to CSGOSTATS")

	
	filenames = ["alientech_hexagone_cache.txt"]
	thescript(filenames)

	return 0

if __name__ == "__main__":
    main()