# SonicSherlock: Audio Recognition System

SonicSherlock is a Shazam-like audio recognition system built using Python, Librosa, FastAPI, Gradio, and PostgreSQL. It identifies songs from audio snippets by creating and matching audio fingerprints.

## Demo Video

[![SonicSherlock Demo](./assets/demo-thumbnail.png)](https://youtu.be/SC_rsnGM6ak)
[Watch Demo on YouTube](https://youtu.be/SC_rsnGM6ak)

## Table of Contents

- [SonicSherlock: Audio Recognition System](#sonicsherlock-audio-recognition-system)
  - [Demo Video](#demo-video)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [PostgreSQL Setup](#postgresql-setup)
    - [Create a Virtual Environment](#create-a-virtual-environment)
    - [Install Dependencies](#install-dependencies)
    - [Configure Environment Variables](#configure-environment-variables)
  - [Running the Application](#running-the-application)
    - [Start FastAPI API](#start-fastapi-api)
    - [Start Gradio Interface](#start-gradio-interface)
  - [Adding Songs to the Database](#adding-songs-to-the-database)
  - [Database Management](#database-management)
    - [Listing Database Contents](#listing-database-contents)
    - [Clearing the Database](#clearing-the-database)
    - [Resetting Song ID Sequence](#resetting-song-id-sequence)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python**: 3.7 or higher ([Download](https://www.python.org/downloads/))
- **pip**: Python package installer (included with Python)
- **PostgreSQL**: Database server ([Download](https://www.postgresql.org/download/))

---

## Setup

1. **Download or Clone the Repository**: Obtain the SonicSherlock codebase.
2. **Create Project Directory**: If downloaded manually, create a directory for the project and place all files inside it.

### PostgreSQL Setup

1. **Install PostgreSQL**: Follow the instructions for your operating system on the [official PostgreSQL website](https://www.postgresql.org/download/).
2. **Start PostgreSQL Server**: Ensure the server is running.
3. **Create a Database and User**:
   - Open a terminal and connect to the `postgres` user:
     ```bash
     sudo -u postgres psql
     ```
   - Inside the `psql` shell, create a new user and database (replace `your_user` and `your_password` with your desired credentials):
     ```sql
     CREATE USER your_user WITH PASSWORD 'your_password';
     CREATE DATABASE sonic_sherlock OWNER your_user;
     GRANT ALL PRIVILEGES ON DATABASE sonic_sherlock TO your_user;
     \q
     ```

### Create a Virtual Environment

Using a virtual environment is recommended to isolate project dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

Navigate to the root project directory (where `requirements.txt` is located) and run:

```bash
pip3 install -r requirements.txt
```

This installs all required Python packages listed in `requirements.txt`.

### Configure Environment Variables

Create a `.env` file in the root directory and add the database URL:

```
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/sonic_sherlock
```

- Replace `your_user` and `your_password` with the credentials from the PostgreSQL setup.
- **Important**: Never commit your `.env` file to public repositories to protect your credentials.

---

## Running the Application

SonicSherlock consists of a FastAPI backend and a Gradio frontend.

### Start FastAPI API

In a terminal, activate the virtual environment, navigate to the `sonic_sherlock` directory, and run:

```bash
uvicorn api.app:app --reload
```

The `--reload` flag restarts the server automatically when code changes are detected.

### Start Gradio Interface

In a new terminal, activate the virtual environment, navigate to the `sonic_sherlock/api` directory, and run:

```bash
python sonic_sherlock/api/gradio_app.py
```

Once both the FastAPI API and Gradio interface are running, access the Gradio interface at [http://localhost:8000/](http://localhost:8000/) in your web browser.

---

## Adding Songs to the Database

1. Place audio files in the `songs/` directory. Filenames must follow the format: `<artist name> - <song name>.mp3`.
2. Run the `add_songs.py` script:

```bash
python3 sonic_sherlock/add_songs.py
```

This script extracts the artist and title from filenames, adds songs to the database, and generates audio fingerprints.

---

## Database Management

### Listing Database Contents

Connect to the `sonic_sherlock` database using `psql`:

```bash
psql -U your_user -d sonic_sherlock
```

Run these SQL queries to view the contents:

```sql
SELECT * FROM songs;
SELECT * FROM fingerprints;
```

### Clearing the Database

To delete all songs and fingerprints, connect to the database:

```bash
psql -U your_user -d sonic_sherlock
```

Then execute:

```sql
TRUNCATE TABLE fingerprints RESTART IDENTITY CASCADE;
TRUNCATE TABLE songs RESTART IDENTITY CASCADE;
```

**Warning**: This permanently deletes all data in the tables.

### Resetting Song ID Sequence

If the song ID sequence doesn’t start from 1 after clearing the database, reset it:

```bash
psql -U your_user -d sonic_sherlock
```

Inside the `psql` shell:

```sql
ALTER SEQUENCE songs_id_seq RESTART WITH 1;
```

---
