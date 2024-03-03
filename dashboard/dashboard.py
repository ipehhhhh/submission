import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import calendar

# Importing Databases
path = os.path.dirname(__file__)
data1_path = os.path.join(path, r"main_data_Changping.csv")
Changping_df = pd.read_csv(data1_path)

path = os.path.dirname(__file__)
data2_path = os.path.join(path, r"main_data_Dongsi.csv")
Dongsi_df = pd.read_csv(data2_path)

# Merge databases
merge_database = pd.concat([Changping_df, Dongsi_df])

# Save merged data to main_data.csv
merge_database.to_csv(r'main_data.csv', index=False)

# Study Case 1: Question, Visualization, Conclusion
def Case1():
    # Mean of PM10 in every month
    monthly_avg_pm10 = Changping_df.groupby('month')['PM10'].mean()

    # highest and lowest PM10 
    highest_month = monthly_avg_pm10.idxmax()
    highest_value = monthly_avg_pm10.max()
    lowest_month = monthly_avg_pm10.idxmin()
    lowest_value = monthly_avg_pm10.min()

    # Plotting monthly tren of PM10
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(monthly_avg_pm10.index, monthly_avg_pm10.values, marker='o', color='navy')
    ax.set_title('Monthly Average PM10 Trend in Changping')
    ax.set_xlabel('Month')
    ax.set_ylabel('Average PM10')

    # Display lowest and highest PM10 value
    ax.scatter(highest_month, highest_value, color='red', label=f'Highest: {highest_value:.2f}', s=100, edgecolor='black', linewidth=1.5)
    ax.scatter(lowest_month, lowest_value, color='green', label=f'Lowest: {lowest_value:.2f}', s=100, edgecolor='black', linewidth=1.5)

    ax.legend()

    # Convert numerical value to the month value
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([calendar.month_name[i] for i in range(1, 13)], rotation=45)

    plt.tight_layout()

    # Display plot
    st.pyplot(fig)

    st.subheader("Conclusion for Question 1:")
    st.write("Based on the data analysis, it can be observed that there is a significant change in air quality conditions, particularly in the PM10 data, for each month in the year 2015 at Changping Station. The lowest air quality occurred in March 2015, while the best air quality was recorded in August 2015. Further analysis of the data can be conducted incorporating additional parameters such as the Rain feature to explore correlations as potential factors influencing variations in air quality.")
            
# Study Case 2: Question, Visualization, Conclusion
def Case2():
    # Mean of CO
    mean_co_changping = Changping_df['CO'].mean()
    mean_co_dongsi = Dongsi_df['CO'].mean()

    # Visualize the comparison
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(['Changping', 'Dongsi'], [mean_co_changping, mean_co_dongsi], color=['blue', 'green'])
    ax.set_title('Comparison of Average CO Levels at Changping and Dongsi Stations')
    ax.set_xlabel('Station')
    ax.set_ylabel('Average CO Level')

    # Display plot
    st.pyplot(fig)

    # Visualization of CO distribution using histogram
    fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
    ax_hist.hist(Changping_df['CO'], bins=30, alpha=0.5, label='Changping', color='blue')
    ax_hist.hist(Dongsi_df['CO'], bins=30, alpha=0.5, label='Dongsi', color='green')
    ax_hist.set_title('Distribution of CO Levels at Changping and Dongsi Stations')
    ax_hist.set_xlabel('CO Level')
    ax_hist.set_ylabel('Frequency')
    ax_hist.legend()

    # Display plot
    st.pyplot(fig_hist)

    # Convert 'year', 'month', and 'day' features to datetime data type
    Changping_df['date'] = pd.to_datetime(Changping_df[['year', 'month', 'day']])
    Dongsi_df['date'] = pd.to_datetime(Dongsi_df[['year', 'month', 'day']])

    # Grouping datas by year and calculate the average of CO 
    Changping_yearly = Changping_df.groupby(Changping_df['date'].dt.year)['CO'].mean()
    Dongsi_yearly = Dongsi_df.groupby(Dongsi_df['date'].dt.year)['CO'].mean()

    # Yealy trend
    fig_yearly, ax_yearly = plt.subplots(figsize=(12, 6))
    ax_yearly.plot(Changping_yearly.index, Changping_yearly.values, label='Changping', color='blue', marker='o')
    ax_yearly.plot(Dongsi_yearly.index, Dongsi_yearly.values, label='Dongsi', color='green', marker='o')
    ax_yearly.set_title('Time Trend of Average CO Levels at Changping and Dongsi (per Year)')
    ax_yearly.set_xlabel('Year')
    ax_yearly.set_ylabel('Average CO Level')
    ax_yearly.legend()
    ax_yearly.grid(True)

    # Display plot
    st.pyplot(fig_yearly)

    st.subheader("Conclusion for Question 2:")
    st.write("Subsequent to visualizing and analyzing the data, it is evident that there is a substantial disparity in the levels of CO or carbon monoxide between Changping Station and Dongsi Station in the year 2013, with the gap gradually diminishing by the year 2017.")

