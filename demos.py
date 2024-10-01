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
sql = "SELECT * FROM buses_routes"
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

# Sidebar to navigate between pages
page = st.sidebar.radio("Select Page", ["Home", "Bus Details"])

# Home Page
if page == "Home":
    st.image("C:/Users/91848/Desktop/DATA_SCIENCE/GUVI/redbus_streamlit/elements/download (1).png", width=700)
    st.write("Click here to know more: [REDBUS](https://www.redbus.in/)")

# Bus Details Page
elif page == "Bus Details":
    st.header("Bus Route and Details")

    # Sidebar filters
    st.sidebar.header("Filters")

    # Step 1: Select State
    state_names = df['State'].unique()  # Updated from 'State_name' to 'State'
    selected_state_name = st.sidebar.selectbox("Select State Name", options=state_names)

    # Step 2: Filter route names based on the selected state
    filtered_routes_by_state = df[df['State'] == selected_state_name]  # Filter routes for the selected state
    route_names = filtered_routes_by_state['Route_name'].unique()  # Get unique routes in the selected state

    # Step 3: Select Route Name
    selected_route_name = st.sidebar.selectbox("Select Route Name", options=route_names)

    # Step 4: Price range filter
    min_price, max_price = st.sidebar.slider("Price Range", 
                                              min_value=int(filtered_routes_by_state['Price'].min()), 
                                              max_value=int(filtered_routes_by_state['Price'].max()), 
                                              value=(int(filtered_routes_by_state['Price'].min()), int(filtered_routes_by_state['Price'].max())))

    # Step 5: Ratings range filter
    min_rating, max_rating = st.sidebar.slider("Ratings Range", 
                                                min_value=1.0, 
                                                max_value=5.0, 
                                                value=(1.0, 5.0), 
                                                step=0.1)

    # Step 6: Availability filter (Seats Available)
    min_seats, max_seats = st.sidebar.slider("Seats Available", 
                                              min_value=int(filtered_routes_by_state['Seats_Available'].min()), 
                                              max_value=int(filtered_routes_by_state['Seats_Available'].max()), 
                                              value=(int(filtered_routes_by_state['Seats_Available'].min()), int(filtered_routes_by_state['Seats_Available'].max())))

    # Display the filtered data based on the sidebar inputs
    filtered_data = filtered_routes_by_state[
        (filtered_routes_by_state['Route_name'] == selected_route_name) &
        (filtered_routes_by_state['Price'].between(min_price, max_price)) &
        (filtered_routes_by_state['Ratings'].between(min_rating, max_rating)) &
        (filtered_routes_by_state['Seats_Available'].between(min_seats, max_seats))
    ]

    # **Main Frame**: Bus Type and Departing Time Filters with Empty Dropdowns
    st.write("### Select Bus Type and Time")

    # Step 7: Filter by Bus Type (in the main frame with an empty option)
    bus_types = filtered_routes_by_state['Bus_type'].unique()  # Get unique bus types in the selected state
    selected_bus_type = st.selectbox("Bus Type", options=[""] + list(bus_types), index=0)

    # Step 8: Filter by Departing Time (Start_time) (in the main frame with an empty option)
    filtered_routes_by_bus_type = filtered_routes_by_state[filtered_routes_by_state['Bus_type'] == selected_bus_type] if selected_bus_type else filtered_routes_by_state
    start_times = filtered_routes_by_bus_type['Start_time'].unique()
    selected_start_time = st.selectbox("Departing Time", options=[""] + list(start_times), index=0)

    # Filter the data only if both Bus Type and Start Time are selected (non-empty)
    if selected_bus_type and selected_start_time:
        filtered_data = filtered_routes_by_bus_type[
            (filtered_routes_by_bus_type['Route_name'] == selected_route_name) &
            (filtered_routes_by_bus_type['Start_time'] == selected_start_time) &
            (filtered_routes_by_bus_type['Price'].between(min_price, max_price)) &
            (filtered_routes_by_bus_type['Ratings'].between(min_rating, max_rating)) &
            (filtered_routes_by_bus_type['Seats_Available'].between(min_seats, max_seats))
        ]

    # Display filtered data if any results are found
    if not filtered_data.empty:
        st.write("### Filtered Bus Details")
        st.dataframe(filtered_data)
        st.write(f"Total results: {len(filtered_data)}")

        # Adding text input fields for bus ID entry
        selected_bus_id_1 = st.text_input("Enter Bus ID 1 (row index)", value="")
        selected_bus_id_2 = st.text_input("Enter Bus ID 2 (row index)", value="")

        # Display comparison table if both IDs are entered
        if selected_bus_id_1 and selected_bus_id_2:
            try:
                bus_1 = filtered_data.loc[int(selected_bus_id_1)]
                bus_2 = filtered_data.loc[int(selected_bus_id_2)]

                # Create a comparison table
                comparison_data = {
                    'Attribute': ['Route Name', 'Bus Name', 'Start Time', 'End Time', 'Price', 'Ratings', 'Seats Available'],
                    'Bus 1': [bus_1['Route_name'], bus_1['Bus_name'], bus_1['Start_time'], bus_1['End_time'], bus_1['Price'], bus_1['Ratings'], bus_1['Seats_Available']],
                    'Bus 2': [bus_2['Route_name'], bus_2['Bus_name'], bus_2['Start_time'], bus_2['End_time'], bus_2['Price'], bus_2['Ratings'], bus_2['Seats_Available']]
                }

                comparison_df = pd.DataFrame(comparison_data)

                # **COMPARISON TABLE**: Display the comparison table with a heading and increased size using st.table
                st.write("### COMPARISON TABLE")
                st.table(comparison_df)  # Display static table with full content
            except KeyError:
                st.write("Invalid Bus ID entered. Please enter valid IDs from the filtered data.")
    else:
        st.write("### No results found for the selected filters.")

# Close the cursor and connection
mycursor.close()
mydb.close()
