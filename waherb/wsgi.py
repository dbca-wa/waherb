from django.core.wsgi import get_wsgi_application
import dotenv
import os
from pathlib import Path

d = Path(__file__).resolve().parents[1]
dot_env = os.path.join(str(d), '.env')
if os.path.exists(dot_env):
    dotenv.read_dotenv(dot_env)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "waherb.settings")
from dj_static import Cling, MediaCling
application = Cling(MediaCling(get_wsgi_application()))
