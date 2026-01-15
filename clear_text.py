#!venv/bin/python
from chardet.universaldetector import UniversalDetector
import os


def detect_encoding(file):
    detector = UniversalDetector()
    with open(file, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']

def read_books(path):
    text = ''
    n = 1
    all_ = len(os.listdir(path))
    ml = len(max(os.listdir(path), key=len))
    for book in os.listdir(path):
        print(f"[{n}/{all_}] Считыаю данные с {book}" + ' '*(ml-len(f"[{n}/{all_}] Считыаю данные с {book}")), end='\r')
        with open(f"{path}/{book}", "r", encoding=detect_encoding(f"books/{book}")) as f:
            text += str(f.read()).lower()
        n += 1
    del [n, all_]
    print()
    return text

def remove_punctuation_extended(text:str):
    print('Очищаю текст')
    rem_data = ['@', '#', '$',
                '%', '^', '—',
                '&', '*', '_',
                '+', '=', '{',
                '}' ,'[', ']',
                '/', '|', ';',
                '<', '>', '/',
                '~', '`', '\\',
                'www', '…', '»',
                '“', '–', '«',
                '•', '1', '2',
                '3', '4', '5',
                '6', '7', '8',
                '9', '0', 'a',
                'b', 'c', 'd',
                'e', 'f', 'g',
                'h', 'i', 'j',
                'k', 'l', 'm',
                'n', 'o', 'p',
                'q', 'r', 's',
                't', 'u', 'v',
                'w', 'x', 'y',
                'z', 'ѣ', '®',
                '©', '™', '№',
                ':', ':.', '.:'
                ]
    
    
    text = text.lower()
    rem_ = ['\n','\t', 'ты:', 'продолжи диалог:', 'собеседник:', 'текст:', 'ответ:']
    for r in rem_data:
        if r in text:
            text = text.replace(r, '')
    for r in rem_:
        if r in text:
            text = text.replace(r, ' ')
    
    text = text.split()
    print('Текст очищен')
    return ' '.join(text)

if __name__ == "__main__":
    if not os.path.exists('text_for_model'):
        os.mkdir('text_for_model')
    with open('text_for_model/text_for_model.txt', 'w') as f:
        f.write(remove_punctuation_extended(read_books('books')))