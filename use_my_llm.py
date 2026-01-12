#!venv/bin/python
from Levenshtein import distance
from array import array
import pickle
import random
import string

class useLLM:
    def __init__(self, model, prosent = None):
        print('Загрузка модели...')
        with open(model, 'rb') as f:
            M = pickle.load(f)
        self.N = M['N']
        self.model = M['LLM']['model']
        self.keys = tuple(M['LLM']['keys'])
        self.word_to_id = M['id']['word_to_id']
        self.id_to_word = {v:k for k,v in self.word_to_id.items()}
        if not prosent:
            prosent = (self.N - 1)/(self.N)
        self.prosent = prosent
        del M
        print('Модель загружена')
        print(f'N - {self.N + 1}') # Длинна граммы равна N - 1 -> self.N = N - 1 -> N = self.N + 1
        print(f'Количество N грамм - {len(self.keys)}')
    
    def remove_punctuation(self, text):
        punctuation = string.punctuation
        russian_punctuation = '0123456789«»„“—–…¿¡•©®™°±≤≥≠≈∞µ∂∑∏π∫Ω\n\t'
        all_punctuation = punctuation + russian_punctuation
        translator = str.maketrans('', '', all_punctuation)
        cleaned_text = text.translate(translator)
        cleaned_text = ' '.join(cleaned_text.split())
        return cleaned_text

    def hight_firts_letter(self, text:list[str]):
        '''
        text - Список слов ['яблоко','банан','груша']
        '''
        text = list(map(list, text))
        text[0][0] = text[0][0].upper()
        for i in range(1, len(text)):
            try:
                if text[i-1][len(text[i-1])-1] in ['.', '!', '?']:
                    text[i][0] = text[i][0].upper()
            except: ...
        return [''.join(word) for word in text]
    
    def del_replays(self, text:list):
        new_text = []
        for word in text:
            if not new_text or word != new_text[-1]:
                new_text.append(word)
        return new_text

    def text_to_id(self, text:list):
        list_id = []
        for word in text:
            list_id.append(self.word_to_id.get(word, -1))
        return list_id
    
    def id_to_text(self, list_id:list):
        text = []
        for id in list_id:
            text.append(self.id_to_word.get(id, ''))
        return text

    def get_key(self, Ngram:list, prosent:float) -> int:
        if Ngram in self.keys:
            return self.keys.index(Ngram)
        else:
            for key in self.keys:
                c = 0
                for i in Ngram:
                    if i in key:
                        c += 1
                if c/len(Ngram) >= prosent:
                    return self.keys.index(key)
            if not (c/len(Ngram) >= prosent):
                return random.randint(0, len(self.keys)-1)

    def next_word(self, text, quantity):
        text = self.remove_punctuation(text).lower().split()
        text = self.text_to_id(text)
        print('Идёт генерация')
        for i in range(quantity):
            if len(text) >= self.N:
                usetext = text[-self.N:]
            else:
                usetext = text
            k = self.get_key(usetext, prosent=self.prosent)
            text.append(random.choices(list(self.model[self.keys[k]].keys()), weights=list(self.model[self.keys[k]].values()))[0])
            print(f'{(i+1)*100/quantity}% [{'='*int((i+1)*100/quantity)}>{' '*int(100-(i+1)*100/quantity)}]', end='\r')
        print()
        text = self.del_replays(text)            
        return ' '.join(self.hight_firts_letter(self.id_to_text(text)))
            

def main():
    UM = useLLM(model='model.pkl')
    while True:
        text = input('Введите текст: ')
        if text == 'exit':
            break
        quality = int(input('Введите количество слов: '))
        print(UM.next_word(text, quality))

if __name__ == '__main__':
    main()