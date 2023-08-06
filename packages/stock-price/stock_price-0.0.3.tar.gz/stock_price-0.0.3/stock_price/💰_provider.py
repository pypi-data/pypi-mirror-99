import os, json
from datetime import datetime

import requests


class 💰Provider:
  def __init__(self):
    with open(os.path.expanduser(f'~/polygon_config.json')) as f:
      text = f.read()
    self.api_token = json.loads(text)['api_token']
    self.session = requests.Session()

  def pull_current_💰(self, symbol):
    url = f'https://api.polygon.io/v1/last_quote/stocks/{symbol}?apiKey={self.api_token}'
    quote_dict = self.session.get(url).json()
    last_quote = quote_dict.get('last')
    if not last_quote:
      return None
    return (last_quote['bid💰'] + last_quote['ask💰']) / 2

def test():
  provider = 💰Provider()
  print('💰:', provider.pull_current_💰('AAPL'))
  provider.session.close()

if __name__ == '__main__':
  test()
