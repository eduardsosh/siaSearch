import os
import requests
from tqdm import tqdm
from loader.load_reports import load_reports
from loader.load_balance import load_balance
from loader.load_business import load_business

BUSINESSES = 'https://data.gov.lv/dati/lv/datastore/dump/25e80bf3-f107-4ab4-89ef-251b5b9374e9?bom=True'
BALANCE =    'https://data.gov.lv/dati/lv/datastore/dump/d5fd17ef-d32e-40cb-8399-82b780095af0?bom=True'
REPORTS =    'https://data.gov.lv/dati/lv/datastore/dump/27fcc5ec-c63b-4bfd-bb08-01f073a52d04?bom=True'

def download_file(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024

    with open(filename, 'wb') as file:
        with tqdm(total=total_size_in_bytes, unit='B', unit_scale=True, desc=filename) as progress_bar:
            for data in response.iter_content(block_size):
                file.write(data)
                progress_bar.update(len(data))


if __name__ == "__main__":
    print("Setting up project ...")
    os.makedirs('datasets', exist_ok=True)
    
    files = {
    'uznemumi.csv': BUSINESSES,
    'profit_loss.csv': BALANCE,
    'report_data.csv': REPORTS
    }   

    print(f"Downloading csv files form data gov")
    for out_filename, file_url in files.items():
        output_filename = os.path.join('datasets', out_filename)
        download_file(file_url, output_filename)
        
    print("Inserting data into database")
    load_reports()
    load_balance()
    load_business()
    print("Done! Use other scripts to query data and show results!")
    
    