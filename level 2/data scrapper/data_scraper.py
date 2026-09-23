"""

data_scraper.py
----------------

A beginner-friendly web scraper that collects book information
(title, price, availability, and rating) from https://books.toscrape.com/
and saves the results into a CSV file named "books.csv".


The website I am using is safe for scraping practice.
This website is a public sandbox specifically built for practicing
web scraping ("We love being scraped!" is written on the homepage),
so it is safe and appropriate for this learning exercise.

Libraries used:
    - requests        : to download the webpage's HTML content
    - bs4 (BeautifulSoup) : to parse and search through the HTML
    - csv (built-in)  : to write the extracted data into a CSV file

"""

import csv
import sys

import requests
from bs4 import BeautifulSoup

# The page I want to scrape. This is page 1 of the book catalogue.
URL = "https://books.toscrape.com/catalogue/page-1.html"

# Output CSV file name.
OUTPUT_FILE = "books.csv"

# A mapping used to convert the word-based star rating class
# (e.g. "Three") into a proper numeric rating (e.g. "3").
RATING_WORDS = {
    "One": "1",
    "Two": "2",
    "Three": "3",
    "Four": "4",
    "Five": "5",
}


def fetch_page(url):
    """
    Send an HTTP GET request to the given URL and return the HTML content.

    Handles connection errors, timeouts, and non-200 status codes so the
    program does not crash unexpectedly.

    Returns:
        str: The HTML content of the page, or None if the request failed.
    """
    try:
        response = requests.get(url, timeout=10)

        # Raise an exception automatically if the status code indicates an error
        # (e.g. 404 Not Found, 500 Server Error).
        response.raise_for_status()

        # The server doesn't always declare its charset correctly, which can
        # cause special characters (like the £ price symbol) to be decoded
        # incorrectly. Forcing UTF-8 here ensures the text comes through clean.
        response.encoding = "utf-8"

        print(f"Successfully fetched page: {url} (status code: {response.status_code})")
        return response.text

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the website. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("Error: The request timed out. The server may be slow or unreachable.")
    except requests.exceptions.HTTPError as http_err:
        print(f"Error: HTTP request failed with status code {response.status_code}. ({http_err})")
    except requests.exceptions.RequestException as err:
        print(f"Error: An unexpected error occurred while fetching the page. ({err})")

    return None


def scrape_books(html_content):
    """
    Parse the HTML content and extract book details.

    Each book on the page is contained inside an <article class="product_pod">
    element. Inside that element we find:
        - Title       -> <h3><a title="...">
        - Price       -> <p class="price_color">
        - Availability -> <p class="instock availability">
        - Rating      -> <p class="star-rating <Word>">

    Args:
        html_content (str): Raw HTML of the page.

    Returns:
        list[dict]: A list of dictionaries, one per book, each containing
                    'title', 'price', 'availability', and 'rating'.
    """
    books = []

    if not html_content:
        print("Error: No HTML content to parse.")
        return books

    soup = BeautifulSoup(html_content, "html.parser")

    # Every book on the page is inside an <article class="product_pod"> tag.
    book_elements = soup.find_all("article", class_="product_pod")

    if not book_elements:
        print("Warning: No book elements were found on the page. "
              "The website structure may have changed.")
        return books

    for book in book_elements:
        try:
            # --- Title ---
            # The title is stored in the "title" attribute of the <a> tag
            # inside the <h3> tag (it's more complete than the link text,
            # which can be truncated with "...").
            title_tag = book.h3.a
            title = title_tag["title"] if title_tag and title_tag.has_attr("title") else "N/A"

            # --- Price ---
            price_tag = book.find("p", class_="price_color")
            price = price_tag.get_text(strip=True) if price_tag else "N/A"

            # --- Availability ---
            availability_tag = book.find("p", class_="instock availability")
            availability = availability_tag.get_text(strip=True) if availability_tag else "N/A"

            # --- Rating ---
            # The rating is encoded as a CSS class, e.g. class="star-rating Three".
            # We look for the second class name and convert it to a number.
            rating_tag = book.find("p", class_="star-rating")
            rating = "N/A"
            if rating_tag and rating_tag.has_attr("class"):
                classes = rating_tag["class"]  # e.g. ['star-rating', 'Three']
                for word, number in RATING_WORDS.items():
                    if word in classes:
                        rating = number
                        break

            books.append({
                "title": title,
                "price": price,
                "availability": availability,
                "rating": rating,
            })

        except AttributeError as err:
            # If a specific book is missing an expected element, skip it
            # instead of crashing the whole program.
            print(f"Warning: Skipping a book due to missing data. ({err})")
            continue

    return books


def save_to_csv(books, filename):
    """
    Save the list of book dictionaries into a CSV file.

    Args:
        books (list[dict]): The scraped book data.
        filename (str): The name of the CSV file to create.

    Returns:
        bool: True if the file was saved successfully, False otherwise.
    """
    if not books:
        print("Error: No book data to save. CSV file was not created.")
        return False

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
            fieldnames = ["title", "price", "availability", "rating"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(books)

        print(f"Data successfully saved to '{filename}'.")
        return True

    except (IOError, OSError) as err:
        print(f"Error: Could not write to file '{filename}'. ({err})")
        return False


def main():
    """
    Main entry point of the program.

    Orchestrates the scraping process:
        1. Fetch the page.
        2. Extract book data.
        3. Save the data to a CSV file.
        4. Report the results to the user.
    """
    print(f"Starting scraper for: {URL}\n")

    html_content = fetch_page(URL)

    if html_content is None:
        print("Scraping aborted because the page could not be retrieved.")
        sys.exit(1)

    books = scrape_books(html_content)

    if not books:
        print("Scraping finished, but no books were found.")
        sys.exit(1)

    save_to_csv(books, OUTPUT_FILE)

    print(f"\nDone! Successfully scraped {len(books)} books.")


if __name__ == "__main__":
    main()

