# bosheng-cgpa-stats-2020
## Project Introduction
The purpose of this project is to automate the process for analysing the data collected from new intake students in UPM.

## Project Details
The project includes 2 python script and a streamlit app deployed to Heroku.
One is for tabulating the mean, mode, range of the CGPA of data collected from students.

The second script is to calculate the ratio of completeness for the responses collected, this is to measure the success of the event.

There are 3 output files produced from the scripts.
The first one is a csv file containing the cgpa categorised and the count, all grouped by the course.The second file is a csv file containing the tabulation of the data, including mean, mode, min, max, count of the response input data received. The third file is a csv file containing converted ratio for the completeness of the response received to the total number of students in the first batch.

The script for tabulating mean mode median has been rewritten into a streamlit app for the convenience of other users. The streamlit app are deployed using Streamlit's services, https://share.streamlit.io/ganthology/bosheng-cgpa-stats-2020/main/analysis.py.

The input and output file format for this app is .csv format.

## Event Details
The event is to collect data from new intake students in UPM, analyzed and upload the results to various websites for students to make reference when filling their choices of university in UPU system.

## Dependencies
This project uses python 3 as the language. streamlit, base64, pandas and numpy library are used in the project.

## Author
The owner of this project is Gan Boon Kit, the committee responsible for the event in the club.
