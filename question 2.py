import os
import pandas as pd

def calculate_average_seasonal_temperature(directory_path):
    # Initialize an empty DataFrame to hold all data
    all_data = pd.DataFrame()

    # Loop through all files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".csv"):  # Process only CSV files
            file_path = os.path.join(directory_path, file_name)
            data = pd.read_csv(file_path)
            
            # Extract monthly temperature columns and append to all_data
            monthly_data = data.loc[:, 'January':'December']
            all_data = pd.concat([all_data, monthly_data], ignore_index=True)
    
    # Define seasons
    seasons = {
        'Summer': ['December', 'January', 'February'],
        'Autumn': ['March', 'April', 'May'],
        'Winter': ['June', 'July', 'August'],
        'Spring': ['September', 'October', 'November']
    }

    # Calculate average temperatures for each season
    seasonal_averages = {}
    for season, months in seasons.items():
        seasonal_averages[season] = all_data[months].mean(axis=1).mean()

    # Save seasonal averages to file
    seasonal_avg_path = os.path.join(directory_path, "average_temp.txt")
    with open(seasonal_avg_path, "w") as file:
        for season, avg_temp in seasonal_averages.items():
            file.write(f"{season}: {avg_temp:.2f} °C\n")
    
    print(f"Seasonal averages saved to: {seasonal_avg_path}")

def find_largest_temperature_range(directory_path):
    station_ranges = {}

    # Loop through all files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".csv"):  # Process only CSV files
            file_path = os.path.join(directory_path, file_name)
            data = pd.read_csv(file_path)
            
            # Calculate temperature range for each station
            for _, row in data.iterrows():
                station_name = row['STATION_NAME']
                temperatures = row.loc['January':'December']
                temperature_range = temperatures.max() - temperatures.min()
                station_ranges[station_name] = temperature_range
    
    # Find station(s) with the largest temperature range
    max_range = max(station_ranges.values())
    largest_range_stations = [station for station, temp_range in station_ranges.items() if temp_range == max_range]

    # Save results to file
    largest_range_path = os.path.join(directory_path, "largest_temp_range_station.txt")
    with open(largest_range_path, "w") as file:
        file.write(f"Largest Temperature Range: {max_range:.2f} °C\n")
        file.write("Station(s):\n")
        for station in largest_range_stations:
            file.write(f"{station}\n")
    
    print(f"Largest temperature range data saved to: {largest_range_path}")

def find_warmest_and_coolest_stations(directory_path):
    station_avg_temps = {}

    # Loop through all files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".csv"):  # Process only CSV files
            file_path = os.path.join(directory_path, file_name)
            data = pd.read_csv(file_path)
            
            # Calculate average temperature for each station
            for _, row in data.iterrows():
                station_name = row['STATION_NAME']
                temperatures = row.loc['January':'December']
                average_temp = temperatures.mean()
                station_avg_temps[station_name] = average_temp
    
    # Find warmest and coolest stations
    max_temp = max(station_avg_temps.values())
    min_temp = min(station_avg_temps.values())
    warmest_stations = [station for station, avg_temp in station_avg_temps.items() if avg_temp == max_temp]
    coolest_stations = [station for station, avg_temp in station_avg_temps.items() if avg_temp == min_temp]

    # Save results to file
    warmest_and_coolest_path = os.path.join(directory_path, "warmest_and_coolest_station.txt")
    with open(warmest_and_coolest_path, "w") as file:
        file.write(f"Warmest Temperature: {max_temp:.2f} °C\n")
        file.write("Warmest Station(s):\n")
        for station in warmest_stations:
            file.write(f"{station}\n")
        file.write(f"\nCoolest Temperature: {min_temp:.2f} °C\n")
        file.write("Coolest Station(s):\n")
        for station in coolest_stations:
            file.write(f"{station}\n")
    
    print(f"Warmest and coolest station data saved to: {warmest_and_coolest_path}")

# Specify the directory containing the temperature data files
temperature_data_directory = "temperature_data"

# Run the program
calculate_average_seasonal_temperature(temperature_data_directory)
find_largest_temperature_range(temperature_data_directory)
find_warmest_and_coolest_stations(temperature_data_directory)
