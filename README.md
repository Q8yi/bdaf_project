# Blockchain Tweets and Market Data Dashboard

This project explores whether tweets from influential accounts are associated with changes in blockchain activity and coin prices.

The main application is a Dash dashboard in [app.py](app.py) that lets you:

- choose a Twitter user and inspect their tweets
- choose a blockchain network and compare available metrics
- view tweet dates alongside blockchain data on charts
- inspect the underlying CSV tables used by the dashboard

## Example

Refer to [docs/example.md](docs/example.md) for a quick look at the app and its main dashboard layout.

## Requirements

- Python 3.10 or newer is recommended
- The datasets in `datasets/` should already be present in the repository

## Setup

Create and activate a virtual environment, then install the Python dependencies:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1 # macOS user: source .venv/bin/activate
pip install -r requirements.txt
```

## Run The App

Start the dashboard with:

```bash
python app.py
```

After the app starts, open the local Dash URL shown in the terminal, usually `http://127.0.0.1:8050`.

## Project Structure

The most important folders are:

- `datasets/tweets/` - tweet data used by the dashboard
- `datasets/network/network_data/` - daily blockchain network metrics
- `datasets/network/prices/` - coin price history
- `datasets/network/merged/` - combined datasets for analysis and machine learning
- `notebooks/` - exploratory analysis and data preparation notebooks

## Data Overview

The dashboard uses several CSV formats:

- `<network>_avg_all.csv` - average transfer value and fees for a day
- `<network>_transac_all.csv` - daily transaction count
- `<network>_gas_all.csv` - gas-related daily metrics
- `tweets_all2.csv` - combined tweet dataset used by the app
- `cleaned_tweets2.csv` - cleaned tweet data prepared for analysis

The files under `datasets/network/merged/` are pre-merged datasets that combine tweet data with network or price data to make analysis and model training easier.

## Analysis Files

- [notebooks/network_data_retrieval.sql](notebooks/network_data_retrieval.sql) contains the BigQuery queries used to retrieve blockchain datasets
- [notebooks/analysis.ipynb](notebooks/analysis.ipynb) contains correlation and exploratory analysis
- [notebooks/clean_tweets.ipynb](notebooks/clean_tweets.ipynb) contains tweet cleaning steps