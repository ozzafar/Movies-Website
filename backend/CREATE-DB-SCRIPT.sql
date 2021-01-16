CREATE TABLE Rated (
  rated_ID TINYINT UNSIGNED AUTO_INCREMENT,
  rated VARCHAR(5) NOT NULL UNIQUE,
  PRIMARY KEY (rated_ID)
);

CREATE TABLE Production_Countries (
  prod_country_ID SMALLINT UNSIGNED AUTO_INCREMENT,
  country VARCHAR(60) NOT NULL UNIQUE,
  PRIMARY KEY (prod_country_ID)
);

CREATE TABLE Genres (
  genre_ID TINYINT UNSIGNED AUTO_INCREMENT,
  genre VARCHAR(20) NOT NULL UNIQUE,
  PRIMARY KEY (genre_ID)
);

CREATE TABLE Movies (
  movie_ID MEDIUMINT UNSIGNED AUTO_INCREMENT,
  title VARCHAR(200) NOT NULL,
  rated_ID TINYINT UNSIGNED,
  released DATE,
  run_time TIME,
  plot TEXT,
  awards SMALLINT UNSIGNED,
  budget INT UNSIGNED,
  revenue INT UNSIGNED,
  poster_URL VARCHAR(200),
  trailer_URL VARCHAR(200),
  PRIMARY KEY (movie_ID),
  FOREIGN KEY (rated_ID) REFERENCES Rated(rated_ID),
  FULLTEXT KEY (title),
  FULLTEXT KEY (plot)
);

CREATE TABLE Person (
  person_ID MEDIUMINT UNSIGNED AUTO_INCREMENT,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  gender TINYINT UNSIGNED,
  picture_URL VARCHAR(200),
  PRIMARY KEY (person_ID),
  FULLTEXT KEY (first_name, last_name)
);

CREATE TABLE Movie_Score (
  movie_ID MEDIUMINT UNSIGNED,
  rotten_tomatoes TINYINT UNSIGNED,
  metacritic TINYINT UNSIGNED,
  imdb TINYINT UNSIGNED,
  imdbVotes INT UNSIGNED,
  PRIMARY KEY (movie_ID),
  FOREIGN KEY (movie_ID) REFERENCES Movies(movie_ID),
  CONSTRAINT CHK_Score CHECK (rotten_tomatoes<=100 AND metacritic<=100 AND imdb<=100)
);

CREATE TABLE Production_companies (
  prod_company_ID SMALLINT UNSIGNED AUTO_INCREMENT,
  company VARCHAR(100) NOT NULL UNIQUE,
  PRIMARY KEY (prod_company_ID)
);

CREATE TABLE Movie_Genres (
  movie_ID MEDIUMINT UNSIGNED ,
  genre_ID TINYINT UNSIGNED,
  PRIMARY KEY (movie_ID, genre_ID),
  FOREIGN KEY (movie_ID) REFERENCES Movies(movie_ID),
  FOREIGN KEY (genre_ID) REFERENCES Genres(genre_ID)
);

CREATE TABLE Movies_Crew (
  person_ID MEDIUMINT UNSIGNED,
  movie_ID MEDIUMINT UNSIGNED,
  role VARCHAR(100) NOT NULL,
  PRIMARY KEY (person_ID, movie_ID, role),
  FOREIGN KEY (person_ID) REFERENCES Person(person_ID),
  FOREIGN KEY (movie_ID) REFERENCES Movies(movie_ID)
);

CREATE TABLE Movie_Countries (
  movie_ID MEDIUMINT UNSIGNED,
  prod_country_ID SMALLINT UNSIGNED,
  PRIMARY KEY (movie_ID, prod_country_ID),
  FOREIGN KEY (movie_ID) REFERENCES Movies(movie_ID),
  FOREIGN KEY (prod_country_ID) REFERENCES Production_Countries(prod_country_ID)
);

CREATE TABLE Movie_Companies (
  movie_ID MEDIUMINT UNSIGNED,
  prod_company_ID SMALLINT UNSIGNED,
  PRIMARY KEY (movie_ID, prod_company_ID),
  FOREIGN KEY (movie_ID) REFERENCES Movies(movie_ID),
  FOREIGN KEY (prod_company_ID) REFERENCES Production_companies(prod_company_ID)
);

CREATE TABLE Movies_Actors (
  person_ID MEDIUMINT UNSIGNED,
  movie_ID MEDIUMINT UNSIGNED,
  figure VARCHAR(100) NOT NULL,
  PRIMARY KEY (person_ID, movie_ID),
  FOREIGN KEY (person_ID) REFERENCES Person(person_ID),
  FOREIGN KEY (movie_ID) REFERENCES Movies(movie_ID)
);

-- Indexes:

CREATE INDEX idx_released
ON Movies (released);

CREATE INDEX idx_run_time
ON Movies (run_time);

CREATE INDEX idx_budget
ON Movies (budget);

CREATE INDEX idx_awards
ON Movies (awards); 