from tkinter import *
import spotipy 
import spotipy.util as util
import time
from pycaw.pycaw import AudioUtilities
from random import randint
import os, sys
import pygame

Username = '# user on spotify developer'
AccessScope = 'user-read-currently-playing user-modify-playback-state'
ClientID = '# ID on spotify developer'
ClientSecret = '# SECRET on spotify developer'
RedirectURI = 'http://google.com/'
run = 0

# Outside Functions

def startMusic():
    rand = randint(1,2)
    print("Ad!")
    app.ad()
    pygame.mixer.init()
    pygame.mixer.music.load(f"./musics/{rand}.mp3")
    pygame.mixer.music.play(loops=0)
    time.sleep(30)
    pygame.mixer.music.stop()
    print("Desmuted!")

def set(username, scope, clientID, clientSecret, redirectURI):
    token = util.prompt_for_user_token(username, scope, clientID, clientSecret, redirectURI)
    return spotipy.Spotify(auth=token)

def mainSpt():
    global spotifyObject

    try:
        trackInfo = spotifyObject.current_user_playing_track()
    except:
        print("Token Expired")
        spotifyObject = spotifyObject(Username, AccessScope, ClientID, ClientSecret, RedirectURI)
        trackInfo = spotifyObject.current_user_playing_track()
    try:
        if trackInfo['currently_playing_type'] == 'ad':
            MuteSpotifyTab(True)
            startMusic()
        else:
            MuteSpotifyTab(False)
    except TypeError:
        pass

def MuteSpotifyTab(mute):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "Spotify.exe":
            if mute: volume.SetMute(1, None)
            else: volume.SetMute(0, None)

def check():
	if run == 1:
		mainSpt()
	root.after(100, check)

# Classes

class MainApp:
	def __init__(self, master):
		self.master = master
		self.master.title("Spotipy")

		self.status = Label(text="Not running.", bg="white")
		self.status.grid(row=0, column=0, pady=2)

		self.button = Button(text="Start", width=20, height=10, font="size=30", command=self.start)
		self.button.grid(row=1, column=0, padx=5, pady=2)

		self.ads = Label(text="Ads prevented: 0")
		self.ads.grid(row=2, column=0)

	def stop(self):
		global run

		run = 0
		self.status["text"] = "Not running."
		self.button["text"] = "Start"
		self.button["command"] = self.start


	def start(self):
		global run

		run = 1
		self.status["text"] = "Runing..."
		self.button["text"] = "Pause"
		self.button["command"] = self.stop

	def ad(self):
		val = int(self.ads["text"].split(" ")[2]) + 1
		print(len(str(val))*-1, self.ads["text"][:(len(str(val))*-1)])
		self.ads["text"] = self.ads["text"][:(len(self.ads["text"].split(" ")[2])*-1)] + str(val)


def main(): 
	global app, root

	root = Tk()
	app = MainApp(root)
	root.after(100, check)
	root.mainloop()

if __name__ == '__main__':
	spotifyObject = set(Username, AccessScope, ClientID, ClientSecret, RedirectURI)
	MuteSpotifyTab(False)
	main()