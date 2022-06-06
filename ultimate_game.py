import random
import os
import json
from os.path import exists

class Player:
	def __init__(self, name, number):
		self.Playernumber = number
		self.PlayerName = name
		self.BoardPosition = [1,0]
		self.PlayerMoney = 3200
		self.OwnedProps = []
		self.IsInJail = False
		self.turnsInJail = 0
		self.isBankrupt = False
		self.travelVouchers = []
		self.heldActionCards = []
		self.rollThreeCards = []
		self.ownedColorGroups = {}
		self.ownsImprovableCG = False
	
	def __repr__(self):
		return self.PlayerName
	def __str__(self):
		return self.PlayerName
		
	def turnsInJailString(self):
		if self.turnsInJail == 0:
			return "First"
		elif self.turnsInJail == 1:
			return "Second"
		elif self.turnsInJail == 2:
			return "Third"
	
	#ownedColorGroups = {"CGName": [improvableBool, [propNum, ofEach]]}
	def checkForCG(self):
		for i in range(len(self.OwnedProps)):
			if Gameboard.propList[self.OwnedProps[i]][1] == "CG":
				if Gameboard.propList[self.OwnedProps[i]][5] in self.ownedColorGroups:
					if self.ownedColorGroups[Gameboard.propList[self.OwnedProps[i]][5]][1].count(self.OwnedProps[i]) == 0:
						self.ownedColorGroups[Gameboard.propList[self.OwnedProps[i]][5]][1].append(self.OwnedProps[i])
					else:
						pass
				else:
					self.ownedColorGroups[Gameboard.propList[self.OwnedProps[i]][5]] = [0, [self.OwnedProps[i]]]
				if len(self.ownedColorGroups[Gameboard.propList[self.OwnedProps[i]][5]][1]) > Gameboard.propList[self.OwnedProps[i]][11] / 2:
					self.ownedColorGroups[Gameboard.propList[self.OwnedProps[i]][5]][0] = 1
					if len(self.ownedColorGroups[Gameboard.propList[self.OwnedProps[i]][5]][1]) == Gameboard.propList[self.OwnedProps[i]][11]:
						self.ownedColorGroups[Gameboard.propList[self.OwnedProps[i]][5]][0] = 2
					self.ownsImprovableCG = True
		for i in list(self.ownedColorGroups):
			if i in self.ownedColorGroups:
				j = 0
				#print(self.ownedColorGroups)
				#print(i)
				length = len(self.ownedColorGroups[i][1])
				while j < length:
					if Gameboard.propList[self.ownedColorGroups[i][1][j]][2] != self.Playernumber:
						self.ownedColorGroups[i][1].pop(j)
						j = j - 1
						#print("we popped one")
						if len(self.ownedColorGroups[i][1]) == 0:
							del self.ownedColorGroups[i]
							break
						elif len(self.ownedColorGroups[i][1]) < Gameboard.propList[self.ownedColorGroups[i][1][0]][11] and len(self.ownedColorGroups[i][1]) > Gameboard.propList[self.ownedColorGroups[i][1][0]][11] / 2:
							self.ownedColorGroups[i][0] = 1
						elif len(self.ownedColorGroups[i][1]) < Gameboard.propList[self.ownedColorGroups[i][1][0]][11] / 2:
							self.ownedColorGroups[i][0] = 0
					j = j + 1
			else:
				continue
		#print(self.ownedColorGroups)

class Diceclass:
	def __init__(self):
		self.State = [random.randint(1,6), random.randint(1,6)]
	
	def Sum(self):
		return self.State[0] + self.State[1]
	def Roll(self):
		return [random.randint(1,6), random.randint(1,6)]
Dice = Diceclass()

