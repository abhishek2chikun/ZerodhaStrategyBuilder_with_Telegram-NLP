import logging


def Place_order(kite,tradingSymbol, qty, direction, exchangeType, product, orderType):
    try:
        orderId = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=exchangeType,
            tradingsymbol=tradingSymbol,
            transaction_type=direction,
            quantity=qty,
            product=product,
            order_type=orderType)

        logging.info('Order placed successfully, orderId = %s', orderId)
        return 'Done'

    except Exception as e:
        return e

def Place_Limit(kite,tradingSymbol, qty, direction, exchangeType, product, orderType,price):
    try:
        orderId = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=exchangeType,
            tradingsymbol=tradingSymbol,
            transaction_type=direction,
            quantity=qty,
            product=product,
            order_type=orderType,
            price=price)

        logging.info('Order placed successfully, orderId = %s', orderId)
        return 'Done'
    except Exception as e:
        return e
    
def Kite_login(Info,access_token=None):
    from kiteconnect import KiteConnect
    import Login
    
    # try:
    #     kite = KiteConnect(Info['APIKey'], access_token)
    #     print('Login Successful')

    # except:
    kite = None
    try:
        kite = Login.login(Info['APIKey'],Info['APISecret'],Info['ClientID'],Info['ZerodhaPassword'],Info['Totp'])
        
        print("Login Successful")
    except Exception as e:
        print(e)


    return kite

import json
with open(f'./Info/User.json','r') as f:
  Info = json.load(f)

# with open(f'./Access_token.txt','r') as f:
#     access_token = f.read()
# print(access_token)

# kite = Kite_login(Info)