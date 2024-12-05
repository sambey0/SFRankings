import requests
import json

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

# Checking the response status
if response.status_code == 200:
    print('Request was successful!')
    result = response.json()
    print(json.dumps(result, indent=4))  # This will print the formatted JSON response from the API

    # Check if there is another page to fetch
    page_info = result.get('data', {}).get('search', {}).get('teachers', {}).get('pageInfo', {})
    has_next_page = page_info.get('hasNextPage', False)
    if has_next_page:
        next_cursor = page_info.get('endCursor')
        print(f'Next cursor: {next_cursor}')
        # You can use the next_cursor to make the next request
else:
    print(f'Failed to fetch data. Status code: {response.status_code}')
