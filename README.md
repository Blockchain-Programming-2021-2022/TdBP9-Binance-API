# TdBP9

API Binance from python using sqlite.

-Market : In this part we use Binance api to extract market's data to our sqlite database.             
-Trades : These endpoints requires Api_key,Secret_key which you can create from your Binance account like this https://www.binance.com/en/support/faq/360002502072.
          You are able to execute all binance dashboard's action from you pyhton IDE. 
          In this repository you can see how to create(def makeOrder(symbol,side,type,timeInForce,quantity,price,):) and cancel an order(def cancelOrder(symbol,orderId):).
