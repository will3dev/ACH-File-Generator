from Database.DBconnection import DatabaseConnection as dbc
from Database.Tables import Tables as tb

table = tb.ORIGINATORS

# will need to be able to do 3 things:
# pull list of originators that will flow to a dropdown
# add a new originator
# pull required originator information to use for generating the ACH file.
# should be able to delete and originator

def create_originator_table():
    try:
        with dbc(table) as connection:
            cursor = connection.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS originators(
                                    originator_name text primary key, 
                                    originator_ID text, 
                                    acct_num text, 
                                    scc text)''')
    except:
        raise ValueError("<DB FAILED>")


def new_originator(name, ID, acct_num, scc):
    try:
        with dbc(table) as connection:
            cursor = connection.cursor()

            cursor.execute('''INSERT INTO originators 
                (originator_name, originator_ID, acct_num, scc)
                VALUES (?, ?, ?, ?)''', (name, ID, acct_num, scc))
    except:
        raise ValueError("<DB FAILED>")


def get_originators():
    try:
        with dbc(table) as connection:
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM originators')
            originators_list = [{'name': row[0], 'ID': row[1][-4:]} for row in cursor.fetchall()]

        return originators_list
    except:
        raise ValueError("<DB FAILED>")


def get_originator_detail(name):
    try:
        with dbc(table) as connection:
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM originators WHERE originator_name=?', (name,))

            row = cursor.fetchone()

            originator_detail = {'originator_name': row[0], 'originatorID': row[1],
                                  'account': row[2], 'serviceClass': row[3],
                                  'odfi': '211374020', 'entry': 'EFT',
                                  'discretionary': ''}

        return originator_detail
    except:
        raise ValueError("<DB FAILED>")


def delete_originator(name, ID):
    try:
        with dbc(table) as connection:
            cursor = connection.cursor()

            cursor.execute('DELETE FROM originators WHERE originator_name=? and originator_ID=?', (name, ID))
    except:
        raise ValueError("<DB FAILED>")

def update_originator(name, ID, acct_num, scc):
    try:
        with dbc(table) as connection:
                cursor = connection.cursor()
                cursor.execute('''UPDATE originators SET 
                originator_name=?, originator_ID=?, acct_num=?, scc=?
                WHERE originator_name=?''', (name, ID, acct_num, scc, name))

    except:
        raise ValueError('Something went wrong')

