# Imports
import networkx as nx # Required for node connections
import matplotlib.pyplot as plt # Required for image processing and saving

g = nx.Graph() # Initialise a graph

nodeList = {} # Initialise the node list - it contains info on node connections

while True: # Until the user says "stop"
    nodeString = input("New connection: ") # Ask user for input (Ex: "netConnection-Core")
    
    # Break out of the loop if the user is finished with connecting
    if nodeString == "end":
        break

    # Skip current iteration if input string is nothing
    if nodeString == "":
        print("Well, you can't connect nothing to nothing. Try again.")
        continue
    dashCount = 0 # Number of hyphens in the input string

    for symbol in nodeString: # Check to see how many hyphens in input, we can't have more or less than one
        if symbol == "-":
            dashCount += 1 
    
    # Tell the user why it can't be accepted and continue
    if dashCount < 0:
        print("Sorry, you haven't given me any connection. Please try again.")
        continue
    elif dashCount > 1:
        print("Sorry, that's too many connections. Please give me one connection at a time.")
        continue
    
    # Extract the node names from the input string
    nodes = nodeString.split("-", 1) # Splits up nodeString from index 0 to the hypen, then hyphen to
                                     # end. Max splits is 1, as specified. It returns an array

    node1 = nodes[0]
    node2 = nodes[1]

    # Check which node is already in the node list, append the other one to it.
    # If none exist, create a new entry.

    # At this point I got confused and gave up. It creates a back-connection, that's all.
    if node1 in nodeList.keys() and node2 not in nodeList.keys():
        nodeList[node1].append(node2)
        nodeList[node2] = [node1]
    elif node2 in nodeList.keys():
        nodeList[node2].append(node1)
        nodeList[node1] = [node2]
    elif node1 in nodeList.keys() and node2 in nodeList.keys():
        nodeList[node1].append(node2)
        nodeList[node2].append(node1)
    else:
        nodeList[node1] = [node2]
        nodeList[node2] = [node1]


# Create nodes based on node list
for node in nodeList.keys():
    g.add_node(node)

# Connect nodes in graph
for node in nodeList.keys():
    for connectedNode in nodeList[node]:
        g.add_edge(node, connectedNode)

nx.draw(g, with_labels = True)
plt.savefig("image.png")
