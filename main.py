import os
import requests
import pandas as pd
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

load_dotenv()

# states for the agents to pass data between each other
class TradingState(TypedDict):
    market_data_summary: str
    analyst_signal: str
    risk_decision: str

# Analyst Agent
def analyst_agent(state: TradingState):
    print("Analyst Agent:") #Reviewing market data and sentiment data
    print(f"Input Data: {state.get('market_data_summary')}")
    # the local SLM will generate this signal once implemented
    return {"analyst_signal": "BUY"} #sample output for testing until real SLM is implemented for mock testing
# Risk Agent
def risk_manager_agent(state: TradingState):
    print(f"Risk Manager:") #Evaluating the analyst's signal
    print(f"Input Signal: {state.get('analyst_signal')}")
    # the local SLM will check risk parameters here in the future with real data
    return {"risk_decision": "APPROVED"}

# pipeline execution graph
builder = StateGraph(TradingState)
builder.add_node("analyst", analyst_agent)
builder.add_node("risk_manager", risk_manager_agent)
builder.add_edge(START, "analyst")
builder.add_edge("analyst", "risk_manager")
builder.add_edge("risk_manager", END)
workflow = builder.compile()


if __name__ == "__main__":
    # Alpaca Data
    data_client = StockHistoricalDataClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"))
    req = StockBarsRequest(symbol_or_symbols=["AAPL"], timeframe=TimeFrame.Day, start="2026-11-01") #using sample date for now to request data from Alpaca API
    df = data_client.get_stock_bars(req).df
    latest_close = df['close'].iloc[-1]
    
    # Marketaux Data
    token = os.getenv("MARKETAUX_API_TOKEN")
    url = f"https://api.marketaux.com/v1/news/all?symbols=AAPL&filter_entities=true&limit=3&api_token={token}"
    news = requests.get(url).json()
    headlines = [article['title'] for article in news.get('data', [])]

    # Formatting summary for the agent to process
    summary = f"AAPL Close: {latest_close}. Headlines: {', '.join(headlines)}"
    
    # feed summary to the agent workflow process
    initial_state = {"market_data_summary": summary, "analyst_signal": "", "risk_decision": ""}
    final_state = workflow.invoke(initial_state)
    
    # determine trade decision based on the final state from the workflow
    if final_state["risk_decision"] == "APPROVED" and final_state["analyst_signal"] == "BUY":
        trading_client = TradingClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True)
        order_data = MarketOrderRequest( #sample request for a paper trade to test the workflow
            symbol="AAPL",
            qty=1,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY
        )
        order = trading_client.submit_order(order_data)
        print(f"Approved, paper trade was executed. Order ID: {order.id}")
    else:
        print("Rejected, paper trade was rejected by Risk Manager.")