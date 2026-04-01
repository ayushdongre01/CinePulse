# CinePulse - Movie Recommender System

CinePulse is a full-stack movie recommendation project that combines:

- A FastAPI backend for data and recommendation endpoints
- A Streamlit frontend for an interactive user experience
- A TF-IDF content-based recommendation engine built from movie metadata
- TMDB API integration for live posters, movie details, trending feeds, and genre discovery

The app lets users browse popular and trending movies, search by title, view rich movie details, and get recommendations based on both local NLP similarity and TMDB genre-based discovery.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Run the Project](#run-the-project)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

## Project Overview

This project uses content-based filtering with TF-IDF vectors generated from movie text features such as:

- Overview
- Genres
- Tagline

These features are transformed into vectors using scikit-learn and stored as serialized artifacts:

- df.pkl
- indices.pkl
- tfidf.pkl
- tfidf_matrix.pkl

At runtime:

1. FastAPI loads these artifacts into memory.
2. Streamlit sends requests to FastAPI for search, details, and recommendations.
3. FastAPI combines local TF-IDF recommendations with TMDB metadata to enrich results with posters and details.

## Features

### User-facing Features

- Search movies by title using TMDB search
- Home feed categories: trending, popular, top rated, now playing, upcoming
- Movie detail page with:
  - Poster
  - Backdrop
  - Release date
  - Rating
  - Genres
  - Overview
- Hybrid recommendations:
  - Local TF-IDF similar movies
  - TMDB genre-based discovery
- Interactive and styled Streamlit UI

### Backend Features

- RESTful endpoints with FastAPI
- CORS enabled for frontend integration
- Safe TMDB request wrapper with error handling
- Startup loading for serialized recommender assets
- Recommendation APIs for:
  - TF-IDF only
  - Genre-based only
  - Combined bundle response

## How It Works

### 1. Data Preparation

Notebook workflow in movies.ipynb:

- Load and clean movies_metadata.csv
- Build combined text tags from overview + genres + tagline
- Apply text preprocessing (stopword removal, lemmatization, cleanup)
- Fit TF-IDF vectorizer
- Save artifacts as pickle files

### 2. Recommendation Logic

Given a movie title:

- Find title index from indices
- Compute similarity using TF-IDF matrix operations
- Rank similar titles by cosine-like score from sparse matrix multiplication
- Return top N titles

### 3. TMDB Enrichment

To improve UX, local recommendations are enriched by querying TMDB:

- Poster path
- Release date
- Vote average
- Movie ID and details

### 4. Frontend Experience

Streamlit frontend consumes backend endpoints for:

- Home feed cards
- Search suggestions and result grids
- Detail views
- Recommendation sections

## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- Streamlit
- Pandas
- NumPy
- SciPy
- scikit-learn
- httpx
- python-dotenv
- TMDB API

## Project Structure

```text
MovieRecommender/
|-- app.py                  # Streamlit frontend
|-- main.py                 # FastAPI backend
|-- movies.ipynb            # Data preprocessing and model artifact generation
|-- movies_metadata.csv     # Source movie metadata dataset
|-- requirements.txt        # Python dependencies
|-- df.pkl                  # Processed movie DataFrame
|-- indices.pkl             # Title to index map for recommendations
|-- tfidf.pkl               # Trained TF-IDF vectorizer
|-- tfidf_matrix.pkl        # Sparse TF-IDF matrix
|-- .env                    # Local environment variables (create manually)
|-- README.md
```

## Prerequisites

- Python 3.10 or later
- pip
- TMDB API key

Get your TMDB key from: https://www.themoviedb.org/settings/api

## Installation

1. Clone the repository and go to the project folder.

```bash
git clone <your-repo-url>
cd MovieRecommender
```

2. Create and activate a virtual environment.

Windows (cmd):

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root.

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

## Run the Project

You need two terminals.

### Terminal 1: Start FastAPI backend

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend URL:

- http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs

### Terminal 2: Start Streamlit frontend

```bash
streamlit run app.py
```

Frontend URL:

- http://localhost:8501

## Environment Variables

Create a .env file in project root:

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

Notes:

- The backend fails at startup if TMDB_API_KEY is missing.
- Keep your key private and do not commit .env.

## API Endpoints

Base URL: http://127.0.0.1:8000

### Health

- GET /health

Response:

```json
{"status": "ok"}
```

### Home Feed

- GET /home?category=popular&limit=24

Supported category values:

- trending
- popular
- top_rated
- now_playing
- upcoming

### Search Movies on TMDB

- GET /tmdb/search?query=avatar&page=1

Returns raw TMDB-style results list used by Streamlit for suggestions and grids.

### Movie Details

- GET /movie/id/{tmdb_id}

Example:

- GET /movie/id/19995

### Genre Recommendations

- GET /recommend/genre?tmdb_id=19995&limit=12

### TF-IDF Recommendations (Local)

- GET /recommend/tfidf?title=Avatar&top_n=10

### Combined Search Bundle

- GET /movie/search?query=Avatar&tfidf_top_n=12&genre_limit=12

Returns:

- Selected movie details
- TF-IDF recommendations enriched with TMDB cards
- Genre recommendation section

## Screenshots

### Home Page

![Home Page 1](https://github.com/ayushdongre01/CinePulse/blob/main/images/1.png)
![Home Page 2](https://github.com/ayushdongre01/CinePulse/blob/main/images/2.png)
![Home Page 3](https://github.com/ayushdongre01/CinePulse/blob/main/images/3.png)

### Search Results

![Search Results](https://github.com/ayushdongre01/CinePulse/blob/main/images/4.png)

### Movie Details

![Movie Details 1](https://github.com/ayushdongre01/CinePulse/blob/main/images/5.png)
![Movie Details 2](https://github.com/ayushdongre01/CinePulse/blob/main/images/6.png)

### Recommendations

![Recommendations 1](https://github.com/ayushdongre01/CinePulse/blob/main/images/7.png)
![Recommendations 2](https://github.com/ayushdongre01/CinePulse/blob/main/images/8.png)

## Troubleshooting

### TMDB key error at startup

Error example: TMDB_API_KEY missing

Fix:

- Ensure .env exists in project root
- Ensure key name is exactly TMDB_API_KEY
- Restart FastAPI server

### Streamlit cannot connect to backend

Fix:

- Ensure FastAPI is running on port 8000
- Verify API_BASE in app.py is http://127.0.0.1:8000

### Module import errors

Fix:

- Activate your virtual environment
- Reinstall dependencies using requirements.txt

### Slow first response

First request can be slower due to startup model loading and TMDB network round trips.

## Future Improvements

- Add robust unit and integration tests
- Improve API response model consistency
- Cache TMDB responses for faster repeated calls
- Add Docker support
- Add CI pipeline
- Add watchlist and user preferences
- Add optional semantic embeddings for better recommendations
