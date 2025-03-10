from pybtex.database import parse_file
import yaml

# Load .bib file
bib_data = parse_file("publications.bib")

# Function to format authors
def format_authors(authors):
    formatted_authors = []
    for author in authors:
        # Extract first and last names
        first_name = " ".join(author.first_names)
        last_name = " ".join(author.last_names)
        formatted_authors.append(f"{first_name} {last_name}")
    return formatted_authors

# Convert to a list of publications grouped by year
publications_by_year = {}
for key, entry in bib_data.entries.items():
    # Extract and format authors
    authors = format_authors(entry.persons.get("author", []))
    
    # Create a paper entry
    paper = {
        "title": entry.fields.get("title", ""),
        "authors": authors,
        "journal": entry.fields.get("journal", ""),
        "doi": entry.fields.get("doi", ""),
    }
    
    # Get the year
    year = entry.fields.get("year", "")
    
    # Group papers by year
    if year not in publications_by_year:
        publications_by_year[year] = []
    publications_by_year[year].append(paper)

# Convert the dictionary to a list of years with papers
publications_list = []
for year, papers in publications_by_year.items():
    publications_list.append({
        "year": year,
        "papers": papers,
    })

# Save as YAML
with open("../data/publications.yaml", "w") as yaml_file:
    yaml.dump(publications_list, yaml_file, default_flow_style=False, sort_keys=False)

print("Conversion complete: publications.yaml created!")