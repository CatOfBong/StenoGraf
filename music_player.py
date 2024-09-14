import pygame
import time
import threading
import sys
import os

music_playing = False

def play_mp3(file_path):
    global music_playing
    music_playing = True

    def play_music():
        pygame.init()
        pygame.mixer.init()

        # Construct the absolute path to the MP3 file
        if getattr(sys, 'frozen', False):
            # If the script is frozen, use the temporary directory created by PyInstaller
            base_path = sys._MEIPASS
        else:
            # If the script is not frozen, use the current working directory
            base_path = os.path.dirname(os.path.abspath(__file__))

        absolute_path = os.path.join(base_path, file_path)

        pygame.mixer.music.load(absolute_path)
        pygame.mixer.music.play()

        # Wait until the music finishes playing or the application is closed
        while pygame.mixer.music.get_busy() and music_playing:
            time.sleep(1)

        pygame.mixer.quit()
        pygame.quit()

    # Start playing the music in a separate thread
    music_thread = threading.Thread(target=play_music)
    music_thread.start()

def stop_music():
    global music_playing
    music_playing = False
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    pygame.quit()
