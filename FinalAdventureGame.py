# Mirror, Mirror on the Wall Text Based Adventure Game
# by Gabriela Johnson
from datetime import datetime
import re
import sys

# user name
name = ""
# Each room with a function should have first scene set to 1
centerMirrorScene = 1
dungeonMirrorScene = 1
foyerScene = 1
bookOfBindingScene = 1
# When false, this variable will allow the user to make choices until they win the game
gameOver = False

# The rooms, exits and objects lists were ideas taken from the template
# Creates every room in the game and their descriptxions
rooms={"Forest":"Lies just outside the Castle.  The castle lies ahead to the north.",
       "Castle Entrance":"The way to enter the castle walls. Turn west on the path to enter the castle.  Turn south to return to the Forest.",
       "Foyer":"The Foyer has dark hard wood floors with arched entryways on either side.  To the north is a long hallway, to the south is a bedroom, and west is the center room of the castle.",
       "Hallway":"A torch lights both sides of the hall's grey stoned walls.  Tapestries hang from both sides of the hallway. To the west is a grand door to the ballroom.",
       "Bedroom":"The bedroom has a a four-poster bed, covered in a ruby red comforter and blue and gold linens.  The stone walls and floor darken the room. West is the study, and north will return you to the foyer.",
       "Study":"To the north is an old wooden desk, covered in intricate carved designs. A large book, the book of binding, lays on top of it. To the west is an old door dark wooden door, with dingy bars on it.",
       "Dungeon Hallway":"To the north is the dungeon, to the east you will be returned from the passageway into the study.",
       "Dungeon":"The room is almost pitchblack, you see a glint of light to the east. The dungeon hallway is to the south.",
       "DungeonMirror":"A broken mirror with speckles of dirts on it. Go west to return to the dungeon",
       "Center Room":"A tall mirror on the southern wall, with a golden frame reaches the ceiling.  The floor is covered in an ornate red carpet. The potion room is down the stairs.",
       "Center Mirror": "A glossy mirror reaching from ground to ceiling.",
       "Ballroom":"The gold ballroom, with its high ceilings and pillars. The glossy tiled floor spreads to the tall window panes, lined with crimson curtains. Go north to view the ballroom paintings. Go east to return to the hallway.",
       "BallroomPainting":"*The painting is a poem in a cursive poem in a simple frame*\nOne red bird flew to the bird bath\nAnother blue jay followed her\nThe yellow canary came for conversation\nAnd the monster came and swallowed her\n\nWhat a creepy poem...",
       "Kitchen":"The counters are covered in pots and pans.  A red checkered table has red, yellow, blue and green potions. Go east to return to the center room",
       "Potion Room":"The room is cast in a purple glow, eerie and bright.  The cauldron is to the east, what lurks in the shadows of this magic place?",
       "Cauldron":f"A bubbly black cauldron with green, purple and yellow steam arising from it."}

# Defines the exits that each room has and which room the exits lead to
exits={"Forest":{"north":["Castle Entrance"]},
       "Castle Entrance":{"west":["Foyer"],"south":["Forest"]},
       "Foyer":{"west":["Center Room"],"north":["Hallway"],"south":["Bedroom"],"east":["Castle Entrance"],"up":["1st Floor","KeyCard"]},
       "Hallway":{"west":["Ballroom"],"south":["Foyer"]},
       "Bedroom":{"west":["Study"],"north":["Foyer"]},
       "Study":{"west":["Dungeon Hallway"],"east":["Bedroom"]},
       "Dungeon Hallway":{"north":["Dungeon"],"east":["Study"]},
       "Dungeon":{"south":["Dungeon Hallway"],"east":["DungeonMirror"]},
       "DungeonMirror":{"west":["Dungeon"]},
       "Center Room":{"west":["Kitchen"],"down":["Potion Room"],"south":["Center Mirror"],"east":["Foyer"]},
       "Center Mirror":{"north":["Center Room"]},
       "Ballroom":{"east":["Hallway"],"north":["BallroomPainting"]},
       "BallroomPainting":{"south":["Ballroom"]},
       "Kitchen":{"east":["Center Room"]},
       "Potion Room":{"up": ["Center Room"], "east":["Cauldron"]},
       "Cauldron":{"west":["Potion Room"]},}

