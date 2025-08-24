from enum import Enum
import pandas as pd
import requests

class Format(Enum):
    Standard = 0
    HalfPPR = 1
    PPR = 2

def get_draft_sharks(format: Format = Format.HalfPPR):
    if format == Format.Standard:
        postfix = ""
    elif format == Format.HalfPPR:
        postfix = "half-ppr"
    elif format == Format.PPR:
        postfix = "ppr"

    endpoint = f"https://www.draftsharks.com/rankings/{postfix}"
    print(f"Fetching data from: {endpoint}")

    try:
        # Check if the URL is accessible
        response = requests.get(endpoint)
        response.raise_for_status()
        print("Successfully accessed the URL.")
    except requests.exceptions.RequestException as e:
        print(f"Error accessing the URL: {e}")
        return

    try:
        # Read the HTML table
        df = pd.read_html(response.text)[0]
        print("Successfully read the HTML table.")
    except ValueError as e:
        print(f"Error reading HTML table: {e}")
        return

    df.columns = df.columns.droplevel(0)

    # Extract number
    df['number'] = df['Positional Rank'].str.extract(r'^(\d+)')

    # Extract team
    df['team'] = df['Positional Rank'].str.extract(r'([A-Z]+)$')

    # Extract name
    df['name'] = df['Positional Rank'].str.extract(r'^\d+([^A-Z]+)')
    df['name'] = df['name'].str.strip()

    print("DataFrame head:")
    print(df.head())

# Example usage
if __name__ == "__main__":
    get_draft_sharks()
