import pymysql
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
# Connect to the MariaDB database
connection = pymysql.connect(
    host='localhost',
    user='rojonbar',
    password='hey',
    database='netflix_top10_data'
)

# Create a cursor object
cursor = connection.cursor()

# Select all data from netflix dataset table
queryNflx = "SELECT * FROM netflix_ds_data"
cursor.execute(queryNflx)

# Fetch the NetflsixDS data into a Pandas DataFrame with column names
netflixDS = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

# Join the netflix data and imdb tables based on common titles. Select the rating values and titles where the category is None English Films
queryNx_imdb = "SELECT rating, title FROM imdb_rating RIGHT JOIN netflix_ds_data ON show_title = title WHERE category = 'Films (Non-English)';"
cursor.execute(queryNx_imdb)


# Fetch the NetflsixDS and imdb data into a Pandas DataFrame with column names
nflx_imdbDS = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

# Join netflix data and runtime table based on common english film titles
queryNx_runtime = "SELECT * FROM runtime RIGHT JOIN netflix_ds_data ON show_title = title WHERE category = 'Films (English)';"
cursor.execute(queryNx_runtime)


# Fetch the NetflsixDS and runtime data into a Pandas DataFrame with column names
nx_runtime = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
# Close the cursor
cursor.close()

##########################################################
# 1.) Identifying the English TV show with most top 10
#     appearances and its average hours viewed
##########################################################
print(netflixDS.columns)
#a.) Instantiate English TV show variable
englishTv = netflixDS['category'] == 'TV (English)'
#b.) Filter english shows from dataset
englishTvFilt = netflixDS[englishTv]
#c.) Find the most frequently apparent english show title
modeShowEng = englishTvFilt['show_title'].mode()
#d.) Print the most apparent show title
print("The English TV show with the most appearances in the top 10 list is ", modeShowEng.to_list())
#e.) Create a filter to only maintain data from the mode
#    english show's appearances
modeShowFilt = netflixDS[netflixDS['show_title'].isin(modeShowEng)]
#f.) Determine the average hours the show was watched
meanHrsViewed = modeShowFilt['weekly_hours_viewed'].mean()
#g.) Print the average ours the show was watched
print("The average weekly hours viewed for the top english show is ", meanHrsViewed)
##########################################################
# 2.) Identifying the Non-English Film with the lowest IMDB
#     rating
############################################################
#a.) Find the index of the lowest rating
minRatingIdx = nflx_imdbDS['rating'].idxmin()
#b.) Locate the film title with the minimum rating
minRateTitle = nflx_imdbDS.loc[minRatingIdx, 'title']
#c.) Print the lowest rated title
print("The lowest Non English film is", minRateTitle)
#e.) Create a list containing the lowest rated non-english film title
minRateTitleList = [minRateTitle]
#f.) Create a Filter to only maintain data about the lowest rated Non eng
#    film in the Netflix Data list
minRateFilt = netflixDS[netflixDS['show_title'].isin(minRateTitleList)]
#g.) Determine the mean hours viewed
meanHrsViewed_nonEng = minRateFilt['weekly_hours_viewed'].mean()
#h.) Print the mean hours viewed
print("The average weekly hours viewed for the lowest rated non english film is ", meanHrsViewed_nonEng)
##########################################################
# 3.) Identifying the English Film with the most cumulative weeks in the top 10
#     and Approximating the number of users who watched the film
############################################################
#a.) Instantiate English Film  variable
englishFilm = netflixDS['category'] == 'Films (English)'
#b.) Filter english Films from dataset
englishFilmFilt = netflixDS[englishFilm]
#c.) Find the  index of the english film with the maximum cummulative weeks in top 10
maxCumWeeksIdx = englishFilmFilt['cumulative_weeks_in_top_10'].idxmax()
#b.) Locate the english film title with the max weeks
maxCumWeeksTitle = englishFilmFilt.loc[maxCumWeeksIdx, 'show_title']
#d.) Print the english film with the most cumulative weeks
print("The English Film  with the most cumulative weeks in the top 10 list is ", maxCumWeeksTitle)
#e.) Create a list containing the max weeks title
maxWeeksTitleList = [maxCumWeeksTitle]
#f.) Create a Filter to only maintain data about the max week
#    film in the Netflix Data list
maxWeeksFilter = netflixDS[netflixDS['show_title'].isin(maxWeeksTitleList)]
#g.) Determine the mean hours viewed
meanHrsViewed_FilmEng = maxWeeksFilter['weekly_hours_viewed'].mean()
#h.) Print the mean hours viewed
print("The average weekly hours viewed for the english film with max cummulative weeks in the top 10 is ", meanHrsViewed_FilmEng)
#modeShowFilt = netflixDS[netflixDS['show_title'].isin(modeShowEng)]
#i.) Locate the film's maximum cumulative weeks
maxCumWeeks = englishFilmFilt.loc[maxCumWeeksIdx, 'cumulative_weeks_in_top_10']
#j.) Print the mean hours viewed
print("The max cummulative weeks in the top 10 is ", maxCumWeeks)
#k.) Find the  index of the english film with the maximum cummulative weeks in top 10
#    in the nx_rt dataframe
maxCumWeeksIdx_nxRt = nx_runtime['cumulative_weeks_in_top_10'].idxmax()
#l.) Locate the english film runtime for the title with the max weeks
maxCumWeeksRuntime = nx_runtime.loc[maxCumWeeksIdx_nxRt, 'runtime']
#j.) Print the runtime
print("The film with the cummulative weeks in the top 10's runtime is ", maxCumWeeksRuntime)
#k.)Calculate the approximate number of users who watched the show
approxNumUsers = (meanHrsViewed_FilmEng * 60 * maxCumWeeks)/118
#l.) Print the approximate number of viewers
print("The approximate number of viewers who watch the English Film with the max cumulative weeks in the top 10 is ", approxNumUsers)
######################################################################
# 4.) Plot weekly hours viewed over time (as an aggregate and
#     for each of the four categories). Document trends.
###################################################################
# a.) Group the data by 'category' and 'week' and the sum of 'weekly_hours_viewed'
category_weekly_hours = netflixDS.groupby(['category', 'week'])['weekly_hours_viewed'].sum().reset_index()
#b.) Pivot the data to have categories as columns
pivot_data = category_weekly_hours.pivot(index='week', columns='category', values='weekly_hours_viewed')
#c.) Plot the data
plt.figure(figsize=(12, 6))
for category in pivot_data.columns:
    plt.plot(pivot_data.index, pivot_data[category], label=category)
#e.) Label the X-axis Week
plt.xlabel('Week')
#f.) Label the Y-Axis Weekly Hours Viewed
plt.ylabel('Weekly Hours Viewed (in hundred millions)')
#g.) The title is Weekly Hours Viewed Over Time by Category
plt.title('Weekly Hours Viewed Over Time by Category')
#h.) Crate a legend to differentiate between category lines
plt.legend()
#i.) Produce a grid for the line chart
plt.grid()
#j.) Display the line chart
plt.show()





