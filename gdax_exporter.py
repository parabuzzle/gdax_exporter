from prometheus_client import start_http_server
from prometheus_client import Gauge
from time import sleep
import gdax


public_client = gdax.PublicClient()

stats = {}


def statit(stat, value):
    if stat in stats.keys():
        gauge = stats[stat]
    else:
        gauge = Gauge(stat, '')
        stats[stat] = gauge

    gauge.set(value)

def spread(data):
    ask = float(data['ask'])
    bid = float(data['bid'])
    return round(((ask - bid) / ask) * 100, 5)


def process_currency(currency, data):
    metric_base = 'gdax_' + currency.lower() + '_'

    statit(metric_base + 'bid', data['bid'])
    statit(metric_base + 'volume', data['volume'])
    statit(metric_base + 'ask', data['ask'])
    statit(metric_base + 'price', data['price'])
    statit(metric_base + 'spread', spread(data))


start_http_server(8000)

while True:
    btc = public_client.get_product_ticker(product_id='BTC-USD')
    eth = public_client.get_product_ticker(product_id='ETH-USD')
    ltc = public_client.get_product_ticker(product_id='LTC-USD')

    process_currency('btc_usd', btc)
    process_currency('eth_usd', eth)
    process_currency('ltc_usd', ltc)
    sleep(1)
