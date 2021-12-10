import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import os
import os.path as osp

# ROOT_PAHT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# FRONT_PATH = osp.join(ROOT_PAHT, 'front')
# UTILS_PATH = osp.join(ROOT_PAHT, 'utils')
#
# books = [['计算机体系结构', '', '人民邮电出版社', '', '', '计算机', 3],
#         ['Python编程', '', '人民邮电出版社', '', '', '计算机', 4],
#         ['数据库系统概论', '', '人民邮电出版社', '', '王珊，萨师煊', '计算机', 2],
#         ]
# users = [['John', 1, '562372'],
#          ['Mike', 0, '783560'],
#          ['Python', 0, '700231'],
#         ]
# index = list(range(3))
# book_df = DataFrame(data=books, columns=['book_name','ISBN','publisher','publish_date','author','label','total_number'],\
#           index=index)
# user_df = DataFrame(data=users, columns=['user_name','user_type','tele',],\
#           index=index)
# book_df.to_csv('books.csv')
# user_df.to_csv('user.csv')
#
# book_df = pd.read_csv(osp.join(UTILS_PATH, 'books.csv'))
# print(type(book_df.ISBN[0]))
# print(book_df.ISBN[0])
# print(type(np.float64('nan')))
# print(np.float64('nan'))
# print(pd.isnull(book_df.ISBN[0]))



