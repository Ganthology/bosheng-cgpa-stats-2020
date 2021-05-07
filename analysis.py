import streamlit as st
import pandas as pd
import base64

"""
# 博升Bosheng CGPA Tabulation App

## Upload Section
"""

file = st.file_uploader("Upload Files", type=['csv'])
if file:
    df = pd.read_csv(file)

    df.info()

    COLUMNS = list(df.columns)
    COLUMN_LEN = len(COLUMNS)
    st.write("""
    ## Columns Name
    """)
    COLUMNS

    """
    ## Data Processing Section
    Choose the correct column name for each column type specified
    """
    # new_intake = st.number_input('New Intake Column', min_value=0, max_value=COLUMN_LEN-1)
    # course = st.number_input("Course Column", min_value=0, max_value=COLUMN_LEN-1)
    # preUni = st.number_input("Type of Pre Uni Course Column", min_value=0, max_value=COLUMN_LEN-1)
    # cgpa = st.number_input("CGPA pointer column", min_value=0, max_value=COLUMN_LEN-1)

    new_intake = st.selectbox('New Intake Column', COLUMNS)
    course = st.selectbox("Course Column", COLUMNS)
    preUni = st.selectbox("Type of Pre Uni Course Column", COLUMNS)
    cgpa = st.selectbox("CGPA Pointer Column", COLUMNS)

    columns_needed = [new_intake, course, preUni, cgpa]

    df = df.loc[:, columns_needed]
    st.write(df.head())

    # Data cleaning
    firstBatchOnlyDf = df[df[new_intake] == '是 Ya'].dropna()

    df = df[[course, preUni, cgpa]]
    df[cgpa] = pd.to_numeric(df[cgpa])


    groupedDf = df.groupby([course,preUni]).agg({ cgpa:['count', 'mean', 'min', 'max'] })
    groupedDf.columns = ['totalCount','mean','min','max']
    groupedDf['mean'] = groupedDf['mean'].round(3)

    modeDf = df.groupby([course, preUni]).agg(pd.Series.mode)
    modeDf.columns = ['mode']

    modeListDf = df.groupby([course, preUni, cgpa]).agg({cgpa:['count']})
    modeListDf.columns = ['count']

    modeCountDf = modeListDf.groupby([course, preUni]).agg({'count':['max']})
    modeCountDf.columns = ['modeCount']

    finalDf = pd.concat([groupedDf, modeDf], axis=1)
    finalDf = pd.concat([finalDf,modeCountDf], axis=1)

    def final_results_download_link(df):
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}" download="Results.csv">Download the csv file</a>'
        return href

    def mode_download_link(df):
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}" download="Mode.csv">Download the csv file</a>'
        return href


    """
    ## Download Section

    Download this file to get the tabulated statistics.
    """
    st.markdown(final_results_download_link(finalDf.reset_index()), unsafe_allow_html=True)
    st.write(finalDf.reset_index().head())
    """
    Download this file to cross check the mode of each courses.
    """
    st.markdown(mode_download_link(modeListDf.reset_index()), unsafe_allow_html=True)
    st.write(modeListDf.reset_index().head())




