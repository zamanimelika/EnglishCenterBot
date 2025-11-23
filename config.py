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
API_TOKEN = "8453754975:AAHfEenvD_MOWunXmGumfbEu0X0V8jMS0UQ"

# Channels & Admins
CHANNEL_CID = -1003320355055
ENGLISH_CHANNEL_CID = -1003320355055
ADMIN_CID = 662801794
admins = [662801794]

# Channel Link for buttons
ENGLISH_CHANNEL_LINK = "https://t.me/englishclass_ed"
COURSES_CHANNEL_CID = -1003320355055
COURSES_CHANNEL_LINK = "https://t.me/englishclass_ed"
