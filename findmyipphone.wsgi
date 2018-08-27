import sys

activate_this = '/opt/findmyipphone/bin/activate_this.py'
exec(open(activate_this).read())
sys.path.insert(0, '/opt/findmyipphone')

from findmyipphone import app as application
