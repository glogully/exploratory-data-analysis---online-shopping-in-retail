import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('customer_activity_transformed_corrected_skew.csv')

# Count the occurrences of each operating system
os_counts = data['operating_systems'].value_counts()
os_percent = (os_counts / os_counts.sum()) * 100

# Plot
plt.figure(figsize=(14, 6))
sns.barplot(x=os_counts.index, y=os_counts.values, palette='viridis')
plt.ylabel('Count')
plt.xlabel('Operating System')
plt.title('Count of Operating Systems Used to Visit the Site')

# Display the percentage on top of each bar
for i, value in enumerate(os_counts.values):
    plt.text(i, value + 100, f'{os_percent.iloc[i]:.2f}%', ha='center')

plt.show()

# Categorize operating systems into mobile and desktop
mobile_os = ['Android', 'iOS']
desktop_os = ['Windows', 'Mac OS', 'Linux']

data['os_category'] = data['operating_systems'].apply(lambda x: 'Mobile' if x in mobile_os else ('Desktop' if x in desktop_os else 'Others'))

# Count the occurrences of each category
os_category_counts = data['os_category'].value_counts()
os_category_percent = (os_category_counts / os_category_counts.sum()) * 100

# Plot
plt.figure(figsize=(8, 6))
sns.barplot(x=os_category_counts.index, y=os_category_counts.values, palette='viridis')
plt.ylabel('Count')
plt.xlabel('OS Category')
plt.title('Users Visiting the Site: Mobile vs. Desktop')

# Display the percentage on top of each bar
for i, value in enumerate(os_category_counts.values):
    plt.text(i, value + 100, f'{os_category_percent.iloc[i]:.2f}%', ha='center')

plt.show()

# Group by browser and OS category to get counts
browser_counts = data.groupby(['browser', 'os_category']).size().unstack().fillna(0)

# Sort the browsers by total count
browser_counts['Total'] = browser_counts.sum(axis=1)
browser_counts = browser_counts.sort_values('Total', ascending=False).drop(columns='Total')

# Plot
plt.figure(figsize=(16, 8))
browser_counts.plot(kind='bar', stacked=True, colormap='viridis', figsize=(16, 8))
plt.ylabel('Count')
plt.xlabel('Browser')
plt.title('Browser Usage Breakdown: Mobile vs. Desktop')
plt.legend(title='OS Category')
plt.tight_layout()
plt.show()

# Group by region and operating system to get counts
region_os_counts = data.groupby(['region', 'operating_systems']).size().unstack().fillna(0)

# Plot
plt.figure(figsize=(18, 10))
region_os_counts.plot(kind='bar', stacked=True, colormap='viridis', figsize=(18, 10))
plt.ylabel('Count')
plt.xlabel('Region')
plt.title('Popular Operating Systems by Region')
plt.legend(title='Operating System')
plt.tight_layout()
plt.show()