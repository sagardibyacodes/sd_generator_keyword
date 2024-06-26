import requests
import json
import pandas as pd
import streamlit as st

def api_call(keyword):
    keywords = [keyword.lower()]
    url = "http://suggestqueries.google.com/complete/search?output=firefox&q=" + keyword.lower()
    
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        suggestions = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        st.error(f"Error making API request: {e}")
        return pd.DataFrame()
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON response: {e}")
        return pd.DataFrame()
    
    for word in suggestions[1]:
        keywords.append(word.lower())
        
    prefixes(keyword.lower(), keywords)
    suffixes(keyword.lower(), keywords)
    numbers(keyword.lower(), keywords)
    get_more(keyword.lower(), keywords)
    df = clean_df(keywords, keyword.lower())
    
    return df

def prefixes(keyword, keywords):
    prefixes = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','y','x','y','z','how','which','why','where','who','when','are','what']
    
    for prefix in prefixes:
        try:
            url = "http://suggestqueries.google.com/complete/search?output=firefox&q=" + prefix + " " + keyword 
            response = requests.get(url, verify=False)
            response.raise_for_status()
            suggestions = json.loads(response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"Error making API request: {e}")
            continue
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON response: {e}")
            continue
        
        kws = suggestions[1]
        length = len(kws)
        
        for n in range(length):
            keywords.append(kws[n].lower())

def suffixes(keyword, keywords):
    suffixes =['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','y','x','y','z','like','for','without','with','versus','vs','to','near','except','has']
       
    for suffix in suffixes:
        try:
            url = "http://suggestqueries.google.com/complete/search?output=firefox&q=" + keyword + " " + suffix 
            response = requests.get(url, verify=False)
            response.raise_for_status()
            suggestions = json.loads(response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"Error making API request: {e}")
            continue
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON response: {e}")
            continue
        
        kws = suggestions[1]
        length = len(kws)
        
        for n in range(length):
            keywords.append(kws[n].lower())

def numbers(keyword, keywords):
    for num in range(0,10):
        try:
            url = "http://suggestqueries.google.com/complete/search?output=firefox&q=" + keyword + " " + str(num)
            response = requests.get(url, verify=False)
            response.raise_for_status()
            suggestions = json.loads(response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"Error making API request: {e}")
            continue
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON response: {e}")
            continue
        
        kws = suggestions[1]
        length = len(kws)
        
        for n in range(length):
            keywords.append(kws[n].lower())

def get_more(keyword, keywords):
    for i in keywords:
        try:
            url = "http://suggestqueries.google.com/complete/search?output=firefox&q=" + i
            response = requests.get(url, verify=False)
            response.raise_for_status()
            suggestions = json.loads(response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"Error making API request: {e}")
            continue
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON response: {e}")
            continue
        
        keywords2 = suggestions[1]
        length = len(keywords2)
        
        for n in range(length):
            keywords.append(keywords2[n].lower())
            
        if len(keywords) >= 100:
            break

def clean_df(keywords, keyword):
    keywords = list(dict.fromkeys(keywords))
    new_list = [word for word in keywords if all(val in word for val in keyword.split(' '))]
    df = pd.DataFrame(new_list, columns=['Keywords'])
    return df

st.set_page_config(layout="wide")
st.title("Keyword Suggestion Tool")

keyword = st.text_input("Topic:", "")

if st.button("Generate Keywords"):
    try:
        df = api_call(keyword)
        st.download_button(
            label="Download keywords as CSV",
            data=df.to_csv(index=False),
            file_name=f"{keyword.lower()}-keywords.csv",
            mime="text/csv",
        )
        st.dataframe(df)
    except Exception as e:
        st.error(f"An error occurred: {e}")
