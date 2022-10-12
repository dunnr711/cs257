'''
    convert.py
    Ryan Dunn, 10 Oct 2022

    Expanded upon Jeff's code. 
'''
import csv

#Functioned designed to return the index of the desired header inputed as a list. 
def getHeaderIndex(lst, headers):
    headerIndexes = []
    i = 0 
    for item in lst: 
      for header in headers:   
          if item == header:
              headerIndexes.append(i)
              break
          else:
            splitItem = item.split(".")
            if len(splitItem) >= 2:
              splitHeader = header.split(".")
              if splitHeader[0] == splitItem[0] and splitHeader[-1] == splitItem[-1]:
                  headerIndexes.append(i)
                  break
      i += 1
    if len(headerIndexes) > 1:                                        
        return headerIndexes
    else: 
        return headerIndexes[0]
#Testing whether or not getHeaderIndex reads quotes. 
def test_getHeaderIndex():
    with open('athlete_events.csv') as original_data_file,\
            open('nocs.csv', 'w') as events_file:
        reader = csv.reader(original_data_file)
        writer = csv.writer(events_file)
        heading_row = next(reader)
        team_index = getHeaderIndex(heading_row, ["Team"])
        print(heading_row[team_index])


def main():
    #Create NOC table
    nocs = {}
    with open('athlete_events.csv') as original_data_file,\
            open('nocs.csv', 'w') as events_file:
        reader = csv.reader(original_data_file)
        writer = csv.writer(events_file)
        heading_row = next(reader) # eat up and ignore the heading row of the data file
        team_index = getHeaderIndex(heading_row, ["Team"])
        noc_index = getHeaderIndex(heading_row, ["NOC"])

        for row in reader:
            team_name = row[team_index]
            noc_abbreviation = row[noc_index]

            if noc_abbreviation not in nocs:
                noc_id = len(nocs) + 1
                nocs[noc_abbreviation] = noc_id
                writer.writerow([noc_id, noc_abbreviation, team_name])

    olympic_games = {}
    with open('athlete_events.csv') as original_data_file,\
            open('olympic_games.csv', 'w') as events_file:
        reader = csv.reader(original_data_file)
        writer = csv.writer(events_file)
        heading_row = next(reader) # eat up and ignore the heading row of the data file
        year_index = getHeaderIndex(heading_row, ["Year"])
        season_index = getHeaderIndex(heading_row, ["Season"])
        city_index = getHeaderIndex(heading_row, ["City"])
        for row in reader:
            year = row[year_index]
            season = row[season_index]
            city = row[city_index]
            games = year + season
            if games not in olympic_games:
                olympic_game_id = len(olympic_games) + 1
                olympic_games[games] = olympic_game_id
                writer.writerow([olympic_game_id, year, season, city])   

    #Athletes table
    athletes = {}
    with open('athlete_events.csv') as original_data_file,\
            open('athletes.csv', 'w') as athletes_file:
        reader = csv.reader(original_data_file)
        writer = csv.writer(athletes_file)
        heading_row = next(reader) # eat up and ignore the heading row of the data file
        for row in reader:
            athlete_id = row[0]
            athlete_name = row[1]
            first_name = athlete_name.split()[0]
            last_name = athlete_name.split()[-1]
            athlete_sex = row[2]
            if athlete_id not in athletes:
                athletes[athlete_id] = athlete_name
                writer.writerow([athlete_id, athlete_name, first_name, last_name, athlete_sex])

    #Event Category Table
    event_categories = {}
    with open('athlete_events.csv') as original_data_file,\
            open('event_categories.csv', 'w') as events_file:
        reader = csv.reader(original_data_file)
        writer = csv.writer(events_file)
        heading_row = next(reader)
        event_index = getHeaderIndex(heading_row, ["Sport"])        
        for row in reader:
            event_category= row[event_index]
            if event_category not in event_categories:
                event_id = len(event_categories) + 1
                event_categories[event_category] = event_id
                writer.writerow([event_id, event_category])
      
    events = {}
    with open('athlete_events.csv') as original_data_file,\
            open('events.csv', 'w') as events_file:
        reader = csv.reader(original_data_file)
        writer = csv.writer(events_file)
        heading_row = next(reader) # eat up and ignore the heading row of the data file

        sport_index = getHeaderIndex(heading_row, ["Sport"])
        event_index = getHeaderIndex(heading_row, ["Event"])

        for row in reader:
            sport = row[sport_index]
            event = row[event_index]
            
            sport_id = event_categories[sport]
            if event not in events:
                event_id = len(events) + 1
                events[event] = event_id
                writer.writerow([event_id, sport_id, event])
    medals = {}
    with open('athlete_events.csv') as original_data_file,\
            open('medals.csv', 'w') as event_results_file:
        reader = csv.reader(original_data_file)
        writer = csv.writer(event_results_file)
        heading_row = next(reader)
        medal_index = getHeaderIndex(heading_row, ["Medal"])
        for row in reader: 
            medal = row[medal_index]
            if medal not in medals: 
                medal_id = len(medals) + 1
                medals[medal] = medal_id
                writer.writerow([medal_id, medal])


    #(3) For each row in the original athlete_events.csv file, build a row
    #       for our new event_results.csv table
    with open('athlete_events.csv') as original_data_file,\
            open('linked_master.csv', 'w') as event_results_file:
        reader = csv.reader(original_data_file)
        writer = csv.writer(event_results_file)
        heading_row = next(reader) # eat up and ignore the heading row of the data file
        noc_index = getHeaderIndex(heading_row, ["NOC"])
        year_index = getHeaderIndex(heading_row, ["Year"])
        season_index = getHeaderIndex(heading_row, ["Season"])
        event_index = getHeaderIndex(heading_row, ["Event"])
        medal_index = getHeaderIndex(heading_row, ["Medal"])
        row_id = 1
        for row in reader:
            athlete_id = row[0]

            noc_abbr = row[noc_index]
            noc_id = nocs[noc_abbr]

            event_name = row[event_index]
            event_id = events[event_name]

            olympic_games_name = row[year_index] + row[season_index]
            olympic_id = olympic_games[olympic_games_name]

            medal = row[medal_index]
            medal_id = medals[medal] 


            medal = row[14]
            writer.writerow([row_id, athlete_id, noc_id, event_id, olympic_id, medal_id])
            row_id += 1
main()
