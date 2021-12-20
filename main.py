import json
import tkinter as tk
import tkinter.filedialog as fd
import shutil
import os

filetypes = (
    ('PNG Files', '*.png'),
)

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
        exit()

    return id
        

def createItem(isTrinket):
    if isTrinket:
        string_Type = "trinket"
        string_Dir = "/resources/gfx/items/trinkets"
        string_Template = "templates/trinketTemplate.lua"
    else:
        string_Type = "item"
        string_Dir = "/resources/gfx/items/collectibles"
        string_Template = "templates/itemTemplate.lua"

    #Open and load the template
    with open(string_Template, "r") as file:
        filedata = file.read()
        file.close()

    #Ask user to specify replacement data
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
    filedata = filedata.replace("%MODNAME", modname)
    filedata = filedata.replace("%ITEMID", itemId)
    filedata = filedata.replace("%NEWITEMNAME", newItemName)
    filedata = filedata.replace("%NEWDESCRIPTION", newItemDesc)

    #Try creating the directory
    try:
        os.mkdir(filePath)
    except OSError:
        print("Creation of the directory %s failed" % filePath)
        exit()

    if spriteAns:
        #Ask user for the item sprite
        input("Make sure the sprite is 32x32 and has a 32-bit depth! Press enter to continue.")
        print("Open the file where the " + string_Type + " sprite is")
        spriteDir = fd.askopenfilename(title="Open the sprite", filetypes=filetypes)

        #Create resources directory for the sprite
        itemsDir = filePath + string_Dir
        os.makedirs(itemsDir)

        if isTrinket:
            with open("trinkets.json", "r") as itemFile:
                jsondata = json.load(itemFile)
                itemFile.close()

            gfxName = jsondata[itemId]['gfx']
        else:
            with open("items.json", "r") as itemFile:
                jsondata = json.load(itemFile)
                itemFile.close()

            gfxName = jsondata[itemId]['gfx']

        #Copy sprite to folder
        shutil.copyfile(spriteDir, itemsDir + "/" + gfxName)


    #Save the new main.lua
    newFile = open(filePath + "/" + "main.lua", "x")
    newFile.write(filedata)
    newFile.close()

    input("Succesfully created mod named " + modname + "!\nPress enter to exit.")

# Ask user to select the mods folder
print("Select the 'mods' directory where Isaac is installed:")

root = tk.Tk()
root.withdraw()
modsPath = fd.askdirectory(title="Select the 'mods' directory where Isaac is installed")

mHead, mTail = os.path.split(modsPath)
if mTail != "mods":
    input("Path is incorrect! Make sure you selected the 'mods' folder in the place where Isaac is installed (where 'isaac-ng.exe' is)")
    exit()
#Ask user for the folder name of the mod
folderName = str(input("What to call the folder that contains the mod?\n"))
filePath = modsPath + "/" + folderName 

trinketItemChoice = input("Do you want to replace an item ( 0 ) or a trinket? ( 1 )?\n")

if trinketItemChoice == "0":
    createItem(False)
elif trinketItemChoice == "1":
    createItem(True)
else:
    input("Wrong choice!")
    exit()
