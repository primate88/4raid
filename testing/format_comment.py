import json
from html import unescape
import re

def format_comment(comment):
    # Remove <span> tags (and any other HTML tags if needed)
    cleaned_html = re.sub(r'<[^>]+>', '', comment)
    
    # Replace <br> tags with newline characters
    cleaned_html = cleaned_html.replace('<br>', '\n')
    
    # Decode HTML entities
    decoded_html = unescape(cleaned_html)
    
    return decoded_html

# Example usage:
input_comment = "Keemstar should run for public office.<br><span class="quote">&gt;Everyone lies about him</span><br><span class="quote">&gt;He&#039;s the hero of truth and justice</span><br><span class="quote">&gt;absolutely destroys every lie about him</span><br><span class="quote">&gt;People still don&#039;t believe him</span><br><br>https://www.youtube.com/watch?v=sJk<wbr>0aYg2jAA<br>God bless Keemstar"
formatted_comment = format_comment(input_comment)
print(formatted_comment)
