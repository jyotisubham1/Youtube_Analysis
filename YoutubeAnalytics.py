import json
import logging
import requests
from kafka import KafkaProducer
from constants import YOUTUBE_API_KEY, PLAYLIST_ID

# Function to fetch a single page of data from YouTube API
def fetch_page(url, parameters, page_token=None):
    # Merge API key and page token with the provided parameters
    params = {**parameters, 'key': YOUTUBE_API_KEY}
    if page_token:
        params['pageToken'] = page_token

    # Send GET request to the specified URL with the parameters
    response = requests.get(url, params=params)
    
    # Parse the JSON response
    payload = json.loads(response.text)
    return payload

# Generator function to fetch all pages of data from YouTube API
def fetch_page_lists(url, parameters, page_token=None):
    while True:
        # Fetch a single page
        payload = fetch_page(url, parameters, page_token)
        
        # Yield each item in the page
        yield from payload['items']
        
        # Get the token for the next page
        page_token = payload.get('nextPageToken')
        if page_token is None:
            break

def format_response(video):
    # Extract relevant information from the video data
    video_res = {
        'TITEL': video['snippet']['title'],  # Corrected to 'TITEL'
        'LIKES': int(video['statistics'].get('likeCount', 0)),
        'COMMENTS': int(video['statistics'].get('commentCount', 0)),
        'VIEWS': int(video['statistics'].get('viewCount', 0)),
        'FAVOURITES': int(video['statistics'].get('favoriteCount', 0)),  # Corrected to 'FAVOURITES'
        'THUMBNAIL': video['snippet']['thumbnails']['default']['url']
    }
    return video_res


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize Kafka producer
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    
    # Fetch video items from the playlist
    for video_item in fetch_page_lists(
            "https://www.googleapis.com/youtube/v3/playlistItems",
            {'playlistId': PLAYLIST_ID, 'part': 'snippet,contentDetails'}):
        
        # Extract video ID from the video item
        video_id = video_item['contentDetails']['videoId']
        
        # Fetch detailed information for the video
        for video in fetch_page_lists(
                "https://www.googleapis.com/youtube/v3/videos",
                {'id': video_id, 'part': 'snippet,statistics'}):
            
            # Format the video data
            formatted_video = format_response(video)
            
            # Send the formatted video data to Kafka topic
            producer.send('youtube_videos', json.dumps(formatted_video).encode('utf-8'), key=video_id.encode('utf-8'))
            
            # Print the title of the video sent
            print('Sent:', video['snippet']['title'])
