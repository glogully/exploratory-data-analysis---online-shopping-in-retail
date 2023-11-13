import psycopg2
from typing import List, Optional
from sqlalchemy import create_engine
import pandas as pd
import yaml
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import numpy as np 

class DataFrameModifier:
    def __init__(self, data_frame: pd.DataFrame):
        self.data_frame = data_frame

    def change_to_category(self, cols: List[str]):
        for column in cols:
            self.data_frame[column] = self.data_frame[column].astype('category')

    def execute_modifications(self):
        cat_cols = ['month', 'operating_systems', 'browser', 'region', 'traffic_type', 'visitor_type']
        self.change_to_category(cat_cols)


class DatasetAnalytics:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset

    def get_column_types(self) -> pd.Series:
        return self.dataset.dtypes

    def compute_basic_stats(self) -> pd.DataFrame:
        return self.dataset.describe(include='all').loc[['mean', 'std', '50%']]

    def unique_value_counts(self) -> pd.Series:
        return self.dataset.select_dtypes(include=['category']).nunique()

    def display_dimensions(self):
        return self.dataset.shape

    def calculate_missing_values(self) -> pd.DataFrame:
        missing_count = self.dataset.isnull().sum()
        missing_percentage = (self.dataset.isnull().sum() / len(self.dataset)) * 100
        return pd.DataFrame({'Total Missing': missing_count, 'Percentage (%)': missing_percentage})


class DataVisualizer:
    def show_null_value_comparison(self, pre_cleaning: pd.Series, post_cleaning: pd.Series):
        comparison_data = pd.DataFrame({'Before Cleaning': pre_cleaning, 'After Cleaning': post_cleaning})
        comparison_data.plot(kind='bar', figsize=(10, 5))
        plt.title('Comparison of Null Values Before and After Cleaning')
        plt.xlabel('Columns')
        plt.ylabel('Count of Null Values')
        plt.show()
    
    def plot_column_distributions(self, data: pd.DataFrame, selected_columns: List[str]):
        for column in selected_columns:
            sns.kdeplot(data[column], fill=True)
            plt.title(f'Distribution for Column: {column}')
            plt.show()


