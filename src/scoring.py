#!/usr/bin/env python3

import os
import sys
import pandas as pd
import numpy as np
import math


ROOT = os.path.abspath(os.path.dirname(os.path.join(__file__, "../../")))

def path_check(path_name: str) -> bool:
    if not os.path.exists(path_name):
        print(f"Error; couldn't find {path_name = }\n")
        return False
    return True


def parse_culm_gas_emissions() -> pd.DataFrame:
    """
    col_headers = ["Year", "CO2 RF (W/m^2)", "CO2 kWh", "CO2 Aggregate warming", \
                "CH4 RF (W/m^2)", "CH4 kWh", "CH4 Aggregate warming", \
                "N2O RF (W/m^2)", "N2O kWh", "N2O Aggregate warming"]
    """
    data_historical = os.path.join(ROOT,
        "data/emissions_data/Radiative_Efficiency_Over_100_Y.csv")
    path_check(data_historical)
    df = pd.read_csv(data_historical)

    # drop columns that don't have top row headers
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # drop any incomplete rows
    df = df.dropna()

    # col_headers = df.columns
    # print(df.columns)
    df.describe()
    df.info()

    print(df.tail(5))

    out_dir = os.path.join(ROOT, "out")
    os.makedirs(out_dir, exist_ok=True)
    radiative_clean_csv = os.path.join(out_dir, "Radiative_Efficiency_100Y.csv")
    df.to_csv(radiative_clean_csv)
    print(f"{radiative_clean_csv = }")

    return df


def calc_climate_score(
        df_emissions: pd.DataFrame,
        year_company_added_to_sp500=1988
    ) -> float:
    """
    inputs:
        dataframe with aggregate emissions for last 100 years (in tons)
        CO2 carbon dioxide
        CH4 methane
        N2O nitrous oxide
    output:
        climate risk score
    """

    """
    calculate the non-worn off global warming that is resultant of the company

    Radiative Forcing
        510.1km^2 = surface area of the earth
        = 510.1 * 1E6 for m^2
        510.1km^2 * 10E12 Watts for TeraWatts

    For each W/m^2, there is a 510E12 W increase in heat rate level
    """
    surface_area_earth_m_sq = 510.1 * 1E12
    past_emissions_carb_diox = 0.0
    years_til_1pct_thresh = 4610

    latest_year = df_emissions["Year"].iloc[0].astype(int) # 2023
    # print(latest_year, type(latest_year))
    idx = 0
    for curr_year in range(int(latest_year), year_company_added_to_sp500 + 1, -1):
        # year_company_added_to_sp500, int(latest_year) + 1):

        rf_co2_year = df_emissions.iloc[idx]["CO2 RF (W/m^2)"]

        year_carb_diox_rf = rf_co2_year * surface_area_earth_m_sq * \
            0.001 * 24 * 365.25
        print(f"year {curr_year} warming {year_carb_diox_rf}")
        past_emissions_carb_diox += year_carb_diox_rf
        print(f"aggregate warming so far: {past_emissions_carb_diox}")
        idx += 1

    print(f"\nwarming from {past_emissions_carb_diox = }\n")

    # FUTURE CALCS til 4610 years of warming
    # extrapolate to future, til 1% threshold is hit
    future_warming_carb_diox = 0.0
    alpha = 5.35 # W/m^2
    conc_ppm = 280 # 284
    conc_ref = 280 # ppm
    r = 0.0057 # growth rate

    for year in range(years_til_1pct_thresh):

        t = year
        # FIXME: co2 conc function C(t) = C_0(t) * e^(rt)
        conc_ppm = conc_ppm * math.exp(r * t)

        rf = alpha * math.log(conc_ppm / conc_ref)

        # future_warming_carb_diox += rf

        year_carb_diox_rf = rf * surface_area_earth_m_sq * 0.001 * 24 * 365.25
        future_warming_carb_diox += year_carb_diox_rf


    # print(f"{future_warming_carb_diox = }\n")

    return past_emissions_carb_diox
    # return past_emissions_carb_diox + future_warming_carb_diox


if __name__ == "__main__":

    df_emissions = parse_culm_gas_emissions()

    calc_climate_score(df_emissions)



""" Radioactive Force Decay (TWh)
       CO2
US    2.37E+10
MSFT  1.91E+07
GOOG  7.52E+10
"""