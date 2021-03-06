# BinanceTools
###### version 1.3.0

This Python code is used to automize some tedious tasks in Binance Crypto Exchange:
1. `postOrder.py` - opening multiple limit orders
2. `trailingOrder.py` - monitoring current price and posting market order once price reaches it's local min or max


## 1. Requirements:
#### 1.1 Libraries
```python
pip install python-binance
pip install pandas
pip install numpy
```

#### 1.2 API
[Generate an API KEY](https://www.binance.com/en/my/settings/api-management), assign relevant permissions:
- Enable Reading
- Enable Spot & Margin Trading

Save your keys in file `parameters/keys.py` as:
```python
Public = '<PASTE YOUR API Key HERE>'
Secret = '<PASTE YOUR Secret Key HERE>'
```
## 2. Posting limit orders
Main file to generate orders is `postOrder.py`: 

For example, if you wish to open **30** orders to **buy Bitcoin** with **1k Tether**, starting at **52k** and ending at
**54k** with **equal** size orders, your code should look like:

```python
from exchange.basics import connect, portfolio
from functions.misc import check_params
from functions.orders import order_manager

if __name__ == '__main__':
    client = connect()
    portfolio = portfolio(client)

    coin = 'BTC'        # <-- edit, coin you want to trade
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

    run = check_params(coin, pair)
    if run:
        order_manager(client, portfolio, side, coin, pair, start, end, steps, part, amount, norm_dist)
```

#### 2.1 order of posting orders
- If you choose to set **BUY**, program will post orders by price **descending**
- If you choose to set **SELL**, program will post orders by price **ascending**
 
#### 2.2 check_params
If you execute `run = check_params('ABC', 'XYZ')`, you'll get result:
```
Missing coin ABC in params.Coins
Missing coin XYZ in params.Coins
```
Also variable `run` will be `False`, and code won't run any further. Before moving further, you have to add missing coins to
`params.Coins`. For example `BTC` has below parameters:

`'BTC': {'lot': 6, 'price': 2}`

If you want to trade **BTC**, you can open order only with:
- price value with precision = 2 
- lot value with precision = 6

You can check precision manually in Binance BUY/SELL window by checking how many decimals are accepted, like below:

![BTC precision](images/BTC_precision.png)

#### 2.3 part vs. amount
Difference between `part` and `amount`:
- `part` is used to take a percentage of your free asset based on your portfolio. For example if you wish to trade 100%
of your coin you should set `part = 100`, and `amount = None`.
- `amount` is used to trade specific amount of your asset. For example if you wish to trade exactly 1000 USDT,
you should set `amout = 1000` and `part = None`.

Code will check for errors:
- if you gave both variables with a value (`if (part is not None) & (amount is not None)`)
- if you have provided amount above your free assets (`if amount > balance`)

#### 2.4 steps
Once your parameters are ready, you can open your first order. Program will ask some questions on the run.
In Binance the minimum value of an order has to be **10 USD** or **0.0001 BTC**. If you wish to trade with other pair,
please edit `def order_adjustment()` in `functions/orders.py`.
Questions to answer:
- do you want to open more orders then specified in `steps` if there is a possibility? Code will look for the maximum
number of steps to split your orders while staying above `min_val`.
- do you want to open less orders then specified in `steps` if at least 1 is below `min_val`?
- abort?

#### 2.5 norm_dist
```python
# True = normal distribution, False = linear distribution, [default: False]
norm_dist = False   # <-- edit, type of orders distribution
```
If `norm_dist = False` then all orders will be divided linearly (equally), (_red bars in chart below_).
If you change that variable to `True`, code will divide your orders based on normal distribution (_blue bars in chart below_).

![norm_dist chart](images/norm_dist_chart.png)

Stats for 15 orders in price range 100-150 are as below:
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

#### 2.6 5x limit
Binance isn't letting for orders with price 5 and above times higher then the current price. To handle issues when user
sets `end` value above that limit, function `check_current_price` has been introduced to check and decide on the next
steps. It reads the current price of paired coin and if `end` is above 5x limit, user has to decide, what to do next:
- _(1) - edit end value manually_ - it will stop the program.
- _(2) - limit number of orders (open less then orders, but all within 5x)_ - the amount of traded coins will be reduced
to cover only orders within 5x limitation. Orders above 5x will be ignored.  
- _(3) - apply 5x as new end for 100% of amount_ - the amount of traded coins will remain the same, but price range
will be updated to fit within 5x limitation

## 3. Trailing Bot
File `trailingOrder.py` contains trailing bot which mimics [3Commas' Trailing TP](https://help.3commas.io/en/articles/3108982-trailing-take-profit-catch-the-rise).

<img src="https://3commas-5474bf3897f2.intercom-attachments-1.com/i/o/131052485/06a1cd81ab4f655230b6cf22/TTP.gif?expires=1620146147&signature=d9768e6de9cefb3492debe7cc5555cdead18b62ca0360861f967dc757970def7" width="666" />

source: [3Commas](https://help.3commas.io/en/articles/3108982-trailing-take-profit-catch-the-rise)

```python
from exchange.basics import connect
from functions.trailOrder import trailing_bot

if __name__ == '__main__':
    client = connect()

    params = {
        'coin': 'BTC',           # <-- edit, coin you want to trade 
        'pair': 'USDT',          # <-- edit, coin you want to trade with
        'side': 'SELL',          # <-- edit, side you want to trade, either 'BUY' or 'SELL'
        'price': 54500,          # <-- edit, value when trailing has to start
        'val': 1000,             # <-- edit, value of pair asset you want to trade
        'deviation': ('V', 250)  # <-- edit, 'P' (percentage) or 'V' (value)
    }

    trailing_bot(client, params)
```
#### 3.1 price
type: `int/double`

You set price for which you wish to BUY or SELL an asset. It means once pair reaches that price level it will start
trailing. Until then it is just monitoring the market. 
 
#### 3.2 val
type: `int/double`

You set value of how much of `pair` you want to give for traded `coin`. For example 1000 USDT for x BTC.

#### 3.3 deviation
type: `touple(str, int/double)`

- `'V'` for **value**, for example `250` if you wish to set boundaries of 250 below and 250 above `price`
- `'P'` for **percentage**, for example `1.5` if you wish to set boundaries of 1.5% below and 1.5% above `price`

### 3.4 monitoring and trailing
When program is running it is **monitoring** exchange to see if the current price of `coin` get withing initial boundaries.
Once the price is in, program start **trailing**. It will shift initial boundaries up (if selling) or down (if buying)
respecting initial **deviation** level. Once the current price goes outside current boundaries it will either:
- **fire** market order:
  - if you are selling and price goes below boundaries
  - if you are buying and price goes above boundaries
- **shift** boundaries to respect new price.

If deviation is `'P'` (percentage) new boundaries are calculate based on the current price, not original one.

## 4. Limitations
Based on API Trading Rules (see: [What kind of limits are there?](https://www.binance.com/en/support/articles/360004492232))
you can be banned from 5 minutes to 3 days if you spam order creation and cancellation very quickly without executing trades.
This program allows you to open hundreds of orders very quickly. Please use trial and error to achieve your ideal
trading pattern and **do not play with opening tones of orders just to close them right after!**

_Error -1015 TOO_MANY_ORDERS_ : API has Hard-Limit of 100 orders per 10 seconds. To keep within this limit, communication
between program and Binance has been artificially slowed down to 10 actions/second.

## 5. Common issues:
`binance.exceptions.BinanceAPIException: APIError(code=-1021): Timestamp for this request was 1000ms ahead of the server's time.`

This is know issue ([link](https://github.com/sammchardy/python-binance/issues/249)), which I couldn't resolve myself.
The only solution for that is restarting your PC and running code again.

## 6. TO DO:
#### postOrder.py
1. add automatic precision checker
2. work on nice GUI
#### trailingOrder.py
1. live price chart with current boundaries