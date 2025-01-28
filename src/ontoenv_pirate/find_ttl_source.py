from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
# Load environment variables
load_dotenv(find_dotenv())
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def find_ttl_src(content):
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            temperature=0,
            messages=[
                {"role": "developer", "content": '''
                    You are an expert in searching the web and webpages. You will be tasked to find the most up-to-date version of an ontology in turtle format.
                    The user will give you a url. This will be a URI (uniform resource identifier) that points to an ontology.
                    However the ontology is not in the given location. Your job is to find the most up-to-date version of the ontology in turtle format and only return the URL of the .ttl file to download.
                    Here's a list of considerations you must make:
                    1. The ontology must be in turtle format
                    2. The ontology must be the most up-to-date version
                    3. Sometimes the ttl file you find will be outdated. In that case, you will see a warning on the link or the page that provides that link.
                    4. Sometimes the link user will provide will be unavailable or doesn't contain any link to the ttl file. In that case you should craft a google search to find the ontology.
                    5. If you cannot find return "THE ONTOLOGY IS NOT AVAILABLE"
                    6. Only return the URL of the .ttl file or "THE ONTOLOGY IS NOT AVAILABLE", do not contain any other information, text, or markdown.
                '''},
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return completion.choices[0].message.content
    except:
        return None