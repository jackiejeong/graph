import tkinter as tk
from tkinter import filedialog
from loadsave import Load, Save

if __name__ == '__main__':
    root = tk.Tk()
    root.title('정량분석')
    root.geometry('300x300+100+100')
    root.resizable(False,False)
    
    불러오기bt = tk.Button(root, text = '불러오기', overrelief = 'solid', width = 10, command = Load)
    불러오기bt.pack()
    저장bt = tk.Button(root, text = '저장', overrelief = 'solid', width = 10, command = Save)
    저장bt.pack()
    전처리bt = tk.Button(root, text = '데이터 전처리', overrelief = 'solid', width = 10)
    전처리bt.pack()
    그래프bt = tk.Button(root, text = '그래프 생성', overrelief = 'solid', width = 10)
    그래프bt.pack()
    지도bt = tk.Button(root, text = '지도 생성', overrelief = 'solid', width = 10)
    지도bt.pack()
    불러오기bt.place(x = 20, y = 20)
    저장bt.place(x = 20, y = 60)
    전처리bt.place(x = 200, y = 20)
    그래프bt.place(x = 200, y = 60)
    지도bt.place(x = 200, y = 100)

    root.mainloop()

