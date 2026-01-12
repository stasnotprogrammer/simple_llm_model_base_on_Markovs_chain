#!venv/bin/python
from array import array
import pickle


class MY_LLM:
    def __init__(self, data:str, N=5, max_indexes_for_word = 50):
        self.data = tuple(self.id_words(data))
        self.N = N - 1
        #self.max_indexes_for_word = max_indexes_for_word
        self.model = {}
    
    def id_words(self, text:str):
        print("Токенизация текста")
        st = text.split()
        self.word_to_id = {w:i for i, w in enumerate(set(st))}
        id_text = []
        for word in st:
            id_text.append(self.word_to_id[word])
        del st
        print("Токенизация прошла успешно")
        return id_text

    def first_version_model(self):
        '''
        Подсчитывает количество повторений слов
        '''

        model = {}
        print("Идёт подсчет слов")
        print(f'Найдено {len(self.data)} слов')
        l = len(self.data) - self.N
        for i in range(l):
            model[self.data[i:i+self.N]] = {}
        print()
        for i in range(l):
            try:
                model[self.data[i:i+self.N]][self.data[i+self.N]] += 1
            except:
                model[self.data[i:i+self.N]][self.data[i+self.N]] = 1
        del l
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
        print("Подсчет вероятностей прошёл успешно")
        return model
    
    def creat_model(self):
        print('Создаю модель')
        model = self.two_version_model()
        print('Токенизация прошла успешна')
        self.model = {"N":self.N,
                      "LLM": {
                          "model":model,
                          "keys": list(model.keys()),
                      },
                      'id': {
                          'word_to_id': self.word_to_id
                      }
                     }
        print('Модель создана')
    
    def safe_model(self, filename=f'model.pkl'):
        print("Сохраняю модель")
        if self.model:
            with open(filename, "wb") as f:
                pickle.dump(obj=self.model, file=f)
            print("Модель сохранена")
        else:
            print("Нет модели ты идиот")


'''Маленький кусок текста, который я использую для экспериментов. Понял кто-нибудь отсылку на JOJO, если да то напишите!'''
text = 'кот ел сыр. кот ел коз. ля-ля тополя. гойда. а я пиво. соно чино садаме джоооооджоооо'

def read_clear_text(filename:str):
    with open(filename, 'r') as f:
        return f.read()

if __name__ == "__main__":
    m = MY_LLM(data=read_clear_text('text_for_model/text_for_model.txt'), N=5)
    m.creat_model()
    m.safe_model("model.pkl")