import unittest

class TestDjangoInstallation(unittest.TestCase):
	def test_django(self):
		"""
		Tests whether Django is installed in this environment.

		Raises:
			ModuleNotFoundError: Raised if the django module is not found on import.
		"""

		try:
			import django
		except ModuleNotFoundError:
			raise ModuleNotFoundError("The `django` module is not installed.")
	
	