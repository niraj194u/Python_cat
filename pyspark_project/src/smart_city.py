from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, row_number, to_timestamp, last
from pyspark.sql.window import Window

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("SmartCityDataProcessing") \
    .getOrCreate()

# File path to the CSV
file_path = "C://Users//NIRAJ//Downloads//smart_city_citizen_activity.csv"

# Read the CSV file into a DataFrame
data = spark.read.option("header", True).csv(file_path)

# Display the first 5 rows
data.show(5)

# Convert 'Sleep_Hours' column to datetime format if it exists
if 'Sleep_Hours' in data.columns:
    data = data.withColumn("Sleep_Hours", to_timestamp(col("Sleep_Hours")))

# Fill missing values using forward-fill method
# PySpark doesn't have a direct forward-fill method; using window functions instead
window_spec = Window.orderBy("Sleep_Hours").rowsBetween(Window.unboundedPreceding, 0)
data = data.select(
    [last(col(c), ignorenulls=True).over(window_spec).alias(c) if c != 'Sleep_Hours' else col(c) for c in data.columns]
)

# Add a binary column indicating if the activity is 'walking'
if 'Activity' in data.columns:
    data = data.withColumn("IsWalking", when(col("Activity") == "walking", 1).otherwise(0))

# Create a cumulative count of records to track overall activity over time
window_spec = Window.orderBy("Sleep_Hours")
data = data.withColumn("CumulativeCount", row_number().over(window_spec))

# PostgreSQL connection details
jdbc_url = "jdbc:postgresql://18.170.23.150:5432/testdb"
connection_properties = {
    "user": "consultants",
    "password": "WelcomeItc@2022",
    "driver": "org.postgresql.Driver"
}

# Write the DataFrame to PostgreSQL table 'smart_city_pyspark'
data.write.jdbc(url=jdbc_url, table="smart_city_pyspark", mode="overwrite", properties=connection_properties)

# Stop the SparkSession
spark.stop()
