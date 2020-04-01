#!/usr/bin/env python3

'''This script currently uses the legacy.aonprd.com/bestiary because the newer
aonprd.com has very poor html for scraping. As a result, the bestiary is more limited at the moment.'''

#This script is intended for pulling stats

import requests, webbrowser, bs4, pprint, re, logging

logging.basicConfig(level=logging.DEBUG, filename='pullStatDebug.txt', format='%(asctime)s - %(levelname)s - %(message)s')

#Ask user for monster for stats
monster = input("What monster do you want stats for? ")
print('''Searching database....
	....
	....
	''')
res = requests.get("http://legacy.aonprd.com/bestiary/" + monster + ".html")

#Gracefully crash program if monster does not exist in bestiary and explain the problem
try:
	res.raise_for_status()
except Exception as exc:
	print("Something went wrong: %s" % (exc))
	print('Try again.')
	exit()

#Search for monster. Display information if multiple monsters are on page.
statSoup = bs4.BeautifulSoup(res.text, features='lxml')
header = statSoup.select('.stat-block-title')
statBlock = statSoup.select('.stat-block-title,.stat-block-breaker,.stat-block-1')
monsterList = []
monsterNum = 0
for i in range(len(statBlock)):
	tag = statBlock[i]
	if tag['class'] == ['stat-block-title']:
		monsterNum += 1
	tag['class'] = tag['class'] + [str(monsterNum)]

if len(header) > 1:
	print('Which of these did you want?')
	for i in range(len(header)):
		monsterList.append(header[i].getText())
		print(str(i + 1) + ') ' + monsterList[i])
	choice = input('Enter the index number: ')
	monsterText = []
	for i in range(len(statBlock)):
		tag = statBlock[i]
		if tag['class'][-1] == choice:
			if tag['class'][0] == 'stat-block-title':
				print('')
				print('/\\/\\/\\/\\' + statBlock[i].getText() + '/\\/\\/\\/\\')
				monsterText.append('/\\/\\/\\/\\' + statBlock[i].getText() + '/\\/\\/\\/\\')
	
			elif tag['class'][0] == 'stat-block-breaker':
				print('-=-=' * 6 + statBlock[i].getText()+ "-=-=" * 6)
				monsterText.append('-=-=' * 6 + statBlock[i].getText()+ "-=-=" * 6)
			else:
				print(statBlock[i].getText())
				monsterText.append(statBlock[i].getText())
	
else:
	print(header[0].getText() +'\nIs this the monster that you want? (y / n)')
	choice = input()
	if choice != "y":
		exit()

	
	#Start pulling data:
	#This will print the monster name and CR level. 
	print('-=-=' * 10)

	#Format the statBlock: the statBlock uses two classes: stat-block-breaker as headers and
	#.stat-block-1 for individual lines.
	statBlock = statSoup.select('.stat-block-title,.stat-block-breaker,.stat-block-1')
	monsterText = []
	for i in range(len(statBlock)):
		tag = statBlock[i]
		if tag['class'][0] == 'stat-block-title':
			print('')
			print('/\\/\\/\\/\\' + statBlock[i].getText() + '/\\/\\/\\/\\')
			monsterText.append('/\\/\\/\\/\\' + statBlock[i].getText() + '/\\/\\/\\/\\')
	
		elif tag['class'][0] == 'stat-block-breaker':
			print('-=-=' * 6 + statBlock[i].getText()+ "-=-=" * 6)
			monsterText.append('-=-=' * 6 + statBlock[i].getText()+ "-=-=" * 6)
		else:
			print(statBlock[i].getText())
			monsterText.append(statBlock[i].getText())
	print('-=-=' * 10)

	#Prepare for stats
	stats = {}
	basicStats = {"Str": "", "Dex": "", "Con": "", "Int": "", "Wis": "", "Cha": "", "Speed": ""}
	for key in basicStats:
		getStat = re.compile(key + r' ([0-9]{1,3})')
		mo = getStat.search(statSoup.getText())
		if mo != None:
			basicStats[key] = mo.group(1) 

	meleeStats = {"Melee": ""}
	for key in meleeStats:
		getStat = re.compile(key + r'\s(.*)')
		mo = getStat.search(statSoup.getText())
		if mo != None:
			meleeStats[key] = mo.group(1)
	print(basicStats)
	print(meleeStats)
print("Do you want to open the web page too? (y / n)")
if input() == "y":
	webbrowser.open("http://legacy.aonprd.com/bestiary/" + monster + ".html")
print('Would you like to save the data to file?')
if input() == 'y':
	monsterFile = open('monster.txt', 'w')
	for i in range(len(monsterText)):
		monsterFile.write(monsterText[i])
		monsterFile.write('\n')
	monsterFile.close()
