import os
import django


project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'livinginsider_project'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'livinginsider_project.settings')

django.setup()