class Gameboardclass:
	def __init__(self):
		self.listspace = [["Free Parking", "Lake Street", "Community Chest (Outer 1)", "Nicollet Avenue", "Hennepin Avenue", "Bus Ticket", "Checker Cab Company", "Reading Railroad", "Esplanade Avenue", "Canal Street", "Chance (Outer 1)", "Cable Company", "Magazine Street", "Bourbon Street", "Holland Tunnel Outer", "Auction", "Katy Freeway", "Westheimer Road", "Internet Service Provider", "Kirby Drive", "Cullen Boulevard", "Chance (Outer 2)", "Black & White Cab Company", "Dekalb Avenue", "Community Chest (Outer 2)", "Andrew Young Intl Boulevard", "Decatur Street", "Peachtree Street", "Payday",    "Randolph Street", "Chance", "Lake Shore Drive", "Wacker Drive", "Michigan Avenue", "Yellow Cab Company", "B&O Railroad Outer", "Community Chest", "South Temple", "West Temple", "Trash Collector", "North Temple", "Temple Square", "Subway", "South Street", "Broad Street", "Walnut Street", "Community Chest", "Market Street", "Bus Ticket", "Sewage System", "Ute Cab Company", "Birthday Gift", "Mulholland Drive", "Ventura Boulevard", "Chance", "Rodeo Drive"],["Go",        "Mediterranean Avenue", "Community Chest", "Baltic Avenue", "Income Tax", "Reading Railroad Middle", "Oriental Avenue", "Chance Middle 1", "Vermont Avenue", "Connecticut Avenue", "Roll Three", "St Charles Place", "Electric Company", "States Avenue", "Virginia Avenue", "Pennsylvania Railroad Middle", "St James Place", "Community Chest Middle 2", "Tennessee Avenue", "New York Avenue", "In Jail / Just Visiting", "Kentucky Avenue", "Chance Middle 2", "Indiana Avenue", "Illinois Avenue", "B&O Railroad Middle", "Atlantic Avenue", "Ventnor Avenue", "Water Works", "Marvin Gardens", "Squeeze Play", "Pacific Avenue", "North Carolina Avenue", "Community Chest Middle 3", "Pennsylvania Avenue", "Short Line Middle", "Chance Middle 3", "Park Place", "Luxury Tax", "Boardwalk"], ["Go to Jail", "The Embarcadero", "Fishermans Wharf", "Telephone Company", "Community Chest Inner", "Beacon Street", "Bonus",    "Boylston Street", "Newbury Street", "Pennsylvania Railroad Inner", "Fifth Avenue", "Madison Avenue", "Stock Exchange", "Wall Street", "Tax Refund", "Gas Company", "Chance Inner", "Florida Avenue", "Holland Tunnel Inner", "Miami Avenue", "Biscayne Avenue", "Short Line Inner", "Reverse Direction", "Lombard Street"]]
		self.spaceType = [["Free Parking", "Property",    "Community Chest",           "Property",        "Property",        "Bus Ticket", "Property",            "Property",         "Property",         "Property",     "Chance",           "Property",      "Property",        "Property",       "Holland Tunnel",       "Auction", "Property",     "Property",        "Property",                  "Property",    "Property",         "Chance",           "Property",                  "Property",      "Community Chest",           "Property",                    "Property",       "Property",         "Paycorner", "Property",        "Chance", "Property",         "Property",     "Property",        "Property",           "Property",           "Community Chest", "Property",     "Property",    "Property",        "Property",     "Property",      "Subway", "Property",     "Property",     "Property",      "Community Chest", "Property",      "Bus Ticket", "Property",      "Property",        "Birthday Gift", "Property",         "Property",          "Chance", "Property"],   ["Paycorner", "Property",             "Community Chest", "Property",      "Income Tax", "Property",                "Property",        "Chance",          "Property",       "Property",           "Roll Three", "Property",         "Property",         "Property",      "Property",        "Property",                     "Property",       "Community Chest" ,         "Property",         "Property",        "Jail",                    "Property",        "Chance",          "Property",       "Property",        "Property",            "Property",        "Property",       "Property",    "Property",       "Squeeze Play", "Property",       "Property",              "Community Chest",          "Property",            "Property",          "Chance",          "Property",   "Luxury Tax", "Property"],  ["Go to Jail", "Property",        "Property",         "Property",          "Community Chest",       "Property",      "Paycorner", "Property",        "Property",       "Property",                    "Property",     "Property",       "Stock Exchange", "Property",    "Tax Refund", "Property",    "Chance",       "Property",       "Holland Tunnel",       "Property",     "Property",        "Property",         "Reverse Direction", "Property"]]
		self.propNum =   [[-1,              0,            -1,                          1,                 2,                 -1,           3,                     4,                  5,                  6,              -1,                 7,               8,                 9,                -1,                     -1,        10,             11,                12,                          13,            14,                 -1,                 15,                          16,              -1,                          17,                            18,               19,                 -1,          20,                -1,       21,                 22,             23,                24,                   25,                   -1,                26,             27,            28,                29,             30,              -1,       31,             32,             33,              -1,                34,              -1,           35,              36,                -1,              37,                 38,                  -1,       39],           [-1,          40,                     -1,                41,              -1,           4,                         42,                -1,                43,               44,                   -1,           45,                 46,                 47,              48,                49,                             50,               -1,                         51,                 52,                -1,                        53,                -1,                54,               55,                25,                    56,                57,               58,            59,               -1,             60,               61,                      -1,                         62,                   63,                  -1,                64,           -1,           65,],         [-1,           66,                67,                 68,                  -1,                      69,              -1,         70,                71,               49,                            72,             73,               -1,               74,            -1,           75,            -1,             76,               -1,                     77,             78,                63,                 -1,                  79]]
		#[0."name", 1."property type", 2."Current owner", 3.price, 4."mortgageStatus", 5."color group name", 6.collectionLevel, 7.developmentLevel, 8.[(base rent), (one house), (two house), (three house), (four house), (hotel), (skyscraper)], 9.mortgagePrice, 10.improvementCost]
		self.propList = [["Lake St.", "CG", "bank", 30, "unmorgaged", "Rose", 0,0, [1,5,15,45,80,125,625], 15, 50, 3],
		["Nicollet Ave.", "CG", "bank", 30, "unmorgaged", "Rose", 0,0, [1,5,15,45,80,125,625], 15, 50, 3],
		["Hennepin Ave.", "CG", "bank", 60, "unmorgaged", "Rose", 0,0, [3,15,45,120,240,350,850], 30, 50, 3],
		["Checker Cab Co.", "CabCo", "bank", 300, "unmorgaged", [30,60,120,240], 150],
		["Reading Railroad", "Railroad", "bank", 200, "unmorgaged", [25,50,100,200], 100],
		["The Esplanade", "CG", "bank", 90, "unmorgaged", "Light Green", 0,0, [5,25,80,225,360,600,1000], 50, 50, 4],
		["Canal St.", "CG", "bank", 90, "unmorgaged", "Light Green", 0,0, [5,25,80,225,360,600,1000], 50, 50, 4],
		["Cable Company", "Utility", "bank", 150, "unmorgaged", [4,10,20,40,80,100,120,150], 75],
		["Magazine St.", "CG", "bank", 120, "unmorgaged", "Light Green", 0,0, [8,40,100,300,450,600,1100], 60, 50, 4],
		["Bourbon St.", "CG", "bank", 120, "unmorgaged", "Light Green", 0,0, [8,40,100,300,450,600,1100], 60, 50, 4],
		["Katy Freeway", "CG", "bank", 150, "unmorgaged", "Light Yellow", 0,0, [11,55,160,475,650,800,1300], 70, 100, 4],
		["Westheimer Rd.", "CG", "bank", 150, "unmorgaged", "Light Yellow", 0,0, [11,55,160,475,650,800,1300], 70, 100, 4],
		["Internet Service Provider", "Utility", "bank", 150, "unmorgaged", [4,10,20,40,80,100,120,150], 75],
		["Kirby Dr.", "CG", "bank", 180, "unmorgaged", "Light Yellow", 0,0, [14,70,200,550,750,950,1450], 80, 100, 4],
		["Cullen Blvd.", "CG", "bank", 180, "unmorgaged", "Light Yellow", 0,0, [14,70,200,550,750,950,1450], 80, 100, 4],
		["Black & White Cab Co.", "CabCo", "bank", 300, "unmorgaged", [30,60,120,240], 150],
		["Dekalb Ave.", "CG", "bank", 210, "unmorgaged", "Teal", 0,0, [17,85,240,670,840,1025,1525], 90, 100, 4],
		["Young Int'l Blvd.", "CG", "bank", 210, "unmorgaged", "Teal", 0,0, [17,85,240,670,840,1025,1525], 90, 100, 4],
		["Decatur St.", "CG", "bank", 240, "unmorgaged", "Teal", 0,0, [20,100,300,750,925,1100,1600], 100, 100, 4],
		["Peachtree St.", "CG", "bank", 240, "unmorgaged", "Teal", 0,0, [20,100,300,750,925,1100,1600], 100, 100, 4],
		["Randolph St.", "CG", "bank", 270, "unmorgaged", "Maroon", 0,0, [23,115,345,825,1010,1180,2180], 110, 150, 4],
		["Lake Shore Dr.", "CG", "bank", 270, "unmorgaged", "Maroon", 0,0, [23,115,345,825,1010,1180,2180], 110, 150, 4],
		["Wacker Dr.", "CG", "bank", 300, "unmorgaged", "Maroon", 0,0, [26,130,390,900,1100,1275,2275], 120, 150, 4],
		["Michigan Ave.", "CG", "bank", 300, "unmorgaged", "Maroon", 0,0, [26,130,390,900,1100,1275,2275], 120, 150, 4],
		["Yellow Cab Co.", "CabCo", "bank", 300, "unmorgaged", [30,60,120,240], 150],
		["B. & O. Railroad", "Railroad", "bank", 200, "unmorgaged", [25,50,100,200], 100],
		["South Temple", "CG", "bank", 330, "unmorgaged", "Brown", 0,0, [32,160,470,1050,1250,1500,2500], 130, 200, 4],
		["West Temple", "CG", "bank", 330, "unmorgaged", "Brown", 0,0, [32,160,470,1050,1250,1500,2500], 130, 200, 4],
		["Trash Collector", "Utility", "bank", 150, "unmorgaged", [4,10,20,40,80,100,120,150], 75],
		["North Temple", "CG", "bank", 360, "unmorgaged", "Brown", 0,0, [38,170,520,1125,1425,1600,2650], 140, 200, 4],
		["Temple Square", "CG", "bank", 360, "unmorgaged", "Brown", 0,0, [38,170,520,1125,1425,1600,2650], 140, 200, 4],
		["South St.", "CG", "bank", 390, "unmorgaged", "Peach", 0,0, [45,210,575,1300,1600,1800,3300], 150, 250, 4],
		["Broad St.", "CG", "bank", 390, "unmorgaged", "Peach", 0,0, [45,210,575,1300,1600,1800,3300], 150, 250, 4],
		["Walnut St.", "CG", "bank", 420, "unmorgaged", "Peach", 0,0, [55,225,630,1450,1750,2050,3550], 160, 250, 4],
		["Market St.", "CG", "bank", 420, "unmorgaged", "Peach", 0,0, [55,225,630,1450,1750,2050,3550], 160, 250, 4],
		["Sewage System", "Utility", "bank", 150, "unmorgaged", [4,10,20,40,80,100,120,150], 75],
		["Ute Cab Co.", "CabCo", "bank", 300, "unmorgaged", [30,60,120,240], 150],
		["Mulholland Blvd.", "CG", "bank", 450, "unmorgaged", "Dark Red", 0,0, [70,350,750,1600,1850,2100,3600], 175, 300, 3],
		["Ventura Blvd.", "CG", "bank", 480, "unmorgaged", "Dark Red", 0,0, [80,400,825,1800,2175,2550,4050], 200, 300, 3],
		["Rodeo Dr.", "CG", "bank", 510, "unmorgaged", "Dark Red", 0,0, [90,450,900,2000,2500,3000,4500], 250, 300, 3],
		["Mediterranean Ave.", "CG", "bank", 60, "unmorgaged", "Purple", 0,0, [2,10,30,90,160,250,750], 30, 50, 2],
		["Baltic Ave.", "CG", "bank", 60, "unmorgaged", "Purple", 0,0, [4,20,60,180,320,450,900], 30, 50, 2],
		["Oriental Ave.", "CG", "bank", 100, "unmorgaged", "Light Blue", 0,0, [6,30,90,270,400,550,1050], 50, 50, 3],
		["Vermont Ave.", "CG", "bank", 100, "unmorgaged", "Light Blue", 0,0, [6,30,90,270,400,550,1050], 50, 50, 3],
		["Connecticut Ave.", "CG", "bank", 120, "unmorgaged", "Light Blue", 0,0, [8,40,100,300,450,600,1100], 60, 50, 3],
		["St. Charles Place", "CG", "bank", 140, "unmorgaged", "Pink", 0,0, [10,50,150,450,625,750,1250], 70, 100, 3],
		["Electric Company", "Utility", "bank", 150, "unmorgaged", [4,10,20,40,80,100,120,150], 75],
		["States Ave.", "CG", "bank", 140, "unmorgaged", "Pink", 0,0, [10,50,150,450,625,750,1250], 70, 100, 3],
		["Virginia Ave.", "CG", "bank", 160, "unmorgaged", "Pink", 0,0, [12,60,180,500,700,900,1400], 80, 100, 3],
		["Pennsylvania R.R.", "Railroad", "bank", 200, "unmorgaged", [25,50,100,200], 100],
		["St. James Place", "CG", "bank", 180, "unmorgaged", "Light Orange", 0,0, [14,70,200,550,750,950,1450], 90, 100, 3],
		["Tennessee Ave.", "CG", "bank", 180, "unmorgaged", "Light Orange", 0,0, [14,70,200,550,750,950,1450], 90, 100, 3],
		["New York Ave.", "CG", "bank", 200, "unmorgaged", "Light Orange", 0,0, [16,80,220,600,800,1000,1500], 100, 100, 3],
		["Kentucky Ave.", "CG", "bank", 220, "unmorgaged", "Light Red", 0,0, [18,90,250,700,875,1050,2050], 100, 150, 3],
		["Indiana Ave.", "CG", "bank", 220, "unmorgaged", "Light Red", 0,0, [18,90,250,700,875,1050,2050], 100, 150, 3],
		["Illinois Ave.", "CG", "bank", 240, "unmorgaged", "Light Red", 0,0, [20,100,300,750,925,1100,2100], 120, 150, 3],
		["Atlantic Ave.", "CG", "bank", 260, "unmorgaged", "Dark Yellow", 0,0, [22,110,330,800,975,1150,2150], 130, 150, 3],
		["Ventnor Ave.", "CG", "bank", 260, "unmorgaged", "Dark Yellow", 0,0, [22,110,330,800,975,1150,2150], 130, 150, 3],
		["Water Works", "Utility", "bank", 150, "unmorgaged", [4,10,20,40,80,100,120,150], 75],
		["Marvin Gardens", "CG", "bank", 280, "unmorgaged", "Dark Yellow", 0,0, [24,120,350,850,1025,1200,2200], 140, 150, 3],
		["Pacific Ave.", "CG", "bank", 300, "unmorgaged", "Dark Green", 0,0, [26,130,390,900,1100,1275,2275], 150, 200, 3],
		["No. Carolina Ave.", "CG", "bank", 300, "unmorgaged", "Dark Green", 0,0, [26,130,390,900,1100,1275,2275], 150, 200, 3],
		["Pennsylvania Ave.", "CG", "bank", 320, "unmorgaged", "Dark Green", 0,0, [28,150,450,1000,1200,1400,2400], 160, 200, 3],
		["Short Line", "Railroad", "bank", 200, "unmorgaged", [25,50,100,200], 100],
		["Park Place", "CG", "bank", 350, "unmorgaged", "Dark Blue", 0,0, [35,175,500,1100,1300,1500,2500], 200, 200, 2],
		["Boardwalk", "CG", "bank", 400, "unmorgaged", "Dark Blue", 0,0, [50,200,600,1400,1700,2000,3000], 200, 200, 2],
		["The Embarcadero", "CG", "bank", 210, "unmorgaged", "White", 0,0, [17,85,240,475,670,1025,1525], 105, 100, 3],
		["Fishermans Wharf", "CG", "bank", 250, "unmorgaged", "White", 0,0, [21,105,320,780,950,1125,1625], 125, 100, 3],
		["Telephone Company", "Utility", "bank", 150, "unmorgaged", [4,10,20,40,80,100,120,150], 75],
		["Beacon St.", "CG", "bank", 330, "unmorgaged", "Black", 0,0, [30,160,470,1050,1250,1500,2500], 165, 200, 3],
		["Boylston St.", "CG", "bank", 330, "unmorgaged", "Black", 0,0, [30,160,470,1050,1250,1500,2500], 165, 200, 3],
		["Newbury St.", "CG", "bank", 380, "unmorgaged", "Black", 0,0, [40,185,550,1100,1500,1700,2700], 190, 200, 3],
		["Fifth Ave.", "CG", "bank", 430, "unmorgaged", "Gray", 0,0, [60,220,650,1500,1800,2100,3600], 215, 300, 3],
		["Madison Ave.", "CG", "bank", 430, "unmorgaged", "Gray", 0,0, [60,220,650,1500,1800,2100,3600], 215, 300, 3],
		["Wall St.", "CG", "bank", 500, "unmorgaged", "Gray", 0,0, [80,300,800,1800,2200,2700,4200], 250, 300, 3],
		["Gas Company", "Utility", "bank", 150, "unmorgaged", [4,10,20,40,80,100,120,150], 75],
		["Florida Ave.", "CG", "bank", 130, "unmorgaged", "Dark Orange", 0,0, [9,45,120,350,500,700,1200], 65, 50, 3],
		["Miami Ave.", "CG", "bank", 130, "unmorgaged", "Dark Orange", 0,0, [9,45,120,350,500,700,1200], 65, 50, 3],
		["Biscayne Ave.", "CG", "bank", 150, "unmorgaged", "Dark Orange", 0,0, [11,55,160,475,650,800,1300], 65, 50, 3],
		["Lombard St.", "CG", "bank", 210, "unmorgaged", "White", 0,0, [17,85,240,475,670,1025,1525], 105, 100, 3]]
		self.poolMoney = 0
	def ref(self, coords):
		return self.listspace[coords[0]][coords[1]]
