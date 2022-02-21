from requests import Request, Session
import json
import tweepy

# Used coinmarketcap because it's the most popular and reliable, and also used tweepy because it has great documentation.
def apiSetUp(url):

    #Twitter API
    auth = tweepy.OAuthHandler('9wAgc9puE2D8XPmNeY6dc6Pif','2eIPCPeivNzmFWTeETWrOW243oSmvULn10xiFTVRP9aR3carGB')
    auth.set_access_token('1495070708883505152-fsr8jydcj5CkIBMMERJEGIpEwmtbN3', '7XNHYz2TX1IJkDz7xXZk0BY1HWBCG6Bd8lCPnQDpUpuL1')
    api = tweepy.API(auth)

    #CoinMarketCap API
    parameters = {
        'slug': 'bitcoin',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '25e2d061-8cd8-4bfb-ad4e-acb3301789f3',
    }
    session = Session()
    session.headers.update(headers)
    return session, parameters, api #Session is the session's details, parameters are what we are searching for in the session, and the api is the twitter api

def collectData(session, parameters, url): #Collects the data 
    response = session.get(url, params=parameters)
    priceData= json.loads(response.text)['data']['1']['quote']['USD']['price']
    percentChangeData= json.loads(response.text)['data']['1']['quote']['USD']['percent_change_24h']
    return priceData, percentChangeData #priceData is the price's information, and percentChangeData is the 24h percent change information


def formatResults(priceData, percentChangeData):
    return('Current Price of BTC: ${:,}\n24 Hour Percent Change: {}%\n#bitcoin'.format((int(priceData)), round(percentChangeData, 2)))

def main():
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    session, parameters, api = apiSetUp(url)
    priceData, percentChangeData = collectData(session, parameters, url)
    results = formatResults(priceData, percentChangeData)
    api.update_status(results)
    raise SystemExit #Had an error where a tweet would repeat somehow, hoping this fixes my issue otherwise it's because of the Heroku software

main()
