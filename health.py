from financetoolkit import Toolkit
import os
import numpy as np  # Import numpy for NaN and inf handling
import yfinance as yf

def health_stats(ticker):
    user_stock = yf.Ticker(ticker)
    my_secret = os.environ['api_key8']

    # Ticker List
    health_tickers = [
        "LLY",
        "NVO",
        "UNH",
        "JNJ",
        "MRK",
        "ABBV",
        "AZN",
        "RHHVF",
        "RHHBY",
        "NVS"
    ]

    # Calls the API for the specific company, data starts from 2022 end
    health_company = Toolkit(tickers=health_tickers,
                          api_key=my_secret,
                          start_date="2022-12-31")

    # Function to get ratio table
    health_ratio_list = {
        "Asset Turnover Ratio": health_company.ratios.get_asset_turnover_ratio(),
        "Inventory Turnover Ratio": health_company.ratios.get_inventory_turnover_ratio(),
        "Accounts Payable Turnover Ratio": health_company.ratios.get_accounts_payables_turnover_ratio(),
        "Receivable Turnover Ratio": health_company.ratios.get_receivables_turnover(),
        "Price to Earnings (P/E) Ratio": health_company.ratios.get_price_earnings_ratio(),
        "Current Ratio": health_company.ratios.get_current_ratio(),
        "Debt to Equity Ratio": health_company.ratios.get_debt_to_equity_ratio(),
        "Earnings Per Share Ratio": health_company.ratios.get_earnings_per_share(),
        "EV to EBITA Ratio":
        health_company.ratios.get_ev_to_ebitda_ratio(),
        "Cash Ratio": health_company.ratios.get_cash_ratio(),
        "Debt to Assets Ratio": health_company.ratios.get_debt_to_assets_ratio(),
        "Price to Book Ratio": health_company.ratios.get_price_to_book_ratio(),
        "Return On Assets (ROA) Ratio": health_company.ratios.get_return_on_assets(),
        "Income Quality Ratio": health_company.ratios.get_income_quality_ratio(),
        "Equity Multiplier Ratio": health_company.ratios.get_equity_multiplier(),
        "Gross Profit Margin Ratio": health_company.ratios.get_gross_margin(),
        "Net Profit Margin Ratio": health_company.ratios.get_net_profit_margin(),
        "Debt Service Coverage Ratio": health_company.ratios.get_debt_service_coverage_ratio(),
        "Interest Coverage Ratio": health_company.ratios.get_interest_burden_ratio(),
        "Short Term Coverage Ratio": health_company.ratios.get_short_term_coverage_ratio()
    }

    # Initialize dictionaries to store averages and standard deviations
    health_ratios = {}
    health_industry_averages = {}
    health_industry_std = {}

    # Calculate and store averages and standard deviations
    for key, value in health_ratio_list.items():
        values = value.loc[health_tickers].iloc[:, -1]
        values = values.replace([np.inf, -np.inf], np.nan).fillna(0)  # Replace inf with NaN and then fill NaN with 0
        health_ratios[key] = values

        health_ratio_avg = round(values.mean(), 2)
        health_ratio_std = round(values.std(), 2)
        health_industry_averages[key] = health_ratio_avg
        health_industry_std[key] = health_ratio_std

    # Print the averages and standard deviations
    print(f"The following are the ratios for the {user_stock.info['sector']} sector")
    for key, value in health_industry_averages.items():
        print(f"Average {key}: {value}")
        

    print("\n\n")
    
    health_weights = {
        "Asset Turnover Ratio": 2,
        "Inventory Turnover Ratio": 1,
        "Accounts Payable Turnover Ratio": 3,
        "Receivable Turnover Ratio": 4,
        "Price to Earnings (P/E) Ratio": 8,
        "Current Ratio": 11,
        "Debt to Equity Ratio": 8,
        "Earnings Per Share Ratio": 6,
        "EV to EBITA Ratio": 6,
        "Cash Ratio": 7,
        "Debt to Assets Ratio": 4,
        "Price to Book Ratio": 5,
        "Return On Assets (ROA) Ratio": 4,
        "Income Quality Ratio": 4,
        "Equity Multiplier Ratio": 2,
        "Gross Profit Margin Ratio": 5,
        "Net Profit Margin Ratio": 6,
        "Debt Service Coverage Ratio": 3,
        "Interest Coverage Ratio": 3,
        "Short Term Coverage Ratio": 8
    }

    health_preferences = {
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

    

    health_pitroski_group = {}
    for ticker in health_tickers:
        health_pitroski_getter = health_company.models.get_piotroski_score().loc[ticker].iloc[9, -1]
        if np.isinf(health_pitroski_getter) or np.isnan(health_pitroski_getter):
            health_pitroski_getter = 0  # Handle infinity and NaN by setting to 0
        health_pitroski_group[ticker] = health_pitroski_getter

    # Calculate the mean of the Piotroski scores
    health_pitroski_score = round(sum(health_pitroski_group.values()) / len(health_pitroski_group), 2)

        
    return {
        "health_industry_std": health_industry_std,
        "health_industry_averages": health_industry_averages,
        "health_weights": health_weights,
        "health_preferences": health_preferences,
        "health_company": health_company,
        "health_pitroski_score": health_pitroski_score
        
    }

