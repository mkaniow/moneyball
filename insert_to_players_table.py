'''
This script insert active players and their teams in season 2023/2024
The lists of names used in dict 'players' was created by script rosters.py
'''
import pandas as pd
import mysql.connector
from create_tuples import create_list_of_tuples
from password import *

#connect to db
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password=pw,
    database='moneyball_db'
    )

mycursor = db.cursor()

players = {
    'ATL': ['Saddiq Bey', 'Bogdan Bogdanovic', 'Kobe Bufkin', 'Clint Capela', 'Bruno Fernando', 'Trent Forrest', 'AJ Griffin', 'Mouhamed Gueye', "De'Andre Hunter", 'Jalen Johnson', 'Vit Krejci', 'Seth Lundy', 'Garrison Mathews', 'Wesley Matthews', 'Patty Mills', 'Dejounte Murray', 'Miles Norris', 'Onyeka Okongwu', 'Trae Young'],
    'BOS': ['Dalano Banton', 'Oshae Brissett', 'Jaylen Brown', 'JD Davison', 'Wenyen Gabriel', 'Sam Hauser', 'Jrue Holiday', 'Al Horford', 'Luke Kornet', 'Svi Mykhailiuk', 'Drew Peterson', 'Kristaps Porzingis', 'Payton Pritchard', 'Neemias Queta', 'Lamar Stevens', 'Jayson Tatum', 'Jordan Walsh', 'Derrick White'],
    'BKN': ['Mikal Bridges', 'Nicolas Claxton', 'Noah Clowney', 'Spencer Dinwiddie', 'Dorian Finney-Smith', 'Harry Giles III', 'Keon Johnson', 'Cameron Johnson', "Royce O'Neale", "Day'Ron Sharpe", 'Ben Simmons', 'Dennis Smith Jr.', 'Cameron Thomas', 'Lonnie Walker IV', 'Trendon Watford', 'Dariq Whitehead', 'Jalen Wilson'],
    'CHA': ['Amari Bailey', 'LaMelo Ball', 'Leaky Black', 'James Bouknight', 'Miles Bridges', 'Gordon Hayward', 'Cody Martin', 'Bryce McGowens', 'Nathan Mensah', 'Brandon Miller', 'Frank Ntilikina', 'Nick Richards', 'Terry Rozier', 'Ish Smith', 'Nick Smith Jr.', 'JT Thor', 'PJ Washington', 'Mark Williams'],
    'CHI': ['Lonzo Ball', 'Onuralp Bitim', 'Jevon Carter', 'Alex Caruso', 'Torrey Craig', 'DeMar DeRozan', 'Ayo Dosunmu', 'Henri Drell', 'Andre Drummond', 'Zach LaVine', 'Julian Phillips', 'Adama Sanogo', 'Terry Taylor', 'Dalen Terry', 'Nikola Vucevic', 'Coby White', 'Patrick Williams'],
    'CLE': ['Jarrett Allen', 'Emoni Bates', 'Darius Garland', 'Ty Jerome', 'Damian Jones', 'Caris LeVert', 'Sam Merrill', 'Donovan Mitchell', 'Evan Mobley', 'Isaiah Mobley', 'Georges Niang', 'Isaac Okoro', 'Craig Porter Jr.', 'Max Strus', 'Tristan Thompson', 'Dean Wade'],
    'DET': ['Marvin Bagley III', 'Bojan Bogdanovic', 'Alec Burks', 'Malcolm Cazalon', 'Cade Cunningham', 'Jalen Duren', 'Joe Harris', 'Killian Hayes', 'Jaden Ivey', 'Kevin Knox II', 'Isaiah Livers', 'Monte Morris', 'Jared Rhoden', 'Marcus Sasser', 'Isaiah Stewart', 'Ausar Thompson', 'Stanley Umude', 'James Wiseman'],
    'IND': ['Bruce Brown', 'Kendall Brown', 'Tyrese Haliburton', 'Buddy Hield', 'Isaiah Jackson', 'James Johnson', 'Bennedict Mathurin', 'T.J. McConnell', 'Andrew Nembhard', 'Aaron Nesmith', 'Jordan Nwora', 'Ben Sheppard', 'Jalen Smith', 'Obi Toppin', 'Oscar Tshiebwe', 'Myles Turner', 'Jarace Walker', 'Isaiah Wong'],
    'MIA': ['Bam Adebayo', 'Thomas Bryant', 'Jimmy Butler', 'Jamal Cain', 'R.J. Hampton', 'Tyler Herro', 'Haywood Highsmith', 'Jaime Jaquez Jr.', 'Nikola Jovic', 'Kevin Love', 'Kyle Lowry', 'Caleb Martin', 'Josh Richardson', 'Duncan Robinson', 'Orlando Robinson', 'Dru Smith', 'Cole Swider'],
    'MIL': ['Giannis Antetokounmpo', 'Thanasis Antetokounmpo', 'Malik Beasley', 'MarJon Beauchamp', 'Pat Connaughton', 'Jae Crowder', 'AJ Green', 'Andre Jackson Jr.', 'Damian Lillard', 'Chris Livingston', 'Brook Lopez', 'Robin Lopez', 'Khris Middleton', 'Cameron Payne', 'Bobby Portis', 'TyTy Washington Jr.'],
    'NYK': ['Precious Achiuwa', 'OG Anunoby', 'Ryan Arcidiacono', 'Charlie Brown', 'Jalen Brunson', 'Donte DiVincenzo', 'Malachi Flynn', 'Evan Fournier', 'Quentin Grimes', 'Josh Hart', 'Isaiah Hartenstein', 'Miles McBride', 'Julius Randle', 'Mitchell Robinson', 'Jericho Sims', 'Dmytro Skapintsev', 'Jacob Toppin', 'Duane Washington Jr.'],
    'ORL': ['Cole Anthony', 'Paolo Banchero', 'Goga Bitadze', 'Anthony Black', 'Wendell Carter Jr.', 'Markelle Fultz', 'Gary Harris', 'Kevon Harris', 'Caleb Houstan', 'Jett Howard', 'Joe Ingles', 'Jonathan Isaac', 'Chuma Okeke', 'Trevelin Queen', 'Admiral Schofield', 'Jalen Suggs', 'Franz Wagner', 'Moe Wagner'],
    'PHI': ['Mo Bamba', 'Nicolas Batum', 'Patrick Beverley', 'Ricky Council IV', 'Robert Covington', 'Joel Embiid', 'Tobias Harris', 'Danuel House Jr.', 'Furkan Korkmaz', 'Kenneth Lofton Jr.', 'Kenyon Martin Jr.', 'Tyrese Maxey', "De'Anthony Melton", 'Marcus Morris', 'Kelly Oubre Jr.', 'Paul Reed', 'Terquavion Smith', 'Jaden Springer'],
    'TOR': ['Scottie Barnes', 'RJ Barrett', 'Chris Boucher', 'Gradey Dick', 'Javon Freeman-Liberty', 'Christian Koloko', 'Jalen McDaniels', 'Markquis Nowell', 'Jakob Poeltl', 'Jontay Porter', 'Otto Porter Jr.', 'Immanuel Quickley', 'Dennis Schroder', 'Pascal Siakam', 'Garrett Temple', 'Gary Trent Jr.', 'Thaddeus Young'],
    'WAS': ['Deni Avdija', 'Patrick Baldwin Jr.', 'Jules Bernard', 'Jared Butler', 'Bilal Coulibaly', 'Johnny Davis', 'Hamidou Diallo', 'Daniel Gafford', 'Danilo Gallinari', 'Anthony Gill', 'Tyus Jones', 'Corey Kispert', 'Kyle Kuzma', 'Mike Muscala', 'Eugene Omoruyi', 'Jordan Poole', 'Landry Shamet', 'Delon Wright'],
    'DAL': ['Greg Brown', 'Seth Curry', 'Luka Doncic', 'Dante Exum', 'Josh Green', 'Tim Hardaway Jr.', 'Jaden Hardy', 'Richaun Holmes', 'Kyrie Irving', 'Derrick Jones Jr.', 'Maxi Kleber', 'AJ Lawson', 'Dereck Lively II', 'Markieff Morris', 'Dwight Powell', 'Olivier-Maxence Prosper', 'Brandon Williams', 'Grant Williams'],
    'DEN': ['Christian Braun', 'Kentavious Caldwell-Pope', 'Vlatko Cancar', 'Collin Gillespie', 'Aaron Gordon', 'Justin Holiday', 'Jay Huff', 'Reggie Jackson', 'Nikola Jokic', 'DeAndre Jordan', 'Braxton Key', 'Jamal Murray', 'Zeke Nnaji', 'Jalen Pickett', 'Michael Porter Jr.', 'Julian Strawther', 'Hunter Tyson', 'Peyton Watson'],
    'GSW': ['Stephen Curry', 'Usman Garuba', 'Draymond Green', 'Trayce Jackson-Davis', 'Cory Joseph', 'Jonathan Kuminga', 'Kevon Looney', 'Moses Moody', 'Chris Paul', 'Gary Payton II', 'Brandin Podziemski', 'Lester Quinones', 'Jerome Robinson', 'Gui Santos', 'Dario Saric', 'Klay Thompson', 'Andrew Wiggins'],
    'HOU': ['Dillon Brooks', 'Reggie Bullock', 'Tari Eason', 'Jalen Green', 'Jeff Green', 'Nate Hinton', 'Aaron Holiday', 'Jock Landale', 'Boban Marjanovic', 'Victor Oladipo', 'Jermaine Samuels', 'Alperen Sengun', 'Jabari Smith', "Jae'Sean Tate", 'Amen Thompson', 'Fred VanVleet', 'Cam Whitmore', 'Jeenathan Williams'],
    'LAC': ['Brandon Boston Jr.', 'Kobe Brown', 'Amir Coffey', 'Moussa Diabate', 'Paul George', 'James Harden', 'Bones Hyland', 'Kawhi Leonard', 'Terance Mann', 'Jordan Miller', 'Xavier Moon', 'Mason Plumlee', 'Norman Powell', 'Joshua Primo', 'Daniel Theis', 'P.J. Tucker', 'Russell Westbrook', 'Ivica Zubac'],
    'LAL': ['Colin Castleton', 'Max Christie', 'Anthony Davis', 'Rui Hachimura', 'Jaxson Hayes', 'Jalen Hood-Schifino', 'LeBron James', 'Maxwell Lewis', 'Skylar Mays', 'Taurean Prince', 'Austin Reaves', 'Cam Reddish', "D'Angelo Russell", 'Jarred Vanderbilt', 'Gabe Vincent', 'Dylan Windler', 'Christian Wood'],
    'MEM': ['Steven Adams', 'Santi Aldama', 'Desmond Bane', 'Brandon Clarke', 'Jacob Gilyard', 'Shaquille Harrison', 'Gregory Jackson', 'Jaren Jackson Jr.', 'Luke Kennard', 'John Konchar', 'Jake LaRavia', 'Ja Morant', 'Jaylen Nowell', 'David Roddy', 'Derrick Rose', 'Marcus Smart', 'Xavier Tillman', 'Ziaire Williams', 'Vince Williams Jr.'],
    'MIN': ['Nickeil Alexander-Walker', 'Kyle Anderson', 'Troy Brown Jr.', 'Jaylen Clark', 'Mike Conley', 'Anthony Edwards', 'Luka Garza', 'Rudy Gobert', 'Jaden McDaniels', 'Jordan McLaughlin', 'Leonard Miller', 'Shake Milton', 'Josh Minott', 'Wendell Moore Jr.', 'Daishen Nix', 'Naz Reid', 'Karl-Anthony Towns'],
    'NOP': ['Jose Alvarado', 'Dyson Daniels', 'Jordan Hawkins', 'Brandon Ingram', 'Herbert Jones', 'Kira Lewis Jr.', 'E.J. Liddell', 'Naji Marshall', 'CJ McCollum', 'Trey Murphy III', 'Larry Nance Jr.', 'Jeremiah Robinson-Earl', 'Matt Ryan', 'Dereon Seabron', 'Jonas Valanciunas', 'Zion Williamson', 'Cody Zeller'],
    'OKC': ['Davis Bertans', 'Ousmane Dieng', 'Luguentz Dort', 'Josh Giddey', 'Shai Gilgeous-Alexander', 'Chet Holmgren', 'Isaiah Joe', 'Keyontae Johnson', 'Tre Mann', 'Vasilije Micic', 'Aleksej Pokusevski', 'Olivier Sarr', 'Cason Wallace', 'Lindy Waters III', 'Aaron Wiggins', 'Jalen Williams', 'Jaylin Williams', 'Kenrich Williams'],
    'PHX': ['Grayson Allen', 'Udoka Azubuike', 'Keita Bates-Diop', 'Bradley Beal', 'Bol Bol', 'Devin Booker', 'Kevin Durant', 'Drew Eubanks', 'Jordan Goodwin', 'Eric Gordon', 'Saben Lee', 'Damion Lee', 'Nassir Little', 'Theo Maledon', 'Chimezie Metu', 'Jusuf Nurkic', 'Josh Okogie', 'Yuta Watanabe'],
    'POR': ['Deandre Ayton', 'Ibou Badji', 'Jamaree Bouyea', 'Malcolm Brogdon', 'Moses Brown', 'Toumani Camara', 'Jerami Grant', 'Scoot Henderson', 'Justin Minaya', 'Kris Murray', 'Duop Reath', 'Rayan Rupert', 'Shaedon Sharpe', 'Anfernee Simons', 'Matisse Thybulle', 'Jabari Walker', 'Robert Williams III'],
    'SAC': ['Harrison Barnes', 'Chris Duarte', 'Kessler Edwards', 'Keon Ellis', 'Jordan Ford', "De'Aaron Fox", 'Kevin Huerter', 'Colby Jones', 'Alex Len', 'Trey Lyles', 'JaVale McGee', 'Davion Mitchell', 'Malik Monk', 'Keegan Murray', 'Domantas Sabonis', 'Jalen Slawson', 'Juan Toscano-Anderson', 'Aleks Vezenkov'],
    'SAS': ['Dom Barlow', 'Charles Bassey', 'Malaki Branham', 'Julian Champagnie', 'Sidy Cissoko', 'Zach Collins', 'Mamadi Diakite', 'David Duke Jr.', "Devonte' Graham", 'Keldon Johnson', 'Tre Jones', 'Sandro Mamukelashvili', 'Doug McDermott', 'Cedi Osman', 'Jeremy Sochan', 'Devin Vassell', 'Victor Wembanyama', 'Blake Wesley'],
    'UTA': ['Ochai Agbaji', 'Jordan Clarkson', 'John Collins', 'Kris Dunn', 'Simone Fontecchio', 'Keyonte George', 'Taylor Hendricks', 'Talen Horton-Tucker', 'Johnny Juzang', 'Walker Kessler', 'Lauri Markkanen', 'Kelly Olynyk', 'Micah Potter', 'Jason Preston', 'Luka Samanic', 'Brice Sensabaugh', 'Collin Sexton', 'Omer Yurtseven']
}

df = pd.DataFrame(columns=['player_name', 'team_id'])

for key, value in players.items():
    for name in value:
        df.loc[len(df.index)] = [name, key]

#insert data to db
players_list = create_list_of_tuples(df)

query = 'INSERT INTO players (player_name, team_id) VALUES (%s,%s)'

mycursor.executemany(query, players_list)

db.commit()