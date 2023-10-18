import pandas as pd

df = pd.read_excel('Login.xlsx')

list = ['apple', 'car']
length = len(df.index)
df.loc[length] = list
print(df)






# def a(x, y):
#     print(x, y)
#
#
# def b(function, *args, **kwargs):
#     function(*args, **kwargs)
#
#
# b(a, 'hello', 'dude')
