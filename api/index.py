import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","hireproof.settings")
import django
django.setup()
try:
 from django.core.management import call_command
 call_command("migrate",interactive=False,verbosity=0)
except Exception as e:
 print(f"[HireProof-AI] migrate skipped: {e}")
try:
 call_command("collectstatic",interactive=False,verbosity=0)
except Exception as e:
 print(f"[HireProof-AI] collectstatic skipped: {e}")
from django.core.wsgi import get_wsgi_application
app=get_wsgi_application()
