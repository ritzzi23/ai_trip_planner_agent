import requests
import os
from typing import List, Dict, Any

class FoursquareSearchTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.foursquare.com/v3"
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"fsq3_{api_key}"
        }
    
    def search_venues(self, query: str, location: str, categories: List[str] = None) -> Dict[str, Any]:
        """
        Search for venues using Foursquare API
        """
        try:
            url = f"{self.base_url}/places/search"
            params = {
                "query": query,
                "near": location,
                "limit": 10,
                "sort": "RATING"
            }
            
            if categories:
                params["categories"] = ",".join(categories)
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Foursquare API error: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            print(f"Foursquare API exception: {e}")
            return {}
    
    def foursquare_search_attractions(self, place: str) -> str:
        """
        Search for attractions in the specified place using Foursquare API.
        """
        try:
            categories = ["16000"]  # Arts & Entertainment
            result = self.search_venues("attractions", place, categories)
            
            if result and "results" in result and result["results"]:
                attractions = []
                for venue in result["results"][:5]:  # Top 5 attractions
                    name = venue.get("name", "Unknown")
                    address = venue.get("location", {}).get("formatted_address", "Address not available")
                    rating = venue.get("rating", "No rating")
                    attractions.append(f"• {name} - {address} (Rating: {rating})")
                
                return "\n".join(attractions) if attractions else f"No attractions found for {place}"
            
            return f"Could not fetch attractions for {place}"
        except Exception as e:
            print(f"Foursquare attractions search error: {e}")
            return f"Foursquare API unavailable for {place}"
    
    def foursquare_search_restaurants(self, place: str) -> str:
        """
        Search for restaurants in the specified place using Foursquare API.
        """
        try:
            categories = ["13065"]  # Food & Drink
            result = self.search_venues("restaurants", place, categories)
            
            if result and "results" in result and result["results"]:
                restaurants = []
                for venue in result["results"][:5]:  # Top 5 restaurants
                    name = venue.get("name", "Unknown")
                    address = venue.get("location", {}).get("formatted_address", "Address not available")
                    rating = venue.get("rating", "No rating")
                    price = venue.get("price", "Price not available")
                    restaurants.append(f"• {name} - {address} (Rating: {rating}, Price: {price})")
                
                return "\n".join(restaurants) if restaurants else f"No restaurants found for {place}"
            
            return f"Could not fetch restaurants for {place}"
        except Exception as e:
            print(f"Foursquare restaurants search error: {e}")
            return f"Foursquare API unavailable for {place}"
    
    def foursquare_search_activities(self, place: str) -> str:
        """
        Search for activities in the specified place using Foursquare API.
        """
        try:
            categories = ["16000", "10000"]  # Arts & Entertainment, Travel & Transport
            result = self.search_venues("activities", place, categories)
            
            if result and "results" in result and result["results"]:
                activities = []
                for venue in result["results"][:5]:  # Top 5 activities
                    name = venue.get("name", "Unknown")
                    address = venue.get("location", {}).get("formatted_address", "Address not available")
                    rating = venue.get("rating", "No rating")
                    activities.append(f"• {name} - {address} (Rating: {rating})")
                
                return "\n".join(activities) if activities else f"No activities found for {place}"
            
            return f"Could not fetch activities for {place}"
        except Exception as e:
            print(f"Foursquare activities search error: {e}")
            return f"Foursquare API unavailable for {place}"
    
    def foursquare_search_transportation(self, place: str) -> str:
        """
        Search for transportation options in the specified place using Foursquare API.
        """
        try:
            categories = ["10000"]  # Travel & Transport
            result = self.search_venues("transportation", place, categories)
            
            if result and "results" in result and result["results"]:
                transport_options = []
                for venue in result["results"][:5]:  # Top 5 transport options
                    name = venue.get("name", "Unknown")
                    address = venue.get("location", {}).get("formatted_address", "Address not available")
                    transport_options.append(f"• {name} - {address}")
                
                return "\n".join(transport_options) if transport_options else f"No transportation options found for {place}"
            
            return f"Could not fetch transportation options for {place}"
        except Exception as e:
            print(f"Foursquare transportation search error: {e}")
            return f"Foursquare API unavailable for {place}" 