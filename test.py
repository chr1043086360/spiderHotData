#######################################################################################
# Author ： CHR_崔贺然
# Time ： 2020.04.13
# TODO ： 听说pandas还能写爬虫？
# *
# !
# ?
#######################################################################################

import pandas as pd

df = pd.DataFrame()

for i in range(6):
    url = 'http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jjzc/index.phtml?p={page}'.format(
        page=i+1)
    df = pd.concat([df, pd.read_html(url)[0]])
    print("第{page}页完成~".format(page=i+1))

df.to_csv('./data.csv', encoding='utf-8', index=0)
