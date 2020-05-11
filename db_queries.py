# Retrieve user's balance from the DB
def get_user_balance(db, user_id):
    cur = db.cursor()
    cur.execute("SELECT net_cash FROM BALANCE WHERE user_ID = %s" % (user_id))
    user_cash = float(cur.fetchone()[0])
    cur.close()
    return user_cash

# Retrieve user's stock quantity given a symbol
def get_user_stock_quantity(db, user_id, symbol):
    cur = db.cursor()
    cur.execute("SELECT quantity FROM STOCK WHERE stock_ID = '%s' AND user_ID = %s" % (symbol, user_id))
    user_quantity = cur.fetchone()[0]
    cur.close()
    return user_quantity

# Get all the stock symbols that the user owns
def get_all_stocks(db, user_id):
    cur = db.cursor()
    cur.execute("SELECT stock_ID, quantity FROM STOCK WHERE user_ID = %s" % (user_id))
    stock_names = cur.fetchall()
    cur.close()
    return stock_names

# Insert stocks into the DB
def insert_stocks(db, user_id, user_cash, symbol, quantity, total_value):
    cur = db.cursor()
    
    # Calculate and update the new value of the user
    user_cash = user_cash - total_value
    cur.execute("UPDATE BALANCE SET net_cash = %f WHERE user_ID = %s" % (user_cash, user_id))
    
    # Check if a row exist in the DB
    cur.execute("SELECT stock_ID FROM STOCK WHERE stock_ID = '%s' AND user_ID = %s" % (symbol, user_id))
    exist = cur.fetchone()

    # If a row already exist update the row in the DB
    if exist:
        # Get the user's quantity and market_value from the DB
        cur.execute("SELECT quantity, market_value FROM STOCK WHERE stock_ID = '%s' AND user_ID = %s" % (symbol, user_id))
        data = cur.fetchone()

        # Update the value of the market_value and quantity
        updated_quantity = int(data[0]) + quantity
        updated_market_value = float(data[1]) + total_value
        cur.execute("UPDATE STOCK SET quantity = %s, market_value = %f WHERE stock_ID = '%s' AND user_ID = %s" % (updated_quantity, updated_market_value, symbol, user_id))
    
    # If a row DOES NOT EXIST then insert a new row
    else:
        cur.execute("INSERT INTO STOCK (user_ID, stock_ID, quantity, market_value) VALUES (%s, '%s', %s, %s)" % (user_id, symbol, quantity, total_value))

    db.commit()
    cur.close()

# Sell stocks given the symbol
def sell_stocks(db, user_id, symbol, total_value, updated_quantity):
    cur = db.cursor()

    # Get and update the user's new balance
    cur.execute("SELECT net_cash FROM BALANCE WHERE user_ID = 0")
    updated_cash = float(cur.fetchone()[0]) + total_value
    print(updated_cash)
    cur.execute("UPDATE BALANCE SET net_cash = %f WHERE user_ID = %s" % (updated_cash, user_id))

    # If the new quantity is 0 then delete the row since the user doesn't own any more of that stock
    if updated_quantity == 0:
        cur.execute("DELETE FROM STOCK WHERE stock_ID = '%s' AND user_ID = %s" % (symbol, user_id))
    
    # If user still have more stocks for that symbol then update the quantity
    else:
        cur.execute("UPDATE STOCK SET quantity = %s WHERE stock_ID = '%s' AND user_ID = %s" % (updated_quantity, symbol, user_id))
    
    db.commit()
    cur.close()