# Scrape and Crawl exercise using SerpAPI and OpenAI
![edos.png](docs%2Fedos.png)
## Prerequisites
  - Docker

## How to run
```shell
docker-compose up -d
```

## How to use
1. Run [src/scrape.py](src/scrape.py) to scrape the first 100 results of a Google search for "web scraping" and save the results in the DB.
2. Query the API to get the results of the scraping.
```shell
curl -X GET --location "http://localhost:5000/segments"
```
3. Review [DDL](db/schema.sql)
   ![schema.png](schema/schema.png)

## How to stop
```shell
docker-compose down
```

## To Do
1. Go through technical debt (TODOs throughout the codebase)
2. Use SQS/Kafka and workers to scale by making the process asynchronous
3. Tweaking the parameters of the Completions API to get better results 
   1. Add Vector Database to store the Completion API results 
   2. Use cheaper GPT-3.5 and compare results
   3. Try with [LangChain](https://anileo.medium.com/building-a-web-scraper-for-scraping-contact-information-from-google-search-a2d9ff53f9ba) and compare results 
   4. Use other models (not OpenAI) and compare results
   5. Try with [Diffbot](https://app.diffbot.com/get-started/) and compare results
4. Add GraphQL API to query more flexibly
5. Add support for robots.txt (or not)
6. Add unit tests 
7. Add more error handling for unexpected data
   1. To OpenAI: validate source of the data (cert), type and length of the data, etc. otherwise could be a costly mistake
   2. From OpenAI: validate the response fields type, data, length, format, etc. before indexing
8. Observability (metrics, logging, tracing, alerting, etc.)
9. Add Selenium/Puppeteer (Docker or as a service) to scrape client-side rendered pages
10. If our API is expected to be heavily used, add caching and consider switching to Django or FastAPI
11. Add support for documents intake using the [Knowledge Retrieval](https://platform.openai.com/docs/assistants/tools/knowledge-retrieval) API
