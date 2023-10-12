--CREATE Netflix Top10 Stats Table
CREATE TABLE netflix_ds_data
 (
	category			VARCHAR(30),
	cumulative_weeks_in_top_10 	INT,
	weekly_hours_viewed		INT,
	season_title			VARCHAR(100),
	weekly_rank			INT,
	show_title			VARCHAR(100),
	date_added			DATE,
	week				DATE
);
--CREATE IMDB Rating Table
CREATE TABLE imdb_rating 
(
	title				VARCHAR(100),
	rating				DECIMAL(2,1)
);
--CREATE runtime table
CREATE TABLE runtime 
(
	title				VARCHAR(100),
	runtime				INT
);

-- Load data from the Netflix Data CSV file
LOAD DATA INFILE 'C:/NFLX_DS_9_23/NFLX_DS_data_9_23.csv'
INTO TABLE netflix_ds_data
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'  -- Change this to '\n' to correctly terminate lines
IGNORE 1 ROWS
(category, cumulative_weeks_in_top_10 , weekly_hours_viewed, season_title, weekly_rank, show_title, @date_added, @week)
SET date_added = STR_TO_DATE(@date_added, '%m/%d/%Y'), week = STR_TO_DATE(@week, '%m/%d/%Y');
-- Load data from the Runtime CSV file
LOAD DATA INFILE 'C:/NFLX_DS_9_23/Runtime.csv'
INTO TABLE runtime
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
-- Load data from the IMDB Rating CSV file
LOAD DATA INFILE 'C:/NFLX_DS_9_23/IMDb Rating.csv'
INTO TABLE imdb_rating
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;




	
	