import requests
import csv
import string

# Define the URL for the GraphQL endpoint
url = 'https://www.ratemyprofessors.com/graphql'

# Define the headers for the request
headers = {
    'Authorization': 'Basic dGVzdDp0ZXN0',  # Replace with the actual base64 authorization token
    'Content-Type': 'application/json',
    'Cookie': '_pubcid=38047a93-f80f-4979-82f9-f4c2ccf23f4f; ...',  # Include necessary cookies
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Referer': 'https://www.ratemyprofessors.com/search/schools?q=a',  # Adjust if needed
    'Origin': 'https://www.ratemyprofessors.com',
    'Accept': '*/*',
}

# Basic query to fetch schools
def fetch_schools_by_letter(letter):
    data = {
        "query": """
        query SchoolSearchPaginationQuery(
          $count: Int!
          $cursor: String
          $query: SchoolSearchQuery!
        ) {
          search: newSearch {
            schools(query: $query, first: $count, after: $cursor) {
              edges {
                cursor
                node {
                  name
                  city
                  state
                  avgRating
                  numRatings
                  id
                }
              }
              pageInfo {
                hasNextPage
                endCursor
              }
              resultCount
            }
          }
        }
        """,
        "variables": {
            "count": 1000,  # Number of results per page
            "cursor": "",  # Starting cursor
            "query": {
                "text": letter,  # Query text for a particular letter
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_data = response.json()
        schools = response_data.get('data', {}).get('search', {}).get('schools', {}).get('edges', [])
        
        if schools:
            return schools, response_data
        else:
            return None, response_data
    else:
        print(f"Failed to fetch data for letter '{letter}'. Status code: {response.status_code}")
        return None, None

# Writing the schools data into a CSV file
with open('all_schools_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'city', 'state', 'avgRating', 'numRatings', 'id']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()  # Write the header
    
    # Loop through the alphabet from A to Z
    for letter in string.ascii_uppercase:
        print(f"Fetching schools starting with '{letter}'...")
        schools, response_data = fetch_schools_by_letter(letter)
        
        if schools:
            # Write data for each school
            for school in schools:
                school_data = school.get('node', {})
                writer.writerow({
                    'name': school_data.get('name', ''),
                    'city': school_data.get('city', ''),
                    'state': school_data.get('state', ''),
                    'avgRating': school_data.get('avgRating', ''),
                    'numRatings': school_data.get('numRatings', ''),
                    'id': school_data.get('id', '')
                })
        else:
            print(f"No valid data found for query '{letter}'. Skipping...")

print("Data saved to 'all_schools_data.csv'.")
