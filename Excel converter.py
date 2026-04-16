import pandas as pd
import logging
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def clean_data(df):
    """Clean and normalize data"""
    
    # Handle missing values
    df = df.fillna({
        col: "Unknown" if df[col].dtype == "object" else 0
        for col in df.columns
    })

    # Strip spaces from column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Example: Rename columns
    rename_map = {
        "dob": "date_of_birth",
        "name": "full_name"
    }
    df = df.rename(columns=rename_map)

    # Parse date columns
    for col in df.columns:
        if "date" in col:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            except Exception:
                logging.warning(f"Could not parse date column: {col}")

    return df


def convert_csv_to_excel(input_file, output_file):
    try:
        logging.info(f"Reading CSV file: {input_file}")
        
        df = pd.read_csv(input_file)

        logging.info("Cleaning data...")
        df = clean_data(df)

        logging.info(f"Saving Excel file: {output_file}")
        df.to_excel(output_file, index=False, engine='openpyxl')

        logging.info("Conversion successful!")

    except FileNotFoundError:
        logging.error("Input file not found.")
    except pd.errors.EmptyDataError:
        logging.error("CSV file is empty.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


def main():
    input_file = "demo.csv"
    output_file = "output.xlsx"

    print("Program started...")   # 👈 add this
    convert_csv_to_excel(input_file, output_file)
    print("Program finished!")   # 👈 add this

if __name__ == "__main__":
    main()