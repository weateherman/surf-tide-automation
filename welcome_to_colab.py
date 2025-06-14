# -*- coding: utf-8 -*-
"""Welcome To Colab

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/notebooks/intro.ipynb
"""

pip install requests pandas openpyxl

import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_noaa_tides():
    today = datetime.now()
    begin_date = today.strftime("%Y%m%d")
    end_date = (today + timedelta(days=1)).strftime("%Y%m%d")

    url = (
        "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
        "?product=predictions"
        f"&begin_date={begin_date}"
        f"&end_date={end_date}"
        "&datum=MLLW"
        "&station=8419318"
        "&time_zone=lst_ldt"
        "&units=english"
        "&interval=hilo"
        "&format=json"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('predictions', [])
    except Exception as e:
        print(f"Error fetching NOAA tides: {e}")
        return []

def fetch_dummy_surf_data():
    # Placeholder: Replace with real API calls or scraping if available
    return {
        'Wave Height (ft)': 3.5,
        'Wave Power': 'Moderate',
        'Wind Direction': 'NW',
        'Wind Speed (mph)': 12,
        'Water Temp (°F)': 58,
    }

def main():
    tides = fetch_noaa_tides()
    surf = fetch_dummy_surf_data()

    # Prepare tides DataFrame
    tide_df = pd.DataFrame(tides)
    if not tide_df.empty:
        tide_df['t'] = pd.to_datetime(tide_df['t'])
        tide_df = tide_df.rename(columns={'t': 'Time', 'v': 'Height (ft)', 'type': 'High/Low'})

    # Prepare surf DataFrame
    surf_df = pd.DataFrame([{
        'Date': datetime.now().strftime("%Y-%m-%d"),
        **surf
    }])

    # Save to Excel file with two sheets
    excel_filename = 'Old_Orchard_Beach_Surf_Tide_Data.xlsx'
    with pd.ExcelWriter(excel_filename) as writer:
        surf_df.to_excel(writer, sheet_name='Surf Data', index=False)
        tide_df.to_excel(writer, sheet_name='Tide Predictions', index=False)

    print(f"Excel file created: {excel_filename}")

if __name__ == "__main__":
    main()

!python surf_tide.py