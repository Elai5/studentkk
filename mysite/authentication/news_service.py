import requests
from requests.exceptions import HTTPError, Timeout, RequestException

class NewsService:
    API_KEY = 'fbae98d6c8c045f5b378e44df0ed23c3'
    BASE_URL = 'https://newsapi.org/v2/everything'  # Use the 'everything' endpoint for keyword-based searches

    @staticmethod
    def get_custom_news(query, location):
        params = {
            'apiKey': NewsService.API_KEY,
            'q': query,  # The query to search for specific topics
            'language': 'en',
            'sortBy': 'relevancy',  # Sort results by relevance
            'pageSize': 5  # Limit the number of results
        }
        try:
            response = requests.get(NewsService.BASE_URL, params=params, timeout=10)  # Added timeout for request

            # Raise an exception if the response status code indicates an error
            response.raise_for_status()
            
            # Try to get 'articles' from the JSON response
            return response.json().get('articles', [])
        
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Log or handle HTTP errors (e.g., 404, 500)
            return []
        except Timeout:
            print("The request timed out.")  # Log or handle request timeouts
            return []
        except RequestException as req_err:
            print(f"Request error occurred: {req_err}")  # Log or handle other request-related errors
            return []
        except Exception as err:
            print(f"An unexpected error occurred: {err}")  # Log or handle any other unexpected errors
            return []
        
def get_news_by_category(location, institution):
    categories = {
        'school': f"{institution}",
        'culture': f"culture in {location}",
        'events': f"events in {location}",
        'food': f"food in {location}",
        'weather': f"weather in {location}"
    }

    news_by_category = {}
    for category, query in categories.items():
        news_by_category[category] = NewsService.get_custom_news(query, location)
    
    return news_by_category
