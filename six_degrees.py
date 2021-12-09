import pandas as pd
from collections import deque
import numpy as np
import tkinter as tk
from tkinter import ttk
import warnings

warnings.filterwarnings("ignore", message="DataFrame columns are not unique")

# Read data
data = pd.read_csv('YouTubers.csv')
data = data.replace(np.nan, '', regex=True)
data['Associates'] = data.Associates.apply(lambda x: x[1:-1].strip("\'").split('\', \''))
result = data.set_index('YouTuber').T.to_dict(orient='records')[0]

'''
BFS search for path between two YouTubers.
'''
def connect(graph, person1, person2):
    queue = deque()
    parents = {}
    explored = []
    queue.append((person1, [person1]))
    while queue:
        cur, path = queue.popleft()
        explored.append(cur)
        if cur in result:
            for i in result[cur]:
                if i == person2:
                    return path + [i]
                else:
                    if i not in explored:
                        explored.append(i)
                        queue.append((i, path + [i]))       
    return path


'''
Output path between two YouTubers.
'''           
def showResult(path, person2):
    output = ""
    if len(path) == 0 or path[len(path)-1] != person2:
        return "No connection found"
    else:
        for i in range(len(path)-1):
            output += (path[i] + " --> ")
        return output + path[len(path)-1]


'''
Window setup
'''
window = tk.Tk()
window.geometry('600x250')
window.title('Six Degrees of Minecraft YouTubers (and then some)')

label1 = ttk.Label(window, text="YouTuber 1:")
label1.grid(column=0, row=0)
label2 = ttk.Label(window, text="YouTuber 2:")
label2.grid(column=0, row=1)

combo1 = ttk.Combobox(window, textvariable=tk.StringVar(), values=data['YouTuber'].tolist(), state='readonly')
combo1.grid(column=1, row=0)
combo2 = ttk.Combobox(window, textvariable=tk.StringVar(), values=data['YouTuber'].tolist(), state='readonly')
combo2.grid(column=1, row=1)
submit = ttk.Button(window, text ="Go")
submit.grid(column=1, row=3)

output = ttk.Label(window, text="", justify="left")
output.grid(row=4, columnspan=2)

current = ['',''] # Holds the current combobox values

'''
* retrieve - get current combobox values
* check    - calculate the path between two YouTubers from combobox values
* on_closing - handle window close
'''
def retrieve(event):
    current[0] = combo1.get()
    current[1] = combo2.get()
    
def check(event):
    if current[0] == '' or current[1] == '':
        return None
    else:
        path = connect(result, current[0],current[1])
        output.labelText = showResult(path,current[1])
        output.config(text=output.labelText)
def on_closing():
    window.destroy()

# Widget bindings 
combo1.bind('<<ComboboxSelected>>', retrieve)
combo2.bind('<<ComboboxSelected>>', retrieve)
submit.bind('<Button-1>', check)
window.protocol("WM_DELETE_WINDOW", on_closing)

# Main loop
window.mainloop()