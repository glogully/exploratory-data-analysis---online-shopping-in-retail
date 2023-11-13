import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('customer_activity_transformed_corrected_skew.csv')

# Group data by region and sum the revenue (True=1, False=0)
region_revenue = data.groupby('region')['revenue'].sum().sort_values(ascending=False)

# Plot the results
plt.figure(figsize=(12, 7))
sns.barplot(x=region_revenue.index, y=region_revenue.values, palette="viridis")
plt.title('Revenue by Region')
plt.ylabel('Total Revenue')
plt.xlabel('Region')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Group data by visitor type and calculate the percentage of visitors generating revenue
visitor_revenue = data.groupby('visitor_type')['revenue'].mean() * 100

# Plot the results
plt.figure(figsize=(8, 6))
sns.barplot(x=visitor_revenue.index, y=visitor_revenue.values, palette="coolwarm")
plt.title('Percentage of Customers Making a Purchase by Visitor Type')
plt.ylabel('Percentage (%)')
plt.xlabel('Visitor Type')
plt.tight_layout()
plt.show()

# Group data by weekend status and calculate the percentage of visits generating revenue
weekend_revenue = data.groupby('weekend')['revenue'].mean() * 100

# Plot the results
plt.figure(figsize=(8, 6))
sns.barplot(x=weekend_revenue.index, y=weekend_revenue.values, palette="magma")
plt.title('Percentage of Sales on Weekends vs. Weekdays')
plt.ylabel('Percentage (%)')
plt.xlabel('Weekend')
plt.xticks([0, 1], ['Weekdays', 'Weekends'])
plt.tight_layout()
plt.show()

# Group data by month and calculate the percentage of visits generating revenue
month_revenue = data.groupby('month')['revenue'].mean().sort_values(ascending=False) * 100

# Plot the results
plt.figure(figsize=(12, 7))
sns.barplot(x=month_revenue.index, y=month_revenue.values, palette="rainbow")
plt.title('Percentage of Sales by Month')
plt.ylabel('Percentage (%)')
plt.xlabel('Month')
plt.tight_layout()
plt.show()

# Group data by traffic type and calculate the percentage of visits generating revenue
traffic_revenue = data.groupby('traffic_type')['revenue'].mean().sort_values(ascending=False) * 100

# Plot the results
plt.figure(figsize=(12, 7))
sns.barplot(x=traffic_revenue.index, y=traffic_revenue.values, palette="flare")
plt.title('Percentage of Sales by Traffic Type')
plt.ylabel('Percentage (%)')
plt.xlabel('Traffic Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()