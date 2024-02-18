import os
import tkinter as tk
from tkinter import ttk, filedialog
import pygame

class AudioPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Lecteur Audio")

        self.current_file = None
        self.playlist = []
        self.current_index = 0
        self.is_playing = False

        # Interface
        self.create_widgets()

        # Initialisation de Pygame
        pygame.init()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#1DB954")
        style.map("TButton", foreground=[('pressed', '#1DB954'), ('active', '#1DB954')])

        self.load_button = ttk.Button(self.master, text="Choisir une piste audio", command=self.load_audio, style="TButton")
        self.load_button.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.play_button = ttk.Button(self.master, text="▶ Lancer", command=self.play_audio, state=tk.DISABLED, style="TButton")
        self.play_button.grid(row=0, column=1, pady=10, padx=10, sticky="e")

        self.pause_button = ttk.Button(self.master, text="❚❚ Mettre en pause", command=self.pause_audio, state=tk.DISABLED, style="TButton")
        self.pause_button.grid(row=0, column=2, pady=10, padx=10, sticky="e")

        self.stop_button = ttk.Button(self.master, text="■ Arrêter", command=self.stop_audio, state=tk.DISABLED, style="TButton")
        self.stop_button.grid(row=0, column=3, pady=10, padx=10, sticky="e")

        self.volume_scale = ttk.Scale(self.master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume, length=150)
        self.volume_scale.set(50)
        self.volume_scale.grid(row=1, column=0, columnspan=4, pady=5)

        self.loop_checkbox = ttk.Checkbutton(self.master, text="Lire en boucle", command=self.toggle_loop, style="TButton")
        self.loop_checkbox.grid(row=2, column=0, pady=5, padx=10, sticky="w")

        self.next_button = ttk.Button(self.master, text="⏭ Musique suivante", command=self.next_track, state=tk.DISABLED, style="TButton")
        self.next_button.grid(row=2, column=1, pady=5, padx=10, sticky="e")

        self.shuffle_button = ttk.Button(self.master, text="🔀 Sélection aléatoire", command=self.shuffle_playlist, style="TButton")
        self.shuffle_button.grid(row=2, column=2, pady=5, padx=10)

        # Barre de progression
        self.progress_bar = ttk.Scale(self.master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_position, length=400)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=3, column=0, columnspan=4, pady=10)

    def load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers audio", "*.mp3;*.wav")])
        if file_path:
            self.playlist.append(file_path)
            if not self.current_file:
                self.current_file = file_path
                self.play_button.config(state=tk.NORMAL)
                self.next_button.config(state=tk.NORMAL)
                self.update_progress_bar()
                self.master.title(f"Lecteur Audio - {os.path.basename(file_path)}")

    def play_audio(self):
        if not self.is_playing:
            pygame.mixer.music.load(self.current_file)
            pygame.mixer.music.play()
            self.is_playing = True
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.play_button.config(state=tk.DISABLED)
            self.update_progress_bar()

    def pause_audio(self):
        pygame.mixer.music.pause()
        self.is_playing = False
        self.pause_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.NORMAL)

    def stop_audio(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.pause_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.NORMAL)
        self.progress_bar.set(0)

    def set_volume(self, value):
        pygame.mixer.music.set_volume(int(value) / 100)

    def toggle_loop(self):
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        if self.loop_checkbox.instate(['selected']):
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
        else:
            pygame.mixer.music.set_endevent(0)

    def update_progress_bar(self):
        if self.is_playing:
            current_time = pygame.mixer.music.get_pos() / 1000  # convert milliseconds to seconds
            total_time = pygame.mixer.Sound(self.current_file).get_length()
            progress_percentage = (current_time / total_time) * 100
            self.progress_bar.set(progress_percentage)
            self.master.after(1000, self.update_progress_bar)

    def set_position(self, value):
        if self.is_playing:
            total_time = pygame.mixer.Sound(self.current_file).get_length()
            seek_time = (int(value) / 100) * total_time
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(seek_time)
            pygame.mixer.music.play(start=int(seek_time * 1000))  # convert seconds to milliseconds

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.current_file = self.playlist[self.current_index]
        self.stop_audio()
        self.play_audio()

    def shuffle_playlist(self):
        import random
        random.shuffle(self.playlist)
        self.current_index = 0
        self.current_file = self.playlist[self.current_index]
        self.stop_audio()
        self.play_audio()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayer(root)
    root.mainloop()

