from prometheus_client import start_http_server
from prometheus_client import Gauge
from prometheus_client import Counter
from time import sleep
import gdax
import signal

stats = {}

class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self,signum, frame):
        self.kill_now = True

class GdaxWebsocketClient(gdax.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["BTC-USD", "ETH-USD", "LTC-USD"]

    def on_message(self, msg):
        process_tick(msg)

    def on_close(self):
        print("-- Goodbye! --")


def statit(stat, value, type="gauge"):
    if stat in stats.keys():
        gauge = stats[stat]
    else:
        if type == "gauge":
            gauge = Gauge(stat, '')
        else:
            gauge = Counter(stat, '')
        stats[stat] = gauge
    if type == "gauge":
        gauge.set(float(value))
    else:
        gauge.inc(float(value))

def process_tick(msg):
    currency = msg['product_id'].replace('-', '_')
    metric_base = 'gdax_' + currency.lower() + '_'
    if msg['type'] == 'received':
        stat_received(msg, metric_base)
    if msg['type'] == 'match':
        stat_match(msg, metric_base)


def stat_received(msg, metric_base):
    if 'price' not in msg:
        return
    if msg['side'] == 'buy':
        statit(metric_base + 'bid', msg['price'])
    if msg['side'] == 'sell':
        statit(metric_base + 'ask', msg['price'])

def stat_match(msg, metric_base):
    statit(metric_base + 'volume', msg['size'], 'counter')
    if 'price' not in msg:
        return
    statit(metric_base + 'price', msg['price'])


start_http_server(8000)
killer = GracefulKiller()

wsClient = GdaxWebsocketClient()
wsClient.start()
print(wsClient.url, wsClient.products)

while True:
    sleep(1)
    if killer.kill_now:
        wsClient.close()
        break

exit(0)