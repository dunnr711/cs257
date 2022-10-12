CREATE TABLE nocs (
    id INTEGER,
    abbreviation TEXT,
    country TEXT
);

CREATE TABLE olympic_games (
    id INTEGER,
    year INTEGER,
    season TEXT,
    city TEXT
);

CREATE TABLE athletes (
    id INTEGER,
    name TEXT,
    first_name TEXT,
    last_name TEXT,
    sex TEXT
);

CREATE TABLE event_categories (
    id INTEGER, 
    name TEXT
)
CREATE TABLE events (
    id INTEGER,
    event_category_id INTEGER,
    event_name TEXT
);

CREATE TABLE medals (
    id INTEGER,
    medal TEXT
);

CREATE TABLE linked_master (
    id INTEGER, 
    athlete_id INTEGER,
    nocs_id INTEGER,
    event_id INTEGER, 
    olympic_games INTEGER,
    medals_id INTEGER
);