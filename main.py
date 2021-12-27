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
        idInt = int(id)
    except ValueError as e:
        input("Item ID is not a number!")
        os._exit(0)

    return id
        

def createItem(isTrinket, multiple, pathToFile):
    cls()
    if isTrinket:
        string_Type = "trinket"
        string_Dir = "/resources/gfx/items/trinkets"
        string_Template = "templates/trinketTemplate.lua"
        string_ItemFile = "trinkets.json"
    else:
        string_Type = "item"
        string_Dir = "/resources/gfx/items/collectibles"
        string_Template = "templates/itemTemplate.lua"
        string_ItemFile = "items.json"
    
    if multiple:
        string_FileOperation = "w" # overwrite
    else:
        string_FileOperation = "x" # create

    #Open and load the template
    if not multiple:
        with open(string_Template, "r") as file:
            filedata = file.read()
            file.close()
    else:
        with open(pathToFile, "r") as file:
            filedata = file.readlines()
            file.close()

    #Ask user to specify replacement data
    if not multiple:
        modname = '"' + str(input("What to call the mod?\n")) + '"'
        
    itemId = parseId(str(input("What is the ID of the " + string_Type + " you want to replace? (search on wiki)\n")))
    newItemName = '"' + str(input("What do you want to call the new " + string_Type + "?\n")) + '"'
    newItemDesc = '"' + str(input("What do you want the new " + string_Type + " description to be?\n")) + '"'

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
        print("Open the file where the " + string_Type + " sprite is")
        spriteDir = fd.askopenfilename(title="Open the sprite", filetypes=filetypes)

        #Create resources directory for the sprite
        itemsDir = filePath + string_Dir
        if not multiple:
            os.makedirs(itemsDir)

        with open(string_ItemFile, "r") as itemFile:
            jsondata = json.load(itemFile)
            itemFile.close()

        gfxName = jsondata[itemId]['gfx']

        #Copy sprite to folder
        shutil.copyfile(spriteDir, itemsDir + "/" + gfxName)


    #Save the new main.lua
    newFilePath = filePath + "/" + "main.lua"
    newFile = open(newFilePath, string_FileOperation)
    if not multiple:
        newFile.write(filedata)
    else:
        newFile.writelines(filedata)

    newFile.close()

    loopAns = input("Do you want to replace another " + string_Type + "? (y/n)\n")
    if loopAns.lower() == "y":
        createItem(isTrinket, True, newFilePath)

    #Could've just removed the modname part...
    if not multiple:
        input("Succesfully created mod named " + modname + "!\nPress enter to exit.")
        os._exit(0)
    else:
        input("Succesfully created mod!\nPress enter to exit.")
        os._exit(0)
    
def askCreateItem():
    trinketItemChoice = input("Do you want to replace an item ( 0 ) or a trinket? ( 1 )?\n")
    if trinketItemChoice == "0":
        createItem(False, False, "")
    elif trinketItemChoice == "1":
        createItem(True, False, "")
    else:
        input("Wrong choice!")
        os._exit(0)

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

    cls()
    askCreateItem()

# Start the sequence
initialize()