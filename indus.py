from financetoolkit import Toolkit
import os
import numpy as np  # Import numpy for NaN and inf handling
import yfinance as yf

def indus_stats(ticker):
    user_stock = yf.Ticker(ticker)
    my_secret = os.environ['api_key18']

    # Ticker List
    indus_tickers = [
        "GE",
        "CAT",
        "HON",
        "UNP",
        "RTX",
        "ETN",
        "UPS",
        "BA",
        "LMT",
        "DE"
    ]

    # Calls the API for the specific company, data starts from 2022 end
    indus_company = Toolkit(tickers=indus_tickers,
                          api_key=my_secret,
                          start_date="2022-12-31")

    # Function to get ratio table
    indus_ratio_list = {
        "Asset Turnover Ratio": indus_company.ratios.get_asset_turnover_ratio(),
        "Inventory Turnover Ratio": indus_company.ratios.get_inventory_turnover_ratio(),
        "Accounts Payable Turnover Ratio": indus_company.ratios.get_accounts_payables_turnover_ratio(),
        "Receivable Turnover Ratio": indus_company.ratios.get_receivables_turnover(),
        "Price to Earnings (P/E) Ratio": indus_company.ratios.get_price_earnings_ratio(),
        "Current Ratio": indus_company.ratios.get_current_ratio(),
        "Debt to Equity Ratio": indus_company.ratios.get_debt_to_equity_ratio(),
        "Earnings Per Share Ratio": indus_company.ratios.get_earnings_per_share(),
        "EV to EBITA Ratio":
        indus_company.ratios.get_ev_to_ebitda_ratio(),
        "Cash Ratio": indus_company.ratios.get_cash_ratio(),
        "Debt to Assets Ratio": indus_company.ratios.get_debt_to_assets_ratio(),
        "Price to Book Ratio": indus_company.ratios.get_price_to_book_ratio(),
        "Return On Assets (ROA) Ratio": indus_company.ratios.get_return_on_assets(),
        "Income Quality Ratio": indus_company.ratios.get_income_quality_ratio(),
        "Equity Multiplier Ratio": indus_company.ratios.get_equity_multiplier(),
        "Gross Profit Margin Ratio": indus_company.ratios.get_gross_margin(),
        "Net Profit Margin Ratio": indus_company.ratios.get_net_profit_margin(),
        "Debt Service Coverage Ratio": indus_company.ratios.get_debt_service_coverage_ratio(),
        "Interest Coverage Ratio": indus_company.ratios.get_interest_burden_ratio(),
        "Short Term Coverage Ratio": indus_company.ratios.get_short_term_coverage_ratio()
    }

    # Initialize dictionaries to store averages and standard deviations
    indus_ratios = {}
    indus_industry_averages = {}
    indus_industry_std = {}

    # Calculate and store averages and standard deviations
    for key, value in indus_ratio_list.items():
        values = value.loc[indus_tickers].iloc[:, -1]
        values = values.replace([np.inf, -np.inf], np.nan).fillna(0)  # Replace inf with NaN and then fill NaN with 0
        indus_ratios[key] = values

        indus_ratio_avg = round(values.mean(), 2)
        indus_ratio_std = round(values.std(), 2)
        indus_industry_averages[key] = indus_ratio_avg
        indus_industry_std[key] = indus_ratio_std

    # Print the averages and standard deviations
    print(f"The following are the ratios for the {user_stock.info['sector']} sector")
    for key, value in indus_industry_averages.items():
        print(f"Average {key}: {value}")
        

    print("\n\n")
    
    indus_weights = {
        "Asset Turnover Ratio": 9,
        "Inventory Turnover Ratio": 9,
        "Accounts Payable Turnover Ratio": 8,
        "Receivable Turnover Ratio": 7,
        "Price to Earnings (P/E) Ratio": 1,
        "Current Ratio": 3,
        "Debt to Equity Ratio": 7,
        "Earnings Per Share Ratio": 4,
        "EV to EBITA Ratio": 6,
        "Cash Ratio": 2,
        "Debt to Assets Ratio": 8,
        "Price to Book Ratio": 3,
        "Return On Assets (ROA) Ratio": 5,
        "Income Quality Ratio": 3,
        "Equity Multiplier Ratio": 7,
        "Gross Profit Margin Ratio": 2,
        "Net Profit Margin Ratio": 2,
        "Debt Service Coverage Ratio": 6,
        "Interest Coverage Ratio": 7,
        "Short Term Coverage Ratio": 1
    }

    indus_preferences = {
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

    

    indus_pitroski_group = {}
    for ticker in indus_tickers:
        indus_pitroski_getter = indus_company.models.get_piotroski_score().loc[ticker].iloc[9, -1]
        if np.isinf(indus_pitroski_getter) or np.isnan(indus_pitroski_getter):
            indus_pitroski_getter = 0  # Handle infinity and NaN by setting to 0
        indus_pitroski_group[ticker] = indus_pitroski_getter

    # Calculate the mean of the Piotroski scores
    indus_pitroski_score = round(sum(indus_pitroski_group.values()) / len(indus_pitroski_group), 2)

        
    return {
        "indus_industry_std": indus_industry_std,
        "indus_industry_averages": indus_industry_averages,
        "indus_weights": indus_weights,
        "indus_preferences": indus_preferences,
        "indus_company": indus_company,
        "indus_pitroski_score": indus_pitroski_score
        
    }

