
# Personalized News Aggregator

## Overview

This Personalized News Aggregator, developed by **Gaurvi Sood**, is an innovative application that provides users with a tailored news experience. By leveraging advanced data structures, AI technologies, and dynamic user interactions, this project showcases a comprehensive understanding of modern software development practices.

## Key Features

1. **Preference Management**: Utilizes hashmaps for efficient storage and retrieval of user preferences.
2. **Smart Article Distribution**: Implements a sophisticated normalization technique for fair distribution of articles across categories.
3. **AI-Powered Summaries**: Integrates with Groq API to generate character-styled news summaries.
4. **Interactive Web Interface**: Built with Streamlit for a responsive and user-friendly experience.
5. **Dynamic Content**: Fetches and updates news articles based on real-time user interactions.
6. **Persistent User Preferences**: Stores user preferences across sessions using JSON files.
7. **Multi-API Integration**: Combines News API for article fetching and Groq API for summary generation.

## Technical Highlights

- **Data Structures**: Efficient use of hashmaps for O(1) data access and retrieval.
- **Algorithms**: Custom algorithm for normalizing and distributing articles fairly.
- **API Integration**: Demonstrates proficiency in working with external APIs (News API and Groq API).
- **Web Development**: Showcases skills in creating interactive web applications using Streamlit.
- **AI Application**: Utilizes AI models for generating creative, character-based summaries.

## Installation

### Prerequisites
- Python 3.7 or higher
- [pip](https://pip.pypa.io/en/stable/installation/)

### Steps

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Gaurvi02/News-analyser-using-Hashmap.git
   cd News-analyser-using-Hashmap
   ```

2. **Create and activate a virtual environment:**
   
   - **Windows:**
     ```sh
     python -m venv myenv
     .\myenv\Scripts\activate
     ```

   - **MacOS/Linux:**
     ```sh
     python3 -m venv myenv
     source myenv/bin/activate
     ```

3. **Install the required libraries:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Update the API keys:**
   
   Open the `app.py` file and update the `GROQ_API_KEY` and `NEWS_API_KEY` with your own API keys:
   ```python
   GROQ_API_KEY = "YOUR_GROQ_API_KEY"
   NEWS_API_KEY = "YOUR_NEWS_API_KEY"
   ```

5. **Run the application:**
   ```sh
   streamlit run app.py
   ```

## How to Use

1. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).
2. Select your preferred news categories from the sidebar.
3. Click the "Fetch News" button to retrieve the latest articles based on your preferences.
4. Interact with the articles by liking or disliking them to refine your feed.
5. Click the "Generate Summary" button to enjoy a fun summary in the style of Harry Potter!

##Screenshots
<img width="1434" alt="1" src="https://github.com/Gaurvi02/News-analyser-using-Hashmap/assets/101133944/7f2e1486-0c77-4355-988c-2c4be85ab530">



## Project Structure

- `app.py`: Main application file containing the Streamlit web app and core logic.
- `requirements.txt`: List of Python dependencies.
- `preferences.txt`: JSON file for storing user preferences (generated upon first run).

## Future Enhancements

- Implement a heap-based structure for more advanced preference ranking.
- Expand character options for summary generation.
- Add more news sources and categories.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- News API for providing access to current news articles.
- Groq API for enabling AI-powered summary generation.
- Streamlit for simplifying web application development.

