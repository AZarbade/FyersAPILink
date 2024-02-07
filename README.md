# Fyers~~API~~Link

Fyers~~API~~Link is an educational project that connects to the Fyers broker using its **fyers_apiv3**. It enables users to control their broker accounts through this link ~~API~~, allowing actions such as fetching historical data and placing orders.
This project is essentially an unnecessary wrapper for fyers_apiv3, created solely for my convenience.

## Features

- Client setup in just 3 lines.
- Historical function for API data retrieval, with data chunking to handle rate limitations.
- *more to come...*


## Caution
<span style="color:red">
Fyers<del>API</del>Link is an educational project designed to facilitate learning and experimentation with financial trading using the Fyers broker's API. It is crucial to understand that engaging in real financial transactions involves risks, and the use of this project is at your own discretion. I am not responsible for any financial losses, and users are advised to exercise caution, conduct thorough research, and seek professional advice before making any actual financial decisions based on the educational content provided by this project.
</span>

## Getting Started

1. Clone the repository:
2. Change credentials in `.env` file. `.env_template` file is provided as an example to `.env`.
3. Run main.py,
    ```python
    python src/main.py --pin 1234 --totp 123456
    ```
4. Once the access_token has been generated on initial login, no need to pass --pin and --totp again. Script will use existing access_token.

## Contributing

If you'd like to contribute to the project, feel free to create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

<span style="color:red">**Note:** This project is not affiliated with Fyers or any financial institution. It is intended for educational purposes only.</span>
