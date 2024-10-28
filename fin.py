from financetoolkit import Toolkit
import os
import numpy as np  # Import numpy for NaN and inf handling
import yfinance as yf

def fin_stats(ticker):
    user_stock = yf.Ticker(ticker)
    my_secret = os.environ['api_key7']

    # Ticker List
    fin_tickers = [
        "BRK-B",
        "JPM",
        "V",
        "MA",
        "BAC",
        "CMCSA",
        "T",
        "DTEGF",
        "DTEGY"
    ]

    # Calls the API for the specific company, data starts from 2022 end
    fin_company = Toolkit(tickers=fin_tickers,
                          api_key=my_secret,
                          start_date="2022-12-31")

    # Function to get ratio table
    fin_ratio_list = {
        "Asset Turnover Ratio": fin_company.ratios.get_asset_turnover_ratio(),
        "Inventory Turnover Ratio": fin_company.ratios.get_inventory_turnover_ratio(),
        "Accounts Payable Turnover Ratio": fin_company.ratios.get_accounts_payables_turnover_ratio(),
        "Receivable Turnover Ratio": fin_company.ratios.get_receivables_turnover(),
        "Price to Earnings (P/E) Ratio": fin_company.ratios.get_price_earnings_ratio(),
        "Current Ratio": fin_company.ratios.get_current_ratio(),
        "Debt to Equity Ratio": fin_company.ratios.get_debt_to_equity_ratio(),
        "Earnings Per Share Ratio": fin_company.ratios.get_earnings_per_share(),
        "EV to EBITA Ratio":
        fin_company.ratios.get_ev_to_ebitda_ratio(),
        "Cash Ratio": fin_company.ratios.get_cash_ratio(),
        "Debt to Assets Ratio": fin_company.ratios.get_debt_to_assets_ratio(),
        "Price to Book Ratio": fin_company.ratios.get_price_to_book_ratio(),
        "Return On Assets (ROA) Ratio": fin_company.ratios.get_return_on_assets(),
        "Income Quality Ratio": fin_company.ratios.get_income_quality_ratio(),
        "Equity Multiplier Ratio": fin_company.ratios.get_equity_multiplier(),
        "Gross Profit Margin Ratio": fin_company.ratios.get_gross_margin(),
        "Net Profit Margin Ratio": fin_company.ratios.get_net_profit_margin(),
        "Debt Service Coverage Ratio": fin_company.ratios.get_debt_service_coverage_ratio(),
        "Interest Coverage Ratio": fin_company.ratios.get_interest_burden_ratio(),
        "Short Term Coverage Ratio": fin_company.ratios.get_short_term_coverage_ratio()
    }

    # Initialize dictionaries to store averages and standard deviations
    fin_ratios = {}
    fin_industry_averages = {}
    fin_industry_std = {}

    # Calculate and store averages and standard deviations
    for key, value in fin_ratio_list.items():
        values = value.loc[fin_tickers].iloc[:, -1]
        values = values.replace([np.inf, -np.inf], np.nan).fillna(0)  # Replace inf with NaN and then fill NaN with 0
        fin_ratios[key] = values

        fin_ratio_avg = round(values.mean(), 2)
        fin_ratio_std = round(values.std(), 2)
        fin_industry_averages[key] = fin_ratio_avg
        fin_industry_std[key] = fin_ratio_std

    # Print the averages and standard deviations
    print(f"The following are the ratios for the {user_stock.info['sector']} sector")
    for key, value in fin_industry_averages.items():
        print(f"Average {key}: {value}")
        

    print("\n\n")
    
    fin_weights = {
        "Asset Turnover Ratio": 8,
        "Inventory Turnover Ratio": 1,
        "Accounts Payable Turnover Ratio": 7,
        "Receivable Turnover Ratio": 7,
        "Price to Earnings (P/E) Ratio": 6,
        "Current Ratio": 7,
        "Debt to Equity Ratio": 7,
        "Earnings Per Share Ratio": 5,
        "EV to EBITA Ratio": 5,
        "Cash Ratio": 6,
        "Debt to Assets Ratio": 2,
        "Price to Book Ratio": 4,
        "Return On Assets (ROA) Ratio": 7,
        "Income Quality Ratio": 5,
        "Equity Multiplier Ratio": 2,
        "Gross Profit Margin Ratio": 6,
        "Net Profit Margin Ratio": 8,
        "Debt Service Coverage Ratio": 1,
        "Interest Coverage Ratio": 2,
        "Short Term Coverage Ratio": 4
    }

    fin_preferences = {
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

    

    fin_pitroski_group = {}
    for ticker in fin_tickers:
        fin_pitroski_getter = fin_company.models.get_piotroski_score().loc[ticker].iloc[9, -1]
        if np.isinf(fin_pitroski_getter) or np.isnan(fin_pitroski_getter):
            fin_pitroski_getter = 0  # Handle infinity and NaN by setting to 0
        fin_pitroski_group[ticker] = fin_pitroski_getter

    # Calculate the mean of the Piotroski scores
    fin_pitroski_score = round(sum(fin_pitroski_group.values()) / len(fin_pitroski_group), 2)

        
    return {
        "fin_industry_std": fin_industry_std,
        "fin_industry_averages": fin_industry_averages,
        "fin_weights": fin_weights,
        "fin_preferences": fin_preferences,
        "fin_company": fin_company,
        "fin_pitroski_score": fin_pitroski_score
        
    }

