# config.py

import os

# Database configuration

db_config = {
    'user': os.environ.get('db_user', 'root'),
    'password': os.environ.get('db_password', ''),
    'host': os.environ.get('db_host', 'localhost'),
    'database': os.environ.get('database_name', 'language_institute')
}

# Bot Token
API_TOKEN = "API_TOKEN"

# Channels & Admins
CHANNEL_CID = -"CHANNEL_CID"
ENGLISH_CHANNEL_CID = -"ENGLISH_CHANNEL_CID"
ADMIN_CID = "ADMIN_CID"
admins = ["admins"]

# Channel Link for buttons
ENGLISH_CHANNEL_LINK = "ENGLISH_CHANNEL_LINK"
COURSES_CHANNEL_CID = "COURSES_CHANNEL_CID"
COURSES_CHANNEL_LINK = "COURSES_CHANNEL_LINK"


