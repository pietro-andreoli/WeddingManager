from datetime import datetime
import pytz
from django.conf import settings
import os

def datetime_from_str(date_str, tz_str):
	"""
	Creates the datetime object from a timestamp string and timezone name.

	Args:
		date_str (str): timestamp as a string in the format YYYY-MM-DD hh:mm:ss (24h time).
		tz_str (str): Name of the timezone. See pytz for a list of valid timezone names.

	Returns:
		datetime: Timezone aware date of the string.
	"""

	tz = pytz.timezone(tz_str)
	return tz.localize(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"))

class EventDetails():
	# Path to the event details file.
	DETAILS_FP = os.path.join(settings.BASE_DIR, "InvitationManager", "configs/event_details_config.json")
	def __init__(self):
		import json

		# Read event details JSON file into memory.
		contents = None
		with open(EventDetails.DETAILS_FP, 'r') as details_f:
			contents = json.load(details_f)
		
		# Load essential information into this object.
		start_timestamp_str = contents["event_date"]["t_stamp"]
		tz_str = contents["event_date"]["tz"]
		self.event_start_timestamp = datetime_from_str(start_timestamp_str, tz_str)
		self.venue_name = contents["venue"]["name"]
		self.venue_address = contents["venue"]["address"]
		self.reply_deadline = datetime_from_str(contents["reply_deadline"], tz_str)
	
	@property
	def event_time(self):
		return self.event_start_timestamp.time()
	
	@property
	def event_date(self):
		return self.event_start_timestamp.date()

