from financetoolkit import Toolkit
import os
import numpy as np  # Import numpy for NaN and inf handling
import yfinance as yf

def real_est_stats(ticker):
    user_stock = yf.Ticker(ticker)
    my_secret = os.environ['api_key10']

    # Ticker List
    real_est_tickers = [
        "PLD",
        "AMT",
        "EQIX",
        "WELL",
        "SPG",
        "SPG-PJ",
        "DLR",
        "PSA",
        "O",
        "PLDGP"
    ]

    # Calls the API for the specific company, data starts from 2022 end
    real_est_company = Toolkit(tickers=real_est_tickers,
                          api_key=my_secret,
                          start_date="2022-12-31")

    # Function to get ratio table
    real_est_ratio_list = {
        "Asset Turnover Ratio": real_est_company.ratios.get_asset_turnover_ratio(),
        "Inventory Turnover Ratio": real_est_company.ratios.get_inventory_turnover_ratio(),
        "Accounts Payable Turnover Ratio": real_est_company.ratios.get_accounts_payables_turnover_ratio(),
        "Receivable Turnover Ratio": real_est_company.ratios.get_receivables_turnover(),
        "Price to Earnings (P/E) Ratio": real_est_company.ratios.get_price_earnings_ratio(),
        "Current Ratio": real_est_company.ratios.get_current_ratio(),
        "Debt to Equity Ratio": real_est_company.ratios.get_debt_to_equity_ratio(),
        "Earnings Per Share Ratio": real_est_company.ratios.get_earnings_per_share(),
        "EV to EBITA Ratio":
        real_est_company.ratios.get_ev_to_ebitda_ratio(),
        "Cash Ratio": real_est_company.ratios.get_cash_ratio(),
        "Debt to Assets Ratio": real_est_company.ratios.get_debt_to_assets_ratio(),
        "Price to Book Ratio": real_est_company.ratios.get_price_to_book_ratio(),
        "Return On Assets (ROA) Ratio": real_est_company.ratios.get_return_on_assets(),
        "Income Quality Ratio": real_est_company.ratios.get_income_quality_ratio(),
        "Equity Multiplier Ratio": real_est_company.ratios.get_equity_multiplier(),
        "Gross Profit Margin Ratio": real_est_company.ratios.get_gross_margin(),
        "Net Profit Margin Ratio": real_est_company.ratios.get_net_profit_margin(),
        "Debt Service Coverage Ratio": real_est_company.ratios.get_debt_service_coverage_ratio(),
        "Interest Coverage Ratio": real_est_company.ratios.get_interest_burden_ratio(),
        "Short Term Coverage Ratio": real_est_company.ratios.get_short_term_coverage_ratio()
    }

    # Initialize dictionaries to store averages and standard deviations
    real_est_ratios = {}
    real_est_industry_averages = {}
    real_est_industry_std = {}

    # Calculate and store averages and standard deviations
    for key, value in real_est_ratio_list.items():
        values = value.loc[real_est_tickers].iloc[:, -1]
        values = values.replace([np.inf, -np.inf], np.nan).fillna(0)  # Replace inf with NaN and then fill NaN with 0
        real_est_ratios[key] = values

        real_est_ratio_avg = round(values.mean(), 2)
        real_est_ratio_std = round(values.std(), 2)
        real_est_industry_averages[key] = real_est_ratio_avg
        real_est_industry_std[key] = real_est_ratio_std

    # Print the averages and standard deviations
    print(f"The following are the ratios for the {user_stock.info['sector']} sector")
    for key, value in real_est_industry_averages.items():
        print(f"Average {key}: {value}")
        

    print("\n\n")
    
    real_est_weights = {
        "Asset Turnover Ratio": 9,
        "Inventory Turnover Ratio": 2,
        "Accounts Payable Turnover Ratio": 5,
        "Receivable Turnover Ratio": 8,
        "Price to Earnings (P/E) Ratio": 1,
        "Current Ratio": 4,
        "Debt to Equity Ratio": 7,
        "Earnings Per Share Ratio": 1,
        "EV to EBITA Ratio": 2,
        "Cash Ratio": 2,
        "Debt to Assets Ratio": 10,
        "Price to Book Ratio": 1,
        "Return On Assets (ROA) Ratio": 7,
        "Income Quality Ratio": 2,
        "Equity Multiplier Ratio": 12,
        "Gross Profit Margin Ratio": 3,
        "Net Profit Margin Ratio": 2,
        "Debt Service Coverage Ratio": 10,
        "Interest Coverage Ratio": 10,
        "Short Term Coverage Ratio": 2
    }

    real_est_preferences = {
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

    

    real_est_pitroski_group = {}
    for ticker in real_est_tickers:
        real_est_pitroski_getter = real_est_company.models.get_piotroski_score().loc[ticker].iloc[9, -1]
        if np.isinf(real_est_pitroski_getter) or np.isnan(real_est_pitroski_getter):
            real_est_pitroski_getter = 0  # Handle infinity and NaN by setting to 0
        real_est_pitroski_group[ticker] = real_est_pitroski_getter

    # Calculate the mean of the Piotroski scores
    real_est_pitroski_score = round(sum(real_est_pitroski_group.values()) / len(real_est_pitroski_group), 2)

        
    return {
        "real_est_industry_std": real_est_industry_std,
        "real_est_industry_averages": real_est_industry_averages,
        "real_est_weights": real_est_weights,
        "real_est_preferences": real_est_preferences,
        "real_est_company": real_est_company,
        "real_est_pitroski_score": real_est_pitroski_score
        
    }

