import shelve
import parameters as p


class Save:
    def __init__(self):
        self.file = shelve.open('data')

        # self.info = {
        #     'name': 'Kanye',
        #     'age' : 24,
        #     'state': State.MENU
        # }

    def save(self):
        # self.file['Info'] = self.info  под ключом инфо записали инфо
        self.file['usr_y'] = p.usr_y

    def add(self, name, value):
        self.file[name] = value

    def get(self, name):
        try:  # попробует, если нет, то не выдаст ошибку, а выдаст ветвь except
            return self.file[name]
        except KeyError:
            return 0

        # num = self.file['Number']
        # print(num)
        # print(self.file['Info'])

    def __del__(self):  # деструктор
        self.file.close()
