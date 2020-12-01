import pandas as pd
import numpy as np

filename = '2020_2021 大学新生入学积分调查表格 (Responses) - Form Responses 1.csv'
responseDf = pd.read_csv(filename)
batch = '请问你是今年第一批入学的新生吗？ (无经过任何上诉管道以及根据大学录取通知书)' 
course = '科系 (只选择一个来填写）'
trimmedDf = responseDf[[course, batch]]
trimmedDf.rename(columns={'请问你是今年第一批入学的新生吗？ (无经过任何上诉管道以及根据大学录取通知书)':'batch',
                        '科系 (只选择一个来填写）':'course'}, inplace=True)

#Only first batch are considered
firstBatchOnlyDf = trimmedDf[trimmedDf.batch == '是 Ya'] 
#Drop rows containing null value/unfilled
firstBatchOnlyDf.dropna(inplace=True)
firstBatchOnlyDf['course'] = firstBatchOnlyDf['course'].astype('str')
firstBatchOnlyDf[['code','course']] = firstBatchOnlyDf['course'].str.split(" ", 1, expand=True)

#print(firstBatchOnlyDf.head(5))
#print(firstBatchOnlyDf.info())
cleanDf = firstBatchOnlyDf[['course']]
groupedDf = cleanDf.groupby(['course']).agg({'course':['count']})
groupedDf.columns = ['totalCollect']
#print(groupedDf.head(5))

totalFilename = '20_21 积分收集 - Sheet1.csv'
totalDf = pd.read_csv(totalFilename)
totalDf = totalDf[['科系名称（巫）','科系华裔生人数']]
totalDf.rename(columns={'科系名称（巫）':'course',
                         '科系华裔生人数':'totalChinese'}, inplace=True)
#totalDf = totalDf.groupby(['course'])

newDf = pd.merge(groupedDf,totalDf,how='left', on=['course'])
#print(newDf.head())

resultNp = newDf.to_numpy()
print(resultNp)
回收率 = (resultNp[:,1].astype(np.float))/(resultNp[:,2].astype(np.float))*100
回收率 = np.round(回收率,2)
print(回收率)
finalNp = np.column_stack((resultNp,回收率))
print(finalNp)

finalDf = pd.DataFrame(finalNp, columns=['Course', 'Total Collected', 'Total Chinese', '回收率'])
print(finalDf.head(5))

path = '/home/gan1386/Documents/博升-积分调查/'

outputFilename = '回收率.csv'
finalDf.to_csv(path+outputFilename)