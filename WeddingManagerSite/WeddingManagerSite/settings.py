"""
Django settings for WeddingManagerSite project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import json
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

def gen_secret_key_fp():
	"""
	Generates the file path for the secret key file.

	Returns:
		str: The file path.
	"""

	return os.path.join(BASE_DIR, "Hidden", "SECRET_KEY.txt")

def load_secret_key(fp):
	"""
	Loads the secret key from it's file into memory.

	Returns:
		str: Secret key string.
	"""

	try:
		return os.environ["SECRET_KEY"]
	except:
		pass

	with open(fp, 'r') as secret_key_f:
		return secret_key_f.read().strip()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = load_secret_key(gen_secret_key_fp())

def gen_env_vars_fp():
	"""
	Generates the file path to the environment variables.

	Returns:
		str: File path.
	"""

	return os.path.join(BASE_DIR, "Hidden", "ENVIRONMENT_VARIABLES.json")

def load_env_vars(fp):
	"""
	Loads the environment variables into a dictionary.

	Returns:
		dict: A dictionary containing environment variables as key-value pairs.
	"""

	print("Attempting to load environment variables from os.environ")
	try:
		return {
			"environment": os.environ["environment"],
			"debug": os.environ["debug"]
		}
		
		print("Environment variables successfully loaded from os.environ")
	except:
		print("Could not load environment variables from os.environ")

	print("Attempting to load environment variables from file")
	with open(fp, 'r') as env_var_f:
		return json.load(env_var_f)

ENVIRONMENT_VARIABLES = load_env_vars(gen_env_vars_fp())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENVIRONMENT_VARIABLES["debug"] == "true"

ALLOWED_HOSTS = [
	"wedding-wizard.herokuapp.com",
	"127.0.0.1"
]


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	"InvitationManager.apps.InvitationmanagerConfig",
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	# Simplified static file serving.
	# https://warehouse.python.org/project/whitenoise/
	'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'WeddingManagerSite.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			os.path.join(BASE_DIR, "InvitationManager/templates/InvitationManager")
		],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'WeddingManagerSite.wsgi.application'

MAX_CONN_AGE = 600

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}

if "DATABASE_URL" in os.environ:
	# Configure Django for DATABASE_URL environment variable.
	DATABASES["default"] = dj_database_url.config(
		conn_max_age=MAX_CONN_AGE, 
		ssl_require=True
	)

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"

USE_TZ = True