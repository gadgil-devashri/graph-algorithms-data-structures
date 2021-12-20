import numpy as np
import pandas as pd

class ShortestPathDijkstras :
  def __init__(self):
    self.noOfVertices = 0
    self.noOfEdges = 0
    self.graphType = ''
    self.startVertex = ''
    self.graph = ''
    self.vertices = []
    self.dataDictParent = {}
    self.cloud = {}
    self.priorityQueue = []
    self.shortestDistanceList =[]
  
  def constructGraph(self,contents):
    #Purpose - This method is used to construct adjacency matrix based on grah input
    vertices = []
    line = contents[0].split(" ")
    self.noOfVertices = line[0]
    self.noOfEdges = line[1]
    self.graphType = line[2]
    line = contents[-1].split(" ")
    self.startVertex = line[0]
    # Creating adjacency matrix
    for i in range (1,len(contents) -1):
      line = contents[i].split(" ")
      if line[0] not in vertices:
        vertices.append(line[0])
      if line[1] not in vertices:
        vertices.append(line[1])
    self.noOfVertices = len(vertices)
    matrix = np.zeros(shape=(self.noOfVertices,self.noOfVertices))
    df = pd.DataFrame(matrix, columns=vertices, index=vertices)
    for i in range(1,len(contents) -1 ):
      line = contents[i].split(" ")
      # first column then row
      df[line[1]][line[0]] = line[2]
      # Edge is both ways in an undirected graph
      if self.graphType == 'U':
        df[line[0]][line[1]] = line[2]
    self.graph = df
    self.vertices = vertices
    # Intialize cloud with all False values
    for vertex in self.vertices:
      self.cloud[vertex] = False
    self.findShortestPath()
  
  def findShortestPath(self):
    # Dijikstras Algorithm start
    # Initialize
    self.printInput() 
    self.initialize()
    # Remove min from queue 
    while(len(self.priorityQueue)!= 0):
      tup = self.priorityQueue.pop(0)
      self.shortestDistanceList.append(tup)
      src = tup[0]
      srcDist = tup[1]
      # Add source vertex to cloud
      self.cloud[src] = True
      for vertex in self.vertices:
        if self.cloud[vertex] == False:
          if self.graph.at[src,vertex] != 0.0:
            self.relax(src,vertex,self.graph[vertex][src],srcDist)
    
    if all(value == True for value in self.cloud.values()):
      self.printResults()
    
  
  def initialize(self):
    # Purpose - Intialize data structure 
    dataDictParent = {}
    for vertex in self.vertices:
      dataDictParent[vertex] = 'NIL'
      if vertex == self.startVertex :
        self.priorityQueue.append((vertex, 0))
      else :
        self.priorityQueue.append((vertex, 100000))
    self.dataDictParent = dataDictParent
    self.priorityQueue.sort(key=lambda x:x[1])

  def relax(self,src,dest,edgeLenSrcDist,srcDist):
    #Purpose - Relax adjecent vertices 
    #print("Relaxing edges for adjecent vertex " +dest)
    self.priorityQueue = dict(self.priorityQueue)
    if self.priorityQueue[dest] > srcDist + edgeLenSrcDist :
      self.priorityQueue[dest] = srcDist + edgeLenSrcDist
      self.dataDictParent[dest] = src
    
    self.priorityQueue = list(self.priorityQueue.items())
    self.priorityQueue.sort(key=lambda x:x[1])

    

  def printResults(self):
    # Purpose : Dedicated method to print results on console
    hierarchy = []
    print("--------------------------------")
    print("Shortest Distance calculated!")
    for tup in self.shortestDistanceList:
      hierarchy = []
      if tup[0] != self.startVertex:
        tempParent = self.dataDictParent[tup[0]]
        if tempParent != self.startVertex:
          # new logic
          while tempParent != self.startVertex:
            hierarchy.insert(0,tempParent)
            if tup[0] not in hierarchy:
              hierarchy.append(tup[0])
            tempParent = self.dataDictParent[tempParent]
          hierarchy.insert(0,tempParent)
          hierarchy.append(tup[1])
          print(*hierarchy, sep = "--> ") 
        else:
          print(tempParent,tup[0],tup[1],sep = "--> ")
  
  def printInput(self):
    # Purpose - Print Input
    print("Graph Type : " +self.graphType)
    print("Total number of vertices: "+ str(self.noOfVertices))
    print("Total number of edges:"+ str(self.noOfEdges))
    print("Start Vertex: "+ self.startVertex)
    print("Set of vertices: "+str(self.vertices))
    # print("Initial state of cloud\n" +str(self.cloud))
    print("Adjacency matrix: \n"+ str(self.graph))
    

# Driver code 
def main():
  print("Welcome to Dijkstra's shortest path algorithm")
  print("Choose graph input file")
  graphNum = input("1,\n2,\n3,\n4 \nInput :")
  print(graphNum)
  if graphNum == "1":
    filePath = 'input_one.txt'
  elif graphNum == "2":
    filePath = 'input_two.txt'
  elif graphNum == "3":
    filePath = 'input_three.txt'
  elif graphNum == "4":
    filePath = 'input_four.txt'
  else:
    print("Wrong input. Terminating program")

  print("Reading graph one from file : " +str(graphNum))
  with open(filePath) as f:
    contents = f.read().splitlines()
    f.close()
  g = ShortestPathDijkstras()
  g.constructGraph(contents)

if __name__ == "__main__":
  main()