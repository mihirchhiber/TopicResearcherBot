from article import Article
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_ollama.llms import OllamaLLM
import os
import random
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
    # Alternative models (commented):
    # llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="deepseek-r1-distill-llama-70b")
    # llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")
    # llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

def unload_llm():
    global llm
    llm = None  # Allow Python to garbage collect

def remove_space(text):
    while "  " in text:
        text = text.replace("  ", " ")
    return text

def get_recent_articles(sites, topics, weeks=1, articlesPerWeek=5):
    articles = []

    id = random.randint(100000,1000000)

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
                    article = Article(
                        id = id,
                        topics = topics,
                        sites = sites,
                        title=item.get('title'),
                        url=item.get('link'),
                        source=site,
                        content=""
                    )

                    try:
                        page = requests.get(article.url, timeout=10)
                        soup = BeautifulSoup(page.content, 'html.parser')
                        main_content = soup.find('article') or soup.find('main') or soup.find('div', class_='content')

                        if main_content:
                            for elem in main_content(['script', 'style', 'nav', 'footer']):
                                elem.decompose()
                            article.content = ' '.join(main_content.stripped_strings)
                        else:
                            for elem in soup(['script', 'style', 'nav', 'footer']):
                                elem.decompose()
                            article.content = remove_space(
                                re.sub(r'[^\x20-\x7E]', ' ', soup.get_text().replace("\n", " "))
                            )

                    except Exception as e:
                        article.content = f'Content extraction failed: {str(e)}'

                    articles.append(article)

            except Exception as e:
                print(f"Error searching {site} for {topic}: {str(e)}")

    return articles

def clean_article_text(article):
    """Updates the Article object with cleaned content."""
    cleaning_messages = [
        ("system",
         "You are a text cleaner specialized in extracting only the main article content from messy website text. "
         "Strictly remove any unrelated material such as ads, cookie notices, navigation bars, subscription prompts, company slogans, headers, footers, or any UI elements. "
         "DO NOT paraphrase, edit, summarize, or add words. Only copy over the original article sentences exactly as they are. "
         "Ensure you preserve the full article's meaning, flow, and structure without omitting any part of the real article body. "
         "If unsure about a piece of text, err on the side of excluding it unless it clearly belongs to the article. "
         "Return ONLY the cleaned article text and nothing else."
         ),
        ("human",
         "The following text is extracted from a webpage about '{subject}'. Please extract and return only the main article content:\n\n{content}")
    ]

    cleaning_prompt_template = ChatPromptTemplate.from_messages(cleaning_messages)

    cleaning_prompt = cleaning_prompt_template.invoke({
        "subject": article.title,
        "content": article.content
    })

    result = llm.invoke(cleaning_prompt)
    article.clean_content = result
    return article

def summarize_article_text(article):
    """Updates the Article object with summarized content."""
    summarization_messages = [
        ("system",
         "You are a professional summarizer. Your task is to create a clear and concise summary of the provided article content, strictly focused on the subject. "
         "Ignore any text that looks like advertisements, navigation prompts, disclaimers, subscription offers, or website boilerplate if it appears. "
         "Summarize ONLY the meaningful article information, without introducing any new facts or interpretations. "
         "Keep the summary factual, neutral, and focused. Reply with the summary ONLY."
         ),
        ("human",
         "Summarize the following article about '{subject}':\n\n{cleaned_content}")
    ]

    summarization_prompt_template = ChatPromptTemplate.from_messages(summarization_messages)

    summarization_prompt = summarization_prompt_template.invoke({
        "subject": article.title,
        "cleaned_content": article.clean_content
    })

    result = llm.invoke(summarization_prompt)
    article.summary = result
    return article
