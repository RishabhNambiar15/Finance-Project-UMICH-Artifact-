from financetoolkit import Toolkit
import os
import fin
import tech
import consume_cyc
import health
import com_serv
import indus
import consume_def
import energy
import basic_mats
import real_est
import util
import numpy as np  # Import numpy for NaN and inf handling
import yfinance as yf
import financedatabase as fd
import pandas as pd

my_secret = os.environ['api_key15']

ticker = input("Enter The Stock Ticker: ").upper()
user_stock = yf.Ticker(ticker)
company_full_name = user_stock.info['longName']
print(f"Full Name: {company_full_name}")
#print(f"Sector: {user_stock.info['sector']}")


#calls the api for the specific company, data starts from 2023 end
user_company = Toolkit(ticker, api_key=my_secret)

# function to get ratio table

user_ratio_list = {
    "Asset Turnover Ratio":
    user_company.ratios.get_asset_turnover_ratio(),
    "Inventory Turnover Ratio":
    user_company.ratios.get_inventory_turnover_ratio(),
    "Accounts Payable Turnover Ratio":
    user_company.ratios.get_accounts_payables_turnover_ratio(),
    "Receivable Turnover Ratio":
    user_company.ratios.get_receivables_turnover(),
    "Price to Earnings (P/E) Ratio":
    user_company.ratios.get_price_earnings_ratio(),
    "Current Ratio":
    user_company.ratios.get_current_ratio(),
    "Debt to Equity Ratio":
    user_company.ratios.get_debt_to_equity_ratio(),
    "Earnings Per Share Ratio":
    user_company.ratios.get_earnings_per_share(),
    "EV to EBITA Ratio":
    user_company.ratios.get_ev_to_ebitda_ratio(),
    "Cash Ratio":
    user_company.ratios.get_cash_ratio(),
    "Debt to Assets Ratio":
    user_company.ratios.get_debt_to_assets_ratio(),
    "Price to Book Ratio":
    user_company.ratios.get_price_to_book_ratio(),
    "Return On Assets (ROA) Ratio":
    user_company.ratios.get_return_on_assets(),
    "Income Quality Ratio":
    user_company.ratios.get_income_quality_ratio(),
    "Equity Multiplier Ratio":
    user_company.ratios.get_equity_multiplier(),
    "Gross Profit Margin Ratio":
    user_company.ratios.get_gross_margin(),
    "Net Profit Margin Ratio":
    user_company.ratios.get_net_profit_margin(),
    "Debt Service Coverage Ratio":
    user_company.ratios.get_debt_service_coverage_ratio(),
    "Interest Coverage Ratio":
    user_company.ratios.get_interest_burden_ratio(),
    "Short Term Coverage Ratio":
    user_company.ratios.get_short_term_coverage_ratio()
}

#searches the ratio table for the number needed

user_ratios = {}

for key, value in user_ratio_list.items():
    searcher = value.loc[ticker].iloc[-1]
    if not np.isnan(searcher) and not np.isinf(searcher):
        user_ratios[key] = searcher
    else:
        searcher = 0
        user_ratios[key] = searcher


print("\n\n")

for key, value in user_ratios.items():
    print(f"{company_full_name}({ticker}) {key}: {round(value,2)}")

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


