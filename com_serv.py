from financetoolkit import Toolkit
import os
import numpy as np  # Import numpy for NaN and inf handling
import yfinance as yf

def com_serv_stats(ticker):
    user_stock = yf.Ticker(ticker)
    my_secret = os.environ['api_key17']

    # Ticker Lister
    com_serv_tickers = [
        "GOOG",
        "META",
        "NFLX",
        "TMUS",
        "DIS",
        "VZ",
        "CMCSA",
        "T",
        "DTEGF",
        "DTEGY"
    ]

    # Calls the API for the specific company, data starts from 2022 end
    com_serv_company = Toolkit(tickers=com_serv_tickers,
                          api_key=my_secret,
                          start_date="2022-12-31")

    # Function to get ratio table
    com_serv_ratio_list = {
        "Asset Turnover Ratio": com_serv_company.ratios.get_asset_turnover_ratio(),
        "Inventory Turnover Ratio": com_serv_company.ratios.get_inventory_turnover_ratio(),
        "Accounts Payable Turnover Ratio": com_serv_company.ratios.get_accounts_payables_turnover_ratio(),
        "Receivable Turnover Ratio": com_serv_company.ratios.get_receivables_turnover(),
        "Price to Earnings (P/E) Ratio": com_serv_company.ratios.get_price_earnings_ratio(),
        "Current Ratio": com_serv_company.ratios.get_current_ratio(),
        "Debt to Equity Ratio": com_serv_company.ratios.get_debt_to_equity_ratio(),
        "Earnings Per Share Ratio": com_serv_company.ratios.get_earnings_per_share(),
        "EV to EBITA Ratio": com_serv_company.ratios.get_ev_to_ebitda_ratio(),
        "Cash Ratio": com_serv_company.ratios.get_cash_ratio(),
        "Debt to Assets Ratio": com_serv_company.ratios.get_debt_to_assets_ratio(),
        "Price to Book Ratio": com_serv_company.ratios.get_price_to_book_ratio(),
        "Return On Assets (ROA) Ratio": com_serv_company.ratios.get_return_on_assets(),
        "Income Quality Ratio": com_serv_company.ratios.get_income_quality_ratio(),
        "Equity Multiplier Ratio": com_serv_company.ratios.get_equity_multiplier(),
        "Gross Profit Margin Ratio": com_serv_company.ratios.get_gross_margin(),
        "Net Profit Margin Ratio": com_serv_company.ratios.get_net_profit_margin(),
        "Debt Service Coverage Ratio": com_serv_company.ratios.get_debt_service_coverage_ratio(),
        "Interest Coverage Ratio": com_serv_company.ratios.get_interest_burden_ratio(),
        "Short Term Coverage Ratio": com_serv_company.ratios.get_short_term_coverage_ratio()
    }

    # Initialize dictionaries to store averages and standard deviations
    com_serv_ratios = {}
    com_serv_industry_averages = {}
    com_serv_industry_std = {}

    # Calculate and store averages and standard deviations
    for key, value in com_serv_ratio_list.items():
        values = value.loc[com_serv_tickers].iloc[:, -1]
        values = values.replace([np.inf, -np.inf], np.nan).fillna(0)  # Replace inf with NaN and then fill NaN with 0
        com_serv_ratios[key] = values

        com_serv_ratio_avg = round(values.mean(), 2)
        com_serv_ratio_std = round(values.std(), 2)
        com_serv_industry_averages[key] = com_serv_ratio_avg
        com_serv_industry_std[key] = com_serv_ratio_std

    # Print the averages and standard deviations
    print(f"The following are the ratios for the {user_stock.info['sector']} sector")
    for key, value in com_serv_industry_averages.items():
        print(f"Average {key}: {value}")
        

    print("\n\n")
    
    com_serv_weights = {
        "Asset Turnover Ratio": 5,
        "Inventory Turnover Ratio": 2,
        "Accounts Payable Turnover Ratio": 4,
        "Receivable Turnover Ratio": 6,
        "Price to Earnings (P/E) Ratio": 8,
        "Current Ratio": 4,
        "Debt to Equity Ratio": 5,
        "Earnings Per Share Ratio": 6,
        "EV to EBITA Ratio": 5,
        "Cash Ratio": 4,
        "Debt to Assets Ratio": 5,
        "Price to Book Ratio": 6,
        "Return On Assets (ROA) Ratio": 6,
        "Income Quality Ratio": 5,
        "Equity Multiplier Ratio": 4,
        "Gross Profit Margin Ratio": 7,
        "Net Profit Margin Ratio": 8,
        "Debt Service Coverage Ratio": 5,
        "Interest Coverage Ratio": 3,
        "Short Term Coverage Ratio": 2
    }

    com_serv_preferences = {
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

    

    com_serv_pitroski_group = {}
    for ticker in com_serv_tickers:
        com_serv_pitroski_getter = com_serv_company.models.get_piotroski_score().loc[ticker].iloc[9, -1]
        if np.isinf(com_serv_pitroski_getter) or np.isnan(com_serv_pitroski_getter):
            com_serv_pitroski_getter = 0  # Handle infinity and NaN by setting to 0
        com_serv_pitroski_group[ticker] = com_serv_pitroski_getter

    # Calculate the mean of the Piotroski scores
    com_serv_pitroski_score = round(sum(com_serv_pitroski_group.values()) / len(com_serv_pitroski_group), 2)

        
    return {
        "com_serv_industry_std": com_serv_industry_std,
        "com_serv_industry_averages": com_serv_industry_averages,
        "com_serv_weights": com_serv_weights,
        "com_serv_preferences": com_serv_preferences,
        "com_serv_company": com_serv_company,
        "com_serv_pitroski_score": com_serv_pitroski_score
        
    }

