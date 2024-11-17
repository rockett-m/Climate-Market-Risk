#!/usr/bin/env python3

import os
import sys
import pandas as pd


ROOT = os.path.abspath(os.path.dirname(os.path.join(__file__, "../../")))

def path_check(path_name: str) -> bool:
    if not os.path.exists(path_name):
        print(f"Error; couldn't find {path_name = }\n")
        return False
    return True


def calc_climate_score(df_emissions: pd.DataFrame) -> float:
    """
    inputs:
        dataframe with aggregate emissions for last 100 years
        carbon dioxide
        methane
        nitrous oxide
    output:
        climate risk score
    """
    climate_score = 0.0

    return climate_score


def parse_culm_gas_emissions() -> pd.DataFrame:
    """
    col_headers = ["Year", "CO2‚RF (W/m^2)", "CO2 kWh", "CO2 Aggregate warming", \
                "CH4‚RF (W/m^2)", "CH4 kWh", "CH4 Aggregate warming", \
                "NO2‚RF (W/m^2)", "NO2 kWh", "NO2 Aggregate warming"]
    """
    data_historical = os.path.join(ROOT,
        "resources/Radiative_Efficiency_Over_100_Y.csv")
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


if __name__ == "__main__":

    df_emissions = parse_culm_gas_emissions()

    calc_climate_score(df_emissions)
