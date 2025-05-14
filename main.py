import streamlit as st
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import os
import dotenv

# --- Load .env file if it exists ---
dotenv.load_dotenv()
API_KEY = os.environ.get("BINANCE_TESTNET_API_KEY")
API_SECRET = os.environ.get("BINANCE_TESTNET_API_SECRET")
TESTNET_BASE_URL = "https://testnet.binancefuture.com" # For REST API calls
logger = logging.getLogger("trading_bot_streamlit")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers if script is re-run in Streamlit
if not logger.handlers:
    # Create a file handler to store logs in a file
    file_handler = logging.FileHandler("trading_bot_streamlit.log")
    file_handler.setLevel(logging.INFO)

    # Create a console handler to display logs in the console (and Streamlit's terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

class BasicBot:
    """
    A simplified trading bot for Binance Futures Testnet.
    """
    def __init__(self, api_key, api_secret, testnet=True):
        """
        Initializes the BasicBot.

        Args:
            api_key (str): Your Binance API key.
            api_secret (str): Your Binance API secret.
            testnet (bool): If True, uses testnet URLs. Defaults to True.
        """
        if not api_key or not api_secret:
            logger.error("API Key and API Secret are required for bot initialization.")
            raise ValueError("API Key and API Secret are required.")

        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.API_URL = TESTNET_BASE_URL + '/fapi' # For futures API
        logger.info(f"Bot initialized. Testnet: {testnet}")

    def get_server_time(self):
        """Checks server time to verify API connectivity."""
        try:
            server_time = self.client.futures_time()
            logger.info(f"Connected to Binance. Server time: {server_time['serverTime']}")
            return server_time
        except BinanceAPIException as e:
            logger.error(f"API Error checking server time: {e}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"An unexpected error occurred checking server time: {e}")
            return {"error": str(e)}

    def place_market_order(self, symbol, side, quantity):
        """Places a market order."""
        try:
            logger.info(f"Attempting to place MARKET order: {side} {quantity} {symbol}")
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            logger.info(f"Market order placed successfully: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Binance API Exception placing market order: {e}")
            return {"error": str(e), "details": e.response.json() if e.response else "No response details"}
        except BinanceOrderException as e:
            logger.error(f"Binance Order Exception placing market order: {e}")
            return {"error": str(e), "details": e.response.json() if e.response else "No response details"}
        except Exception as e:
            logger.error(f"An unexpected error occurred placing market order: {e}")
            return {"error": str(e)}

    def place_limit_order(self, symbol, side, quantity, price):
        """Places a limit order."""
        try:
            logger.info(f"Attempting to place LIMIT order: {side} {quantity} {symbol} @ {price}")
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type=Client.ORDER_TYPE_LIMIT,
                timeInForce=Client.TIME_IN_FORCE_GTC,  # Good 'Til Canceled
                quantity=quantity,
                price=str(price) # Price needs to be a string
            )
            logger.info(f"Limit order placed successfully: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Binance API Exception placing limit order: {e}")
            return {"error": str(e), "details": e.response.json() if e.response else "No response details"}
        except BinanceOrderException as e:
            logger.error(f"Binance Order Exception placing limit order: {e}")
            return {"error": str(e), "details": e.response.json() if e.response else "No response details"}
        except Exception as e:
            logger.error(f"An unexpected error occurred placing limit order: {e}")
            return {"error": str(e)}

    def get_order_status(self, symbol, order_id):
        """Retrieves the status of a specific order."""
        try:
            logger.info(f"Fetching status for order ID {order_id} on {symbol}")
            order_status = self.client.futures_get_order(symbol=symbol.upper(), orderId=order_id)
            logger.info(f"Order Status: {order_status}")
            return order_status
        except BinanceAPIException as e:
            logger.error(f"Binance API Exception fetching order status: {e}")
            return {"error": str(e), "details": e.response.json() if e.response else "No response details"}
        except Exception as e:
            logger.error(f"An unexpected error occurred fetching order status: {e}")
            return {"error": str(e)}

    def get_account_balance(self, asset="USDT"):
        """Retrieves the balance for a specific asset in the futures account."""
        try:
            logger.info(f"Fetching account balance for asset: {asset}")
            balances = self.client.futures_account_balance()
            for balance_info in balances:
                if balance_info['asset'] == asset.upper():
                    logger.info(f"Balance for {asset}: {balance_info}")
                    return balance_info
            logger.warning(f"Asset {asset} not found in futures account balance.")
            return {"error": f"Asset {asset} not found."}
        except BinanceAPIException as e:
            logger.error(f"Binance API Exception fetching account balance: {e}")
            return {"error": str(e), "details": e.response.json() if e.response else "No response details"}
        except Exception as e:
            logger.error(f"An unexpected error occurred fetching account balance: {e}")
            return {"error": str(e)}

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="Binance Futures Bot")

