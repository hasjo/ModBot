#This is a sample module, meant as the basis for creating a new module

# The module needs a Dictionary of the command that can be run, and the name of the module.
# The logic for needing the module name is that the main program will run the receiving program
# on the module and the module will handle the input and return the message or do what is needed
CommandDict = {"!weak":"PokeBot", "!resist":"PokeBot","!type":"PokeBot","!item":"PokeBot","!pokemon":"PokeBot"}

#This tells the main program what commands the module is looking for and the name of the module
def GiveDict():
    return CommandDict

#This function is what the main program calls to execute the command
def ReceiveMsg(command):
    import sqlite3
    
    sqliteconn = sqlite3.connect('/home/jordan/Git/pokedex/pokedex/data/pokedex.sqlite')
    
    print(command + " - PokeBot")
    #I used find so you could potentially use arguments
    if command.find("!weak") != -1:
        workstring = command.partition("!weak ")[2]
        inpstring = workstring.partition(" ")[0].lower()
        NewList = []
        NewList.append(inpstring)
        while workstring.partition(" ")[2] != "":
            workstring = workstring.partition(" ")[2]
            inpstring = workstring.partition(" ")[0].lower()
            NewList.append(inpstring)
        maxtup = len(NewList)
        ReturnMSG = weakto(NewList)
        return ReturnMSG
    if command.find("!resist") != -1:
        workstring = command.partition("!resist ")[2]
        inpstring = workstring.partition(" ")[0].lower()
        NewList = []
        NewList.append(inpstring)
        while workstring.partition(" ")[2] != "":
            workstring = workstring.partition(" ")[2]
            inpstring = workstring.partition(" ")[0].lower()
            NewList.append(inpstring)
        maxtup = len(NewList)
        ReturnMSG = resistantto(NewList)
        return ReturnMSG
    if command.find("!item ") != -1:
        workstring = command
        workstring = workstring.partition("!item ")[2]
        return itemsearch(workstring, sqliteconn)
    if command.find("!pokemon ") != -1:
        #Do Things
        workstring = command
        workstring = workstring.partition("!pokemon ")[2]
        return pokesearch(workstring, sqliteconn)
    if command.find("!type ") != -1:
        workstring = command
        workstring = workstring.partition("!type ")[2]
        inpstring = workstring.partition(" ")[0]
        NewList = []
        NewList.append(inpstring)
        while workstring.partition(" ")[2] != "":
            workstring = workstring.partition(" ")[2]
            inpstring = workstring.partition(" ")[0]
            NewList.append(inpstring)
        maxtup = len(NewList)
        #for x in range(0,maxtup):
            #print(NewList[x])
        OutString = []
        OutString.append(weakto(NewList))
        OutString.append(resistantto(NewList))
        return OutString

def pokesearch(poke, conn):
    poke = poke.lower()
    poke = poke.replace(" ", "-")

    pokeid = ""
    Type1id = ""
    Type2id = ""
    Type1Name = ""
    Type2Name = ""

    HP = ""
    Atk = ""
    Def = ""
    SpA = ""
    SpD = ""
    Spe = ""

    c = conn.cursor()

    outstring = str(poke).title()

    try:
        c.execute('SELECT id FROM pokemon WHERE identifier = \'' + poke + "\'")
    except:
        return "Error in search"
    for row in c:
         row = row[0]
         pokeid = row
         #print(row)

    c.execute('SELECT base_stat FROM pokemon_stats WHERE pokemon_id = \'' + str(pokeid) + "\'")
    x = 0
    for row in c:
        row = row[0]
        if x == 0:
            HP = row
        elif x == 1:
            Atk = row
        elif x == 2:
            Def = row
        elif x == 3:
            SpA = row
        elif x == 4:
            SpD = row
        elif x == 5:
            Spe = row
        x += 1

    c.execute('SELECT type_id FROM pokemon_types WHERE pokemon_id = \'' + str(pokeid) + "\'")
    x = 0
    for row in c:
        row = row[0]
        if x == 0:
            Type1id = row
        if x == 1:
            Type2id = row
        x += 1

    c.execute("SELECT name FROM type_names WHERE type_id = \'" + str(Type1id) + "\'" + "and local_language_id = \'9\'")
    for row in c:
        Type1Name = row[0]

    c.execute("SELECT name FROM type_names WHERE type_id = \'" + str(Type2id) + "\'" + "and local_language_id = \'9\'")
    for row in c:
        Type2Name = row[0]

    OutString = poke.title() + " - " + Type1Name
    if Type2Name != "":
        OutString = OutString + " " + Type2Name + " - "
    else:
        OutString = OutString + " - "
    OutString = OutString + "HP: " + str(HP) + " Atk: " + str(Atk) + " Def: " + str(Def) + " SpA: " + str(SpA) + " SpD: " + str(SpD) + " Spe: " + str(Spe)
    if pokeid == "":
        return "No pokemon chosen"
    else:
        return OutString

