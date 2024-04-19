import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
#df.set_index('date', inplace=True, drop=False)
df['date'] = pd.to_datetime(df['date'])
# Clean data
percen2_5 = df['value'].quantile(0.025)
percen_97_5 = df['value'].quantile(0.975)
df = df.loc[~((df['value'] <= percen2_5) | (df['value'] >= percen_97_5))]


def draw_line_plot():
    # Draw line plot

    fig, ax = plt.subplots() 
    ax.plot(df['date'], df['value'])
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['date_str'] = df_bar['date'].dt.strftime('%Y-%m-%d')
    df_bar[['Year', 'Months', 'Day']] = df_bar['date_str'].str.split('-', expand=True)
    month = {'01': 'January', '02':'February', '03':'March', '04': 'April', '05':'May', '06':'June', '07':'July', '08':'August',
             '09':'September', '10':'October', '11':'November','12':'December'}

    df_bar = df_bar.groupby([df_bar['Year'],df_bar['Months']])
    df_bar = df_bar['value'].mean()
    df1 = df_bar.reset_index()

    df1.columns = ['Year', 'Months', 'Value']
    df1 = df1.sort_values('Months', ascending=True)
    df1['Months'] = df1['Months'].map(month)
    meses_ordenados = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df1['Months'] = pd.Categorical(df1['Months'], categories=meses_ordenados, ordered=True)

   
    # Draw bar plot
    df1 = df1.sort_values('Year', ascending=True)
    fig, ax = plt.subplots(figsize=(12, 6))
    df1.pivot("Year", "Months", "Value").plot(kind='bar', ax=ax)
    ax.set_xticklabels(df1['Year'].unique(), rotation=45)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months', labels=meses_ordenados)
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    meses_ordenados = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=meses_ordenados, ordered=True)
    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
   
    sns.boxplot(data=df_box, x="year", y="value", ax=axs[0], palette= sns.color_palette("pastel"))
    axs[0].set_title("Year-wise Box Plot (Trend)")
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')

    sns.boxplot(data=df_box, x="month", y="value", ax=axs[1], palette= sns.color_palette("deep"))
    axs[1].set_title("Month-wise Box Plot (Seasonality)")
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')





    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
