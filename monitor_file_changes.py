import sys,os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
'''
Script monitors the json file in the directory mentioned in command line arguments for any changes
If any changes/modification of content is observed, calls the file_compare.py file using os.system
'''

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.json"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        if event.event_type=='modified':
            os.system('python file_compare.py')
        print(event.src_path, event.event_type)  # print now only for degug

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    path_to_monitor = args[0] if args else '.'
    observer.schedule(MyHandler(), path=path_to_monitor,recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()