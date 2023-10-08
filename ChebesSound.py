# SOURCE CODE FOR CHEBESSOUND 0.2.0
# COPYRIGHT (C) 2016(EC) 2023(GC) Bigg Smoke

# YOU HAVE THE PERMISSON TO USE THIS SOFTWARE AS LONG YOU ACCEPT THESE TERMS:
# 1. YOU HAVE THE PERMISSION TO REDISTRIBUTE AND/OR MODIFY THE PROGRAM, AS LONG YOU INCLUDE
# THIS LICENSE TEXT ON ALL OF YOUR COPIES.

# 2. UNDER NO CIRCUMSTANCES, THE CREATOR OF THIS PROGRAM SHOULD BE HELD RESPONSIBLE FOR THE
#  DAMAGE CAUSED BY THE INSTALLATION AND/OR THE USE OF THIS SOFTWARE. IF YOU WANT TO FIND 
# BUGS IN THIS SOFTWARE, USE A SANDBOX OR A VIRTUALIZATION SOFTWARE TO AVERT ANY DAMAGE THAT MAY HAPPEN.

# 3. YOU AGNOWLEDGE THAT THE PUBLISHER "CHEBES GROUP/LUNAR SURFACE" DOES NOT ENCOURAGE USERS TO 
# USE ALCOHOL OR ANY DRUG NOR HAS ANY CONNECTIONS TO SUCH INDUSTRIES.


from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import pygame
import os
import webbrowser as wb


class ChebesSound():
    def __init__(self):
        # window init config
        self.root = Tk()

        self.icon = PhotoImage(file="icons\\icon.png")
        self.root.iconphoto( True,self.icon)
        self.root.title("ChebesSound")
        self.root.geometry("520x275")
        # self.root.config(background="#3f3f3f")
        # window contents
        self.menubar = Menu(self.root)
        
        self.root.config(menu=self.menubar)
        self.file_menu = Menu(self.menubar , tearoff=False)
        self.help_menu = Menu(self.menubar , tearoff=False)

        self.file_menu.add_command(label="Select Folder..." , command=self.load_music)
        self.help_menu.add_command(label="How it works...",command=self.how_it_works)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Visit homepage..." , command=self.visit)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About..." , command= self.about)

        self.menubar.add_cascade(label="File" , menu=self.file_menu)
        self.menubar.add_cascade(label="Help" , menu=self.help_menu)

        self.songslist = Listbox(self.root, bg="#222222" , fg="white" , width="100" , height="25" ,  relief=FLAT , borderwidth=0)
        self.songslist.config(height=self.songslist.size())

        self.controlframe = Frame(self.root)
        # self.controlframe.config(background="#3F3F3F")
        self.play_btn =  ttk.Button(master=self.controlframe,    text="Play" , command=self.play_music)
        self.pause_btn = ttk.Button(master=self.controlframe ,   text="Pause" , command=self.pause_music)
        self.prev_btn =  ttk.Button(master=self.controlframe ,   text="Previous" , command=self.prev_music)
        self.next_btn =  ttk.Button(master=self.controlframe ,   text="Next" , command=self.next_music)
        self.play_btn.grid(row=0, column=1 ,padx=7 , pady=10)
        self.pause_btn.grid(row=0, column=2 ,padx=7 , pady=10)
        self.next_btn.grid(row=0, column=3 ,padx=7 , pady=10)
        self.prev_btn.grid(row=0, column=0 ,padx=7 , pady=10)
        self.controlframe.pack()

        self.vol_controlframe = Frame(self.root)
        self.volslider =ttk.Scale(self.vol_controlframe , from_=0 , to=100 , orient=HORIZONTAL , length=400)

        self.vol_set_btn = ttk.Button(self.vol_controlframe , text='Set Volume' , command=self.set_vol)

        self.volslider.grid(row=0 , column=1 , padx=10 , pady=10 )
        self.vol_set_btn.grid(row=0 , column=3 , pady=10 , padx=10)
        self.vol_controlframe.pack()


        self.songs = []
        self.current_song = ""
        self.paused = False
        self.MUSIC_END = pygame.USEREVENT + 1
        self.now_playing  = ""


     # menubar functions (except file menu)

    def visit(self):
        wb.open("https://thesundowner12.github.io")

    def about(self):
        messagebox.showinfo(title="About" , message="ChebesSound v0.2.0\na dumb music player\nMade by the big man himself - Bigg Smoke\nPublished by Chebes Group/Lunar Surface (C) 2016/23")
    
    def how_it_works(self):
        messagebox.showinfo(title="How it works" , message="Choose the folder which contains the music you want to play. and click on 'Play' to start playback.\n\nSince it's in an early stage, bugs are quite often. Please report if you find one." , icon=None)



    # playback functions
    # def check_event(self):
    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == self.MUSIC_END:
    #                 print('end')
    #             else:
    #                 print("not end")
    #    


    def set_vol(self):
        pygame.mixer.music.set_volume(self.volslider.get() / 100)
        

  

    def load_music(self):
        try:
            if len(self.songs)>0:
                self.songs.clear()
                self.songslist.delete(0,END)

            self.root.directory = filedialog.askdirectory()
            for song in os.listdir(self.root.directory):
                name,ext = os.path.splitext(song)
                if ext == '.mp3':
                    self.songs.append(song)
               
            for song in self.songs:
                self.songslist.insert(END , song)
                self.songslist.selection_set(0)
                self.current_song = self.songs[self.songslist.curselection()[0]]
            print("found:"  , self.songs)
            self.songslist.pack(padx=10 ,pady=10)

            self.play_music()
        except FileNotFoundError:
          if not len(self.songs) > 1:
            messagebox.showerror(title="nigga..." , message="well I ain't gonna play myself...")
          else:
            pass

    def play_music(self):
       try:
            self.volslider.set(pygame.mixer.music.get_volume() * 100)
            if not self.paused:
                pygame.mixer.music.set_endevent(self.MUSIC_END)
                pygame.mixer.music.load(os.path.join(self.root.directory , self.current_song))
                pygame.mixer.music.play()

                print(self.current_song)
                # self.check_event()
            else:

                pygame.mixer.music.unpause()
                self.paused = False
                print("resumed playback")
       except:
           messagebox.showerror(title="You dumbass" , message="Specify a folder containing a valid '.mp3' file biatch!")

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True
        print("paused playback")

    def next_music(self):
        try:
            self.songslist.selection_clear(0,END)
            self.songslist.select_set(self.songs.index(self.current_song) + 1)
            self.current_song = self.songs[self.songslist.curselection()[0]]
            self.play_music()
        except:
           pass

    def prev_music(self):
        try:
            self.songslist.selection_clear(0,END)
            self.songslist.select_set(self.songs.index(self.current_song) - 1)
            self.current_song = self.songs[self.songslist.curselection()[0]]
            self.play_music()

        except:
            pass



    def run(self):
        pygame.mixer.init()
        # screen = pygame.display.set_mode((1,1))
        self.root.mainloop()
        
        



app = ChebesSound()
app.run()