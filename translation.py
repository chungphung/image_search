from os import mkdir
from os.path import exists, join
import pickle

from googletrans import Translator as T


class Translator:
    def __init__(self, data='translated_data.pickle'):
        self.translator = T()
        self.translated_data_file = data
        if exists(f'./data/{self.translated_data_file}'):
            with open(f'./data/{self.translated_data_file}', 'rb') as f:
                self.translated_items = pickle.load(f)
        else:
            if not exists('./data/'):
                mkdir('./data/')
            self.translated_items = {}

    def _save_data(self):
        with open(f'./data/{self.translated_data_file}', 'wb') as f:
            pickle.dump(self.translated_items, f)

    def translate(self, items):
        new_items = []
        translated = []
        for item in items:
            if item not in self.translated_items:
                new_items.append(item)
            else:
                translated.append(self.translated_items[item])
        translations = self.translator.translate(
            new_items, dest='en', src='vi')
        for t in translations:
            translated.append(t.text)
            self.translated_items[t.origin] = t.text
        self._save_data()
        return translated
