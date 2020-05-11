def price_lookup(api, symbol):
    try:
        stock_price = float(api.get_quote_endpoint(symbol=symbol)[0]["05. price"])
        print(stock_price)
        
        return stock_price

    except:
        print("API call failed")
        return None

def convert_to_dollar(num):
    return '$' + format(num, '.2f')