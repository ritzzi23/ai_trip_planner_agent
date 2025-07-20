import os
from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool
from utils.foursquare_search import FoursquareSearchTool
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv

class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.google_api_key = os.environ.get("GPLACES_API_KEY")
        self.foursquare_api_key = os.environ.get("FOURSQUARE_API_KEY")
        
        # Initialize Google Places search only if API key is available
        if self.google_api_key and self.google_api_key.strip():
            try:
                self.google_places_search = GooglePlaceSearchTool(self.google_api_key)
                self.google_available = True
            except Exception as e:
                print(f"Warning: Google Places API initialization failed: {e}")
                self.google_available = False
        else:
            print("Warning: GPLACES_API_KEY not found or empty")
            self.google_available = False
        
        # Initialize Foursquare search only if API key is available
        if self.foursquare_api_key and self.foursquare_api_key.strip():
            try:
                self.foursquare_search = FoursquareSearchTool(self.foursquare_api_key)
                self.foursquare_available = True
            except Exception as e:
                print(f"Warning: Foursquare API initialization failed: {e}")
                self.foursquare_available = False
        else:
            print("Warning: FOURSQUARE_API_KEY not found or empty")
            self.foursquare_available = False
            
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""
        @tool
        def search_attractions(place:str) -> str:
            """Search attractions of a place"""
            # Try Google Places first
            if self.google_available:
                try:
                    attraction_result = self.google_places_search.google_search_attractions(place)
                    if attraction_result:
                        return f"Following are the attractions of {place} as suggested by Google: {attraction_result}"
                except Exception as e:
                    print(f"Google Places API error: {e}")
            
            # Try Foursquare second
            if self.foursquare_available:
                try:
                    foursquare_result = self.foursquare_search.foursquare_search_attractions(place)
                    if foursquare_result and "No attractions found" not in foursquare_result:
                        return f"Following are the attractions of {place} as suggested by Foursquare: {foursquare_result}"
                except Exception as e:
                    print(f"Foursquare API error: {e}")
            
            # Fallback to Tavily search
            tavily_result = self.tavily_search.tavily_search_attractions(place)
            return f"Following are the attractions of {place}: {tavily_result}"
        
        @tool
        def search_restaurants(place:str) -> str:
            """Search restaurants of a place"""
            # Try Google Places first
            if self.google_available:
                try:
                    restaurants_result = self.google_places_search.google_search_restaurants(place)
                    if restaurants_result:
                        return f"Following are the restaurants of {place} as suggested by Google: {restaurants_result}"
                except Exception as e:
                    print(f"Google Places API error: {e}")
            
            # Try Foursquare second
            if self.foursquare_available:
                try:
                    foursquare_result = self.foursquare_search.foursquare_search_restaurants(place)
                    if foursquare_result and "No restaurants found" not in foursquare_result:
                        return f"Following are the restaurants of {place} as suggested by Foursquare: {foursquare_result}"
                except Exception as e:
                    print(f"Foursquare API error: {e}")
            
            # Fallback to Tavily search
            tavily_result = self.tavily_search.tavily_search_restaurants(place)
            return f"Following are the restaurants of {place}: {tavily_result}"
        
        @tool
        def search_activities(place:str) -> str:
            """Search activities of a place"""
            # Try Google Places first
            if self.google_available:
                try:
                    activities_result = self.google_places_search.google_search_activity(place)
                    if activities_result:
                        return f"Following are the activities in and around {place} as suggested by Google: {activities_result}"
                except Exception as e:
                    print(f"Google Places API error: {e}")
            
            # Try Foursquare second
            if self.foursquare_available:
                try:
                    foursquare_result = self.foursquare_search.foursquare_search_activities(place)
                    if foursquare_result and "No activities found" not in foursquare_result:
                        return f"Following are the activities in and around {place} as suggested by Foursquare: {foursquare_result}"
                except Exception as e:
                    print(f"Foursquare API error: {e}")
            
            # Fallback to Tavily search
            tavily_result = self.tavily_search.tavily_search_activity(place)
            return f"Following are the activities of {place}: {tavily_result}"
        
        @tool
        def search_transportation(place:str) -> str:
            """Search transportation of a place"""
            # Try Google Places first
            if self.google_available:
                try:
                    transport_result = self.google_places_search.google_search_transportation(place)
                    if transport_result:
                        return f"Following are the modes of transportation available in {place} as suggested by Google: {transport_result}"
                except Exception as e:
                    print(f"Google Places API error: {e}")
            
            # Try Foursquare second
            if self.foursquare_available:
                try:
                    foursquare_result = self.foursquare_search.foursquare_search_transportation(place)
                    if foursquare_result and "No transportation options found" not in foursquare_result:
                        return f"Following are the modes of transportation available in {place} as suggested by Foursquare: {foursquare_result}"
                except Exception as e:
                    print(f"Foursquare API error: {e}")
            
            # Fallback to Tavily search
            tavily_result = self.tavily_search.tavily_search_transportation(place)
            return f"Following are the modes of transportation available in {place}: {tavily_result}"
        
        return [search_attractions, search_restaurants, search_activities, search_transportation]