if user_stock.info['sector'] == "Financial Services":
    fin_total_score = 0
    fin_stats = fin.fin_stats(ticker)
    fin_industry_averages = fin_stats["fin_industry_averages"]
    fin_industry_std = fin_stats["fin_industry_std"]
    fin_weights = fin_stats["fin_weights"]
    fin_preferences = fin_stats["fin_preferences"]
    fin_company = fin_stats["fin_company"]
    fin_pitroski_score = fin_stats["fin_pitroski_score"]


    #print(user_company.models.get_piotroski_score())
    #print(user_company.models.get_altman_z_score())
    print("Here are some other relevant metrics you may wish to use:")
    print("\n\n")
    user_pitroski_score = user_company.models.get_piotroski_score(
        ).loc[ticker].iloc[9, -1]

    print(f"Protoski Score for {ticker}: {user_pitroski_score}")
    print(f"Protoski Score for the {user_stock.info['sector']} sector {fin_pitroski_score}")
    print(f"A Protoski score below 2 is considered a low value stock. A score above 8 is considered a good value stock. Scores range for 1 to 9")

    print("\n\n")


    for ratio in user_ratios:
        if fin_industry_std[ratio] == 0:
            fin_industry_std[ratio] = 1

        z_score = (user_ratios[ratio] -
                   fin_industry_averages[ratio]) / fin_industry_std[ratio]
        fin_ratio_weight = fin_weights.get(ratio)

        preference = fin_preferences.get(ratio)

        if preference == "lower":
             z_score = -z_score
        else:
             z_score = z_score
        transformed_z_score = sigmoid(z_score)
        weighted_score = transformed_z_score * fin_weights[ratio]

        print(
            f"Score for {ratio}: {round(weighted_score,2)}/{round(fin_weights[ratio],2)}"
        )

        fin_total_score += float(weighted_score)

    print(
        f"Total Score: {round(fin_total_score,2)} /{sum(fin_weights.values())}"
    )

if user_stock.info['sector'] == "Technology":

    tech_total_score = 0
    tech_stats = tech.tech_stats(ticker)
    tech_industry_averages = tech_stats["tech_industry_averages"]
    tech_industry_std = tech_stats["tech_industry_std"]
    tech_weights = tech_stats["tech_weights"]
    tech_preferences = tech_stats["tech_preferences"]
    tech_company = tech_stats["tech_company"]
    tech_pitroski_score = tech_stats["tech_pitroski_score"]


    #print(user_company.models.get_piotroski_score())
    #print(user_company.models.get_altman_z_score())
    print("Here are some other relevant metrics you may wish to use:")
    print("\n\n")
    user_pitroski_score = user_company.models.get_piotroski_score(
        ).loc[ticker].iloc[9, -1]

    print(f"Protoski Score for {ticker}: {user_pitroski_score}")
    print(f"Protoski Score for the {user_stock.info['sector']} sector {tech_pitroski_score}")
    print(f"A Protoski score below 2 is considered a low value stock. A score above 8 is considered a good value stock. Scores range for 1 to 9")

    print("\n\n")

    user_altman_z_score = user_company.models.get_altman_z_score(
    ).loc[ticker].iloc[5, -1]

    print(f"Altman Z-score: {user_altman_z_score}")

    print("Please Note the Altman Z-Score has an accuracy of 82% to 94% ")
    if user_altman_z_score < 3 and user_altman_z_score > 1.8:
        print("Score is in gray area: moderate chance of bankruptcy")
    elif user_altman_z_score > 3:
        print("Score is in safe zone: bankruptcy is unlikely")
    elif user_altman_z_score < 1.8:
        print(
            f"Score is in danger zone: bankruptcy likely, closer to zero indicates greater chance of bankruptcy.")

    print("\n\n")

    for ratio in user_ratios:
        if tech_industry_std[ratio] == 0:
            tech_industry_std[ratio] = 1

        z_score = (user_ratios[ratio] -
                   tech_industry_averages[ratio]) / tech_industry_std[ratio]
        tech_ratio_weight = tech_weights.get(ratio)

        preference = tech_preferences.get(ratio)

        if preference == "lower":
            z_score = -z_score
        else:
            z_score = z_score
        transformed_z_score = sigmoid(z_score)
        
        weighted_score = transformed_z_score * tech_weights[ratio]

        print(
            f"Score for {ratio}: {round(weighted_score,2)}/{round(tech_weights[ratio],2)}"
        )

        tech_total_score += float(weighted_score)

    print(
        f"Total Score: {round(tech_total_score,2)} /{sum(tech_weights.values())}"
    )





