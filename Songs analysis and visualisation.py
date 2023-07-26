import os
import sqlite3
from mutagen.easyid3 import EasyID3  # For mp3 files
from mutagen.mp4 import MP4          # For m4a files
from mutagen.flac import FLAC     # For FLAC files

# Function to get the artist and song name from audio file metadata
def get_metadata(file_path):
    _, ext = os.path.splitext(file_path)
    if ext.lower() == ".mp3":
        audio = EasyID3(file_path)
        artist = audio["artist"][0] if "artist" in audio else "Unknown Artist"
        title = audio["title"][0] if "title" in audio else "Unknown Title"
        genre = audio["genre"][0] if "genre" in audio else "Unknown Genre"
        year = audio["date"][0].split("-")[0] if "date" in audio else "Unknown Year"
    elif ext.lower() == ".m4a":
        audio = MP4(file_path)
        artist = audio["\xa9ART"][0] if "\xa9ART" in audio else "Unknown Artist"
        title = audio["\xa9nam"][0] if "\xa9nam" in audio else "Unknown Title"
        genre = audio["\xa9gen"][0] if "\xa9gen" in audio else "Unknown Genre"
        year = audio["\xa9day"][0].split("-")[0] if "\xa9day" in audio else "Unknown Year"

    elif ext.lower() == ".flac":
        audio = FLAC(file_path)
        artist = audio["artist"][0] if "artist" in audio else "Unknown Artist"
        title = audio["title"][0] if "title" in audio else "Unknown Title"
        genre = audio["genre"][0] if "genre" in audio else "Unknown Genre"
        year = audio["date"][0].split("-")[0] if "date" in audio else "Unknown Year"
    else:
        # For other formats, you may need to implement additional handlers
        return None, None, None, None

    return artist, title, genre, year

def process_audio_files(folder_path, database_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.executescript('''DROP TABLE IF EXISTS songs''')

    # Create the table if it doesn't exist
    cursor.executescript('''
    
    CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT,
            title TEXT,
            genre TEXT,
            year INTEGER
        )
    ''')

    # Loop through the files in the folder and process each audio file
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            artist, title, genre, year = get_metadata(file_path)
            if artist and title:
                # Insert the extracted metadata into the database
                cursor.execute('INSERT INTO songs (artist, title, genre, year) VALUES (?, ?, ?, ?)', (artist, title, genre, year))
    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    folder_path = "D:\Music\mp3"
    database_path = "songs.sqlite"

    process_audio_files(folder_path, database_path)
