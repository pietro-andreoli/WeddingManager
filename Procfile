release: python WeddingManagerSite/manage.py migrate
web: gunicorn --chdir WeddingManagerSite WeddingManagerSite.wsgi --log-file - --log-level debug