# Redfin Scraper (Flask App)

Opens up /api/data/ route when run. Send a request with a list of ZIP codes and receive a json of all the homes for sale in that ZIP code. Details include address, sale price, currency, beds, baths, sq ft, link to Redfin listing. 

To run the flask app: 

```
source venv/bin/activate
python3 app.py
```
# To Do

- Put in Docker container, push to DockerHub. 
- Test in GPS/AWS. 
- Develop individual home links. Search by address? 
