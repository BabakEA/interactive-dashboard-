# interactive-dashboard-
 python-based application to analysis the baseballs team performances and help clients to win on the online betting

Objectives:

team(s) had the most double headers in 2016.
data frame to shows the number or Wins and Losses for each team.
The game with the most odds changes (Lines field) in 2016? 
Visualize the ML market (MoneyUs2) for this match after using odds.converter to convert MoneyUs2 to probability.
Best Pitchers based of the largest favorite on average for any pitcher with >= 10 starts, using the Closing MoneyLine

How To Run :

Run the Database.R to extract Json file to CSVs
Run the Start.bat or Start.Sh to run the Python file,
Note: I will generates 4 interactives graphs using Dash, Flask Library using : the following Urlhttp://127.0.0.1:8050/

Start.bat Or Start.Sh file:

Installing the python libraries 
pip install pandas, numpuy, decimal, flask, pandas_datareader.data, dash, dash_core_components, dash_html_components, dash.dependencies
Call the project file : 
python Questions.py


The model a Jason file extracted from R library and simulated in python.

The model has an interactive graph reports using Dash library, it’s a competitive library in oppose of the Rshiny on R programming.

Input: Baseball games datasets

Output: Interactive graphs which present pitchers, scores, odds convert and teams performances

 