# Creates objects present in each room
objects={"Forest":[],
       "Castle Entrance":[],
       "Foyer":[],
       "Hallway":["torch"],
       "Bedroom":[],
       "Study":["book of binding"],
       "Dungeon Hallway":[],
       "Dungeon":[],
       "Center Room":[],
       "Ballroom":[],
       "Kitchen":["red potion","green potion","yellow potion","blue potion"],
       "Potion Room":[],
       "Cauldron": []}

# Blocks rooms from user at the beginning of the game
blockedRooms = ["Hallway","Bedroom","Kitchen","Dungeon Hallway"]

# User inventory
inventory=[]

# Prints out room description
def roomDetails(room):
  print(room,":","\n",rooms[room])


# USER ACTION FUNCTIONS

# This function  was initally from the template
# Allows the user to move to another room if possible
def go(direction,room):
    possible=False
    if direction in exits[room]:
        if len(exits[room][direction])==1:     
            possible=True
        elif len(exits[room][direction])>1:
            if exits[room][direction][1] in inventory:
                possible=True
    if possible==True:
        if exits[room][direction][0] in blockedRooms:
          print("You can't go in this room right now")
          return room
        else:
          room=exits[room][direction][0]
        roomDetails(room)
    else:
        print("You can't go in that room yet")
        return False
    return room

# Allows the user to use an object in their inventory
def use(object):
    if object in inventory and object in objectFunctions:
        objectFunctions[object]()
    elif object not in inventory:
        print("You don't have this object")
    else:
        print("It isn't possible to use this object by itself")

# This function was initially from the template
# Allows the user to add an object to their inventory
def collect(object,room):
  if object.lower() in objects[room] and object.lower() not in inventory:
    inventory.append(object.lower())
    print(object,"has been added to your inventory.")
  elif object in inventory:
    print(f"{object} already in inventory")
  else:
    print("You can not add this object to your inventory.")

# Allows the user to combine objects in their inventory
def combine(objects):
  global dungeonMirrorScene
  global gameOver
  # Join objects in one string
  objectsString = " ".join(objects)
  # Get all objects by splitting the string by and
  splitObjects = objectsString.split(" and ")
  
  # Ensure that the objects haven't been combined before
  if(len(splitObjects) == 2):
    twoItems = {splitObjects[0].lower(),splitObjects[1].lower()}
    if twoItems in combinedObjects:
      print("It isn't possible to combine these objects")
      return
    object1 = splitObjects[0].lower()
    object2 = splitObjects[1].lower()
  elif(len(splitObjects) == 3):
    threeItems = {splitObjects[0].lower(),splitObjects[1].lower(),splitObjects[2].lower()}
    if threeItems in combinedObjects:
      print("It isn't possible to combine these objects")
      return
    object1 = splitObjects[0].lower()
    object2 = splitObjects[1].lower()
    object3 = splitObjects[2].lower()

  # Check if all objects are in inventory
  if len(splitObjects) == 3 and object1 in inventory and object2 in inventory and object3:
    # Only combine potions if they were entered in the correct order
    if (object1 == "red potion" and object2 == "blue potion" and object3 == "yellow potion" and currentRoom.lower() == "cauldron"):
        print(f"You have combined {object1} and {object2} and {object3}")
        global DungeonMirrorScene
        DungeonMirrorScene = 2
        print("*WOOSH*BUBBLE*BUBBLE*TOIL*TROUBLE*")
        print("You have created the potion!")
        print("The mirror potion has been added to your inventory")
        inventory.append("mirror potion")
        # Move on to next scene in dungeon mirror now that we have the potion
        dungeonMirrorScene = 3
        # Add new combination to combinedObjects, so we can't do it again
        combinedObjects.append({object1,object2,object3})
        return
    elif (object1 == "red potion" and object2 == "blue potion" and object3 == "yellow potion" and currentRoom.lower() == "cauldron"):
        print("You must be by the cauldron to combine these potions")
  # Check if all objects are in inventory
  elif len(splitObjects) == 2 and object1 in inventory and object2 in inventory:
    # Only combine certain pairs of objects
    if (object1 == "miriam's page" and object2 == "torch") or (object2 == "miriam's page" and object1 == "torch"):
      print(f"You have combined {splitObjects[0]} and {splitObjects[1]}")
      global centerMirrorScene
      # Move on to next scene in center mirror now that we freed Miriam
      centerMirrorScene = 3
      print("*CLANG*")
      print("That sounded like it came from the center room")
      combinedObjects.append({object1,object2})
      return
    elif (object1 == "hector's page" and object2 == "torch") or (object2 == "hector's page" and object1 == "torch" and currentRoom.lower() == "dungeon"):
      print(f"You have combined {object1} and {object2}")
      print("*CLANG*")
      print("That sounded like it came from the dungeon mirror")
      # Move on to next scene in dungeon mirror now that we freed Hector
      dungeonMirrorScene = 4
      combinedObjects.append({object1,object2})
      return
    elif (object1 == "book of binding" and object2 == "torch") or (object2 == "book of binding" and object1 == "torch" and currentRoom.lower() == "dungeon") and dungeonMirrorScene == 4:
      combinedObjects.append({object1,object2})
      print(f"You have combined {object1} and {object2}")
      print("The book of binding burns into flames....")
      print("Congratulations on freeing Hector and Miriam! You have completed your adventure.")
      print("End of Game")
      # Ends the game
      gameOver = True
      return
  print("It isn't possible to combine these objects")

