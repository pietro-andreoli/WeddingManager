import datetime
import sqlite3

def backup_db():
	def print_backup_progress(status, remaining, total):
		print(f'Copied {total - remaining} of {total} pages...')
	try:
		connection = sqlite3.connect('db.sqlite3')
		print('Connected to database')
		timestamp = datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
		backupConnection = sqlite3.connect(f'backup_{timestamp}.sqlite3')
		print('Connected to backup database')
		print('Backing up database...')
		connection.backup(backupConnection, progress=print_backup_progress)
		print('Backup complete!')
	except sqlite3.Error as error:
		print("Error while backing up database", error)
		return False
	finally:
		if connection:
			connection.close()
			print("The SQLite connection is closed")
		if backupConnection:
			backupConnection.close()
			print("The backup SQLite connection is closed")
	return True