if user_stock.info['sector'] == "Consumer Cyclical":

    consume_cyc_total_score = 0
    consume_cyc_stats = consume_cyc.consume_cyc_stats(ticker)
    consume_cyc_industry_averages = consume_cyc_stats["consume_cyc_industry_averages"]
    consume_cyc_industry_std = consume_cyc_stats["consume_cyc_industry_std"]
    consume_cyc_weights = consume_cyc_stats["consume_cyc_weights"]
    consume_cyc_preferences = consume_cyc_stats["consume_cyc_preferences"]
    consume_cyc_company = consume_cyc_stats["consume_cyc_company"]
    consume_cyc_pitroski_score = consume_cyc_stats["consume_cyc_pitroski_score"]


    #print(user_company.models.get_piotroski_score())
    #print(user_company.models.get_altman_z_score())
    print("Here are some other relevant metrics you may wish to use:")
    print("\n\n")
    user_pitroski_score = user_company.models.get_piotroski_score(
        ).loc[ticker].iloc[9, -1]

    print(f"Protoski Score for {ticker}: {user_pitroski_score}")
    print(f"Protoski Score for the {user_stock.info['sector']} sector {consume_cyc_pitroski_score}")
    print(f"A Protoski score below 2 is considered a low value stock. A score above 8 is considered a good value stock. Scores range for 1 to 9")

    print("\n\n")

    user_altman_z_score = user_company.models.get_altman_z_score(
    ).loc[ticker].iloc[5, -1]

    print(f"Altman Z-score: {user_altman_z_score}")

    print("Please Note the Altman Z-Score has an accuracy of 82% to 94% ")
    if user_altman_z_score < 3 and user_altman_z_score > 1.8:
        print("Score is in gray area: moderate chance of bankruptcy")
    elif user_altman_z_score > 3:
        print("Score is in safe zone: bankruptcy is unlikely")
    elif user_altman_z_score < 1.8:
        print(
            f"Score is in danger zone: bankruptcy likely, closer to zero indicates greater chance of bankruptcy.")

    print("\n\n")
    for ratio in user_ratios:
        if consume_cyc_industry_std[ratio] == 0:
            consume_cyc_industry_std[ratio] = 1

        z_score = (user_ratios[ratio] -
                   consume_cyc_industry_averages[ratio]) / consume_cyc_industry_std[ratio]
        consume_cyc_ratio_weight = consume_cyc_weights.get(ratio)

        preference = consume_cyc_preferences.get(ratio)

        if preference == "lower":
             z_score = -z_score
        else:
             z_score = z_score
        transformed_z_score = sigmoid(z_score)
        weighted_score = transformed_z_score * consume_cyc_weights[ratio]

        print(
            f"Score for {ratio}: {round(weighted_score,2)}/{round(consume_cyc_weights[ratio],2)}"
        )

        consume_cyc_total_score += float(weighted_score)

    print(
        f"Total Score: {round(consume_cyc_total_score,2)} /{sum(consume_cyc_weights.values())}"
    )





if user_stock.info['sector'] == "Healthcare":

    health_total_score = 0
    health_stats = health.health_stats(ticker)
    health_industry_averages = health_stats["health_industry_averages"]
    health_industry_std = health_stats["health_industry_std"]
    health_weights = health_stats["health_weights"]
    health_preferences = health_stats["health_preferences"]
    health_company = health_stats["health_company"]
    health_pitroski_score = health_stats["health_pitroski_score"]


    #print(user_company.models.get_piotroski_score())
    #print(user_company.models.get_altman_z_score())
    print("Here are some other relevant metrics you may wish to use:")
    print("\n\n")
    user_pitroski_score = user_company.models.get_piotroski_score(
        ).loc[ticker].iloc[9, -1]

    print(f"Protoski Score for {ticker}: {user_pitroski_score}")
    print(f"Protoski Score for the {user_stock.info['sector']} sector {health_pitroski_score}")
    print(f"A Protoski score below 2 is considered a low value stock. A score above 8 is considered a good value stock. Scores range for 1 to 9")

    print("\n\n")

    user_altman_z_score = user_company.models.get_altman_z_score(
    ).loc[ticker].iloc[5, -1]

    print(f"Altman Z-score: {user_altman_z_score}")

    print("Please Note the Altman Z-Score has an accuracy of 82% to 94% ")
    if user_altman_z_score < 3 and user_altman_z_score > 1.8:
        print("Score is in gray area: moderate chance of bankruptcy")
    elif user_altman_z_score > 3:
        print("Score is in safe zone: bankruptcy is unlikely")
    elif user_altman_z_score < 1.8:
        print(
            f"Score is in danger zone: bankruptcy likely, closer to zero indicates greater chance of bankruptcy.")

    print("\n\n")
    for ratio in user_ratios:
        if health_industry_std[ratio] == 0:
            health_industry_std[ratio] = 1

        z_score = (user_ratios[ratio] -
                   health_industry_averages[ratio]) / health_industry_std[ratio]
        health_ratio_weight = health_weights.get(ratio)

        preference = health_preferences.get(ratio)

        if preference == "lower":
             z_score = -z_score
        else:
             z_score = z_score
        transformed_z_score = sigmoid(z_score)
        weighted_score = transformed_z_score * health_weights[ratio]

        print(
            f"Score for {ratio}: {round(weighted_score,2)}/{round(health_weights[ratio],2)}"
        )

        health_total_score += float(weighted_score)

    print(
        f"Total Score: {round(health_total_score,2)} /{sum(health_weights.values())}"
    )





