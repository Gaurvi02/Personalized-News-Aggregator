import heapq
import requests
import streamlit as st
from groq import Groq
import json
import math

# Groq API key
GROQ_API_KEY = "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"
LLAMA_MODEL = "llama3-70b-8192"

# Default character for summary
DEFAULT_CHARACTER = "News Reporter"

# News API key
NEWS_API_KEY = "395bd6703d534c759c1172ea087291e3"

# News categories
categories = [
    "business", "entertainment", "general", "health", "science", 
    "sports", "technology"
]

# File to store preferences
PREFERENCES_FILE = "preferences.txt"

# Total number of articles to fetch
TOTAL_ARTICLES = 20

# Initialize the preference dictionary in session state
if 'preferences' not in st.session_state:
    try:
        with open(PREFERENCES_FILE, 'r') as f:
            st.session_state.preferences = json.load(f)
    except FileNotFoundError:
        st.session_state.preferences = {category: 0 for category in categories}

def save_preferences():
    with open(PREFERENCES_FILE, 'w') as f:
        json.dump(st.session_state.preferences, f)

def get_user_preferences():
    st.header("Choose your news preferences")
    preferences = []
    for category in categories:
        # When a user selects a category, increase its value in preferences
        if st.checkbox(category.capitalize(), key=f"checkbox_{category}"):
            st.session_state.preferences[category] += 1
            preferences.append(category)
    return preferences

def distribute_articles(preferences, total_articles):
    # Filter out categories with non-positive preferences
    filtered_prefs = {k: v for k, v in preferences.items() if v > 0}
    if not filtered_prefs:
        return {k: 0 for k in preferences}

    # Normalize the preferences to be non-negative
    min_pref = min(filtered_prefs.values())
    normalized_prefs = {k: v - min_pref + 1 for k, v in filtered_prefs.items()}

    # Calculate the sum of the normalized preferences
    total_prefs = sum(normalized_prefs.values())

    # Calculate the number of articles for each category based on normalized preferences
    category_articles = {k: (v / total_prefs) * total_articles for k, v in normalized_prefs.items()}

    # Round the number of articles and handle rounding issues
    rounded_articles = {k: math.floor(v) for k, v in category_articles.items()}

    # Calculate how many more articles we need to distribute due to rounding down
    remaining_articles = total_articles - sum(rounded_articles.values())

    # Distribute the remaining articles to the categories with the highest fractional part
    fractional_parts = {k: v - math.floor(v) for k, v in category_articles.items()}
    for k in sorted(fractional_parts, key=fractional_parts.get, reverse=True):
        if remaining_articles <= 0:
            break
        rounded_articles[k] += 1
        remaining_articles -= 1

    # Include zero or negative preference categories in the result with 0 articles
    final_articles = {k: rounded_articles.get(k, 0) for k in preferences}
    return final_articles

def fetch_news(api_key, preferences):
    article_distribution = distribute_articles(preferences, TOTAL_ARTICLES)
    news = []
    for category, article_count in article_distribution.items():
        if article_count > 0:
            response = requests.get(
                f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={api_key}&language=en&pageSize={article_count}"
            )
            response.raise_for_status()
            data = response.json()
            for article in data.get("articles", []):
                if article.get("title") and article.get("url"):
                    news.append({
                        "title": article["title"],
                        "description": article.get("description", "No description available."),
                        "url": article["url"],
                        "category": category
                    })
    return news

def display_news(news):
    for i, article in enumerate(news):
        col1, col2 = st.columns([9, 1])
        with col1:
            st.write(f"### {article['title']}")
            st.write(f"**Category:** {article['category'].capitalize()}")
            st.write(article['description'])
            st.write(f"[Read more]({article['url']})")
        with col2:
            if st.button("👍", key=f"like_{i}"):
                update_preference(article['category'], 1)
            if st.button("👎", key=f"dislike_{i}"):
                update_preference(article['category'], -1)
        st.write("---")

def update_preference(category, value):
    st.session_state.preferences[category] += value
    save_preferences()
    st.experimental_rerun()

def get_chat_response(news_articles, character):
    client = Groq(api_key=GROQ_API_KEY)
    messages = [
        {
            "role": "system",
            "content": (f"You are an expert news summarizer. I will provide you with news articles, you have to Summarize them in conversational paragraphs like how {character} would say this. Keeping coherent and concise is key. Also have a bit of fun with it!")
        },
        {"role": "user", "content": news_articles}
    ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=LLAMA_MODEL,
        temperature=0.7,
        max_tokens=1024,
        top_p=1
    )
    return chat_completion.choices[0].message.content

def main():
    st.title("Personalized News Feed")
    
    # Sidebar content
    st.sidebar.title("Welcome to the Personalized News Feed!")
    st.sidebar.header("About This Project")
    st.sidebar.write("""
    This application, developed by **Gaurvi Sood**, brings you a personalized news experience:

    1. **Select Categories**: Choose your preferred news categories.
    2. **Fetch News**: Get the latest articles based on your preferences.
    3. **Interact**: Like or dislike articles to refine your feed.
    4. **AI Summary**: Enjoy a fun summary in the style of your favorite character!

    Your interactions help tailor the news to your interests. The more you use it, the better it gets!
    """)
    
    user_preferences = get_user_preferences()
    
    if 'news' not in st.session_state:
        st.session_state.news = []
    
    if st.button("Fetch News"):
        if not user_preferences:
            st.warning("Please select at least one category.")
        else:
            st.write(f"Your preferences: {', '.join(user_preferences)}")
            
            # Fetch news based on preferences
            st.session_state.news = fetch_news(NEWS_API_KEY, st.session_state.preferences)
    
    if st.session_state.news:
        st.subheader("Your personalized news feed:")
        display_news(st.session_state.news)
        
        collected_news = "\n\n".join([f"Title: {article['title']}\nDescription: {article['description']}" for article in st.session_state.news])
        
        # User input for character
        character = st.text_input("Enter a character for the summary:", DEFAULT_CHARACTER)
        
        # Get the chat response
        if st.button("Generate Summary"):
            with st.spinner(f"Generating summary in the style of {character}..."):
                chat_response = get_chat_response(collected_news, character)
            
            st.subheader(f"Summary in the style of {character}:")
            st.write(chat_response)

if __name__ == "__main__":
    main()