Gameboard = Gameboardclass()

class aCardClass:
	def __init__(self):
		self.chanceDeck = [0,1,2,2,2,2,2,2,3,4,5,6,7,8,9,10,11,12,13,14,14,15,16,17,18,19,20,20,21,21,22,23,24,25,26,26,26,26,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58]
		#[0. "title", 1. "text", 2. "handler", 3. [handlerdata]]
		self.chanceCards = [["Advance to Illinois Ave.", "If Unowned, you may buy it from the Bank, or put it up for Auction.\nIf Owned, pay the owner the normal rent due.\nPlay this card immediately.", "ast", [1,24]],
		["Advance to Saint Charles Place.", "If Unowned, you may buy it from the Bank, or put it up for Auction.\nIf Owned, pay the owner the normal rent due.\nPlay this card immediately.", "ast", [1,11]],
		["Advance to the Stock Exchange", "If you pass 'Pay Day' collect $300 from the Bank.\nPlay this card immediately.", "ast", [2,12]],
		["Advance to Boardwalk", "If Unowned, you may buy it from the Bank, or put it up for Auction.\nIf Owned, pay the owner the normal rent due.\nPlay this card immediately.", "ast", [1,39]],
		["Ride on the Reading", "If Unowned, you may buy it from the Bank, or put it up for Auction.\nIf Owned, pay the owner the normal rent due.\nPlay this card immediately.", "ast", [1,5]],
		["Occupy Wall Street", "If Unowned, you may buy it from the Bank, or put it up for Auction.\nIf Owned, pay the owner the normal rent due.\nPlay this card immediately.", "ast", [1,11]],
		["Get Rollin'", "Advance to Roll 3!\nRoll the dice.\nPlay this card immediately.", "ast", [1,10]],
		["Advance to Boylston Street", "If you pass a Pay Corner, collect your income from the Bank.\nPlay this card immediately.", "ast", [2,7]],
		["Advance to Lombard Street", "If you pass a Pay Corner, collect your income from the Bank.\nPlay this card immediately.", "ast", [2,23]],
		["HEY! TAXI!!! *whistle*", "Advance to Black & White Cab Co.\nIf Unowned, you may buy it from the Bank, or put it up for Auction.\nIf Owned, pay the owner the normal rent due.\nPlay this card immediately.", "ast", [0,22]],
		["Advance to Squeeze Play", "If you pass a Pay Corner, collect your income from the Bank.\nPlay this card immediately.", "ast", [1.30]],
		["Garbage Day", "Advance to Trash Collector. If owned, roll 2 dice and pay the owner 10x the roll. If unowned, you may buy it, or put it up for auction. If you pass a Pay Corner, collect your income.\nPlay this card immediately", "ast", [1,30]],
		["Advance to the Pay Corner", "Collect your income for landing there from the Bank.\nOn the Outer Track - 'Payday' - $400\nOn the Center Track - 'Go' - $200\nOn the Inner Track - 'Bonus' - $300\nPlay this card immediately", "apc"],
		["Advance to the Nearest Utility", "If Unowned, you may buy it from the Bank, or put it up for Auction.\nIf Owned, roll 2 dice and pay the owner 10 times the roll.\nPlay this card immediately.", "atn", "utility"],
		["Advance to the Nearest Railroad", "If Unowned, you may buy it from the Bank, or put it up for Auction.\nIf Owned, pay the owner the normal rent due.\nPlay this card immediately.", "atn", "railroad"],
		["Taxi Wars are not Fare!", "Take any 1 Cab Company from any player. If none are owned, purchase your choice from the bank. Advance to that space. If you pass a Pay Corner, collect your income.\nPlay this card immediately.", "atcsp"], 
		["Advance to Tax Refund", "Collect 50% of the Pool, if any.\nGive each player $50 for their help in doing your taxes.\nPlay this card immediately.", "astpep", [2,14]],
		["Ride the Subway", "Move directly to the Subway space.\nOn your next turn, move to any space on the board.\nPlay this card immediately.", "mdst", [0,42]],
		["MARDI GRAS!", "Everyone has to see the parade of Rex, King of Carnival.\nALL players must move directly to Canal Street.\nPlay this card immediately.", "amdst", [0,9]],
		["Get Taken for a Ride", "Cabbie takes the scenic route.\nGo directly to the nearest Cab Company. If owned pay double rent. If Unowned, do nothing. (You cannot purchase or auction the property.)\nPlay this card immediately.", "mdn", "cabco"],
		["Changing Lanes", "Move directly to the space that is 1 track below this one. If you are on the Outer Track, do nothing.\nPlay this card immediately.", "mdup", "down"],
		["Changing Lanes", "Move directly to the space that is 1 track above this one. If you are on the Inner Track, do nothing.\nPlay this card immediately.", "mdup", "up"],
		["GPS is not working", "Stop and ask for directions.\nAllow the player to your left to move your token directly to any space on the board, their choice.\nPlay this card immediately.", "mdc"],
		["Go to Jail!", "Go directly to Jail.\nDo not pass any Pay Corner.\nDo not collect any money.\nPlay this card immediately.", "gtj"],
		["Pay Back!", "Go directly to jail for illegal business practices. While in jail, you may not collect rent. All rent due to you goes to the Pool.\nPlay this card immediately.", "gtjnr"],
		["Get Out of Jail Free!", "Keep until needed. Play at any time on your turn. This card may be traded or sold.", "keep", "gojf"],
		["Just Say 'NO'!", "Play at any time to stop another player's action against you.\nKeep until needed. Play at any time. This card may be traded or sold.", "keep", "jsn"],
		["Buyer's Market!", "Move to any Unowned Outer Track property. Buy it from the Bank for 1/2 price.\nKeep until needed. Play at any time on your turn.", "keep", "mduopbd"],
		["Excellent Accounting", "Advance to Tax Refund.\nCollect ALL of the Pool.\nKeep until needed. Play at any time on your turn. This card may be traded or sold.", "keep", "atfca"],
		["Strong-armed Deal", "Swap a property card with a player of your choice. It can't be part of a monopoly.\nKeep until needed. Play at any time on your turn. This card may be traded or sold.", "keep", "mft"],
		["See You In Court!", "Sue any player for unfair business practices. Take $250 from any player of your choice.\nKeep until needed. Play at any time on your turn.", "keep", "sap"],
		["Slick Move", "Steal a property card from a player of your choice. It can't be part of a monopoly.\nKeep until needed. Play at any time on your turn. This card may be traded or sold.", "keep", "stap"],
		["Foreclosed Property Sale!", "Foreclose on any opponent's mortgaged property. Pay the mortgage value to the bank to claim the property.\nKeep until needed. Play at any time on your turn.", "keep", "camp"],
		["Zero Dollars Down!", "Build 1 FREE house on any property in a monopoly you own.\nKeep until needed. Play at any time on your turn. This card may be traded or sold.", "keep", "bfh"],
		["Always Bank on Family", "Your cousin becomes the President of the Bank. The Bank will add $100 to your final bid in the next auction.\nKeep until needed. Play at any time. This card may be traded or sold.", "keep", "iaub"],
		["Comped Room", "The next time you land on anyone else's property, you are excused from paying rent.\nPlay this card the next time you land on someone's property.", "keep", "pnr"],
		["School Fees", "Pay the Pool $150\nPlay this card immediately.", "pmp", 150],
		["Party Time", "You hold a Party to impress community leaders.\nPay $25 to the Pool.\nPlay this card immediately.", "pmp", 25],
		["Loan Matures!", "Collect $150 from the Bank.\nPlay this card immediately.", "cmb", 150],
		["Holiday Bonus!", "Collect $100 from the Bank.\nPlay this card immediately.", "cmb", 100],
		["Gain Interest from Savings", "Collect $50 from the Bank.\nPlay this card immediately.", "cmb", 50],
		["Win the Marathon!", "Take a victory lap around the board (on your current Track) and collect the Pay Corner income from the Bank.\nPlay this card immediately.", "ccpc"],
		["You are elected as the Chairperson", "Pay each player $50.\nPlay this card immediately.", "pep", 50],
		["Social Media Fail!", "Someone posting to your company's official online presence made you look bad. Pay each other player $50 to restore good PR.\nPlay this card immediately.", "pep", 50],
		["New Fitness Craze", "The latest trend in exercise is here. Pay each player $25 for lessons and equipment.\nPlay this card immediately.", "pep", 50],
		["Shouldn't the Train be here already?", "If you own any railroads or United Railways stock, pay each player $50 as a refund for poor service.\nPlay this card immediately.", "ifxpep", ["railroad", 50] ],
		["Go Back Three (3) Spaces", "Play this card immediately.", "mxs", -3],
		["Forward Thinker", "Advance forward 3 spaces.\nPlay this card immediately.", "mxs", 3],
		["Stock Market CRASH!", "ALL Stockholders turn in 1/2 (rounded up) of all their stocks for each company to the bank.\n(They may be repurchased later.)\nPlay this card immediately.", "retstk"],
		["Video Killed the Radio Star!", "Dividends for General Radio are 1/2 (rounded up to the nearest dollar) for all stockholders for the next 2 payouts.\nPlay this card immediately.", "reddiv", "general radio"],
		["Entertainment Rocks!", "Stockholders in Motion Pictures and General Radio can immediately collect dividends.\nPlay this card immediately.", "coldiv", ["motion pictures", "general radio"]],
		["Travel is all the Rage!","Stockholders in United Railways, Acme Motors, and Allied Steamships cnan immediately collect dividends.\nPlay this card immediately.", "coldiv", ["united railways", "acme motors", "allied steamships"]],
		["Electric Car Shocking Success!", "Stockholder in Acme Motors and National Utilities can immedieately collect dividends. Owner of Electric Company collects TRIPLE dividends!\nPlay this card immediately.", "coldivec", ["acme motors", "national utilities"]],
		["Caught Insider Trading!", "Pay the Pool a fine equal to the dividends on all the stock you hold - AND - Go directly to Jail.\nIf you do not own any stock - you do not go to jail.\nPlay this card immediately.", "fjifs"],
		["Business Trip", "Take one Travel Voucher from the deck.\nPlay this card immediately.", "travvou"],
		["Hurricane makes landfall!", "Remove 1 House from each property in any player's 1 color group. (Downgrade Skyscrapers to Hotels; Hotels to 4 houses.)\nPlay this card immediately", "remhou"],
		["Make General Repairs to all your properties.", "$25 per House, Cab Stand, and Transit Station\n$100 per Hotel and Skyscraper.\nPlay this card immediately", "ppimp", [25,25,100]],
		["Property Taxes", "Pay $25 to the Pool for each unmortgaged property you own.\nPlay this card immediately.", "ppp", 25],
		["Assets Seized!", "Surrender any one undeveloped, unmortgaged property - or any one building to the Bank. If you do not own property - go directly to Jail.\nPlay this card immediately.", "surprop"]]
		
		self.chestDeck = [0,0,0,0,0,0,1,2,3,4,5,6,6,7,78,9,10,11,12,12,12,12,12,12,13,14,15,16,17,18,19,20,21,22,23,24,25,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57]
		
		self.chestCards = [["Advance to the Stock Exchange", "If you pass 'Pay Day' collect $300.\nPlay this card immediately.", "ast", [2,12]],
		["Advance to this Track's Pay Corner", "Collect your income from the Bank.\nOuter Track - 'Payday' - $400\nCenter Track - 'Go' - $200\nInner Track - 'Bonus' - $300\nPlay this card immediately.", "apc"],
		["Advance to Bonus", "Collect $300 from the Bank.\nPlay this card immediately.", "astcmb", [2,6], 300],
		["Shopping Spree", "Go directly to Rodeo Drive. Pay the Pool $150 for new clothes.\nPlay this card immediately.", "mdstpmp", [0,55], 150],
		["April 15, Taxes Due!", "Move directly to Income Tax, (do not pass any Pay Corner, do not collect any money), and pay the fine - OR - go directly to Jail.\nPlay this card immediately.", "mdstgtj", [1,4]],
		["Discount Travel", "Advance to the nearest unowned transit property (Railroad or Cab Co.) and buy it at 1/2 price (or put it up for auction).\nPlay this card immediately.", "mdn"],
		["Changing Lanes", "Move directly to the space that is 1 track below this one. If you are on the Outer Track, do nothing.\nPlay this card immediately.", "mdud", "up"],
		["Changing Lanes", "Move directly to the space that is 1 track above this one. If you are on the Inner Track, do nothing.\nPlay this card immediately.", "mdud", "down"],
		["A Moving Experience", "Move to Any Transportation Property (Railroad or Cab Co.) If Unowned, you may purchase it or put it up for auction. If Owned, pay rent.\nPlay this card immediately.", "mdcr"],
		["Go to Jail!", "Go directly to Jail. Do not pass any Pay Corner. Do not collect any money.\nPlay this card immediately.", "gtj"],
		["Get Out of Jail Free!", "Keep until needed. Play at any time on your turn. This card may be traded or sold.", "keep", "gojf"],
		["Just Say 'NO'!'", "Play at any time to stop another player's action against you.\nKeep until needed. Play at any time. This card may be traded or sold.", "keep", "jsn"],
		["Sale of Stock Bonus", "You may sell any one stock back to the bank for its value plus $50\nKeep until needed. Play at any time on your turn.", "keep", "ssp"],
		["Special Online Pricing", "The next time you land on anyone else's railroad, only pay 1/2 the rent.\nPlay this card the next time you land on someone's railroad.", "keep", "phr"],
		["Elected District Attorney", "Send any other player of your choice directly to jail.\nKeep until needed. Play at any time. This card may be traded or sold.", "keep", "apgtj"],
		["Renovation Success", "Collect $50 extra rent from the next player who lands on any of your properties.\nPlay this card the next time someone lands on your property.", "keep", "cexr"],
		["Deal Buster", "When another player is about to buy a property, play this card and buy it from the bank yourself.\nKeep until needed. Play at any time. This card may be traded or sold.", "keep", "cppur"],
		["Hostile Takeover", "Steal a property card from a player of your choice. It can't be part of a monopoly.\nKeep until needed. Play at any time on your turn. This card may be traded or sold.", "keep", "stealprop"],
		["Bargain Business!", "When you land on an unowned property you want, buy it for only $100.\nKeep until needed. Play at any time on your turn. This card may be traded or sold.", "keep", "buyfrx"],
		["Reverse Rent!", "Collect the rent due when you land on another player's property.\nKeep until needed. Play at any time on your turn. This card may be traded or sold.", "keep", "revren"],
		["The Rent is Too Darn High!", "Only pay $50 Rent to any owned property.\nKeep until needed. Play at any time on your turn. This card may be traded or sold.", "keep", "renisx"],
		["Insider Trading", "Pay 1/2 Par Value on your next stock purchase. (May NOT be used at auction.)\nKeep until needed. Play at any time. This card may be traded or sold.", "keep", "discstk"],
		["Lawyer on Retainer", "Avoid Stock Fine Penalties, 'See you in Court', or 'Caught Insider Trading' cards.\nKeep until needed. Play at any time. This card may be traded or sold.", "keep", "antifine"],
		["Share in their Good Fortune", "Take 1/2 of any player's Roll 3! winnings.\nKeep until needed. Play at any time. This card may be traded or sold.", "keep", "collr3"],
		["Insurance Premiums Due", "Pay $50 to the Pool.\nPlay this card immediately.", "pmp", 50],
		["Doctor's Fee", "Pay $50 to the Pool.\nPlay this card immediately.", "pmp", 50],
		["Pay Hospital Bills", "Pay $100 to the Pool.\nPlay this card immediately.", "pmp", 100],
		["Tech Bubble Bursts", "Pay $150 to the Pool.\nPlay this card immediately.", "pmp", 150],
		["Vehicle Impounded!", "Pay $50 to the Pool, move directly to 'Just Visiting' to pick up your car.\nLose 1 turn.\nPlay this card immediately.", "pmpmdstlt"],
		["You Inherit $100", "Collect $100 from the Bank.\nPlay this card immediately.", "cmb", 100],
		["Receive Consultancy Fee", "Collect $25 from the Bank\nPlay this card immediately.", "cmb", 25],
		["Bank Error in Your Favor!", "Collect $200 from the Bank.\nPlay this card immediately.", "cmb", 200],
		["Income Tax Refund!", "Collect $20 from the Bank.\nPlay this card immediately.", "cmb", 20],
		["You Won a Crossword Contest!", "Collect $100 from the Bank.\nPlay this card immediately.", "cmb", 100],
		["Life Insurance Matures", "Collect $20 from the Bank\nPlay this card immediately.", "cmb", 20],
		["You Win 2nd Place in a Board Game Remix Design Contest!", "Collect $10 form the Bank\nPlay this card immediately.", "cmb", 10],
		["Fluffy Takes First!", "Your pet wins the city pet show! Collect $75.\nPlay this card immediately.", "cmb", 75],
		["IPO", "Your company goes public.\nCollect $500 from the Bank.\nPlay this card immediately.", "cmb", 500],
		["Kickstart some Fun!", "Your idea for a variant of a classic board game grows from a hobby to a crowdfunded success story! Collect $200 from the Bank.\nPlay this card immediately.", "cmb", 200],
		["The Insider's Edge", "If you are on the Inner Track, collect $250 from the Bank. If the Outer Track, pay the Pool $50, if the Center Track, do nothing.\nPlay this card immediately.", "iftrkxcmbx", [250, 0, -50]],
		["Opening Night Tickets!", "You won tickets to the hottest show in town.\nSell them to each other player for $50.\n(Collect $50 from each player.)\nPlay this card immediately.", "cep", 50],
		["Happy Birthday!", "Collect $10 from each player, and move to the Birthday Gift space and follow the instructions.\nPlay this card immediately.", "cep", 10],
		["Entrepreneur of the Year!", "Collect $50 from each player in honor of your award.\nPlay this card immediately.", "cep", 50],
		["You're getting Married", "Collect $25 from each player as a wedding gift.\nPlay this card immediately.", "cep", 25],
		["Always Tip your Driver", "Pay $50 to all other players who own a Cab Co.\nPlay this card immediately.", "pepwithx", "cabco", 50],
		["Game Night!", "Pick an opponent. Both Roll. Highest-roller collects $200 from the Bank.\nPlay this card immediately.", "rcfl", 200],
		["Be Kind, Rewind", "Roll the dice again, move BACKWARDS that number of spaces. Pay double rent if you land on an owned space.\nPlay this card immediately.", "ramb"],
		["Inherit Stock", "You may chose any 1 share of any unpurchased stock to add to your portfolio.\nPlay this card immediately.", "freestk"],
		["Utility Regulation", "Stockholders in National Utilities must pay the Pool fines to Dividends.\nPlay this card immediately.", "findiv", ["national utilities"]],
		["Scandal in Hollywood!", "Stockholders in Motion Pictures and General Radio must pay the Pool fines to Dividends.\nPlay this card immediately.", "findiv", ["motion pictures", "general radio"]],
		["Unions on Strike", "Stockholders in United Railways, Acme Motors, and Allied Steamships must pay the Pool fines to Dividends.\nPlay this card immediately.", "findiv", ["united railways", "acme motors", "allied steamships"]],
		["Business Trip", "Draw 2 Travel Vouchers from the deck.\nPlay this card immediately.", "travvou", 2],
		["Business Trip", "Take one Travel Voucher from the deck.\nPlay this card immediately.", "travvou", 1],
		["Finders Keepers", "Take a Travel Vouchers from any player of your choice.\nPlay this card immediately.", "stealtrav"],
		["Losers Weepers", "Put 1 of your Travel Vouchers back on the deck.\nPlay this card immediately.", "losetrav"],
		["HOUSE CONDEMNED", "The city condemns one of your houses. Sell one house back to the Bank at 1/2 the price you paid for it. (Houses only. If you don't own any houses, do nothing.\nPlay this card immediately.", "sellhous"],
		["Tornado Hits!", "Remove one House from each property in any 1 of your color groups. (Downgrade Skyscrapers to Hotels; Hotels to 4 houses.)\nPlay this card immediately.", "remhou"],
		["Assessed for Street Repairs", "$25 per Cab Stand & Transit Station, $40 per House, $115 per Hotel, and $100 per Skyscraper.\nPlay this card immediately.", "ppimp"]]
		random.shuffle(self.chanceDeck)
		random.shuffle(self.chestDeck)
		
