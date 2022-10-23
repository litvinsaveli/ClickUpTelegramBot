import os
import sys

import clickupTelegram.DB_connector as DB
import clickupApi.clickup_telegram_connector as infinity
import config.config as config


class collect_user_data:
    def __init__(self, api_key, user_id):

        self.api_key = api_key
        self.user_id = user_id

    def fill_user_workspaces(self, user_workspaces: dict):
        # insert global workspaces associated with user
        WORKSPACES = {}
        for workspace_name, workspace_id in user_workspaces.items():
            DB.insert_spaces(self.user_id, workspace_name, workspace_id)

            user_spaces = infinity.get_user_spaces(self.api_key, str(workspace_id))
            WORKSPACES.update(user_spaces)
        return WORKSPACES

    def fill_user_spaces(self, user_spaces: dict):
        USERSPACES = {}
        for space_name, space_id in user_spaces.items():
            DB.insert_user_spaces(self.user_id, workspace_id, space_name, space_id)

            user_lists = infinity.get_user_lists(user_input, space_id)


t = collect_user_data("pk_42568319_HBYFKNV9WW7JSQQ5XWIKMV54ZTDG4EEI", "163506579")
print(t.fill_user_workspaces({"SPLUST": 4733034}))
