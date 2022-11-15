#!/usr/bin/evn python

# By: Clempton
# 9/17/21

import time
import nmap
import socket
from tkinter import *
from urllib.request import urlopen
from urllib.error import *
import requests

# Moves the cursor back to the a position
def gethome(up,left,count_r, count_c):

    for n in range(0,count_r):
        requests.post(left)
    for n in range(0,count_c):
        requests.post(up)
    return

# Moves the cursor to correct row
def leftright(row_mov,left,right):
    
    # Finds correct number of shifts left or right
    t = abs(row_mov)
    count = 0
    while t != 0:
        if row_mov < 0:
            requests.post(left)
            count = count - 1
        else:
            requests.post(right)
            count = count + 1
        t = t - 1

    return(count)
# Moves the cursor to the correct column
def updown(col_mov,up,down):

    # Finds correct number of shifts up or down
    t = abs(col_mov)
    count = 0
    while t !=0:
        if col_mov < 0:
            requests.post(up)
            count = count - 1
        else:
            requests.post(down)
            count = count + 1
        t = t - 1

    return(count)

def printer(message,up,down,right,left,select,root,status):

    cur_pos = 0
    # Counts positions of rows and columns at end of letter
    count_r = 0
    count_c = 0

    # Representation of the Roku keyboard
    board = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,
    'g':6,'h':7,'i':8,'j':9,'k':10,'l':11,
    'm':12,'n':13,'o':14,'p':15,'q':16,'r':17,
    's':18,'t':19,'u':20,'v':21,'w':22,'x':23,
    'y':24,'z':25,'1':26,'2':27,'3':28,'4':29,
    '5':30,'6':31,'7':32,'8':33,'9':34,'0':35,
    '~':36,'!':37,' ':38,'@':39,'bck':40,'$':41
    }
    word = ''
    # Finds letter in message and matches it to value in keyboard
    for letter in message:
        active = board.get(letter)
        
        # Prints working letter in message
        
        #print("[+] Typing: " + letter)
        word = word + letter
        step = "[...] Typing: "+word
        status['text'] = "{}".format(step)
        root.update()

        # Check to make sure letter isnt the same as pervious letter    
        if(active != cur_pos):
            
            # Calculates number of moves
            col_mov = (active//6)-(cur_pos//6)
            row_mov = (active%6)-(cur_pos%6)

            # Fixes problem with bottom row only having 3 buttons
            if(letter==' ' or letter=='~'):
                count_r = count_r + leftright(row_mov,left,right)
                count_c = count_c + updown(col_mov,up,down)
            else:
                count_c = count_c + updown(col_mov,up,down)
                count_r = count_r + leftright(row_mov,left,right)
        requests.post(select)
        
        # Updates position of cursor to be correct for the next letter
        cur_pos = active
    gethome(up,left,count_r, count_c)
    
    return()

# Main Function
def main(IP,root,status,windowback,window):
    
    # Get IP address input
    #try:
    #    IP = str(input("\nEnter Roku IP Address. If unknown, press enter for nmap scan automation: "))
    #except KeyError:
    #    pass
    # Automates nmap search for Roku IP address onnetwork
    if IP == '':
        # Finds the gateway IP address
        proc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        proc.connect(("8.8.8.8",80))
        nam = proc.getsockname()[0]
        proc.close()
        nam = nam.split('.')
        gateway = ''
        for x in nam[:-1]:
            gateway=gateway+x+'.'
        gateway = gateway + '1'
        #print("Gateway found at: "+gateway)
        step = "[+] Gateway found at: "+gateway
        status['text'] = "{}".format(step)
        root.update()
        # Finds the Roku IP address on network from quick nmap scan
    
        nm = nmap.PortScanner()
        nm.scan(gateway[:-1]+'0/24', arguments='-sn') 
        for device in nm._scan_result['scan']:
            #print(device)
            working = list(nm._scan_result['scan'][device]['vendor'].values())
            #if(len(working) > 0):
                #print(str(working[0]))
            if(len(working) > 0 and str(working[0]) == 'Roku'):
                IP = device
                
    
        #print("Roku IP address found at: "+IP)
        step = "[+] Roku IP address found at: "+IP
        status['text'] = "{}".format(step)
        root.update()

        
    
    # Curl request strings with IP address added
    # These are remote control button requests
    #up ="curl -d '' \"http://"+IP+":8060/keypress/up\""
    #down ="curl -d '' \"http://"+IP+":8060/keypress/down\""
    #right = "curl -d '' \"http://"+IP+":8060/keypress/right\""
    #left = "curl -d '' \"http://"+IP+":8060/keypress/left\""
    home ='http://'+IP+':8060/keypress/home'
    #select = "curl -d '' \"http://"+IP+":8060/keypress/select\""
    search = 'http://'+IP+':8060/search/a'
    try: 
        urlopen("http://"+IP+":8060")
    except HTTPError as e:
        step = "[!] Roku device not found at this IP"
        windowback = PhotoImage(file='Data/backgroundRed.png')
        window.create_image(0,0,image=windowback,anchor=NW)
        root.update()
        status['text'] = "{}".format(step)
        root.update()
        time.sleep(1)
        return(0)
    except URLError as e:
        step = "[!] Roku device not found at this IP"
        windowback = PhotoImage(file='Data/backgroundRed.png')
        window.create_image(0,0,image=windowback,anchor=NW)
        root.update()
        status['text'] = "{}".format(step)
        root.update()
        time.sleep(1)
        return(0)
    
    
    # Operations to get to the search menu / keyboard
    requests.post(home)
    time.sleep(2)
    requests.post(search)
    time.sleep(2)


    step = "[+] Enter a Message:"
    windowback = PhotoImage(file='Data/backgroundGreen.png')
    window.create_image(0,0,image=windowback,anchor=NW)
    root.update()
    status['text'] = "{}".format(step)
    root.update()
    
        
        
        # Run printer methods
    #printer(message,up,down,right,left,select,root,status,windowback,window)
    
    return(IP)

# Calls the main() function
if __name__ == '__main__':
    main()