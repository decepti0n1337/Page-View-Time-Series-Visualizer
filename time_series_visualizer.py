import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', header=0)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Clean data
threshold_low = df['value'].quantile(0.025)
threshold_high = df['value'].quantile(0.975)
df = df[(df['value'] >= threshold_low) & (df['value'] <= threshold_high)]

def draw_line_plot():
    # Draw line plot

    fig, ax = plt.subplots(figsize=(24, 6))
    plt.plot(df.index, df['value'])

    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy(deep=True)
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    df_bar['month'] = pd.Categorical(df_bar['month'], categories=[
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)

    average_page_views = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(average_page_views))  # Number of bars
    width = 0.7 / len(average_page_views.columns)  # Width of each bar

    years = df_bar.index.year.unique()
    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years)

    for i, month in enumerate(average_page_views.columns):
        ax.bar([p + width * i for p in x], average_page_views[month], width, label=month)

    plt.title('Average Daily Page Views by Month')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')

    plt.legend(title='Months', labels=average_page_views.columns.tolist())

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=month_order)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
