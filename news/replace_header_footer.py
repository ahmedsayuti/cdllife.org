import requests
from bs4 import BeautifulSoup

# --- Configuration ---
LIVE_URL = "https://cdllife.com/news/"
LOCAL_FILE = "index_copy.html"      # your existing file
OUTPUT_FILE = "index_updated.html"   # where the result will be saved

# --- 1. Fetch the live page ---
print("Fetching live page...")
response = requests.get(LIVE_URL, headers={"User-Agent": "Mozilla/5.0"})
response.raise_for_status()
live_soup = BeautifulSoup(response.text, "html.parser")

# --- 2. Extract header and footer from live page ---
# Based on the structure of your provided HTML, the header is inside:
# <div class="td-header-template-wrap" style="position: relative">
# and the footer inside:
# <div class="td-footer-template-wrap" style="position: relative">

header_wrap = live_soup.find("div", class_="td-header-template-wrap")
footer_wrap = live_soup.find("div", class_="td-footer-template-wrap")

if not header_wrap or not footer_wrap:
    print("Could not locate header/footer on the live page. Exiting.")
    print("Header found:", header_wrap is not None)
    print("Footer found:", footer_wrap is not None)
    exit(1)

# Convert to string for replacement
new_header = str(header_wrap)
new_footer = str(footer_wrap)

# --- 3. Read your local HTML file ---
with open(LOCAL_FILE, "r", encoding="utf-8") as f:
    local_html = f.read()

local_soup = BeautifulSoup(local_html, "html.parser")

# --- 4. Locate the old header and footer in your local file ---
old_header_wrap = local_soup.find("div", class_="td-header-template-wrap")
old_footer_wrap = local_soup.find("div", class_="td-footer-template-wrap")

if not old_header_wrap or not old_footer_wrap:
    print("Could not locate header/footer in the local file. Exiting.")
    exit(1)

# --- 5. Replace them with the live versions ---
old_header_wrap.replace_with(BeautifulSoup(new_header, "html.parser"))
old_footer_wrap.replace_with(BeautifulSoup(new_footer, "html.parser"))

# --- 6. Save the result ---
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(str(local_soup))

print(f"Done! Updated file saved as: {OUTPUT_FILE}")