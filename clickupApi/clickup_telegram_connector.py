import clickupython.client as client
import config.config as config


API_KEY = config.clickup_api
BoardID = config.DailyDigest

def create_task(description):
    c = client.ClickUpClient(API_KEY)
    c.create_task(list_id=BoardID, name=description)
