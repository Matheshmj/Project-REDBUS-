import pandas as pd
import mysql.connector
import numpy as np
final_df=pd.read_csv("C:/Users/91848/Desktop/REDBUS PROJECT/red_bus_data.csv")
df=final_df

def clean_duration(duration):
    try:
        if pd.isna(duration):
            return "00:00:00"
        duration = duration.strip()
        if "h" in duration and "m" in duration:
            hours, minutes = duration.split("h")
            minutes = minutes.replace('m', '').strip()
            return f"{hours.zfill(2)}:{minutes.zfill(2)}:00"
        return "00:00:00"
    
    except (ValueError, IndexError):
        return "00:00:00"


def clean_price(price):
    try:
        if pd.isna(price):
            return 0.0
            
        # Convert price to string if it's a float
        price_str = str(price)

        # Remove 'INR' and any other unwanted text, and keep only digits and periods
        cleaned_price = ''.join(filter(lambda x: x.isdigit() or x == '.', price_str))

        # Convert to float
        return float(cleaned_price) if cleaned_price else 0.0
    
    except (ValueError, AttributeError):
        return 0.0

def clean_seats(seats):
    try:
        if pd.isna(seats):
            return 0
        
        if isinstance(seats, int):
            return seats
        
        return int(seats.split()[0])
    
    except (ValueError, IndexError):
        return 0
 
def clean_ratings(rating):
    try:
        if pd.isna(rating) or rating == 'No Rating':
            return 0.0
        
        if isinstance(rating, float):
            return rating
        cleaned_rating = rating.split('\n')[0]
        return float(cleaned_rating)
    
    except (ValueError, IndexError):
        return 0.0


df['Total_duration']=df['Total_duration'].apply(clean_duration)
df['Price']=df['Price'].apply(clean_price)
df['Seats_Available']=df['Seats_Available'].apply(clean_seats)
df['Ratings']=df['Ratings'].apply(clean_ratings)


df_cleaned = df.dropna(subset=['Bus_name', 'Bus_type'], how='all')
print(df_cleaned)


df_cleaned = df_cleaned.reset_index(drop=True)
print(df_cleaned)

df=df_cleaned

#database connection
try:
    conn=mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='848981',
        database='route'
    )
    cursor= conn.cursor()
    print("database connection successfull")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)
        

# List of routes for each state
kerala_routes = [
    "Bangalore to Kozhikode", "Kozhikode to Bangalore", "Kozhikode to Ernakulam",
    "Ernakulam to Kozhikode", "Bangalore to Kannur", "Kozhikode to Mysore",
    "Kannur to Bangalore", "Kozhikode to Thiruvananthapuram", "Mysore to Kozhikode",
    "Bangalore to Kalpetta (kerala)", "Kalpetta (kerala) to Bangalore", 
    "Thiruvananthapuram to Kozhikode", "Kozhikode to Thrissur", "Kozhikode to Kottayam",
    "Kottayam to Kozhikode"
]

andhra_pradesh_routes = [
    "Hyderabad to Vijayawada", "Vijayawada to Hyderabad", "Hyderabad to Ongole", 
    "Kakinada to Visakhapatnam", "Bangalore to Tirupati", "Bangalore to Kadapa", 
    "Ongole to Hyderabad", "Kadapa to Bangalore", "Chittoor (Andhra Pradesh) to Bangalore", 
    "Visakhapatnam to Kakinada", "Bangalore to Anantapur (andhra pradesh)", 
    "Bangalore to Chittoor (Andhra Pradesh)", "Anantapur (andhra pradesh) to Bangalore", 
    "Hyderabad to Kurnool", "Tirupati to Bangalore", "Narasaraopet to Hyderabad", 
    "Vinukonda to Hyderabad", "Hyderabad to Vinukonda", "Visakhapatnam to Vijayawada", 
    "Bangalore to Rayachoti", "Hyderabad to Guntur (Andhra Pradesh)", 
    "Guntur (Andhra Pradesh) to Hyderabad", "Hyderabad to Eluru", 
    "Eluru to Hyderabad", "Bangalore to Kadiri", "Madanapalli to Bangalore", 
    "Bangalore to Madanapalli", "Macherla (andhra pradesh) to Hyderabad", 
    "Rajahmundry to Visakhapatnam", "Nandyal to Hyderabad", "Rayachoti to Bangalore", 
    "Kurnool to Hyderabad", "Kadiri to Bangalore", "Visakhapatnam to Rajahmundry", 
    "Hyderabad to Addanki", "Hyderabad to Anantapur (andhra pradesh)", 
    "Hyderabad to Markapuram", "Rajahmundry to Vijayawada", "Tirupati to Chennai", 
    "Vijayawada to Visakhapatnam", "Hyderabad to Macherla (andhra pradesh)", 
    "Hyderabad to Rajahmundry", "Chilakaluripet to Hyderabad", "Rajahmundry to Hyderabad", 
    "Kurnool to Bangalore", "Hyderabad to Nandyal"
]

