import requests
import json
import pandas as pd
import streamlit as st

def get_keyword_suggestions(keyword, max_suggestions=100):
    """
    Fetch keyword suggestions from the Google Suggest API.
    
    Args:
        keyword (str): The keyword to search for.
        max_suggestions (int): The maximum number of suggestions to fetch.
        
    Returns:
        list: A list of keyword suggestions.
    """
    keywords = [keyword]
    url = f"http://suggestqueries.google.com/complete/search?output=firefox&q={keyword}"
    response = requests.get(url, verify=False)
    suggestions = json.loads(response.text)
    
    for word in suggestions[1]:
        keywords.append(word)
        if len(keywords) >= max_suggestions:
            break
    
    return keywords

def clean_keywords(keywords, original_keyword):
    """
    Clean and filter the list of keywords.
    
    Args:
        keywords (list): The list of keywords to clean.
        original_keyword (str): The original keyword used to search.
        
    Returns:
        pandas.DataFrame: A DataFrame containing the cleaned keywords.
    """
    keywords = list(dict.fromkeys(keywords))
    new_list = [word for word in keywords if all(val in word for val in original_keyword.split())]
    df = pd.DataFrame(new_list, columns=['Keywords'])
    return df

def main():
    st.title("Keyword Suggestion Tool")
    
    keyword = st.text_input("Enter your keyword:", "")
    
    if st.button("Generate Keywords"):
        try:
            keywords = get_keyword_suggestions(keyword)
            df = clean_keywords(keywords, keyword)
            st.download_button(
                label
