import os
import argparse
from dotenv import load_dotenv
from util import Fyers

# load environment variables
load_dotenv()
user_details = {
    'username': os.getenv('USERNAME'),
    'client_id': os.getenv('CLIENT_ID'),
    'redirect_uri': os.getenv('REDIRECT_URI'),
    'secret_key': os.getenv('SECRET_KEY')
}

# utility function for parsing runtime arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Fetch historical stock data from Fyers API.')
    parser.add_argument('--totp', type=str, required=True, help='Time-Based One-Time Password for authentication')
    parser.add_argument('--pin', type=str, required=True, help='PIN for authentication')
    return parser.parse_args()


def main():
    args = parse_arguments()

    broker = Fyers(user_details, args.pin, args.totp)
    broker.start_session()
    client = broker.start_client()
    print(client.get_profile())

main()
