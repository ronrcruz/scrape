import requests
import streamlit as st
import json

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
            if "com" in thread and keyword.lower() in thread["com"].lower():
                links.append(f"https://boards.4chan.org/gif/thread/{thread['no']}")
                links_found = True
    if not links_found:
        links.append("No links found")
    return links

def main():
    # Ask the user for a keyword
    keyword = st.text_input("Enter a keyword:")

    # If a keyword is entered, scrape 4chan with the given keyword
    if keyword:
        links = scrape_4chan(keyword)

        # Display the links
        for link in links:
            if link != "No links found":
                st.markdown(f"[Thread]({link})")
            else:
                st.write("No links found")

if __name__ == "__main__":
    main()
