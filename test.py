#!/usr/bin/env python
 
"""Scans for pages content and checks for errors."""

import logging
import requests
from bs4 import BeautifulSoup
import language_tool_python

# Global settings
logging.basicConfig(filename='mylog.log', encoding='utf-8')
tool = language_tool_python.LanguageTool('en-US')  # use a local server (automatically set up), language English

# Data
urls = [
    'https://github.com/.../wiki',
]

"""Logger function."""
def log(text):
    logging.info(text)
    print(text)
    
"""Main script function."""
def main():
    for url in urls:
        log('\n###############################################################################')
        log('# ' + url)
        log('###############################################################################\n')

        # Download and extract text from webpage
        html_page = res.content
        res = requests.get(url)
        soup = BeautifulSoup(html_page, 'html.parser')
        #TODO: Remove divs with class=highlight to remove code samples
        try:
            soup.pre.decompose()
        except AttributeError:
            pass

        body = soup.find(id='wiki-body')
        #print(body.text)

        # Check text for problems
        matches = tool.check(body.text)
        for match in matches:
            # Print the context
            log(match.context)
            
            # Show error offset
            pointer = ''
            for i in range(match.offsetInContext):
                pointer += ' '
                
            pointer += '^'
            for i in range(match.errorLength - 1):
                pointer += '^'
            
            log(pointer)
            
            # Print the problem
            log('>> ' + match.ruleIssueType + ': ' + match.message)
            
            # Replacements
            rep_amount = len(match.replacements)
            if rep_amount > 5:
                rep_amount = 5
            
            reps = '>> solutions: '
            for i in range(rep_amount):
                reps += match.replacements[i] + ' | '
            reps = reps[:len(reps) - 3]
            
            log(reps)
            log('\n----------\n')

if __name__ == '__main__':
    main()
