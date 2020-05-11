from flask import Flask, render_template, request, redirect, send_file
from alpha_vantage.timeseries import TimeSeries
from db_queries import get_user_balance, insert_stocks, get_user_stock_quantity, sell_stocks, get_all_stocks
from stock_ops import price_lookup, convert_to_dollar
from plotlyCharts import get_stockcharts, get_freshGraph
import MySQLdb
import base64

# Initialize the flask application
app = Flask(__name__)

# Connection to the local database
db = MySQLdb.connect(host="localhost",
                     user = "root",
                     passwd = "Namanhtran1!",
                     db = "STOCK_TRADER")

cur = db.cursor()
cur.execute("SELECT net_cash FROM BALANCE WHERE user_ID = 0")
rows = cur.fetchone()
print(float(rows[0]))
db.commit()
cur.close()

user_id = 0

# Alpha Vantage API
api = TimeSeries(key='H2AKUMZSFASPIHZH')

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Portfolio page login required
@app.route('/portfolio')
def portfolio():

    stock_data = get_all_stocks(db, user_id)

    # Holds a lists full of stock info 
    portfolio_data = []

    # Final total of all the stocks
    final_total = 0
    
    # Cacluate the total value of the stocks and final total
    for symbol, quantity in stock_data:
        cur_price = price_lookup(api, symbol)
        total = cur_price * quantity
        portfolio_data.append([symbol, quantity, convert_to_dollar(cur_price), convert_to_dollar(total)])
        final_total = final_total + total
    
    user_cash = get_user_balance(db, user_id)

    # Send the data to the template and generate it
    return render_template('portfolio.html', data=portfolio_data, final_total=convert_to_dollar(final_total + user_cash), user_cash=convert_to_dollar(user_cash))

# Quote page login NOT required
@app.route('/quote', methods=["GET", "POST"])
def quote():
    # If user is request for page send html
    if request.method == "GET":
        return render_template('quote.html')
    
    # If user is sending data send html with price
    elif request.method == "POST":
        # Get the symbol input from the user
        symbol = request.form.get('quote-input')

        # Get the stock price
        stock_value = price_lookup(api, symbol)
        if stock_value == None:
            return render_template('error.html', string="Please enter a valid stock symbol")

        # Send data to html page and give user the rendered html page
        data = {'price': stock_value, 'symbol': symbol}
        return render_template('quote_response.html', data=data, chart=get_stockcharts(symbol, "Day", 5))

# Buy page login required
@app.route("/buy", methods=["GET", "POST"])
def buy():
    # If user is request for page send html
    if request.method == "GET":
        return render_template('buy.html', chart=get_freshGraph())
    
    # If user is sending data update DB with info given
    elif request.method == "POST":
        # Get the symbol and quantity input from the user
        symbol = request.form.get('buy-input').upper()
        quantity = int(request.form.get('buy-quantity'))

        # Get the stock price
        stock_value = price_lookup(api, symbol)
        if stock_value == None:
            return render_template('error.html', string="Please enter a valid stock symbol")
        
        # Calculate total value of the transaction
        total_value = stock_value * quantity

        user_cash = get_user_balance(db, user_id)
        
        # Update DB if user has enough money to buy
        if (user_cash > total_value):
            insert_stocks(db, user_id, user_cash, symbol, quantity, total_value)
            return redirect('/buy')
        
        # Return error page if user does not have enough money
        else:
            return render_template('error.html', string="You do not have enough in your balance to make this purchase")

# Sell page login requried
@app.route("/sell", methods=["GET", "POST"])
def sell():
    # If user is request for page send html 
    if request.method == "GET":
        # Retrieve all stocks that the user owns
        symbol_list = get_all_stocks(db, user_id)
        print(symbol_list)

        # Send the user a list of possiable stocks that the can sell
        return render_template('sell.html', data=symbol_list, chart=get_freshGraph())
    
    # If user is sending data update DB to sell stocks
    if request.method == "POST":
        # Get the symbol and quantity
        symbol = request.form.get('sell-input')
        quantity = int(request.form.get('buy-quantity'))
        
        # Get the stock value
        stock_value = price_lookup(api, symbol)
        if stock_value == None:
            return render_template('error.html', string="Please enter a valid stock symbol")
        
        # Calcuate the total value, and the updated quantity
        total_value = stock_value * quantity
        user_quantity = get_user_stock_quantity(db, user_id, symbol)
        updated_quantity = user_quantity - quantity

        # If the user has enough stocks to sell then sell the stocks
        if updated_quantity > -1:
            sell_stocks(db, user_id, symbol, total_value, updated_quantity)
            return redirect('/sell')
        
        # If user DOES NOT have enough stocks then return error page
        else:
            return render_template('error.html', string="You do not own enough stocks to sell this many")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')

# Register page 
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')

# XML test page 
@app.route("/xml", methods=["GET", "POST"])
def xml():
    if request.method == "GET":
        return render_template('xml.html')
    
    elif request.method == "POST":
        symbol = request.form["text-input"]
        id = request.form["id"]
        number = int(request.form["num"])
        print(symbol)
        div_string = get_stockcharts(symbol, id, number)
        
        return div_string
