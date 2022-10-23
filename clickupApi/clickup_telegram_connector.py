import clickupython.client as client
import config.config as config
import requests

API_KEY = config.clickup_api
BoardID = config.DailyDigest


def check_authorisation(api_key):
    url = "https://api.clickup.com/api/v2/user"
    headers = {"Authorization": api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


# simple create new task on selected board
def create_task(api_key, task_name, list_id):
    c = client.ClickUpClient(api_key)
    c.create_task(list_id=list_id, name=task_name)


# get list of spaces to allocate which space would like to be used by user
def get_list_of_workspaces(api_key):
    try:
        c = client.ClickUpClient(api_key)
        user_teams = {}
        teams = c.get_teams().teams

        print(c)
        for i in range(len(teams)):
            user_teams[teams[i].name] = teams[i].id
        return user_teams
    except ValueError:
        return "User does not have any workspaces"


"""Next flow is described to get user lists"""


def get_user_spaces(api_key, space_id):
    try:
        c = client.ClickUpClient(api_key)
        space_list = {}
        spaces = c.get_spaces(space_id, False).spaces

        for i in range(len(spaces)):
            space_list[spaces[i].name] = spaces[i].id

        return space_list
    except ValueError:
        return "User does not have any spaces"


def get_user_lists(api_key, space_id):
    """return associated lists with space"""
    try:
        c = client.ClickUpClient(api_key)
        user_lists = {}
        board_lists = c.get_folderless_lists(space_id).lists

        for i in range(len(board_lists)):
            user_lists[board_lists[i].name] = board_lists[i].id

        return user_lists

    except ValueError:
        return "User does not have any lists"


"""
Step by step execution:
    get_list_of_workspaces returns list of global workspaces > 
    get_user_spaces returns local spaces on global workspace board >
    get_user_lists returns lists on choosed local spaces
        Therefore its enable to push task in choosed list
"""

