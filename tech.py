from financetoolkit import Toolkit
import os
import numpy as np  # Import numpy for NaN and inf handling
import yfinance as yf

def tech_stats(ticker):
    user_stock = yf.Ticker(ticker)
    my_secret = os.environ['api_key11']

    # Ticker List
    tech_tickers = [
        "MSFT",
        "AAPL",
        "NVDA",
        "TSM",
        "AVGO",
        "XOM",
        "ASML",
        "ORCL",
        "CVX",
        "AMD"
    ]

    # Calls the API for the specific company, data starts from 2022 end
    tech_company = Toolkit(tickers=tech_tickers,
                          api_key=my_secret,
                          start_date="2022-12-31")

    # Function to get ratio table
    tech_ratio_list = {
        "Asset Turnover Ratio": tech_company.ratios.get_asset_turnover_ratio(),
        "Inventory Turnover Ratio": tech_company.ratios.get_inventory_turnover_ratio(),
        "Accounts Payable Turnover Ratio": tech_company.ratios.get_accounts_payables_turnover_ratio(),
        "Receivable Turnover Ratio": tech_company.ratios.get_receivables_turnover(),
        "Price to Earnings (P/E) Ratio": tech_company.ratios.get_price_earnings_ratio(),
        "Current Ratio": tech_company.ratios.get_current_ratio(),
        "Debt to Equity Ratio": tech_company.ratios.get_debt_to_equity_ratio(),
        "Earnings Per Share Ratio": tech_company.ratios.get_earnings_per_share(),
        "EV to EBITA Ratio":
        tech_company.ratios.get_ev_to_ebitda_ratio(),
        "Cash Ratio": tech_company.ratios.get_cash_ratio(),
        "Debt to Assets Ratio": tech_company.ratios.get_debt_to_assets_ratio(),
        "Price to Book Ratio": tech_company.ratios.get_price_to_book_ratio(),
        "Return On Assets (ROA) Ratio": tech_company.ratios.get_return_on_assets(),
        "Income Quality Ratio": tech_company.ratios.get_income_quality_ratio(),
        "Equity Multiplier Ratio": tech_company.ratios.get_equity_multiplier(),
        "Gross Profit Margin Ratio": tech_company.ratios.get_gross_margin(),
        "Net Profit Margin Ratio": tech_company.ratios.get_net_profit_margin(),
        "Debt Service Coverage Ratio": tech_company.ratios.get_debt_service_coverage_ratio(),
        "Interest Coverage Ratio": tech_company.ratios.get_interest_burden_ratio(),
        "Short Term Coverage Ratio": tech_company.ratios.get_short_term_coverage_ratio()
    }

    # Initialize dictionaries to store averages and standard deviations
    tech_ratios = {}
    tech_industry_averages = {}
    tech_industry_std = {}

    # Calculate and store averages and standard deviations
    for key, value in tech_ratio_list.items():
        values = value.loc[tech_tickers].iloc[:, -1]
        values = values.replace([np.inf, -np.inf], np.nan).fillna(0)  # Replace inf with NaN and then fill NaN with 0
        tech_ratios[key] = values

        tech_ratio_avg = round(values.mean(), 2)
        tech_ratio_std = round(values.std(), 2)
        tech_industry_averages[key] = tech_ratio_avg
        tech_industry_std[key] = tech_ratio_std

    # Print the averages and standard deviations
    print(f"The following are the ratios for the {user_stock.info['sector']} sector")
    for key, value in tech_industry_averages.items():
        print(f"Average {key}: {value}")
        

    print("\n\n")

    print(tech_industry_std)
    tech_weights = {
        "Asset Turnover Ratio": 6,
        "Inventory Turnover Ratio": 7,
        "Accounts Payable Turnover Ratio": 7,
        "Receivable Turnover Ratio": 7,
        "Price to Earnings (P/E) Ratio": 8,
        "Current Ratio": 5,
        "Debt to Equity Ratio": 6,
        "Earnings Per Share Ratio": 5,
        "EV to EBITA Ratio": 4,
        "Cash Ratio": 4,
        "Debt to Assets Ratio": 2,
        "Price to Book Ratio": 5,
        "Return On Assets (ROA) Ratio": 6,
        "Income Quality Ratio": 6,
        "Equity Multiplier Ratio": 3,
        "Gross Profit Margin Ratio": 6,
        "Net Profit Margin Ratio": 7,
        "Debt Service Coverage Ratio": 1,
        "Interest Coverage Ratio": 2,
        "Short Term Coverage Ratio": 3
    }

    tech_preferences = {
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

    

    tech_pitroski_group = {}
    for ticker in tech_tickers:
        tech_pitroski_getter = tech_company.models.get_piotroski_score().loc[ticker].iloc[9, -1]
        if np.isinf(tech_pitroski_getter) or np.isnan(tech_pitroski_getter):
            tech_pitroski_getter = 0  # Handle infinity and NaN by setting to 0
        tech_pitroski_group[ticker] = tech_pitroski_getter

    # Calculate the mean of the Piotroski scores
    tech_pitroski_score = round(sum(tech_pitroski_group.values()) / len(tech_pitroski_group), 2)

        
    return {
        "tech_industry_std": tech_industry_std,
        "tech_industry_averages": tech_industry_averages,
        "tech_weights": tech_weights,
        "tech_preferences": tech_preferences,
        "tech_company": tech_company,
        "tech_pitroski_score": tech_pitroski_score
        
    }

