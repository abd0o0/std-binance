import math

from binance import Client
import pandas as pd
import matplotlib.pyplot as plt

plt.show()
# from IPython.display import display

Client = Client(api_key='lfr4xrolx8CtcNleqpbZk2s2uUDJxWqYk7wWt5utdU3ZxIbC5KfobAlUEUTOZ1VH',
                api_secret='JD0zVJwhNf3xcm4dt04Ptnv6Zw7w0wjOdpEnIDjUAmlYwbouyOTmtifQtyztdVtq ')

#print(pd.DataFrame(Client.get_historical_klines('BTCUSDT', '1m', '30min ago GMT+2')))

def getminutedata(symbol, interval, lookback):
    frame = pd.DataFrame(Client.get_historical_klines(symbol, interval, lookback + 'min ago GMT+2'))
    #here we used iloc to select colomn we want to show
    frame = frame.iloc[:, :5]

    # just gave every column a name
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close']
    # we need to convert iske to readable time so we select the time column
    frame = frame.set_index('Time')
    # changing iske to date time
    frame.index = pd.to_datetime(frame.index, unit='ms')
    # changing iske number to decimal
    frame = frame.astype(float)
    return frame

#getminutedata('BTCUSDT', '1m', '30')
#print(getminutedata('BTCUSDT', '1m', '30'))
def standardd(symbol, interval, lookback):
    frame = pd.DataFrame(Client.get_historical_klines(symbol, interval, lookback + 'min ago GMT+2'))
    frame = frame.iloc[:, :5]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    # average price per min
    frame['avrm'] = (frame['High'] + frame['Low']) / 2
    # average price over the interval
    Avr = frame['avrm'].sum() / int(lookback)
    print(Avr)
    # Square the difference
    frame['diff'] = frame['avrm'] - Avr
    frame['diffsq'] = pow(frame['diff'], 2)
    # Sum the squared differences&variance:

    variance = frame['diffsq'].sum() / int(lookback)
    print(variance)
    # standard deviation
    sd = math.sqrt(variance)
    print(sd)
    test = getminutedata('BTCUSDT', '1m', '200')
    test.plot.line()
    # print(test)
    # test.line.plot()
    return sd


# to show the interval
# plt.interactive(True)

#test = getminutedata('BTCUSDT', '1m', '200')
#test.plot.line()
## print(test)
##test.line.plot()
#plt.show(block=True)


# stratigy
# buy if the asset fell by more than SD% by calculating the volatility (standard deviation) within the last 30min
# sell if asset rise by more than SD-5% or falls further by SD-5%
# Return of Assets= Net Income / Total Assets
# smaller ratio
# Return of Assets of today(checking how the asset performing over the interval)
# == (return of the day - return of yesterday)/return of yesterday
# == day/yesterday -1
# cumulative return = (1+ ROA)*(1+ROY)-1 to solve the product problem we use LOG of return
# after the sum we take the exp -1 and we get the same result

def strategyetest(sympol, interval, lookback, qty, entry=False):
    global order
    df = getminutedata(sympol, interval, lookback)
    df2 = standardd(sympol, interval, lookback)
    # pct_change() is takeing the sum of %change return
    # cumpord() cumulative product
    cumulret = (df.Open.pct_change() + 1).cumprod() - 1
    if not entry:
        if cumulret[-1] < df2:
            order = Client.create_order()(symbol=sympol,side='BUY',type='MARKET'
                                          ,quantity=qty)
            print(order)
            entry=True
        else:
            print('No trade has been executed')
    #selling order
    if entry:
        while True:
            df = getminutedata(sympol,interval,lookback)
            #to keep checking the price
            sincebuy = df.loc[df.index > pd.to_datatime(
                order['transactTime'], unit='ms')]
            if len(sincebuy) > 0:
                sincebuyret = (sincebuy.Open.pct_change() + 1).cumprod() - 1
                if sincebuyret[-1] > df2-0.005 or sincebuyret[-1] < df2-0.005:
                    order = Client.create_order(sympol=sympol,side='SELL',
                                                type ='MARKET',quantity=qty)
                    print(order)
                    break




#strategyetest('BTCUSDT','1m','30m', 0.0005)
