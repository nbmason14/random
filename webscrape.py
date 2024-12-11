import requests
import pandas as pd
from itertools import combinations

# Your Bing Search API key
API_KEY = "12d1cf59a9b3433e807c9d446b576577"
ENDPOINT = "https://api.bing.microsoft.com/v7.0/news/search"

# List of base search terms
search_terms = [
    "school closures",
    "school consolidations",
    "building repurposing",
    "guideway",
    "Chadbourn Middle",
    "Acme-Delco Middle",
    "Hallsboro Middle"
]

# Function to query Bing News Search API
def query_bing_news_search(query):
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    params = {
        "q": query,
        #"count": 10,  # Number of results per request
        #"textDecorations": True,
        "textFormat": "HTML"#,
        #"freshness": "Year"  # Options: Day, Week, Month, Year
    }
    response = requests.get(ENDPOINT, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Generate combinations of search terms
search_combinations = []
for r in range(1, len(search_terms) + 1):
    search_combinations.extend([" ".join(combo) for combo in combinations(search_terms, r)])

# Query Bing News API for each combination and extract relevant results
results = []
for search_query in search_combinations:
    print(f"Querying: {search_query}")
    try:
        result = query_bing_news_search(search_query)
        if "value" in result:
            for article in result["value"]:
                name = article.get("name", "")
                url = article.get("url", "")
                description = article.get("description", "")
                date_published = article.get("datePublished", "")
                provider = article.get("provider", [{}])[0].get("name", "")
                results.append({
                    "Query": search_query,
                    "Title": name,
                    "Snippet": description,
                    "URL": url,
                    "Date Published": date_published,
                    "Source": provider
                })
    except Exception as e:
        print(f"Error querying {search_query}: {e}")

# Save the results to the Downloads folder
file_path = "H:/GitHub/Random/bing_news_results.csv"  # Adjust for your system if needed

if results:
    df = pd.DataFrame(results)
    df.to_csv(file_path, index=False)
    print(f"Search complete. Results saved to '{file_path}'")
else:
    print("No results found. CSV file was not created.")
