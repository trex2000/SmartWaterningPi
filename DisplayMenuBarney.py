import time
import os #for clearing of the screen
import xml.etree.ElementTree as ET
from termcolor import colored #to be able to write with colors on the terminal
#for checking the arrow buttons
import getch


def main_menu():
    selectedItem=0  #menu item that is selected by default is the first one
    redrawNeeded=True
    numberOfElements=len(root[0])
    print("Number of elements:",numberOfElements)
    while 1:
        if redrawNeeded == True:
            redrawNeeded = False #reset the flag so that the menu will be redrawn only in case the arrow keys were pressed
            #we need to redraw the menu
            os.system('clear') #clear the screen
            print("Navigate the menu by 'w' and 's' keys, select by 'd', exit with 'x' key")
            for i in range(0,numberOfElements): 
                if i==selectedItem:
                    print(colored(root[0][i].text, 'green'))
                else:    
                    print(colored(root[0][i].text, 'white'))
        #check if there was an up or down button pressed?
        key = getch.getch()
        if key == 's':
            if selectedItem<numberOfElements:
                selectedItem = selectedItem + 1
                redrawNeeded=True
        elif key == 'w':
            if selectedItem>0:
                selectedItem = selectedItem - 1
                redrawNeeded=True
        if key == 'd':
           selectMenuItem(root[0][i].text)
        #'x'  key will end the program and exit
        if key == 'x':
            print ("Goodbye. Don't forget to do some cleanup")
            exit            
        #sleep for a while
        time.sleep(0.1)

#function that handles selected item
def selectMenuItem(selectedItemText):
    print ("The following Item was selected:",selectedItemText)
    #pause until keypress
    getch.getch()

#read the XML tree
tree = ET.parse('smart_watering_menu.xml')  # parsed the xml file
root = tree.getroot()

#running the menu
main_menu()

