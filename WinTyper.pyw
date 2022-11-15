from scapy.all import *
from tkinter import *
import Runner
import re


IP=''
count=0
found = 0

def main(dstIP):
    #distIP = label.get()
    if (not(re.match('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',dstIP)) and not dstIP == 'Enter Roku IP, or leave blank to auto scan' and not dstIP == ''):
        windowback = PhotoImage(file='Data/backgroundRed.png')
        window.create_image(0,0,image=windowback,anchor=NW)
        root.update()
        step = '[!] Incorrect IP Address'
        status['text'] = "{}".format(step)
        root.update()
        time.sleep(1)
        return
    elif dstIP == 'Enter Roku IP, or leave blank to auto scan' or dstIP == '':
        dstIP = ''
        windowback = PhotoImage(file='Data/backgroundBlue.png')
        window.create_image(0,0,image=windowback,anchor=NW)
        root.update()
        step = '[-] Searching for IP address automatically'
        status['text'] = "{}".format(step)
        root.update()
        time.sleep(.5)

    
    
    windowback = PhotoImage(file='Data/backgroundBlue.png')
    window.create_image(0,0,image=windowback,anchor=NW)
    root.update()
    step = '[+] Connecting to IP'
    status['text'] = "{}".format(step)
    root.update()
    global IP
    IP = Runner.main(dstIP,root,status,windowback,window)
    step = "[~] Enter a Message:"
    windowback = PhotoImage(file='Data/backgroundGreen.png')
    window.create_image(0,0,image=windowback,anchor=NW)
    root.update()
    status['text'] = "{}".format(step)
    root.update()
    time.sleep(1)
    global found
    found = 1
    


def send(IP,message):

    if (not(re.match('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',IP))):
        step = "[!] IP Address Invalid"
        windowback = PhotoImage(file='Data/backgroundRed.png')
        window.create_image(0,0,image=windowback,anchor=NW)
        root.update()
        status['text'] = "{}".format(step)
        root.update()
        time.sleep(2)
        return

    
    global count
    if count == 1:
        message = '~' + message

    if found == 0:

        step = "[!] IP Address Invalid"
        windowback = PhotoImage(file='Data/backgroundRed.png')
        window.create_image(0,0,image=windowback,anchor=NW)
        root.update()
        status['text'] = "{}".format(step)
        root.update()
        time.sleep(2)

    up ='http://'+IP+':8060/keypress/up'
    down = 'http://'+IP+':8060/keypress/down'
    right = 'http://'+IP+':8060/keypress/right'
    left = 'http://'+IP+':8060/keypress/left'
    selectt = 'http://'+IP+':8060/keypress/select'

    windowback = PhotoImage(file='Data/backgroundYellow.png')
    window.create_image(0,0,image=windowback,anchor=NW)
    root.update()
    
    Runner.printer(message.lower(),up,down,right,left,selectt,root,status)
    
    
    count = 1

    step = "[~] Enter a new message:"
    windowback = PhotoImage(file='Data/backgroundGreen.png')
    window.create_image(0,0,image=windowback,anchor=NW)
    root.update()
    status['text'] = "{}".format(step)
    root.update()
    time.sleep(1)

root = Tk()
root.option_add('*Font', 'TkTooltipFont')

status = Label(root,text="[+] Enter IP address or leave blank and Scan to begin",bg='#1b1b1b', fg='#ffffff', anchor='sw', width='300')


# turns off title bar, geometry
root.overrideredirect(True)
# set new geometry
root.geometry('300x140+200+200')
# set background color of title bar
back_ground = "#1b1b1b"

# set background of window
content_color = "#ffffff"
# make a frame for the title bar
title_bar = Frame(root, bg=back_ground, relief='raised', bd=0, highlightcolor=back_ground,highlightthickness=0)

# put a close button on the title bar
close_button = Button(title_bar, text='x',  command=root.destroy,bg=back_ground, padx=15, pady=0, activebackground="red", bd=0, fg='white', activeforeground="white", highlightthickness=0)

# window title
logo = PhotoImage(file='Data/logo.png')
windowback = PhotoImage(file='Data/backgroundOff.png')
title_window = "Paul Loblaw Pol Blog Logger"
title_name = Label(title_bar, image=logo, text=title_window, bg=back_ground, fg="white")
# a canvas for the main area of the window
window = Canvas(root, bg="#4B4B4B", highlightthickness=0)
window.create_image(0,0,image=windowback,anchor=NW)

start = Button(window, text=" Find Roku", command=lambda : main(label.get()),  bg='#393939', padx=10, pady=2, activebackground='#393939',bd=0, fg='white', activeforeground='white', highlightthickness=0)
stop = Button(window, text="Send     ", command=lambda : send(IP,label.get()), bg='#393939', padx=10, pady=2, activebackground='#393939',bd=0, fg='white', activeforeground='white', highlightthickness=0)

#Entry Text stuff

v = StringVar(root, value='Enter Roku IP, or leave blank to auto scan')
label = Entry(window, bg='#525e54', bd=0, fg='#ffffff',selectborderwidth=5, width=200, textvariable=v)

def delete_text(event):
    if default_text:
        label.delete(0,END)
        defualt_text = False
default_text=True
label.bind("<Button-1>", delete_text)

# pack the widgets
title_bar.pack(expand=0, fill=X)
title_name.pack(side=LEFT)

close_button.pack(side=RIGHT)
label.pack(side=BOTTOM, padx=40, pady=10)
window.pack(expand=1, fill=BOTH)

start.pack(side=LEFT,padx=30,pady=5)
stop.pack(side=RIGHT,padx=30,pady=5)
status.pack(side=LEFT, padx=0,pady=0)

x_axis = None
y_axis = None
# bind title bar motion to the move window function

def move_window(event):
    root.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

# hover effect on close button
def change_on_hovering(event):
    global close_button
    close_button['bg'] = 'red'
    

def return_to_normal_state(event):
   global close_button
   close_button['bg'] = back_ground


title_bar.bind('<B1-Motion>', move_window)
close_button.bind('<Enter>', change_on_hovering)
close_button.bind('<Leave>', return_to_normal_state)

root.mainloop()