# import pathlib
# import textwrap

import google.generativeai as genai
import os

os.environ['https_proxy'] = '127.0.0.1:7890'
os.environ['http_proxy'] = '127.0.0.1:7890'
# # Used to securely store your API key
# from google.colab import userdata

# from IPython.display import display
# from IPython.display import Markdown


# def to_markdown(text):
#   text = text.replace('•', '  *')
#   return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.

genai.configure(api_key="AIzaSyCjA9AiKk1VuIRk-YIiKffx7_xC46JXj80")
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)