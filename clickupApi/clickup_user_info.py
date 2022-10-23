import clickupython.client as client
import config.config as config


API_KEY = config.clickup_api
c = client.ClickUpClient(API_KEY)
user_teams = {}


teams = c.get_teams().teams
print(teams)
for i in range(len(teams)):
    user_teams[teams[i].name] = teams[i].id