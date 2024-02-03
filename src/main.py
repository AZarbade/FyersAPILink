import os
import argparse
from dotenv import load_dotenv
from fyers import Fyers
from utils import GetHistorical


# utility function for parsing runtime arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Fetch historical stock data from Fyers API.")
    parser.add_argument("--totp", type=str, required=True, help="Time-Based One-Time Password for authentication")
    parser.add_argument("--pin", type=str, required=True, help="PIN for authentication")
    return parser.parse_args()

def main():

    # load environment variables
    load_dotenv()
    user_details = {
        "username": os.getenv("USERNAME"),
        "client_id": os.getenv("CLIENT_ID"),
        "redirect_uri": os.getenv("REDIRECT_URI"),
        "secret_key": os.getenv("SECRET_KEY")
    }

    # stock information
    stock_info = {
        "symbol": "NSE:SBIN-EQ",
        "resolution": "15",
        "date_format": "1",
        "range_from": "2023-01-01",
        "range_to": "2023-07-01",
        "cont_flag": "1",
    }

    broker = Fyers(user_details)
    if not os.path.exists('access_token.txt'):
        args = parse_arguments()
        broker.start_session(args.pin, args.totp)
    client = broker.start_client()
    print(client.get_profile())


if __name__ == "__main__":
    main()
