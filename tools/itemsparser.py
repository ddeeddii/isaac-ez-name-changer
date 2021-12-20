# This tool parses the items.xml file in order to extract item id's and thier corresponding graphic file names.

from xml.dom import minidom
import tkinter as tk
import tkinter.filedialog as fd
import json

itemIds = {}

filetypes = (
    ('XML Files', '*.xml'),
    ('All Files', '*.*')
)

def extractData():
    print("Open items.xml")
    root = tk.Tk()
    root.withdraw()
    xmlPath = fd.askopenfilename(title="Open items.xml", filetypes=filetypes)

    xmldoc = minidom.parse(xmlPath)

    activelist = xmldoc.getElementsByTagName("active")
    passivelist = xmldoc.getElementsByTagName("passive")
    trinketlist = xmldoc.getElementsByTagName("trinket")
    familiarList = xmldoc.getElementsByTagName("familiar")
    items = activelist + passivelist + familiarList #+ trinketlist

    out = open("items.json", "a")

    for s in items:
        name = str(s.attributes["gfx"].value)
        id = s.attributes["id"].value
        itemIds[id] = {"gfx": name}

    json.dump(itemIds, out)
    out.close()
    input("\nSuccesfully extracted " + str(len(items)) + " ids and gfxs! Press enter to close\n")


extractData()