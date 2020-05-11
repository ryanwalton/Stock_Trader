import mysql.connector

db = mysql.connector.connect(host = '',
                             user = '',
                            passwd = '',
                            database = 'STOCK_TRADER'
                            
mycursor = db.cursor()

                             
/*FOR DASHBOARD: selects the rows in STOCK where the userID matches the username, will return the stockid, how many shares and its price*/                         
username = /*Needs to get username from the html, not sure how to implement*/
mycursor.execute("SELECT stockID, quantity, market_value 
                 FROM STOCK
                 WHERE user_ID = '%s'
                 ORDER BY stockID ASC", username)
data = mycursor.fetchall()
printf(data)
         
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*FOR BUYING: returns the users money amount to check to see if they have enough to buy*/
mycursor.execute("SELECT net_cash
                 FROM BALANCE
                 WHERE user_ID = '%s'", username)
data = mycursor.fetchall()
printf(data)
       
//////////////////////////////////////////////////////////////////////////////////////////////////////////////                 
/*FOR BUYING: adds shares if the user is buying      
num_of_shares = /* current amount of shares + shares user is buying*/
mycursor.execute("UPDATE STOCK
                 SET quantity = '%s'
                 WHERE user_ID = '%s'", num_of_shares, username)   
data = mycursor.fetchall()
printf(data)
                 
 /////////////////////////////////////////////////////////////////////////////////////////////////////////////                
 /*FOR SELLING: subtracts shares if the user is selling*/
 num_of_shares = /*current amount of shares - shares user is selling*/
 mycursor.execute(UPDATE STOCK
                 SET quantity = '%s'
                 WHERE user_ID = '%s'", num_of_shares, username)
data = mycursor.fetchall()
printf(data)
                  
//////////////////////////////////////////////////////////////////////////////////////////////////////////////                  
/*FOR DASHBOARD/SELLING: If the quantity of shares is zero then delete the row*/
mycursor.execute("DELETE FROM STOCK
                 WHERE quantity = '%s'", num_of_shares)
data = mycursor.fetchall()
printf(data)                 
                 
                 
db.close()
