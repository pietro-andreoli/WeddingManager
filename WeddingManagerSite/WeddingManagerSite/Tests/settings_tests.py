from json import load
import unittest

class TestFileBasedFunctions(unittest.TestCase):
	"""
	Tests any functions in the settings.py created by me which have to do with file use.

	"""
	def test_environment_var_file_path(self):
		"""
		Test that the environment variables file path is valid.
		"""

		from os import path
		from WeddingManagerSite.WeddingManagerSite.settings import gen_env_vars_fp

		fp = gen_env_vars_fp()
		self.assertIsInstance(fp, str)
		self.assertGreater(len(fp), 0, "File path appears to be an empty string.")
		self.assertTrue(path.exists(fp), "File path does not seem to exist.")

	def test_secret_key_file_path(self):
		"""
		Test that the secret key file path is valid.
		"""

		from os import path
		from WeddingManagerSite.WeddingManagerSite.settings import gen_secret_key_fp

		fp = gen_secret_key_fp()
		self.assertIsInstance(fp, str)
		self.assertGreater(len(fp), 0, "File path appears to be an empty string.")
		self.assertTrue(path.exists(fp), "File path does not seem to exist.")

	def test_environment_vars_file(self):
		"""
		Test that the environment variable file is loaded properly.
		"""

		from os import path
		from WeddingManagerSite.WeddingManagerSite.settings import gen_env_vars_fp, load_env_vars

		fp = gen_env_vars_fp()
		env_vars = load_env_vars(fp)
		self.assertIsInstance(env_vars, dict)

	def test_secret_key_file(self):
		"""
		Test that the secret key file is loaded properly.
		"""

		from os import path
		from WeddingManagerSite.WeddingManagerSite.settings import gen_secret_key_fp, load_secret_key

		fp = gen_secret_key_fp()
		secret_key = load_secret_key(fp)
		self.assertIsInstance(secret_key, str)
	
