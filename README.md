# YouTube Data Analysis Pipeline

YouTube Data Analysis Pipeline is a project designed to extract video analytics data from YouTube using its API, process it locally, and stream it into Kafka for further analysis using kSQLDB.

## Overview
This project fetches video data from a specified YouTube playlist using the YouTube Data API, processes the data to extract relevant metrics, and sends the formatted data to Kafka topics for real-time analytics.

## Setup
### Prerequisites
Before running this project, ensure you have the following installed and set up:

Docker

Python (3.x recommended)

Access to Google Cloud Platform (GCP) with YouTube Data API enabled

## Steps
### Clone the repository:

bash

git clone https://github.com/your_username/your_repository.git

cd your_repository

### Set up configuration:

Create a config/config.local file with your YouTube API credentials (API_KEY) and the target YouTube playlist ID (PLAYLIST_ID). 

Example:

[youtube]
API_KEY = your_youtube_api_key_here

PLAYLIST_ID = your_youtube_playlist_id_here


### Build and run Docker containers:

Run the following command to start Zookeeper, Kafka, Schema Registry, and kSQLDB containers using Docker Compose:

docker-compose up -d

### Install Python dependencies:

Use pip to install the required Python packages:

pip install -r requirements.txt

### Usage

To run the YouTube Data Analysis Pipeline:

### Execute the Python script:

python youtube_analysis.py(Your folder name.py)

This script fetches video data from the specified playlist, formats it, and publishes it to the youtube_videos Kafka topic.

### Monitor the pipeline:

Access Confluent Control Center at http://localhost:9021 to monitor Kafka topics and kSQLDB queries.


Use kSQLDB CLI or Control Center UI to perform real-time data analysis on the streamed YouTube data.



## Technologies Used

Python

Docker

Kafka

kSQLDB

GCP (Google Cloud Platform)

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests.

## License
This project is licensed under the GNU License.