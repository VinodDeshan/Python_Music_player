import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk
from mutagen.mp3 import MP3 , HeaderNotFoundError
from mutagen.id3 import ID3
import os
from pygame import mixer
import threading
import random

class Music_player():
    # Collecting song cards #######################################################################################
    cards = []
    # Collecting button_pannels ###################################################################################
    button_pannels = []
    # Collecting All Songs ########################################################################################
    songs = []
    # Music file directory#########################################################################################
    music_dir = r"C:\Users\USER\\Desktop\\song"
    # Current song id #############################################################################################
    current_song_id = -1
    # All threading ###############################################################################################
    threading = []
    # Collecting all  durations bar################################################################################
    slide_bars = []
    # colours #####################################################################################################
    color_1 = '#353a40'
    color_2 = '#91a5a7'
    color_3 = '#5e68e6'
    color_4 = '#cd873c'
    color_5 = '#000000'
    
    #Constructor###################################################################################################
    def __init__(self):
        # Create Root window#######################################################################################
        self.root = ctk.CTk()# Create ctk object
        self.root.geometry('1060x650+20+20')# Set root window width and height
        self.root.resizable(False,False)
        self.root.overrideredirect(True)
        self.root.configure(bgcolor = '#1B2137')
        self.root.wm_attributes('-transparentcolor' , '#0F0E0E')
        self.root.wm_attributes('-alpha' , 1)
        
        # Create Main frame########################################################################################
        self.main_frame = ctk.CTkFrame(
            master=self.root,
            fg_color= self.color_5,
            corner_radius=20,
            height=650,
            bg_color='#0F0E0E'
        )
        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=0
        )
        
        # Create app close button#################################################################################
        self.close_button = ctk.CTkButton(
            master=self.main_frame,
            text_color='white',
            corner_radius=5,
            text="✕",
            width=30,
            height=30,
            fg_color=self.color_5,
            hover_color=self.color_5,
            font=('Segoe UI Bold', 12),
            command=self.close_app
        )
        self.close_button.pack(
            padx=5,
            pady=(5, 0),
            anchor='se'
        )
        
        # Bind events for dragging the window########################################################################
        self.main_frame.bind("<Button-1>", self.start_move)
        self.main_frame.bind("<ButtonRelease-1>", self.stop_move)
        self.main_frame.bind("<B1-Motion>", self.on_motion)
        
        # Create side bar###########################################################################################
        self.side_bar = ctk.CTkFrame(
            master=self.main_frame, 
            fg_color=self.color_5, 
            corner_radius=20, 
            height=650, 
            width=52
        )
        self.side_bar.pack(side="left", padx=(20, 0))
        
        #Run the sidebar buttons create function####################################################################
        self.create_sidebar_button('Home', 'icons/Home.png', self.color_3)
        self.create_sidebar_button('Song', 'icons/song.png', self.color_5)
        self.create_sidebar_button('Artist', 'icons/user.png', self.color_5)
        self.create_sidebar_button('Favourite', 'icons/Favourite.png', self.color_5)
        self.create_sidebar_button('Settings', 'icons/Settings.png', self.color_5)
        
        # Create search bar########################################################################################
        self.search_bar_frame = ctk.CTkFrame(
            master=self.main_frame,
            width=506, 
            height=40, 
            corner_radius=100, 
            fg_color=self.color_1
        )
        self.search_bar_frame.pack(side='top', padx=(0, 55), pady=(0, 0))
        self.search_bar_frame.pack_propagate(False)
        
        # Search bar icon and text area
        self.search_icon = ctk.CTkLabel(
            master=self.search_bar_frame, 
            text='', fg_color=self.color_1,
            image=ImageTk.PhotoImage(Image.open('icons/Search.png').resize((15, 15)))
        )
        self.search_icon.pack(side='left', padx=(21, 0))
        self.search_area = ctk.CTkEntry(
            master=self.search_bar_frame, 
            fg_color=self.color_1, 
            bg_color=self.color_1,
            border_color=self.color_1, 
            placeholder_text='Search Music',
            font=('Arial Bold', 11), 
            text_color=self.color_2, 
            placeholder_text_color=self.color_2, 
            width=400
        )
        self.search_area.pack(side='left', padx=(15, 0))
        
        # Create main window########################################################################################
        self.main_window = ctk.CTkFrame(
            master=self.main_frame, 
            width=1200, 
            height=520, 
            fg_color=self.color_5
        )
        self.main_window.pack(side='top', padx=(0, 0))
        self.main_window.pack_propagate(False)
        
        # Run the home page function ###############################################################################
        self.home_page()
        
        # Run the root window#######################################################################################
        self.root.mainloop()
        
        
        
        
        
        
    
    
    
    ################################################################################################################
    ################################################################################################################
    ################################################################################################################
    ################################################################################################################
    ################################################################################################################
    ################################################################################################################
    # All functions ################################################################################################
    # App move functions ###########################################################################################
    def start_move(self, event):
        self.root.x = event.x
        self.root.y = event.y
    def stop_move(self, event):
        self.root.x = None
        self.root.y = None
    def on_motion(self, event):
        deltax = event.x - self.root.x
        deltay = event.y - self.root.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        
    # App close function ###########################################################################################
    ################################################################################################################
    ################################################################################################################
    def close_app(self):
        for thr in self.threading:
            thr.cancel()
        self.root.destroy()
        
    # Create side menu buttons######################################################################################
    ################################################################################################################
    ################################################################################################################
    def create_sidebar_button(self , name , icon_path , fg_color):
        btn_frame = ctk.CTkFrame(
            master=self.side_bar, 
            width=40, 
            height=40, 
            fg_color=fg_color, 
            corner_radius=100
        )
        btn_frame.pack(pady=(0, 12))
        btn_frame.pack_propagate(False)
        
        btn = ctk.CTkButton(
            master=btn_frame, 
            text='', 
            width=0, 
            height=0, 
            fg_color=fg_color, 
            hover_color=fg_color,
            image=ImageTk.PhotoImage(Image.open(icon_path).resize((15, 15)))
        )
        btn.pack(pady=(7, 0))
    
    # Home page Function ###########################################################################################
    ################################################################################################################
    ################################################################################################################
    def home_page(self):
        # Create scroll frame
        self.scroll_frame = ctk.CTkScrollableFrame(
            master=self.main_window, 
            width=990, 
            height=480, 
            corner_radius=20,
            fg_color=self.color_5,
            orientation="horizontal",
            scrollbar_button_color='#222222',
            scrollbar_button_hover_color='#222222',
            border_width=0,
        )
        self.scroll_frame.pack()
        # Run the load song function
        self.load_songs()
        
        # run the song card function
        self.len = len(self.songs)
        for x in range(self.len):
            self.song_cards(id = x)
        
            
        # Key Handler###################################################################################################
        ################################################################################################################
        ################################################################################################################
        self.volume = 0.75
        self.song_play_or_stop = True
        self.song_pos = 0
        def key_handler(event):
            if(event.keysym == 'Right'):
                self.scroll_right()
            elif(event.keysym == 'Left'):
                self.scroll_left()
            elif(event.keysym == 'Up'):
                if(self.volume <= 1.0):
                    mixer.music.set_volume(self.volume)
                    self.volume = self.volume + 0.01
                    print("volume = " + str(mixer.music.get_volume() * 100))
            elif(event.keysym == 'Down'):
                if(self.volume >= 0.0):
                    mixer.music.set_volume(self.volume)
                    self.volume = self.volume - 0.01
                    print("volume = " + str(mixer.music.get_volume() * 100))
            elif(event.keysym == 'space'):
                for thr in self.threading:
                        thr.cancel()
                if(self.song_play_or_stop and mixer.music.get_busy() != True and self.current_song_id != -1):
                    title , artist , duration , length = self.get_mp3_details(self.songs[self.current_song_id])
                    self.play_next_song(song_duration=length - self.song_pos)
                    self.set_interval(func=self.set_song_duration , sec=1)
                    print(self.song_pos)
                    mixer.music.play(start=self.song_pos)
                    self.song_play_or_stop = False
                    print('song played')
                else:
                    for thr in self.threading:
                        thr.cancel()
                    self.song_pos = (mixer.music.get_pos() / 1000) + self.song_pos
                    mixer.music.stop()
                    print(self.song_pos)
                    self.song_play_or_stop = True
                    print('song stoped')
            else:
                print(event.keysym)
        self.root.bind('<Key>' , key_handler)
        
    # Scroll to right###############################################################################################
    ################################################################################################################
    ################################################################################################################
    def scroll_right(self):
        current_pos = self.scroll_frame._parent_canvas.xview()[0]
        self.scroll_frame._parent_canvas.xview_moveto(current_pos + self.len/(self.len*(self.len/2)))
            
    # Scroll left ##################################################################################################
    ################################################################################################################
    ################################################################################################################
    def scroll_left(self):
        current_pos = self.scroll_frame._parent_canvas.xview()[0]
        self.scroll_frame._parent_canvas.xview_moveto(current_pos - self.len/(self.len*(self.len/2)))
        
    # Rounded cornner image macker function#########################################################################
    ################################################################################################################
    ################################################################################################################
    def add_rounded_corners(self, image_path, radius):
        # Open the image
        img = Image.open(image_path).resize((290, 225))
        # Create a mask with rounded corners
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
        # Apply the mask to the image
        img.putalpha(mask)
        return img
    
    # Loop the song cards###########################################################################################
    ################################################################################################################
    ################################################################################################################
    def song_cards(self , id):
        title , artist , duration , length = self.get_mp3_details(self.songs[id])
        self.card = ctk.CTkFrame(
            master=self.scroll_frame, 
            width=307, 
            height=480, 
            fg_color=self.color_3, 
            corner_radius=20,
        )
        self.card.pack(side='left', padx=(0, 18))
        self.card.pack_propagate(False)
        self.cards.append(self.card)

        photo = ImageTk.PhotoImage(self.add_rounded_corners(f'img'+str(11)+'.png', radius=20))
        self.img = ctk.CTkLabel(master=self.card, text='', image=photo)
        self.img.pack(pady=(7, 0))
            
        self.title = ctk.CTkLabel(master=self.card , text=title[0:35] , font=('Calibri Bold' , 15) , text_color='#FFFFFF',height=5)
        self.title.pack(pady = (21 , 0) , padx = 10)
            
        self.artist = ctk.CTkLabel(master=self.card , text=artist , font=('Calibri Bold' , 11) , text_color='#FFFFFF')
        self.artist.pack(pady = (0 , 0))
        
        self.duration_bar_frame = ctk.CTkFrame(
            master=self.card,
            height=20,
            fg_color='#222222'
        )
        self.duration_bar_frame.pack(pady = (10 , 0))
        self.duration_bar_frame.pack_propagate(False)
        self.slide_bars.append(self.duration_bar_frame)
        
        
        self.play_btn = ctk.CTkButton(
            master=self.card , 
            width=40 , 
            height=40 , 
            fg_color='#2D2D2D' , 
            corner_radius=100 , 
            text='' , 
            hover_color='#2D2D2D' ,
            command=lambda:self.play_song(id = id)
        )
        self.play_btn.pack(pady = (0 , 0))
        self.play_btn.pack_propagate(False)
        self.play_icon = ctk.CTkLabel(
            master=self.play_btn ,
            text='' , 
            width=0 ,
            height=0,
            image=ImageTk.PhotoImage(Image.open('icons\play.png'))
        )
        self.play_icon.pack(pady = (12 ,0) , padx = (1 , 0))
        
        self.delete_btn = ctk.CTkButton(
            master=self.card , 
            width=40 , 
            height=40 , 
            fg_color='#2D2D2D' , 
            corner_radius=100 , 
            text='' , 
            hover_color='#2D2D2D',
            command=lambda:self.delete_song(id = id)
        )
        self.delete_btn.pack(side = 'left' , pady = (0 , 10) , padx = (10 , 0) , anchor = 'sw')
        self.delete_btn.pack_propagate(False)
        self.delete_icon = ctk.CTkLabel(
            master=self.delete_btn , 
            text='' , 
            width=0 , 
            height=0 , 
            image=ImageTk.PhotoImage(Image.open('icons\Trash.png'))
        )
        self.delete_icon.pack(pady = (12 , 0))
        
        self.like_btn = ctk.CTkButton(
            master=self.card , 
            width=40 , 
            height=40 , 
            fg_color='#2D2D2D' , 
            corner_radius=100 , 
            text='' , 
            hover_color='#2D2D2D',
            command=lambda:self.like_song(id = id)
        )
        self.like_btn.pack(side = 'left' , pady = (0 , 10) , padx = (10 , 0) , anchor = 'sw')
        self.like_btn.pack_propagate(False)
        self.like_icon = ctk.CTkLabel(
            master=self.like_btn , 
            text='' , 
            width=0 , 
            height=0 , 
            image=ImageTk.PhotoImage(Image.open('icons\like.png'))
        )
        self.like_icon.pack(pady = (12 , 0))
        
        self.button_pannel = ctk.CTkFrame(
            master=self.card,
            fg_color='#222222',
            corner_radius=20
        )
        self.button_pannel.pack(side = 'left' , pady = (0 , 10) , padx = (0 ,2) , anchor = 'sw')
        self.button_pannels.append(self.button_pannel)
        
    # play song function ###########################################################################################
    ################################################################################################################
    ################################################################################################################
    pr_card_index = 0
    mixer.init()
    def play_song(self , id = 0):
        self.song_pos = 0
        # Clear all threading
        for thr in self.threading:
            thr.cancel()
        #print current song id
        print('Play Song = ' + str(id))
        # Set current song id
        self.current_song_id = id
        # play current song
        mixer.music.load(self.songs[self.current_song_id])
        mixer.music.play()
        # start song duration count
        self.min = 0
        self.sec = 0
        self.set_interval(func=self.set_song_duration , sec=1)
        # Get song details
        title , artist , duration , length = self.get_mp3_details(self.songs[id])
        # auto play next song
        self.play_next_song(song_duration=length)
        # print the song lenght
        print('song length = ' + str(length))
        
        self.cards[self.pr_card_index].configure(fg_color = '#222222')
        self.button_pannels[self.pr_card_index].configure(fg_color = '#222222')
        for frame in self.button_pannels[self.pr_card_index].winfo_children():
                frame.destroy()
        
        self.cards[id].configure(fg_color = '#565658')
        self.button_pannels[id].configure(fg_color = '#565658')
        
        for frame in self.slide_bars[self.pr_card_index].winfo_children():
            frame.destroy()
        self.slide_bars[self.pr_card_index].configure(fg_color = '#222222')
        
        self.duration_bar = ctk.CTkSlider(
            master=self.slide_bars[id],
            button_color= '#000000',
            button_corner_radius=100,
            progress_color= '#000000',
            fg_color= '#222222',
            height=10,
            from_=0,
            to=100
        )
        self.duration_bar.pack(pady = (0 , 0) , side = 'top')
        self.duration_bar.set(0.0)
        self.slide_bars[id].configure(fg_color = '#565658')
        
        self.duration = ctk.CTkLabel(
            master=self.slide_bars[id],
            font=('Arial Bold' , 10),
            text_color='black',
            text='00.00'
        )
        self.duration.pack(side = 'left'  , padx = (7 , 0))
        
        self.time = ctk.CTkLabel(
            master=self.slide_bars[id],
            font=('Arial Bold' , 10),
            text_color='black',
            text=duration
        )
        self.time.pack(side = 'right' , padx = (0 , 7))
        
        # Set color to if btn on off
        self.Shuffle_color = '#2D2D2D'
        if(self.Shuffle_on_or_off):
            self.Shuffle_color = '#2D2D2D'
        else:
            self.Shuffle_color = 'black'
            
            
        self.Shuffle_btn = ctk.CTkButton(
            master=self.button_pannels[id] , 
            width=40 , 
            height=40 , 
            fg_color=self.Shuffle_color , 
            corner_radius=100 , 
            text='' , 
            hover_color=self.Shuffle_color,
            command=lambda:self.Shuffle()
        )
        # Create Shuffle_btn
        self.Shuffle_btn.pack(side = 'left' , pady = (0 , 0) , padx = (10 , 0) , anchor = 'sw')
        self.Shuffle_btn.pack_propagate(False)
        self.Shuffle_icon = ctk.CTkLabel(
            master=self.Shuffle_btn , 
            text='' , 
            width=0 , 
            height=0 , 
            image=ImageTk.PhotoImage(Image.open('icons\Shuffle.png')),
        )
        self.Shuffle_icon.pack(pady = (12 , 0))
        
        # Set color to if shuffle btn on off
        self.repeat_color = '#2D2D2D'
        if(self.Repeat_on_or_off):
            self.repeat_color = '#2D2D2D'
        else:
            self.repeat_color = 'black'
            
        # Create repeate btn
        self.repeat_btn = ctk.CTkButton(
            master=self.button_pannels[id] , 
            width=40 , 
            height=40 , 
            fg_color=self.repeat_color , 
            corner_radius=100 , 
            text='' , 
            hover_color=self.repeat_color,
            command=lambda:self.Repeat()
        )
        self.repeat_btn.pack(side = 'left' , pady = (0 , 0) , padx = (10 , 0) , anchor = 'sw')
        self.repeat_btn.pack_propagate(False)
        self.repeat_icon = ctk.CTkLabel(
            master=self.repeat_btn , 
            text='' , 
            width=0 , 
            height=0 , 
            image=ImageTk.PhotoImage(Image.open('icons\Repeat.png'))
        )
        self.repeat_icon.pack(pady = (12 , 0))
        # Create volume Bar
        self.Volume_btn = ctk.CTkButton(
            master=self.button_pannels[id] , 
            width=40 , 
            height=40 , 
            fg_color='#2D2D2D' , 
            corner_radius=100 , 
            text='' , 
            hover_color='#2D2D2D'
        )
        self.Volume_btn.pack(side = 'left' , pady = (0 , 0) , padx = (55 , 0) , anchor = 'sw')
        self.Volume_btn.pack_propagate(False)

        self.volume_icon = ctk.CTkLabel(
            master=self.Volume_btn , 
            text='' , 
            width=0 , 
            height=0 , 
            image=ImageTk.PhotoImage(Image.open('icons\Volume.png'))
        )
        self.volume_icon.pack(pady = (0 , 12) , side = 'bottom')
        
        self.pr_card_index = id
    
    # Play Next song################################################################################################
    ################################################################################################################
    ################################################################################################################
    first_click = False
    def play_next_song(self,song_duration):
        # Check the shuffle on or off
        if(self.Shuffle_on_or_off):
            # Start the threading to play next song
            t = threading.Timer(song_duration , lambda:self.play_song(id=self.current_song_id + 1))
            t.start()
            # append the threading to list
            self.threading.append(t)

            if(self.current_song_id != 0 and self.first_click):
                self.scroll_frame._parent_canvas.xview_moveto(self.len/(self.len*(self.len/self.current_song_id)) - (self.len/(self.len*(self.len/1))))
                print((self.len/(self.len*(self.len/self.current_song_id)) - (self.len/(self.len*(self.len/1)))))
            else:
                self.first_click = True
                pass
        else:
            self.scroll_frame._parent_canvas.xview_moveto((self.len/(self.len*(self.len/2)) - (self.len/(self.len*(self.len/1)))) * (self.current_song_id - 1))
            print(0.024390243902439025 * (self.current_song_id - 1))
            
            self.current_song_id = self.songs.index(random.choice(self.songs))
            t = threading.Timer(song_duration , lambda:self.play_song(id=self.current_song_id))
            t.start()
            self.threading.append(t)
            
    
    # Delete song function##########################################################################################
    ################################################################################################################
    ################################################################################################################
    def delete_song(self,id):
        print('Deleted = ' + str(id))
        
    # Liked song function##########################################################################################
    ################################################################################################################
    ################################################################################################################
    def like_song(self,id):
        print('Liked = ' + str(id))
        
    # Shuffle function #############################################################################################
    ################################################################################################################
    ################################################################################################################
    Shuffle_on_or_off = True
    def Shuffle(self):
        if(self.Shuffle_on_or_off):
            print('Shuffle ON')
            self.Shuffle_btn.configure(fg_color = 'black' , hover_color='black')
            self.Shuffle_icon.configure(fg_color = 'black')
            self.Shuffle_on_or_off = False
        else:
            print('Shuffle OFF')
            self.Shuffle_btn.configure(fg_color = '#2D2D2D' , hover_color='#2D2D2D')
            self.Shuffle_icon.configure(fg_color = '#2D2D2D')
            self.Shuffle_on_or_off = True
            
    # Repeat function #############################################################################################
    ################################################################################################################
    ################################################################################################################
    Repeat_on_or_off = True
    def Repeat(self):
        if(self.Repeat_on_or_off):
            print('Repeat ON')
            self.repeat_btn.configure(fg_color = 'black' , hover_color='black')
            self.repeat_icon.configure(fg_color = 'black')
            self.Repeat_on_or_off = False
        else:
            print('Repeat OFF')
            self.repeat_btn.configure(fg_color = '#2D2D2D' , hover_color='#2D2D2D')
            self.repeat_icon.configure(fg_color = '#2D2D2D')
            self.Repeat_on_or_off = True
        
    # Load song function ###########################################################################################
    ################################################################################################################
    ################################################################################################################
    def load_songs(self):
        for file_name in os.listdir(self.music_dir):
            if file_name.lower().endswith('.mp3'):
                file_path = os.path.join(self.music_dir, file_name)
                self.songs.append(file_path)
                
    # Get song details function ####################################################################################
    ################################################################################################################
    ################################################################################################################
    def get_mp3_details(self,file_path):
        try:
            audio = MP3(file_path, ID3=ID3)
            title = audio.get('TIT2').text[0] if audio.get('TIT2') else 'Unknown Title'
            artist = audio.get('TPE1').text[0] if audio.get('TPE1') else 'Unknown Artist'
            duration = int(audio.info.length)
            minutes, seconds = divmod(duration, 60)
            return title, artist, f"{minutes}.{seconds:02}" , duration
        except HeaderNotFoundError:
            return 'Unknown Title', None, None , None
        
    # Create set interval function #################################################################################
    ################################################################################################################
    ################################################################################################################
    def set_interval(self , func , sec):
        def func_wrapper():
            self.set_interval(func , sec)
            func()
        t = threading.Timer(sec , func_wrapper)
        t.start()
        self.threading.append(t)
        
    # set song duration ############################################################################################
    ################################################################################################################
    ################################################################################################################
    min = 0
    sec = 0
    duration_count  = 0
    def set_song_duration(self):
        self.sec = self.sec + 1
        
        if(self.sec == 60):
            self.min = self.min + 1
        if(self.sec == 60):
            self.sec = 0
        time = ''   
        # if(self.sec < 10):
        #     time = str(self.min) + '.0' + str(self.sec)
        # else:
        #     time = str(self.min) + '.' + str(self.sec)
            
        if(self.sec < 10):
            time = str(self.min) + '.0' + str(self.sec)
        else:
            time =  str(self.min) + '.' + str(self.sec)
        self.duration.configure(text = time)
        
        title , artist , duration , length = self.get_mp3_details(self.songs[self.current_song_id])
        self.duration_count = self.duration_count + (100/length)
        self.duration_bar.set(self.duration_count)
        
        
        
    ################################################################################################################
    ################################################################################################################
# Run the app#######################################################################################################
Music_player()
