# transaction_system

To run the transaction system, follow the following steps:
1.clone or download the repo.
2.install the required packages mentioned in the requirement.txt(also make sure that python is installed on the system).
3.after installation, go to the directory of the code, open cmd and write the following line:
    python transaction_management.py
4.now use some application used for API testing like postman, and write the link to hit the API, by default the path to the API should be:
    http://127.0.0.1:5000/transfer
  This might differ from system to sytem, so take path as mentioned in the cmd after executing step 3. The line should look like:
  Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
5.Now open postman, and follow the mentioned steps:
  i.  enter the url from step 4.
  ii. select 'post' type.
  iii.in body select raw, and select drop down to JSON.In the opened space copy the lines:
      {
       "from": "1003",
       "to": "1001",
       "amount": "100"
      }
  iv.click send.
6.After successfull execution the API returns json data in the following forrmat:
     {
      "id": "transaction_id",
      "from":{
        "id": "account_no",
        "balance": "current_balance"
      },
      "to":{
        "id": "account_no",
        "balance": "current_balance"
      },
      "transfered": "transfer_amount"
      "created_datetime": "transaction created time"
    }

The scehma for db transaction is updated here, reciever_account_no and sender_account_no are added, this is done to make the table simple as now each row contains the whole information related to a transaction otherwise, another column was needed to be added to make sure that the two transaction were linked together that is one for deducting the money from sender account and another that adds amount to the reciever account.

Current code suports the following checks:
1.if sender account no entered is equal to the reciever account no.
2.if amount to de deducated is less than the balance of sender account.
3.if user presses the transfer button twice(by mistake).
4.if sender account/reciever account does not exists.

Current code does not suport the following:
1.concurrent transactions, the code might fail in such case.
