import os
from flask import Flask, flash, render_template, request, session, redirect, url_for, abort
app = Flask(__name__)
app.secret_key = '^\x83J\xd3) \x1a\xa4\x05\xea\xd8,\t=\x14]\xfd\x8c%\x90\xd6\x9f\xa1Z'

# Import Modules
import justHealthServer.api
import justHealthServer.views
