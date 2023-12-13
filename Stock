import requests
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

alpaca_api_key = 'PKBL3JHF9AQTJPEVXPB5'
alpaca_secret_key = 'lnYLaAvAp34Pr2BS6YRjf9sonIltjuVFuf2vIs3f'
base_url = "https://paper-api.alpaca.markets"

weather_api_key = "bdb08a1cfe0e641014d62d0fca4d82a8"
weather_api_url = "http://api.openweathermap.org/data/2.5/weather"

stock_symbol = "APPL"

trading_client = TradingClient(alpaca_api_key, alpaca_secret_key, paper=True)

def get_current_weather():
    response = requests.get(f"{weather_api_url}?q=your_location&appid={weather_api_key}")
    weather_data = response.json()
    return "rain" not in [condition["main"] for condition in weather_data.get("weather", [])]

def get_last_game_result(team_id):
    url = f'https://www.balldontlie.io/api/v1/games'
    params = {
        'team_ids[]': team_id,
        'per_page': 1,
        'order': 'desc'
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'data' in data and data['data']:
        game_data = data['data'][0]
        home_team_score = game_data.get('home_team_score')
        visitor_team_score = game_data.get('visitor_team_score')

        if home_team_score is not None and visitor_team_score is not None:
            return 'Win' if home_team_score > visitor_team_score else 'Loss'
        else:
            return "Unable to determine game result from the scores."
    else:
        return f"No results found for team ID {team_id}. Response: {data}"

def buy_stock():
    account = trading_client.get_account()

    team_id_houston_rockets = 10
    result = get_last_game_result(team_id_houston_rockets)

    print(f"Current Buying Power: {account.buying_power}")
    print(f"Conditions: Weather - {get_current_weather()}, Game Result - {result}")

    if get_current_weather() and result == 'Win':
        if float(account.buying_power) > 0:
            # Preparing orders
            market_order_data = MarketOrderRequest(
                symbol=stock_symbol,
                qty=1,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            )

            # Submitting the market order
            try:
                market_order = trading_client.submit_order(order_data=market_order_data)
                print(f"Market order placed to buy {stock_symbol}. Order ID: {market_order.id}")
            except Exception as e:
                print(f"Error placing order: {e}")
        else:
            print("Not enough buying power to place the order.")
    else:
        print("Conditions are not met to buy a stock.")

if __name__ == "__main__":
    buy_stock()
