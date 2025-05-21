import sys
import os
from urllib.parse import urlparse
import re

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# Import the Company class
from models.company import Company

# Create a simplified version of the functions we need
def extract_domain_name(url):
    """Extract the domain name from a URL."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    # Remove www. if present
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def normalize_url(url):
    """Normalize a URL to ensure consistent comparison."""
    if not url:
        return url

    # Add scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Parse the URL
    parsed_url = urlparse(url)

    # Normalize domain (remove www. if present)
    netloc = parsed_url.netloc
    if netloc.startswith("www."):
        netloc = netloc[4:]

    # Rebuild the URL with normalized domain and without trailing slash
    path = parsed_url.path
    if path.endswith("/"):
        path = path[:-1]

    # Rebuild the URL
    normalized = f"{parsed_url.scheme}://{netloc}{path}"

    # Add query and fragment if they exist
    if parsed_url.query:
        normalized += f"?{parsed_url.query}"
    if parsed_url.fragment:
        normalized += f"#{parsed_url.fragment}"

    return normalized

def get_company_name(url):
    """Get company name from domain."""
    domain = extract_domain_name(url)
    if not domain:  # Handle empty domain case
        return "Unknown Company"

    # Remove TLD and split by dots or hyphens
    name_parts = re.split(r"\.|-", domain)[0]
    # Capitalize words
    return (
        " ".join(
            word.capitalize() for word in re.split(r"(?=[A-Z])", name_parts) if word
        )
        or "Unknown Company"
    )  # Fallback if we can't extract a name

def create_company_from_data(client_data, fallback_url=None):
    """Create a Company object from client data."""
    # Step 1: Try to get the URL from client_data or use fallback_url
    url = client_data.get("website_url", fallback_url)
    print(f"Step 1: URL from data or fallback: {url}")
    
    # Step 2: Check if we have a URL
    if not url:
        print("Step 2: No URL found, returning None")
        return None

    # Step 3: Normalize the URL
    normalized_url = normalize_url(url)
    print(f"Step 3: Normalized URL: {normalized_url}")

    # Step 4: Get company name (from client_data or generate from URL)
    name = client_data.get("name")
    if not name:
        name = get_company_name(normalized_url)
        print(f"Step 4: Generated name from URL: {name}")
    else:
        print(f"Step 4: Using name from client data: {name}")

    # Step 5: Create and return the Company object
    company = Company(name=name, website_url=normalized_url)
    print(f"Step 5: Created company: {company}")
    return company

# Test cases
test_cases = [
    {
        "description": "Case 1: Complete client data",
        "client_data": {"name": "Acme Inc", "website_url": "www.acme.com"},
        "fallback_url": None
    },
    {
        "description": "Case 2: Missing name, has URL",
        "client_data": {"website_url": "example.com"},
        "fallback_url": None
    },
    {
        "description": "Case 3: Missing URL, has fallback",
        "client_data": {"name": "Backup Company"},
        "fallback_url": "backup.com"
    },
    {
        "description": "Case 4: Missing URL, no fallback",
        "client_data": {"name": "No URL Company"},
        "fallback_url": None
    },
    {
        "description": "Case 5: Empty client data, has fallback",
        "client_data": {},
        "fallback_url": "last-resort.com"
    },
    {
        "description": "Case 6: Empty client data, no fallback",
        "client_data": {},
        "fallback_url": None
    }
]

# Run the tests
for i, test in enumerate(test_cases):
    print(f"\n{'='*50}")
    print(f"TEST {i+1}: {test['description']}")
    print(f"{'='*50}")
    print(f"Client data: {test['client_data']}")
    print(f"Fallback URL: {test['fallback_url']}")
    print(f"{'-'*50}")
    
    result = create_company_from_data(test['client_data'], test['fallback_url'])
    
    print(f"{'-'*50}")
    if result:
        print(f"RESULT: Company created with name '{result.name}' and URL '{result.website_url}'")
    else:
        print("RESULT: No company created (None returned)")