actionCards = aCardClass()


recentBankruptcyFlag = False

class tradeObject:
	def __init__(self, playerProposing, playerProposed):
		self.proposedBy = playerProposing
		self.proposedTo = playerProposed
		self.proposedByMoney = 0
		self.proposedToMoney = 0
		self.proposedByProps = []
		self.proposedToProps = []
		
	def viewTrade(self):
		print("The trade consists of:")
		print("From", self.proposedBy.PlayerName, "to", self.proposedTo.PlayerName)
		print(self.proposedByMoney, "dollars")
		if len(self.proposedByProps) > 0:
			for i in range(len(self.proposedByProps)):
				print(Gameboard.propList[self.proposedByProps[i]][0])
		print("From", self.proposedTo.PlayerName, "to", self.proposedBy.PlayerName)
		print(self.proposedToMoney, "dollars")
		if len(self.proposedToProps)> 0:
			for i in range(len(self.proposedToProps)):
				print(Gameboard.propList[self.proposedToProps[i]][0])
				
	def finalize(self):
		print(self.proposedBy.PlayerName, "gave", self.proposedByMoney, "dollars to", self.proposedTo.PlayerName)
		self.proposedBy.PlayerMoney = self.proposedBy.PlayerMoney - self.proposedByMoney
		self.proposedTo.PlayerMoney = self.proposedTo.PlayerMoney + self.proposedByMoney
		if len(self.proposedByProps) > 0:
			print(self.proposedBy.PlayerName, "gave the following properties to", self.proposedTo.PlayerName)
			for i in range(len(self.proposedByProps)):
				print(Gameboard.propList[self.proposedByProps[i]][0])
			for i in range(len(self.proposedByProps)):
				Gameboard.propList[self.proposedByProps[i]][2] = self.proposedTo.Playernumber
				self.proposedTo.OwnedProps.append(self.proposedByProps[i])
				self.proposedBy.OwnedProps.pop(self.proposedBy.OwnedProps.index(self.proposedByProps[i]))
		print(self.proposedTo.PlayerName, "gave", self.proposedToMoney, "dollars to", self.proposedBy.PlayerName)
		self.proposedTo.PlayerMoney = self.proposedTo.PlayerMoney - self.proposedToMoney
		self.proposedBy.PlayerMoney = self.proposedBy.PlayerMoney + self.proposedToMoney
		if len(self.proposedToProps) > 0:
			print(self.proposedTo.PlayerName, "gave the following properties to", self.proposedBy.PlayerName)
			for i in range(len(self.proposedToProps)):
				print(Gameboard.propList[self.proposedToProps[i]][0])
			for i in range(len(self.proposedToProps)):
				Gameboard.propList[self.proposedToProps[i]][2] = self.proposedBy.Playernumber
				self.proposedBy.OwnedProps.append(self.proposedToProps[i])
				self.proposedTo.OwnedProps.pop(self.proposedTo.OwnedProps.index(self.proposedToProps[i]))
		self.proposedBy.OwnedProps.sort()
		self.proposedTo.OwnedProps.sort()
		self.proposedBy.checkForCG()
		self.proposedTo.checkForCG()

