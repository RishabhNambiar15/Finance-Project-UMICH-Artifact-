from financetoolkit import Toolkit
import os
import numpy as np  # Import numpy for NaN and inf handling
import yfinance as yf

def basic_mats_stats(ticker):
    user_stock = yf.Ticker(ticker)
    my_secret = os.environ['api_key2']

    # Ticker List
    basic_mats_tickers = [
        "LIN",
        "BHP",
        "RIO",
        "SCCO",
        "SHW",
        "FCX",
        "ECL",
        "CTA-PB",
        "APD",
        "CRH"
    ]

    # Calls the API for the specific company, data starts from 2022 end
    basic_mats_company = Toolkit(tickers=basic_mats_tickers,
                          api_key=my_secret,
                          start_date="2022-12-31")

    # Function to get ratio table
    basic_mats_ratio_list = {
        "Asset Turnover Ratio": basic_mats_company.ratios.get_asset_turnover_ratio(),
        "Inventory Turnover Ratio": basic_mats_company.ratios.get_inventory_turnover_ratio(),
        "Accounts Payable Turnover Ratio": basic_mats_company.ratios.get_accounts_payables_turnover_ratio(),
        "Receivable Turnover Ratio": basic_mats_company.ratios.get_receivables_turnover(),
        "Price to Earnings (P/E) Ratio": basic_mats_company.ratios.get_price_earnings_ratio(),
        "Current Ratio": basic_mats_company.ratios.get_current_ratio(),
        "Debt to Equity Ratio": basic_mats_company.ratios.get_debt_to_equity_ratio(),
        "Earnings Per Share Ratio": basic_mats_company.ratios.get_earnings_per_share(),
        "EV to EBITA Ratio":
        basic_mats_company.ratios.get_ev_to_ebitda_ratio(),
        "Cash Ratio": basic_mats_company.ratios.get_cash_ratio(),
        "Debt to Assets Ratio": basic_mats_company.ratios.get_debt_to_assets_ratio(),
        "Price to Book Ratio": basic_mats_company.ratios.get_price_to_book_ratio(),
        "Return On Assets (ROA) Ratio": basic_mats_company.ratios.get_return_on_assets(),
        "Income Quality Ratio": basic_mats_company.ratios.get_income_quality_ratio(),
        "Equity Multiplier Ratio": basic_mats_company.ratios.get_equity_multiplier(),
        "Gross Profit Margin Ratio": basic_mats_company.ratios.get_gross_margin(),
        "Net Profit Margin Ratio": basic_mats_company.ratios.get_net_profit_margin(),
        "Debt Service Coverage Ratio": basic_mats_company.ratios.get_debt_service_coverage_ratio(),
        "Interest Coverage Ratio": basic_mats_company.ratios.get_interest_burden_ratio(),
        "Short Term Coverage Ratio": basic_mats_company.ratios.get_short_term_coverage_ratio()
    }

    # Initialize dictionaries to store averages and standard deviations
    basic_mats_ratios = {}
    basic_mats_industry_averages = {}
    basic_mats_industry_std = {}

    # Calculate and store averages and standard deviations
    for key, value in basic_mats_ratio_list.items():
        values = value.loc[basic_mats_tickers].iloc[:, -1]
        values = values.replace([np.inf, -np.inf], np.nan).fillna(0)  # Replace inf with NaN and then fill NaN with 0
        basic_mats_ratios[key] = values

        basic_mats_ratio_avg = round(values.mean(), 2)
        basic_mats_ratio_std = round(values.std(), 2)
        basic_mats_industry_averages[key] = basic_mats_ratio_avg
        basic_mats_industry_std[key] = basic_mats_ratio_std

    # Print the averages and standard deviations
    print(f"The following are the ratios for the {user_stock.info['sector']} sector")
    for key, value in basic_mats_industry_averages.items():
        print(f"Average {key}: {value}")
        

    print("\n\n")
    
    basic_mats_weights = {
        "Asset Turnover Ratio": 5,
        "Inventory Turnover Ratio": 3,
        "Accounts Payable Turnover Ratio": 4,
        "Receivable Turnover Ratio": 3,
        "Price to Earnings (P/E) Ratio": 2,
        "Current Ratio": 7,
        "Debt to Equity Ratio": 10,
        "Earnings Per Share Ratio": 3,
        "EV to EBITA Ratio": 3,
        "Cash Ratio": 6,
        "Debt to Assets Ratio": 8,
        "Price to Book Ratio": 8,
        "Return On Assets (ROA) Ratio": 6,
        "Income Quality Ratio": 3,
        "Equity Multiplier Ratio": 10,
        "Gross Profit Margin Ratio": 3,
        "Net Profit Margin Ratio": 3,
        "Debt Service Coverage Ratio": 5,
        "Interest Coverage Ratio": 7 ,
        "Short Term Coverage Ratio": 1 
    }

    basic_mats_preferences = {
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

    

    basic_mats_pitroski_group = {}
    for ticker in basic_mats_tickers:
        basic_mats_pitroski_getter = basic_mats_company.models.get_piotroski_score().loc[ticker].iloc[9, -1]
        if np.isinf(basic_mats_pitroski_getter) or np.isnan(basic_mats_pitroski_getter):
            basic_mats_pitroski_getter = 0  # Handle infinity and NaN by setting to 0
        basic_mats_pitroski_group[ticker] = basic_mats_pitroski_getter

    # Calculate the mean of the Piotroski scores
    basic_mats_pitroski_score = round(sum(basic_mats_pitroski_group.values()) / len(basic_mats_pitroski_group), 2)

        
    return {
        "basic_mats_industry_std": basic_mats_industry_std,
        "basic_mats_industry_averages": basic_mats_industry_averages,
        "basic_mats_weights": basic_mats_weights,
        "basic_mats_preferences": basic_mats_preferences,
        "basic_mats_company": basic_mats_company,
        "basic_mats_pitroski_score": basic_mats_pitroski_score
        
    }