class EnhancedDataFrameTransform(DatasetAnalytics):
    def remove_columns(self, columns_to_drop: List[str]):
        self.dataset.drop(columns=columns_to_drop, inplace=True)

    def fill_missing_values(self):
        for column in self.dataset.columns:
            if self.dataset[column].isnull().sum() > 0:
                if self.dataset[column].dtype == 'object' or self.dataset[column].dtype.name == 'category':
                    self.dataset[column].fillna(self.dataset[column].mode()[0], inplace=True)
                else:
                    if self.dataset[column].dtype in ['int64', 'float64']:
                        if self.dataset[column].skew() > 1:
                            self.dataset[column].fillna(self.dataset[column].median(), inplace=True)
                        else:
                            self.dataset[column].fillna(self.dataset[column].mean(), inplace=True)

    def find_skewed_columns(self, skew_threshold: float = 0.5) -> List[str]:
        numeric_columns = self.dataset.select_dtypes(include=['int64', 'float64'])
        highly_skewed_columns = numeric_columns.columns[numeric_columns.skew().abs() > skew_threshold].tolist()
        return highly_skewed_columns

    class AdvancedDataFrameManipulator(DatasetAnalytics):
        def normalize_skewed_data(self, target_columns: List[str]):
            for column in target_columns:
                if self.dataset[column].min() > 0:
                    try:
                        self.dataset[column], _ = stats.boxcox(self.dataset[column])
                    except Exception as e:
                        print(f"Could not transform {column} using Box-Cox. Error: {e}")
                    else:
                        try:
                            self.dataset[column], _ = stats.yeojohnson(self.dataset[column])
                        except Exception as e:
                            print(f"Could not transform {column} using Yeo-Johnson. Error: {e}")

    
    def manage_outliers(self, target_columns: List[str], method="IQR"):
        for column in target_columns:
            if method == "IQR":
                Q1 = self.dataset[column].quantile(0.25)
                Q3 = self.dataset[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                self.dataset = self.dataset[(self.dataset[column] >= lower_bound) & (self.dataset[column] <= upper_bound)]
    
    def calculate_correlation(self):
        return self.dataset.corr(numeric_only=True)

    def display_correlation_heatmap(self, correlation_matrix):
        plt.figure(figsize=(15, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title("Correlation Heatmap")
        plt.show()

    def find_high_correlation_columns(self, correlation_threshold=0.9):
        correlation_matrix = self.dataset.corr(numeric_only=True).abs()
        upper_triangle = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool))
        columns_to_remove = [column for column in upper_triangle.columns if any(upper_triangle[column] > correlation_threshold)]
        return columns_to_remove

    def discard_columns(self, columns_to_discard: List[str]):
        self.dataset.drop(columns=columns_to_discard, inplace=True)

class RDSConnectionManager:
    def __init__(self, config: dict):
        self.host = config['RDS_HOST']
        self.port = config['RDS_PORT']
        self.database_name = config['RDS_DATABASE']
        self.username = config['RDS_USER']
        self.pwd = config['RDS_PASSWORD']
        self.db_engine = None

    def initialize_engine(self):
        connection_url = f"postgresql://{self.username}:{self.pwd}@{self.host}:{self.port}/{self.database_name}"
        self.db_engine = create_engine(connection_url)

    def fetch_table_data(self, table: str) -> pd.DataFrame:
        sql_query = f"SELECT * FROM {table};"
        result_dataframe = pd.read_sql(sql_query, self.db_engine)
        return result_dataframe


def export_dataframe_to_csv(df: pd.DataFrame, file_name: str):
    df.to_csv(file_name, index=False)


def retrieve_credentials(file_path='credentials.yaml') -> dict:
    with open(file_path, 'r') as yaml_file:
        creds = yaml.safe_load(yaml_file)
    return creds

if __name__ == "__main__":
    # Load database credentials and establish a connection
    credentials = retrieve_credentials()
    db_manager = RDSConnectionManager(credentials)
    db_manager.initialize_engine()
    customer_activity_df = db_manager.fetch_table_data('customer_activity')

    # Apply initial transformations
    data_modifier = DataFrameModifier(customer_activity_df)
    data_modifier.execute_modifications()

    # Perform exploratory data analysis and transformations
    data_analyzer = EnhancedDataFrameTransform(customer_activity_df)

    # Assess null values before and after imputation
    null_counts_before = data_analyzer.calculate_missing_values()['Total Missing']
    print("Null Values Before:", null_counts_before)

    data_analyzer.fill_missing_values()

    null_counts_after = data_analyzer.calculate_missing_values()['Total Missing']
    print("Null Values After:", null_counts_after)

    # Visualize the null value removal
    visualizer = DataVisualizer()
    visualizer.show_null_value_comparison(null_counts_before, null_counts_after)

    # Identify and handle skewed columns
    skewed_columns = data_analyzer.find_skewed_columns()
    numeric_columns = customer_activity_df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    visualizer.plot_column_distributions(customer_activity_df, numeric_columns)

    data_analyzer.manage_outliers(numeric_columns)

    visualizer.plot_column_distributions(customer_activity_df, numeric_columns)

    # Visualize data distribution before and after skew transformation
    for column in skewed_columns:
        sns.kdeplot(customer_activity_df[column], label='Before Skew Transformation', fill=True)

    for column in skewed_columns:
        sns.kdeplot(customer_activity_df[column], label='After Skew Transformation', fill=True)
        plt.legend()
        plt.show()
    
    # Correlation analysis
    correlation_matrix = data_analyzer.calculate_correlation()
    data_analyzer.display_correlation_heatmap(correlation_matrix)

    # Identify and remove highly correlated columns
    columns_to_discard = data_analyzer.find_high_correlation_columns()
    data_analyzer.discard_columns(columns_to_discard)

    # Export the transformed data to a CSV file
    export_dataframe_to_csv(customer_activity_df, 'customer_activity_transformed_corrected_skew.csv')

 