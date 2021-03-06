__author__ = "Amrut Jadhav"
__credits__ = ["Amrut Jadhav"]
__license__ = "MIT"
__maintainer__ = "Amrut Jadhav"
__email__ = "amrutjadhav2294@gmail.com"
__status__ = "Development"


import time
import pdb
import sys

# custom modules import
from databasehandler import DatabaseHandler

from watchdog.observers import Observer                   # import observer 
from watchdog.events import PatternMatchingEventHandler	 

class DeepSearchHandler(PatternMatchingEventHandler):
	""" Deep file search handler to handle the events gengerated by file changes """
	def __init__(self):	
		self.datahandler = DatabaseHandler()
		self._ignore_directories = False
		self._ignore_patterns = False
		self._ignore_patterns = ["*.log","*.logger"]
		self._case_sensitive = False
		self._patterns = ["*.rb","*.py","*.java","*.mp4","*.mp3","*.txt"]
		print "instance created"


	def on_created(self,event):
		"""Called when a file or directory is created."""
		print "file create event"+str(event)
		self.datahandler.create(event.src_path)		

	def on_modified(self,event):
		""""Called when a file or directory is modified."""
		print "file modify event"+str(event)
		self.datahandler.update(event.src_path)

	def on_deleted(self,event):
		"""" Called when a file or directory is deleted. """
		print "file delete event"+str(event)
		self.datahandler.delete(event.src_path)

	def on_moved(self,event):
		""""Called when a file or a directory is moved or renamed."""
		print "file moved event"+str(event)
		self.datahandler.moved(event.src_path)

	def close_db_connection(self):
		""" call close_connection function of datanadler """
		self.datahandler.close_connection()

if __name__=='__main__':
	args = sys.argv[1:]
	directory_path = "/home/atom/Pictures/"
	handler = DeepSearchHandler()
	observer = Observer()
	observer.schedule(handler,path=args[0] if args else directory_path)	# Scheduling the handler
	observer.start()
	
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:								# Stop execution if ctrl+'c' hits teminal
		observer.stop()
	finally:
		handler.close_db_connection()					#close db connection finally
		print("Deep file search deamon terminated")

	observer.join()											#	wait till thread joins