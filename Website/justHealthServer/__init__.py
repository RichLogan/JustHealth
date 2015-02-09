import os
import sys
from flask import Flask, flash, render_template, request, session, redirect, url_for, abort
#from flask_sslify import SSLify
app = Flask(__name__)
#sslify = SSLify(app)
app.secret_key = '^\x83J\xd3) \x1a\xa4\x05\xea\xd8,\t=\x14]\xfd\x8c%\x90\xd6\x9f\xa1Z'
app.config['PROFILE_PICTURE'] = sys.prefix + "/../justHealthServer/static/images/profilePictures/"
# Import Modules
import justHealthServer.api
import justHealthServer.views
