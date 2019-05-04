import time
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

now = datetime.datetime.now()

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Choose a city to start [Chicago / New York city / Washington / All]): ").lower()
    while city not in CITY_DATA and city !='all':        
        city = input("Not a valid city! Please input again: ").lower()
        continue 
    
    # TO DO: get user input for month (all, january,y, ... , june)
    op = input("Would you like to filter the data by month? [yes/no],[y/n]: ").lower()  
    if op == 'yes' or op == 'y':
        month = input("Choose a month: ").lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        while month not in months:
            month = input("Not a valid month, please input again:").lower()
            continue
    else:
        month='all'
        
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    op = input("Would you like to filter the data by day of week? [yes/no],[y/n]: ").lower()
    if op == 'yes' or op == 'y':
        day = input("Choose a day: ").title()
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        while day not in weekdays:
            day = input("Not a valid day of week, please input again:").title()
            continue
    else:
        day='all'


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
    if city == 'all':
        dfs = [pd.read_csv(CITY_DATA[city]) for city in CITY_DATA]
        df = pd.concat(dfs, sort=False)
    else:
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
    
    # display total records after filter
    total_records = df['Start Time'].count()
    print("Analysis based on",total_records,"records:\n")
    
    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    
    print('Most Popular Month:', popular_month)
    

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
              
    print('Most Popular Day of Week:', popular_day)
    

    # TO DO: display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Start Hour'].mode()[0]
              
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
        
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # TO DO: display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " -> " + df['End Station']
    popular_trip = df['trip'].mode()[0]
    
    print("Most Popular Trip: ",popular_trip)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    print("Total Travel Time: {} h {} m".format(int(total_duration/3600), int(total_duration%3600/60)))

    # TO DO: display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print("Average Travel Time: {} h {} m".format(int(mean_duration//3600), int(mean_duration%3600//60)))
    
    # BONUS: display most common travel time
    common_duration = df['Trip Duration'].mode()[0]
    print("Common Travel Time: {} h {} m".format(int(common_duration//3600), int(common_duration%3600//60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    try:
        user_genders= df['Gender'].value_counts()
    except:
        print('\nNo Gender Data For This City.')
    else:   
        print("\n")
        print(user_genders)
    
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])
        df['Age']= now.year - df['Birth Year']
        print("\nOldest User Born in {}, Age {}".format(oldest, now.year - oldest))
        print("Yougest User Born in {}, Age {}".format(youngest, now.year - youngest))
        print("Most Users Born in {}, Age {}".format(common, now.year - common))
        
    except:
        print("\nNo Birth Year Data For This City")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # BONUS: plot for results
    anw = input("\nDo you want to see some plot of the results? [yes/no] [y/n]: ").lower()
    if anw == 'y' or anw == 'yes':
        
        i = 231
        plt.figure(figsize=(15,8))
        #plt.title('Analysis based on records')
        for key in ['month','day_of_week','Start Hour','User Type','Gender','Age']:
            try:
                plt.subplot(i)
                df.groupby([key])[key].count().plot(kind = 'bar', color = 'grey')
                plt.title('By {}\n Most Popular: {}'.format(key,df[key].mode()[0]),fontsize=10)
                plt.xlabel('')
                plt.xticks(rotation = 45)

            except:
                plt.title('By {} (Missing Data)'.format(key),fontsize=10)                
            finally:
                i+=1

        plt.show()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? [yes/no] [y/n]: ').lower()
        if restart != 'yes'and restart != 'y':
            break


if __name__ == "__main__":
	main()
