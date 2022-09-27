# Project 1
# Exploring Data of a Bike Share System for 3 major US cities.

import time
import pandas as pd

City_Data = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
filters = ['month', 'day', 'both', 'neither']


def apply_filters():
    """
    Asks User for specific filters: city, month, day to analyze

    Returns:
        city (string) - city chosen to be analyzed
        month (string) - month name to filter by, or 'all' to disable month filter
        day (string) - day name to filter by, or 'all' to disable day filter

    """
    # Welcome message
    print("Welcome!\nLet's explore the data of a bike share system! ")
    print('*' * 40)

    # Preliminary values for month & day
    month = 'all'
    day = 'all'
    # Asking user to specify the data he wants to explore
    city = input(
        "Please enter the name of the city you wish to explore: Chicago, New York City, or Washington \n").lower()
    while city not in City_Data:
        city = input('Incorrect Input! Please Try Entering City Name Again: \n').lower()

    # Ask user for filter type
    choose_filter = input("Do you want to filter data by month, day, both, or neither?\n").lower()
    while choose_filter not in filters:
        choose_filter = input("Incorrect Input! Try Entering Filter again: \n").lower()

    # Month Filter
    if choose_filter == 'month' or choose_filter == 'both':
        month = input("Please enter a month name from January to June): \n").lower()
        while month not in months:
            month = input('Incorrect Input! Please Try Entering Month Name Again: \n').lower()

    # Day Filter
    if choose_filter == 'day' or choose_filter == 'both':
        day = input("Please enter a day name: \n").lower()
        while day not in days:
            day = input('Incorrect Input! Please Try Entering Day Name Again: \n').lower()

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for specified city and month & day filters if specified

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        dataframe - Pandas DataFrame containing city data filtered by month and day (if specified)

    """

    # Load chosen city file into a dataframe
    dataframe = pd.read_csv(City_Data[city])

    # To access months and days, we need to convert Start_Time to a datetime type
    dataframe['Start Time'] = pd.to_datetime(dataframe['Start Time'])

    # Access months from Start_Time
    dataframe['month'] = dataframe['Start Time'].dt.month

    # Filter by month
    if month != 'all':
        # Convert months name to its corresponding integer value
        month = months.index(month) + 1
        # Update dataframe with filtered month
        dataframe = dataframe[dataframe['month'] == month]

    # Access days from Start_Time
    dataframe['day'] = dataframe['Start Time'].dt.day_name()

    # Filter by day
    if day != 'all':
        # Update dataframe with filtered day
        dataframe = dataframe[dataframe['day'] == day.title()]

    return dataframe


def frequent_time(city):
    """
    Displays statistics on the most frequent times of travel:
        -- Most common month
        -- Most common day
        -- Most common hour
    """
    start_time = time.time()
    # Show most frequent times of travel statistics
    print("Now Displaying Most Common Time periods in the specified city generally...\n")
    # Display Introductory Message
    print("You chose the city of {}\n".format(city.title()))

    # Access whole database of specific city
    dataframe = pd.read_csv(City_Data[city])
    dataframe['Start Time'] = pd.to_datetime(dataframe['Start Time'])

    # Display Most Common Start Hour
    dataframe['hour'] = dataframe['Start Time'].dt.hour
    popular_hour = dataframe['hour'].mode()[0]
    print("Most Common Hour is {}".format(popular_hour))

    # Display Most Common Month
    dataframe['month'] = dataframe['Start Time'].dt.month
    popular_month_index = dataframe['month'].mode()[0]
    popular_month = months[popular_month_index - 1]
    print("Most Common Month is {}".format(popular_month.title()))

    # Display Most Common Day of Week
    dataframe['day'] = dataframe['Start Time'].dt.day_name()
    popular_day = dataframe['day'].mode()[0]
    print("Most Common Day of the Week is {}\n".format(popular_day))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_stations(dataframe):
    """Displays statistics on the most popular trip, start and end stations."""

    start_time = time.time()
    print("Now Displaying Most Popular Start & End Stations according to specified filters...\n")
    # Display Most Popular Start Station
    popular_start_station = dataframe['Start Station'].mode()[0]
    print("Most Popular Start Station is {}".format(popular_start_station))

    # Display Most Popular End Station
    popular_end_station = dataframe['End Station'].mode()[0]
    print("Most Popular End Station is {}\n".format(popular_end_station))

    # Display Most Popular Trip (From & To)
    dataframe['trip'] = "From " + dataframe['Start Station'] + " To " + dataframe['End Station']
    print("Most Popular Trip (From and To) is {}".format(dataframe['trip'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration(dataframe):
    """Displays statistics on the total and average trip duration."""

    start_time = time.time()
    print("Now Displaying Time Durations of Trips according to specified filters...\n")
    # Display Total Travel Time
    seconds_travelled = dataframe['Trip Duration'].sum()
    minutes_travelled = int(seconds_travelled / 60)
    seconds_travelled = seconds_travelled - 60 * minutes_travelled
    hours_travelled = int(minutes_travelled / 60)
    minutes_travelled = minutes_travelled - 60 * hours_travelled
    print("Total Travel Time is: {} hours, {} minutes, and {} seconds.".format(hours_travelled, minutes_travelled,
                                                                               seconds_travelled))
    # Display Mean Travel Time
    seconds_travelled = dataframe['Trip Duration'].mean()
    minutes_travelled = int(seconds_travelled / 60)
    seconds_travelled = seconds_travelled - 60 * minutes_travelled
    hours_travelled = int(minutes_travelled / 60)
    minutes_travelled = minutes_travelled - 60 * hours_travelled
    print("Average Travel Time is {} hours, {} minutes, and {} seconds.\n".format(hours_travelled, minutes_travelled,
                                                                                  seconds_travelled))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stat(city, dataframe):
    """Displays statistics on bikeshare users."""

    start_time = time.time()
    print("Now Displaying User Statistics for your specified filters...\n")
    # Display counts of user types
    user_types = dataframe['User Type'].value_counts()
    print(user_types)
    print()

    if city != 'washington':
        # Used the following code to check for null values
        # dataframe[  key  ].isnull().values.any()

        # Dealing with Nan values
        dataframe['Gender'] = dataframe['Gender'].fillna("Not Specified")
        dataframe['Birth Year'] = dataframe['Birth Year'].interpolate(method='linear')

        # Display counts of gender
        gender_types = dataframe['Gender'].value_counts()
        print(gender_types)
        print()

        # Display Earliest Date of Birth
        oldest_user = int(dataframe['Birth Year'].min())
        print("Oldest user registered was born in {}\n".format(oldest_user))

        # Display Youngest Date of Birth
        youngest_user = int(dataframe['Birth Year'].max())
        print("Youngest user registered was born in {}\n".format(youngest_user))

        # Display Most Common Date of Birth
        average_birthdate = int(dataframe['Birth Year'].mean())
        print("Average Birthdate is {}\n".format(average_birthdate))

    else:
        print("Gender & BirthDate features aren't available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def print_dataframe(dataframe):
    """ Display five rows of data according to specified filters """

    start_time = time.time()
    x = 0
    y = 5
    print('Printing Individuals Data of specified filters...')
    while y < dataframe.size:
        for row in range(x, y):
            dict_five_rows = pd.Series(data=dataframe.iloc[row], index=dataframe.columns)
            print(dict_five_rows)
            print()
        more_data = input('Load more data? \nType yes or no\n').lower()
        while more_data != 'yes' and more_data != 'no':
            more_data = input('Incorrect Input! Please try again').lower()
        if more_data == 'yes':
            x += 5
            y += 5
        else:
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = apply_filters()
        print()
        dataframe = load_data(city, month, day)
        print()
        trip_stations(dataframe)
        print()
        trip_duration(dataframe)
        print()
        user_stat(city, dataframe)
        print()
        frequent_time(city)

        more_data = input("Do you wish to view individual data? \nType yes or no.\n").lower()
        while more_data != 'yes' and more_data != 'no':
            more_data = input('Incorrect Input! Please try again').lower()
        if more_data == 'yes':
            print_dataframe(dataframe)

        again = input("Do you wish to do more exploring? \nType yes or no.\n").lower()
        while again != 'yes' and again != 'no':
            again = input('Incorrect Input! Please try again').lower()
        if again == 'no':
            print("Thank you! Bye!")
            break


if __name__ == "__main__":
    main()
