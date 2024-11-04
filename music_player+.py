import os
import random
import pygame
import tkinter as tk
from tkinter import filedialog, messagebox

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("600x500")
        self.root.configure(bg="#1f1f1f")

        pygame.mixer.init()
        self.playlist = []
        self.current_track_index = -1
        self.playing = False
        self.paused = False

        # Labels and Buttons
        self.track_label = tk.Label(self.root, text="No track loaded", fg="white", bg="#1f1f1f", font=("Arial", 14))
        self.track_label.pack(pady=20)

        self.load_button = tk.Button(self.root, text="Load Playlist", command=self.load_playlist, bg="#555555", fg="white", width=15)
        self.load_button.pack(pady=5)

        # Listbox to show playlist
        self.playlist_box = tk.Listbox(self.root, bg="#333333", fg="white", selectbackground="#4CAF50", width=50, height=10)
        self.playlist_box.pack(pady=10)
        self.playlist_box.bind('<Double-1>', self.play_selected_song)

        # Control Buttons
        self.play_button = tk.Button(self.root, text="Play", command=self.play_music, bg="#4CAF50", fg="white", width=15)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_music, bg="#FFC107", fg="white", width=15)
        self.pause_button.pack(pady=5)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_music, bg="#2196F3", fg="white", width=15)
        self.next_button.pack(pady=5)

        self.remove_button = tk.Button(self.root, text="Remove Track", command=self.remove_song, bg="#FF5722", fg="white", width=15)
        self.remove_button.pack(pady=5)

        self.shuffle_button = tk.Button(self.root, text="Shuffle", command=self.shuffle_playlist, bg="#9C27B0", fg="white", width=15)
        self.shuffle_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_music, bg="#F44336", fg="white", width=15)
        self.stop_button.pack(pady=5)

        # Volume Control Slider
        self.volume_slider = tk.Scale(self.root, from_=0, to=1, orient="horizontal", resolution=0.1, command=self.set_volume, bg="#1f1f1f", fg="white", label="Volume")
        self.volume_slider.set(0.5)  # Default volume
        self.volume_slider.pack(pady=10)

        # Check for song end
        self.root.after(100, self.check_for_song_end)

    def load_playlist(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.playlist = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".mp3")]
            if self.playlist:
                self.current_track_index = 0
                self.update_playlist_display()
                self.update_track_label()
                messagebox.showinfo("Playlist Loaded", f"{len(self.playlist)} songs loaded.")
            else:
                messagebox.showwarning("No Songs", "No mp3 files found in the selected folder.")

    def update_playlist_display(self):
        self.playlist_box.delete(0, tk.END)
        for track in self.playlist:
            self.playlist_box.insert(tk.END, os.path.basename(track))

    def update_track_label(self):
        if self.playlist:
            track_name = os.path.basename(self.playlist[self.current_track_index])
            self.track_label.config(text=f"Playing: {track_name}")
        else:
            self.track_label.config(text="No track loaded")

    def play_music(self):
        if not self.playlist:
            messagebox.showwarning("No Playlist", "Please load a playlist first.")
            return
        if not self.playing:
            pygame.mixer.music.load(self.playlist[self.current_track_index])
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(self.volume_slider.get())
            self.playing = True
            self.paused = False
            self.update_track_label()
        elif self.paused:
            pygame.mixer.music.unpause()
            self.paused = False

    def play_selected_song(self, event):
        if not self.playlist:
            return
        selected_index = self.playlist_box.curselection()
        if selected_index:
            self.current_track_index = selected_index[0]
            self.stop_music()
            self.play_music()

    def pause_music(self):
        if self.playing and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
        elif self.paused:
            pygame.mixer.music.unpause()
            self.paused = False

    def stop_music(self):
        if self.playing:
            pygame.mixer.music.stop()
            self.playing = False
            self.paused = False
            self.track_label.config(text="Music Stopped")

    def next_music(self):
        if not self.playlist:
            messagebox.showwarning("No Playlist", "Please load a playlist first.")
            return
        self.stop_music()
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        self.play_music()

    def shuffle_playlist(self):
        if not self.playlist:
            messagebox.showwarning("No Playlist", "Please load a playlist first.")
            return
        random.shuffle(self.playlist)
        self.update_playlist_display()
        self.current_track_index = 0
        self.play_music()

    def check_for_song_end(self):
        if self.playing and not pygame.mixer.music.get_busy():
            self.next_music()
        self.root.after(100, self.check_for_song_end)

    def remove_song(self):
        if not self.playlist:
            messagebox.showwarning("No Playlist", "Please load a playlist first.")
            return
        selected_index = self.playlist_box.curselection()
        if selected_index:
            song_to_remove = self.playlist.pop(selected_index[0])
            self.playlist_box.delete(selected_index)
            messagebox.showinfo("Removed", f"Removed {os.path.basename(song_to_remove)} from playlist.")
            if self.current_track_index == selected_index[0]:
                self.stop_music()
                self.current_track_index = -1 if not self.playlist else min(self.current_track_index, len(self.playlist) - 1)
                if self.playlist:
                    self.play_music()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

if __name__ == "__main__":
    root = tk.Tk()
    MusicPlayer(root)
    root.mainloop()
