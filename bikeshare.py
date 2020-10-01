import time
import pandas as pd
import numpy as np


# used Practice Problem #3: Load and Filter the Dataset
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. No need to capitalize.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
	print('\nHello! Let\'s explore some US bikeshare data! Have fun!\n')
    
    # get user input for city (chicago, new york city, washington).
    # see readme.txt -- referenced https://wiki.python.org/moin/WhileLoop for help on while loops
    # see readme.txt -- referenced https://docs.python.org/3/tutorial/inputoutput.html for help on fancier input
    while True:
        city = input('What city would you like to view bikeshare statistics for? Choose Chicago, New York City, or Washington: ').lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print(F"You entered {city}. Choose Chicago, New York City, or Washington. Try again, please!\n")
            continue
        else:
            print("Thanks. Next question.\n")
            break
            
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('What month? Choose January, February, March, April, May, June, or all (for all months): ').lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
            print(F"You entered {month}. Enter one of the months listed or all. Try again, please!\n")
            continue
        else:
            print("Thanks. Next question.\n")
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('What day of the week? Choose Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all (for all days): ').lower()
        if day not in ( 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print(F"You entered {day}. Enter one of the days listed or all. Try again, please!\n")
            continue
        else:
            break

    print('-'*70)
    
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]    

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('The most common month is', popular_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day of week is', popular_day)

    # display the most common start hour
    # referenced Practice Solution #1: Compute the Most Popular Start Hour for help on finding the most commmon start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour is', popular_hour)

    print("\nThis took %s seconds" % (time.time() - start_time))
    print('-'*70)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most common used start station is', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most common used end station is', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['freq_combo'] = df['Start Station'] + ' (start station) ' + 'to '  + df['End Station'] + ' (end station)'
    most_freq_combo = df['freq_combo'].mode()[0]
    print('The most frequent combination of start station and end station trip is', most_freq_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*70)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(F'Total travel time is', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Total mean travel time is', mean_travel_time)
   
    print("\nThis took %s seconds" % (time.time() - start_time))
    print('-'*70)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    # referenced Practice Solution #2: Display a Breakdown of User Types for help on displaying counts of user types
    counts_user_types = df['User Type'].value_counts()
    print('Counts of user types is equal to:')
    print(counts_user_types)

    # display counts of gender
    # some cities do not have gender or birth year, need to check for this
    if 'Gender' in df:
        counts_gender = df['Gender'].value_counts()
        print('\nCounts of gender is equal to:')
        print(counts_gender)
    else:
        print('\nNo gender data in the city chosen!')

    #  display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birthyear = df['Birth Year'].min()
        most_recent_birthyear = df['Birth Year'].max()
        most_common_birthyear = df['Birth Year'].mode()[0]
        print('\nEarliest year of birth:',earliest_birthyear)
        print('Most recent year of birth:',most_recent_birthyear)
        print('Most common year of birth:',most_common_birthyear)
    else:
        print('No birth year data in the city chosen.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*70)


def show_data(df):
    """Displays promt for user to input number of rows that would like to see"""   
    # continue these prompts and displays until the user says 'no'
    # see readme.txt --- referenced https://docs.python.org/3/tutorial/errors.html for help on error handling to check for integer input
    while True:
        view_data = input('Do you want to see the raw data? Enter yes or no: ')
        if view_data not in ('yes', 'no'):
           print("Please try again. Enter yes or no.\n")
           continue
        elif view_data == 'yes':
            while True:
                try:
                    num_rows = int(input('How many rows of data do you want to see? Enter integer from 1 - 300000: '))
                    print(df.iloc[0:num_rows])
                    break
                except ValueError:
                    print("That was not a valid number.  Try again...")
            continue
        else:
           break
        return


def main(): 
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
