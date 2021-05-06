# this file is executed first in the whole application and its set using command $env:FLASK_APP = "run.py"
# used this command to run the app --> python -m flask run
# used this command to change app to development server --> $env:FLASK_ENV = "development" 
# to activate debugger then --> set FLASK_DEBUG= 1 

from flaskblog import app