st.title("📈 Binance Futures Trading Bot (Testnet)")

# --- Session State Initialization ---
if 'bot_instance' not in st.session_state:
    st.session_state.bot_instance = None
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.environ.get("BINANCE_TESTNET_API_KEY", "")
if 'api_secret' not in st.session_state:
    st.session_state.api_secret = os.environ.get("BINANCE_TESTNET_API_SECRET", "")

# --- Sidebar for API Credentials and Connection ---
st.sidebar.header("API Configuration")
st.sidebar.info(
    "Ensure your API keys are for the **Binance Futures Testnet** and have "
    "**'Enable Futures'** permissions. IP restrictions might also cause issues."
    "\n\nConsider using a `.env` file for your API keys:"
    "\n`BINANCE_TESTNET_API_KEY=your_key`"
    "\n`BINANCE_TESTNET_API_SECRET=your_secret`"
)

api_key_input = st.sidebar.text_input("Testnet API Key", value=st.session_state.api_key, type="password")
api_secret_input = st.sidebar.text_input("Testnet API Secret", value=st.session_state.api_secret, type="password")

if st.sidebar.button("Connect to Binance Testnet"):
    if api_key_input and api_secret_input:
        try:
            st.session_state.bot_instance = BasicBot(api_key_input, api_secret_input, testnet=True)
            st.session_state.api_key = api_key_input # Save to session state if manually entered
            st.session_state.api_secret = api_secret_input

            with st.spinner("Connecting..."):
                server_time_response = st.session_state.bot_instance.get_server_time()
            if server_time_response and "error" not in server_time_response:
                st.session_state.connected = True
                st.sidebar.success(f"Connected! Server Time: {server_time_response.get('serverTime')}")
                logger.info("Successfully connected via Streamlit UI.")
            else:
                st.session_state.connected = False
                error_msg = server_time_response.get('error', 'Unknown connection error.')
                st.sidebar.error(f"Connection Failed: {error_msg}")
                logger.error(f"Streamlit UI connection failed: {error_msg}")
        except ValueError as ve: # Catches API key/secret missing from BasicBot.__init__
            st.sidebar.error(f"Initialization Error: {ve}")
            logger.error(f"Streamlit UI bot initialization error: {ve}")
        except Exception as e:
            st.sidebar.error(f"An unexpected error occurred: {e}")
            logger.error(f"Unexpected error during Streamlit connection: {e}", exc_info=True)
    else:
        st.sidebar.warning("Please enter both API Key and Secret.")

if st.session_state.connected:
    st.sidebar.success("✅ Connected to Binance Futures Testnet")
else:
    st.sidebar.error("❌ Not Connected")

