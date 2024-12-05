import requests
import json
import csv

# The URL for the GraphQL endpoint
url = 'https://www.ratemyprofessors.com/graphql'

# Headers from the network request
headers = {
    'Authorization': 'Basic dGVzdDp0ZXN0',  # Replace with the actual base64 authorization token
    'Content-Type': 'application/json',
    'Cookie': '_pubcid=38047a93-f80f-4979-82f9-f4c2ccf23f4f; ...',  # Include necessary cookies
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Referer': 'https://www.ratemyprofessors.com/search/professors/971?q=',
    'Origin': 'https://www.ratemyprofessors.com',
    'Accept': '*/*',
}

# Initial query payload with the necessary structure
data = {
    "query": """
    query TeacherSearchPaginationQuery(
      $count: Int!
      $cursor: String
      $query: TeacherSearchQuery!
    ) {
      search: newSearch {
        ...TeacherSearchPagination_search_1jWD3d
      }
    }

    fragment TeacherSearchPagination_search_1jWD3d on newSearch {
      teachers(query: $query, first: $count, after: $cursor) {
        didFallback
        edges {
          cursor
          node {
            ...TeacherCard_teacher
            id
            __typename
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
        resultCount
        filters {
          field
          options {
            value
            id
          }
        }
      }
    }

    fragment TeacherCard_teacher on Teacher {
      id
      legacyId
      avgRating
      numRatings
      ...CardFeedback_teacher
      ...CardSchool_teacher
      ...CardName_teacher
      ...TeacherBookmark_teacher
    }

    fragment CardFeedback_teacher on Teacher {
      wouldTakeAgainPercent
      avgDifficulty
    }

    fragment CardSchool_teacher on Teacher {
      department
      school {
        name
        id
      }
    }

    fragment CardName_teacher on Teacher {
      firstName
      lastName
    }

    fragment TeacherBookmark_teacher on Teacher {
      id
      isSaved
    }
    """,
    "variables": {
        "count": 1000,  # Number of results per page
        "cursor": "YXJyYXljb25uZWN0aW9uOjE1",  # Cursor for pagination (replace with actual value if necessary)
        "query": {
            "text": "",
            "schoolID": "U2Nob29sLTk3MQ==",  # Example school ID
            "fallback": True
        }
    }
}

# Making the POST request
response = requests.post(url, headers=headers, json=data)

# Check if the response was successful
if response.status_code == 200:
    print('Request was successful!')
    result = response.json()

    # Extract relevant data
    teachers = result.get('data', {}).get('search', {}).get('teachers', {}).get('edges', [])

    # Prepare data for CSV
    data_to_save = []
    for teacher in teachers:
        node = teacher['node']
        department = node.get('department', '')
        first_name = node.get('firstName', '')
        last_name = node.get('lastName', '')
        school_name = node.get('school', {}).get('name', '')
        avg_rating = node.get('avgRating', '')
        num_ratings = node.get('numRatings', '')
        would_take_again = node.get('wouldTakeAgainPercent', '')
        avg_difficulty = node.get('avgDifficulty', '')

        # Here we prepare the row for the CSV file
        data_to_save.append([
            department,  # tDept
            "",  # tSid (You can add this if the data is available)
            school_name,  # institution_name
            first_name,  # tFname
            "",  # tMiddlename
            last_name,  # tLname
            node.get('id', ''),  # tid
            num_ratings,  # tNumRatings
            "",  # rating_class (Could be derived from the ratings if needed)
            "TEACHER",  # contentType
            "PROFESSOR",  # categoryType
            avg_rating  # overall_rating
        ])

    # Save data to CSV file
    csv_file = 'professors_data.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Writing headers
        writer.writerow(["tDept", "tSid", "institution_name", "tFname", "tMiddlename", "tLname", "tid", "tNumRatings", "rating_class", "contentType", "categoryType", "overall_rating"])
        # Writing data
        writer.writerows(data_to_save)

    print(f"Data has been saved to {csv_file}")

else:
    print(f'Failed to fetch data. Status code: {response.status_code}')
