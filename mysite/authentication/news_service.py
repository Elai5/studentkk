import time
import requests
from requests.exceptions import HTTPError, RequestException, Timeout
from django.core.cache import cache

class NewsService:
    # API Base URLs and Keys
    NEWSAPI_BASE_URL = 'https://newsapi.org/v2/everything'
    NEWSAPI_API_KEY = 'fbae98d6c8c045f5b378e44df0ed23c3'
    NEWSDATA_BASE_URL = 'https://newsdata.io/api/1/news'
    NEWSDATA_API_KEY = 'pub_501748e191671851253a67ffe6b68a4c03d8b'
    EVENTREGISTRY_BASE_URL = 'https://eventregistry.org/api/v1/article/getArticles'
    EVENTREGISTRY_API_KEY = 'dfde48d7-1d1e-4ed6-b710-a28ac9cee41d'  # Replace with your EventRegistry API key

    @staticmethod
    def get_custom_news(query, location):
        newsapi_articles = NewsService.fetch_news_from_newsapi(query, location)
        if newsapi_articles:
            return newsapi_articles
        
        newsdata_articles = NewsService.fetch_news_from_newsdata(query, location)
        if newsdata_articles:
            return newsdata_articles
        
        eventregistry_articles = NewsService.fetch_news_from_eventregistry(query, location)
        return eventregistry_articles

    @staticmethod
    def fetch_news_from_newsapi(query, location):
        cache_key = f"news_newsapi_{query.replace(' ', '_')}_{location.replace(' ', '_')}"
        cached_news = cache.get(cache_key)
        
        if cached_news:
            return cached_news

        params = {
            'q': f"{query} AND {location}",
            'language': 'en',
            'sortBy': 'relevancy',
            'pageSize': 3,
            'apiKey': NewsService.NEWSAPI_API_KEY
        }

        attempt = 0
        max_attempts = 5
        backoff_time = 1  # Initial backoff time in seconds

        while attempt < max_attempts:
            try:
                response = requests.get(NewsService.NEWSAPI_BASE_URL, params=params, timeout=10)
                response.raise_for_status()
                articles = response.json().get('articles', [])
                
                # Deduplicate articles
                unique_articles = []
                seen_urls = set()
                
                for article in articles:
                    url = article.get('url')
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        unique_articles.append(article)
                
                cache.set(cache_key, unique_articles, 3600)  # Cache the results for 1 hour
                return unique_articles

            except HTTPError as http_err:
                if response.status_code == 429:  # Rate limit exceeded
                    print(f"Rate limit exceeded. Retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                    backoff_time *= 2  # Exponential backoff
                    attempt += 1
                else:
                    print(f"HTTP error occurred: {http_err}")
                    return []

            except Timeout:
                print("The request timed out.")
                return []

            except RequestException as req_err:
                print(f"Request error occurred: {req_err}")
                return []

            except Exception as err:
                print(f"An unexpected error occurred: {err}")
                return []

        print("Max retries exceeded. Could not fetch the news from NewsAPI.")
        return []

    @staticmethod
    def fetch_news_from_newsdata(query, location):
        cache_key = f"news_newsdata_{query.replace(' ', '_')}_{location.replace(' ', '_')}"
        cached_news = cache.get(cache_key)
        
        if cached_news:
            return cached_news

        params = {
            'q': f"{query} AND {location}",
            'language': 'en',
            'apikey': NewsService.NEWSDATA_API_KEY
        }

        try:
            response = requests.get(NewsService.NEWSDATA_BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            articles = response.json().get('results', [])
            
            # Deduplicate articles
            unique_articles = []
            seen_urls = set()
            
            for article in articles:
                url = article.get('link')
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    unique_articles.append({
                        'title': article.get('title'),
                        'description': article.get('description'),
                        'url': article.get('link'),
                        'urlToImage': article.get('image_url')  # Assuming 'image_url' is the key in NewsData.io response
                    })
            
            cache.set(cache_key, unique_articles, 3600)  # Cache the results for 1 hour
            return unique_articles

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return []

        except Timeout:
            print("The request timed out.")
            return []

        except RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            return []

        except Exception as err:
            print(f"An unexpected error occurred: {err}")
            return []

    @staticmethod
    def fetch_news_from_eventregistry(query, location):
        cache_key = f"news_eventregistry_{query.replace(' ', '_')}_{location.replace(' ', '_')}"
        cached_news = cache.get(cache_key)
        
        if cached_news:
            return cached_news

        params = {
            'apiKey': NewsService.EVENTREGISTRY_API_KEY,
            'query': f"{query} AND {location}",
            'lang': 'eng',
            'sortBy': 'relevance',
            'maxItems': 3
        }

        try:
            response = requests.get(NewsService.EVENTREGISTRY_BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            articles = response.json().get('articles', [])
            
            # Deduplicate articles
            unique_articles = []
            seen_urls = set()
            
            for article in articles:
                url = article.get('url')
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    unique_articles.append({
                        'title': article.get('title'),
                        'description': article.get('description'),
                        'url': article.get('url'),
                        'urlToImage': article.get('imageUrl')  # Adjust key if necessary
                    })
            
            cache.set(cache_key, unique_articles, 3600)  # Cache the results for 1 hour
            return unique_articles

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return []

        except Timeout:
            print("The request timed out.")
            return []

        except RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            return []

        except Exception as err:
            print(f"An unexpected error occurred: {err}")
            return []

    @staticmethod
    def get_news_by_category(category, location, institution):
        queries = {
            'accommodation': f"affordable student housing in {location}",
            'transportation': f"public transportation for students in {location}",
            'student_resources': f"resources for international students in {location}",
            'school': f"universities OR colleges in {location}"
        }

        query = queries.get(category, '')
        if not query:
            return []

        return NewsService.get_custom_news(query, location)