# --- Main Area for Bot Actions ---
if st.session_state.bot_instance and st.session_state.connected:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Place Order", "📄 Order Status", "💰 Account Balance", "📜 Logs"])

    with tab1:
        st.subheader("Place New Order")
        order_type = st.radio("Select Order Type", ("Market", "Limit"), horizontal=True)

        with st.form(key="order_form"):
            col1, col2 = st.columns(2)
            with col1:
                symbol = st.text_input("Symbol (e.g., BTCUSDT)", "BTCUSDT").upper()
                side = st.selectbox("Side", ("BUY", "SELL"))
            with col2:
                quantity_str = st.text_input("Quantity (e.g., 0.001)", "0.001")
                price_str = "0" # Default for market
                if order_type == "Limit":
                    price_str = st.text_input("Limit Price (e.g., 20000)", "0")

            submit_button = st.form_submit_button(label=f"Place {order_type} Order")

            if submit_button:
                try:
                    quantity = float(quantity_str)
                    if quantity <= 0:
                        st.error("Quantity must be a positive number.")
                    else:
                        response = None
                        with st.spinner(f"Placing {order_type} order..."):
                            if order_type == "Market":
                                response = st.session_state.bot_instance.place_market_order(symbol, side, quantity)
                            elif order_type == "Limit":
                                price = float(price_str)
                                if price <= 0:
                                    st.error("Price must be a positive number for limit orders.")
                                else:
                                    response = st.session_state.bot_instance.place_limit_order(symbol, side, quantity, price)
                        
                        if response:
                            if "error" in response:
                                st.error(f"Order Placement Failed: {response['error']}")
                                if "details" in response:
                                    st.json(response["details"])
                                logger.error(f"Streamlit UI Order Failed: {response}")
                            else:
                                st.success(f"{order_type} Order Placed Successfully!")
                                st.json(response)
                                logger.info(f"Streamlit UI Order Success: {response}")
                        else:
                             st.warning("No response from order placement. Check logs.")


                except ValueError:
                    st.error("Invalid input for quantity or price. Please enter numbers.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    logger.error(f"Unexpected error in Streamlit order form: {e}", exc_info=True)

    with tab2:
        st.subheader("Check Order Status")
        with st.form(key="status_form"):
            status_symbol = st.text_input("Symbol (e.g., BTCUSDT)", "BTCUSDT").upper()
            order_id_str = st.text_input("Order ID")
            status_submit = st.form_submit_button("Get Order Status")

            if status_submit:
                if not status_symbol or not order_id_str:
                    st.warning("Please enter Symbol and Order ID.")
                else:
                    try:
                        order_id = int(order_id_str)
                        with st.spinner("Fetching order status..."):
                            status_response = st.session_state.bot_instance.get_order_status(status_symbol, order_id)
                        
                        if status_response:
                            if "error" in status_response:
                                st.error(f"Failed to get order status: {status_response['error']}")
                                if "details" in status_response:
                                    st.json(status_response["details"])
                                logger.error(f"Streamlit UI Get Status Failed: {status_response}")
                            else:
                                st.success("Order Status Retrieved:")
                                st.json(status_response)
                                logger.info(f"Streamlit UI Get Status Success: {status_response}")
                        else:
                            st.warning("No response when fetching order status. Check logs.")

                    except ValueError:
                        st.error("Invalid Order ID. Please enter a number.")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {e}")
                        logger.error(f"Unexpected error in Streamlit status form: {e}", exc_info=True)
    with tab3:
        st.subheader("Account Balance (USDT)")
        if st.button("Fetch USDT Balance"):
            with st.spinner("Fetching account balance..."):
                balance_response = st.session_state.bot_instance.get_account_balance("USDT")
            
            if balance_response:
                if "error" in balance_response:
                    st.error(f"Failed to fetch balance: {balance_response['error']}")
                    if "details" in balance_response:
                        st.json(balance_response["details"])
                    logger.error(f"Streamlit UI Get Balance Failed: {balance_response}")
                else:
                    st.success("USDT Balance Retrieved:")
                    st.metric(label="Asset", value=balance_response.get('asset'))
                    st.metric(label="Total Balance", value=f"{float(balance_response.get('balance',0)):.4f} USDT")
                    st.metric(label="Available Balance", value=f"{float(balance_response.get('availableBalance',0)):.4f} USDT")
                    st.json(balance_response) # Show full details
                    logger.info(f"Streamlit UI Get Balance Success: {balance_response}")
            else:
                st.warning("No response when fetching balance. Check logs.")
        
        st.markdown("---")
        st.subheader("Fetch Balance for Other Asset")
        with st.form(key="other_asset_balance_form"):
            other_asset_symbol = st.text_input("Asset Symbol (e.g., BTC, ETH)", "BNB").upper()
            fetch_other_asset_button = st.form_submit_button("Fetch Balance")

            if fetch_other_asset_button:
                if not other_asset_symbol:
                    st.warning("Please enter an asset symbol.")
                else:
                    with st.spinner(f"Fetching {other_asset_symbol} balance..."):
                        balance_response = st.session_state.bot_instance.get_account_balance(other_asset_symbol)
                    
                    if balance_response:
                        if "error" in balance_response:
                            st.error(f"Failed to fetch balance for {other_asset_symbol}: {balance_response['error']}")
                            if "details" in balance_response and balance_response['error'] != f"Asset {other_asset_symbol} not found.": # Avoid showing details for simple not found
                                st.json(balance_response["details"])
                            logger.error(f"Streamlit UI Get Balance Failed for {other_asset_symbol}: {balance_response}")
                        else:
                            st.success(f"{other_asset_symbol} Balance Retrieved:")
                            st.metric(label="Asset", value=balance_response.get('asset'))
                            st.metric(label="Total Balance", value=f"{float(balance_response.get('balance',0)):.8f} {other_asset_symbol}") # More precision for crypto
                            st.metric(label="Available Balance", value=f"{float(balance_response.get('availableBalance',0)):.8f} {other_asset_symbol}")
                            st.json(balance_response)
                            logger.info(f"Streamlit UI Get Balance Success for {other_asset_symbol}: {balance_response}")
                    else:
                        st.warning(f"No response when fetching {other_asset_symbol} balance. Check logs.")


    with tab4:
        st.subheader("Application Logs")
        try:
            with open("trading_bot_streamlit.log", "r") as f:
                log_content = f.read()
                st.text_area("Log Output", log_content, height=400, key="log_area")
        except FileNotFoundError:
            st.info("Log file not yet created.")
        if st.button("Refresh Logs"):
            st.rerun()


elif not st.session_state.connected and (st.session_state.api_key or st.session_state.api_secret):
    st.warning("Please click 'Connect to Binance Testnet' in the sidebar after entering API credentials.")
else:
    st.info("Enter your Binance Testnet API credentials in the sidebar and click 'Connect' to begin.")