def goToJail(token):
	token.IsInJail = True
	token.BoardPosition = [1,20]
	print("You have been placed in Jail")


def payCorner(cornerName, token):
	if cornerName == "Go":
		print("You have received 200 dollars for passing Go")
		token.PlayerMoney = token.PlayerMoney + 200
	if cornerName == "Bonus":
		if token.BoardPosition == [2,6]:
			print("You have received 300 dollars for landing on Bonus")
			token.PlayerMoney = token.PlayerMoney + 300
		else:
			print("You have received 250 dollars for passing Bonus")
			token.PlayerMoney = token.PlayerMoney + 250
	if cornerName == "Payday":
		if Dice.Sum() % 2 == 0:
			print("You have received 400 dollars for passing Payday")
			token.PlayerMoney = token.PlayerMoney + 400
		else:
			print("You have received 300 dollars for passing Payday")
			token.PlayerMoney = token.PlayerMoney + 300

def makeTrade(token):
	inputLoop = True
	while inputLoop == True:
		print("Making a trade")
		for i in range(len(listPlayers)):
			if listPlayers[i].Playernumber != token.Playernumber and listPlayers[i].isBankrupt == False:
				print("Player", listPlayers[i].Playernumber + 1, "is", listPlayers[i].PlayerName)
		response = input("Who would you like to trade with (enter player number)?")
		if response.isnumeric():
			response = int(response)
			if response < len(listPlayers) + 1 and response > 0:
				target = response - 1
				inputLoop = False
	Trade = tradeObject(token, listPlayers[target])
	tokenProps = []
	for i in range(len(token.OwnedProps)):
		if Gameboard.propList[token.OwnedProps[i]][1] == "CG":
			if Gameboard.propList[token.OwnedProps[i]][7] == 0:
				tokenProps.append(token.OwnedProps[i])
		else:
			tokenProps.append(token.OwnedProps[i])
	targetProps = []
	for i in range(len(listPlayers[target].OwnedProps)):
		if Gameboard.propList[listPlayers[target].OwnedProps[i]][1] == "CG":
			if Gameboard.propList[listPlayers[target].OwnedProps[i]][7] == 0:
				targetProps.append(listPlayers[target].OwnedProps[i])
		else:
			tokenProps.append(listPlayers[target].OwnedProps[i])
	inputLoop = True
	while inputLoop == True:
		Trade.viewTrade()
		print("Options:")
		print("(m1): Add or remove money from", token.PlayerName, "to", listPlayers[target].PlayerName)
		print("(m2): Add or remove money from", listPlayers[target].PlayerName, "to", token.PlayerName)
		print("(p1): Add or remove property from", token.PlayerName, "to", listPlayers[target].PlayerName)
		print("(p2): Add or remove property from", listPlayers[target].PlayerName, "to", token.PlayerName)
		print("(finalize): Attempt to finalize the trade as is")
		print("(cancel): Cancel trading and resume turn")
		responseTI = input("What would you like to do?)")
		if responseTI == "m1":
			print(token.PlayerName, "has", token.PlayerMoney, "dollars")
			addMoney = input("How much money would you like to add?")
			if addMoney.isnumeric():
				addMoney = int(addMoney)
				if addMoney <= token.PlayerMoney and addMoney > 0:
					Trade.proposedByMoney = Trade.proposedByMoney + addMoney
				elif addMoney < 0 and abs(addMoney) <= Trade.proposedByMoney:
					Trade.proposedByMoney = Trade.proposedByMoney + addMoney
				else:
					print("that was too much money")
			else:
				print("Invalid number")
		if responseTI == "m2":
			print(listPlayers[target].PlayerName, "has", listPlayers[target].PlayerMoney, "dollars")
			addMoney = int(input("How much money would you like to add?"))
			if addMoney.isnumeric():
				addMoney = int(addMoney)
				if addMoney <= listPlayers[target].PlayerMoney and addMoney > 0:
					Trade.proposedToMoney = Trade.proposedToMoney + addMoney
				elif addMoney < 0 and abs(addMoney) <= Trade.proposedToMoney:
					Trade.proposedToMoney = Trade.proposedToMoney + addMoney
				else:
					print("that was too much money")
			else:
				print("Invalid number")
		if responseTI == "p1":
			for i in range(len(tokenProps)):
				print(i+1,Gameboard.propList[tokenProps[i]][0])
			inputLoop1 = True
			print("Enter 'done' when you are finished adding properties")
			while inputLoop1 == True:
				responseAP = input("Enter the number of the property you would like to add:")
				if responseAP == "done":
					inputLoop1 == False
					break
				elif responseAP.isnumeric():
					if Trade.proposedByProps.count(tokenProps[int(responseAP) - 1]) == 0:
						Trade.proposedByProps.append(tokenProps[int(responseAP) - 1])
					else:
						Trade.proposedByProps.pop(Trade.proposedByProps.index(tokenProps[int(responseAP) - 1]))
				else:
					print("Invalid Input")
				Trade.viewTrade()
		if responseTI == "p2":
			for i in range(len(targetProps)):
				print(i+1,Gameboard.propList[targetProps[i]][0])
			inputLoop1 = True
			print("Enter 'done' when you are finished adding properties")
			while inputLoop1 == True:
				responseAP = input("Enter the number of the property you would like to add:")
				if responseAP == "done":
					inputLoop1 == False
					break
				elif responseAP. isnumeric():
					if Trade.proposedToProps.count(targetProps[int(responseAP) - 1]) == 0:
						Trade.proposedToProps.append(targetProps[int(responseAP) - 1])
					else:
						Trade.proposedToProps.pop(Trade.proposedToProps.index(targetProps[int(responseAP) - 1]))
				else:
					print("Invalid Input")
				Trade.viewTrade()
		if responseTI == "finalize":
			Trade.viewTrade()
			agreement = input("Do the parties agree to the trade?")
			if agreement == "yes":
				Trade.finalize()
				break
		if responseTI == "cancel":
			break

def stockExchangePass():
	pass

