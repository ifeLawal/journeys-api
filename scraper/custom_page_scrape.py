import os
import re

from sqlalchemy.orm import sessionmaker

from connecting import get_engine
from models import Comments, Covers, Locations, Movies, Pictures
from scraper.helpers import (alt_select_sections, get_img_paths,
                             get_sections_from_root, get_text, get_url_routes,
                             save_image, select_section)

engine = get_engine(name="ontheset")
Session = sessionmaker(engine)

BASEDIR = os.path.dirname(__file__)


def get_title_and_year(root):
    # Title lxml: //div[@id='post-20']//h2
    title_h2 = get_sections_from_root(root, xpath="//h2")[0]
    title = get_text(title_h2)[0]
    year = re.findall("\(\d+\)", title)[0]  # noqa W605
    year = year[1:-1]

    return (title, year)


def get_cover_image_and_summary(root):
    # Movie_table lxml: //div[@id='post-20']//table[1]
    movie_table = get_sections_from_root(root, xpath="//table")[0]
    # Cover image lxml: //div[@id='post-20']//table[1]//img
    cover_image_path = get_img_paths(movie_table)[0]
    image_name = cover_image_path.split("/")[-1]

    # Movie summary lxml: //div[@id='post-20']//table[1]//p
    movie_summary = get_text(movie_table, inner_tag="//p")[0]
    movie_summary = movie_summary.replace("\n", "")

    return (cover_image_path, image_name, movie_summary)


def get_location_picture_and_comments(root, url_link):
    # Addresses table full lxml: //div[@id='post-20']//table[@background='images/locationbody.jpg']
    # Address full lxml //div[@id='post-20']//table[@background='images/locationbody.jpg'][1]//b/text()
    # Address piece //b/text()
    # Address image paths full lxml //div[@id='post-20']//table[@background='images/locationbody.jpg'][1]/preceding::p[img]/img/@src
    # image path /preceding::p[img]/img/@src
    # Comments //div[@id='post-20']//table[@background='images/locationbody.jpg'][1]/preceding::p[b]/text()
    addresses = get_sections_from_root(
        root, xpath="//table[@background='images/locationbody.jpg']"
    )
    tables = alt_select_sections(
        url=url_link,
        xpath="//div[@id='post-20']//table[@background='images/locationbody.jpg']",
    )
    prev_table = ""
    locations = []
    all_image_paths = []
    all_comments = []

    for index in range(len(tables)):
        address = addresses[index]
        table = tables[index]
        location = get_text(address, inner_tag="//b")[0]
        location_parsed = location[:-1] if location.endswith(".") else location
        locations.append(location_parsed)

        if index == 0:
            image_paths = get_img_paths(table, inner_tag="./preceding::p[img]")
            add_on = get_img_paths(table, inner_tag="./following::p[img]/img")[0]
            image_paths = image_paths + [add_on]
            comments = get_text(table, inner_tag=".//preceding-sibling::p[b]")
        else:
            # To have the lxml choose the images in between the tables, we need to go from the previous table to the current index. lxml starts at a 1 index
            # //div[@id='post-20']//table[@background='images/locationbody.jpg'][1]/following::p[img and count(preceding::table[@background="images/locationbody.jpg"])=1]/img
            image_paths = get_img_paths(
                prev_table,
                inner_tag=f"./following::p[img and count(preceding::table[@background='images/locationbody.jpg'])={index}]/img",
            )
            image_paths = image_paths[1:]
            comments = get_text(
                prev_table,
                inner_tag=f"./following::p[b and count(preceding::table[@background='images/locationbody.jpg'])={index}]",
            )
            if index == len(tables) - 1:
                add_on = get_img_paths(
                    table, inner_tag="./following-sibling::p[img]/img"
                )
                image_paths = image_paths + add_on

        for idx, comment in enumerate(comments):
            if "otsoNY" in comment:
                comments.remove(comment)
            else:
                comments[idx] = comment.replace("\n", "").replace("\t", "")

        all_image_paths.append(image_paths)
        all_comments.append(comments)
        prev_table = table

    return (locations, all_image_paths, all_comments)


def scrape_ontheset_movie_page(base, path):
    url_link = base + path
    root = select_section(url=url_link, xpath="//div[@id='post-20']")

    title, year = get_title_and_year(root)

    print("Title: " + title)
    print("===============")
    print("Year: " + year)
    print("===============")

    with Session() as sess:
        movie = sess.query(Movies).filter_by(name=title, year=year).first()

    if movie is None:
        cover_image_path, image_name, movie_summary = get_cover_image_and_summary(root)

        print("Movie Summary: " + movie_summary)
        print("===============")
        print("Cover Image Path: " + cover_image_path)
        print("===============")
        print("Cover Name: " + image_name)
        print("===============")

        # locations is an array, image_paths and comments are dictionaries
        locations, image_paths, comments = get_location_picture_and_comments(
            root=root, url_link=url_link
        )

        with Session() as session:
            movie = Movies(name=title, year=year, summary=movie_summary)
            session.add(movie)
            session.commit()

            save_image(
                image_url=base + cover_image_path,
                destination=os.path.join(BASEDIR, f"files/{title}/"),
                save_name=image_name,
            )
            cover = Covers(
                file_location=f"files/{title}/{image_name}",
                movie_id=movie.id,
            )
            session.add(cover)
            session.commit()

            for idx, location in enumerate(locations):
                print("Location: " + location)
                print("===============")
                location = Locations(address=locations[idx], movie_id=movie.id)
                session.add(location)
                session.commit()

                print("Images: ", end="")
                for img in image_paths[idx]:
                    image_name = img.split("/")[-1]
                    print(image_name, end=", ")
                    save_image(
                        image_url=base + img,
                        destination=os.path.join(BASEDIR, f"files/{title}/"),
                        save_name=image_name,
                    )
                    picture = Pictures(
                        file_location=f"files/{title}/{image_name}",
                        location_id=location.id,
                        movie_id=movie.id,
                    )
                    session.add(picture)
                print("\n===============")
                print("Comments: ", end="")
                for comment in comments[idx]:
                    print(comment, end=", ")
                    comment = Comments(
                        comment=comment, location_id=location.id, movie_id=movie.id
                    )
                    session.add(comment)
                    pass

                session.commit()
                print("\n===============")
    else:
        pass


def scrape_full_movie_list(base, path):
    url_link = base + path
    root = select_section(url=url_link, xpath="//div[@id='post-20']//table")[0]
    links = get_url_routes(root=root)
    for link in links:
        try:
            scrape_ontheset_movie_page(base=base, path=link)
        except Exception as Argument:
            with open("logging.csv", "a") as log:
                log.write(f"url_link: {base}{link}, failed somehow\n")
                log.write(str(Argument))
                log.write("\n==========\n")
            continue
