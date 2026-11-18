from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. states for the agents to pass data between each other
class TradingState(TypedDict):
    market_data_summary: str
    analyst_signal: str
    risk_decision: str

# 2. Analyst Agent Node
def analyst_agent(state: TradingState):
    print("Analyst Agent:") #Reviewing market data and sentiment data
    print(f"Input Data: {state.get('market_data_summary')}")
    # the local SLM will generate this signal once implemented
    return {"analyst_signal": "BUY"} #sample output for testing until real SLM is implemented for mock testing

# 3. Risk Manager Agent Node
def risk_manager_agent(state: TradingState):
    print(f"Risk Manager:") #Evaluating the analyst's signal
    print(f"Input Signal: {state.get('analyst_signal')}")
    # the local SLM will check risk parameters here in the future with real data
    return {"risk_decision": "APPROVED"}

# 4. Graph
builder = StateGraph(TradingState)
builder.add_node("analyst", analyst_agent)
builder.add_node("risk_manager", risk_manager_agent)

# flow of execution 1. analyst 2. risk manager
builder.add_edge(START, "analyst")
builder.add_edge("analyst", "risk_manager")
builder.add_edge("risk_manager", END)

workflow = builder.compile()

# execute workflow
if __name__ == "__main__":
    # pass in fake summarized data for testing
    initial_state = {
        "market_data_summary": "AAPL close is 351.91, above SMA_10. Sentiment includes Tech Earnings.",
        "analyst_signal": "",
        "risk_decision": ""
    }
    
    final_state = workflow.invoke(initial_state)
    
    print("\nFinal Output:")
    print(f"Analyst Recommended: {final_state['analyst_signal']}")
    print(f"Risk Manager Status: {final_state['risk_decision']}")