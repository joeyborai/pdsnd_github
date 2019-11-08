import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city, month, day = '', '', ''
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while not city in ['chicago', 'new york city', 'washington']:
        city = input("Enter the city that you would like to collect data for(Chicago, New York City, Washington): ").lower()

    # get user input for month (all, january, february, ... , june)
    while not month in ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all']:
        month = input("Enter the month that you would like to collect data for: ").lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while not day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        day = input("Enter the day of the week that you would like to collect data for: ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    city = city.replace(' ', '_')
    df = pd.read_csv(str(city) + '.csv')

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['Week Day'] = df['Start Time'].dt.weekday_name
    df['Month'] = df['Start Time'].dt.month_name()


    if day != 'all':
        df = df[df['Week Day'].str.lower() == day]
    if month != 'all':
        df = df[df['Month'].str.lower() == month]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_groups = df['Month'].value_counts()
    print('Most common month of travel was: ' + str(month_groups.index[0]))

    # display the most common day of week
    day_counts = df['Week Day'].value_counts()
    print('Most popular weekday for travel was: ' + str(day_counts.index[0]))

    # display the most common start hour
    hours = df['Start Time'].dt.hour
    hour_counts = hours.value_counts()
    print('Most popular hour for travel was: ' + str(hour_counts.index[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_count = df['Start Station'].value_counts()
    print('Most popular start station was: ' + str(start_count.index[0]))

    # display most commonly used end station
    end_count = df['End Station'].value_counts()
    print('Most popular end station was: ' + str(end_count.index[0]))

    # display most frequent combination of start station and end station trip
    combo_stations = df.groupby(['Start Station', 'End Station'])
    combo_counts = combo_stations.count()
    combo_counts['count'] = combo_counts['Unnamed: 0']

    print('Most popular start/end station combo was: ' + str(combo_counts['count'].idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print('Total travel time is: ' + str(total))

    # display mean travel time
    mean = total/df['Trip Duration'].count()
    print('Average travel time was: ' + str(mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df.groupby(['User Type']).count()
    user_counts['count'] = user_counts['Unnamed: 0']
    print('Count for each type of user: \n' + str(user_counts['count']) + '\n\n')

    # Display counts of gender
    gender_counts = df.groupby(['Gender']).count()
    gender_counts['count'] = gender_counts['Unnamed: 0']
    print('Count of user genders for travel: \n' + str(gender_counts['count']) + '\n\n')

    # Display earliest, most recent, and most common year of birth
    early_year = df['Birth Year'].min()
    latest_year = df['Birth Year'].max()
    common_year = df['Birth Year'].value_counts()

    print('Earliest birth year was : ' + str(early_year))
    print('Most recent birth year was : ' + str(latest_year))
    print('Most common birth year was : ' + str(common_year.index[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
