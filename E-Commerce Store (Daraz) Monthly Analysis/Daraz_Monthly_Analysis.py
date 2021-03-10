import numpy as np
import pandas as pd
from io import StringIO, BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('finance.export.order-item-transaction 2021-03-03.csv')   #add file name here
# print(df.head())
df = df.drop(['Lazada SKU', 'Statement', 'Paid Status', 'Order Item No.', 'Order Item Status', 'Shipping Provider',
             'Shipping Speed', 'Shipment Type', 'Reference', 'Comment', 'PaymentRefId', 'PaymentRefId', 'Reference',
              'Transaction Date', 'Transaction Type', 'Fee Name', 'Transaction Number', 'Details', 'WHT Amount',
              'WHT included in Amount'], axis=1)

# print(df.head())
# df.to_csv('clean_data.csv', index=False)
newDf = pd.DataFrame({"Seller SKU": [1],
                      "Amount": [1],
                      "Order No.": [1]})
amount = 0
temp = df.iloc[0]['Order No.']
for i in range(df.shape[0]):

    if df.iloc[i]['Order No.'] == temp:
        amount += df.iloc[i]['Amount'] - df.iloc[i]['VAT in Amount']
    else:
        sSku = df.iloc[i-1]['Seller SKU']
        df2 = pd.DataFrame({"Seller SKU": [sSku],
                            "Amount": [amount],
                            "Order No.": [temp]})
        newDf = newDf.append(df2, ignore_index=True)
        temp = df.iloc[i]['Order No.']
        amount = 0
newDf = newDf.drop([0])
newDf.to_csv('TOTAL_ITEMS_SOLD.csv', index=False)


srs = newDf['Seller SKU'].value_counts()
x_axis = srs.index.tolist()
y_axis = srs.values
print(srs)
sns.set_theme(style="whitegrid")
# sns.barplot(x_axis, y_axis)
ax = sns.barplot(x=x_axis, y=y_axis)
#plt.show()
d = {"Seller SKU": x_axis, "Amount": np.zeros(len(x_axis))}
pDf = pd.DataFrame(data=d)


for i in range(newDf.shape[0]):
    for j in range(pDf.shape[0]):
        if newDf.iloc[i]["Seller SKU"] == pDf.iloc[j]["Seller SKU"]:
            temp = newDf.iloc[i]["Amount"]
            pDf.at[j, 'Amount'] += temp

pDf.to_csv('REVENUE.csv', index=False)
pDf.plot(x='Seller SKU', y='Amount', kind='bar')
plt.show()




