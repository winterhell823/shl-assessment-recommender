from app.scraper.scrape_catalog import scrape_catalog
from app.scraper.clean_catalog import clean_catalog


def main():
    print("Scraping SHL catalog...")
    raw_items = scrape_catalog()

    print(f"Scraped {len(raw_items)} items")

    print("Cleaning catalog...")
    clean_items = clean_catalog()

    print(f"Cleaned {len(clean_items)} items")

    print("Done.")


if __name__ == "__main__":
    main()