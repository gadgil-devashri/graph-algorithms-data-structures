import numpy as np
import pandas as pd

class StronglyConnectedComponents:
  def __init__(self):
    self.noOfVertices = 0
    self.noOfEdges = 0
    self.graphType = ''
    self.startVertex = ''
    self.graph = ''
    self.vertices = []
    self.transposeGraph = ''
    self.dataDict = {}
    self.time = 0
    self.DFS_Output = []
    self.isInitialRun = ''
  
  def constructGraph(self,contents):
    # Function to construct main graph from input file
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
    
    
  
  def findStronglyConnectedComponents(self):
    # Function to call sub ordinate functions
    self.printInput()
    self.runDFS()
  

  def printInput(self):
    # Purpose - Print Input
    print("Graph Type : " +self.graphType)
    print("Total number of vertices: "+ str(self.noOfVertices))
    print("Total number of edges:"+ str(self.noOfEdges))
    print("Start Vertex: "+ self.startVertex)
    print("Set of vertices: "+str(self.vertices))
    # print("Initial state of cloud\n" +str(self.cloud))
    print("Adjacency matrix: \n"+ str(self.graph))
    print("Transpose Adjacency matrix: \n" +str(self.transposeGraph))
  
  def runDFS(self):
    #Purpose - DFS Entry Function
    print("Running Depth First Search")
    self.initialize(self.vertices)
    self.isInitialRun = True
    self.time = 0
    for vertex in self.vertices:
      if self.dataDict[vertex]['color'] == 'white':
        self.DFS_Visit(vertex)
    
    # Arraging vertices in decresing order of their finish times
    self.DFS_Output.reverse()
    print("DFS_Output : \n"+ str(self.DFS_Output))

    # DFS On transpose graph as per DFS_Output order
    print("Running Depth First Search on transpose")
    self.initialize(self.DFS_Output)
    self.isInitialRun = False
    self.time = 0
    for vertex in self.DFS_Output:
      if self.dataDict[vertex]['color'] == 'white':
        print("-----Component-----")
        self.DFS_Visit(vertex)

  def initialize(self, seq):
    # Function to initialize data structure for DFS
    for vertex in seq:
      self.dataDict[vertex] = {
        'color':'white',
        'parent':'NIL',
        'startTime': 0,
        'endTime': 0
      }

  
  def constructTranspose(self,contents):
    # Function to construct reverse graph
    print("Constructing transpose")
    matrix = np.zeros(shape=(self.noOfVertices,self.noOfVertices))
    df = pd.DataFrame(matrix, columns=self.vertices, index=self.vertices)
    for i in range(1,len(contents) -1 ):
      line = contents[i].split(" ")
      # Reverse the direction of orginal edges 
      df[line[0]][line[1]] = line[2]
      # Edge is both ways in an undirected graph
      if self.graphType == 'U':
        df[line[0]][line[1]] = line[2]
    self.transposeGraph = df
    self.findStronglyConnectedComponents()

  def DFS_Visit(self,vertex):
    # DFS Main function
    if self.isInitialRun:
      seq = self.vertices
      graph = self.graph
    else:
      seq = self.DFS_Output
      graph = self.transposeGraph

    self.time = self.time + 1
    self.dataDict[vertex]['startTime'] = self.time
    self.dataDict[vertex]['color'] = 'gray'

    # for loop
    for v in seq:
      if graph.at[vertex,v] != 0.0:
        if self.dataDict[v]['color'] == 'white':
          self.dataDict[v]['parent'] = vertex
          self.DFS_Visit(v)
  
    self.dataDict[vertex]['color'] = 'black'
    self.time = self.time + 1
    self.dataDict[vertex]['endTime'] = self.time

    if self.isInitialRun == True:
      self.DFS_Output.append(vertex)
    else:
      print(vertex)
 
# Drivers code 
def main():
  print("Lets find SCC for given directed graph")
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
  
  g = StronglyConnectedComponents()
  g.constructGraph(contents)
  g.constructTranspose(contents)

if __name__ == "__main__":
  main()