import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' };
months = ['january', 'february', 'march', 'april', 'may', 'june'];
days= ['monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday', 'sunday'];

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
    while True:
        city_name = str(input('Please enter one of the cities Chicago, Washington or New York City for your analysis : ')).lower();
        if city_name == 'chicago':
            city_name =CITY_DATA[city_name]
            break;
        elif city_name == 'washington':
            city_name =CITY_DATA[city_name]
            break;
        elif city_name == 'new york city':
            city_name =CITY_DATA[city_name]
            break;
        else: 
            # city_name not match please input again
            print('city_name not match');
            continue;

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
         month = str(input('Please enter any one of the first 6 months or enter All to select all 6 months : ')).lower();
         
         if month == 'january':
            month = months[0]
            break;
         elif month == 'february':
            month = months[1]
            break;
         elif month == 'march':
            month = months[2]
            break;
         elif month == 'april':
            month = months[3]
            break;
         elif month =='may':
            month = months[4]
            break;
         elif month == 'june':
            month = months[5]
            break;
         elif month == "all":
            print('no month need filter');
            break;
         else: 
            print('name of the month not match');
            continue;


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = str(input('input name of the day of week for filter by day, or can input "all" for no day need filter : ')).lower();
            

            if day == 'monday':
                day = days[0]
                break;
            elif day == 'tuesday':
                day = days[1]
                break;
            elif day == 'wednesday':
                day = days[2]
                break;
            elif day == 'thursday':
                day = days[3]
                break;
            elif day =='friday':
                day = days[4]
                break;
            elif day == 'saturday':
                day = days[5]
                break;
            elif day == 'sunday':
                day = days[6]
                break;
            elif day == 'all':
                print('no month need filter');
                break;
            else: 
                print('name of the day of week not match');
                continue;

    print('-'*40)
    return city_name, month, day


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
    
    df = pd.read_csv(city);
    df['Start Time'] = pd.to_datetime(df['Start Time']);
    df['month'] = df['Start Time'].dt.month;
    df['day_of_week'] = df['Start Time'].dt.weekday_name;
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1;
        df = df[df['month'] == month];

    if day != 'all':
        df = df[df['day_of_week'] == day.title()];
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_mode = pd.Series(pd.DatetimeIndex(df['Start Time'])).dt.month.mode();
    print("display the most common month : ", month_mode);


    # TO DO: display the most common day of week
    week_day_mode = pd.Series(pd.DatetimeIndex(df['Start Time'])).dt.weekday_name.mode();
    print("display the most common day of week : ", week_day_mode);

    # TO DO: display the most common start hour
    hour_mode = pd.Series(pd.DatetimeIndex(df['Start Time'])).dt.hour.mode();
    print("display the most common start hour : ", hour_mode)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    data_frame = df['Start Station'];
    start_station = data_frame.mode();
    print("display most commonly used start station : ",start_station );
    # TO DO: display most commonly used end station
    end_station = df['Start Station'].mode();
    print("Most Common Used End Station : ",end_station);

    # TO DO: display most frequent combination of start station and end station trip
    df["frequent stations"] = df["Start Station"].map(str) + " to " + df["End Station"]
    frequent_station_mode = df["frequent stations"].mode()
    print ("display most frequent combination of start station and end station trip : ", frequent_station_mode)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("display total travel time : ", total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print ("display mean travel time : ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    sub = len(df[df["User Type"] == "Subscriber"]);
    cus = len(df[df["User Type"] == "Customer"]);
    print ('subscribers : ' , sub);
    print ('customers : ', cus);

    # TO DO: Display counts of gender
    try:    
        males = len(df[df["Gender"] == "Male"])
        females = len(df[df["Gender"] == "Female"])
    except:    
        print('get gender data error')
    else:
        print('Males : ', males);
        print('Females : ', females);

    # TO DO: Display earliest, most recent, and most common year of birth
    try:    
        earliest = df['Birth Year'].min();
        most_recent = df['Birth Year'].max();
        most_common = df['Birth Year'].mode();
    except:
        print('get Birth Year data error');
    else:
        print ('Earliest : ', earliest);
        print ('Most recent : ', most_recent);
        print ('Most common : ', most_common);

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ display raw data each time 5 rows """
    i = 0
    raw = str(input("\nDo you need to see raw data from ? yes or no.\n")).lower();
    pd.set_option('display.max_columns',200)

    while True:            
        if raw == 'no':
            break;
        elif raw == 'yes':
            print(df[i:i+5]);
            raw = str(input("\nDo you need to see raw data ? yes or no.\n")).lower();
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
