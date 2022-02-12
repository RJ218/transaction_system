from ConnectToDatabase import get_from_db, perform_transfer, execute_db_command
from mysql.connector import Error
from flask import Flask, request
import datetime;

#This dictionary is used to keep track of incoming request
#key -> str(request_data)
#value -> timestamp when this request hits the transfer POST method
request_dict = {}

app = Flask(__name__)

def transferAPI(sender_account_no, reciever_account_no, ammount):
    try:
        sender_info = get_from_db(sender_account_no)
        reciever_info = get_from_db(reciever_account_no)

        #checking if sender account exists
        if sender_info == None:
            return 'Sender account number ' + sender_account_no + ' does not exists. Please provide correct account number.'

        #checking if reciever account exists
        if reciever_info == None:
            return 'Reciever account number ' + reciever_account_no + ' does not exists. Please provide correct account number.'

        sender_balance_before_transaction = sender_info[1]

        if float(sender_balance_before_transaction) < float(ammount):
            return 'Account- ' + sender_account_no + ', does not have the required balance.'

        transaction_id = perform_transfer(sender_account_no, reciever_account_no, ammount)
        transaction = execute_db_command('''SELECT * 
        FROM transactions  
        WHERE 
         id = %s;'''%(transaction_id))
        sender_info = get_from_db(sender_account_no)
        reciever_info = get_from_db(reciever_account_no)

        sender_current_balance = sender_info[1]
        reciever_current_balance = reciever_info[1]
        createdTime = transaction[0][4]
        transactionDict = {
            'id': transaction_id,
            "from": {
                "id": sender_account_no,
                "balance": sender_current_balance
            },
            "to": {
                "id": reciever_account_no,
                "balance": reciever_current_balance
            },
            "transfered": ammount,
                          "created_datetime": createdTime

        }

        return transactionDict



    except Exception as e:
        print('Error while connecting to MySql. ', e)


@app.route('/transfer', methods = ['POST'])
def transfer():
    try:
        if request.method == 'POST':
            global request_dict
            request_data = request.get_json()
            #print(request_data)

            #To check correct json format is provided to the request
            if 'from' not in request_data or \
                'to' not in request_data or \
                'amount' not in request_data:
                return '''Incorrect json data provided, correct format is: 
                {
                  "from": "account_no",
                  "to": "account_no",
                  "amount": "money"
                }'''

            request_data_str = str(request_data)
            time_before_same_transaction = 15
            ct = datetime.datetime.now()
            timestamp = ct.timestamp()

            if request_data_str in request_dict:
                prev_time = request_dict[request_data_str]
                #To check the twice button clicked case
                if timestamp - prev_time < time_before_same_transaction:
                    return 'Send button may be pressed twice by mistake, please try again after few seconds.'
            else:
                request_dict[request_data_str] = timestamp

            sender_account_no = request_data['from']
            reciever_account_no = request_data['to']
            ammount = request_data['amount']

            #remove '+' sign from provided amount
            if '+' in ammount:
                ammount = ammount.replace('+','')

            if not ammount.isdigit():
                return 'ammount should be a positive digit.'

            #To handle the case when sender and reciever account number are same
            if sender_account_no == reciever_account_no:
                return 'sender account number is equal to reciever account number, sender account number should be different from reciever account number.'

            transaction_json = transferAPI(sender_account_no, reciever_account_no, ammount)
            return transaction_json
    except Exception as e:
        return 'Some unknown errror occured, ' + e
    finally:
        if request_data_str in request_dict:
            del request_dict[request_data_str]

# main driver function
if __name__ == '__main__':
	app.run()