telangana_routes = [
    "Hyderabad to Vijayawada", "Khammam to Hyderabad", "Hyderabad to Khammam", 
    "Hyderabad to Srisailam", "Karimnagar to Hyderabad", "Hyderabad to Karimnagar", 
    "Hyderabad to Mancherial", "Hyderabad to Nirmal", "Hyderabad to Adilabad", 
    "Hyderabad to Ongole", "Kothagudem to Hyderabad", "Guntur (Andhra Pradesh) to Hyderabad", 
    "Hyderabad to Guntur (Andhra Pradesh)", "Godavarikhani to Hyderabad", 
    "Hyderabad to Kothagudem", "Hyderabad to Sathupally", "Hyderabad to Warangal", 
    "Kodad to Hyderabad", "Jagityal to Hyderabad", "Hyderabad to Bhadrachalam", 
    "Hyderabad to Tirupati", "Hyderabad to Godavarikhani", "Hyderabad to Armoor", 
    "Hyderabad to Nandyal", "Hyderabad to Kodad", "Hyderabad to Addanki"
]

rajasthan_routes = [
    "Udaipur to Jodhpur", "Jodhpur to Ajmer", "Beawar (Rajasthan) to Jaipur (Rajasthan)", 
    "Sikar to Jaipur (Rajasthan)", "Jaipur (Rajasthan) to Jodhpur", 
    "Aligarh (uttar pradesh) to Jaipur (Rajasthan)", "Jaipur (Rajasthan) to Aligarh (uttar pradesh)", 
    "Jodhpur to Beawar (Rajasthan)", "Jaipur (Rajasthan) to Pilani", 
    "Kishangarh to Jaipur (Rajasthan)", "Pali (Rajasthan) to Udaipur", 
    "Udaipur to Pali (Rajasthan)", "Kota(Rajasthan) to Udaipur", 
    "Jaipur (Rajasthan) to Bhilwara", "Sikar to Bikaner", "Jaipur (Rajasthan) to Bharatpur", 
    "Jaipur (Rajasthan) to Mathura", "Jaipur (Rajasthan) to Kota(Rajasthan)"
]

