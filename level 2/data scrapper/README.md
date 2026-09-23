# Python Web Data Scraper — Books to Scrape

A beginner-friendly Python project that scrapes book data from the public
practice website [books.toscrape.com](https://books.toscrape.com/) and
saves it into a CSV file.

## What It Does

`data_scraper.py` downloads a page of the book catalogue, parses the HTML,
extracts each book's **title**, **price**, **availability**, and **rating**,
and saves everything into `books.csv`.

## Why This Site?

books.toscrape.com is a sandbox built specifically for scraping practice —
its homepage literally says "We love being scraped!". No login or private
data is involved, so it's safe for learning.

## Libraries Used

- `requests` — downloads the webpage's HTML.
- `beautifulsoup4` — parses the HTML and finds the elements we need.
- `csv` (built-in) — writes the extracted data to a CSV file.

## How It Works

1. `fetch_page()` sends an HTTP GET request and returns the raw HTML.
2. `scrape_books()` uses BeautifulSoup to find every
   `<article class="product_pod">` (each book), then pulls out the title,
   price, availability, and star rating from inside it.
3. `save_to_csv()` writes the list of extracted books to `books.csv`
   using Python's built-in `csv` module.
4. `main()` ties it all together and prints how many books were scraped.

## Installation

```bash
cd data-scraper
pip install -r requirements.txt
```

## Run the Scraper

```bash
python data_scraper.py
```

Expected output:

```
Starting scraper for: https://books.toscrape.com/catalogue/page-1.html

Successfully fetched page: https://books.toscrape.com/catalogue/page-1.html (status code: 200)
Data successfully saved to 'books.csv'.

Done! Successfully scraped 20 books.
```

## Output

Results are saved to `books.csv` in the same folder, with columns:
`title, price, availability, rating`.

Example rows:

| title                  | price  | availability | rating |
|------------------------|--------|--------------|--------|
| A Light in the Attic   | £51.77 | In stock     | 3      |
| Tipping the Velvet     | £53.74 | In stock     | 1      |
| Sharp Objects          | £47.82 | In stock     | 4      |

## Error Handling

Handles connection errors, timeouts, bad HTTP status codes, missing HTML
elements, and empty results without crashing.

## Ethical Note

Only a public, scraping-friendly demo page is used here. When scraping
real sites, always check `robots.txt` and the site's terms of service.
