import pandas as pd

# filename = '2020_2021 大学新生入学积分调查表格 (Responses) - Form Responses 1.csv'
# responseDf = pd.read_csv(filename)
filename = '2020_2021 大学新生入学积分调查表格 (Responses).csv'
responseDf = pd.read_csv(filename)
#Show total response we collected
print(responseDf.info())
#Only 4 columns containing useful information
batch = '请问你是今年第一批入学的新生吗？ (无经过任何上诉管道以及根据大学录取通知书)' 
course = '科系 (只选择一个来填写）'
preUni = '进入大学的管道'
cgpa = '平均累计积分 CGPA '
trimmedDf = responseDf[[batch, course, preUni, cgpa]]
trimmedDf.rename(columns={'请问你是今年第一批入学的新生吗？ (无经过任何上诉管道以及根据大学录取通知书)':'batch',
                        '科系 (只选择一个来填写）':'course',
                        '进入大学的管道':'preUni',
                        '平均累计积分 CGPA ':'cgpa'}, inplace=True)

print(trimmedDf.info())

#Only first batch are considered
firstBatchOnlyDf = trimmedDf[trimmedDf.batch == '是 Ya'] 
print(firstBatchOnlyDf.info())
#Drop rows containing null value/unfilled
firstBatchOnlyDf.dropna(inplace=True)
print(firstBatchOnlyDf.info())

cleanDf = firstBatchOnlyDf[['course', 'preUni', 'cgpa']]
cleanDf['cgpa'] = pd.to_numeric(cleanDf['cgpa'])
print(cleanDf.dtypes)
#cleanDf.insert(3, 'mode','')

groupedDf = cleanDf.groupby(['course','preUni']).agg({'cgpa':['count', 'mean', 'min', 'max']})
groupedDf.columns = ['totalCount','mean','min','max']
groupedDf['mean'] = groupedDf['mean'].round(3)

modeDf = cleanDf.groupby(['course', 'preUni']).agg(pd.Series.mode)
modeDf.columns = ['mode']
#modeDf.drop(columns='course', inplace=True)
#modeDf.rename(columns={'cgpa':'modeCgpa'}, inplace=True)

modeListDf = cleanDf.groupby(['course','preUni','cgpa']).agg({'cgpa':['count']})
modeListDf.columns = ['count']

modeCountDf = modeListDf.groupby(['course','preUni']).agg({'count':['max']})
modeCountDf.columns = ['modeCount']
#modeCountDf = modeCountDf.drop(modeCountDf.iloc[:, 0:2], axis=1)


finalDf = pd.concat([groupedDf, modeDf], axis=1)
finalDf = pd.concat([finalDf,modeCountDf], axis=1)

path = '/home/gan1386/Documents/bosheng-cgpa-stats-2020/'

modeOutput = 'modeListNew.csv'
modeListDf.to_csv(path+modeOutput)

output = 'finalResultsNew.csv'
finalDf.to_csv(path+output)
