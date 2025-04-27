# llm_articles.py

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_ollama.llms import OllamaLLM
import os
import re
import requests

# Load environment variables
load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")
google_cse_id = os.environ.get("GOOGLE_CSE_ID")
groq_api_key = os.environ.get("GROQ_APIKEY")

llm = None

def load_llm():
    global llm
    llm = OllamaLLM(
        model="llama3.2",
        temperature=0.2,
        top_p=0.9,
        repeat_penalty=1.2
    )
    # llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="deepseek-r1-distill-llama-70b")
    # llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")
    # llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

def unload_llm():
    global llm
    llm = None  # let Python garbage collect it

def remove_space(text):
    while "  " in text:
        text = text.replace("  ", " ")
    return text

def get_recent_articles(sites, topics, weeks=1, articlesPerWeek=5):
    articles = []

    for site in sites:
        for topic in topics:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'q': topic,
                'key': google_api_key,
                'cx': google_cse_id,
                'num': articlesPerWeek * weeks,
                'siteSearch': site,
                'dateRestrict': f'w{weeks}',
                'lr': 'lang_en'
            }

            try:
                response = requests.get(url, params=params)
                results = response.json()

                for item in results.get('items', []):
                    article = {
                        'title': item.get('title'),
                        'url': item.get('link'),
                        'source': site,
                        'content': ''
                    }

                    try:
                        page = requests.get(article['url'], timeout=10)
                        soup = BeautifulSoup(page.content, 'html.parser')
                        main_content = soup.find('article') or soup.find('main') or soup.find('div', class_='content')

                        if main_content:
                            for elem in main_content(['script', 'style', 'nav', 'footer']):
                                elem.decompose()
                            article['content'] = ' '.join(main_content.stripped_strings)
                        else:
                            for elem in soup(['script', 'style', 'nav', 'footer']):
                                elem.decompose()
                            article['content'] = remove_space(re.sub(r'[^\x20-\x7E]', ' ', soup.get_text().replace("\n", " ")))

                    except Exception as e:
                        article['content'] = f'Content extraction failed: {str(e)}'

                    articles.append(article)

            except Exception as e:
                print(f"Error searching {site} for {topic}: {str(e)}")

    return articles

def clean_article_text(subject, text):
    cleaning_messages = [
        ("system",
         "You are a text cleaner. Your task is to extract only the meaningful, article-related content based on the subject provided. "
         "Remove anything unrelated like ads, cookie notices, navigation bars, buttons, website slogans, subscription prompts, or any boilerplate text. "
         "Make sure no information from the article related content is missed. Do not rephrase the text, give back the same text which is relevant. Reply with the cleaned text ONLY"
         ),
        ("human",
         "Here is an article about '{subject}'. Extract only the main content and ignore any irrelevant site text:\n\n{content}")
    ]

    cleaning_prompt_template = ChatPromptTemplate.from_messages(cleaning_messages)

    cleaning_prompt = cleaning_prompt_template.invoke({
        "subject": subject,
        "content": text
    })

    result = llm.invoke(cleaning_prompt)
    return result

def summarize_article_text(subject, text):
    summarization_messages = [
        ("system",
         "You are a professional summarizer. Your job is to generate a concise, clear summary of the provided article content, focused on the subject. "
         "Summarize only the essential information without adding new details. Reply with the summary ONLY"
         ),
        ("human",
         "Summarize the following article about '{subject}':\n\n{cleaned_content}")
    ]

    summarization_prompt_template = ChatPromptTemplate.from_messages(summarization_messages)

    summarization_prompt = summarization_prompt_template.invoke({
        "subject": subject,
        "cleaned_content": text
    })

    result = llm.invoke(summarization_prompt)
    return result