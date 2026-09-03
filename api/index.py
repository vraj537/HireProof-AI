import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","hireproof.settings")
from django.core.wsgi import get_wsgi_application
app=get_wsgi_application()
