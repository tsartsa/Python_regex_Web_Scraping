## Information

This is a script showcasing the use of regex in Python, for the purpose of performing Web Scraping.

## Details

The page used to perform the scraping is the laptops' page of `e-shop.gr` and consequently, the use of greek character regex had to be performed.

Not all product pages work, due to inconsistencies in product details formatting.

## Required Python Libraries

- requests (for getting the HTML code of each URL)
- pandas (for inserting all extracted data to a dataframe)
- openpyxl (for exporting the combined data to a .xlsx file)

## Instructions

To execute the script, open a terminal on the directory of where your `e-shop_scraper.py` program is downloaded and execute the `python e-shop_scraper.py` command.

If you are getting errors while executing the script, try changing the base URL to one of the next laptop pages.
You can do this by opening the initial base URL on your browser, selecting the next page of laptops and then replacing the base URL with that of the page you are at until it works.

If the above doesn't work, you can tweak the code even more and make it work (if feeling bold) or you can open up and check the `laptop-data.xlsx` file that I have included in this repository, in order to get a taste of the data that were collected during the Web Scraping process.

## Topics

- Python
- regex
- Web scraping

## Technologies Used

- Python 3.10
- Visual Studio Code

## Notes

University project for the course of Advanced Topics of Programming Languages

Enjoy! 😁