def itemsearch(item, conn):
    item = item.lower()
    item = item.replace(" ","-")

    c = conn.cursor()

    try:
        c.execute('SELECT id FROM items WHERE identifier = \'' + item + "\'")
    except:
        return "Error in search"
    
    outstring = ""
    itemid = ""
    for row in c:
         row = row[0]
         itemid = row
         #print(row)
     
    command = "SELECT name FROM item_names WHERE item_id = \'" + str(itemid) + "\'" + " and local_language_id = \'9\'"
    c.execute(command)
    for row in c:
         row = row[0]
         #print(row)
         outstring = row + " - "
     
    c.execute('SELECT short_effect FROM item_prose WHERE item_id = \'' + str(itemid) + "\'" + " and local_language_id = \'9\'")
    for row in c:
        row = row[0]
        row = row.replace("\n"," ")
        row = row.replace("Held: ","")
        #print(row)
        outstring = outstring + row
    return outstring

def weakto(List1):
    Normal = 0
    Fighting = 0
    Flying = 0
    Poison = 0
    Ground = 0
    Rock = 0
    Bug = 0
    Ghost = 0
    Steel = 0
    Fire = 0
    Water = 0
    Grass = 0
    Electric = 0
    Psychic = 0
    Ice = 0
    Dragon = 0
    Dark = 0
    Fairy = 0
    GhostImm = False
    GroundImm = False
    NormalImm = False
    ElectricImm = False
    FightingImm = False
    PoisonImm = False
    PsychicImm = False
    DragonImm = False

    #Potential Immunities:
    #Ghost, Ground, Normal, Electric, Fight, Poison, Psychic Dragon

    # Types:
    # Normal: +1 Fight, Immune Ghost
    # Fighting: -1 Rock Bug Dark, +1 Flying Psychic Fairy
    # Flying: -1 Fight Bug Grass, +1 Rock Electric Ice, Immune Ground
    # Poison: -1 Fight Poison Bug Grass Fairy, +1 Ground Psychic
    # Ground: -1 Poison Rock, +1 Water Grass Ice, Immune Electric
    # Rock: -1 Normal Flying Poison Fire, +1 Fight Ground Steel Water Grass
    # Bug: -1 Fight Ground Grass, +1 Flying Rock Fire
    # Ghost: -1 Poison Bug, +1 Ghost Dark, Immune Fight Normal
    # Steel: -1 Normal Flying Rock Bug Steel Grass Psychic Ice Fairy, +1 Fight Ground Fire, Immune Poison
    # Fire: -1 Bug Steel Fire Grass Ice Fairy, +1 Ground Rock Water
    # Water: -1 Steel Fire Water Ice, +1 Grass Electric
    # Grass: -1 Ground Water Grass Electric, +1 Flying Poison Bug Fire Ice
    # Electric: -1 Flying Steel Electric, +1 Ground
    # Psychic: -1 Fight Psychic, +1 Bug Ghost Dark
    # Ice: -1 Ice, +1 Fight Rock Steel Fire
    # Dragon: -1 Fire Water Grass Electric, +1 Ice Dragon Fairy
    # Dark: -1 Ghost Dark, +1 Fairy Bug Fight, Immune Psychic
    # Fairy: -1 Fight Bug Dark, +1 Poison Steel, Immune Dragon

    ListLen = len(List1)
    cont = True
    for x in range(0,ListLen):
        if List1[x] == "normal":
            Fighting += 1
            GhostImm = True
        elif List1[x] == "fighting":
            Flying += 1
            Psychic += 1
            Fairy += 1
            Rock += -1
            Bug += -1
            Dark += -1
        elif List1[x] == "flying":
            Rock += 1
            Electric += 1
            Ice += 1
            Fighting += -1
            Bug += -1
            Grass += -1
            GroundImm = True
        elif List1[x] == "poison":
            Ground += 1
            Psychic += 1
            Fighting += -1
            Poison += -1
            Bug += -1
            Grass += -1
            Fairy += -1
        elif List1[x] == "ground":
            Water += 1
            Grass += 1
            Ice += 1
            Poison += -1
            Rock += -1
            ElectricImm = True
        elif List1[x] == "rock":
            Fighting += 1
            Ground += 1
            Steel += 1
            Water += 1
            Grass += 1
            Normal += -1
            Flying += -1
            Poison += -1
            Fire += -1
        elif List1[x] == "bug":
            Flying += 1
            Rock += 1
            Fire += 1
            Fighting += -1
            Ground += -1
            Grass += -1
        elif List1[x] == "ghost":
            Ghost += 1
            Dark += 1
            Poison += -1
            Bug += -1
            NormalImm = True
            FightImm = True
        elif List1[x] == "steel":
            Fighting += 1
            Ground += 1
            Fire += 1
            Normal += -1
            Flying += -1
            Rock += -1
            Bug += -1
            Steel += -1
            Grass += -1
            Psychic += -1
            Ice += -1
            Dragon += -1
            Fairy += -1
            PoisonImm = True
        elif List1[x] == "fire":
            Ground += 1
            Rock += 1
            Bug += -1
            Steel += -1
            Fire += -1
            Grass += -1
            Ice += -1
            Fairy += -1
        elif List1[x] == "water":
            Grass += 1
            Electric += 1
            Steel += -1
            Fire += -1
            Water += -1
            Ice += -1
        elif List1[x] == "grass":
            Flying += 1
            Poison += 1
            Bug += 1
            Fire += 1
            Ice += 1
            Ground += -1
            Water += -1
            Grass += -1
            Electric += -1
        elif List1[x] == "electric":
            Ground += 1
            Flying += -1
            Steel += -1
            Electric += -1
        elif List1[x] == "psychic":
            Bug += 1
            Ghost += 1
            Dark += 1
            Fighting += -1
            Psychic += -1
        elif List1[x] == "ice":
            Fighting += 1
            Rock += 1
            Steel += 1
            Fire += 1
            Ice += -1
        elif List1[x] == "dragon":
            Ice += 1
            Dragon += 1
            Fairy += 1
            Fire += -1
            Water += -1
            Grass += -1
            Electric += -1
        elif List1[x] == "dark":
            Fighting += 1
            Bug += 1
            Fairy += 1
            Ghost += -1
            Dark += -1
            PsychicImm = True
        elif List1[x] == "fairy":
            Poison += 1
            Steel += 1
            Fighting += -1
            Bug += -1
            Dark += -1
            DragonImm = True
        else:
            print("Improper input")
            cont = False

    if cont == True:
        OutString = ""
        for x in range(0,ListLen):
            OutString = OutString + List1[x].title()
            if x != ListLen - 1:
                OutString = OutString + " "
        OutString = OutString + " is weak to"
        if Normal > 0 and NormalImm != True:
            OutString = OutString + " Normal" + " - " + str(Normal * 2) + "x"
        if Fighting > 0 and FightingImm != True:
            OutString = OutString + " Fighting" + " - " + str(Fighting * 2) + "x"
        if Flying > 0:
            OutString = OutString + " Flying" + " - " + str(Flying * 2) + "x"
        if Poison > 0 and PoisonImm != True:
            OutString = OutString + " Poison" + " - " + str(Poison * 2) + "x"
        if Ground > 0 and GroundImm != True:
            OutString = OutString + " Ground" + " - " + str(Ground * 2) + "x"
        if Rock > 0:
            OutString = OutString + " Rock" + " - " + str(Rock * 2) + "x"
        if Bug > 0:
            OutString = OutString + " Bug" + " - " + str(Bug * 2) + "x"
        if Ghost > 0 and GhostImm != True:
            OutString = OutString + " Ghost" + " - " + str(Ghost * 2) + "x"
        if Steel > 0:
            OutString = OutString + " Steel" + " - " + str(Steel * 2) + "x"
        if Fire > 0:
            OutString = OutString + " Fire" + " - " + str(Fire * 2) + "x"
        if Water > 0:
            OutString = OutString + " Water" + " - " + str(Water * 2) + "x"
        if Grass > 0:
            OutString = OutString + " Grass" + " - " + str(Grass * 2) + "x"
        if Electric > 0 and ElectricImm != True:
            OutString = OutString + " Electric" + " - " + str(Electric * 2) + "x"
        if Psychic > 0 and PsychicImm != True:
            OutString = OutString + " Psychic" + " - " + str(Psychic * 2) + "x"
        if Ice > 0:
            OutString = OutString + " Ice" + " - " + str(Ice * 2) + "x"
        if Dragon > 0 and DragonImm != True:
            OutString = OutString + " Dragon" + " - " + str(Dragon * 2) + "x"
        if Dark > 0:
            OutString = OutString + " Dark" + " - " + str(Dark * 2) + "x"
        if Fairy > 0:
            OutString = OutString + " Fairy" + " - " + str(Fairy * 2) + "x"
        return OutString
    else:
        return "There is an improper input in the types"