if user_stock.info['sector'] == "Communication Services":

    com_serv_total_score = 0
    com_serv_stats = com_serv.com_serv_stats(ticker)
    com_serv_industry_averages = com_serv_stats["com_serv_industry_averages"]
    com_serv_industry_std = com_serv_stats["com_serv_industry_std"]
    com_serv_weights = com_serv_stats["com_serv_weights"]
    com_serv_preferences = com_serv_stats["com_serv_preferences"]
    com_serv_company = com_serv_stats["com_serv_company"]
    com_serv_pitroski_score = com_serv_stats["com_serv_pitroski_score"]


    #print(user_company.models.get_piotroski_score())
    #print(user_company.models.get_altman_z_score())
    print("Here are some other relevant metrics you may wish to use:")
    print("\n\n")
    user_pitroski_score = user_company.models.get_piotroski_score(
        ).loc[ticker].iloc[9, -1]

    print(f"Protoski Score for {ticker}: {user_pitroski_score}")
    print(f"Protoski Score for the {user_stock.info['sector']} sector {com_serv_pitroski_score}")
    print(f"A Protoski score below 2 is considered a low value stock. A score above 8 is considered a good value stock. Scores range for 1 to 9")

    print("\n\n")

    user_altman_z_score = user_company.models.get_altman_z_score(
    ).loc[ticker].iloc[5, -1]

    print(f"Altman Z-score: {user_altman_z_score}")

    print("Please Note the Altman Z-Score has an accuracy of 82% to 94% ")
    if user_altman_z_score < 3 and user_altman_z_score > 1.8:
        print("Score is in gray area: moderate chance of bankruptcy")
    elif user_altman_z_score > 3:
        print("Score is in safe zone: bankruptcy is unlikely")
    elif user_altman_z_score < 1.8:
        print(
            f"Score is in danger zone: bankruptcy likely, closer to zero indicates greater chance of bankruptcy.")

    print("\n\n")
    for ratio in user_ratios:
        if com_serv_industry_std[ratio] == 0:
            com_serv_industry_std[ratio] = 1

        z_score = (user_ratios[ratio] -
                   com_serv_industry_averages[ratio]) / com_serv_industry_std[ratio]
        com_serv_ratio_weight = com_serv_weights.get(ratio)

        preference = com_serv_preferences.get(ratio)

        if preference == "lower":
             z_score = -z_score
        else:
             z_score = z_score
        transformed_z_score = sigmoid(z_score)
        weighted_score = transformed_z_score * com_serv_weights[ratio]

        print(
            f"Score for {ratio}: {round(weighted_score,2)}/{round(com_serv_weights[ratio],2)}"
        )

        com_serv_total_score += float(weighted_score)

    print(
        f"Total Score: {round(com_serv_total_score,2)} /{sum(com_serv_weights.values())}"
    )




