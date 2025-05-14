# Binance Futures Trading Bot (Testnet) with Streamlit UI

This project is a simplified trading bot that interacts with the Binance Futures Testnet. It provides a user-friendly interface built with Streamlit to place market and limit orders, check order statuses, and view account balances.

## 🚀 Features

* **Testnet Focused:** Operates exclusively on the Binance Futures Testnet, ensuring no real funds are at risk.
* **Streamlit UI:** Easy-to-use web interface for all bot interactions.
* **Order Placement:**
    * Place Market Orders (BUY/SELL)
    * Place Limit Orders (BUY/SELL)
* **Order Management:**
    * Check the status of specific orders by Order ID.
* **Account Information:**
    * View USDT account balance.
    * Fetch balance for other specified assets.
* **API Interaction:** Uses the `python-binance` library for communication with the Binance API.
* **Logging:** Comprehensive logging of API requests, responses, errors, and application events to a `trading_bot_streamlit.log` file and displayed within the UI.
* **Configuration:** Supports API key management via a `.env` file or direct input in the UI.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

* Python (3.7 or higher recommended)
* pip (Python package installer)

You will also need:

* A **Binance Futures Testnet account**. You can register at [Binance Futures Testnet](https://testnet.binancefuture.com/).
* **API Key and Secret Key** generated from your Binance Futures Testnet account.
    * **Crucial:** When generating API keys, ensure you grant **"Enable Futures"** permissions.
    * Be mindful of IP restrictions if you've set them for your API key.

## ⚙️ Setup and Installation

1.  **Clone the Repository (or Download Files):**
    If this project is in a Git repository:
    ```bash
    git clone (https://github.com/agusain2001/Binance_Testnet.git)
    cd Binance_Testnet
    ```
    Otherwise, ensure all project files (`streamlit_app.py`, etc.) are in the same directory.

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    Create a `requirements.txt` file with the following content:
    ```text
    streamlit
    python-binance
    python-dotenv
    ```
    Then install them:
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Configuration: API Keys

You need to provide your Binance Futures Testnet API Key and Secret. You have two options:

1.  **Using a `.env` File (Recommended):**
    * Create a file named `.env` in the root directory of the project.
    * Add your API credentials to this file as follows:

        ```plaintext
        # .env
        BINANCE_TESTNET_API_KEY="YOUR_FUTURES_TESTNET_API_KEY_HERE"
        BINANCE_TESTNET_API_SECRET="YOUR_FUTURES_TESTNET_API_SECRET_HERE"
        ```
    * Replace `"YOUR_FUTURES_TESTNET_API_KEY_HERE"` and `"YOUR_FUTURES_TESTNET_API_SECRET_HERE"` with your actual Testnet keys.
    * The application will automatically load these keys if the `.env` file is present.

2.  **Manual Input in UI:**
    * If a `.env` file is not found or you prefer to enter credentials manually, you can input the API Key and Secret directly into the sidebar of the Streamlit application when it runs.

## ▶️ How to Run the Application

1.  **Navigate to the Project Directory:**
    Open your terminal or command prompt and change to the directory where `streamlit_app.py` is located.

2.  **Run the Streamlit App:**
    ```bash
    streamlit run streamlit_app.py
    ```

3.  **Access the UI:**
    Streamlit will typically open the application automatically in your default web browser (e.g., at `http://localhost:8501`). If not, the terminal will display the local URL you can use.

## 🖥️ Using the Bot Interface

The Streamlit interface is organized into a sidebar for configuration and main tabs for actions:

* **Sidebar (API Configuration):**
    * Input your Testnet API Key and Secret (if not using `.env`).
    * Click "Connect to Binance Testnet" to initialize the bot and verify the connection. Connection status will be displayed.

* **Place Order Tab:**
    * Select order type (Market or Limit).
    * Enter the trading symbol (e.g., `BTCUSDT`).
    * Choose side (BUY or SELL).
    * Specify the quantity.
    * For Limit orders, set the limit price.
    * Submit the order. Responses and errors will be shown.

* **Order Status Tab:**
    * Enter the symbol and Order ID for an existing order.
    * Fetch and display its current status.

* **Account Balance Tab:**
    * Fetch and display your USDT balance on the Testnet.
    * Option to fetch the balance for any other asset by specifying its symbol.

* **Logs Tab:**
    * Displays the contents of the `trading_bot_streamlit.log` file, providing a history of operations and detailed error messages.
    * A "Refresh Logs" button is available to update the view.

## 📜 Logging

All significant actions, API calls, responses, and errors are logged to:

* The console (terminal where Streamlit is running).
* A file named `trading_bot_streamlit.log` in the project directory.
* The "Logs" tab within the Streamlit UI.

This helps in debugging and tracking the bot's activity.

## ⚠️ Important Notes & Disclaimer

* **TESTNET ONLY:** This bot is designed **exclusively for the Binance Futures Testnet**. Do NOT use Mainnet API keys or attempt to use this bot with real funds without extensive modifications, security audits, and a thorough understanding of the risks involved.
* **API Key Security:** Protect your API keys. While `.env` files are convenient for local development, consider more secure methods like Streamlit Secrets Management if deploying the application.
* **API Permissions:** Ensure your Testnet API keys have "Enable Reading" and **"Enable Futures"** permissions. Incorrect permissions are a common source of errors (e.g., `APIError(code=-2015)`).
* **IP Restrictions:** If you have configured IP restrictions for your API keys on the Binance website, ensure the IP address of the machine running the bot is whitelisted.
* **No Financial Advice:** This tool is for educational and testing purposes only. It does not constitute financial advice. Trading cryptocurrencies involves significant risk.

## 💡 Potential Future Enhancements (Optional)

* Support for additional order types (e.g., Stop-Limit, Take-Profit, OCO).
* Real-time price display using WebSockets.
* Basic charting or technical indicator display.
* More sophisticated error handling and retry mechanisms.
* Strategy implementation backtesting capabilities.
* User authentication for multi-user scenarios (if deployed).

---
