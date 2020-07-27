from tkinter import *
import pygame
from tkinter.filedialog import askdirectory
import os
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root=Tk()
root.title('MP3 player')
image = PhotoImage(file="bg4.png")

root.geometry("500x400")

'''C = Canvas(root, bg="blue", height=250, width=300)
filename = PhotoImage(file = "bg4.png")
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

photo = PhotoImage(file = "bg3.png")
w = Label(root, image=photo)'''


def resize(event):
    slider.config(length=1500)

root.bind("<Configure>", resize)


playlist=[]
global paused
paused=False

song_length=0
#initialize pygame mixer
pygame.mixer.init()

# To add background image


def play_time():
        if stopped:
                return
        
        # position of current song
        current_time=pygame.mixer.music.get_pos()/1000
        #slider_label.config(text=f'Slider:{int(slider.get())} and song pos: {int(current_time)}')

        # To convert to time format
        converted_current_time=time.strftime('%M:%S',time.gmtime(current_time))

        current_song=mp3list.get(ACTIVE)
        song=os.path.realpath(current_song)

        #load song with mutagen
        song_mut=MP3(song)
        
        #get song length and converting it in time 
        global song_length
        song_length=song_mut.info.length
        converted_song_length=time.strftime('%M:%S',time.gmtime(song_length))
        #To synch slider and current time
        current_time+=1

        #To update current postion when song end and slider reches to end
        if int(slider.get())==int(song_length):
                status_bar.config(text=f'{converted_song_length} / {converted_song_length}')
        elif paused:
                pass
        elif int(slider.get()) == int(current_time):
                #slider has not moved 
                slider_position=int(song_length)
                slider.config(to=slider_position,value=int(current_time))
        else:
                #slider has been repositioned
                slider_position=int(song_length)
                slider.config(to=slider_position,value=int(slider.get()))
                converted_current_time=time.strftime('%M:%S',time.gmtime(slider.get()))

                status_bar.config(text=f'{converted_current_time} / {converted_song_length}')
                next_time=int(slider.get())+1
                slider.config(value=next_time)
        
        
        status_bar.after(1000,play_time)

def Play() :
        global stopped
        stopped=False
        song=mp3list.get(ACTIVE)
        pygame.mixer.music.load(os.path.realpath(song))
        pygame.mixer.music.play(loops=0)
        play_time()
        

        
def previous_music():
        pygame.mixer.music.stop()
        status_bar.config(text='')
        slider.config(value=0)
        prev_song=mp3list.curselection()
        if prev_song[0]==0:
            pass
        else:
            prev_song=prev_song[0]-1
        song=mp3list.get(prev_song)
        pygame.mixer.music.load(os.path.realpath(song))
        pygame.mixer.music.play(loops=0)
        mp3list.selection_clear(0,END)
        mp3list.activate(prev_song)
        mp3list.selection_set(prev_song,last=None)
def next_music():
        status_bar.config(text='')
        slider.config(value=0)
        next_song=mp3list.curselection()
        if next_song[0]==len(playlist)-1:
            pass
        else:
            next_song=next_song[0]+1
        song=mp3list.get(next_song)
        pygame.mixer.music.load(os.path.realpath(song))
        pygame.mixer.music.play(loops=0)
        
        mp3list.selection_clear(0,END)
        mp3list.activate(next_song)
        mp3list.selection_set(next_song,last=None)
global stopped
stopped=False        
def stop_music():
        status_bar.config(text='')
        slider.config(value=0)
        pygame.mixer.music.stop()
        global stopped
        stopped=True
        #paused=False
        #mp3list.selection_clear(ACTIVE)
def pause_music(is_paused):
        global paused
        paused=is_paused
        if paused:
                pygame.mixer.music.unpause()
        else:
                pygame.mixer.music.pause()
        paused=not paused
def directorychooser():
        directory=askdirectory()
        os.chdir(directory)
        for files in os.listdir(directory):
                if files.endswith(".mp3"):
                    realdir = os.path.realpath(files)
                    playlist.append(files)
        playlist.reverse()
        for items in playlist:
                mp3list.insert(0, items)
        playlist.reverse()

def slide(x):
        #slider_label.config(text=f'{int(slider.get())} / {song_length}')
        song=mp3list.get(ACTIVE)
        pygame.mixer.music.load(os.path.realpath(song))
        pygame.mixer.music.play(loops=0 ,start=int(slider.get()))

def set_vol(val):
    volume=int(val)/100
    pygame.mixer.music.set_volume(volume)



#create playlist listbox
mp3list=Listbox(root, bg='black',fg='yellow', width=60)
mp3list.pack(pady=10,fill="both", expand=True )

#button images
backward=PhotoImage(file = "previous.png")
forward=PhotoImage(file = "next.png")
play=PhotoImage(file = "play.png")
pause=PhotoImage(file = "pause.png")
stop=PhotoImage(file = "stop.png")

#create button frame
frame=Frame(root)
frame.pack()
previous_button = Button(frame, image=backward,command=previous_music)
play_button=Button(frame, image=play,command=Play)
next_button=Button(frame, image=forward,command=next_music)
pause_button=Button(frame ,image=pause,command=lambda: pause_music(paused))
stop_button=Button(frame, image=stop,command=stop_music)


previous_button.grid(row=0, column=0, padx=10)
play_button.grid(row=0, column=1, padx=10)
next_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)
#vol_label.grid(row=1,column=0)
#scale.grid(row=1,column=1,columnspan=4)

vol_label=Label(root,text='volume')
scale=Scale(root,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
scale.set(70)
vol_label.pack(side=BOTTOM)
scale.pack(side=BOTTOM)

# status bar
song_frame=Frame(root)
song_frame.pack(pady=30)
status_bar=Label(song_frame,text='',bd=0,relief=RAISED,anchor=W)
status_bar.pack(ipady=2)
slider=ttk.Scale(song_frame,from_=0,to_=100,orient=HORIZONTAL,value=0,command=slide,length=200)
slider.pack(expand=True)

#temporary label
#slider_label=Label(root,text='0')
#slider_label.pack(pady=10)

#create menubar
menubar =Menu(root)
root.config(menu=menubar)
submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label='Add song',menu=submenu)
submenu.add_command(label='open',command=directorychooser)




#w.pack(fill="both",expand=True)
#C.pack(fill="both",expand=True)
root.mainloop()

