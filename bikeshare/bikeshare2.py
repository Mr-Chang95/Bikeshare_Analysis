import time
import pandas as pd
import numpy as np
import calendar

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
months = ['january', 'february', 'march', 'april', 'may', 'june']
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
    print('Hello! Let\'s explore some US bikeshare data!')
# get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to analyze the data for Chicago, New York City, or Washington?\n").lower()
        print()
        if city in CITY_DATA.keys():
            print(f"It looks like you selected {city.title()}. \nIf this isn't correct, please restart program.")
            break
        else:
            print("Sorry invalid input. Please select Chicago, New York City, or Washington.")
# get user input for month (all, january, february, ... , june)
    while True:
        filter = input("Would you like to filter the data by month, day, or nothing? ").lower()
        filters = ["month", "day", "nothing"]
        if filter in filters:
            if filter == "month":
                month = input("""Which month - January, February, March, April, May, or June?
Please type out the full name of month.
Type 'all' to apply no filter""").lower()
                if month in months:
                    day = "all"
                    break
                elif month == "all":
                    day = "all"
                    month = "all"
                    break
                else:
                    print()
                    print("Please input month full name correctly! Let's start over.")
        # get user input for day of week (all, monday, tuesday, ... sunday)
            elif filter == "day":
                day = input("""Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?
Please type the full name of day.
Type 'all' to apply no filter""").lower()
                if day in days:
                    month = "all"
                    break
                elif day == "all":
                    day = "all"
                    month = "all"
                    break
                else:
                    print()
                    print("Please input day full name correctly! Let's start over.")
            elif filter == "nothing":
                print("You have selected 'nothing'. ")
                day = "all"
                month = "all"
                break
        elif filter not in filters:
            print("Please input: 'month', 'day', or 'nothing'")

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
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
# convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
# extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
# filter by month if applicable
    if month != 'all':
    # use the index of the months list to get the corresponding int
        print("Filtering by month. You have selected {}".format(month.title()))
        month = months.index(month) + 1
    # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        #day = days.index(day)

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    #print(df["month"].head())
    #print(df["day_of_week"].head())
    #print(df["day_of_week"].head())

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    if month == "all" and day != "all":
        common_month = df["month"].value_counts().idxmax()
        print('Most Common Month:', calendar.month_name[common_month])
    # display the most common day of week
    elif day == "all" and month != "all":
        common_day = df["day_of_week"].value_counts().idxmax()
        print('Most Common Day of Week:', common_day)
    elif (day != "all" and month != "all") or (day == "all" and month == "all"):
        common_month = df["month"].value_counts().idxmax()
        common_day = df["day_of_week"].value_counts().idxmax()
        print('Most Common Month: ', calendar.month_name[common_month])
        print('Most Common Day of Week: ', common_day)
    print()

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {common_hour}:00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df["Start Station"].mode()[0]
    print("Most Common Start Station: \n", common_start)
    # display most commonly used end station
    common_end = df["End Station"].mode()[0]
    print("Most Common End Station: \n", common_end)
    # display most frequent combination of start station and end station trip
    df["Trip Combo"] = df["Start Station"] + " --> " + df["End Station"]
    common_combo = df["Trip Combo"].mode()[0]
    print(f"Most Common Trip Combo.: {common_combo}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #print("DF from  trip_duration_stats(): ", df.head())
    # display total travel time
    total_travel = df["Trip Duration"].sum()
    adjusted_total = total_travel/3600
    print(f"Total Travel Time: {total_travel} hours.")

    # display mean travel time
    avg_travel = df["Trip Duration"].mean()
    adjusted_avg = avg_travel/60
    print(f"Average Travel Time: {adjusted_avg} minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df["User Type"].value_counts()
    print(user_types_count)

        # Display counts of gender

    if city != "washington":
        gender_count = df["Gender"].value_counts(dropna=False)
        print(f"Gender Count: \n{gender_count}")

        # Display earliest, most recent, and most common year of birth
        earliest_birth = df["Birth Year"].sort_values(ascending = True)
        latest_birth = df["Birth Year"].sort_values(ascending = False)
        common_birth = df["Birth Year"].mode()[0]

        print("Earliest Birth Year: \n",earliest_birth.iloc[0])
        print("Most Recent Birth Year: \n",latest_birth.iloc[0])
        print("Common Birth Year: \n", common_birth)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def view_datas(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
    start_loc = 0
    if view_data != 'no':
        while True:
            print(df.iloc[start_loc: start_loc + 5])
            start_loc += 5
            view_display = input("Do you wish to continue?: ").lower()
            if view_display == "no":
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        view_datas(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