def moveToken(token, distance):
	#Normal movement
	oldPosition = [0,0]
	oldPosition[0] = token.BoardPosition[0]
	oldPosition[1] = token.BoardPosition[1]
	if distance % 2 == 1:
		token.BoardPosition[1] = token.BoardPosition[1] + distance
		if token.BoardPosition[0] == 0 and token.BoardPosition[1] > 55:
			token.BoardPosition[1] = token.BoardPosition[1] - 56
		if token.BoardPosition[0] == 1 and token.BoardPosition[1] > 39:
			token.BoardPosition[1] = token.BoardPosition[1] - 40
		if token.BoardPosition[0] == 2 and token.BoardPosition[1] > 23:
			token.BoardPosition[1] = token.BoardPosition[1] - 24
		if token.BoardPosition[0] == 0:
			if oldPosition[1] < 28 and oldPosition[1] + distance > 27:
				payCorner("Payday", token)
			if oldPosition[1] > 27 and oldPosition[1] + distance - 55 > 27:
				payCorner("Payday", token)
		if token.BoardPosition[0] == 1:
			if oldPosition[1] + distance > 39:
				payCorner("Go", token)
		if token.BoardPosition[0] == 2:
			if oldPosition[1] < 6 and oldPosition[1] + distance > 5:
				payCorner("Bonus", token)
			if oldPosition[1] > 5 and oldPosition[1] + distance - 23 > 5:
				payCorner("Bonus", token)
			if oldPosition[1] < 12 and oldPosition[1] + distance > 11:
				stockExchangePass()
			if oldPosition[1] > 11 and oldPosition[1] + distance - 23 > 11:
				stockExchangePass()
	else:
		while distance > 0:
			oldPosition = [0,0]
			oldPosition[0] = token.BoardPosition[0]
			oldPosition[1] = token.BoardPosition[1]
			if token.BoardPosition[0] == 0:
				if token.BoardPosition[1] > 34 and token.BoardPosition[1] + distance > 55:
					distance = distance - (56 - token.BoardPosition[1])
					token.BoardPosition[1] = 0
				if token.BoardPosition[1] < 7 and token.BoardPosition[1] + distance > 6:
					distance = distance - (7 - token.BoardPosition[1])
					token.BoardPosition = [1, 5]
				elif token.BoardPosition[1] > 6 and token.BoardPosition[1] < 35 and token.BoardPosition[1] + distance > 34:
					if oldPosition[1] < 28 and oldPosition[1] + distance > 27:
						payCorner("Payday", token)
					distance = distance - (35 - token.BoardPosition[1])
					token.BoardPosition = [1, 25]
				else:
					if oldPosition[1] < 28 and oldPosition[1] + distance > 27:
						payCorner("Payday", token)
					token.BoardPosition[1] = token.BoardPosition[1] + distance
					distance = 0
			elif token.BoardPosition[0] == 1:
				if token.BoardPosition[1] > 34 and token.BoardPosition[1] + distance > 39:
					payCorner("Go", token)
					distance = distance - (40 - token.BoardPosition[1])
					token.BoardPosition[1] = 0
				if token.BoardPosition[1] < 5 and token.BoardPosition[1] + distance > 4:
					distance = distance - (5 - token.BoardPosition[1])
					token.BoardPosition = [0, 7]
				elif token.BoardPosition[1] > 4 and token.BoardPosition[1] < 15 and token.BoardPosition[1] + distance > 14:
					distance = distance - (15 - token.BoardPosition[1])
					token.BoardPosition = [2, 9]
				elif token.BoardPosition[1] > 14 and token.BoardPosition[1] < 25 and token.BoardPosition[1] + distance > 24:
					distance = distance - (25 - token.BoardPosition[1])
					token.BoardPosition = [0, 35]
				elif token.BoardPosition[1] > 24 and token.BoardPosition[1] < 35 and token.BoardPosition[1] + distance > 34:
					distance = distance - (35 - token.BoardPosition[1])
					token.BoardPosition = [2, 21]
				else:
					token.BoardPosition[1] = token.BoardPosition[1] + distance
					distance = 0
			elif token.BoardPosition[0] == 2:
				if token.BoardPosition[1] > 20 and token.BoardPosition[1] + distance > 23:
					distance = distance - (24 - token.BoardPosition[1])
					token.BoardPosition[1] = 0
				if token.BoardPosition[1] < 9 and token.BoardPosition[1] + distance > 8:
					if oldPosition[1] < 6 and oldPosition[1] + distance > 5:
						payCorner("Bonus", token)
					distance = distance - (9 - token.BoardPosition[1])
					token.BoardPosition = [1, 15]
				elif token.BoardPosition[1] > 8 and token.BoardPosition[1] < 21 and token.BoardPosition[1] + distance > 20:
					if oldPosition[1] < 12 and oldPosition[1] + distance > 11:
						stockExchangePass()
					distance = distance - (21 - token.BoardPosition[1])
					token.BoardPosition = [1, 35]
				else:
					if oldPosition[1] < 6 and oldPosition[1] + distance > 5:
						payCorner("Bonus", token)
					if oldPosition[1] < 12 and oldPosition[1] + distance > 11:
						stockExchangePass()
					token.BoardPosition[1] = token.BoardPosition[1] + distance
					distance = 0

def numberOwned(creditor, propType):
	count = 0
	for i in range(len(creditor.OwnedProps)):
		if Gameboard.propList[creditor.OwnedProps[i]][1] == propType:
			count = count + 1
	return count
	
def improveProps(token):
	count = 1
	for i in token.ownedColorGroups:
		if token.ownedColorGroups[i][0] > 0:
			print(count, i)
			count = count + 1
	inputLoop = True
	while inputLoop == True:
		response = input("Which color group would you like to improve?")
		if response in token.ownedColorGroups:
			if token.ownedColorGroups[response][0] > 0:
				inputLoop = False
			else:
				print("That color group cannot be improved right now")
		else:
			print("That doesn't appear to be the name of a color group that you own.")
	inputLoop = True
	propsToImprove = token.ownedColorGroups[response][1]
	while inputLoop == True:
		minimumImpLevel = 7
		for i in range(len(propsToImprove)):
			if Gameboard.propList[propsToImprove[i]][7] < minimumImpLevel:
				minimumImpLevel = Gameboard.propList[propsToImprove[i]][7]
		for i in range(len(propsToImprove)):
			if Gameboard.propList[propsToImprove[i]][7] == minimumImpLevel and Gameboard.propList[propsToImprove[i]][7] < 7:
				print(i + 1, Gameboard.propList[propsToImprove[i]][0])
		print("Enter 'done' to quit, or")
		response = input("Enter the number of the property you would like to improve:")
		if response == "done":
			inputLoop = False
		elif response.isnumeric():
			response = int(response)
			if response > 0 and response - 1 < len(propsToImprove):
				if Gameboard.propList[propsToImprove[response - 1]][7] == minimumImpLevel and Gameboard.propList[propsToImprove[i]][7] < 7:
					if token.PlayerMoney > Gameboard.propList[propsToImprove[response - 1]][10]:
						token.PlayerMoney = token.PlayerMoney - Gameboard.propList[propsToImprove[response - 1]][10]
						Gameboard.propList[propsToImprove[response - 1]][7] = Gameboard.propList[propsToImprove[response - 1]][7] + 1
						print("You paid", Gameboard.propList[propsToImprove[response - 1]][10], "dollars to the bank")
						print(Gameboard.propList[propsToImprove[response - 1]][0], "is improved to level", Gameboard.propList[propsToImprove[response - 1]][7])
					else:
						print("You don't have enough money to do that.")
				else:
					print("Improvements to that property would not satisfy the build evenly rule, or else the property is already improved to max level")
			else:
				print("Invalid response.")
		else:
			print("Invalid response.")
		
def purchaseFromBank(token, coords):
	token.PlayerMoney = token.PlayerMoney - Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][3]
	Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2] = token.Playernumber
	token.OwnedProps.append(Gameboard.propNum[coords[0]][coords[1]])
	token.OwnedProps.sort()
	token.checkForCG()

def auctioneer(propNumber):
	print("The property", Gameboard.propList[propNumber][0], "is going up for Auction")
	highBid = 0
	biddersList = []
	biddersBidsList = []
	biddersActiveList = []
	for i in range(len(listPlayers)):
		if listPlayers[i].isBankrupt == False and listPlayers[i].IsInJail == False:
			biddersList.append(i)
			biddersBidsList.append(0)
			biddersActiveList.append(True)
	auctionContinues = True
	while auctionContinues == True:
		print("The current high bid is", highBid, "dollars")
		for i in range(len(biddersList)):
			if biddersActiveList[i] == True:
				inputLoop = True
				while inputLoop == True:
					print(listPlayers[biddersList[i]].PlayerName, "you have", listPlayers[biddersList[i]].PlayerMoney, "dollars and your current bid is", biddersBidsList[i], "dollars")
					response = input("To drop out, enter a bid lower than your current bid. What would you like to bid?")
					if response.isnumeric():
						response = int(response)
						if response < biddersBidsList[i]:
							biddersActiveList[i] = False
						elif listPlayers[biddersList[i]].PlayerMoney >= response:
							biddersBidsList[i] = response
						inputLoop = False
		highBid = sorted(biddersBidsList, reverse=True)[0]
		highBidder = biddersList[biddersBidsList.index(highBid)]
		if biddersActiveList.count(True) < 2:
			auctionContinues = False
	print(listPlayers[highBidder].PlayerName, "has purchased", Gameboard.propList[propNumber][0], "at auction for", highBid, "dollars")
	listPlayers[highBidder].PlayerMoney = listPlayers[highBidder].PlayerMoney - highBid
	Gameboard.propList[propNumber][2] = listPlayers[highBidder].Playernumber
	listPlayers[highBidder].OwnedProps.append(propNumber)
	listPlayers[highBidder].OwnedProps.sort()
	listPlayers[highBidder].checkForCG()
		

def declareBankruptcy(token, creditor):
	if creditor == "bank":
		for i in range(len(token.OwnedProps)):
			Gameboard.propList[token.OwnedProps[i]][2] = 0
		print(token.PlayerName, "has declared bankruptcy to the Bank")
		token.isBankrupt = True
	else:
		listPlayers[creditor].PlayerMoney = listPlayers[creditor].PlayerMoney + token.PlayerMoney
		for i in range(len(token.OwnedProps)):
			Gameboard.propList[token.OwnedProps[i]][2] = listPlayers[creditor].Playernumber
		print(listPlayers[creditor].OwnedProps)
		print(token.OwnedProps)
		listPlayers[creditor].OwnedProps.extend(token.OwnedProps)
		print(listPlayers[creditor].OwnedProps)
		listPlayers[creditor].OwnedProps.sort()
		target = token.Playernumber
		token.isBankrupt = True
	recentBankruptcyFlag = True

def checkForWinner():
	activePlayers = 0
	winner = 0
	for i in range(len(listPlayers)):
		if listPlayers[i].isBankrupt == False:
			activePlayers = activePlayers + 1
		print(activePlayers)
	if i > 1:
		print("returnFalse")
		return -1
	else:
		for i in range(len(listPlayers)):
			if listPlayers[i].isBankrupt == False:
				winner = i
		print("return", winner)
		return winner

def payRentTo(token, rent, landlord):
	paymentComplete = False
	while paymentComplete == False:
		if token.PlayerMoney > rent:
			token.PlayerMoney = token.PlayerMoney - rent
			listPlayers[landlord].PlayerMoney = listPlayers[landlord].PlayerMoney + rent
			print("You paid", rent, "dollars to", listPlayers[landlord].PlayerName)
			paymentComplete = True
		else:
			inputLoop = True
			print("You do not have enough money for rent")
			while inputLoop == True:
				print("Attempt a (t)rade")
				print("(M)ortgage propery")
				print("(S)ell improvements")
				print("Declare (b)ankruptcy")
				response = input("What would you like to do?")
				if response == "b":
					declareBankruptcy(token, landlord)
					inputLoop = False
					paymentComplete = True
		
			
