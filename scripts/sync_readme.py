
import os
import sys
from pathlib import Path

import markdown
import requests
from requests.auth import HTTPBasicAuth

base_url = os.environ["CONFLUENCE_BASE_URL"].rstrip("/")
email = os.environ["CONFLUENCE_EMAIL"]
api_token = os.environ["CONFLUENCE_API_TOKEN"]
page_id = os.environ["CONFLUENCE_PAGE_ID"]

readme_path = Path("README.md")

if not readme_path.is_file():
    sys.exit("README.md not found")

# Convert GitHub Markdown into HTML for Confluence storage.
readme_text = readme_path.read_text(encoding="utf-8")

html = markdown.markdown(
    readme_text,
    extensions=["tables", "fenced_code"]
)

auth = HTTPBasicAuth(email, api_token)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# Fetch the existing Confluence page and its current version.
page_url = f"{base_url}/wiki/api/v2/pages/{page_id}"

response = requests.get(
    page_url,
    params={"body-format": "storage"},
    headers=headers,
    auth=auth,
    timeout=30,
)
response.raise_for_status()

page = response.json()

# Replace the page body with the latest README content.
payload = {
    "id": str(page["id"]),
    "status": "current",
    "title": page["title"],
    "spaceId": str(page["spaceId"]),
    "body": {
        "representation": "storage",
        "value": html,
    },
    "version": {
        "number": page["version"]["number"] + 1,
        "message": "Synced from GitHub README.md",
    },
}

update_response = requests.put(
    page_url,
    json=payload,
    headers=headers,
    auth=auth,
    timeout=30,
)
update_response.raise_for_status()

print(
    f"Successfully synced README.md to Confluence page: "
    f"{page['title']} (ID: {page_id})"
)
