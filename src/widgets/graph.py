import dash_cytoscape as cyto
from collections import defaultdict
from src.Dataset import Dataset

data = Dataset.data




my_stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "label": "data(label)",
                        "width": "mapData(degree, 1, 15, 20, 60)",
                        "height": "mapData(degree, 1, 15, 20, 60)",
                        "background-color": "#0074D9",
                        "text-valign": "center",
                        "text-halign": "center",
                        "text-outline-color": "#fff",
                        "text-outline-width": 2,
                        "color": "#222",   
                    },
                },
                {
                    "selector": "edge",
                    "style": {
                        "width": "mapData(weight, 1, 5, 1, 6)",
                        "line-color": "#bbb",
                        "curve-style": "bezier",
                    },
                },
            ]

def create_graph(selected_rows=None):
    return cyto.Cytoscape(
        id="graph",
        elements=build_elements(selected_rows),
        style={"width": "100%", "height": "100%"},
        className="stretchy-widget border-widget",
        layout={"name": "cose"},
        stylesheet=my_stylesheet,
            
    )
def build_elements(selected_rows):

    if not selected_rows: #if there are no selected rows, return an empty list
        return []
    
    bird_names = {row["class_name"] for row in selected_rows} #get only the unique bird classes

    edge_weights = defaultdict(int) #create a default dict 

    for bird in bird_names:
        bird_sep = bird.split() #tokenize the bird name into seperate words 
        for i in range (len(bird_sep)):
            for j in range(i+1, len(bird_sep)):
                word1, word2 = bird_sep[i], bird_sep[j] #create tuple of words
                word1, word2 = sorted([word1, word2]) #sort the words 
                edge_weights[(word1, word2)] += 1 #increment the weight of the edge connecting the two words (bigger edge weight means more bird names share those two words)


    node_degree = defaultdict(int) #create a default dict to store the degree of each node

    for word1, word2 in edge_weights: 
        node_degree[word1] += 1#increment the degree of word1 by the weight of the edge
        node_degree[word2] += 1 #increment the degree of word2 by the weight of the edge

    elements = [] 

    #node creation
    for word, degree in node_degree.items():
        elements.append({"data":{"id": word, "label" : word, "degree": degree}})
    
    #edge creation
    for (word1, word2), weight in edge_weights.items(): 
        elements.append({"data":{"id" : f"{word1}_{word2}", "source": word1, "target": word2, "weight": weight}})

    return elements
    

