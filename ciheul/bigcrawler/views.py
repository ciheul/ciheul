from django.shortcuts import render
from boilerpipe.extract import Extractor
import pymongo
import zlib


def home(request):
    results = search_crawled_pages()
    context = {
        'title_head': 'BigCrawler',
        'title': 'BigCrawler',
        'results': results
    }
    return render(request, "base_bigcrawler.html", context)


def search_crawled_pages(NUM_ARTICLES=10):
    conn = pymongo.MongoClient()
    db = conn.crawl_repository
    results = list(db.articles.find().limit(NUM_ARTICLES))

    for result in results:
        html = zlib.decompress(result['html'])
        extractor = Extractor(extractor='ArticleExtractor', html=html)
        result['content'] = extractor.getText().replace('\n', '<br /><br />')

    conn.close()

    return results
