mport os
import argparse
from dotenv import load_dotenv
from fyers import Fyers
from utils import GetHistorical
import pandas as pd 
from sqlalchemy import create_engine

# utility function for parsing runtime arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Fetch historical stock data from Fyers API.")
    parser.add_argument("--totp", type=str, required=True, help="Time-Based One-Time Password for authentication")
    parser.add_argument("--pin", type=str, required=True, help="PIN for authentication")
    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()
    # user details
    user_details = {
        "username": os.getenv("USERNAME"),
        "client_id": os.getenv("CLIENT_ID"),
        "redirect_uri": os.getenv("REDIRECT_URI"),
        "secret_key": os.getenv("SECRET_KEY")}

    # broker API setup
    broker = Fyers(user_details)
    if not os.path.exists('access_token.txt'):
        args = parse_arguments()
        broker.start_session(args.pin, args.totp)
    client = broker.start_client()
    
    # database setup
    db_pass = os.dotenv("DB_PASSWORD")
    engine = create_engine("mysql+pymysql://root:db_pass@192.168.1.5:3306/nifty_50")

    # data fetching loop
    symbols = pd.read_csv("symbol_lists/nifty_50.csv")
    for index, row in symbols.iterrows():
        symbol = row["Symbol"]

        stock_info = {
        "symbol": symbol,
        "resolution": "15",
        "date_format": "1",
        "range_from": "2024-01-01",
        "range_to": "2024-02-01",
        "cont_flag": "1",}

        data = pd.DataFrame(GetHistorical(client, stock_info).fetch_data())
        print(f"Fetching data for {symbol}")

        data.to_sql(symbol, engine, if_exists="replace")
        print(f"Data for {symbol} stored in database")
    
    print("Data fetching complete")
