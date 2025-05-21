import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def scrape_pubmed(query, max_articles=3):
    base_url = "https://pubmed.ncbi.nlm.nih.gov/"
    
    params = {"term": query}
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    article_links = [
        base_url + a["href"] for a in soup.select(".docsum-title")[:max_articles]
    ]

    articles = []
    for link in article_links:
        try:
            page = requests.get(link, headers=headers)
            article_soup = BeautifulSoup(page.text, "html.parser")
            abstract_tag = article_soup.find("div", class_="abstract-content")
            abstract_text = abstract_tag.get_text(separator=" ").strip() if abstract_tag else ""
            articles.append(abstract_text)
        except Exception as e:
            print(f"⚠️ Failed to scrape {link}: {e}")

    return articles

def generate_diet_recommendation(user_input, allergies, docs):
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    allergy_str = ", ".join(allergies) if allergies else "none"
    docs_text = "\n\n".join(docs) if docs else "No relevant articles found."

    prompt = f"""
You are a helpful, professional dietitian AI.

User's health problem(s): {user_input}
User's allergies: {allergy_str}

Based on the following PubMed abstracts:
{docs_text}

Please provide a personalized, safe, and evidence-based dietary recommendation, avoiding foods related to the allergies.

👉 Structure the response clearly using:
- Section titles (if applicable)
- Bullet points or numbered lists
- Line breaks between sections
"""

    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    # Optional cleanup: Ensure line breaks between points and remove extra whitespace
    formatted_text = "\n".join(
        f"• {line.strip()}" if not line.strip().startswith(("•", "-", "1.", "2.")) else line.strip()
        for line in raw_text.split('\n') if line.strip()
    )

    return formatted_text
