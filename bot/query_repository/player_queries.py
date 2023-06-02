
import json

class PlayerQueries:
    def get_player_data_all(self, player: str, session):
        query = "SELECT Nation, Pos, Squad FROM outfield_players WHERE Player = ?"
        result = session.fetch_query(query, (player,))
        return result
    
    def get_players_ga_dict(self, players: list, session):
        player_list = players # Replace with your list of players

        query_result = {}

        for player in player_list:
            query = f"SELECT `G+A` FROM outfield_players WHERE Player = ?"
            result = session.fetch_query(query, (player,))
            # Check if the result has a row
            if result:
                g_a_value = result[0][0]  
                if not g_a_value:
                    g_a_value=0 # Assuming 'G+A' is in the first column of the result
                
                # Add the player and the 'G+A' value to the dictionary
                query_result[player] = g_a_value

            else:
                query_result[player] = 0
        print(query_result)
        return query_result
    
    def get_players_npxg_dict(self, players: list, session):
        player_list = players # Replace with your list of players

        query_result = {}

        for player in player_list:
            query = f"SELECT `npxGPer90` FROM outfield_players WHERE Player = ?"
            result = session.fetch_query(query, (player,))
            # Check if the result has a row
            if result:
                g_a_value = result[0][0] # Assuming 'G+A' is in the first column of the result
                
                # Add the player and the 'G+A' value to the dictionary
                query_result[player] = g_a_value
            else:
                query_result[player] = 0
        print(query_result)
        return query_result


player_queries_repo = PlayerQueries()