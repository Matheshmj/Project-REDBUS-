import pandas as pd
import streamlit as st
import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="848981",
    database="route",
    autocommit=True
)
mycursor = mydb.cursor()

# Fetch bus routes data from MySQL
sql = "SELECT * FROM bus_routes"
mycursor.execute(sql)
data = mycursor.fetchall()

# Create a DataFrame with actual column names
columns = [desc[0] for desc in mycursor.description]
df = pd.DataFrame(data, columns=columns)

# Function to format time in HH:MM:SS
def format_time_column(time_series):
    # Convert the series to timedelta, handling errors gracefully
    time_series = pd.to_timedelta(time_series, errors='coerce')
    
    # Format the time in HH:MM:SS
    formatted_times = time_series.dt.components[['hours', 'minutes', 'seconds']]
    return formatted_times.apply(lambda x: f"{int(x['hours']):02}:{int(x['minutes']):02}:{int(x['seconds']):02}", axis=1)

# Apply formatting to Start_time and End_time
df['Start_time'] = format_time_column(df['Start_time'])
df['End_time'] = format_time_column(df['End_time'])

# Streamlit application
st.title("REDBUS")
st.image("C:/Users/91848/Desktop/DATA_SCIENCE/GUVI/redbus_streamlit/elements/download (1).png", width=700)
st.write("Click here to know more: [REDBUS](https://www.redbus.in/)")

# Sidebar filters
st.sidebar.header("Filters")

# Route Name filter as selectbox
route_names = df['Route_name'].unique()
selected_route_name = st.sidebar.selectbox("Select Route Name", options=route_names)

# Price range filter
min_price, max_price = st.sidebar.slider("Price Range", 
                                          min_value=int(df['Price'].min()), 
                                          max_value=int(df['Price'].max()), 
                                          value=(int(df['Price'].min()), int(df['Price'].max())))

# Ratings range filter
min_rating, max_rating = st.sidebar.slider("Ratings Range", 
                                            min_value=1.0, 
                                            max_value=5.0, 
                                            value=(1.0, 5.0), 
                                            step=0.1)

# Availability filter (Seats Available)
min_seats, max_seats = st.sidebar.slider("Seats Available", 
                                          min_value=int(df['Seats_Available'].min()), 
                                          max_value=int(df['Seats_Available'].max()), 
                                          value=(int(df['Seats_Available'].min()), int(df['Seats_Available'].max())))

# Create a button to fetch filtered bus details
if st.button("Fetch Bus Details"):
    # Filtering data
    filtered_data = df[
        (df['Route_name'] == selected_route_name) &
        (df['Price'].between(min_price, max_price)) &
        (df['Ratings'].between(min_rating, max_rating)) &
        (df['Seats_Available'].between(min_seats, max_seats))
    ]

    # Display filtered data if any results are found
    if not filtered_data.empty:
        st.write("### Filtered Bus Details")
        st.dataframe(filtered_data)
        st.write(f"Total results: {len(filtered_data)}")
    else:
        st.write("### No results found for the selected filters.")

# Close the cursor and connection
mycursor.close()
mydb.close()
