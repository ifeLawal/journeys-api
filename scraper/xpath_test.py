import urllib.request

import scraper.xpath_scrapers as x_scrape
from scraper.custom_page_scrape import scrape_data_from_ontheset

image_url = "https://bit.ly/2XuVzB4"  # the image on the web
save_name = "my_image.jpg"  # local name to be saved
urllib.request.urlretrieve(image_url, save_name)


def flatten_list(list):
    return [item for sublist in list for item in sublist]


ontheset_url = "http://onthesetofnewyork.com/"
all_movies = "filmlocations-a-z.html"

table = x_scrape.select_sections_from_url(
    url=ontheset_url + all_movies, xpath='//div[@id="post-20"]//table[1]'
)
ontheset_df = x_scrape.scrape_section(
    roots=table,
    scrape_data=scrape_data_from_ontheset,
    columns=["Movie Name", "Movie Page Link"],
    xpath="//a",
)

movie_page_routes = flatten_list(ontheset_df["Movie Page Link"].tolist())
ontheset_url_list = [ontheset_url + page_route for page_route in movie_page_routes]

movie_page_sections = x_scrape.select_sections_from_urllist(
    url_list=ontheset_url_list[0:2], xpath="//div[@id='post-20']"
)
flattened = flatten_list(movie_page_sections)
print(flattened)
