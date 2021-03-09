# BinanceTools
###### version 1.0

This Python code is used to automize some tedious tasks around setting limit orders in Binance Crypto Exchange.


## Requirements:
#### libraries
```python
pip install python-binance
pip install pandas
pip install numpy
```

#### API
[Generate an API KEY](https://www.binance.com/en/my/settings/api-management), assign relevant permissions:
- Enable Reading
- Enable Spot & Margin Trading

Save your keys in file `parameters/keys.py` as:
```python
Public = '<PASTE YOUR API Key HERE>'
Secret = '<PASTE YOUR Secret Key HERE>'
```
## Running code:
Main file to generate orders is `postOrder.py`: 

For example, if you wish to open orders to buy **Bitcoin** with **1k Tether**, starting at **52k** and ending at **54k** with **equal** size orders,
your code should look like:

```python
from exchange.basics import connect, portfolio
from functions.misc import check_params
from functions.orders import order_manager

if __name__ == '__main__':
    client = connect()
    portfolio = portfolio(client)

    coin = 'BTC'        # <-- edit, coin you want to trade for
    pair = 'USDT'       # <-- edit, coin you want to trade with
    side = 'BUY'        # <-- edit, side you want to trade, either 'BUY' or 'SELL'

    # Choose only one:  [Part: None|1-100, Amount: None|int]
    part = None         # <-- edit, percentage of your pair coin in portfolio you want to trade with
    amount = 1000       # <-- edit, either None or specific value

    start = 52000       # <-- edit, value you want to start your orders
    end = 54000         # <-- edit, value you want to end your orders
    steps = 30          # <-- edit, number of orders you want to place 

    # True = normal distribution, False = linear distribution, [default: False]
    norm_dist = False   # <-- edit, type of orders distribution

    # Do you want to print all orders? [bool, default: True]
    show = True         # <-- edit, keep True to see your orders printed in console before placing them

    run = check_params(coin, pair)

    if run:
        order_manager(client, portfolio,
                      side, coin, pair, start, end, steps, part, amount,
                      norm_dist, show)
```

#### check_params
If you execute line like this: `run = check_params('ABC', 'XYZ')`, you'll get result as below:
```
Missing coin ABC in params.Coins
Missing coin XYZ in params.Coins
```
Also variable `run` will be `False`, and code won't run any further. Before moving further, you have to add missing coins to
`params.Coins`. For example `BTC` has below params:

`'BTC': {'lot': 6, 'price': 2}`

If you want to trade **BTC**, you can place order only with:
- precision = 2 on the price value.
- precision = 6 on the lot value,

You can check precision manually in binance by typing values in BUY/SELL window and checking how many decimals are accepted, like below:

![BTC precision](images/BTC_precision.png)

#### part vs. amount
Difference between `part` and `amount`:
- `part` is used to take some % of your asset based on your portfolio. For example if you wish to trade 100% of a coin
you should set `part = 100`, and `amount = None`.
- `amount` is used to trade specific amount of your asset. For example if you wish to trade exactly 1000 USDT,
you should set `amout = 1000` and `part = None`.

Code will check if you gave both variables with value and ask to correct it. Also code will check if you have provided
amount above your free asset and ask to correct it as well.

#### steps
Once your parameters are complete, you can place your first order. Program will ask you some questions on the run.
In Binance the minimum value of an order has to be **10 USDT/C** or **0.0001 BTC**. If you wish to trade with other pair,
please edit `def order_adjustment()` in `functions/orders.py`.
Questions to answer:
- do you want to place more orders then specified in `steps` if there is a possibility? Code will look for the maximum number of
steps to split your orders while staying above `min_val`.
- do you want to place less order then specified in `steps` if at least 1 of the orders is below `min_val`?
- abort?

#### norm_dist
```python
# True = normal distribution, False = linear distribution, [default: False]
norm_dist = False   # <-- edit, type of orders distribution
```

If `norm_dist = False` then all orders will be divided linearly (equally), (_red bars in chart below_).
If you change that variable to `True`, code will devided your orders based on normal distribution (_blue bars in chart below_).

![norm_dist chart](images/norm_dist_chart.png)

Stats for 15 orders between 100 and 150 are as below:
```
            normal (True)   linear (False)
count               15.00            15.00
min_price          100.00           100.00
max_price          150.00           150.00
average_price      125.00           125.00
min_coins           17.59            43.33
max_coins           65.37            43.33
average_coins       43.33            43.33
sum                650.00           650.00	
std_dev             16.56             0.00
```

## TO DO:
1. error: due to differences between Python and Binance way of rounding total order value, when trading 100% of asset on max number of steps,
sometimes the last order has insufficient amount of asset (like missing only 0.2 USDT to reach 10 USDT min_val).
`binance.exceptions.BinanceAPIException: APIError(code=-2010): Account has insufficient balance for requested action.`
2. add automatic precision checker
3. work on nice GUI