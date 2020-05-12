

# data load
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
from datetime import datetime
#import calendar
import math

df = pd.read_csv("Data/us_states_covid19_daily.csv",index_col=False)

df = df.set_index(pd.to_datetime(df['date'], format="%Y%m%d"))

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

df = df[df.state.isin(list(states.keys()))]
df = df[['state', 'positive', 'negative',
           'hospitalizedCurrently', 'hospitalizedCumulative', 'inIcuCurrently',
           'inIcuCumulative', 
           'recovered', 'death', 'hospitalized',
           'deathIncrease',
           'hospitalizedIncrease',
           ]]
import datetime
df_full = pd.DataFrame()
for state in list(states.keys()): #list(states.keys()) #["NY"]
    df_state = df[df.state==state]
    df_state = df_state.sort_index()
    weeks = range(0,int(1+len(df_state)/7)*7,7)
    df_state_week = df_state.iloc[weeks,:]
    df_state_week["new_cases"] = (df_state_week.positive-df_state_week.positive.shift(periods=1)).to_numpy()
    df_state_week["date_string"] = df_state_week.index.strftime('%Y-%m-%d')
    df_state_week["week_number"] = range(len(df_state_week))
    df_state_week["new_cases"][0]=1
    df_state_week["color"] = 'blue'
    df_state_week["change"] = df_state_week.new_cases.pct_change()
    df_state_week["death_change"] = df_state_week.death.pct_change()
    # add two new predictions
    for i in range(2):
        temp = (df_state_week.iloc[-1])
        temp.change=df_state_week.iloc[-1].change*0.80+df_state_week.iloc[-2].change*0.2
        temp.new_cases = math.ceil(temp.new_cases*(1+temp.change))
        temp.positive = temp.positive+temp.new_cases
        temp.week_number = temp.week_number + 1
        temp.death = temp.death + math.ceil(temp.death*(temp.death_change))
        temp.color = "red"
        temp.date_string = str(df_state_week.index[-1] + datetime.timedelta(days=7))[:10]
        df_state_week.loc[df_state_week.index[-1] + datetime.timedelta(days=7)] = temp
    df_full = df_full.append(df_state_week)
    
    
    
####
# Import figure from bokeh.plotting
from bokeh.plotting import figure

# Import the ColumnDataSource class from bokeh.plotting
from bokeh.plotting import ColumnDataSource

# Import output_file and show from bokeh.io
from bokeh.io import output_file, show

N=4
state = "NY"
# Create a ColumnDataSource: source
source = ColumnDataSource(data={'positive': df_full[df_full.state==state].iloc[:(N+2)].positive.tolist(),
                                'new_cases': df_full[df_full.state==state].iloc[:(N+2)].new_cases.tolist(),
                               "date_string" : df_full[df_full.state==state].iloc[:(N+2)].date_string.tolist(),
                                "week_number" : df_full[df_full.state==state].iloc[:(N+2)].week_number.tolist(),
                                "death" : df_full[df_full.state==state].iloc[:(N+2)].death.tolist(),
                                "color_test" : df_full[df_full.state==state].iloc[:(N+2)].color.tolist()
                               })    

    
    
# Create a figure with x_axis_type='datetime': p
p = figure(tools = "",title = "COVID-19 development in each US state",plot_width=700*0.65,plot_height=400*0.65,x_axis_type='log',y_axis_type='log', x_axis_label='Total confirmed cases', y_axis_label='New weekly cases')

# Plot date along the x-axis and price along the y-axis
p.line(x='positive', y='new_cases',source=source)

# Add circle glyphs to the figure p
p.circle(x='positive', y='new_cases',fill_color="color_test", size=8, source=source,legend = "Observed")

p.circle(x=[0], y=[0],fill_color="red", size=8,legend = "Prediction")


# import hoverTool form bokeh.models
from bokeh.models import HoverTool

# creat a hovertool object: hover
hover = HoverTool(tooltips=[('Date','@date_string'),("Week","@week_number"),("Total Confirmed cases","@positive"),("Total new weekly cases","@new_cases"),("Total deaths","@death")])
# add the hovertool object to my figure
p.add_tools(hover)


from bokeh.models import ColumnDataSource, Slider

slider = Slider(start=0,end=12,value=N+1,step=1,title="Week")

# Define a callback function: callback
def callback(attr, old, new):

    # Read the current value of the slider: scale
    N = slider.value + 1
    state = states_short[menu.value]
    # Update source with the new data values
    source.data = {'positive': df_full[df_full.state==state].iloc[:N].positive.tolist(),
                                'new_cases': df_full[df_full.state==state].iloc[:N].new_cases.tolist(),
                               "date_string" : df_full[df_full.state==state].iloc[:N].date_string.tolist(),
                                "week_number" : df_full[df_full.state==state].iloc[:N].week_number.tolist(),
                                "death" : df_full[df_full.state==state].iloc[:N].death.tolist(),
                                "color_test" : df_full[df_full.state==state].iloc[:(N)].color.tolist()
                                }

# Attach the callback to the 'value' property of slider
slider.on_change('value', callback)



from bokeh.models import Select
states_short = {}
for i in range(len(list(states.values()))):
    states_short[list(states.values())[i]] = list(states.keys())[i]


menu = Select(options=list(states.values()),value= "New York",title = "Select State")

def callback2(attr, old, new):
    state = states_short[menu.value]
    N = slider.value + 1 
    source.data = {'positive': df_full[df_full.state==state].iloc[:N].positive.tolist(),
                                'new_cases': df_full[df_full.state==state].iloc[:N].new_cases.tolist(),
                               "date_string" : df_full[df_full.state==state].iloc[:N].date_string.tolist(),
                                "week_number" : df_full[df_full.state==state].iloc[:N].week_number.tolist(),
                                "death" : df_full[df_full.state==state].iloc[:N].death.tolist(),
                                "color_test" : df_full[df_full.state==state].iloc[:(N)].color.tolist()
                                }
menu.on_change("value",callback2)

p.legend.location = "top_left"

from bokeh.io import curdoc
from bokeh.layouts import column
# Create layout and add to current document
layout = column(p,slider,menu)
curdoc().add_root(layout)  

