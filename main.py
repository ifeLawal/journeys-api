# from models import drop_all
# from models.db import create_ontheset_tables, drop_ontheset_table
from scraper.custom_page_scrape import scrape_full_movie_list

BASE_URL = "http://onthesetofnewyork.com/"
TEST_PAGE = "serpico.html"
FULL_LIST_PAGE = "filmlocations-a-z.html"

# scrape_ontheset_movie_page(BASE_URL, TEST_PAGE)
scrape_full_movie_list(BASE_URL, FULL_LIST_PAGE)

# drop_ontheset_table(table_name="movies")
# drop_all(engine_name="ontheset")
# create_ontheset_tables()
