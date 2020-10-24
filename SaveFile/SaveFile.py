import os
import datetime as dt

class SaveACHFile:
    def __init__(self, originator_name):
        self.originator_name = originator_name

    @property
    def create_dir(self):
        transactions_path = os.path.abspath('../TRANSACTIONS')
        new_path = transactions_path + f'/{self.originator_name}'
        if self.originator_name not in os.listdir(transactions_path):
            os.makedirs(new_path)

        return new_path

    def name_file(self, path):
        time = dt.datetime.now().strftime('%H%M%S')
        date = dt.datetime.now().strftime('%Y%m%d')
        filename = f'{date}_{time}'

        count = 0
        for file in os.listdir(path):
            if filename in file:
                count += 1

        filename = filename + f'_{count + 1}.txt'

        return filename

    def generate_file_path(self, filename, path):

        return f'{path}/{filename}'

    def save_file(self, contents):
        folder = self.create_dir
        path_to_file = self.generate_file_path(
            self.name_file(folder),
            folder
        )

        with open(path_to_file, 'w') as ach:
            ach.write(contents)

