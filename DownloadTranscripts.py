import pandas as pd
import requests
from datetime import datetime

daterange = pd.bdate_range(datetime(2020,1,29), datetime(2020,1,30))

def download_senate_pdf(date):
    try:
        url = f'https://www.congress.gov/116/crec/{single_date.year}/{single_date.month:02d}/{single_date.day:02d}/CREC-{single_date.year}-{single_date.month:02d}-{single_date.day:02d}.pdf'
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()
        open(f'transcripts-pdf/{date.strftime("%Y-%m-%d")}.pdf', 'wb').write(r.content)
        print(f"downloaded to transcripts/{date.strftime('%Y-%m-%d')}.pdf" )
    except requests.HTTPError as e:
        pass

for single_date in daterange:
    download_senate_pdf(single_date)
