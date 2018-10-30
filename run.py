from tkinter import *
import hashlib
from Crypto.Cipher import DES
from tkinter import filedialog


crypkey = b'CryptKey'

x = 0

def insertText():
    file_name = filedialog.askopenfilename()
    f = open(file_name, 'rb')
    string = f.read()
    des = DES.new(crypkey, DES.MODE_ECB)
    string = des.decrypt(string)
    string = string.decode()
    #text.delete(0, END)
    text.insert(1.0, string)
    f.close()


def extractText():
    file_name = filedialog.asksaveasfilename(filetypes=(("DAT files", "*.dat"),
                                                ("All files", "*.*")))
    f = open(file_name, 'wb')
    des = DES.new(crypkey, DES.MODE_ECB)
    string = text.get(1.0, END)
    string = bytes(string, 'utf-8')
    while len(string) % 8 != 0:
        string += b' '
    string = des.encrypt(string)
    f.write(string)
    f.close()



def contin(event):
    global crypkey, x
    crypkey = key.get()
    print(len(crypkey) == 9)
    crypkey = bytes(crypkey, 'utf-8')
    if len(crypkey) != 9:
        newind.destroy()
        print('Уничтожение окна')
        x = 1
    else:
        print(len(crypkey) != 9)
        print('Введите ключ с числом символов равным восьми')


def lgreater(text):
    while len(text) % 8 != 0:
        text += b' '
    return text


def addme(event):
    print('Добавить')
    uget = user.get()
    paget = password.get()
    if uget == '' or paget == '':
        print('Невозможно добавить пользователя без имени или пароля')
        vyv.delete(0, END)
        vyv.insert(0, 'Невозможно добавить пользователя без имени или пароля')
    if len(uget) < 3:
        print('Невозможно добавить пользователя - размер меньше 3-х символов')
        vyv.delete(0, END)
        vyv.insert(0, 'Невозможно добавить пользователя - размер меньше 3-х символов')
    else:
        fo = open('check.dat', 'rb')
        passlist = []
        text = fo.read()
        des = DES.new(crypkey, DES.MODE_ECB)
        text = des.decrypt(text)
        text = text.decode('utf-8')
        fo.close()
        passlist = text.split('|')
        for pl in passlist:
            pl = pl.split(' ')
            # if string[1] == uget:
            #   print('Такой пользователь уже существует')
            #  vyv.delete(0, END)
            # vyv.insert(0, 'Такой пользователь уже существует')
            # fo.close()
            # return 0
        fo.close()

        f = open('check.dat', 'ab')
        hash = paget
        hash = hash.encode('utf-8')
        hash = hashlib.sha1(hash).hexdigest()

        text = '|1 ' + uget + ' ' + hash

        des = DES.new(crypkey, DES.MODE_ECB)
        text = bytes(text, encoding='utf-8')
        text = lgreater(text)
        text = des.encrypt(text)
        print(text)

        f.write(text)
        vyv.delete(0, END)
        vyv.insert(0, 'Пользователь добавлен')


def check(event):
    print('Проверка подлинности...')
    uget = user.get()
    paget = password.get()
    # print(uget + ' ' + paget)
    f = open('check.dat', 'rb')
    # passlist = []
    if uget == '' or paget == '':
        print('Невозможно проверить пользователя без имени или пароля')
        vyv.delete(0, END)
        vyv.insert(0, 'Невозможно проверить пользователя без имени или пароля')
    if len(uget) < 3:
        print('Невозможно проверить пользователя - размер меньше 3-х символов')
        vyv.delete(0, END)
        vyv.insert(0, 'Невозможно проверить пользователя - размер меньше 3-х символов')
    string = f.read()
    print(string)
    print('Point')
    print(uget)
    print(paget)
    des = DES.new(crypkey, DES.MODE_ECB)
    string = des.decrypt(string)
    string = string.decode()
    # print(string)
    string = string.split('|')
    # print(string)
    datab = []
    for data in string:
        datab.append(data.split())
        value = 0
    for spl in datab:
        value += 1
        print(value)
        try:
            if spl[1] == uget:
                if hashlib.sha1(paget.encode('utf-8')).hexdigest() == spl[2] and spl[0] == '0':
                    print('Совпадение пароля и имени')
                    print('Хэш-сумма пароля пользователя ' + spl[2])
                    vyv.delete(0, END)
                    vyv.insert(0, 'Добро пожаловать, пользователь')

                    root.destroy()
                    return 0
                if hashlib.sha1(paget.encode('utf-8')).hexdigest() == spl[2] and spl[0] == '1':
                    print('Совпадение пароля и имени администратора')
                    print('Хэш-сумма пароля ' + spl[2])
                    vyv.delete(0, END)
                    vyv.insert(0, 'Вход администратора')

                    root.destroy()
                    return 0

        except:
            pass
    print('Неверный пароль')
    vyv.delete(0, END)
    vyv.insert(0, 'Неверный пароль')

    f.close()
    return 0



root = Tk()
root.title("База данных")
root.geometry('180x180')

user = Entry(root, width=20, bd=2)
Label(root, text='Пользователь:').pack()
user.pack()
Label(root, text='Пароль:').pack()
password = Entry(root, width=20, bd=2, show="*")
password.pack()

button1 = Button(root, text='Авторизация')
button1.bind('<Button-1>', check)
button1.pack()

button2 = Button(root, text='Добавить пользователя')
button2.bind('<Button-1>', addme)
button2.pack()

vyv = Entry(root, width=125, bd=2)
vyv.pack()

Label(root, text='\n').pack()

root.mainloop()

if 1 == 1:
    newind = Tk()

    newind.title('Выбор действия')
    newind.geometry('165x100')

    Label(newind, text='Введите свой ключ:').pack()

    key = Entry(newind, width=150, bd=2)
    key.pack()

    decr = Button(newind, text='Продолжить')
    decr.bind('<Button-1>', contin)
    decr.pack()


    newind.mainloop()


if x == 1:
    fw = Tk()
    text = Text(width=50, height=25)
    text.grid(columnspan=2)
    b1 = Button(text="Открыть", command=insertText)
    b1.grid(row=1, sticky=E)
    b2 = Button(text="Сохранить", command=extractText)
    b2.grid(row=1, column=1, sticky=W)

    fw.mainloop()
