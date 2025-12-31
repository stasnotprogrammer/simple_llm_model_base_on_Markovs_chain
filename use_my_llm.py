#!venv/bin/python
from Levenshtein import distance
import pickle
import random
import string

class useLLM:
    def __init__(self, model):
        with open(model, 'rb') as f:
            M = pickle.load(f)
        self.N = M['N']
        self.model = M['LLM']['model']
        self.keys = M['LLM']['keys']
    
    def trying_in(self, part: list, whole: list, percent: float = 1):
        i, j = 0, 0   
        while i < len(part) and j < len(whole):
            if part[i] == whole[j]:
                i += 1
            j += 1
        
        if i == len(part):
            return True
        
        str_part = " ".join(part)
        
        if len(part) <= len(whole):
            best_similarity = 0
            for start in range(len(whole) - len(part) + 1):
                str_sub = " ".join(whole[start:start + len(part)])
                similarity = 1 - distance(str_part, str_sub) / max(len(str_part), len(str_sub))
                best_similarity = max(best_similarity, similarity)
            
            return best_similarity >= percent
        else:
            str_whole = " ".join(whole)
            similarity = 1 - distance(str_part, str_whole) / max(len(str_part), len(str_whole))
            return similarity >= percent

    def remove_punctuation(self, text):
        punctuation = string.punctuation
        russian_punctuation = '0123456789«»„“—–…¿¡•©®™°±≤≥≠≈∞µ∂∑∏π∫Ω\n\t'
        all_punctuation = punctuation + russian_punctuation
        translator = str.maketrans('', '', all_punctuation)
        cleaned_text = text.translate(translator)
        cleaned_text = ' '.join(cleaned_text.split())
        return cleaned_text

    def next_word(self, text, quantity, prosent=0.8):
        text = self.remove_punctuation(text).lower().split()
        print('Идёт генерация')
        for i in range(quantity):
            if len(text) >= self.N:
                usetext = text[-self.N:]
            else:
                usetext = text
            k = random.choice(self.keys)
            for key in self.keys:
                if self.trying_in(usetext, key, percent=prosent):
                    k = key
            text.append(random.choices(list(self.model[k].keys()), weights=list(self.model[k].values()))[0])
            print(f'{(i+1)*100/quantity}% [{'='*int((i+1)*100/quantity)}>{' '*int(100-(i+1)*100/quantity)}]', end='\r')
        print()
                    
                
        return ' '.join(text)
            

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