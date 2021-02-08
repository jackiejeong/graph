import tkinter
from tkinter import filedialog

창 = tkinter.Tk()
창.title('정량분석')
창.geometry('300x300+100+100')
창.resizable(False,False)

def Load():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("Python files","*.py"),
                                          ("all files", "*.*")))
    print(filename)

def Save():
    filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                          filetypes=(("Python files","*.py"),
                                          ("all files", "*.*")))
    print(filename)

불러오기bt = tkinter.Button(창, text = '불러오기', overrelief = 'solid', width = 10, command = Load)
불러오기bt.pack()

저장bt = tkinter.Button(창, text = '저장', overrelief = 'solid', width = 10, command = Save)
저장bt.pack()

전처리bt = tkinter.Button(창, text = '데이터 전처리', overrelief = 'solid', width = 10)
전처리bt.pack()

그래프bt = tkinter.Button(창, text = '그래프 생성', overrelief = 'solid', width = 10)
그래프bt.pack()


불러오기bt.place(x = 20, y = 20)
저장bt.place(x = 20, y = 60)
전처리bt.place(x = 200, y = 20)
그래프bt.place(x = 200, y = 60)



창.mainloop()