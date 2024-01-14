# Airbnb Analysis

## Domain : Travel Industry

## Problem Statement: 
This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends 

## About:
  This project is about extracting the data from the MongoDB database with python scripting and use premeasures to clean and preprocess the data
and then use the available data to analyze the pricing, where the hotel rooms are located and the reviews of the place. Using geo maps and othe ploting tools to visualise the data and use other visualisation tools like PowerBI to create a dynamic dashboard for efective analysis.

## Technologies Used
1. Python
2. MongoDB Atlas
3. Pymongo
4. Streamlit
5. Plotly Express
6. Matplotlib
7. Pandas

## Pre Processing the Data
The data was stored in mongoDB atlas, We have to create a cluster to connect to the database and extract the data using python scripting.
Then we use pandas to pre process the data like finding and removing the blank columns and use appropriate measures to fill the data.
After that we use matplotlib to plot some graph to analyse the data which going to be working or throw some error. If the data has outliers we should remove it before we start analysing.

##Process Steps:
Step-1:
As the first step make a streamlit app with three pages With Home page, Extraction page, Explore page.

Step-2:
Use functional blocks to define the code and use it whereever it has to be used,
Iam Creating codes for connecting to database, and preprocess the data, then examine the data, and to optimise the data.

Step-3:
In the extract page I used to give four buuttons like connect to database, then extract the data, Then examine the data,
While examining the data I created scatter plot against the price will all other numerical columns to check if there is some outliers.

Step-4:
In this step I use fourth button to optimise the data which is going to remove outliers for us to optimse the data to be used.

Step-5:
Then in the explore page I created visuals and geo maps for visualisation of the data.

Step-6:
After the streamlit app creation the data extracted is saved in the same folder as the base code file available.
I use PowerBI to analyse and create a dynamic dashboard for price analysis. I have given the dashboard file in this repository for everyone to see.

![image](https://github.com/praks8870/Airbnb_Analysis/blob/main/PowerBI_Dashboard.png)
