import pandas as pd
import requests
from datetime import datetime

daterange = pd.bdate_range(datetime(2019,1,1), datetime(2020,1,30))

def download_senate_pdf(date):
    url = f'https://www.congress.gov/116/crec/{single_date.year}/{single_date.month:02d}/{single_date.day:02d}/CREC-{single_date.year}-{single_date.month:02d}-{single_date.day:02d}.pdf'
    r = requests.get(url, allow_redirects=True)
    open(f'transcripts/{date.strftime("%Y-%m-%d")}.pdf', 'wb').write(r.content)
    print(f"downloaded to transcripts/{date.strftime('%Y-%m-%d')}.pdf" )

for single_date in daterange:
    download_senate_pdf(single_date)