if user_stock.info['sector'] == "Industrials":
        indus_total_score = 0
        indus_stats = indus.indus_stats(ticker)
        indus_industry_averages = indus_stats["indus_industry_averages"]
        indus_industry_std = indus_stats["indus_industry_std"]
        indus_weights = indus_stats["indus_weights"]
        indus_preferences = indus_stats["indus_preferences"]
        indus_company = indus_stats["indus_company"]
        indus_pitroski_score = indus_stats["indus_pitroski_score"]


        #print(user_company.models.get_piotroski_score())
        #print(user_company.models.get_altman_z_score())
        print("Here are some other relevant metrics you may wish to use:")
        print("\n\n")
        user_pitroski_score = user_company.models.get_piotroski_score(
            ).loc[ticker].iloc[9, -1]

        print(f"Protoski Score for {ticker}: {user_pitroski_score}")
        print(f"Protoski Score for the {user_stock.info['sector']} sector {indus_pitroski_score}")
        print(f"A Protoski score below 2 is considered a low value stock. A score above 8 is considered a good value stock. Scores range for 1 to 9")

        print("\n\n")

        user_altman_z_score = user_company.models.get_altman_z_score(
        ).loc[ticker].iloc[5, -1]

        print(f"Altman Z-score: {user_altman_z_score}")

        print("Please Note the Altman Z-Score has an accuracy of 82% to 94% ")
        if user_altman_z_score < 3 and user_altman_z_score > 1.8:
            print("Score is in gray area: moderate chance of bankruptcy")
        elif user_altman_z_score > 3:
            print("Score is in safe zone: bankruptcy is unlikely")
        elif user_altman_z_score < 1.8:
            print(
                f"Score is in danger zone: bankruptcy likely, closer to zero indicates greater chance of bankruptcy.")

        print("\n\n")
        for ratio in user_ratios:
            if indus_industry_std[ratio] == 0:
                indus_industry_std[ratio] = 1

            z_score = (user_ratios[ratio] -
                       indus_industry_averages[ratio]) / indus_industry_std[ratio]
            indus_ratio_weight = indus_weights.get(ratio)

            preference = indus_preferences.get(ratio)

            if preference == "lower":
                 z_score = -z_score
            else:
                 z_score = z_score
            transformed_z_score = sigmoid(z_score)
            weighted_score = transformed_z_score * indus_weights[ratio]

            print(
                f"Score for {ratio}: {round(weighted_score,2)}/{round(indus_weights[ratio],2)}"
            )

            indus_total_score += float(weighted_score)

        print(
            f"Total Score: {round(indus_total_score,2)} /{sum(indus_weights.values())}"
        )




if user_stock.info['sector'] == "Consumer Defensive":
    consume_def_total_score = 0
    consume_def_stats = consume_def.consume_def_stats(ticker)
    consume_def_industry_averages = consume_def_stats["consume_def_industry_averages"]
    consume_def_industry_std = consume_def_stats["consume_def_industry_std"]
    consume_def_weights = consume_def_stats["consume_def_weights"]
    consume_def_preferences = consume_def_stats["consume_def_preferences"]
    consume_def_company = consume_def_stats["consume_def_company"]
    consume_def_pitroski_score = consume_def_stats["consume_def_pitroski_score"]


    #print(user_company.models.get_piotroski_score())
    #print(user_company.models.get_altman_z_score())
    print("Here are some other relevant metrics you may wish to use:")
    print("\n\n")
    user_pitroski_score = user_company.models.get_piotroski_score(
        ).loc[ticker].iloc[9, -1]

    print(f"Protoski Score for {ticker}: {user_pitroski_score}")
    print(f"Protoski Score for the {user_stock.info['sector']} sector {consume_def_pitroski_score}")
    print(f"A Protoski score below 2 is considered a low value stock. A score above 8 is considered a good value stock. Scores range for 1 to 9")

    print("\n\n")

    user_altman_z_score = user_company.models.get_altman_z_score(
    ).loc[ticker].iloc[5, -1]

    print(f"Altman Z-score: {user_altman_z_score}")

    print("Please Note the Altman Z-Score has an accuracy of 82% to 94% ")
    if user_altman_z_score < 3 and user_altman_z_score > 1.8:
        print("Score is in gray area: moderate chance of bankruptcy")
    elif user_altman_z_score > 3:
        print("Score is in safe zone: bankruptcy is unlikely")
    elif user_altman_z_score < 1.8:
        print(
            f"Score is in danger zone: bankruptcy likely, closer to zero indicates greater chance of bankruptcy.")

    print("\n\n")

    for ratio in user_ratios:
        if consume_def_industry_std[ratio] == 0:
            consume_def_industry_std[ratio] = 1

        z_score = (user_ratios[ratio] -
                   consume_def_industry_averages[ratio]) / consume_def_industry_std[ratio]
        consume_def_ratio_weight = consume_def_weights.get(ratio)

        preference = consume_def_preferences.get(ratio)

        if preference == "lower":
             z_score = -z_score
        else:
             z_score = z_score
        transformed_z_score = sigmoid(z_score)
        weighted_score = transformed_z_score * consume_def_weights[ratio]

        print(
            f"Score for {ratio}: {round(weighted_score,2)}/{round(consume_def_weights[ratio],2)}"
        )

        consume_def_total_score += float(weighted_score)

    print(
        f"Total Score: {round(consume_def_total_score,2)} /{sum(consume_def_weights.values())}"
    )







