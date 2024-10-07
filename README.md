# Project: Redbus Data Scraping and Visualization
This project automates the extraction of bus route data from Redbus using Selenium, storing the information in an SQL database. A Streamlit-based app enables users to filter and visualize the data, offering valuable insights for travel planning and market analysis.

# Project Scope
**Data Extraction**

Scrape bus route information including bus name, type, departure time, duration, arrival time, rating, price, and seat availability.
Automate navigation through multiple pages and states on the Redbus website.
**Automation**

Utilize Selenium for automated web scraping, handling multi-page navigation and state-wise data retrieval.
**Data Storage**

Store all extracted data in a structured SQL database to ensure scalability and easy retrieval.
**Visualization**

Implement a Streamlit application to allow users to explore and visualize bus route data, filter by attributes like price, star rating, and bus name, and provide analytical insights.
# Solution Overview
The project consists of three key components:

**Web Scraping**

A Selenium-based scraper navigates the Redbus website, extracting relevant bus route and schedule information, ensuring error handling and data consistency.
**SQL Database Integration**

The scraped data is stored in an SQL database. Data integrity is ensured by handling duplicates and database schema design tailored for efficient query performance.
**Streamlit App Development**

A user-friendly Streamlit app connects to the SQL database, allowing users to filter data by bus name, price, and rating, and visualize relevant insights through interactive charts and tables.
# Web Scraping Process
**Initialize Web Driver**
Open the browser using Selenium and navigate to the Redbus website, maximizing the window for efficient interaction.

**Load Target Web Page**
Navigate to the specific state or route page, managing page loading delays dynamically.

**Scrape Bus Routes**
Extract all bus route links and names, managing pagination to capture data from all available routes.

**Scrape Bus Details**
For each bus route, extract detailed information such as bus name, type, departure time, duration, arrival time, star rating, price, and seat availability.

**Error Handling**
Implement robust error handling for missing elements, page loading failures, and logging errors for debugging.

# SQL Database Integration
**Database Setup**
Create a structured SQL database with appropriate tables to store bus route and schedule information.

**Data Insertion**
Insert the scraped data into the SQL database, ensuring data integrity and handling duplicates or errors.

# Streamlit App Development
**Database Connection**
Establish a secure connection between the Streamlit app and the SQL database.

**Data Querying**
Efficiently query the database to fetch bus route information for visualization and analysis.

**Data Filtering**
Allow users to filter bus routes based on price, rating, and bus name using Streamlit’s interactive components.

# Conclusion
The "Redbus Data Scraping and Filtering with Streamlit Application" project offers a robust and scalable solution for automating the extraction, storage, and analysis of bus route data. By leveraging web scraping and visualization technologies, this project enables streamlined travel planning, market analysis, and data-driven decision-making within the transportation industry. The Streamlit app further enhances user experience, providing interactive and customizable data exploration tools.
