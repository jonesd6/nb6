from tkinter import Tk, Entry, Frame, BOTH, Button, filedialog, X
import pandas as pd
import datetime
import calendar

def main():
    pass
def csv_reader(filepath):
    """  Read data from filename.
    
    Reads ES data from .csv files.  
    
     Args:
        directory: The directory in which the .csv file resides.  
        filename: The filename of the .csv file.
           
    Returns:
        A pandas DataFrame with the daily ES data.  
    """
    print("Reading {}.".format(filepath))
    fields = ['Date', 
              'Open', 
              'High', 
              'Low', 
              'Close', 
              'Volume',
              'Open_Interest']
    parse = lambda x: datetime.datetime.strptime(x, '%m/%d/%Y')
    data =  pd.read_csv(filepath,
                        parse_dates=['Date'],
                        date_parser=parse,
                        header = None,
                        names=fields)
                        
    print("Reading {} complete.".format(filepath))
    data = data.set_index(['Date'], drop=False)
    return data

filename = filedialog.askopenfilename()
if filename:
    data = csv_reader(filename)


period_selection = input("Enter time period to test: 'Daily', 'Weekly', or 'Monthly'\n")




#month = selection[1]
month_dict = {name : num for num, name in enumerate(calendar.month_abbr) if num}
if period_selection == 'Monthly':
    date_input = input("Enter a month in the format: 'mm'\n")
    date_selected = datetime.datetime.strptime(date_input, '%m')
    data_month = data[data.index.weekday<5]
    data_month = data_month.groupby(pd.TimeGrouper('1M')).max()
    data_month = data_month.set_index('Date',drop=False)
    data_month = data_month.diff()
    data_month = data_month[data_month.index.month==date_selected.month]
    data_out = data_month

elif period_selection == 'Weekly':
    date_input = input("Enter a month in the format: 'mm'\n")
    date_selected = datetime.datetime.strptime(date_input, '%m')
    week_input = int(input("Enter a week number:\n"))
    data_week = data[data.index.weekday==4].diff()
    data_week = data_week.groupby(pd.TimeGrouper('1M')).nth(week_input-1)
    data_week = data_week[data_week.index.month==date_selected.month]
    data_out = data_week

    
elif period_selection == 'Daily':
    date_input = input("Enter a day in the format: 'mm-dd'\n")
    date_selected = datetime.datetime.strptime(date_input, '%m-%d')
    # Filter dates that fall on weekends.
    # 
    data_day_weekdays = data[data.index.weekday<5]
    data_day_diff = data_day_weekdays.diff()
    data_day_sel = data_day_diff[(data_day_diff.index.month==date_selected.month) &
                                 (data_day_diff.index.day==date_selected.day)]
    data_out = data_day_sel
    
print(data_out)

prob_high = data_out['Close'].gt(0).sum() / data_out['Close'].shape[0]
prob_low = data_out['Close'].lt(0).sum() / data_out['Close'].shape[0]
print("Probability of a higher close on the selected end points: {0}".format(prob_high))
print("Probability of a lower close on the selected end points: {0}".format(prob_low))
save_file = input ("Save file as: ")
data_out.to_csv(save_file + '.csv')




if __name__ == '__main__':
    main()