if user_stock.info['sector'] == "Energy":
    energy_total_score = 0
    energy_stats = energy.energy_stats(ticker)
    energy_industry_averages = energy_stats["energy_industry_averages"]
    energy_industry_std = energy_stats["energy_industry_std"]
    energy_weights = energy_stats["energy_weights"]
    energy_preferences = energy_stats["energy_preferences"]
    energy_company = energy_stats["energy_company"]
    energy_pitroski_score = energy_stats["energy_pitroski_score"]


    #print(user_company.models.get_piotroski_score())
    #print(user_company.models.get_altman_z_score())
    print("Here are some other relevant metrics you may wish to use:")
    print("\n\n")
    user_pitroski_score = user_company.models.get_piotroski_score(
        ).loc[ticker].iloc[9, -1]

    print(f"Protoski Score for {ticker}: {user_pitroski_score}")
    print(f"Protoski Score for the {user_stock.info['sector']} sector {energy_pitroski_score}")
    print(f"A Protoski score below 2 is considered a low value stock. A score above 8 is considered a good value stock. Scores range for 1 to 9")

    print("\n\n")

    user_altman_z_score = user_company.models.get_altman_z_score(
    ).loc[ticker].iloc[5, -1]

    print(f"Altman Z-score: {user_altman_z_score}")

    print("Please Note the Altman Z-Score has an accuracy of 82% to 94% ")
    if user_altman_z_score < 3 and user_altman_z_score > 1.8:
        print("Score is in gray area: moderate chance of bankruptcy")
    elif user_altman_z_score > 3:
        print("Score is in safe zone: bankruptcy is unlikely")
    elif user_altman_z_score < 1.8:
        print(
            f"Score is in danger zone: bankruptcy likely, closer to zero indicates greater chance of bankruptcy.")


    print("\n\n")

    for ratio in user_ratios:
        if energy_industry_std[ratio] == 0:
            energy_industry_std[ratio] = 1

        z_score = (user_ratios[ratio] -
                   energy_industry_averages[ratio]) / energy_industry_std[ratio]
        energy_ratio_weight = energy_weights.get(ratio)

        preference = energy_preferences.get(ratio)

        if preference == "lower":
             z_score = -z_score
        else:
             z_score = z_score
        transformed_z_score = sigmoid(z_score)
        weighted_score = transformed_z_score * energy_weights[ratio]

        print(
            f"Score for {ratio}: {round(weighted_score,2)}/{round(energy_weights[ratio],2)}"
        )

        energy_total_score += float(weighted_score)

    print(
        f"Total Score: {round(energy_total_score,2)} /{sum(energy_weights.values())}"
    )



