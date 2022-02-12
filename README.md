# transaction_system

To run the transaction system, follow the following steps:<br />
1.clone or download the repo.<br />
2.install the required packages mentioned in the requirement.txt(also make sure that python(3.7 or above) is installed on the system).<br />
3.after installation, go to the directory of the code, open cmd and write the following line:<br />
    &emsp;python transaction_management.py<br />
4.now use some application used for API testing like postman, and write the link to hit the API, by default the path to the API should be:<br />
    &emsp;http://127.0.0.1:5000/transfer<br />
  This might differ from system to sytem, so take path as mentioned in the cmd after executing step 3. The line should look like:<br />
  Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)<br />
5.Now open postman, and follow the mentioned steps:<br />
  &emsp;i.  enter the url from step 4.<br />
  &emsp;ii. select 'post' type.<br />
  &emsp;iii.in body select raw, and select drop down to JSON.In the opened space copy the lines:<br />
      &emsp;{<br />
       &emsp;&emsp;"from": "1003",<br />
       &emsp;&emsp;"to": "1001",<br />
       &emsp;&emsp;"amount": "100"<br />
      &emsp;}<br />
  &emsp;iv.click send.<br />
6.After successfull execution the API returns json data in the following forrmat:<br />
     &emsp;{<br />
      &emsp;&emsp;"id": "transaction_id",<br />
      &emsp;"from":{<br />
        &emsp;&emsp;"id": "account_no",<br />
        &emsp;&emsp;"balance": "current_balance"<br />
      &emsp;},<br />
      &emsp;"to":{<br />
        &emsp;&emsp;"id": "account_no",<br />
        &emsp;&emsp;"balance": "current_balance"<br />
      &emsp;},<br />
      &emsp;"transfered": "transfer_amount"<br />
      &emsp;"created_datetime": "transaction created time"<br />
    &emsp;}<br />
<br />
The scehma for db transaction is updated here, reciever_account_no and sender_account_no are added, this is done to make the table simple as now each row contains the whole information related to a transaction otherwise, another column was needed to be added to make sure that the two transaction were linked together that is one for deducting the money from sender account and another that adds amount to the reciever account.<br />
<br />
Current code suports the following checks:<br />
1.if sender account no entered is equal to the reciever account no.<br />
2.if amount to de deducated is less than the balance of sender account.<br />
3.if user presses the transfer button twice(by mistake).<br />
4.if sender account/reciever account does not exists.<br />
<br />
Current code does not suport the following:<br />
1.concurrent transactions, the code might fail in such case.<br />
<br />
