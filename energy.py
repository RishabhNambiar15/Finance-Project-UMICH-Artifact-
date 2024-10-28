from financetoolkit import Toolkit
import os
import numpy as np  # Import numpy for NaN and inf handling
import yfinance as yf

def energy_stats(ticker):
    user_stock = yf.Ticker(ticker)
    my_secret = os.environ['api_key16']

    # Ticker List
    energy_tickers = ["XOM",
                    "CVX",
                    "SHEL",
                    "TTE",
                    "COP",
                    "BP",
                    "PBR",
                    "PBR-A",
                    "EQNR",
                    "CNQ"]

    # Calls the API for the specific company, data starts from 2022 end
    energy_company = Toolkit(tickers=energy_tickers,
                          api_key=my_secret,
                          start_date="2022-12-31")

    # Function to get ratio table
    energy_ratio_list = {
        "Asset Turnover Ratio": energy_company.ratios.get_asset_turnover_ratio(),
        "Inventory Turnover Ratio": energy_company.ratios.get_inventory_turnover_ratio(),
        "Accounts Payable Turnover Ratio": energy_company.ratios.get_accounts_payables_turnover_ratio(),
        "Receivable Turnover Ratio": energy_company.ratios.get_receivables_turnover(),
        "Price to Earnings (P/E) Ratio": energy_company.ratios.get_price_earnings_ratio(),
        "Current Ratio": energy_company.ratios.get_current_ratio(),
        "Debt to Equity Ratio": energy_company.ratios.get_debt_to_equity_ratio(),
        "Earnings Per Share Ratio": energy_company.ratios.get_earnings_per_share(),
        "EV to EBITA Ratio":
        energy_company.ratios.get_ev_to_ebitda_ratio(),
        "Cash Ratio": energy_company.ratios.get_cash_ratio(),
        "Debt to Assets Ratio": energy_company.ratios.get_debt_to_assets_ratio(),
        "Price to Book Ratio": energy_company.ratios.get_price_to_book_ratio(),
        "Return On Assets (ROA) Ratio": energy_company.ratios.get_return_on_assets(),
        "Income Quality Ratio": energy_company.ratios.get_income_quality_ratio(),
        "Equity Multiplier Ratio": energy_company.ratios.get_equity_multiplier(),
        "Gross Profit Margin Ratio": energy_company.ratios.get_gross_margin(),
        "Net Profit Margin Ratio": energy_company.ratios.get_net_profit_margin(),
        "Debt Service Coverage Ratio": energy_company.ratios.get_debt_service_coverage_ratio(),
        "Interest Coverage Ratio": energy_company.ratios.get_interest_burden_ratio(),
        "Short Term Coverage Ratio": energy_company.ratios.get_short_term_coverage_ratio()
    }

    # Initialize dictionaries to store averages and standard deviations
    energy_ratios = {}
    energy_industry_averages = {}
    energy_industry_std = {}

    # Calculate and store averages and standard deviations
    for key, value in energy_ratio_list.items():
        values = value.loc[energy_tickers].iloc[:, -1]
        values = values.replace([np.inf, -np.inf], np.nan).fillna(0)  # Replace inf with NaN and then fill NaN with 0
        energy_ratios[key] = values

        energy_ratio_avg = round(values.mean(), 2)
        energy_ratio_std = round(values.std(), 2)
        energy_industry_averages[key] = energy_ratio_avg
        energy_industry_std[key] = energy_ratio_std

    # Print the averages and standard deviations
    print(f"The following are the ratios for the {user_stock.info['sector']} sector")
    for key, value in energy_industry_averages.items():
        print(f"Average {key}: {value}")
        

    print("\n\n")
    
    energy_weights = {
        "Asset Turnover Ratio": 17,
        "Inventory Turnover Ratio": 1,
        "Accounts Payable Turnover Ratio": 2,
        "Receivable Turnover Ratio": 2,
        "Price to Earnings (P/E) Ratio": 4,
        "Current Ratio": 3,
        "Debt to Equity Ratio": 4,
        "Earnings Per Share Ratio": 5,
        "EV to EBITA Ratio": 3,
        "Cash Ratio": 4,
        "Debt to Assets Ratio": 10,
        "Price to Book Ratio": 2,
        "Return On Assets (ROA) Ratio": 8,
        "Income Quality Ratio": 1,
        "Equity Multiplier Ratio": 11,
        "Gross Profit Margin Ratio": 1,
        "Net Profit Margin Ratio": 1,
        "Debt Service Coverage Ratio": 10,
        "Interest Coverage Ratio": 10,
        "Short Term Coverage Ratio": 1
    }

    energy_preferences = {
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

    

    energy_pitroski_group = {}
    for ticker in energy_tickers:
        energy_pitroski_getter = energy_company.models.get_piotroski_score().loc[ticker].iloc[9, -1]
        if np.isinf(energy_pitroski_getter) or np.isnan(energy_pitroski_getter):
            energy_pitroski_getter = 0  # Handle infinity and NaN by setting to 0
        energy_pitroski_group[ticker] = energy_pitroski_getter

    # Calculate the mean of the Piotroski scores
    energy_pitroski_score = round(sum(energy_pitroski_group.values()) / len(energy_pitroski_group), 2)

        
    return {
        "energy_industry_std": energy_industry_std,
        "energy_industry_averages": energy_industry_averages,
        "energy_weights": energy_weights,
        "energy_preferences": energy_preferences,
        "energy_company": energy_company,
        "energy_pitroski_score": energy_pitroski_score
        
    }

