import newspaper
import pandas as pd
import lxml.etree
import lxml.html
import lxml.html.clean
import datetime
import re
from lxml import html
from urllib.parse import urlparse


def get_article_urls(main_url):
    try:
        article_urls = []
        main_page = newspaper.build(main_url)
        for article in main_page.articles:
            article_urls.append(article.url)

        return article_urls if article_urls else None

    except Exception as e:
        print("Error: ", e)


def remove_citations(text):
    citation_patterns = [
        r'\[\d+\]',
        r'\(\w+\s*,\s*\d+\)'
    ]
    combined_pattern = '|'.join(citation_patterns)
    cleaned_text = re.sub(combined_pattern, '', text)

    return cleaned_text


def remove_n(text):
    return text.replace("\n", ' ')


def remove_t(text):
    return text.replace('\t', ' ')


def extract_tables(html_content):
    tree = html.fromstring(html_content)
    tables = tree.xpath('//table')
    table_data = []
    if tables:
        for table in tables:
            df = pd.read_html(html.tostring(table), header=0, encoding='utf-8')[0]
            df.fillna('-', inplace=True)

            table_data.append(df.to_dict(orient='records'))

        return table_data
    else:
        return None


def replace_nonbreaking_spaces(text):
    return re.sub(r'\s+', ' ', text)


def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc.split('.')[1]


def encoding_text(text):
    encoded_text = text.encode('utf-8')
    decoded_text = encoded_text.decode('utf-8')
    return decoded_text


def clean_special_char(text):
    return re.sub(r'\s+', ' ', text)