def payFineToPool(token, fine):
	paymentComplete = False
	while paymentComplete == False:
		if token.PlayerMoney > fine:
			token.PlayerMoney = token.PlayerMoney - fine
			Gameboard.poolMoney = Gameboard.poolMoney + fine
			print("You paid", fine, "dollars to the Pool")
			paymentComplete = True
		else:
			inputLoop = True
			print("You do not have enough money for your fine")
			while inputLoop == True:
				print("Attempt a (t)rade")
				print("(M)ortgage propery")
				print("(S)ell improvements")
				print("Declare (b)ankruptcy")
				response = input("What would you like to do?")
				if response == "b":
					declareBankruptcy(token, "bank")
					inputLoop = False
					paymentComplete = True

def landOnProperty(token, coords):
	if Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2] == "bank":
		print("The bank owns", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][0])
		inputLoop = True
		while inputLoop == True:
			print("The price for this property is", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][3])
			if token.PlayerMoney > Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][3]:
				print("You have enough money to (p)urchase this property")
			print("Or you may (a)uction it")
			response = input("What would you like to do?")
			if token.PlayerMoney > Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][3] and response == "p":
				purchaseFromBank(token, coords)
				inputLoop = False
			if response == "a":
				auctioneer(Gameboard.propNum[coords[0]][coords[1]])
				inputLoop = False
	elif Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2] == token.Playernumber:
		print("You already own", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][0])
	else:
		if Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][1] == "CG":
			print("Player", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2] + 1, ",", listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]].PlayerName, "owns", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][0])
			if listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]].ownedColorGroups[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][5]][0] == 0:
				print(listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]].PlayerName, "does not have majority ownership, the rent is", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][8][0], "dollars.")
				payRentTo(token, Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][8][0], Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2])
			elif Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][7] > 0:
				print(listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]].PlayerName, "owns", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][7], "improvement(s) on this property, the rent is", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][8][Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][7]], "dollars.")
				payRentTo(token, Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][8][Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][7]], Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2])
			else:
				print(listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]].PlayerName, "owns a majority, the rent is doubled from", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][8][0], "dollars.")
				payRentTo(token, Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][8][0] * 2, Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2])
		if Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][1] == "CabCo":
			count = numberOwned(listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]], "CabCo")
			print("Player", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2] + 1, ",", listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]].PlayerName, "owns", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][0])
			print(listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]].PlayerName, "owns", count, "Cab Companies, the rent is", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][5][count - 1], "dollars.")
			payRentTo(token, Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][5][count - 1], Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2])
		if Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][1] == "Railroad":
			count = numberOwned(listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]], "Railroad")
			print("Player", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2] + 1, ",", listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]].PlayerName, "owns", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][0])
			print(listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]].PlayerName, "owns", count, "Railroads, the rent is", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][5][count - 1], "dollars.")
			payRentTo(token, Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][5][count - 1], Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2])
		if Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][1] == "Utility":
			count = numberOwned(listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]], "Utility")
			Dice.Roll()
			print("Player", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2] + 1, ",", listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]].PlayerName, "owns", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][0])
			print(listPlayers[Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2]].PlayerName, "owns", count, ", the rent is", Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][5][count - 1], "times", Dice.Sum(), ",", Dice.Sum() * Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][5][count - 1], "dollars")
			payRentTo(token, Dice.Sum() * Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][5][count - 1], Gameboard.propList[Gameboard.propNum[coords[0]][coords[1]]][2])
	
	
def moveDirectly(token, coords):
	token.BoardPosition = coords
	print(token.PlayerName, "moved directly to", Gameboard.ref(token.BoardPosition))
	landOnSpace(token, coords)
	
def readActionCard(pulledCard, token, coords):
	print(f"\n")
	print(pulledCard[0])
	print(pulledCard[1])
	cardType = pulledCard[2]
	if cardType == "ast":
	#advance to single target
		pass
	elif cardType == "apc":
	#advance to pay corner
		pass
	elif cardType == "atn":
	#advance to nearest
		pass
	elif cardType == "atcsp":
	#advance to choice and steal or purchase
		pass
	elif cardType == "astpep":
	#advance to single target and pay every player
		pass
	elif cardType == "astcmb":
	#advance to single target and collect
		pass
	elif cardType == "mdst":
	#move directly to single target
		moveDirectly(token, pulledCard[3])
	elif cardType == "mdstpmp":
	#move directly to single target and pay to pool
		pass
	elif cardType == "mdstgtj":
	#move directly to single target or go to jail
		pass
	elif cardType == "amdst":
		pass
	elif cardType == "mdn":
		pass
	elif cardType == "mdud":
		pass
	elif cardType == "mdc":
		pass
	elif cardType == "mdcr":
		pass
	elif cardType == "gtj":
		goToJail(token)
	elif cardType == "gtjnr":
		pass
	elif cardType == "keep":
		pass
	elif cardType == "pmp":
	#pay money to the pool
		payFineToPool(token, pulledCard[3])
	elif cardType == "pmpmdstlt":
	#pay money to the pool and move directly to a single target and lose 1 turn
		pass
	elif cardType == "cmb":
	#collect money from the bank
		print("You collected", pulledCard[3], "from the bank")
		token.PlayerMoney = token.PlayerMoney + pulledCard[3]
	elif cardType == "iftrkxcmbx":
		pass
	elif cardType == "cep":
		pass
	elif cardType == "ccpc":
		pass
	elif cardType == "pep":
		pass
	elif cardType == "ifxpep":
		pass
	elif cardType == "pepwithx":
		pass
	elif cardType == "rcfl":
		pass
	elif cardType == "mxs":
		pass
	elif cardType == "ram":
		pass
	elif cardType == "retstk":
		pass
	elif cardType == "freestk":
		pass
	elif cardType == "reddiv":
		pass
	elif cardType == "coldiv":
		pass
	elif cardType == "fjifs":
		pass
	elif cardType == "travvou":
		pass
	elif cardType == "stealtrav":
		pass
	elif cardType == "losetrav":
		pass
	elif cardType == "remhou":
		pass
	elif cardType == "ppimp":
		pass
	elif cardType == "ppp":
		pass
	elif cardType == "surprop":
		pass
	
def pullChanceCard(token, coords):
	pulledCard = actionCards.chanceCards[actionCards.chanceDeck[0]]
	readActionCard(pulledCard, token, coords)
	actionCards.chanceDeck.append(actionCards.chanceDeck[0])
	actionCards.chanceDeck.pop(0)
	
def pullCommChestCard(token, coords):
	pulledCard = actionCards.chestCards[actionCards.chestDeck[0]]
	readActionCard(pulledCard, token, coords)
	actionCards.chestDeck.append(actionCards.chestDeck[0])
	actionCards.chestDeck.pop(0)
	
def listAssets(token):
	print("")
	print(token.PlayerName, "has", token.PlayerMoney, "dollars")
	propsPrinted = 0
	for i in range(len(token.OwnedProps)):
		if Gameboard.propList[token.OwnedProps[i]][1] == "CG":
			if propsPrinted > 0:
				print(" || ", end="")
			print(Gameboard.propList[token.OwnedProps[i]][0], end="")
			propsPrinted = propsPrinted + 1
			if token.ownedColorGroups[Gameboard.propList[token.OwnedProps[i]][5]][0] > 0 and Gameboard.propList[token.OwnedProps[i]][7] == 0:
				print(", improvable", end="")
			elif token.ownedColorGroups[Gameboard.propList[token.OwnedProps[i]][5]][0] > 0 and Gameboard.propList[token.OwnedProps[i]][7] > 0 and Gameboard.propList[token.OwnedProps[i]][7] < 5:
				print(",", Gameboard.propList[token.OwnedProps[i]][7], "houses", end="")
			elif token.ownedColorGroups[Gameboard.propList[token.OwnedProps[i]][5]][0] > 0 and Gameboard.propList[token.OwnedProps[i]][7] == 5:
				print(",", "hotel", end="")
			elif token.ownedColorGroups[Gameboard.propList[token.OwnedProps[i]][5]][0] > 0 and Gameboard.propList[token.OwnedProps[i]][7] == 6:
				print(",", "skyscraper", end="")
		if i == len(token.OwnedProps) - 1 and propsPrinted > 0:
			print("")
	propsPrinted = 0
	for i in range(len(token.OwnedProps)):
		if Gameboard.propList[token.OwnedProps[i]][1] == "Railroad":
			if propsPrinted > 0:
				print(" || ", end="")
			print(Gameboard.propList[token.OwnedProps[i]][0], end="")
			propsPrinted = propsPrinted + 1
		if i == len(token.OwnedProps) - 1 and propsPrinted > 0:
			print("")
	propsPrinted = 0
	for i in range(len(token.OwnedProps)):
		if Gameboard.propList[token.OwnedProps[i]][1] == "Utility":
			if propsPrinted > 0:
				print(" || ", end="")
			print(Gameboard.propList[token.OwnedProps[i]][0], end="")
			propsPrinted = propsPrinted + 1
		if i == len(token.OwnedProps) - 1 and propsPrinted > 0:
			print("")
	propsPrinted = 0
	for i in range(len(token.OwnedProps)):
		if Gameboard.propList[token.OwnedProps[i]][1] == "CabCo":
			if propsPrinted > 0:
				print(" || ", end="")
			print(Gameboard.propList[token.OwnedProps[i]][0], end="")
			propsPrinted = propsPrinted + 1
		if i == len(token.OwnedProps) - 1 and propsPrinted > 0:
			print("")
		#print(Gameboard.propList[token.OwnedProps[i]][0], end=" ")
	
