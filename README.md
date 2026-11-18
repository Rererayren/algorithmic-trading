# Algorithmic Trading Using Consensus in Multi-Agent Systems for Edge AI

## Prerequisites
* Python 3.8+, I recommend Anaconda environment due to windows security policies. 
* An [Alpaca](https://alpaca.markets/) Paper Trading account.
* A [Marketaux](https://www.marketaux.com/) free API account.
* [Ollama](https://ollama.com/) installed locally. Not implemented yet.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rererayren/algorithmic-trading.git
   cd algorithmic-trading/edge-trading-ai
   ```

2. **Set up the Python environment (using Conda):**
   ```bash
   conda create -n trading_env python=3.10
   conda activate trading_env
   ```

3. **Create a `.env` file in the repository root:**

   ```text
   ALPACA_API_KEY=your_paper_api_key
   ALPACA_SECRET_KEY=your_paper_secret_key
   MARKETAUX_API_TOKEN=your_marketaux_token
   ```


## Run

Solo testing with sample data / no api calls/orders:

```powershell
python agent_workflow.py
```

To grab current data without placing an order:

```powershell
python data_ingestion.py
```
to execute the entire pipeline process of API call and purchase order submission to paper trading account 
```powershell
python main.py
```