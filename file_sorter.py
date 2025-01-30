import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

# Define file type categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
}


# Function to move files
def move_file(file_path):
    # Wait for the file to be completely written
    for _ in range(20):
        if os.path.exists(file_path):
            break
        time.sleep(2)

    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Skipping...")
        return  # Skip if file doesn't exist after waiting

    _, ext = os.path.splitext(file_path)  # Get file extension
    ext = ext.lower()

    # Find the correct category
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            dest_folder = os.path.join(DOWNLOADS_FOLDER, category)
            # Create folder if not exists
            os.makedirs(dest_folder, exist_ok=True)
            try:
                shutil.move(file_path, os.path.join(
                    dest_folder, os.path.basename(file_path)))
                print(f"Moved {file_path} -> {dest_folder}")
            except Exception as e:
                print(f"Error moving {file_path}: {e}")
            return

    # If no category found, move to "Others"
    others_folder = os.path.join(DOWNLOADS_FOLDER, "Others")
    os.makedirs(others_folder, exist_ok=True)
    try:
        shutil.move(file_path, os.path.join(
            others_folder, os.path.basename(file_path)))
        print(f"Moved {file_path} -> {others_folder}")
    except Exception as e:
        print(f"Error moving {file_path}: {e}")


class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and not event.src_path.endswith(".tmp"):
            move_file(event.src_path)


# Monitor folder for changes
observer = Observer()
event_handler = DownloadHandler()
observer.schedule(event_handler, DOWNLOADS_FOLDER, recursive=False)

print(f"Monitoring {DOWNLOADS_FOLDER} for new files...")
observer.start()

try:
    while True:
        pass  # Keep script running
except KeyboardInterrupt:
    observer.stop()
    observer.join()
