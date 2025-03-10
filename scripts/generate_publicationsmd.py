import re
from pybtex.database import parse_file

# Load the .bib file
bib_data = parse_file("publications.bib")

# Define your name in both formats (to catch both variations)
your_name_variations = [r"\\textbf\{Zahn, Einara\}", r"\\textbf\{Einara Zahn\}"]
your_name_html = "<b>Einara Zahn</b>"

# Function to clean up LaTeX commands and replace \textbf{} with <b>, CO$_2$ to CO<sub>2</sub>, etc.
def clean_latex(text):
    """Removes LaTeX commands and replaces LaTeX-specific formatting with HTML equivalents."""
    # Replace \textbf{} with <b>
    text = re.sub(r"\\textbf\{(.*?)\}", r"**\1**", text)
    # Remove \hack{\break} or similar
    text = re.sub(r"\\hack\{.*?\}", "", text)
    # Remove \break if present
    text = re.sub(r"\\break", "", text)
    
    # Handle LaTeX math (e.g., CO$_2$ to CO<sub>2</sub>)
    text = re.sub(r"\$(.*?)\$", lambda m: m.group(1).replace("_", "<sub>").replace("$", "</sub>"), text)
    
    return text

# Organize publications by year and separate submitted papers
publications_by_year = {}
submitted_papers = []

for entry in bib_data.entries.values():
    year = entry.fields.get("year", "Unknown")
    title = clean_latex(entry.fields.get("title", "No Title"))
    journal = clean_latex(entry.fields.get("journal", entry.fields.get("booktitle", "Unknown Journal")))
    doi = entry.fields.get("doi", None)  # DOI if available
    url = entry.fields.get("url", None)  # URL if available
    keywords = entry.fields.get("keywords", "")

    # Get authors and format names
    authors = []
    for person in entry.persons["author"]:
        full_name = " ".join(person.first_names + person.last_names)
        full_name = clean_latex(full_name)  # Clean LaTeX artifacts

        # Ensure your name appears in **bold**
        for pattern in your_name_variations:
            full_name = re.sub(pattern, your_name_html, full_name)

        authors.append(full_name)

    # Check if the paper is marked as "submitted"
    if "submitted" in keywords.lower():
        citation = f"{', '.join(authors)}. *{title}*. *{journal}*."
        
        # Handle DOI (correctly adding the link)
        if doi:
            if not doi.startswith("https://doi.org/"):
                citation += f' <a href="https://doi.org/{doi}" target="_blank">https://doi.org/{doi}</a>'
            else:
                citation += f' <a href="{doi}" target="_blank">{doi}</a>'
        
        # Handle URL if no DOI
        elif url:
            citation += f' <a href="{url}" target="_blank">{url}</a>'
        
        submitted_papers.append(citation)
        
    elif "book" in keywords.lower():
        continue
    else:
        if year not in publications_by_year:
            publications_by_year[year] = []

        # Create citation string
        citation = f"{', '.join(authors)}. *{title}*. *{journal}*."
        
        # Handle DOI (correctly adding the link)
        if doi:
            if not doi.startswith("https://doi.org/"):
                citation += f' <a href="https://doi.org/{doi}" target="_blank">https://doi.org/{doi}</a>'
            else:
                citation += f' <a href="{doi}" target="_blank">{doi}</a>'
        
        # Handle URL if no DOI
        elif url:
            citation += f' <a href="{url}" target="_blank">{url}</a>'
        
        publications_by_year[year].append(citation)

# Generate Markdown content
md_content = """---
title: "Publications"
date: 2025-03-02
type: "page"
---

<div style="text-align: center;">
  # Publications
</div>

"""

# Add submitted papers first
if submitted_papers:
    md_content += "## Submitted Papers\n\n"
    for citation in submitted_papers:
        md_content += f"- {citation}\n\n"  # Add a newline after each publication for extra space

md_content += "## Published Papers\n\n"
# Sort years in descending order
for year in sorted(publications_by_year.keys(), reverse=True):
    md_content += f"## {year}\n\n"
    for citation in publications_by_year[year]:
        md_content += f"- {citation}\n\n"  # Add a newline after each publication for extra space

# Write to the Hugo content file
with open("../content/en/publications.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("publications.md updated successfully!")
