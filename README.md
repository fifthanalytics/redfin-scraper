# Redfin Scraper

## Run the Flask App locally

Opens up /api/data/ route when run. Send a request with a list of ZIP codes and receive a json of all the homes for sale in that ZIP code. Details include address, sale price, currency, beds, baths, sq ft, link to Redfin listing. 

To run the flask app: 

```
source venv/bin/activate
python3 app.py
```

## Run without Flask 

Edit the `main.py` and create a `listingDetail` object. Example: 

```
from listingDetail import listingDetails

listing_detail = listingDetail('12345')
listing_detail.get_detail()
```

Response will be a JSON object with all homes for sale in the 12345 ZIP code. 

## To Do

- Put in Docker container, push to DockerHub. 
- Test in GCP/AWS. 
- Develop individual home links. Search by address? 