# Explains to use how to navigate game
def getHelp():
  print("Here is how you will get around in this world:")
  print("You can enter these commands to perform these actions:")
  print("GO - move north, south, east, west, up or down (i.e. go north)")
  print("COLLECT - collect an object (i.e. collect pencil)")
  print("COMBINE - Combines two objects in your inventory(i.e. combine pencil and paper)")
  print("USE - Use an object in your inventory(i.e. use book)")
  print("BYE - To exit a conversation or stop using an object (i.e. bye)")
  print("INVENTORY - View Inventory (i.e. inventory)")
  print("EXIT - Exit the game (i.e. exit)")
  print("\nType 'Help' if you want to pull up this menu again")


def viewInventory():
  print(inventory)

#ROOM SCENE FUNCTIONS

def foyer():
  global foyerScene
  if foyerScene == 1:
    print(f"\n*Thump Thump*")
    print(f"A low knocking noise is coming from the center room")
    # Set to 2 so we can only experience this scene once
    foyerScene = 2
    return

def centerMirror():
  global centerMirrorScene
  directive = "start"

  # Meet Miriam
  if centerMirrorScene == 1:
    print(f"Old woman: {name}!{name}!!!!")
    print(f"Old woman: It's me, Miriam!")
    print(f"Miriam: Please help me I'm trapped\nMiriam: You must retrieve the book of binding.  Find my face in its pages, then rip out the page and burn it.  Then I will be free.")
    blockedRooms.remove("Hallway")
    blockedRooms.remove("Bedroom")
    centerMirrorScene = 2
    return
  # Get a hint from Miriam about book
  elif centerMirrorScene == 2:
    print(f"Free me {name}! Burn my page in the book of binding. Do you need a hint?")
  # You have saved Miriam
  elif centerMirrorScene == 3:
    print(f"Miriam: You have saved me {name}! I can't believe that worked so easy...")
    print(f"Miriam: I haven't seen Hector, we must find him")
    blockedRooms.remove("Dungeon Hallway")
    centerMirrorScene = 4
    return
  # Get a hint from Miriam about Hector
  elif centerMirrorScene == 4:
    print(f"We must find Hector. Do you need a hint?")
  
  # If we're getting a hint, initalize while loop so we can submit input (yes/no/bye)
  if centerMirrorScene == 2 or centerMirrorScene == 4:
    while (directive.lower() != "bye") and (directive.lower() != "no") and (directive.lower() != "yes"): 
        print("Center Mirror Command Line")
        directive=input(": ")
        if directive.lower()=="yes": 
          if centerMirrorScene == 2:
            print("The book of binding can be found in the study.")
          elif centerMirrorScene == 4:
            print("He wasn't in any of the main living spaces, he must be with the prisoners.")
          elif directive.lower() == "help": 
            getHelp()
          elif directive.lower() != "bye" and directive.lower() != "no":
            print("I'm sorry I didn't understand that command.")
    print(f"Goodluck {name}, please hurry!")


