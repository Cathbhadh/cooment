import streamlit as st
import requests
from requests.exceptions import RequestException

# Function to fetch comments for a given post UUID
def fetch_comments(post_uuid, max_retries=3, timeout=30):
    response = requests.get(url)
    if response.status_code == 200:
        comments = response.json()["comments"]
        return comments
    else:
        return []


# Function to fetch post UUIDs for a given user ID
def fetch_post_uuids(user_id, max_retries=3, timeout=30):
    url = f"https://api.yodayo.com/v1/users/{user_id}/posts?offset=0&limit=500&width=600&include_nsfw=true"
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(url, timeout=timeout, stream=True)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and "posts" in data:
                posts = data["posts"]
                uuids = [post["uuid"] for post in posts]
                return uuids
            else:
                st.error(f"Unexpected response structure: {data}")
                return []
        except RequestException as e:
            retries += 1
            if retries == max_retries:
                st.error(f"Failed to fetch post UUIDs after {max_retries} retries. Error: {str(e)}")
                return []

    return []




# Streamlit app
def app():
    st.title("Yodayo Comment Viewer")

    # Get user ID from the user
    user_id = st.text_input("Enter User ID", value="0b56f7c9-b80a-4b3e-9a9f-36b038898b1b")

    if user_id:
        # Fetch post UUIDs for the user
        post_uuids = fetch_post_uuids(user_id)

        # Display comments for each post
        for post_uuid in post_uuids:
            comments = fetch_comments(post_uuid)

            if comments:
                st.subheader(f"Comments for Post {post_uuid}")
                for comment in comments:
                    st.write(f"**{comment['profile']['name']}** ({comment['created_at']})")
                    st.write(comment["text"])
                    st.write("---")
            else:
                st.write(f"No comments found for Post {post_uuid}")

if __name__ == "__main__":
    app()
