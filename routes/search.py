import pandas as pd
import networkx as nx

df = pd.read_csv('data/modified_final.csv')
G = nx.read_gexf('gexf/bipartite_recipe.gexf')

def get_exact_recipes(vegetable_groups):
    result = []
    
    for vegetables in vegetable_groups:
        exact_recipes = []
        
        # Convert vegetable list to a set for easier comparison
        vegetable_set = set(vegetables)
        
        # Loop through each recipe node in the graph
        for node in G.nodes:
            # Skip nodes that are not recipes (assuming recipes are only connected to vegetables)
            node_neighbors = set(G.neighbors(node))
            
            # Check if the recipe's neighbors match the exact vegetable set
            if node_neighbors == vegetable_set:
                exact_recipes.append(node)
        
        result.append(exact_recipes)
    
    return result

