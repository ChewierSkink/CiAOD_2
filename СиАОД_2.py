import random    #импортируем библиотеку random для случайной генерации файла
import time      #импортируем библиотеку time для отслеживания времени работы функций


class Hesh_table:                   #класс Hesh_table
    def __init__(self):             #конструктор
        global d, f, m, count, del_count    #глобальные переменные
        del_count = 0               #количество удалённых переменных
        count = 0                   #количество записанных переменных
        d = []                      #хеш-таблица
        #далее производится выбор с каким файлом работать
        print("Введите число 1 или 2")
        print("1 - для работы с небольшим файлом, заполнение вручную")
        print("2 - для работы с большим файлом, заполнение случайное")
        vvod = int(input())         #выбор режима работы
        if vvod == 1:               #если 1, то первый режим
            m = 10                  #количество ячеек хеш-таблицы
            #заполнение хеш-таблицы пустыми ячейками
            for i in range(m):
                d.append([0, 0, 1, 0])
            self.manual()           #запуск метода manual
        elif vvod == 2:             #иначе если 2, то второй режим
            m = 8000                #количество ячеек хеш-таблицы
            #заполнение хеш-таблицы пустыми ячейками
            for i in range(m):
                d.append([0, 0, 1, 0])
            self.generate()         #запуск метода generate


    #метод для ручного ввода небольшого файла
    def manual(self):
        f = open('text.txt', 'w')   #открытие файла на запись, старые данные удаляются
        print("Введите 10 строк для записи в файл")
        print("Формат строки:")
        print("7-ми значное число, имя, адрес")
        #процесс записывания в файл строк, введённых пользователем
        for i in range(m):
            f.write(input())        #записывание ввода в файл
            f.write('\n')           #запись перехода на следующую строку
        f.close()                   #закрытие файла


    #метод для случайной генерации большого файла
    def generate(self):
        f = open('text.txt', 'w')   #открытие файла на запись, старые данные удаляются
        #процесс записывания в файл случайно сгенерированных строк
        for i in range(m):
            f.write(str(random.randint(1000000, 9999999))) #запись счёта в банке
            f.write(' name_')       #запись имени
            f.write(str(i))         #запись номера имени
            f.write(' address_')    #запись адреса
            f.write(str(i))         #запись номера адреса
            f.write('\n')           #запись перехода на следующую строку
        f.close()                   #закрытие файла


    #метод хеш-функции для получения ключа
    def hesh(self, check):
        global m                    #использование глобальных переменных
        return int(check) % m       #возвращает остаток от деления номера счёта на количество ячеек


    #метод рехеширования
    def rehesh(self):
        global m, d, count, del_count   #использование глобальных переменных
        old_d = d                   #создание старой хеш-таблицы
        d = []                      #новая хеш-таблица
        m *= 2                      #увеличение количества ячеек хеш-таблицы в два раза
        #заполнение хеш-таблицы пустыми ячейками
        for i in range(m):
            d.append([0, 0, 1, 0])
        count = 0                   #обнуление количества записанных переменных
        del_count = 0               #обнуление количества удалённых переменных
        #перезапись данных старой хеш-таблицы в новую
        for i in range(m // 2):
            if old_d[i][0] != 0 and old_d[i][3] == 0:   #если в ячейке номер счёта не 0 и флаг "удаление" 0
                self.input_d(old_d[i][0], old_d[i][1])  #запуск метода ввода информации в хеш-таблицу


    #метод ввода информации из файла в хеш-таблицу
    def input_d(self, numb, k):
        global count                #использование глобальных переменных
        key = self.hesh(numb)       #получение ключа из номера счёта с помощью хеш-функции
        x = key                     #фиксация изначального ключа
        n = 1                       #номер подбора
        while d[key][2] != 1:       #пока в ячейке с индексом ключа флаг "доступна для записи" не 1
            key += n                #увеличение ключа на номер подбора
            n += 1                  #увеличение номера подбора на 1
            if key >= m:            #если ключ больше количества ячеек хеш-таблицы
                key %= m            #ключ равен остатку от деления ключа на количество ячеек хеш-таблицы
            if key == x and count + del_count > m * 0.75:   #если вернулись в изначальную позицию и неравенство выполняется
                self.rehesh()       #выполнить рехеширование
                key = x             #перезапись ключа
                n = 1               #номер подбора
        #в ячейку с индексом ключа записываются номер счёта, номер строки в файле, "доступна для зписи", "удаление"
        d[key] = [numb, k, 0, 0]
        count += 1                  #увеличение количества записанных переменных на 1


    #метод поиска ячейки в хеш-таблице
    def find_d(self, numb):
        start_time = time.time()    #фиксация времени начала функции
        key = self.hesh(numb)       #получение ключа из номера счёта с помощью хеш-функции
        x = key                     #фиксация изначального ключа
        n = 1                       #номер подбора
        while d[key][0] != numb:    #пока номер счёта ячейки не совпадёт с введённым
            if d[key][2] == 1 and d[key][3] == 0:   #если ячейка пуста
                print("Время поиска в таблице:", "%s секунд" % (time.time() - start_time))
                return "Запись не существует"   #возврат сообщения
            key += n                #увеличение ключа на номер подбора
            n += 1                  #увеличение номера подбора на 1
            if key >= m:            #если ключ больше количества ячеек хеш-таблицы
                key %= m            #ключ равен остатку от деления ключа на количество ячеек хеш-таблицы
        if d[key][3] == 1:          #если ячейка удалена
            print("Время поиска в таблице:", "%s секунд" % (time.time() - start_time))
            return "Запись удалена"     #возврат сообщения
        print("Время поиска в таблице:", "%s секунд" % (time.time() - start_time))
        return key                  #возврат ключа


    #метод поиска ячейки в файле
    def find_f(self, numb):
        start_time = time.time()    #фиксация времени начала функции
        p = self.find_d(numb)       #результат поиска в хеш-таблице
        if p == "Запись не существует":     #если сообщение об ошибке
            print("Время поиска в файле:", "%s секунд" % (time.time() - start_time))
            return p                #возврат сообщения
        if p == "Запись удалена":   #если сообщение об ошибке
            print("Время поиска в файле:", "%s секунд" % (time.time() - start_time))
            return p                #возврат сообщения
        f = open('text.txt')        #открытие файла на чтение
        lines = f.readlines()       #массив из строк файла
        f.close()                   #закрытие файла
        print("Время поиска в файле:", "%s секунд" % (time.time() - start_time))
        return lines[d[p][1]]       #возврат искомой строки файла


    #метод удаления информации из хеш-таблицы и строки из файла
    def del_df(self, numb):
        global count, del_count     #использование глобальных переменных
        p = self.find_d(numb)       #результат поиска в хеш-таблице
        if p == "Запись не существует":     #если сообщение об ошибке
            return p                #возврат сообщения
        if p == "Запись удалена":   #если сообщение об ошибке
            return "Запись уже удалена"     #возврат сообщения
        d[p][2] = 1                 #флаг "доступна для зписи" 1
        d[p][3] = 1                 #флаг "удаление" 1
        count -= 1                  #уменьшение количества записанных переменных на 1
        del_count += 1              #увеличение количества удалённых переменных на 1
        new_f = open('new_text', 'w')   #открытие нового файла на запись, старые данные удаляются
        f = open('text.txt')        #открытие файла на чтение
        #переписывание строк из файла в новый
        for ln in f:
            if ln == "\n":          #если пустая строка
                new_f.write('\n')   #записывание пустой строки
            elif str(numb) == ln.split()[0]:  #если введённый номер счёта равен номеру счёта в строке
                new_f.write('\n')   #записывание пустой строки
            else:                   #иначе
                new_f.write(ln)     #переписывание строки в новый файл
        new_f.close()               #закрытие нового файла
        f.close()                   #закрытие файла
        new_f = open('new_text')    #открытие нового файла на чтение
        f = open('text.txt', 'w')   #открытие файла на запись, старые данные удаляются
        #переписывание строк из нового файла в старый
        for ln in new_f:
            f.write(ln)             #переписывание строки в старый файл
        new_f.close()               #закрытие нового файла
        f.close()                   #закрытие файла
        return "Запись удалена"     #возврат сообщения


    #метод добавления строки в файл и информации по ней в хеш-таблицу
    def add_s(self):
        global count                #использование глобальных переменных
        f = open('text.txt', 'a')   #открытие файла на дозапись
        print("Введите строку для записи в файл")
        print("Формат строки:")
        print("7-ми значное число, имя, адрес")
        vvod = input()              #пользовтельская строка
        f.write(vvod)               #записывание ввода в файл
        f.close()                   #закрытие файла
        self.input_d(int(vvod.split()[0]), count)   #добавление данных из строки в хеш-таблицу


if __name__ == "__main__":
    h_t = Hesh_table()
    f = open('text.txt')
    for ln in f:
        h_t.input_d(int(ln.split()[0]), count)
    f.close()
    print("Введите команду для тестирования")
    print("1 - найти запись в таблице",
          "2 - найти запись в файле",
          "3 - удалить запись из таблицы и файла",
          "4 - добавить запись в файл и таблицу",
          "0 - завершить работу", sep = '\n')
    a = int(input())
    while a != 0:
        if a == 1:
            print("Введите номер счёта для поиска строки в таблице:")
            print(h_t.find_d(int(input())))
        elif a == 2:
            print("Введите номер счёта для поиска строки в файле:")
            print(h_t.find_f(int(input())))
        elif a == 3:
            print("Введите номер счёта для удаления из таблицы и файла:")
            print(h_t.del_df(int(input())))
        elif a == 4:
            h_t.add_s()
        print("Введите команду для тестирования")
        a = int(input())
