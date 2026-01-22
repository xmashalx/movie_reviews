# 🎬 Movie Review Site

A full-stack movie review platform that allows users to browse movies, read reviews, and share their own opinions. Built with Flask and PostgreSQL, featuring an ETL pipeline that fetches movie data from The Movie Database (TMDB) API.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [ETL Pipeline](#etl-pipeline)

## ✨ Features

### User Features
- **Browse Movies** - View all movies with pagination
- **Search & Filter** - Search movies by title, filter by genre, director, or studio
- **Movie Details** - View detailed information including synopsis, budget, revenue, and reviews
- **User Profiles** - View user profiles and their review history
- **User Directory** - Browse all registered users

### Authentication
- **User Registration** - Create an account with username, password, and bio
- **Login/Logout** - Secure session-based authentication
- **Password Hashing** - Passwords securely hashed with bcrypt

### Reviews
- **Post Reviews** - Logged-in users can write reviews with ratings
- **Delete Reviews** - Users can remove their own reviews
- **View Reviews** - See reviews on movie pages and user profiles

## 📁 Project Structure

```
review_site/
├── api/                    # Flask web application
│   ├── api.py              # Main Flask routes and application
│   ├── database.py         # Database connection and queries
│   ├── requirements.txt    # Python dependencies for API
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # Application styles
│   │   └── js/             # JavaScript files
│   └── templates/          # Jinja2 HTML templates
│       ├── home.html       # Homepage with movie listings
│       ├── login.html      # Login form
│       ├── register.html   # Registration form
│       ├── movie_detail.html   # Individual movie page
│       ├── user_profile.html   # User profile page
│       └── users.html      # User directory
├── movie_pipeline/         # ETL pipeline for movie data
│   ├── main.py             # Pipeline orchestration
│   ├── extract.py          # Data extraction from TMDB API
│   ├── transform.py        # Data transformation
│   ├── load.py             # Data loading to PostgreSQL
│   └── requirements.txt    # Python dependencies for pipeline
├── reviewdb/               # Database scripts
│   ├── schema.sql          # Table definitions
│   ├── create_database.sql # Database creation script
│   └── insert.sql          # Sample data insertion
├── docs/
│   └── user_stories.md     # User stories documentation
└── README.md
```

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, Jinja2 Templates
- **External API**: [The Movie Database (TMDB)](https://www.themoviedb.org/)
- **Caching**: Flask-Caching
- **Authentication**: bcrypt for password hashing

## 📦 Prerequisites

- Python 3.8+
- PostgreSQL
- TMDB API Key (get one at [themoviedb.org](https://www.themoviedb.org/settings/api))

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd review_site
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   # For the API
   pip install -r api/requirements.txt
   
   # For the ETL pipeline
   pip install -r movie_pipeline/requirements.txt
   ```

## 🔐 Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_IP=localhost
DATABASE_PORT=5432
DATABASE_NAME=reviews
DATABASE_USERNAME=your_username
DATABASE_PASSWORD=your_password

# Flask Configuration
SECRET_KEY=your_secret_key_here

# TMDB API (for ETL pipeline)
API_KEY=your_tmdb_api_key
```

## 🗄 Database Setup

1. **Create the database**
   ```bash
   psql -U postgres -f reviewdb/create_database.sql
   ```

2. **Create tables**
   ```bash
   psql -d reviews -f reviewdb/schema.sql
   ```

3. **Insert sample data (optional)**
   ```bash
   psql -d reviews -f reviewdb/insert.sql
   ```

### Database Schema

| Table | Description |
|-------|-------------|
| `users` | User accounts (username, bio, password) |
| `movie` | Movie information (title, release date, score, overview, budget, revenue) |
| `director` | Director names |
| `studio` | Production studio names |
| `genre` | Movie genres |
| `movie_genres` | Many-to-many relationship between movies and genres |
| `review` | User reviews with ratings and text |

## ▶️ Running the Application

1. **Start the Flask server**
   ```bash
   cd api
   python api.py
   ```

2. **Access the application**
   
   Open your browser and navigate to `http://localhost:80`

## 🔄 ETL Pipeline

The movie pipeline fetches data from TMDB and populates your database with movie information.

### Full Run (Popular + Top Rated Movies)
```bash
cd movie_pipeline
python main.py
```
This fetches ~5000 unique movies from popular and top-rated lists.

### Daily Run (Now Playing Movies)
```bash
cd movie_pipeline
python main.py --daily
```
This fetches currently playing movies for daily updates.

### Pipeline Stages

1. **Extract** - Fetches movie data from TMDB API including genres, credits, and details
2. **Transform** - Processes and normalizes data for database insertion
3. **Load** - Inserts transformed data into PostgreSQL

## 📝 API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Homepage with movie listings |
| `/movie/<id>` | GET | Movie detail page |
| `/movie/<id>/review` | POST | Submit a review |
| `/users` | GET | List all users |
| `/user/<id>` | GET | User profile page |
| `/review/<id>/delete` | POST | Delete a review |
| `/register` | GET/POST | User registration |
| `/login` | GET/POST | User login |
| `/logout` | GET | User logout |

## 📄 License

This project is for educational purposes.

