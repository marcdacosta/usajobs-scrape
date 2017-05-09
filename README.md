# USAJOBS scraper

USAJOBS is the centralized job posting site for the US government. While it appears that at some point there was a fully functioning REST API (https://developer.usajobs.gov/) it currently appears to be no longer supported.

This scraper takes a search query and saves all job listings to a JSON file. By default, it scrapes the every 12 hours.

You can define an `on_job` callback that is fired whenever a new job listing is detected for the query. This can, for instance, post it to Twitter.

## Usage

    python scrape.py