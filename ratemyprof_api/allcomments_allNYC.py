import requests
import json
import csv
import time
import os

# Function to read professors CSV file
def read_professors_csv(file_path):
    professors = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        print(f"CSV Headers: {reader.fieldnames}")  # Print out the column names for verification
        for row in reader:
            professors.append({
                'tid': row.get('tid', ''),
                'name': f"{row.get('tFname', '')} {row.get('tLname', '')}",
                'school_id': row.get('sId', ''),
                'school_name': row.get('institution_name', '')
            })
    return professors

# Function to fetch comments for a specific professor using their tid
def fetch_comments_for_professor(tid):
    url = 'https://www.ratemyprofessors.com/graphql'
    headers = {
        'Authorization': 'Basic dGVzdDp0ZXN0',  # Replace with the actual base64 authorization token
        'Content-Type': 'application/json',
        'Accept': '*/*',
    }

    # GraphQL query for fetching professor comments
    data = {
        "query": """
        query RatingsListQuery($count: Int!, $id: ID!, $cursor: String) {
          node(id: $id) {
            __typename
            ... on Teacher {
              ratings(first: $count, after: $cursor) {
                edges {
                  cursor
                  node {
                    comment
                    clarityRating
                    helpfulRating
                    difficultyRating
                    createdByUser
                    date
                    id
                    flagStatus
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
            "count": 20,  # Number of comments to fetch per request
            "id": tid,
            "cursor": None  # This will be used for pagination (null for the first request)
        }
    }

    # Make the POST request to fetch the data
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for professor {tid}. Status code: {response.status_code}")
        return None

# Function to save comments data to CSV
def save_comments_to_csv(comments_data, file_name='comments_data.csv'):
    # Define the CSV headers
    headers = [
        "tid", "attendance", "clarityColor", "easyColor", "helpColor", "helpCount", "id", "notHelpCount", "onlineClass",
        "quality", "rClarity", "rClass", "rComments", "rDate", "rEasy", "rEasyString", "rErrorMsg", "rHelpful", "rInterest",
        "rOverall", "rOverallString", "rStatus", "rTextBookUse", "rTimestamp", "rWouldTakeAgain", "sId", "takenForCredit",
        "teacher", "teacherGrade", "teacherRatingTags", "unUsefulGrouping", "usefulGrouping"
    ]

    # Check if the file already exists, append to it if yes, otherwise create a new one
    file_exists = os.path.exists(file_name)

    # Open the CSV file and write the comments
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Writing the headers if the file is empty
        if not file_exists:
            writer.writerow(headers)

        # Writing the data
        for comment in comments_data:
            writer.writerow(comment)

# Main function to fetch and save all comments for professors
def main():
    professors = read_professors_csv('./professors_data_ny_schools.csv')  # Load the professor data

    all_comments = []

    for professor in professors:
        tid = professor['tid']
        print(f"Fetching comments for professor with tid: {tid}")

        try:
            # Fetch the comments for the professor
            response_data = fetch_comments_for_professor(tid)

            if response_data:
                comments = response_data.get('data', {}).get('node', {}).get('ratings', {}).get('edges', [])

                # Prepare the data for each comment
                for comment in comments:
                    node = comment['node']
                    row = [
                        tid,
                        "Not Mandatory",  # Placeholder for attendance
                        "good",           # Placeholder for clarityColor
                        "poor",           # Placeholder for easyColor
                        "good",           # Placeholder for helpColor
                        0,                # helpCount
                        node.get('id', ''),
                        0,                # notHelpCount
                        "",               # onlineClass
                        "awesome",        # quality
                        node.get('clarityRating', ''),
                        node.get('class', ''),
                        node.get('comment', ''),
                        node.get('date', ''),
                        node.get('helpfulRating', ''),
                        "",               # rEasyString
                        "",               # rErrorMsg
                        node.get('helpfulRating', ''),
                        node.get('difficultyRating', ''),
                        node.get('helpfulRating', ''),
                        "N/A",            # rStatus
                        "Yes",            # rTextBookUse
                        int(time.time() * 1000),  # Timestamp in milliseconds
                        "Yes",            # rWouldTakeAgain
                        professor['school_id'],
                        "Yes",            # takenForCredit
                        professor['name'],
                        "A",              # teacherGrade
                        [],               # teacherRatingTags
                        "people",         # unUsefulGrouping
                        "people"          # usefulGrouping
                    ]
                    all_comments.append(row)

            # To prevent hitting API rate limits, you can add a delay between requests
            # time.sleep(2)  # Adding a sleep time of 2 seconds between requests

        except Exception as e:
            print(f"Error while processing professor {tid}: {e}")

        # Save the comments data to a CSV after each professor
        save_comments_to_csv(all_comments)

    print(f"All comments have been saved to comments_data.csv")

# Run the script
if __name__ == "__main__":
    main()
