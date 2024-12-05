import pandas as pd
import csv
from scholarly import scholarly

def fetch_research_data_bulk(professor_names, output_file='research_data.csv'):
    # Open the CSV file for writing
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        # Initialize CSV writer
        fieldnames = ['Professor', 'Title', 'Year', 'Citations', 'Venue']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()

        for professor_name in professor_names:
            search_query = scholarly.search_author(professor_name)
            
            try:
                author = next(search_query)
            except StopIteration:
                # If no author is found, add a row with 0 citations for that professor
                writer.writerow({
                    'Professor': professor_name,
                    'Title': 'N/A',
                    'Year': 'N/A',
                    'Citations': 0,
                    'Venue': 'N/A'
                })
                continue  # Skip to the next professor if no results are found
            
            author_info = scholarly.fill(author)
            publications = author_info.get('publications', [])
            
            if not publications:  # If no publications are found, add a row with 0 citations
                writer.writerow({
                    'Professor': professor_name,
                    'Title': 'N/A',
                    'Year': 'N/A',
                    'Citations': 0,
                    'Venue': 'N/A'
                })
            else:
                for paper in publications:
                    title = paper.get('bib', {}).get('title', 'N/A')
                    year = paper.get('bib', {}).get('pub_year', 'N/A')
                    citation_count = paper.get('num_citations', 0)
                    venue = paper.get('bib', {}).get('venue', 'N/A')
                    writer.writerow({
                        'Professor': professor_name,
                        'Title': title,
                        'Year': year,
                        'Citations': citation_count,
                        'Venue': venue
                    })

    # Return the file path of the CSV
    return output_file




ny_professor_df = pd.read_csv('./professors_data_ny_schools.csv')
ny_professor_df['full_name'] = ny_professor_df['tFname'] + ' ' + ny_professor_df['tLname']
ny_professor_df
pnames =ny_professor_df['full_name']
pnames

# Run the function to start saving data progressively
professor_csv = fetch_research_data_bulk(pnames)

# Optional: load the CSV for review if needed
df = pd.read_csv(professor_csv)
df