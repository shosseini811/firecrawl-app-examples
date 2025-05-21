import re
from urllib.parse import urlparse

# Helper function: extract domain name from URL
def extract_domain_name(url):
    """Extract the domain name from a URL."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    # Remove www. if present
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

# Main function: get company name from URL
def get_company_name(url):
    """Get company name from domain."""
    # Step 1: Extract the domain
    domain = extract_domain_name(url)
    
    # Step 2: Handle empty domain case
    if not domain:
        return "Unknown Company"

    # Step 3: Remove TLD and split by dots or hyphens
    print(f"  Domain: {domain}")
    name_parts = re.split(r"\.|-", domain)[0]
    print(f"  Main part: {name_parts}")
    
    # Step 4: Split by capital letters (for camelCase domains)
    words = re.split(r"(?=[A-Z])", name_parts)
    print(f"  Split by capitals: {words}")
    
    # Step 5: Capitalize each word and join with spaces
    capitalized = [word.capitalize() for word in words if word]
    print(f"  Capitalized: {capitalized}")
    
    # Step 6: Join words or use fallback
    result = " ".join(capitalized) or "Unknown Company"
    return result

# Test with various URLs
test_urls = [
    "https://amazon.com",
    "https://www.google.com",
    "http://myCompany-site.co.uk",
    "https://acme-corp.com",
    "https://facebook.com",
    "https://airBnB.com",
    "https://example-site.io",
    "https://micro-soft.com",
    "https://apple.com",
    ""  # Empty URL to test fallback
]

# Run the tests
print("Testing get_company_name function:\n")
for url in test_urls:
    print(f"URL: {url}")
    company_name = get_company_name(url)
    print(f"Company name: {company_name}")
    print("-" * 40)