south_bengal_routes = [
    "Durgapur to Calcutta", "Kolkata to Burdwan", "Haldia to Calcutta", 
    "Kolkata to Haldia", "Kolkata to Durgapur (West Bengal)", 
    "Kolkata to Arambagh (West Bengal)", "Midnapore to Kolkata", 
    "Kolkata to Digha", "Digha to Calcutta", "Kolkata to Bankura", 
    "Kolkata to Midnapore", "Kolkata to Asansol (West Bengal)", 
    "Kolkata to Nimtouri", "Jhargram to Kolkata", "Kolkata to Contai (Kanthi)", 
    "Kolkata to Kolaghat", "Kolkata to Nandakumar (west bengal)", 
    "Kolkata to Mecheda (West Bengal)", "Digha to Durgapur (West Bengal)", 
    "Midnapore to Barasat (West Bengal)", "Durgapur (West Bengal) to Digha", 
    "Kolkata to Chandipur (West Bengal)", "Barasat (West Bengal) to Midnapore", 
    "Kolkata to Debra", "Kirnahar (West Bengal) to Kolkata", 
    "Kolkata to Panskura", "Kolkata to Heria", "Digha to Barasat (West Bengal)", 
    "Illambazar to Kolkata", "Kolkata to Suri", 
    "Berhampore (West Bengal) to Durgapur (West Bengal)", 
    "Purulia to Durgapur (West Bengal)", "Durgapur (West Bengal) to Berhampore (West Bengal)", 
    "Kolkata to Futishanko", "Kolkata to Kirnahar (West Bengal)", 
    "Durgapur (West Bengal) to Barasat (West Bengal)", 
    "Kolkata to Ramnagar (West Bengal)", "Durgapur (West Bengal) to Purulia", 
    "Durgapur (West Bengal) to Bankura", "Kolkata to Ashari", 
    "Barasat (West Bengal) to Digha"
]
himachal_pradesh_routes = [
    "Delhi to Shimla",
    "Chandigarh to Hamirpur (Himachal Pradesh)",
    "Hamirpur (Himachal Pradesh) to Chandigarh",
    "Shimla to Delhi",
    "Delhi to Chandigarh",
    "Hamirpur (Himachal Pradesh) to Delhi",
    "Chamba (Himachal Pradesh) to Chandigarh",
    "Delhi to Hamirpur (Himachal Pradesh)",
    "Chandigarh to Dharamshala (Himachal Pradesh)",
    "Delhi to Chamba (Himachal Pradesh)",
    "Chamba (Himachal Pradesh) to Delhi",
    "Kangra to Chandigarh",
    "Shimla to Chandigarh",
    "Delhi to Baddi (Himachal Pradesh)",
    "Delhi to Solan",
    "Delhi to Nalagarh",
    "Dharamshala (Himachal Pradesh) to Chandigarh",
    "Palampur to Chandigarh",
    "Ghumarwin to Delhi",
    "Chandigarh to Kangra",
    "Baddi (Himachal Pradesh) to Delhi",
    "Manali to Chandigarh",
    "Solan to Delhi",
    "Chandigarh to Manali",
    "Delhi to Sarkaghat",
    "Ghumarwin to Chandigarh",
    "Chandigarh to Kullu",
    "Delhi to Bilaspur (Himachal Pradesh)",
    "Delhi to Ghumarwin",
    "Chamba (Himachal Pradesh) to Shimla",
    "Delhi to Palampur",
    "Chandigarh to Reckong Peo (Himachal Pradesh)",
    "Bilaspur (Himachal Pradesh) to Delhi",
    "Sarkaghat to Delhi",
    "Manali to Delhi"
]
assam_routes = [
    "Tezpur to Guwahati",
    "Guwahati to Tezpur",
    "Guwahati to Nagaon (Assam)",
    "Nagaon (Assam) to Guwahati",
    "Goalpara to Guwahati",
    "Jorhat to North Lakhimpur",
    "Dhubri to Guwahati",
    "Jorhat to Dibrugarh",
    "North Lakhimpur to Jorhat",
    "North Lakhimpur to Sibsagar",
    "Guwahati to Dhubri",
    "Dhekiajuli to Guwahati",
    "Sibsagar to North Lakhimpur",
    "Dibrugarh to Jorhat",
    "Jorhat to Dhemaji",
    "Jorhat to Tinsukia",
    "Tezpur to Dibrugarh",
    "Dhemaji to Jorhat",
    "North Lakhimpur to Tezpur",
    "Guwahati to Biswanath Charali",
    "North Lakhimpur to Dibrugarh",
    "Tinsukia to Jorhat",
    "Tezpur to North Lakhimpur",
    "North Lakhimpur to Moran",
    "Guwahati to Gohpur",
    "Guwahati to Kaliabor",
    "Guwahati to Tumuki (Tezpur Medical)",
    "Dibrugarh to Tezpur",
    "Biswanath Charali to Guwahati",
    "Dibrugarh to North Lakhimpur",
    "Moran to North Lakhimpur",
    "Tumuki (Tezpur Medical) to Guwahati",
    "Biswanath Charali to Dibrugarh",
    "Gohpur to Guwahati",
    "Sibsagar to Dhemaji",
    "North Lakhimpur to Guwahati",
    "Haflong to Guwahati",
    "Tezpur to Moran",
    "Moran to Tezpur",
    "Bokakhat to Dibrugarh",
    "North Lakhimpur to Nagaon (Assam)",
    "Bihpuria to Dibrugarh",
    "Haflong to Nagaon (Assam)",
    "Guwahati to Golaghat",
    "Jorhat to Gogamukh",
    "Dibrugarh to Biswanath Charali",
    "Golaghat to North Lakhimpur"
]
west_bengal_routes = [
    "Digha to Barasat (West Bengal)",
    "Durgapur to Calcutta",
    "Digha to Calcutta",
    "Kolkata to Digha",
    "Barasat (West Bengal) to Digha",
    "Kolkata to Suri",
    "Barasat (West Bengal) to Midnapore",
    "Midnapore to Kolkata",
    "Barasat (West Bengal) to Kolaghat",
    "Barasat (West Bengal) to Contai (Kanthi)",
    "Habra to Digha",
    "Barasat (West Bengal) to Nandakumar (West Bengal)",
    "Kolkata to Durgapur (West Bengal)",
    "Digha to Habra",
    "Midnapore to Barasat (West Bengal)",
    "Kolkata to Bolpur (West Bengal)",
    "Barasat (West Bengal) to Durgapur (West Bengal)",
    "Barasat (West Bengal) to Heria",
    "Haldia to Barasat (West Bengal)",
    "Barasat (West Bengal) to Haldia",
    "Haldia to Kolkata",
    "Barasat (West Bengal) to Debra",
    "Barasat (West Bengal) to Burdwan",
    "Kolkata to Bakkhali",
    "Kolkata to Purulia",
    "Durgapur (West Bengal) to Purulia",
    "Habra to Midnapore",
    "Kolkata to Asansol (West Bengal)",
    "Durgapur (West Bengal) to Barasat (West Bengal)",
    "Barasat (West Bengal) to Asansol (West Bengal)",
    "Jayrambati (West Bengal) to Barasat (West Bengal)",
    "Kolkata to Haldia",
    "Habra to Durgapur (West Bengal)",
    "Habra to Nandakumar (West Bengal)",
    "Habra to Kolaghat",
    "Kolkata to Mayapur ISKCON",
    "Habra to Heria",
    "Midnapore to Kolkata Airport"
]
uttar_pradesh_routes = [
    "Delhi to Bareilly",
    "Bareilly to Delhi",
    "Aligarh (Uttar Pradesh) to Delhi",
    "Delhi to Aligarh (Uttar Pradesh)",
    "Lucknow to Allahabad",
    "Lucknow to Delhi",
    "Delhi to Farrukhabad (Uttar Pradesh)",
    "Farrukhabad (Uttar Pradesh) to Delhi",
    "Badaun to Delhi",
    "Allahabad to Lucknow",
    "Lucknow to Agra",
    "Sitapur (Uttar Pradesh) to Delhi",
    "Delhi to Badaun",
    "Delhi to Sitapur (Uttar Pradesh)",
    "Agra to Delhi",
    "Delhi to Moradabad",
    "Delhi to Lucknow",
    "Agra to Lucknow",
    "Lucknow to Varanasi",
    "Agra to Bareilly",
    "Lucknow to Bareilly",
    "Bareilly to Agra",
    "Delhi to Agra",
    "Varanasi to Lucknow",
    "Moradabad to Delhi",
    "Kanpur (Uttar Pradesh) to Jhansi",
    "Delhi to Shahjahanpur (Uttar Pradesh)",
    "Shahjahanpur (Uttar Pradesh) to Delhi",
    "Gorakhpur (Uttar Pradesh) to Lucknow",
    "Kanpur (Uttar Pradesh) to Bareilly",
    "Lucknow to Aligarh (Uttar Pradesh)",
    "Lucknow to Kanpur (Uttar Pradesh)",
    "Delhi to Pilibhit",
    "Lucknow to Ballia",
    "Delhi to Etah (Uttar Pradesh)",
    "Lucknow to Gorakhpur (Uttar Pradesh)",
    "Aligarh (Uttar Pradesh) to Lucknow",
    "Aligarh (Uttar Pradesh) to Agra",
    "Bareilly to Dehradun",
    "Pilibhit to Delhi"
]
punjab_routes = [
    "Delhi to Patiala",
    "Patiala to Delhi",
    "Delhi to Ludhiana",
    "Ludhiana to Delhi",
    "Jalandhar to Delhi",
    "Delhi to Jalandhar",
    "Delhi Airport to Patiala",
    "Ludhiana to Delhi Airport",
    "Delhi Airport to Ludhiana",
    "Jalandhar to Delhi Airport",
    "Phagwara to Delhi Airport",
    "Delhi to Phagwara",
    "Delhi Airport to Jalandhar",
    "Phagwara to Delhi",
    "Delhi to Amritsar",
    "Amritsar to Delhi",
    "Amritsar to Delhi Airport",
    "Delhi Airport to Phagwara"
]
chandigarh_routes = [
    "Yamuna Nagar to Chandigarh",
    "Chandigarh to Delhi",
    "Delhi to Chandigarh",
    "Ludhiana to Chandigarh",
    "Chandigarh to Yamuna Nagar",
    "Chandigarh to Ludhiana",
    "Hamirpur (Himachal Pradesh) to Chandigarh",
    "Chandigarh to Vrindavan",
    "Chandigarh to Hamirpur (Himachal Pradesh)",
    "Chandigarh to Pathankot",
    "Chandigarh to Dehradun",
    "Dehradun to Chandigarh",
    "Pathankot to Chandigarh",
    "Sujanpur (Himachal Pradesh) to Chandigarh",
    "Chandigarh to Sujanpur (Himachal Pradesh)",
    "Talwara to Chandigarh",
    "Vrindavan to Chandigarh",
    "Chandigarh to Shimla",
    "Chandigarh to Dinanagar (Punjab)",
    "Chandigarh to Baijnath",
    "Dinanagar (Punjab) to Chandigarh",
    "Chandigarh to Dharamshala (Himachal Pradesh)",
    "Chandigarh to Talwara",
    "Chandigarh to Amritsar",
    "Chandigarh to Agra",
    "Rohtak to Chandigarh",
    "Narnaul to Chandigarh",
    "Amritsar to Chandigarh",
    "Chandigarh to Haridwar",
    "Hisar (Haryana) to Chandigarh",
    "Dharamshala (Himachal Pradesh) to Chandigarh",
    "Jawala Ji to Chandigarh",
    "Baijnath to Chandigarh",
    "Chandigarh to Rohtak",
    "Chandigarh to Hisar (Haryana)",
    "Chandigarh to Una (Himachal Pradesh)",
    "Chandigarh to Rishikesh",
    "Rishikesh to Chandigarh",
    "Shimla to Chandigarh",
    "Agra to Chandigarh"
]
north_bengal_routes = [
    "Siliguri to Darjeeling",
    "Siliguri to Kolkata",
    "Kolkata to Siliguri",
    "Raiganj to Kolkata",
    "Kolkata to Raiganj",
    "Kolkata to Malda",
    "Malda to Kolkata",
    "Cooch Behar (West Bengal) to Berhampore (West Bengal)",
    "Kolkata to Cooch Behar (West Bengal)",
    "Kolkata to Balurghat",
    "Berhampore (West Bengal) to Cooch Behar (West Bengal)",
    "Berhampore (West Bengal) to Siliguri",
    "Cooch Behar (West Bengal) to Raiganj",
    "Malda to Cooch Behar (West Bengal)",
    "Balurghat to Kolkata",
    "Siliguri to Berhampore (West Bengal)",
    "Cooch Behar (West Bengal) to Malda",
    "Kolkata to Gangarampur",
    "Falakata (West Bengal) to Berhampore (West Bengal)",
    "Kolkata to Jalpaiguri",
    "Cooch Behar (West Bengal) to Kolkata",
    "Kolkata to Farakka",
    "Kolkata to Islampur (West Bengal)",
    "Berhampore (West Bengal) to Falakata (West Bengal)",
    "Siliguri to Cooch Behar (West Bengal)",
    "Raiganj to Krishnanagar (West Bengal)",
    "Kolkata to Buniadpur",
    "Siliguri to Ranaghat",
    "Kolkata to Itahar (West Bengal)",
    "Kolkata to Gazole",
    "Falakata (West Bengal) to Malda",
    "Siliguri to Krishnanagar (West Bengal)",
    "Gangarampur to Kolkata",
    "Cooch Behar (West Bengal) to Siliguri",
    "Buniadpur to Kolkata",
    "Raiganj to Barasat (West Bengal)",
    "Kolkata to Dhupguri (West Bengal)",
    "Raiganj to Ranaghat",
    "Kolkata to Kishanganj",
    "Kolkata to Falakata (West Bengal)"
]
bihar_routes = [
    "Gopalganj (Bihar) to Delhi",
    "Patna (Bihar) to Bettiah",
    "Patna (Bihar) to Motihari",
    "Motihari to Delhi",
    "Bettiah to Patna (Bihar)",
    "Delhi to Motihari",
    "Balmiki Nagar (Bihar) to Patna (Bihar)",
    "Patna (Bihar) to Balmiki Nagar (Bihar)",
    "Patna (Bihar) to Purnea",
    "Patna (Bihar) to Katihar",
    "Patna (Bihar) to Ranchi",
    "Hazaribagh to Patna (Bihar)",
    "Ranchi to Patna (Bihar)",
    "Patna (Bihar) to Kathmandu",
    "Muzaffarpur (Bihar) to Ranchi",
    "Lucknow to Motihari",
    "Patna (Bihar) to Hazaribagh",
    "Ranchi to Muzaffarpur (Bihar)",
    "Patna (Bihar) to Raxaul",
    "Purnea to Patna (Bihar)",
    "Agra to Motihari",
    "Hazaribagh to Muzaffarpur (Bihar)",
    "Motihari to Agra",
    "Motihari to Lucknow",
    "Muzaffarpur (Bihar) to Hazaribagh",
    "Katihar to Patna (Bihar)",
    "Patna (Bihar) to Araria (Bihar)",
    "Patna (Bihar) to Forbesganj",
    "Darbhanga to Patna (Bihar)",
    "Patna (Bihar) to Saharsa",
    "Patna (Bihar) to Darbhanga",
    "Lucknow to Darbhanga",
    "Patna (Bihar) to Muzaffarpur (Bihar)",
    "Ranchi to Bihar Sharif",
    "Lucknow to Gopalganj (Bihar)",
    "Darbhanga to Lucknow",
    "Gopalganj (Bihar) to Lucknow",
    "Muzaffarpur (Bihar) to Bihar Sharif",
    "Kathmandu to Patna (Bihar)"
]
west_bengal_surface_routes = [
    "Digha to Kolkata",
    "Kolkata to Digha",
    "Kolkata to Mandarmani",
    "Mandarmani to Kolkata"
]