def landOnSpace(token, coords):
	if Gameboard.spaceType[coords[0]][coords[1]] == "Property":
		landOnProperty(token, coords)
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Chance":
		pullChanceCard(token, coords)
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Community Chest":
		pullCommChestCard(token, coords)
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Auction":
		pass
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Bus Ticket":
		pass
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Free Parking":
		pass
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Holland Tunnel":
		if token.BoardPosition == [0,14]:
			token.BoardPosition = [2,18]
			print("Took Holland Tunnel from the Outer track to the Inner track")
		elif token.BoardPosition == [2,18]:
			token.BoardPosition = [0,14]
			print("Took Holland Tunnel from the Inner track to the Outer track")
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Paycorner":
		pass
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Subway":
		pass
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Birthday Gift":
		pass
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Income Tax":
		inputLoop = True
		while inputLoop == True:
			print("You have landed on Income Tax, you must either:")
			print("Pay fine to pool equal to 10% the value of all your assets, (pay10), or")
			print("Pay a fine to the pool of 200 dollars (pay200)")
			response = input("What would you like to do?")
			if response == "pay10":
				assetValue = token.PlayerMoney
				for i in range(len(token.OwnedProps)):
					if Gameboard.propList[token.OwnedProps[i]][1] == "CG":
						assetValue = assetValue + Gameboard.propList[token.OwnedProps[i]][9]
						assetValue = assetValue + Gameboard.propList[token.OwnedProps[i]][7] * Gameboard.propList[token.OwnedProps[i]][10]
					else:
						assetValue = assetValue + Gameboard.propList[token.OwnedProps[i]][6]
				print("Your fine is", int(assetValue * 0.1), "dollars")
				payFineToPool(token, int(assetValue * 0.1))
				inputLoop = False
			if response == "pay200":
				payFineToPool(token, 200)
				inputLoop = False
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Roll Three":
		pass
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Jail":
		pass
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Squeeze Play":
		pass
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Luxury Tax":
		print("Your have landed on Luxury Tax, you must pay 75 dollars to the pool.")
		payFineToPool(token, 75)
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Go to Jail":
		goToJail(token)
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Stock Exchange":
		pass
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Tax Refund":
		pass
	elif Gameboard.spaceType[coords[0]][coords[1]] == "Reverse Direction":
		pass
		
def setUpNewGame():
	inputLoop = True
	while inputLoop:
		playerNum = input("How many players?")
		if playerNum.isnumeric():
			playerNum = int(playerNum)
			if playerNum < 2:
				print("Must be a minimum of 2 players.")
			else:
				inputLoop = False
		else:
			print("Please enter a number")
	for i in range(playerNum):
		listPlayers.append(Player(input(f"Player {i+1} name?"),i))
def readSaveFile():
	savFile = open("ultimate_game.sav", "r")
	global resumeCurrentPlayer
	resumeCurrentPlayer = json.loads(savFile.readline())
	global resumeEndTurn
	resumeEndTurn = json.loads(savFile.readline())
	playerNum = json.loads(savFile.readline())
	for i in range(playerNum):
		readNumber = json.loads(savFile.readline())
		if readNumber != i:
			print("Something is probably wrong")
		playerNameFile = json.loads(savFile.readline())
		listPlayers.append(Player(playerNameFile, i))
		listPlayers[i].BoardPosition = json.loads(savFile.readline())
		listPlayers[i].PlayerMoney = json.loads(savFile.readline())
		listPlayers[i].OwnedProps = json.loads(savFile.readline())
		for j in range(len(listPlayers[i].OwnedProps)):
			Gameboard.propList[listPlayers[i].OwnedProps[j]][2] = listPlayers[i].Playernumber
		print(listPlayers[i].OwnedProps)
		listPlayers[i].IsInJail = json.loads(savFile.readline())
		listPlayers[i].turnsInJail = json.loads(savFile.readline())
		listPlayers[i].isBankrupt = json.loads(savFile.readline())
		listPlayers[i].travelVouchers = json.loads(savFile.readline())
		listPlayers[i].heldActionCards = json.loads(savFile.readline())
		listPlayers[i].rollThreeCards = json.loads(savFile.readline())
		listPlayers[i].ownedColorGroups = json.loads(savFile.readline())
		listPlayers[i].ownsImprovableCG = json.loads(savFile.readline())
	savFile.close()

gameloop = True
listPlayers = []
resumingFromFile = False

if exists("ultimate_game.sav"):
	response = input("A save file exists, would you like to load it(y/n)?")
	if response == "y" or response == "Y" or response == "yes":
		readSaveFile()
		resumingFromFile = True
	else:
		setUpNewGame()
else:
	setUpNewGame()

if os.name == "nt":
	pass
	#os.system('cls')
else:
	os.system('clear')
isTurn = True
rollDoublesCount = 0

while gameloop == True:
	for currentPlayer in range(len(listPlayers)):
		if resumingFromFile == True and currentPlayer < resumeCurrentPlayer:
			print("debug 1")
			continue
		print("debug 2")
		endTurn = False
		if resumingFromFile == True:
			endTurn = resumeEndTurn
			resumingFromFile = False
			print("debug 3")
		isTurn = True
		if listPlayers[currentPlayer].isBankrupt == False:
			while isTurn == True:
				print("\nPlayer", currentPlayer+1, "is", listPlayers[currentPlayer].PlayerName)
				#print("You have", listPlayers[currentPlayer].PlayerMoney, "dollars and ", len(listPlayers[currentPlayer].OwnedProps), "properties")
				listAssets(listPlayers[currentPlayer])
				print("You are currently on", Gameboard.ref(listPlayers[currentPlayer].BoardPosition))
				if listPlayers[currentPlayer].IsInJail == True:
					print("You are in Jail, this is your", listPlayers[currentPlayer].turnsInJailString(), "in Jail")
				print("\nOptions:")
				if endTurn == False and listPlayers[currentPlayer].IsInJail == False:
					print("(R)oll the dice and move")
					print("Use a (b)us ticket")
				if endTurn == False and listPlayers[currentPlayer].IsInJail == True:
					print("Roll for (d)oubles")
					print("Pay fine (50)")
				print("(V)iew your assets")
				if listPlayers[currentPlayer].ownsImprovableCG == True:
					print("(I)mprove a property")
				print("(T)rade with another player")
				if endTurn == True:
					print("(E)nd turn")
				print("E(x)it the game")
				response = input("What would you like to do?")
				if response == "cheat":
					print("Cheats Menu")
					cheating = input("?")
					if cheating == "b":
						creditor = int(input("creditor"))
						declareBankruptcy(listPlayers[currentPlayer], creditor)
					if cheating == "roll":
						forceRoll = int(input("roll"))
						moveToken(listPlayers[currentPlayer], forceRoll)
						print("Player", listPlayers[currentPlayer].PlayerName, "cheated a", forceRoll, "and landed on", Gameboard.ref(listPlayers[currentPlayer].BoardPosition))
						landOnSpace(listPlayers[currentPlayer], listPlayers[currentPlayer].BoardPosition)
						endTurn = True
					if cheating == "property":
						print(Gameboard.propList[int(input("?"))])
					if cheating == "chance":
						cardToRead = int(input("card"))
						readActionCard(actionCards.chanceCards[cardToRead], listPlayers[currentPlayer], listPlayers[currentPlayer].BoardPosition)
					if cheating == "chest":
						cardToRead = int(input("card"))
						readActionCard(actionCards.chestCards[cardToRead], listPlayers[currentPlayer], listPlayers[currentPlayer].BoardPosition)
				if response == "i" and listPlayers[currentPlayer].ownsImprovableCG == True:
					improveProps(listPlayers[currentPlayer])
				if response == "r" and endTurn == False and listPlayers[currentPlayer].IsInJail == False:
					Dice.State = Dice.Roll()
					if Dice.State[0] == Dice.State[1] and rollDoublesCount == 2:
						goToJail(listPlayers[currentPlayer])
					moveToken(listPlayers[currentPlayer], Dice.Sum())
					print("Player", listPlayers[currentPlayer].PlayerName,"rolled a", Dice.State[0], "and a", Dice.State[1], "and landed on", Gameboard.ref(listPlayers[currentPlayer].BoardPosition))
					landOnSpace(listPlayers[currentPlayer], listPlayers[currentPlayer].BoardPosition)
					if Dice.State[0] == Dice.State[1] and rollDoublesCount < 2:
						rollDoublesCount = rollDoublesCount + 1
					else:
						rollDoublesCount = 0
						endTurn = True
				if response == "d" and endTurn == False and listPlayers[currentPlayer].IsInJail == True and listPlayers[currentPlayer].turnsInJail < 2:
					#roll for doubles
					Dice.State = Dice.Roll()
					if Dice.State[0] == Dice.State[1]:
						listPlayers[currentPlayer].IsInJail = False
						listPlayers[currentPlayer].turnsInJail = 0
					else:
						endTurn = True
					pass
				if response == "50" and endTurn == False and listPlayers[currentPlayer].IsInJail == True:
					#pay50
					payFineToPool(listPlayers[currentPlayer], 50)
					listPlayers[currentPlayer].IsInJail = False
					listPlayers[currentPlayer].turnsInJail = 0
				if response == "v":
					listAssets(listPlayers[currentPlayer])
				if response == "t":
					makeTrade(listPlayers[currentPlayer])
				if listPlayers[currentPlayer].isBankrupt == True:
					print(listPlayers[currentPlayer].PlayerName, "has gone bankrupt")
					isItTheEnd = checkForWinner()
					if isItTheEnd != -1:
						print(listPlayers[isItTheEnd].PlayerName, "is the last solvent player and wins the Game")
						gameloop = False
						break
					isTurn = False
				if response == "e" and endTurn == True:
					if os.name == "nt":
						os.system('cls')
					else:
						os.system('clear')
					isTurn = False
				if response == "x":
					gameloop = False
					break
		if recentBankruptcyFlag == True:
			break
		if gameloop == False:
			break
savFile = open("ultimate_game.sav", "w")
json.dump(currentPlayer, savFile)
savFile.write("\n")
json.dump(endTurn, savFile)
savFile.write("\n")
json.dump(len(listPlayers), savFile)
savFile.write("\n")
for i in range(len(listPlayers)):
	json.dump(listPlayers[i].Playernumber, savFile)
	savFile.write("\n")
	json.dump(listPlayers[i].PlayerName, savFile)
	savFile.write("\n")
	json.dump(listPlayers[i].BoardPosition, savFile)
	savFile.write("\n")
	json.dump(listPlayers[i].PlayerMoney, savFile)
	savFile.write("\n")
	json.dump(listPlayers[i].OwnedProps, savFile)
	savFile.write("\n")
	json.dump(listPlayers[i].IsInJail, savFile)
	savFile.write("\n")
	json.dump(listPlayers[i].turnsInJail, savFile)
	savFile.write("\n")
	json.dump(listPlayers[i].isBankrupt, savFile)
	savFile.write("\n")
	json.dump(listPlayers[i].travelVouchers, savFile)
	savFile.write("\n")
	json.dump(listPlayers[i].heldActionCards, savFile)
	savFile.write("\n")
	json.dump(listPlayers[i].rollThreeCards, savFile)
	savFile.write("\n")
	json.dump(listPlayers[i].ownedColorGroups, savFile)
	savFile.write("\n")
	json.dump(listPlayers[i].ownsImprovableCG, savFile)
	savFile.write("\n")

savFile.close()
print("Thank you for playing Ultimate Monopoly")
