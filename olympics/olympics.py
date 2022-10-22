#Ryan Dunn, Oct 22nd
import sys
import psycopg2
import config

def get_connection():
    ''' Returns a database connection object with which you can create cursors,
        issue SQL queries, etc. This function is extremely aggressive about
        failed connections--it just prints an error message and kills the whole
        program. Sometimes that's the right choice, but it depends on your
        error-handling needs. Copied from Jeff's psycopg2-sample.py'''
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

def read_request():
    "Returns a letter from the data that the user requests that is used to prompt the correct action in main"
    command_line = sys.argv 
    if len(command_line) <= 3 or len(command_line) > 1: 
        if command_line[1] == "-a" or command_line[1] == "--athletes":
            if len(command_line) == 3:
                return "-a"
            else:
                return "-A"
        elif command_line[1] == "-n" or command_line[1] == "--noc":
            return "-n"
        elif command_line[1] == "-y" or command_line[1] == "--year":
            return "-y"
        elif command_line[1] == "-h" or command_line[1] == "--help":
            return "-h"
        else:
            return "incorrect command"
    else: 
        if len(command_line) > 3: 
            return "-e"
        else: 
            return "-E"

def get_athletes(search_text):
    ''' Returns a list of the full names of all athletes in the database
       from the specified noc '''
    athletes = []
    try:
        query = '''SELECT athletes.first_name, athletes.last_name, nocs.abbreviation
                    FROM athletes, nocs, linked_master
                    WHERE athletes.id = linked_master.athlete_id
                    AND nocs.id = linked_master.nocs_id
                    AND nocs.abbreviation ILIKE CONCAT('%%', %s, '%%');'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_text,))
        for row in cursor:
            given_name = row[0]
            surname = row[1]
            athletes.append(f'{given_name} {surname}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes

def get_all_athletes():
    ''' Returns a list of the full names of all athletes in the database
       from the specified noc '''
    athletes = []
    try:
        query = '''SELECT athletes.first_name, athletes.last_name
                    FROM athletes
                    '''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            given_name = row[0]
            surname = row[1]
            athletes.append(f'{given_name} {surname}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes

def get_athletes_from_year(year):
    year = str(year)
    ''' Returns a list of the full names of all athletes who competed in the given year '''
    athletes = []
    try:
        query = '''SELECT athletes.first_name, athletes.last_name, olympic_games.year, olympic_games.season
                    FROM athletes, olympic_games, linked_master
                    WHERE olympic_games.id = linked_master.olympic_games
                    AND athletes.id = linked_master.athlete_id
                    AND olympic_games.year  = %s
                    ORDER BY athletes.last_name;'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (year,))
        for row in cursor:
            given_name = row[0]
            surname = row[1]
            season = row[3]
            athletes.append(f'{given_name} {surname} : {season}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes    

def get_noc():
    noc = []
    try:
        query = '''SELECT COUNT (medals.medal), nocs.country
                    FROM nocs, medals, linked_master
                    WHERE medals.id = linked_master.medals_id
                    AND nocs.id = linked_master.nocs_id
                    AND medals.medal = 'Gold'
                    GROUP BY nocs.country
                    ORDER BY COUNT(medals.id) DESC;'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)

        for row in cursor:
            count = row[0]
            country = row[1]
            noc.append(f'{country} | {count}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return noc
    
def get_help():
    with open('usage.txt', 'r') as f:
        lines = f.readlines()
    return lines
def main():
    request = read_request()
    if request == "-a":
        athletes = get_athletes(sys.argv[-1])
        print(f'Athletes from {sys.argv[-1]}:')
        for athlete in athletes: 
            print(athlete)
    elif request == "-A":
        athletes = get_all_athletes()
        for athlete in athletes: 
            print(athlete)
    elif request == "-n":
        noc_list = get_noc()
        for item in noc_list:
            print(item)
    elif request == "-y":
        athletes = get_athletes_from_year(sys.argv[-1])
        print("Athletes from " + sys.argv[-1])
        for athlete in athletes: 
            print(athlete)
    elif request == "-e":
        print("You have too many command arguments. Type \"python3 olympics.py --help\" for valid commands.")
    elif request == "-E":
        print("You have too few command arguments. Type \"python3 olympics.py --help\" for valid commands.")
    elif request == "-h":
        for line in get_help():
            print(line)
    elif request == "incorrect command":
        print("Did you enter the correct command? Need help? Type \"python3 olympics.py --help\" for valid commands. ")
    else:
        print("This should never happen.")
        


main()
