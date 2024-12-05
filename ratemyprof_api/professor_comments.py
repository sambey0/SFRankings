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

# Replace with the actual professor ID
professor_id = 'VGVhY2hlci0zMzYwMTc='

# Initial query payload to fetch comments for a professor
data = {
    "query": """
    query RatingsListQuery(
      $count: Int!
      $id: ID!
      $courseFilter: String
      $cursor: String
    ) {
      node(id: $id) {
        __typename
        ... on Teacher {
          ratings(first: $count, after: $cursor, courseFilter: $courseFilter) {
            edges {
              cursor
              node {
                id
                comment
                class
                helpfulRating
                clarityRating
                difficultyRating
                grade
                textbookUse
                attendanceMandatory
                wouldTakeAgain
                createdByUser
                thumbsUpTotal
                thumbsDownTotal
                flagStatus
                date
              }
            }
            pageInfo {
              hasNextPage
              endCursor
            }
          }
        }
      }
    }
    """,
    "variables": {
        "count": 50,  # Number of comments per request
        "id": professor_id,
        "courseFilter": "",
        "cursor": ""  # Leave empty to get the first batch of comments
    }
}

# Making the POST request
response = requests.post(url, headers=headers, json=data)

# Check if the response was successful
if response.status_code == 200:
    print('Request was successful!')
    result = response.json()

    # Extract ratings (comments) data
    ratings = result.get('data', {}).get('node', {}).get('ratings', {}).get('edges', [])

    # Prepare data for CSV
    data_to_save = []
    for rating in ratings:
        node = rating['node']
        comment = node.get('comment', '')
        date = node.get('date', '')
        clarity_rating = node.get('clarityRating', '')
        helpful_rating = node.get('helpfulRating', '')
        difficulty_rating = node.get('difficultyRating', '')
        grade = node.get('grade', '')
        textbook_use = node.get('textbookUse', '')
        attendance = node.get('attendanceMandatory', '')
        would_take_again = node.get('wouldTakeAgain', '')
        thumbs_up = node.get('thumbsUpTotal', 0)
        thumbs_down = node.get('thumbsDownTotal', 0)
        flag_status = node.get('flagStatus', '')

        # Constructing the row for CSV
        data_to_save.append([
            node.get('id', ''),  # tid
            attendance,  # attendance
            '',  # clarityColor
            '',  # easyColor
            '',  # helpColor
            '',  # helpCount
            node.get('id', ''),  # id
            '',  # notHelpCount
            '',  # onlineClass
            '',  # quality
            clarity_rating,  # rClarity
            node.get('class', ''),  # rClass
            comment,  # rComments
            date,  # rDate
            '',  # rEasy
            '',  # rEasyString
            '',  # rErrorMsg
            helpful_rating,  # rHelpful
            '',  # rInterest
            '',  # rOverall
            '',  # rOverallString
            '',  # rStatus
            textbook_use,  # rTextBookUse
            '',  # rTimestamp
            would_take_again,  # rWouldTakeAgain
            '',  # sId
            '',  # takenForCredit
            '',  # teacher
            '',  # teacherGrade
            '',  # teacherRatingTags
            '',  # unUsefulGrouping
            ''  # usefulGrouping
        ])

    # Save data to CSV file
    csv_file = 'professor_comments.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Writing headers
        writer.writerow([
            "tid", "attendance", "clarityColor", "easyColor", "helpColor", "helpCount", "id",
            "notHelpCount", "onlineClass", "quality", "rClarity", "rClass", "rComments", "rDate",
            "rEasy", "rEasyString", "rErrorMsg", "rHelpful", "rInterest", "rOverall", "rOverallString",
            "rStatus", "rTextBookUse", "rTimestamp", "rWouldTakeAgain", "sId", "takenForCredit", "teacher",
            "teacherGrade", "teacherRatingTags", "unUsefulGrouping", "usefulGrouping"
        ])
        # Writing data
        writer.writerows(data_to_save)

    print(f"Data has been saved to {csv_file}")

else:
    print(f'Failed to fetch data. Status code: {response.status_code}')
