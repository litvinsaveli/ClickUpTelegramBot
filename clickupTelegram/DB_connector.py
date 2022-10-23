import config.config as config
from mysql.connector import connect, Error
import ast


def new_user(userID, apiKey):
    try:
        with connect(
                host=config.db_server_name,
                database=config.db_name,
                user=list(config.db_creds.keys())[0],
                password=list(config.db_creds.values())[0]
        ) as connection:

            query_1 = f"""INSERT INTO splustdb.users (userID, apiKey) 
                        VALUES ({userID}, '{apiKey}')"""
            query_2 = f"""INSERT INTO splustdb.userPerms (userID, status)
                          VALUES ({userID}, 1)"""
            cursor = connection.cursor()
            cursor.execute(query_1)
            connection.commit()
            cursor.execute(query_2)
            connection.commit()

            print(cursor.rowcount, "Record inserted successfully into users tables")
            cursor.close()

    except Error as error:
        print("Failed to insert record into users table {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


def check_is_user_registed(userID):
    try:
        with connect(
                host=config.db_server_name,
                database=config.db_name,
                user=list(config.db_creds.keys())[0],
                password=list(config.db_creds.values())[0]
        ) as connection:

            query = f"""SELECT userID, status
                        FROM splustdb.userPerms
                        WHERE userID = {int(userID)}
                        LIMIT 1"""

            cursor = connection.cursor()
            cursor.execute(query)

            execution = cursor.fetchall()

            if len(execution) == 0:
                return 0
            else:
                for user, status in execution:
                    return status

            cursor.close()

    except Error as error:
        print("user does not exist {}".format(error))
        return 0

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


def get_user_api (user_id):

    try:
        with connect(
                host=config.db_server_name,
                database=config.db_name,
                user=list(config.db_creds.keys())[0],
                password=list(config.db_creds.values())[0]
        ) as connection:

            query = f"""SELECT apiKey
                        FROM splustdb.users
                        WHERE userID = {int(user_id)}
                        LIMIT 1"""

            cursor = connection.cursor()
            cursor.execute(query)

            execution = cursor.fetchall()

            if len(execution) == 0:
                return 0
            else:
                for user, api_key in execution:
                    return api_key

            cursor.close()

    except Error as error:
        print("user does not exist {}".format(error))
        return 0

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

"""
USER SPACE ACTIONS
"""


def insert_spaces(userID, boardName, boardId):
    try:
        with connect(
                host=config.db_server_name,
                database=config.db_name,
                user=list(config.db_creds.keys())[0],
                password=list(config.db_creds.values())[0]
        ) as connection:

            query = f"""INSERT INTO splustdb.userWorkSpaces (user_id, board_name, board_id, is_Active)
                        VALUES ({userID}, '{boardName}', {boardId}, 0)
                    """

            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            print(cursor.rowcount, "Record inserted successfully into userWorkSpaces table")
            cursor.close()

    except Error as error:
        print("Failed to insert record into UserWorkSpaces {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


def insert_user_spaces(userID, workspace_id, space_name, space_id):
    try:
        with connect(
                host=config.db_server_name,
                database=config.db_name,
                user=list(config.db_creds.keys())[0],
                password=list(config.db_creds.values())[0]
        ) as connection:

            query = f"""INSERT INTO splustdb.user_spaces (user_id, workspace_id, space_name, space_id, is_Active)
                        VALUES ({userID},{workspace_id}, '{space_name}', {space_id}, 0)
                    """

            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            print(cursor.rowcount, "Record inserted successfully into user_spaces table")
            cursor.close()

    except Error as error:
        print("Failed to insert record into user_spaces {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


def insert_user_lists(userID, space_id, list_name, list_id):
    try:
        with connect(
                host=config.db_server_name,
                database=config.db_name,
                user=list(config.db_creds.keys())[0],
                password=list(config.db_creds.values())[0]
        ) as connection:

            query = f"""INSERT INTO splustdb.user_lists (user_id, space_id, list_name, list_id, is_Active)
                        VALUES ({userID}, {space_id}, '{list_name}', {list_id}, 0)
                    """

            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            print(cursor.rowcount, "Record inserted successfully into user_lists table")
            cursor.close()

    except Error as error:
        print("Failed to insert record into user_lists {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


def get_list_workspaces(userID):
    try:
        with connect(
                host=config.db_server_name,
                database=config.db_name,
                user=list(config.db_creds.keys())[0],
                password=list(config.db_creds.values())[0]
        ) as connection:

            query = f"""SELECT JSON_ARRAYAGG(boardName)
                        from splustdb.userWorkSpaces
                        where userID = {userID}"""

            cursor = connection.cursor()
            cursor.execute(query)

            execution = cursor.fetchall()

            if len(execution) == 0:
                return 0
            else:
                return ast.literal_eval(execution[0][0])

            cursor.close()

    except Error as error:
        print("user have no boards".format(error))
        return 0

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


def get_active_userspace(userID):
    try:
        with connect(
                host=config.db_server_name,
                database=config.db_name,
                user=list(config.db_creds.keys())[0],
                password=list(config.db_creds.values())[0]
        ) as connection:

            query = f"""select JSON_ARRAY(list_name, list_id) 
                        from splustdb.vw_user_lists
                        where userID = {userID} and is_active_list = 1"""

            cursor = connection.cursor()
            cursor.execute(query)

            execution = cursor.fetchall()

            if len(execution) == 0:
                return []
            else:
                return ast.literal_eval(execution[0][0])

            cursor.close()

    except Error as error:
        print("user have no boards".format(error))
        return []

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


def get_workspace_list(user_id):
    workspaces_list = {}

    try:
        with connect(
                host=config.db_server_name,
                database=config.db_name,
                user=list(config.db_creds.keys())[0],
                password=list(config.db_creds.values())[0]
        ) as connection:

            query = f"""select JSON_ARRAY(workspace_name, workspace_id)
                        from (select workspace_Name as workspace_name, workspace_ID as workspace_id
                              from splustdb.vw_user_lists
                              where userID = {user_id}
                              group by workspace_Name, workspace_ID
                              ) T1"""

            cursor = connection.cursor()
            cursor.execute(query)

            execution = cursor.fetchall()

            if len(execution) == 0:
                return 0
            else:
                for i in range(len(execution)):
                    lister = ast.literal_eval(execution[i][0])
                    workspaces_list[lister[0]] = lister[1]
                return workspaces_list

            cursor.close()

    except Error as error:
        print("user have no boards".format(error))
        return 0

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


def get_space_list(user_id, workspace_id=None):
    userspaces_list = {}

    try:
        with connect(
                host=config.db_server_name,
                database=config.db_name,
                user=list(config.db_creds.keys())[0],
                password=list(config.db_creds.values())[0]
        ) as connection:
            if workspace_id:
                query = f"""select JSON_ARRAY(space_name, space_id)
                            from (select space_name as space_name, space_id as space_id
                              from splustdb.vw_user_lists
                              where userID = {user_id} and workspace_ID = {workspace_id}
                              group by space_name, space_id
                              ) T1"""
            else:
                query = f"""select JSON_ARRAY(space_name, space_id)
                                            from (select space_name as space_name, space_id as space_id
                                              from splustdb.vw_user_lists
                                              where userID = {user_id}
                                              group by space_name, space_id
                                              ) T1"""

            cursor = connection.cursor()
            cursor.execute(query)

            execution = cursor.fetchall()

            if len(execution) == 0:
                return 0
            else:
                for i in range(len(execution)):
                    lister = ast.literal_eval(execution[i][0])
                    userspaces_list[lister[0]] = lister[1]
                return userspaces_list

            cursor.close()

    except Error as error:
        print("user have no boards".format(error))
        return 0

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


def get_space_lists_list(user_id, space_id=None):
    userlists_list = {}

    try:
        with connect(
                host=config.db_server_name,
                database=config.db_name,
                user=list(config.db_creds.keys())[0],
                password=list(config.db_creds.values())[0]
        ) as connection:

            if space_id:
                query = f"""select JSON_ARRAY(list_name, list_id)
                        from (select list_name as list_name, list_id as list_id
                              from splustdb.vw_user_lists
                              where userID = {user_id} and space_id = {space_id}
                              group by list_name, list_id
                              ) T1"""
            else:
                query = f"""select JSON_ARRAY(list_name, list_id)
                        from (select list_name as list_name, list_id as list_id
                              from splustdb.vw_user_lists
                              where userID = {user_id}
                              group by list_name, list_id
                              ) T1"""


            cursor = connection.cursor()
            cursor.execute(query)

            execution = cursor.fetchall()

            if len(execution) == 0:
                return 0
            else:
                for i in range(len(execution)):
                    lister = ast.literal_eval(execution[i][0])
                    userlists_list[lister[0]] = lister[1]
                return userlists_list

            cursor.close()

    except Error as error:
        print("user have no lists"
              "".format(error))
        return 0

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


# Update actions
def update_active_list(user_id, list_id):
    try:
        with connect(
                host=config.db_server_name,
                database=config.db_name,
                user=list(config.db_creds.keys())[0],
                password=list(config.db_creds.values())[0]
        ) as connection:

            query_1 = f"""update splustdb.user_lists
                            set is_Active = 0
                          where user_id = {user_id}"""

            query_2 = f"""update splustdb.user_lists
                            set is_Active = 1 
                          where user_id = {user_id} and list_id = {list_id}"""

            cursor = connection.cursor()
            cursor.execute(query_1)
            connection.commit()
            cursor.execute(query_2)
            connection.commit()

            cursor.close()

    except Error as error:
        print("Row are not updated {}".format(error))
        return 0

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


# DB rollback statements
def rollback_set_api(user_id):
    querry = [f"delete from user_lists where user_id = {user_id}",
              f"delete from user_spaces where user_id = {user_id}",
              f"delete from userWorkSpaces where user_id = {user_id}",
              f"delete from userPerms where userID = {user_id}",
              f"delete from users where userID = {user_id}"]
    try:
        with connect(
                host=config.db_server_name,
                database=config.db_name,
                user=list(config.db_creds.keys())[0],
                password=list(config.db_creds.values())[0]
        ) as connection:

            cursor = connection.cursor()
            for querry in querry:
                cursor.execute(querry)
                connection.commit()
    except Error as error:
        print("Failed to insert record into user_lists {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


