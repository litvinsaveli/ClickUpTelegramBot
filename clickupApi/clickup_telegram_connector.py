import sys
sys.path.insert(1, "D:\\CodeProjects\\ClickUpBot\\config")
sys.path.insert(1, "D:\\CodeProjects\\ClickUpBot\\clickupApi")
sys.path.insert(1, "D:\\CodeProjects\\ClickUpBot\\clickupython")

import client
import config as config


API_KEY = config.clickup_api
BoardID = config.DailyDigest

def create_task(description):
    c = client.ClickUpClient(API_KEY)
    c.create_task(list_id=BoardID, name=description)