if user_stock.info['sector'] == "Basic Materials":
        basic_mats_total_score = 0
        basic_mats_stats = basic_mats.basic_mats_stats(ticker)
        basic_mats_industry_averages = basic_mats_stats["basic_mats_industry_averages"]
        basic_mats_industry_std = basic_mats_stats["basic_mats_industry_std"]
        basic_mats_weights = basic_mats_stats["basic_mats_weights"]
        basic_mats_preferences = basic_mats_stats["basic_mats_preferences"]
        basic_mats_company = basic_mats_stats["basic_mats_company"]
        basic_mats_pitroski_score = basic_mats_stats["basic_mats_pitroski_score"]


        #print(user_company.models.get_piotroski_score())
        #print(user_company.models.get_altman_z_score())
        print("Here are some other relevant metrics you may wish to use:")
        print("\n\n")
        user_pitroski_score = user_company.models.get_piotroski_score(
            ).loc[ticker].iloc[9, -1]

        print(f"Protoski Score for {ticker}: {user_pitroski_score}")
        print(f"Protoski Score for the {user_stock.info['sector']} sector {basic_mats_pitroski_score}")
        print(f"A Protoski score below 2 is considered a low value stock. A score above 8 is considered a good value stock. Scores range for 1 to 9")

        print("\n\n")

        user_altman_z_score = user_company.models.get_altman_z_score(
        ).loc[ticker].iloc[5, -1]

        print(f"Altman Z-score: {user_altman_z_score}")

        print("Please Note the Altman Z-Score has an accuracy of 82% to 94% ")
        if user_altman_z_score < 3 and user_altman_z_score > 1.8:
            print("Score is in gray area: moderate chance of bankruptcy")
        elif user_altman_z_score > 3:
            print("Score is in safe zone: bankruptcy is unlikely")
        elif user_altman_z_score < 1.8:
            print(
                f"Score is in danger zone: bankruptcy likely, closer to zero indicates greater chance of bankruptcy.")


        print("\n\n")

        for ratio in user_ratios:
            if basic_mats_industry_std[ratio] == 0:
                basic_mats_industry_std[ratio] = 1

            z_score = (user_ratios[ratio] -
                       basic_mats_industry_averages[ratio]) / basic_mats_industry_std[ratio]
            basic_mats_ratio_weight = basic_mats_weights.get(ratio)

            preference = basic_mats_preferences.get(ratio)

            if preference == "lower":
                 z_score = -z_score
            else:
                 z_score = z_score
            transformed_z_score = sigmoid(z_score)
            weighted_score = transformed_z_score * basic_mats_weights[ratio]

            print(
                f"Score for {ratio}: {round(weighted_score,2)}/{round(basic_mats_weights[ratio],2)}"
            )

            basic_mats_total_score += float(weighted_score)

        print(
            f"Total Score: {round(basic_mats_total_score,2)} /{sum(basic_mats_weights.values())}"
        )



