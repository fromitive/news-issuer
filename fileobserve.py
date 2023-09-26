from watchdog.observers import Observer
from watchdog.events import *
import time
import datetime
import subprocess

TIMEDELAY = 10


def executeGit():
    COMMIT_DATE = datetime.datetime.now()
    STR_COMMIT_DATE = datetime.datetime.strftime(COMMIT_DATE, "%Y-%m-%d")

    print("[+] GIT PULL")
    subprocess.run(["git", "pull"])

    print("[+] GIT ADD --ALL")
    subprocess.run(["git", "add", "--all"])

    print("[+] GIT COMMIT -M")
    subprocess.run(["git", "commit", "-m", "news.txt updated.. {}".format(STR_COMMIT_DATE)])

    print("[+] GIT PUSH")
    subprocess.run(["git", "push"])


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)
        self.modified_time = datetime.datetime.now()

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            if "./news.txt" in event.src_path:
                print("file modified:{0}".format(event.src_path))
                executeGit()


if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, ".", True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
