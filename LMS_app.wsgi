#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/LMS/")

from LMS import routes as application
application.secret_key = 'sdffggohr30ifrnf3e084fn0348'

