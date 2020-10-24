from Database.DBconnection import DatabaseConnection as dbc
from Database.Tables import Tables as tb
import random

table = tb.RECEIVERS

# will need to be able to:
# inactivate a receiver
    # new receiver will be set with a '0' to indicate active
    # to inactivate receiver the status will change to a '1'
# create new receiver
# get list of receivers
# select one or multiple receivers with details
    # this would be a query to get multiple search results for a specified list

def create_receiver_table():
    try:
        with dbc(table) as connection:
            cursor = connection.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS receivers(
                                    originator text,
                                    name text primary key,
                                    receivingID text,
                                    ID_num text,
                                    acct text,
                                    transcode text,
                                    amount text,
                                    inactive_status text)                      
            ''' )
    except:
        raise ValueError("<DB FAILED>")

def new_receiver(originator, name, receivingID, acct, transcode, amount):
    try:
        with dbc(table) as connection:
            cursor = connection.cursor()

            cursor.execute('''INSERT INTO receivers
                (originator, name, receivingID, ID_num, acct, transcode, amount, inactive_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0)
            ''', (originator, name, receivingID, random.randrange(1000), acct, transcode, amount))
    except:
        raise ValueError("<DB FAILED>")

def get_active_receivers(originator):
    '''
    Will only pull active receivers tied to an originator.

    :param originator:
    :return:
    '''
    try:
        with dbc(table) as connection:
            cursor = connection.cursor()

            cursor.execute('''SELECT * FROM receivers 
            WHERE originator=? and inactive_status=?''', (originator, '0'))
            receiver_list = [{'name': row[1]} for row in cursor.fetchall()]

        return receiver_list
    except:
        raise ValueError("<DB FAILED>")

def get_all_receivers(originator):
    '''
    Will all receivers tied to an originator.

    :param originator:
    :return:
    '''
    try:
        with dbc(table) as connection:
            cursor = connection.cursor()

            cursor.execute('''SELECT * FROM receivers 
            WHERE originator=?''', (originator,))
            receiver_list = [{'name': row[1]} for row in cursor.fetchall()]

        return receiver_list
    except:
        raise ValueError("<DB FAILED>")


def get_receiver_detail(originator, receiver):
    try:
        with dbc(table) as connection:
            cursor = connection.cursor()

            cursor.execute('''SELECT * FROM receivers 
                WHERE originator=? and name=?''',
                (originator, receiver)
            )

            rows = cursor.fetchall()

            receiver_detail = [{'transcode': row[5], 'receivingID': row[2], 'acct': row[4],
                            'amt': row[6], 'id_num': row[3], 'name': row[1]} for row in rows]

        return receiver_detail
    except:
        raise ValueError("<DB FAILED>")


def inactivate_receiver(originator, receiver):
    try:
        with dbc(table) as connection:
            cursor = connection.cursor()

            cursor.execute('''UPDATE receivers SET inactive_status=1 
                WHERE originator=? and name=?''',
                (originator, receiver)
            )
    except:
        raise ValueError("<DB FAILED>")

def update_receiver(originator, name, receivingID, acct, transcode, amount):
    try:
        with dbc(table) as connection:
            cursor = connection.cursor()
            cursor.execute('''
            UPDATE receivers
            SET originator=?, name=?, receivingID=?, ID_num=?, 
            acct=?, transcode=?, amount=?, inactive_status=?
            WHERE originator=? and name=?
            ''', (originator, name, receivingID, random.randrange(1000),
                  acct, transcode, amount, 0, originator, name)
            )
    except:
        raise ValueError('Something went wrong')