def dungeonMirror():
  global dungeonMirrorScene
  directive = "start"
  # Talk to Hector trapped in mirror
  if dungeonMirrorScene == 1:
    print(f"Old Man: {name}!  Oh my how did you find me??")
    print("*It's very dark, you barely make out his face*")
    print("Old Man: I know it's dark, it's me Hector.")
    print("Hector: I don't even know how I was trapped here. I kept having nightmares of a dark figure for weeks.")
    print("Hector: Then one night, I didn't wake up in my bed, I woke up in here.")
    print("Hector: It's so cold...")
    print("Hector: This mirror holding me is broken.  You will need to make a potion and throw it on this mirror.")
    print("Hector: I'm not sure how to make the potion, there must be a hint somewhere in this castle.  It's full of secrets.")
    print(f"Hector: Please fight for me {name}")
    dungeonMirrorScene = 2
    blockedRooms.remove("Kitchen")
    return
  # Get a hint from Hector
  elif dungeonMirrorScene == 2:
    print(f"Hello {name}, do you need a hint?")
  # After you have created the potion to free Hector
  elif dungeonMirrorScene == 3:
    print("Hector: You have the potion! Please use it!!")
    return
  # After you have freed Hector
  elif dungeonMirrorScene == 4:
    print(f"Hector: You have freed me {name}! I am forever in your debt.  Please now burn the entire book of binding so Miriam and I will always be free.")
  return
  # If we're getting a hint, initalize while loop so we can submit input (yes/no/bye)
  if dungeonMirrorScene == 2:
    while (directive.lower() != "bye") and (directive.lower() != "no") and (directive.lower() != "yes"): 
        print("Dungeon Mirror Command Line")
        directive=input(": ")
        if directive.lower()=="yes": 
          if centerMirrorScene == 2:
            print("You must collect the potions to mix, where would liquids be found?")
          elif directive.lower() == "help": 
            getHelp()
          elif directive.lower() != "bye" and directive.lower() != "no":
            print("I'm sorry I didn't understand that command.")

def cauldron():
  global dungeonMirrorScene
  # If we have never spoken to Hector
  if dungeonMirrorScene == 1:
    print("The cauldron looks ready to go, maybe you will have to use this in the future?")
  # If we have all the potions needed to free Hector
  elif "red potion" in inventory and "yellow potion" in inventory and "blue potion" in inventory:
    print("Combine the potions in the correct order")
  # If we don't have all the potions to free Hector
  elif "red potion" not in inventory or "yellow potion" or inventory or "blue potion" in inventory and dungeonMirrorScene == 2:
    print("You must collect all of the potions you need to make the potion")



# USE OBJECT FUNCTIONS

def useBookOfBinding():
  global bookOfBindingScene
  directive = "start"

  if bookOfBindingScene == 1:
    print("You open a large leather bound book, it barely fits in your hands.")
    print("You leaf through the heavy pages until you reach Miriam's face.  Her hair streaked grey and brown, her mole on the right side of her face.")
    print("You must rip Miriam's page out, and burn it as she said.")
    objects["Study"].append("miriam's page")
  elif bookOfBindingScene == 2:
    print("You have already collected the page")
  elif bookOfBindingScene == 3:
    print("You open the book of binding again.  You flip to Hector's page, you must rip it out like you did Miriam's page, and burn it with your torch.")
    objects["Study"].append("hector's page")
  while (directive[0].lower() != "bye") and directive[0].lower() != "collect":
    print("Book of Binding Command Line")
    directive=input(": ")
    directive = directive.split()
    if directive[0].lower()=="collect":
      collect(" ".join(directive[1:]),"Study")
      if ("miriam's page" in inventory or "hector's page" in inventory):
        print("You have ripped the page out of the book")
        bookOfBindingScene = 2
    elif directive[0].lower() == "help": 
      getHelp()
    elif (directive[0].lower() != "bye"):
      print("I'm sorry I didn't understand that command.")
  return

