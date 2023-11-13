import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('customer_activity_transformed_corrected_skew.csv')

# Group by 'region' and 'traffic_type', then sum the 'revenue' column to get total revenue for each combination
revenue_by_region_traffic = data.groupby(['region', 'traffic_type'])['revenue'].sum().reset_index()

# Plot
plt.figure(figsize=(16, 8))
sns.barplot(x='region', y='revenue', hue='traffic_type', data=revenue_by_region_traffic, errorbar=None)
plt.title('Revenue by Region and Traffic Type')
plt.xticks(rotation=45)
plt.ylabel('Total Revenue')
plt.legend(title='Traffic Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Group by 'region' and 'traffic_type' and then calculate the average bounce rate for each combination
bounce_rate_by_region_traffic = data.groupby(['region', 'traffic_type'])['bounce_rates'].mean().reset_index()

# Plot
plt.figure(figsize=(16, 8))
sns.barplot(x='region', y='bounce_rates', hue='traffic_type', data=bounce_rate_by_region_traffic, errorbar=None)
plt.title('Average Bounce Rate by Region and Traffic Type')
plt.xticks(rotation=45)
plt.ylabel('Average Bounce Rate')
plt.legend(title='Traffic Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Filter data for rows where the 'traffic_type' indicates ad traffic (contains the word "ads")
ads_data = data[data['traffic_type'].str.contains("ads")]

# Group by 'month' and sum the 'revenue' column to see the sales for each month
sales_by_month = ads_data.groupby('month')['revenue'].sum().reset_index()

# Sort data by month for better visualization
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
sales_by_month['month'] = pd.Categorical(sales_by_month['month'], categories=month_order, ordered=True)
sales_by_month = sales_by_month.sort_values('month')

# Plot
plt.figure(figsize=(12, 6))
sns.barplot(x='month', y='revenue', data=sales_by_month, errorbar=None, color='skyblue')
plt.title('Sales from Ad Traffic by Month')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.show()