# Study Case 3: Question, Visualization, Conclusion
def Case3():
    # Convert 'year', 'month', and 'day' features to datetime data type
    Dongsi_df['date'] = pd.to_datetime(Dongsi_df[['year', 'month', 'day']])

    # Filter data for November 2014 to January 2015
    start_date = '2014-11-01'
    end_date = '2015-01-28'  # Changed 30 to 28 because February has only 28 days
    filtered_df = Dongsi_df[(Dongsi_df['date'] >= start_date) & (Dongsi_df['date'] <= end_date)]

    # Visualize the relationship between air pollution levels and air temperature
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(x='TEMP', y='PM2.5', data=filtered_df, label='PM2.5', alpha=0.5, ax=ax)
    sns.scatterplot(x='TEMP', y='PM10', data=filtered_df, label='PM10', alpha=0.5, ax=ax)
    plt.title('Relationship between Air Pollution Levels and Air Temperature (Nov 2014 - Jan 2015)')
    plt.xlabel('Air Temperature (°C)')
    plt.ylabel('Air Pollution Level (PM2.5 / PM10)')
    plt.legend()
    plt.grid(True)

    # Display the plot using st.pyplot
    st.pyplot(fig)

    # Calculate correlation matrix
    correlation_matrix = filtered_df[['PM2.5', 'PM10', 'TEMP']].corr()

    st.subheader("Correlation Matrix:")
    st.dataframe(correlation_matrix)

    # Visualize correlation matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='twilight', fmt=".2f")
    plt.title('Correlation Matrix between PM2.5, PM10, and Temperature')
    plt.show()

    st.subheader("Conclusion for Question 3:")
    st.write("The correlation or relationship between air quality, represented by the PM2.5 and PM10 features, and temperature demonstrates a negative correlation.")

# Sidebar layout
st.sidebar.title("Options")

# Data Distribution Display
def display_data_hist(data):
    """
    Display the distribution of the selected data.

    Parameters:
        data (DataFrame): The DataFrame containing the data to be displayed.
    """
    st.subheader("Data Distribution:")
    st.text(data.describe())

# Data Description
def display_data_description(data):
    """
    Display the description of the selected data.

    Parameters:
        data (DataFrame): The DataFrame containing the data to be displayed.
    """
    st.subheader("Data Description:")
    st.text(data.describe())

# Select Dabase from Station
st.sidebar.header("Sort Data")
station_name = st.sidebar.radio("Select Data", ("Changping", "Dongsi"))
dataFeatures = st.sidebar.multiselect("Select Columns to Display", Changping_df.columns)

# Feature 2: Question and Visualization
st.sidebar.header("Explore Data")
StudyCase = st.sidebar.selectbox("Select a Question", ("Question 1", "Question 2", "Question 3"))

# Main content
st.title("Air Quality Analysis")

if station_name == "Changping":
    dataframe = Changping_df
else:
    dataframe = Dongsi_df

# Display sorted data or selected function
if station_name:
    st.subheader("Selected Data:")
    st.write(dataframe[dataFeatures])

# Display selected question and visualization
if StudyCase == "Question 1":
    st.subheader("Question 1: ")
    st.subheader("How did the air quality conditions change based on the PM2.5 data each month in 2015 at the Changping Station?")
    #st.write("")
    Case1()

elif StudyCase == "Question 2":
    st.subheader("Question 2:")
    st.subheader("How is the comparison of carbon monoxide levels in the air at Changping Station and Dongsi Station?")
    #st.write("Is there a correlation between operating hours and air quality based on PM 2.5 and O3 levels?")
    Case2()

elif StudyCase == "Question 3":
    st.subheader("Question 3: ")
    st.subheader("What is the correlation between air pollution levels (represented by PM2.5 and PM10) and air temperature (TEMP) from November 2014 to January 2015 at Dongsi Station?")
    #st.write("How does the O3 level vary from year to year at Changping and Dongsi stations?")
    Case3()

# Feature 3: Data Info
st.sidebar.header("Data Info")
dataInfo = st.sidebar.selectbox("View Data Info", ("Data Distribution", "Data Description"))

if dataInfo == "Data Distribution":
    st.subheader("Data Distribution:")
    st.write(dataframe)

elif dataInfo == "Data Description":
    st.subheader("Data Description:")
    st.dataframe(dataframe.describe().round(2))