# Combine all routes into a dictionary
routes_dict = {
    'Kerala': kerala_routes,
    'Andhra Pradesh': andhra_pradesh_routes,
    'Telangana': telangana_routes,
    'Rajasthan': rajasthan_routes,
    'South Bengal': south_bengal_routes,
    'Himachal pradesh': himachal_pradesh_routes,
    'Assam' : assam_routes,
    'West bengal': west_bengal_routes,
    'uttar pradesh':uttar_pradesh_routes,
    'punjab':punjab_routes,
    'Chandigarh':chandigarh_routes,
    'North bengal':north_bengal_routes,
    'Bihar':bihar_routes,
    'west bengal surface':west_bengal_surface_routes
    
}

# Function to assign the state based on the route
def assign_state(route):
    for state, routes in routes_dict.items():
        if route in routes:
            return state
    return 'Other'

# Apply the function to the DataFrame
df['State'] = df['Route_name'].apply(assign_state)

# Display the updated DataFrame
df

#insert data into mysql

try:
    for index, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO buses_routes (
                Bus_name, Bus_type, Start_time, End_time, Total_duration, 
                Price, Seats_Available, Ratings, Route_link, Route_name,State
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
            """,
            (row['Bus_name'], row['Bus_type'], row['Start_time'], row['End_time'],
             row['Total_duration'], row['Price'], row['Seats_Available'],
             row['Ratings'], row['Route_link'], row['Route_name'],row['State'])
        )
        conn.commit()
    print(f"Inserted {len(df)} rows successfully.")
except Exception as e:
    print(f"An error occurred: {e}")



finally:
    cursor.close()
    conn.close()
    print("database connection closed")

    

            



