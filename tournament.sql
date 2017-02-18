-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- Drop Database if exists

DROP DATABASE IF EXISTS tournament;

-- Drop Tables if exist
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

--Drop view if exists
DROP VIEW IF EXISTS results CASCADE;

-- Create Database
CREATE DATABASE tournament;

-- Connect Database
\c tournament;

-- Create Players Table
CREATE TABLE players(
    p_id serial PRIMARY KEY,
    p_name text
);

-- Create Matches Table
CREATE TABLE matches(
    m_id serial PRIMARY KEY,
    winner INTEGER,
    loser INTEGER,
    FOREIGN KEY(winner) REFERENCES players(p_id),
    FOREIGN KEY(loser) REFERENCES players(p_id)
);


-- Create view results
CREATE VIEW results AS SELECT players.p_id, players.p_name,
coalesce((SELECT count(winner) from matches where players.p_id = matches.winner),0) as winnings,
coalesce((SELECT count(*) FROM matches where players.p_id = matches.winner OR players.p_id = matches.loser),0) as matches
FROM players LEFT JOIN matches ON playeRS.P_ID = MATCHES.WINNER
GROUP BY players.p_id ORDER BY winnings DESC;






