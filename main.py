import json
import tkinter as tk
import tkinter.filedialog as fd
import shutil
import os

filetypes = (
    ('PNG Files', '*.png'),
)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def parseId(id):
    if id.startswith("5.100"):
        newId = id.replace("5.100.", "")
        print("Parsed item to be " + newId)
        return newId
    elif id.startswith("5.350"):
        newId = id.replace("5.350.", "")
        print("Parsed item to be " + newId)
        return newId

    try:
        _ = int(id)
    except ValueError as e:
        input("Item ID is not a number!\n")
        return False

    return id
        

def createItem(isTrinket, multiple, pathToFile):
    cls()
    if isTrinket:
        string_Type = "trinket"
        string_Dir = "/resources/gfx/items/trinkets"
        string_Template = "templates/trinketTemplate.lua"
        string_ItemFile = "data/trinkets.json"
    else:
        string_Type = "item"
        string_Dir = "/resources/gfx/items/collectibles"
        string_Template = "templates/itemTemplate.lua"
        string_ItemFile = "data/items.json"
    
    if multiple:
        string_FileOperation = "w" # overwrite
    else:
        string_FileOperation = "x" # create

    #Open and load the template
    if not multiple:
        with open(string_Template, "r") as file:
            filedata = file.read()
    else:
        with open(pathToFile, "r") as file:
            filedata = file.readlines()

    #Ask user to specify replacement data
    if not multiple:
        modname = '"' + str(input("What to call the mod?\n")) + '"'
        
    itemId = parseId(str(input(f"What is the ID of the {string_Type} you want to replace? (search on wiki)\n")))
    while itemId == False: # Ensure the item ID is correct
        itemId = parseId(str(input(f"What is the ID of the {string_Type} you want to replace? (search on wiki)\n")))
    newItemName = '"' + str(input(f"What do you want to call the new {string_Type}?\n")) + '"'
    newItemDesc = '"' + str(input(f"What do you want the new {string_Type} description to be?\n")) + '"'

    #Ask user if they want to include a sprite
    spriteAns = input("Add a sprite? (y/n)\n")
    if spriteAns.lower() == "y":
        spriteAns = True
    else:
        spriteAns = False

    #Replace template.lua data with user-specified data
    if not multiple:
        filedata = filedata.replace("%MODNAME", modname)
        filedata = filedata.replace("%ITEMID", itemId)
        filedata = filedata.replace("%NEWITEMNAME", newItemName)
        filedata = filedata.replace("%NEWDESCRIPTION", newItemDesc)
    else:
        itemEntry = "	" + "{" + itemId + "," + newItemName + "," + newItemDesc + "},\n"
        filedata.insert(3, itemEntry)

    #Try creating the directory
    if not multiple:
        try:
            os.mkdir(filePath)
        except OSError:
            print("Creation of the directory %s failed" % filePath)
            os._exit(0)

    if spriteAns:
        #Ask user for the item sprite
        input("Make sure the sprite is 32x32 and has a 32-bit depth! Press enter to continue.")
        print(f"Open the file where the {string_Type} sprite is")
        spriteDir = fd.askopenfilename(title="Open the sprite", filetypes=filetypes)

        #Create resources directory for the sprite
        itemsDir = filePath + string_Dir
        if not multiple:
            os.makedirs(itemsDir)

        with open(string_ItemFile, "r") as itemFile:
            jsondata = json.load(itemFile)

        gfxName = jsondata[itemId]['gfx']

        #Copy sprite to folder
        shutil.copyfile(spriteDir, itemsDir + "/" + gfxName)
        print("Sprite added!\n")

    #Save the new main.lua
    newFilePath = filePath + "/" + "main.lua"

    with open(newFilePath, string_FileOperation) as newFile:
        if not multiple:
            newFile.write(filedata)
        else:
            newFile.writelines(filedata)

    loopAns = input(f"Do you want to replace another {string_Type}? (y/n)\n")
    if loopAns.lower() == "y":
        createItem(isTrinket, True, newFilePath)

    input("Succesfully created mod!\nPress enter to exit.")
    os._exit(0)
    
def askCreateItem():
    cls()

    trinketItemChoice = input("Do you want to replace an item ( 0 ) or a trinket? ( 1 )?\n")
    if trinketItemChoice == "0":
        createItem(False, False, "")
    elif trinketItemChoice == "1":
        createItem(True, False, "")
    else:
        input("Incorrect choice. Try again.")
        askCreateItem()

def initialize():
    # Ask user to select the mods folder
    print("Select the 'mods' directory where Isaac is installed:")

    root = tk.Tk()
    root.withdraw()
    modsPath = fd.askdirectory(title="Select the 'mods' directory where Isaac is installed")

    mHead, mTail = os.path.split(modsPath)
    if mTail != "mods":
        input("Path is incorrect! Make sure you selected the 'mods' folder in the place where Isaac is installed (where 'isaac-ng.exe' is)")
        os._exit(0)
    #Ask user for the folder name of the mod
    folderName = str(input("What to call the folder that contains the mod?\n"))
    global filePath
    filePath = modsPath + "/" + folderName 

    askCreateItem()

# Start the sequence
initialize()