def useMirrorPotion():
  global bookOfBindingScene
  if currentRoom.lower() == "dungeonmirror":
    print("The mirror is fixed!  Now you can burn Hector's page in the book of binding. Step west, back into the dungeon, so you light the page away from the mirror.")
    bookOfBindingScene = 3
  elif currentRoom.lower() != "dungeonmirror":
    print("You have to be facing the dungeon mirror to use this potion.")
  return

roomFunctions={"Center Mirror": centerMirror,"Foyer": foyer,"DungeonMirror": dungeonMirror,"Cauldron": cauldron}
objectFunctions={"book of binding": useBookOfBinding,"mirror potion": useMirrorPotion}
combinedObjects = list()


# INTRO FUNCTIONS

currentRoom="Forest"

# Post Current Date and Time to user
def postDate():
  currentDate = datetime.now()
  print("It is",currentDate.strftime("%B %d, %Y"),"...\nthe time is", currentDate.strftime("%H:%M"))

# The first scene in the whole game
def intro():
  postDate()
  print("Mirror, Mirror on the Wall")
  continueLoop = True
  roomDetails(currentRoom)

  print("\nLet us begin...\n")

  print("\n\nWake up Wake up")
  print("Wake up!")
  print("*You doze a bit*")
  print("Will you wake up? (Yes/No)")

  # Choose whether or not to open your eyes
  while continueLoop:
    command=input(": ")
    command=command.lower().strip()
    if command=="yes":
        print ("You open your eyes")
        continueLoop = False

    elif command=="no":
        print("*You twist to your left, ignoring the voice*")
        print("The Voice: Wake! You must wake!")

  print("You peer around your surroundings.  An old man with a bushy pepper beard stands over you, annoyed at your laziness to wake up.")

  print("Old Man: What is your name?")

  global name
  name=input(": ")
  name=name.strip()

  print(f"Old Man: That's quite a name, {name}")
  print("Old Man: You've been missing for hours, how did you get here? Nevermind, you must go to the castle! Much chaos there, Miriam has been missing for hours.")
  getHelp()

  print("\nNow that you have your bearings, run to the castle! It lies to the north.")

intro()

# This code was initially from the template
# User will enter a command here, either go, collect, combine and use.
# Or they can ask for help or view their inventory
while gameOver != True:
    print("\nMain Command Line")
    # User input
    initialCommand=input(": ")
    # Split command so we can analyze the command and then parameters
    command=initialCommand.split()

    if initialCommand == "":
      print("You entered nothing, please enter a command")
    elif command[0].lower()=="go": # walk
      tempRoom = currentRoom
      currentRoom=go(command[1].lower(),currentRoom)
      # Run room functions if room is not blocked from user
      if currentRoom in roomFunctions and (currentRoom not in blockedRooms) and currentRoom:
        roomFunctions[currentRoom]()
      # If currentroom is false, set it to previous room
      if not currentRoom:
        currentRoom = tempRoom
    elif command[0].lower()=="collect":
      collect(" ".join(command[1:]),currentRoom)
    elif command[0].lower()=="combine" and ("and" in command):
      # If "and" is found in the combine command, you can pass it through
      if re.search("and", " ".join(command[1:])):
        combine(command[1:])
    elif command[0].lower()=="use":
      use(" ".join(command[1:]))
    elif command[0].lower()=="inventory":
      viewInventory()
    elif command[0].lower() == "help": 
      getHelp()
    elif command[0].lower() == "exit":
      sys.exit(0)
    else:
      print("I'm sorry I didn't understand that command.")
