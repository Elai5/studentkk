import time
import requests
from requests.exceptions import HTTPError, RequestException, Timeout
from django.core.cache import cache

class NewsService:
    BASE_URL = 'https://newsapi.org/v2/everything'
    API_KEY = 'fbae98d6c8c045f5b378e44df0ed23c3'

    @staticmethod
    def get_custom_news(query):
        cache_key = f"news_{query.replace(' ', '_')}"
        cached_news = cache.get(cache_key)
        
        if cached_news:
            return cached_news

        params = {
            'apiKey': NewsService.API_KEY,
            'q': query,
            'language': 'en',
            'sortBy': 'relevancy',
            'pageSize': 3
        }

        attempt = 0
        max_attempts = 5
        backoff_time = 1  # Initial backoff time in seconds

        while attempt < max_attempts:
            try:
                response = requests.get(NewsService.BASE_URL, params=params, timeout=10)
                response.raise_for_status()
                articles = response.json().get('articles', [])
                cache.set(cache_key, articles, 3600)  # Cache the results for 1 hour
                return articles

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

        print("Max retries exceeded. Could not fetch the news.")
        return []

    @staticmethod
    def get_news_by_category(category, location, institution):
        queries = {
            'accommodation': f"housing tips in {location}",
            'transportation': f"transportation in {location}",
            'student_resources': f"student resources in {location}",
            'school': f"{institution} news" if institution else ''
        }

        query = queries.get(category, '')
        if not query:
            return []

        return NewsService.get_custom_news(query)
