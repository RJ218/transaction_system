import mysql.connector
from mysql.connector import Error


def get_connection_obect():
    try:
        connection = mysql.connector.connect(host='localhost', database='payswifter', user='root', password='test')
        return connection
    except Exception as e:
        print("error while setting connection to sql server - " + str(e))
        exit()

def perform_transfer(sender_account_no, reciever_account_no, ammount):
    try:
        connection = get_connection_obect()
        connection.start_transaction()
        if connection.is_connected():
            cursor = connection.cursor()
            updated_sender_account = '''
            UPDATE balances
                SET balance = balance - %s
            WHERE account_no = %s;
            '''%(ammount, sender_account_no)

            updated_reciever_account = '''
            UPDATE balances
                SET balance = balance + %s
            WHERE account_no = %s;
            '''%(ammount, reciever_account_no)

            add_to_transaction_table = '''
            INSERT INTO transactions(sender_account_no, reciever_account_no, amount,created_datetime) 
            VALUES(%s,%s,%s,now());'''%(sender_account_no, reciever_account_no, ammount)

            cursor.execute(updated_sender_account)
            cursor.execute(updated_reciever_account)
            #perform_transfer(sender_account_no, reciever_account_no, ammount)
            cursor.execute(add_to_transaction_table)
            cursor.lastrowid
            result = cursor.fetchall()
            connection.commit()
            print(connection.in_transaction)
            return cursor.lastrowid
    except Exception as e:
        print('Error performing this transfer. ', e)
        return e

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print('MySql connection is closed.')

def execute_db_command(sqlCommand):
    try:
        connection = get_connection_obect()
        connection.start_transaction()
        print(connection.in_transaction)
        if connection.is_connected():
            #uncomment to get the server info
            #db_Info = connection.get_server_info()
            #print('Connected to MySql server version', db_Info)
            cursor = connection.cursor()
            cursor.execute(sqlCommand)
            result = cursor.fetchall()
            connection.commit()
            print(connection.in_transaction)
            print('On executing ', sqlCommand, ' result is ', result)
            return result
    except Exception as e:
        print('Error while connecting to MySql. ', e)
        return 'Error while connecting to MySql. ', e

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print('MySql connection is closed.')

def get_from_db(account_no):
    sql_command = '''SELECT * FROM balances  WHERE account_no = '%s' '''%(account_no)
    output = execute_db_command(sql_command)
    if len(output) == 1:
        return output[0]
    return None

def add_account_to_db(account_info_dict):
    sql_command = ''
    for account_no in account_info_dict:
        balance = account_info_dict[account_no]
        sql_command = '''INSERT INTO balances (
                        account_no, 
                        balance)
                        VALUES (
                        '%s', '%s')'''%(account_no, balance)
        execute_db_command(sql_command)

execute_db_command('''CREATE TABLE Balances ( 
                             account_no INTEGER NOT NULL,
                             balance DECIMAL NOT NULL, 
                             PRIMARY KEY (account_no),
                             CHECK(balance >= 0))''')

#added reciever_account number to this schema so that a single row can contain the needed information related to that transaction
execute_db_command('''CREATE TABLE Transactions ( 
                             id INTEGER NOT NULL AUTO_INCREMENT,
                             amount DECIMAL NOT NULL,
                             sender_account_no INTEGER NOT NULL,
                             reciever_account_no INTEGER NOT NULL,
                             created_datetime DATETIME  NOT NULL,
                             PRIMARY KEY (id))''')

#initial account info that will added in the db
account_info_dict = {
    '1001' : '5000',
    '1002' : '7000',
    '1003' : '9000'
}

add_account_to_db(account_info_dict)