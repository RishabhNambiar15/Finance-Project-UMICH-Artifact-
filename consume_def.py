from financetoolkit import Toolkit
import os
import numpy as np  # Import numpy for NaN and inf handling
import yfinance as yf

def consume_def_stats(ticker):
    user_stock = yf.Ticker(ticker)
    my_secret = os.environ['api_key5']

    # Ticker List
    consume_def_tickers = [
        "WMT",
        "PG",
        "COST",
        "KO",
        "PEP",
        "FMX",
        "PM",
        "UL",
        "BUD",
        "MDLZ"
    ]

    # Calls the API for the specific company, data starts from 2022 end
    consume_def_company = Toolkit(tickers=consume_def_tickers,
                          api_key=my_secret,
                          start_date="2022-12-31")

    # Function to get ratio table
    consume_def_ratio_list = {
        "Asset Turnover Ratio": consume_def_company.ratios.get_asset_turnover_ratio(),
        "Inventory Turnover Ratio": consume_def_company.ratios.get_inventory_turnover_ratio(),
        "Accounts Payable Turnover Ratio": consume_def_company.ratios.get_accounts_payables_turnover_ratio(),
        "Receivable Turnover Ratio": consume_def_company.ratios.get_receivables_turnover(),
        "Price to Earnings (P/E) Ratio": consume_def_company.ratios.get_price_earnings_ratio(),
        "Current Ratio": consume_def_company.ratios.get_current_ratio(),
        "Debt to Equity Ratio": consume_def_company.ratios.get_debt_to_equity_ratio(),
        "Earnings Per Share Ratio": consume_def_company.ratios.get_earnings_per_share(),
        "EV to EBITA Ratio":
        consume_def_company.ratios.get_ev_to_ebitda_ratio(),
        "Cash Ratio": consume_def_company.ratios.get_cash_ratio(),
        "Debt to Assets Ratio": consume_def_company.ratios.get_debt_to_assets_ratio(),
        "Price to Book Ratio": consume_def_company.ratios.get_price_to_book_ratio(),
        "Return On Assets (ROA) Ratio": consume_def_company.ratios.get_return_on_assets(),
        "Income Quality Ratio": consume_def_company.ratios.get_income_quality_ratio(),
        "Equity Multiplier Ratio": consume_def_company.ratios.get_equity_multiplier(),
        "Gross Profit Margin Ratio": consume_def_company.ratios.get_gross_margin(),
        "Net Profit Margin Ratio": consume_def_company.ratios.get_net_profit_margin(),
        "Debt Service Coverage Ratio": consume_def_company.ratios.get_debt_service_coverage_ratio(),
        "Interest Coverage Ratio": consume_def_company.ratios.get_interest_burden_ratio(),
        "Short Term Coverage Ratio": consume_def_company.ratios.get_short_term_coverage_ratio()
    }

    # Initialize dictionaries to store averages and standard deviations
    consume_def_ratios = {}
    consume_def_industry_averages = {}
    consume_def_industry_std = {}

    # Calculate and store averages and standard deviations
    for key, value in consume_def_ratio_list.items():
        values = value.loc[consume_def_tickers].iloc[:, -1]
        values = values.replace([np.inf, -np.inf], np.nan).fillna(0)  # Replace inf with NaN and then fill NaN with 0
        consume_def_ratios[key] = values

        consume_def_ratio_avg = round(values.mean(), 2)
        consume_def_ratio_std = round(values.std(), 2)
        consume_def_industry_averages[key] = consume_def_ratio_avg
        consume_def_industry_std[key] = consume_def_ratio_std

    # Print the averages and standard deviations
    print(f"The following are the ratios for the {user_stock.info['sector']} sector")
    for key, value in consume_def_industry_averages.items():
        print(f"Average {key}: {value}")
        

    print("\n\n")
    
    consume_def_weights = {
        "Asset Turnover Ratio": 8,
        "Inventory Turnover Ratio": 8,
        "Accounts Payable Turnover Ratio": 5,
        "Receivable Turnover Ratio": 4,
        "Price to Earnings (P/E) Ratio": 3,
        "Current Ratio": 2,
        "Debt to Equity Ratio": 6,
        "Earnings Per Share Ratio": 2,
        "EV to EBITA Ratio": 5,
        "Cash Ratio": 3,
        "Debt to Assets Ratio": 1,
        "Price to Book Ratio": 3,
        "Return On Assets (ROA) Ratio": 10,
        "Income Quality Ratio": 9,
        "Equity Multiplier Ratio": 7,
        "Gross Profit Margin Ratio": 10,
        "Net Profit Margin Ratio": 11,
        "Debt Service Coverage Ratio": 1,
        "Interest Coverage Ratio": 1,
        "Short Term Coverage Ratio": 1
    }

    consume_def_preferences = {
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

    

    consume_def_pitroski_group = {}
    for ticker in consume_def_tickers:
        consume_def_pitroski_getter = consume_def_company.models.get_piotroski_score().loc[ticker].iloc[9, -1]
        if np.isinf(consume_def_pitroski_getter) or np.isnan(consume_def_pitroski_getter):
            consume_def_pitroski_getter = 0  # Handle infinity and NaN by setting to 0
        consume_def_pitroski_group[ticker] = consume_def_pitroski_getter

    # Calculate the mean of the Piotroski scores
    consume_def_pitroski_score = round(sum(consume_def_pitroski_group.values()) / len(consume_def_pitroski_group), 2)

        
    return {
        "consume_def_industry_std": consume_def_industry_std,
        "consume_def_industry_averages": consume_def_industry_averages,
        "consume_def_weights": consume_def_weights,
        "consume_def_preferences": consume_def_preferences,
        "consume_def_company": consume_def_company,
        "consume_def_pitroski_score": consume_def_pitroski_score
        
    }

