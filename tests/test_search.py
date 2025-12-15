from dotenv import load_dotenv
import os
from src.search import GoogleCustomSearch

if __name__ == "__main__":
    load_dotenv()


    google = GoogleCustomSearch(
        api_key=os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY"), 
        search_engine_id=os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_ID")
    )

    search_results = google.search(query="Palash from Dedalus", substring="linkedin.com/in/")
    print(search_results)
