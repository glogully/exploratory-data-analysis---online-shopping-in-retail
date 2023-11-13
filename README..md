# Data Analysis in Online Retail Shopping

## RetailDBConnector

### Table of Contents
- [Project Overview](#description)
- [Setup Guide](#installation)

### Project Overview
The `RetailDBConnector` project is an intuitive Python script that enables the extraction of data from a PostgreSQL database, especially tailored for RDS instances. The aim of the project is to illustrate the application of SQLAlchemy and Pandas to establish a connection with PostgreSQL databases, retrieve data, and export it as a CSV file. This initiativeect is an educational exercise in database connectivity, data extraction, and Python programming.

### Setup Guide
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required Python packages if you haven't. You can install them using pip:
pip install pandas sqlalchemy pyyaml

4. Create a `credentials.yaml` file in the project directory and populate it with your PostgreSQL RDS instance credentials. The YAML file should have the following structure:

- `RDS_HOST: 'your_host'`
  
- `RDS_PORT: 'your_port'`
  
- `RDS_DATABASE: 'your_database'`
  
- `RDS_USER: 'your_username'`
  
- `RDS_PASSWORD: 'your_password'`

Open a terminal and navigate to the project directory.

Run the script using Python:

- `python db_utils.py`

A CSV file named customer_activity.csv containing data from the customer_activity table in your PostgreSQL database will be generated in the project directory.




