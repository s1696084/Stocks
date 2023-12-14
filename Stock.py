import requests
import alpaca_trade_api as tradeapi

alpaca_api_key = 'PKBL3JHF9AQTJPEVXPB5'
alpaca_secret_key = 'lnYLaAvAp34Pr2BS6YRjf9sonIltjuVFuf2vIs3f'
base_url = "https://paper-api.alpaca.markets"

weather_api_key = "bdb08a1cfe0e641014d62d0fca4d82a8"
weather_api_url = "http://api.openweathermap.org/data/2.5/weather"

stock_symbol = "AAPL"  # Assuming you meant "AAPL" instead of "APPL"

# Initialize the Alpaca API client
alpaca_client = tradeapi.REST(alpaca_api_key, alpaca_secret_key, base_url=base_url, api_version='v2')

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
    account = alpaca_client.get_account()

    team_id_houston_rockets = 10
    result = get_last_game_result(team_id_houston_rockets)

    print(f"Current Buying Power: {account.buying_power}")
    print(f"Conditions: Weather - {get_current_weather()}, Game Result - {result}")

    if get_current_weather() and result == 'Win':
        if float(account.buying_power) > 0:
            # Preparing orders
            alpaca_client.submit_order(
                symbol=stock_symbol,
                qty=1,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print(f"Market order placed to buy {stock_symbol}.")
        else:
            print("Not enough buying power to place the order.")
    else:
        print("Conditions are not met to buy a stock.")

if __name__ == "__main__":
    buy_stock()
