-- Table: categories
CREATE TABLE categories (
    id    INTEGER PRIMARY KEY,
    name  TEXT    NOT NULL,
    count INTEGER NOT NULL
                  DEFAULT ( 0 )
);


-- Table: shows
CREATE TABLE shows (
    id          INTEGER PRIMARY KEY,
    title       TEXT    NOT NULL,
    description TEXT,
    total       INTEGER,
    begin_date  DATE,
    end_date    DATE
);


-- Table: listings
CREATE TABLE listings (
    id       INTEGER PRIMARY KEY,
    category INTEGER NOT NULL
                     REFERENCES categories ( id ) ON DELETE CASCADE
                                                  ON UPDATE CASCADE,
    show     INTEGER NOT NULL
                     UNIQUE
                     REFERENCES shows ( id ) ON DELETE CASCADE
                                             ON UPDATE CASCADE,
    episodes INTEGER NOT NULL
                     DEFAULT ( 0 ),
    rating   INTEGER NOT NULL
                     CHECK ( rating BETWEEN 1 AND 10 )
                     DEFAULT ( 1 )
);

