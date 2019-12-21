from tkinter import *
import re

root = Tk()


# функция преобразования
def convert():
    text_to_convert = textLabel1.get('1.0', END+'-1c')

    text_to_convert = re.sub(r'\n', ' ', text_to_convert)
    text_to_convert = re.sub(r'\t', ' ', text_to_convert)
    text_to_convert = re.sub(r'\r', ' ', text_to_convert)
    text_to_convert = re.sub(r'\s+', ' ', text_to_convert)

    textLabel1.delete('1.0', END+'-1c')
    textLabel2.delete('1.0', END + '-1c')

    textLabel1.insert('1.0', text_to_convert)

    ib = 49
    ia = 50
    glasnie = set(["а", "о", "у", "ы", "э", "я", "ё", "ю", "и", "е"])
    znak = set({'ь', 'ъ'})
    while ia < len(text_to_convert):  # пока не конец текста
        temp_char_before = text_to_convert[ib]
        temp_char_after = text_to_convert[ia]

        if (temp_char_before != ' ') and (temp_char_after != ' '):  # если до или после переноса нет пробелов (единое слово)
            word_start_index = text_to_convert.rfind(" ", ib - 15, ib)  # начало слова
            word_end_index = text_to_convert.find(" ", ia, ia + 15)  # конец слова
            reserve_before = ib - word_start_index   # количество букв до пенеоса

            if reserve_before > 2:  # если в запасе 3 символа и более, то можно пытаться перенести слово
                i = ib  # индекс символа, где предположительно будет перенос
                temp_i = 0  # количество сиволов, на которое мы сдвигаемся при неудачном подборе i

                while i > word_start_index:  # если индекс предположительного места переноса еще не вышел за границу начала слова, то пытаемся перенести

                    if (text_to_convert[ib - 1 - temp_i].lower() in glasnie) and \
                            (text_to_convert[ib - temp_i].lower() in glasnie):  # если до и после переносапопадает гласная, то переносим
                        i = 0  # обнуляем, чтобы выйти из цикла и пойти на следующую строчку
                        text_to_convert = text_to_convert[:ib - temp_i] + "-" + ' ' * temp_i + text_to_convert[ib - temp_i:]  # вставили перенос

                    elif (text_to_convert[ib - 1 - temp_i].lower() not in glasnie) and \
                            (text_to_convert[ib - temp_i].lower() not in glasnie) and \
                            (text_to_convert[ib - temp_i].lower() not in znak) and \
                            (glasnie.intersection(set(text_to_convert[word_start_index: ib - 1 - temp_i])) != {}) and \
                            (glasnie.intersection(set(text_to_convert[ib - temp_i: word_end_index])) != {}):  # если две согласные, но до и после перноса есть гласные
                        i = 0  # обнуляем, чтобы выйти из цикла и пойти на следующую строчку
                        text_to_convert = text_to_convert[:ib - temp_i] + "-" + ' ' * temp_i + text_to_convert[ib - temp_i:]  # вставили перенос

                    elif (text_to_convert[ib - 1 - temp_i].lower() in glasnie) and \
                            (text_to_convert[ib - temp_i].lower() not in glasnie) and \
                            (text_to_convert[ib - temp_i].lower() not in znak) and \
                            (glasnie.intersection(set(text_to_convert[ib - temp_i: word_end_index])) != {}):  # гласная, потом согласная
                        i = 0  # обнуляем, чтобы выйти из цикла и пойти на следующую строчку
                        text_to_convert = text_to_convert[:ib - temp_i] + "-" + ' ' * temp_i + text_to_convert[ib - temp_i:]  # вставили перенос
                    else:
                        i = 0  # обнуляем, чтобы выйти из цикла и пойти на следующую строчку
                        text_to_convert = text_to_convert[:word_start_index] + ' ' * reserve_before + text_to_convert[word_start_index:]  # перенос слова целиком
                    i -= 1
                    temp_i += 1
            else:
                text_to_convert = text_to_convert[:word_start_index] + ' ' * reserve_before + text_to_convert[word_start_index:]  # перенос слова целиком

        ib += 50
        ia += 50
    textLabel2.insert('1.0', text_to_convert)


# функция очистки
def delete():
    textLabel1.delete('1.0', END + '-1c')
    textLabel2.delete('1.0', END + '-1c')


# окно с текстом
textLabel1 = Text(width=50, height=20)
textLabel1.pack(side=LEFT)


# окно с текстом
textLabel2 = Text(width=50, height=20)
textLabel2.pack(side=RIGHT)


# скролл бар
scroll1 = Scrollbar(command=textLabel1.yview)
scroll1.pack(side=LEFT, fill=Y)

textLabel1.config(yscrollcommand=scroll1.set)


# скролл бар
scroll2 = Scrollbar(command=textLabel2.yview)
scroll2.pack(side=RIGHT, fill=Y)

textLabel2.config(yscrollcommand=scroll2.set)


# кнопка
buttonC = Button(text=" Convert ", command=convert)
buttonC.pack()

# кнопка
buttonD = Button(text="Delete all", command=delete)
buttonD.pack()


root.mainloop()
