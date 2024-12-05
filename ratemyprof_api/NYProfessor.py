import requests
import csv
import json

# The URL for the GraphQL endpoint
url = 'https://www.ratemyprofessors.com/graphql'

# Headers for the request
headers = {
    'Authorization': 'Basic dGVzdDp0ZXN0',  # Replace with the actual base64 authorization token
    'Content-Type': 'application/json',
    'Cookie': '_pubcid=38047a93-f80f-4979-82f9-f4c2ccf23f4f; ...',  # Include necessary cookies
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Referer': 'https://www.ratemyprofessors.com/search/professors/971?q=',
    'Origin': 'https://www.ratemyprofessors.com',
    'Accept': '*/*',
}

# Query to fetch professors based on school ID
def fetch_professors_by_school(school_id):
    data = {
        "query": """
        query TeacherSearchPaginationQuery(
          $count: Int!
          $cursor: String
          $query: TeacherSearchQuery!
        ) {
          search: newSearch {
            teachers(query: $query, first: $count, after: $cursor) {
              edges {
                cursor
                node {
                  id
                  legacyId
                  avgRating
                  numRatings
                  firstName
                  lastName
                  department
                  school {
                    name
                    id
                  }
                  wouldTakeAgainPercent
                  avgDifficulty
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
            "count": 100,  # Adjust the number of results per page
            "cursor": "",
            "query": {
                "schoolID": school_id,
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        professors = response_data.get('data', {}).get('search', {}).get('teachers', {}).get('edges', [])
        return professors, response_data
    else:
        print(f"Failed to fetch professors data for school {school_id}. Status code: {response.status_code}")
        return None, None


# Reading school data from CSV and filtering by New York (NY)
with open('all_schools_data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # List to hold professors data
    professors_data = []

    # Loop through each school and fetch professors only for New York schools
    for row in reader:
        school_id = row.get('id')
        school_name = row.get('institution_name')
        state = row.get('state')

        # Check if the school is located in New York (NY)
        if state == 'NY' and school_id:
            print(f"Fetching professors for school: {school_name} (ID: {school_id})")
            professors, response_data = fetch_professors_by_school(school_id)
            
            if professors:
                for professor in professors:
                    node = professor['node']
                    department = node.get('department', '')
                    first_name = node.get('firstName', '')
                    last_name = node.get('lastName', '')
                    school_name = node.get('school', {}).get('name', '')
                    avg_rating = node.get('avgRating', '')
                    num_ratings = node.get('numRatings', '')
                    would_take_again = node.get('wouldTakeAgainPercent', '')
                    avg_difficulty = node.get('avgDifficulty', '')
                    
                    # Prepare the data for each professor
                    professors_data.append([
                        department,  # tDept
                        "",  # tSid
                        school_name,  # institution_name
                        first_name,  # tFname
                        "",  # tMiddlename
                        last_name,  # tLname
                        node.get('id', ''),  # tid
                        num_ratings,  # tNumRatings
                        "",  # rating_class
                        "TEACHER",  # contentType
                        "PROFESSOR",  # categoryType
                        avg_rating  # overall_rating
                    ])
            else:
                print(f"No professors data found for school: {school_name}")
        else:
            print(f"Skipping row: {school_name} (ID: {school_id}) - Not a New York school")

# Saving the professors data into CSV
with open('professors_data_ny_schools.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Writing headers
    writer.writerow(["tDept", "tSid", "institution_name", "tFname", "tMiddlename", "tLname", "tid", "tNumRatings", "rating_class", "contentType", "categoryType", "overall_rating"])
    # Writing the collected professors data
    writer.writerows(professors_data)

print(f"All professors data for New York schools has been saved to 'professors_data_ny_schools.csv'.")
