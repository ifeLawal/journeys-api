import os
import urllib.request

import pandas as pd
import requests
from lxml import etree, html


def save_image(image_url, destination, save_name):
    if not os.path.isdir(destination):
        os.makedirs(destination)
    urllib.request.urlretrieve(image_url, destination + save_name)


def element_to_htmlstring(element, pretty_print=False):
    # Parsing to a file is simply: etree.parse(x).write("outputfile", encoding="utf-8")
    pretty_str = etree.tostring(
        element, pretty_print=pretty_print, encoding="unicode" if pretty_print else None
    )
    return str(pretty_str)


def get_text(root, inner_tag=""):
    return root.xpath(f"{inner_tag}//text()")


def get_url_routes(root, inner_tag=""):
    return root.xpath(f"{inner_tag}//@href")


def get_img_paths(root, inner_tag=""):
    return root.xpath(f"{inner_tag}//@src")


def select_section(url, xpath, position=0):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    section = tree.xpath(xpath)[position]
    section_html_string = etree.tostring(section, pretty_print=True)
    section_root = html.fromstring(section_html_string)
    return section_root


def alt_select_sections(url, xpath):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree.xpath(xpath)


def select_sections(url, xpath):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return set_sections_as_root(roots=[tree], xpath=xpath)


def get_sections_from_root(elem, xpath):
    sections = elem.xpath(xpath)
    section_roots = []
    for section in sections:
        section_html_string = etree.tostring(section)
        section_root = html.fromstring(section_html_string)
        section_roots.append(section_root)
    return section_roots


def set_sections_as_root(roots, xpath):
    for root in roots:
        sections = root.xpath(xpath)
        section_roots = []
        for section in sections:
            section_html_string = etree.tostring(section)
            section_root = html.fromstring(section_html_string)
            section_roots.append(section_root)
    return section_roots


def select_sections_from_url(url, xpath):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return set_sections_as_root(roots=[tree], xpath=xpath)


def select_sections_from_urllist(url_list, xpath):
    section_list = []
    for url in url_list:
        section_list.append(select_sections_from_url(url, xpath))
    return section_list


def scrape_section(
    roots, scrape_data, columns, xpath="//body"
):  # start with returning a dataframe
    # use url and xpath to get to new_root
    section_roots = set_sections_as_root(roots, xpath)
    column_data = []
    for section in section_roots:
        column_data.append(scrape_data(section))
    return pd.DataFrame(column_data, columns=columns)
