from bs4 import BeautifulSoup
import requests
from extractor_2 import update
import random
from colorama import init
from termcolor import colored
import json

init()

usage_site_basepath = 'https://sentence.yourdictionary.com/'
meaning_site_basepath = 'https://www.yourdictionary.com/'
status_file_path = 'status'
limit = 10
words = []
meanings = []
usages = []

def set_status(lword, lstatus):
    if os.path.exists(path) and os.path.isfile(path):
        with open(status_file_path, '+t') as file:
            words2status = json.load(file)
            words2status[lword] = lstatus
    else:
        print('**STATUS FILE NOT FOUND**')

def get_status(lword):
    if os.path.exists(path) and os.path.isfile(path):
        with open(status_file_path, 'rt') as file:
            words2status = json.load(file)
            return words2status.get(lword, '**NOT FOUND**')
    else:
        print('**STATUS FILE NOT FOUND**')

def load():
    with open('vocab', 'rt') as file:
        words_dict = json.load(file)
        for key in words_dict:
            words.append(key)
            meanings.append(words_dict[key][0])
            usages.append(words_dict[key][1])

def choose():
    index = random.randint(0, len(words) - 1)
    return (words[index], meanings[index], usages[index])

if __name__ == '__main__':
    load()
    while True:
        user_input = input('q: quit\nu: update the collection of words\ns: search from local record\nws: web search for usage\nany other key to proceed: ').lower()
        
        if user_input == 'q':
            break

        elif user_input == 'u':
            update()
            load()
            continue

        elif user_input == 's':
            query = input('enter the word ').lower()
            if query not in words:
                print('**WORD NOT IN LOCAL RECORD**')
                continue
            else:
                index = words.index(query)
                lword = query
                lmeaning = meanings[index]
                lusage = usages[index]
        elif user_input == 'ws':
            query = input('make sure the spellings are correct ')
            if not query:
                print('**NO WORD ENTERED**')
            else:
                try:
                    print('\nUSAGE:\n')
                    src1 = requests.get('https://sentence.yourdictionary.com/reckoning').content
                    soup1 = BeautifulSoup(src1, 'html.parser')
                    selected1 = soup1('div', {'class': 'sentence component'}, limit=limit   )

                    for i, sentence in enumerate(selected1):
                        print(i, sentence.text, sep='. ')

                    print('\nMEANINGS: \n')
                    src2 = requests.get('https://www.yourdictionary.com/company').content
                    soup2 = BeautifulSoup(src2, 'html.parser')
                    selected2 = soup2('div', {'class': 'relative flex'}, limit=limit)

                    for i, meaning in enumerate(selected2):
                        print(i, meaning.text, sep='. ')
                            

                except requests.exceptions.ConnectionError:
                    print('**INTERNET CONNECTION LOST**')
                except IndexError:
                    print('**WORD NOT IN RECORD**')
            continue
        else:
            lword, lmeaning, lusage = choose()

        print(colored('  WORD: ', 'cyan'), colored(lword, 'cyan'))
        temp = input('press m to return to the menu press any key to reveal the usage')
        if temp == 'm': continue
        print(colored('  USAGE:', 'cyan'), colored(lusage, 'cyan'))
        input('press any key to reveal the meaning')
        print(colored('  MEANING:', 'cyan'), colored(lmeaning, 'cyan'))