if user_stock.info['sector'] == "Real Estate":
        real_est_total_score = 0
        real_est_stats = real_est.real_est_stats(ticker)
        real_est_industry_averages = real_est_stats["real_est_industry_averages"]
        real_est_industry_std = real_est_stats["real_est_industry_std"]
        real_est_weights = real_est_stats["real_est_weights"]
        real_est_preferences = real_est_stats["real_est_preferences"]
        real_est_company = real_est_stats["real_est_company"]
        real_est_pitroski_score = real_est_stats["real_est_pitroski_score"]


        #print(user_company.models.get_piotroski_score())
        #print(user_company.models.get_altman_z_score())
        print("Here are some other relevant metrics you may wish to use:")
        print("\n\n")
        user_pitroski_score = user_company.models.get_piotroski_score(
            ).loc[ticker].iloc[9, -1]

        print(f"Protoski Score for {ticker}: {user_pitroski_score}")
        print(f"Protoski Score for the {user_stock.info['sector']} sector {real_est_pitroski_score}")
        print(f"A Protoski score below 2 is considered a low value stock. A score above 8 is considered a good value stock. Scores range for 1 to 9")

        print("\n\n")

        user_altman_z_score = user_company.models.get_altman_z_score(
        ).loc[ticker].iloc[5, -1]

        print(f"Altman Z-score: {user_altman_z_score}")

        print("Please Note the Altman Z-Score has an accuracy of 82% to 94% ")
        if user_altman_z_score < 3 and user_altman_z_score > 1.8:
            print("Score is in gray area: moderate chance of bankruptcy")
        elif user_altman_z_score > 3:
            print("Score is in safe zone: bankruptcy is unlikely")
        elif user_altman_z_score < 1.8:
            print(
                f"Score is in danger zone: bankruptcy likely, closer to zero indicates greater chance of bankruptcy.")

        print("\n\n")

        for ratio in user_ratios:
            if real_est_industry_std[ratio] == 0:
                real_est_industry_std[ratio] = 1

            z_score = (user_ratios[ratio] -
                       real_est_industry_averages[ratio]) / real_est_industry_std[ratio]
            real_est_ratio_weight = real_est_weights.get(ratio)

            preference = real_est_preferences.get(ratio)

            if preference == "lower":
                 z_score = -z_score
            else:
                 z_score = z_score
            transformed_z_score = sigmoid(z_score)
            weighted_score = transformed_z_score * real_est_weights[ratio]

            print(
                f"Score for {ratio}: {round(weighted_score,2)}/{round(real_est_weights[ratio],2)}"
            )

            real_est_total_score += float(weighted_score)

        print(
            f"Total Score: {round(real_est_total_score,2)} /{sum(real_est_weights.values())}"
        )







if user_stock.info['sector'] == "Utilities":
    util_total_score = 0
    util_stats = util.util_stats(ticker)
    util_industry_averages = util_stats["util_industry_averages"]
    util_industry_std = util_stats["util_industry_std"]
    util_weights = util_stats["util_weights"]
    util_preferences = util_stats["util_preferences"]
    util_company = util_stats["util_company"]
    util_pitroski_score = util_stats["util_pitroski_score"]


    #print(user_company.models.get_piotroski_score())
    #print(user_company.models.get_altman_z_score())
    print("Here are some other relevant metrics you may wish to use:")
    print("\n\n")
    user_pitroski_score = user_company.models.get_piotroski_score(
        ).loc[ticker].iloc[9, -1]

    print(f"Protoski Score for {ticker}: {user_pitroski_score}")
    print(f"Protoski Score for the {user_stock.info['sector']} sector {util_pitroski_score}")
    print(f"A Protoski score below 2 is considered a low value stock. A score above 8 is considered a good value stock. Scores range for 1 to 9")

    print("\n\n")

    user_altman_z_score = user_company.models.get_altman_z_score(
    ).loc[ticker].iloc[5, -1]

    print(f"Altman Z-score: {user_altman_z_score}")

    print("Please Note the Altman Z-Score has an accuracy of 82% to 94% ")
    if user_altman_z_score < 3 and user_altman_z_score > 1.8:
        print("Score is in gray area: moderate chance of bankruptcy")
    elif user_altman_z_score > 3:
        print("Score is in safe zone: bankruptcy is unlikely")
    elif user_altman_z_score < 1.8:
        print(
            f"Score is in danger zone: bankruptcy likely, closer to zero indicates greater chance of bankruptcy.")

    print("\n\n")

    for ratio in user_ratios:
        if util_industry_std[ratio] == 0:
            util_industry_std[ratio] = 1

        z_score = (user_ratios[ratio] -
                   util_industry_averages[ratio]) / util_industry_std[ratio]
        util_ratio_weight = util_weights.get(ratio)

        preference = util_preferences.get(ratio)

        if preference == "lower":
             z_score = -z_score
        else:
             z_score = z_score
        transformed_z_score = sigmoid(z_score)
        weighted_score = transformed_z_score * util_weights[ratio]

        print(
            f"Score for {ratio}: {round(weighted_score,2)}/{round(util_weights[ratio],2)}"
        )

        util_total_score += float(weighted_score)

    print(
        f"Total Score: {round(util_total_score,2)} /{sum(util_weights.values())}"
    )





