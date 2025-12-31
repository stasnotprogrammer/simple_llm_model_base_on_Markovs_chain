#!venv/bin/python
from chardet.universaldetector import UniversalDetector
import pickle
import os


class MY_LLM:
    def __init__(self, data, N=5):
        self.data = tuple(data.split())
        self.N = N - 1
        self.model = {}
    
    def first_version_model(self):
        '''
        Подсчитывает количество повторений слов
        '''

        model = {}
        print("Идёт подсчет слов")
        print(f'Найдено {len(self.data)} слов')
        for i in range(len(self.data) - self.N):
            model[self.data[i:i+self.N]] = {}
        for i in range(len(self.data) - self.N):
            try:
                model[self.data[i:i+self.N]][self.data[i+self.N]] += 1
            except:
                model[self.data[i:i+self.N]][self.data[i+self.N]] = 1
        return model
    
    def two_version_model(self):
        model_ = self.first_version_model()
        print("Идёт подсчет вероятностей")
        model = {}
        for key1 in model_:
            sum_ = sum(model_[key1].values())
            model[key1] = {}
            for key2 in model_[key1]:
                model[key1][key2] = model_[key1][key2] / sum_
        return model
    
    def creat_model(self):
        print('Создаю модель')
        model = self.two_version_model()
        self.model = {"N":self.N,
                      "LLM": {
                          "model":model,
                          "keys": list(model.keys())
                      }}
    
    def safe_model(self, filename):
        print("Сохраняю модель")
        if self.model:
            with open(filename, "wb") as f:
                pickle.dump(obj=self.model, file=f)
            print("Модель сохранена")
        else:
            print("Нет модели ты идиот")

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
    for book in os.listdir(path):
        print(f"[{n}/{all_}] Считыаю данные с {book}", end='\r')
        with open(f"{path}/{book}", "r", encoding=detect_encoding(f"books/{book}")) as f:
            text += str(f.read()).lower()
        n += 1
    print()
    return text

def remove_punctuation_extended(text):
    print('Очищаю текст')
    rem_data = ['!', '@', '#',
                '$', '%', '^',
                '&', '*', '(',
                ')', '_' ,'-',
                '+', '=', '{',
                '}' ,'[', ']',
                '/', '|', ';',
                ':', '"', "'",
                '<', '>', ',',
                '.', '?', '/',
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
                '—'
                ]
    rem_ = '\n\t'
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
    m = MY_LLM(data=remove_punctuation_extended(read_books('books')), N=7) #В данном вариате файлы для обучения находятся в директории books, измените на вашу директорию с данными
    m.creat_model()
    m.safe_model("model.pkl")
