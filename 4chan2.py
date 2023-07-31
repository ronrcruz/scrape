
import requests
import streamlit as st
import json
from PIL import Image
from io import BytesIO

def scrape_4chan(keyword):
    # Make a request to the website
    url = "https://a.4cdn.org/gif/catalog.json"
    r = requests.get(url)
    r_json = r.json()

    # Loop through threads, append link if keyword is found
    links_found = False
    links = []
    for page in r_json:
        for thread in page["threads"]:
            subject = thread.get("sub", "")
            # If the keyword is in the subject
            if keyword.lower() in subject.lower():
                link = f"https://boards.4chan.org/gif/thread/{thread['no']}"
                # Get the thumbnail URL
                thumbnail_url = f"http://i.4cdn.org/gif/{thread['tim']}s.jpg"  # use '.jpg' for thumbnails
                links.append((subject if subject else "No subject", link, thumbnail_url))
                links_found = True
    if not links_found:
        links.append(("No links found", "", ""))  # Add an empty string as the link and thumbnail_url
    return links

def main():
    # Ask the user for a keyword
    keyword = st.text_input("Enter a keyword:")

    # If a keyword is entered, scrape 4chan with the given keyword
    if keyword:
        links = scrape_4chan(keyword)

        # Display the links
        for subject, link, thumbnail_url in links:
            if link:  # If link is not empty
                response = requests.get(thumbnail_url)
                img = Image.open(BytesIO(response.content))
                st.image(img)  # Display the thumbnail
                st.markdown(f"[{subject}]({link})")
            else:
                st.write(subject)  # If link is empty, write the subject only


if __name__ == "__main__":
    main()
