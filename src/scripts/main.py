from newspaper import Article
from newspaper import fulltext

from ..utils.helper import *
import json


def newspaper_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        text = article.text
        text = remove_citations(text)
        text = remove_n(text)
        text = remove_t(text)
        text = encoding_text(text)
        text = clean_special_char(text)

        title = article.title
        title = remove_citations(title)
        title = remove_n(title)
        title = remove_t(title)
        title = encoding_text(title)
        title = clean_special_char(title)

        summary = article.summary
        summary = remove_citations(summary)
        summary = remove_n(summary)
        summary = remove_t(summary)
        summary = encoding_text(summary)
        summary = clean_special_char(summary)

        result = {
            "Domain": extract_domain(url),
            "Published date": article.publish_date.strftime("%d/%m/%Y") if article.publish_date else None,
            "Authors": article.authors if article.authors else None,
            'Keywords': article.keywords if article.keywords else None,
            "Title": title if title else None,
            'Summary': summary if summary else None,
            "Content": {"heading": title if title else None,
                        "text": text if text else None,
                        }
        }
        tables = extract_tables(article.html)
        if tables:
            result['Content']['tables'] = tables
        return result

    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":

    df = pd.read_csv(r"data\urls - content_details.csv")
    urls = df['url']
    urls = urls.dropna().to_list()

    article_data = []
    for url in urls[:60]:
        try:
            result = newspaper_article(url)
            article_data.append({'url': url,
                                 'data': result})
        except Exception as e:
            print(url, e)
            article_data.append({'url': url,
                                 'error': e})

    # with open(r'data\newspaper_output.json', 'w') as file:
    #     json.dump(article_data, file)