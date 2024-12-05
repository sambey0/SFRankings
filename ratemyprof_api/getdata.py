import requests
from bs4 import BeautifulSoup

# Define the URL with your search query (e.g., Computer Science)
url = "https://www.ratemyprofessors.com/search/professors/971?q="

# Set headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

# Send GET request to the URL
response = requests.get(url, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    professor_cards = soup.find_all('a', class_='TeacherCard__StyledTeacherCard-syjs0d-0')

    professors = []

    # Loop through each card and extract details
    for card in professor_cards:
        professor = {}

        # Extracting professor name
        name_tag = card.find('div', class_='CardName__StyledCardName-sc-1gyrgim-0')
        if name_tag:
            professor['name'] = name_tag.text.strip()

        # Extracting department
        department_tag = card.find('div', class_='CardSchool__Department-sc-19lmz2k-0')
        if department_tag:
            professor['department'] = department_tag.text.strip()

        # Extracting school
        school_tag = card.find('div', class_='CardSchool__School-sc-19lmz2k-1')
        if school_tag:
            professor['school'] = school_tag.text.strip()

        # Extracting quality rating
        rating_tag = card.find('div', class_='CardNumRating__CardNumRatingNumber-sc-17t4b9u-2')
        if rating_tag:
            professor['rating'] = rating_tag.text.strip()

        # Extracting 'Would take again' percentage
        would_take_again_tag = card.find('div', class_='CardFeedback__CardFeedbackNumber-lq6nix-2')
        if would_take_again_tag:
            professor['would_take_again'] = would_take_again_tag.text.strip()

        # Extracting difficulty level
        difficulty_tag = card.find('div', class_='CardFeedback__CardFeedbackNumber-lq6nix-2')
        if difficulty_tag:
            professor['difficulty'] = difficulty_tag.text.strip()

        # Add the professor to the list
        professors.append(professor)

    # Print the extracted professor data
    for professor in professors:
        print(professor)