from urllib.parse import urlparse

# This is a standalone version of the normalize_url function from ClientScraper
def normalize_url(url):
    """
    Normalize a URL to ensure consistent comparison.

    Handles variations like:
    - Adding scheme if missing
    - Normalizes domain with or without www
    - Removes trailing slash
    """
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

# Example URLs to test
urls = [
    "www.example.com/page/",
    "http://www.example.com/page/",
    "https://example.com/page/",
    "example.com/page",
    "https://example.com/page/?query=1#frag",
    ""
]

for url in urls:
    normalized = normalize_url(url)
    print(f"Original: {url}")
    print(f"Normalized: {normalized}")
    print("---")