def resistantto(List1):
    Normal = 0
    Fighting = 0
    Flying = 0
    Poison = 0
    Ground = 0
    Rock = 0
    Bug = 0
    Ghost = 0
    Steel = 0
    Fire = 0
    Water = 0
    Grass = 0
    Electric = 0
    Psychic = 0
    Ice = 0
    Dragon = 0
    Dark = 0
    Fairy = 0
    GhostImm = False
    GroundImm = False
    NormalImm = False
    ElectricImm = False
    FightingImm = False
    PoisonImm = False
    PsychicImm = False
    DragonImm = False

    #Potential Immunities:
    #Ghost, Ground, Normal, Electric, Fight, Poison, Psychic Dragon

    # Types:
    # Normal: +1 Fight, Immune Ghost
    # Fighting: -1 Rock Bug Dark, +1 Flying Psychic Fairy
    # Flying: -1 Fight Bug Grass, +1 Rock Electric Ice, Immune Ground
    # Poison: -1 Fight Poison Bug Grass Fairy, +1 Ground Psychic
    # Ground: -1 Poison Rock, +1 Water Grass Ice, Immune Electric
    # Rock: -1 Normal Flying Poison Fire, +1 Fight Ground Steel Water Grass
    # Bug: -1 Fight Ground Grass, +1 Flying Rock Fire
    # Ghost: -1 Poison Bug, +1 Ghost Dark, Immune Fight Normal
    # Steel: -1 Normal Flying Rock Bug Steel Grass Psychic Ice Fairy, +1 Fight Ground Fire, Immune Poison
    # Fire: -1 Bug Steel Fire Grass Ice Fairy, +1 Ground Rock Water
    # Water: -1 Steel Fire Water Ice, +1 Grass Electric
    # Grass: -1 Ground Water Grass Electric, +1 Flying Poison Bug Fire Ice
    # Electric: -1 Flying Steel Electric, +1 Ground
    # Psychic: -1 Fight Psychic, +1 Bug Ghost Dark
    # Ice: -1 Ice, +1 Fight Rock Steel Fire
    # Dragon: -1 Fire Water Grass Electric, +1 Ice Dragon Fairy
    # Dark: -1 Ghost Dark, +1 Fairy Bug Fight, Immune Psychic
    # Fairy: -1 Fight Bug Dark, +1 Poison Steel, Immune Dragon

    ListLen = len(List1)
    cont = True
    for x in range(0,ListLen):
        if List1[x] == "normal":
            Fighting += 1
            GhostImm = True
        elif List1[x] == "fighting":
            Flying += 1
            Psychic += 1
            Fairy += 1
            Rock += -1
            Bug += -1
            Dark += -1
        elif List1[x] == "flying":
            Rock += 1
            Electric += 1
            Ice += 1
            Fighting += -1
            Bug += -1
            Grass += -1
            GroundImm = True
        elif List1[x] == "poison":
            Ground += 1
            Psychic += 1
            Fighting += -1
            Poison += -1
            Bug += -1
            Grass += -1
            Fairy += -1
        elif List1[x] == "ground":
            Water += 1
            Grass += 1
            Ice += 1
            Poison += -1
            Rock += -1
            ElectricImm = True
        elif List1[x] == "rock":
            Fighting += 1
            Ground += 1
            Steel += 1
            Water += 1
            Grass += 1
            Normal += -1
            Flying += -1
            Poison += -1
            Fire += -1
        elif List1[x] == "bug":
            Flying += 1
            Rock += 1
            Fire += 1
            Fighting += -1
            Ground += -1
            Grass += -1
        elif List1[x] == "ghost":
            Ghost += 1
            Dark += 1
            Poison += -1
            Bug += -1
            NormalImm = True
            FightImm = True
        elif List1[x] == "steel":
            Fighting += 1
            Ground += 1
            Fire += 1
            Normal += -1
            Flying += -1
            Rock += -1
            Bug += -1
            Steel += -1
            Grass += -1
            Psychic += -1
            Ice += -1
            Dragon += -1
            Fairy += -1
            PoisonImm = True
        elif List1[x] == "fire":
            Ground += 1
            Rock += 1
            Bug += -1
            Steel += -1
            Fire += -1
            Grass += -1
            Ice += -1
            Fairy += -1
        elif List1[x] == "water":
            Grass += 1
            Electric += 1
            Steel += -1
            Fire += -1
            Water += -1
            Ice += -1
        elif List1[x] == "grass":
            Flying += 1
            Poison += 1
            Bug += 1
            Fire += 1
            Ice += 1
            Ground += -1
            Water += -1
            Grass += -1
            Electric += -1
        elif List1[x] == "electric":
            Ground += 1
            Flying += -1
            Steel += -1
            Electric += -1
        elif List1[x] == "psychic":
            Bug += 1
            Ghost += 1
            Dark += 1
            Fighting += -1
            Psychic += -1
        elif List1[x] == "ice":
            Fighting += 1
            Rock += 1
            Steel += 1
            Fire += 1
            Ice += -1
        elif List1[x] == "dragon":
            Ice += 1
            Dragon += 1
            Fairy += 1
            Fire += -1
            Water += -1
            Grass += -1
            Electric += -1
        elif List1[x] == "dark":
            Fighting += 1
            Bug += 1
            Fairy += 1
            Ghost += -1
            Dark += -1
            PsychicImm = True
        elif List1[x] == "fairy":
            Poison += 1
            Steel += 1
            Fighting += -1
            Bug += -1
            Dark += -1
            DragonImm = True
        else:
            print("Improper input")
            cont = False

    if cont == True:
        OutString = ""
        for x in range(0,ListLen):
            OutString = OutString + List1[x].title()
            if x != ListLen - 1:
                OutString = OutString + " "
        OutString = OutString + " resists"
        if Normal < 0 and NormalImm != True:
            OutString = OutString + " Normal" + " - " + str(Normal * -2) + "x"
        if Fighting < 0 and FightingImm != True:
            OutString = OutString + " Fighting" + " - " + str(Fighting * -2) + "x"
        if Flying < 0:
            OutString = OutString + " Flying" + " - " + str(Flying * -2) + "x"
        if Poison < 0 and PoisonImm != True:
            OutString = OutString + " Poison" + " - " + str(Poison * -2) + "x"
        if Ground < 0 and GroundImm != True:
            OutString = OutString + " Ground" + " - " + str(Ground * -2) + "x"
        if Rock < 0:
            OutString = OutString + " Rock" + " - " + str(Rock * -2) + "x"
        if Bug < 0:
            OutString = OutString + " Bug" + " - " + str(Bug * -2) + "x"
        if Ghost < 0 and GhostImm != True:
            OutString = OutString + " Ghost" + " - " + str(Ghost * -2) + "x"
        if Steel < 0:
            OutString = OutString + " Steel" + " - " + str(Steel * -2) + "x"
        if Fire < 0:
            OutString = OutString + " Fire" + " - " + str(Fire * -2) + "x"
        if Water < 0:
            OutString = OutString + " Water" + " - " + str(Water * -2) + "x"
        if Grass < 0:
            OutString = OutString + " Grass" + " - " + str(Grass * -2) + "x"
        if Electric < 0 and ElectricImm != True:
            OutString = OutString + " Electric" + " - " + str(Electric * -2) + "x"
        if Psychic < 0 and PsychicImm != True:
            OutString = OutString + " Psychic" + " - " + str(Psychic * -2) + "x"
        if Ice < 0:
            OutString = OutString + " Ice" + " - " + str(Ice * -2) + "x"
        if Dragon < 0 and DragonImm != True:
            OutString = OutString + " Dragon" + " - " + str(Dragon * -2) + "x"
        if Dark < 0:
            OutString = OutString + " Dark" + " - " + str(Dark * -2) + "x"
        if Fairy < 0:
            OutString = OutString + " Fairy" + " - " + str(Fairy * -2) + "x"
        
        if GhostImm == True:
            OutString = OutString + " Ghost - Immune"
        if GroundImm == True:
            OutString = OutString + " Ground - Immune"
        if NormalImm == True:
            OutString = OutString + " Normal - Immune"
        if ElectricImm == True:
            OutString = OutString + " Electric - Immune"
        if FightingImm == True:
            OutString = OutString + " Fighting - Immune"
        if PoisonImm == True:
            OutString = OutString + " Poison - Immune"
        if PsychicImm == True:
            OutString = OutString + " Psychic - Immune"
        if DragonImm == True:
            OutString = OutString + " Dragon - Immune"
        
        return OutString

    else:
        return "There is an improper input in the types"
