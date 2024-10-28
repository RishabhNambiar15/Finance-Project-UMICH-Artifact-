from financetoolkit import Toolkit
import os
import numpy as np  # Import numpy for NaN and inf handling
import yfinance as yf

def util_stats(ticker):
    user_stock = yf.Ticker(ticker)
    my_secret = os.environ['api_key12']

    # Ticker List
    util_tickers = [
        "NEE",
        "SO",
        "DUK",
        "CEG",
        "DUK-PA",
        "NGG",
        "SRE",
        "GEV",
        "AEP",
        "PCG"
    ]

    # Calls the API for the specific company, data starts from 2022 end
    util_company = Toolkit(tickers=util_tickers,
                          api_key=my_secret,
                          start_date="2022-12-31")

    # Function to get ratio table
    util_ratio_list = {
        "Asset Turnover Ratio": util_company.ratios.get_asset_turnover_ratio(),
        "Inventory Turnover Ratio": util_company.ratios.get_inventory_turnover_ratio(),
        "Accounts Payable Turnover Ratio": util_company.ratios.get_accounts_payables_turnover_ratio(),
        "Receivable Turnover Ratio": util_company.ratios.get_receivables_turnover(),
        "Price to Earnings (P/E) Ratio": util_company.ratios.get_price_earnings_ratio(),
        "Current Ratio": util_company.ratios.get_current_ratio(),
        "Debt to Equity Ratio": util_company.ratios.get_debt_to_equity_ratio(),
        "Earnings Per Share Ratio": util_company.ratios.get_earnings_per_share(),
        "EV to EBITA Ratio":
        util_company.ratios.get_ev_to_ebitda_ratio(),
        "Cash Ratio": util_company.ratios.get_cash_ratio(),
        "Debt to Assets Ratio": util_company.ratios.get_debt_to_assets_ratio(),
        "Price to Book Ratio": util_company.ratios.get_price_to_book_ratio(),
        "Return On Assets (ROA) Ratio": util_company.ratios.get_return_on_assets(),
        "Income Quality Ratio": util_company.ratios.get_income_quality_ratio(),
        "Equity Multiplier Ratio": util_company.ratios.get_equity_multiplier(),
        "Gross Profit Margin Ratio": util_company.ratios.get_gross_margin(),
        "Net Profit Margin Ratio": util_company.ratios.get_net_profit_margin(),
        "Debt Service Coverage Ratio": util_company.ratios.get_debt_service_coverage_ratio(),
        "Interest Coverage Ratio": util_company.ratios.get_interest_burden_ratio(),
        "Short Term Coverage Ratio": util_company.ratios.get_short_term_coverage_ratio()
    }

    # Initialize dictionaries to store averages and standard deviations
    util_ratios = {}
    util_industry_averages = {}
    util_industry_std = {}

    # Calculate and store averages and standard deviations
    for key, value in util_ratio_list.items():
        values = value.loc[util_tickers].iloc[:, -1]
        values = values.replace([np.inf, -np.inf], np.nan).fillna(0)  # Replace inf with NaN and then fill NaN with 0
        util_ratios[key] = values

        util_ratio_avg = round(values.mean(), 2)
        util_ratio_std = round(values.std(), 2)
        util_industry_averages[key] = util_ratio_avg
        util_industry_std[key] = util_ratio_std

    # Print the averages and standard deviations
    print(f"The following are the ratios for the {user_stock.info['sector']} sector")
    for key, value in util_industry_averages.items():
        print(f"Average {key}: {value}")
        

    print("\n\n")
    
    util_weights = {
        "Asset Turnover Ratio": 7,
        "Inventory Turnover Ratio": 6,
        "Accounts Payable Turnover Ratio": 5,
        "Receivable Turnover Ratio": 4,
        "Price to Earnings (P/E) Ratio": 3,
        "Current Ratio": 5,
        "Debt to Equity Ratio": 9,
        "Earnings Per Share Ratio": 2,
        "EV to EBITA Ratio": 5,
        "Cash Ratio": 5,
        "Debt to Assets Ratio": 8,
        "Price to Book Ratio": 2,
        "Return On Assets (ROA) Ratio": 1,
        "Income Quality Ratio": 1,
        "Equity Multiplier Ratio": 11,
        "Gross Profit Margin Ratio": 1,
        "Net Profit Margin Ratio": 1,
        "Debt Service Coverage Ratio": 10,
        "Interest Coverage Ratio": 8,
        "Short Term Coverage Ratio": 3
    }

    util_preferences = {
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

    

    util_pitroski_group = {}
    for ticker in util_tickers:
        util_pitroski_getter = util_company.models.get_piotroski_score().loc[ticker].iloc[9, -1]
        if np.isinf(util_pitroski_getter) or np.isnan(util_pitroski_getter):
            util_pitroski_getter = 0  # Handle infinity and NaN by setting to 0
        util_pitroski_group[ticker] = util_pitroski_getter

    # Calculate the mean of the Piotroski scores
    util_pitroski_score = round(sum(util_pitroski_group.values()) / len(util_pitroski_group), 2)

        
    return {
        "util_industry_std": util_industry_std,
        "util_industry_averages": util_industry_averages,
        "util_weights": util_weights,
        "util_preferences": util_preferences,
        "util_company": util_company,
        "util_pitroski_score": util_pitroski_score
        
    }

