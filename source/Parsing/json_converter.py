import json
import shutil


class Converter:
    def __init__(self, filename):
        self.__filename = filename
        self.__links = {}
        self.__pointer = 0

    def start(self):
        print('Добро пожаловать!')
        while self._listen() != 'exit':
            link = input('Вставьте сслыку: ')
            from_ = input('От: ')
            to = input('До: ')
            step = input('Шаг: ')
            self.__links[str(self.__pointer)] = {"link": link, "start": from_, "stop": to, "step": step}
            self.__pointer += 1

        with open(self.__filename, 'w') as file:
            json.dump(self.__links, file)

    def _listen(self):
        inp = input('-' * shutil.get_terminal_size()[0])

        if inp == '':
            return

        # show last n records
        if inp.startswith('show'):
            try:
                n = inp.split(' ')[1]
                for i in range(len(self.__links) - 1, len(self.__links) - int(n) - 1, -1):
                    print(str(i), self.__links[str(i)])
                return self._listen()
            except:
                return self._listen()
        elif inp.startswith('edit'):
            n = inp.split(' ')[1]
            link = input('Вставьте сслыку: ')
            from_ = input('От: ')
            to = input('До: ')
            step = input('Шаг: ')
            self.__links[n] = {"link": link, "start": from_, "stop": to, "step": step}
            return self._listen()
        elif inp.startswith('del'):
            n = inp.split(' ')[1]
            self.__links.pop(n)
            return self._listen()
        else:
            return inp


if __name__ == '__main__':
    converter = Converter('test.json')
    converter.start()
