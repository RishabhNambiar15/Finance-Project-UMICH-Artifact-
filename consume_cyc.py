from financetoolkit import Toolkit
import os
import numpy as np  # Import numpy for NaN and inf handling
import yfinance as yf

def consume_cyc_stats(ticker):
    user_stock = yf.Ticker(ticker)
    my_secret = os.environ['api_key13']

    # Ticker List
    consume_cyc_tickers = [
        "AMZN",
        "TSLA",
        "HD", 
        "TM", 
        "PDD", 
        "BABA", 
        "MCD", 
        "BKNG", 
        "TJX", 
        "LOW"
    ]

    # Calls the API for the specific company, data starts from 2022 end
    consume_cyc_company = Toolkit(tickers=consume_cyc_tickers,
                          api_key=my_secret,
                          start_date="2022-12-31")

    # Function to get ratio table
    consume_cyc_ratio_list = {
        "Asset Turnover Ratio": consume_cyc_company.ratios.get_asset_turnover_ratio(),
        "Inventory Turnover Ratio": consume_cyc_company.ratios.get_inventory_turnover_ratio(),
        "Accounts Payable Turnover Ratio": consume_cyc_company.ratios.get_accounts_payables_turnover_ratio(),
        "Receivable Turnover Ratio": consume_cyc_company.ratios.get_receivables_turnover(),
        "Price to Earnings (P/E) Ratio": consume_cyc_company.ratios.get_price_earnings_ratio(),
        "Current Ratio": consume_cyc_company.ratios.get_current_ratio(),
        "Debt to Equity Ratio": consume_cyc_company.ratios.get_debt_to_equity_ratio(),
        "Earnings Per Share Ratio": consume_cyc_company.ratios.get_earnings_per_share(),
        "EV to EBITA Ratio":
        consume_cyc_company.ratios.get_ev_to_ebitda_ratio(),
        "Cash Ratio": consume_cyc_company.ratios.get_cash_ratio(),
        "Debt to Assets Ratio": consume_cyc_company.ratios.get_debt_to_assets_ratio(),
        "Price to Book Ratio": consume_cyc_company.ratios.get_price_to_book_ratio(),
        "Return On Assets (ROA) Ratio": consume_cyc_company.ratios.get_return_on_assets(),
        "Income Quality Ratio": consume_cyc_company.ratios.get_income_quality_ratio(),
        "Equity Multiplier Ratio": consume_cyc_company.ratios.get_equity_multiplier(),
        "Gross Profit Margin Ratio": consume_cyc_company.ratios.get_gross_margin(),
        "Net Profit Margin Ratio": consume_cyc_company.ratios.get_net_profit_margin(),
        "Debt Service Coverage Ratio": consume_cyc_company.ratios.get_debt_service_coverage_ratio(),
        "Interest Coverage Ratio": consume_cyc_company.ratios.get_interest_burden_ratio(),
        "Short Term Coverage Ratio": consume_cyc_company.ratios.get_short_term_coverage_ratio()
    }

    # Initialize dictionaries to store averages and standard deviations
    consume_cyc_ratios = {}
    consume_cyc_industry_averages = {}
    consume_cyc_industry_std = {}

    # Calculate and store averages and standard deviations
    for key, value in consume_cyc_ratio_list.items():
        values = value.loc[consume_cyc_tickers].iloc[:, -1]
        values = values.replace([np.inf, -np.inf], np.nan).fillna(0)  # Replace inf with NaN and then fill NaN with 0
        consume_cyc_ratios[key] = values

        consume_cyc_ratio_avg = round(values.mean(), 2)
        consume_cyc_ratio_std = round(values.std(), 2)
        consume_cyc_industry_averages[key] = consume_cyc_ratio_avg
        consume_cyc_industry_std[key] = consume_cyc_ratio_std

    # Print the averages and standard deviations
    print(f"The following are the ratios for the {user_stock.info['sector']} sector")
    for key, value in consume_cyc_industry_averages.items():
        print(f"Average {key}: {value}")
        

    print("\n\n")
    
    consume_cyc_weights = {
        "Asset Turnover Ratio": 4,
        "Inventory Turnover Ratio": 8,
        "Accounts Payable Turnover Ratio": 4,
        "Receivable Turnover Ratio": 3,
        "Price to Earnings (P/E) Ratio": 9,
        "Current Ratio": 2,
        "Debt to Equity Ratio": 7,
        "Earnings Per Share Ratio": 9,
        "EV to EBITA Ratio": 9,
        "Cash Ratio":3,
        "Debt to Assets Ratio": 3,
        "Price to Book Ratio": 9,
        "Return On Assets (ROA) Ratio": 7,
        "Income Quality Ratio": 6,
        "Equity Multiplier Ratio": 2,
        "Gross Profit Margin Ratio": 7,
        "Net Profit Margin Ratio": 3,
        "Debt Service Coverage Ratio": 2,
        "Interest Coverage Ratio": 2,
        "Short Term Coverage Ratio": 1
    }


    consume_cyc_preferences = {
        "Asset Turnover Ratio": "higher",
        "Inventory Turnover Ratio": "higher",
        "Accounts Payable Turnover Ratio": "higher",
        "Receivable Turnover Ratio": "higher",
        "Price to Earnings (P/E) Ratio": "lower",
        "Current Ratio": "higher",
        "Debt to Equity Ratio": "lower",
        "Earnings Per Share Ratio": "higher",
        "EV to EBITA Ratio": "higher",
        "Cash Ratio": "higher",
        "Debt to Assets Ratio": "lower",
        "Price to Book Ratio": "higher",
        "Return On Assets (ROA) Ratio": "higher",
        "Income Quality Ratio": "higher",
        "Equity Multiplier Ratio": "lower",
        "Gross Profit Margin Ratio": "higher",
        "Net Profit Margin Ratio": "higher",
        "Debt Service Coverage Ratio": "higher",
        "Interest Coverage Ratio": "higher",
        "Short Term Coverage Ratio": "higher"
    }

    

    consume_cyc_pitroski_group = {}
    for ticker in consume_cyc_tickers:
        consume_cyc_pitroski_getter = consume_cyc_company.models.get_piotroski_score().loc[ticker].iloc[9, -1]
        if np.isinf(consume_cyc_pitroski_getter) or np.isnan(consume_cyc_pitroski_getter):
            consume_cyc_pitroski_getter = 0  # Handle infinity and NaN by setting to 0
        consume_cyc_pitroski_group[ticker] = consume_cyc_pitroski_getter

    # Calculate the mean of the Piotroski scores
    consume_cyc_pitroski_score = round(sum(consume_cyc_pitroski_group.values()) / len(consume_cyc_pitroski_group), 2)

        
    return {
        "consume_cyc_industry_std": consume_cyc_industry_std,
        "consume_cyc_industry_averages": consume_cyc_industry_averages,
        "consume_cyc_weights": consume_cyc_weights,
        "consume_cyc_preferences": consume_cyc_preferences,
        "consume_cyc_company": consume_cyc_company,
        "consume_cyc_pitroski_score": consume_cyc_pitroski_score
        
    }

