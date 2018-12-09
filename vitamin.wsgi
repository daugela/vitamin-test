activate_this = '/home/andrius/www-vitamin/djenv/bin/activate_this.py'
with open(activate_this) as file_:
	exec(file_.read(), dict(__file__=activate_this))


import sys
sys.path.insert(0, '/home/andrius/www-vitamin')

from vitamintest import app as application

