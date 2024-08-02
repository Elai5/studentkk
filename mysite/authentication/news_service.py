import requests
from requests.exceptions import HTTPError, Timeout, RequestException

class NewsService:
    API_KEY = 'fbae98d6c8c045f5b378e44df0ed23c3'
    BASE_URL = 'https://newsapi.org/v2/everything'  # Use the 'everything' endpoint for keyword-based searches

    @staticmethod
    def get_custom_news(query):
        params = {
            'apiKey': NewsService.API_KEY,
            'q': query,  # The query to search for specific topics
            'language': 'en',
            'sortBy': 'relevancy',  # Sort results by relevance
            'pageSize': 3  # Limit the number of results
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
    
    def get_news_by_category(category, location, institution):
        queries = {
            'accommodation': f"housing tips in {location}",
            'culture': f"culture in {location}",
            'transportation': f"transportation in {location}",
            'food': f"food options in {location}",
            'healthcare': f"healthcare services in {location}",
            'weather': f"weather in {location}",
            'student_resources': f"student resources in {location}",
            'legal': f"legal advice for students in {location}",
            'events': f"events and social activities in {location}",
            'financial': f"financial management for students in {location}",
            'school': f"{institution} news" if institution else ''
        }
        
        query = queries.get(category, '')
        if not query:
            return []
        
        return NewsService.get_custom_news(query)

        
# def get_news_by_category(location, institution):
#     categories = {
#         'school': f"{institution}",
#         'culture': f"culture in {location}",
#         'events': f"events in {location}",
#         'food': f"food in {location}",
#         'weather': f"weather in {location}"
#     }

#     news_by_category = {}
#     for category, query in categories.items():
#         news_by_category[category] = NewsService.get_custom_news(query, location)
    

