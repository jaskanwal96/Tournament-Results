#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2


def connect(db_name = "tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(db_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Cannot connect to database!")

def deleteMatches():
    """Remove all the match records from the database."""
    conn, cursor = connect()
    cursor.execute("TRUNCATE TABLE matches CASCADE")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, cursor = connect()
    cursor.execute("TRUNCATE TABLE players CASCADE")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, cursor = connect()
    # Count number of players in the players table
    cursor.execute("select count(*) from players")
    countP = cursor.fetchone()[0]
    conn.close()
    return countP


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn, cursor = connect()
    query = "INSERT INTO players(p_name) VALUES(%s)"
    cursor.execute(query, (name, ))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, cursor = connect()
    cursor.execute("select * from results")
    results = cursor.fetchall()
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, cursor = connect()
    query = "INSERT INTO matches(winner, loser) VALUES(%s, %s)"
    params = (winner, loser, )
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    results = playerStandings()
    # List of Pairs of players
    pairings_total = []
    # Counting length of results
    count_results = len(results)
    # Getting Pair of players at a time who will compete
    for i in range(0, count_results - 1, 2):
        pairing = (results[i][0], results[i][1],
                   results[i+1][0], results[i+1][1])
        pairings_total.append(pairing)
    conn.close()

    return pairings_total


