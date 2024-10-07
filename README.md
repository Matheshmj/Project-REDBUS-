# Project-REDBUS-
This project automates the extraction of bus route data from Redbus using Selenium and stores it in a SQL database. A Streamlit app allows users to filter and visualize the data, providing insights for travel planning and market analysis.
# scope
•	Data Extraction: Scrape bus route links, names, and detailed information for each route, including bus name, type, departing time, duration, reaching time, star rating, price, and seat availability.
•	Automation: Automate navigation through multiple pages and states on the RedBus website.
•	Data Storage: Store the scraped data in an SQL database.
•	Visualization: Develop a Streamlit app to visualize and analyze the stored data.
# SOLUTION OVERVIEW
The solution involves three main components: web scraping, SQL database integration, and Streamlit app development.
# WEB SCRAPING

Step by step procedure:
i.	Initialize Web Driver: Open and maximize the browser, and navigate to the RedBus website.
ii.	Load Web Page: Load the specific URL for the target state, handling any loading delays.
iii.	Scrape Bus Routes: Identify and extract all bus route links and names on the page, managing pagination to capture all routes.
iv.	Scrape Bus Details: Navigate to each bus route link and extract detailed information about available buses, such as name, type, departing time, duration, reaching time, star rating, price, and seat availability.
v.	Handle Errors: Implement error handling for missing elements or loading failures, logging errors and continuing the scraping process.
# SQL DATABASE INTEGRATION.

Step by step procedure:
i.	Database Setup: Create a database and define a table structure to store bus route and schedule details.
ii.	Data Insertion: Insert the scraped data into the SQL database, ensuring data integrity and handling duplicates or errors.
# STREAMLIT APP DEVELOPMENT

Steps:
i.	Database Connection: Establish a connection to the SQL database.
ii.	Query Data: Fetch data from the database to be displayed in the app.
iii.	Filtering: Use Streamlit components to filter the bus route name, price and star rating
