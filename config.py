# This file should be included in .gitignore to not store sensitive data in version control
import os
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

database_setup = {
   "database_name" : "casting_agency",
   "db_user" : "jamesmerriam", # default postgres user name
   "db_password" : None, # if applicable. If no password, just type in None
   "db_location": "localhost",
   "db_port" : "5432" # default postgres port
}


