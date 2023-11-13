import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('customer_activity_transformed_corrected_skew.csv')


# Are sales proportionally happening more on weekends?
sales_by_day_type = df.groupby('weekend')['revenue'].sum()
weekend_sales_proportion = sales_by_day_type[True] / sales_by_day_type.sum()
print(f"Percentage of sales on weekends: {weekend_sales_proportion * 100:.2f}%")

# Which regions are generating the most revenue currently?
sales_by_region = df.groupby('region')['revenue'].sum().sort_values(ascending=False)
print("\nSales by Region:\n", sales_by_region)

# Is there any particular website traffic that stands out when generating sales?
sales_by_traffic = df.groupby('traffic_type')['revenue'].sum().sort_values(ascending=False)
print("\nSales by Traffic Type:\n", sales_by_traffic)

# What percentage of time is spent on the website performing administrative/product or informational related tasks?
total_admin_duration = df['administrative_duration'].sum()
total_product_duration = df['product_related_duration'].sum()
total_info_duration = df['informational_duration'].sum()
total_duration = total_admin_duration + total_product_duration + total_info_duration
admin_percentage = total_admin_duration / total_duration
product_percentage = total_product_duration / total_duration
info_percentage = total_info_duration / total_duration
print(f"\nPercentage time on Administrative tasks: {admin_percentage * 100:.2f}%")
print(f"Percentage time on Product-related tasks: {product_percentage * 100:.2f}%")
print(f"Percentage time on Informational tasks: {info_percentage * 100:.2f}%")

# Are there any informational/administrative tasks which users spend time doing most?
avg_admin_duration = df['administrative_duration'].mean()
avg_info_duration = df['informational_duration'].mean()
print(f"\nAverage time on Administrative tasks: {avg_admin_duration:.2f}")
print(f"Average time on Informational tasks: {avg_info_duration:.2f}")

# What is the breakdown of months making the most sales from january to december in order?
sales_by_month = df.groupby('month')['revenue'].sum().sort_values(ascending=False)
print("\nSales by Month:\n", sales_by_month)



