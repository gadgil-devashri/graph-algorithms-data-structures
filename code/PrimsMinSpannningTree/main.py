import numpy as np
import pandas as pd

class PrimsMST:
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
    self.mstDistanceList =[]
  
  def constructGraph(self,contents):
    # Purpose - Creating adj matrix from input file
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
    for vertex in self.vertices:
      self.cloud[vertex] = False
    self.primsAlgo()
  
  def primsAlgo(self):
    # Purpose - Prims Algorithm to find MST
    self.printInput()
    self.initialize()
    while(len(self.priorityQueue)!= 0):
      tup = self.priorityQueue.pop(0)
      self.mstDistanceList.append(tup)
      src = tup[0]
      srcDist = tup[1]
      # Add  vertex to cloud
      self.cloud[src] = True
      for vertex in self.vertices:
        if self.cloud[vertex] == False:
          if self.graph.at[src,vertex] != 0.0:
            # Relax vertex only if its adjecent to source and not in cloud
            self.relax(src,vertex,self.graph[vertex][src],srcDist)
    
    if all(value == True for value in self.cloud.values()):
      self.printResults()
  
  def printInput(self):
    # Purpose - Print Input
    print("Graph Type : " +self.graphType)
    print("Total number of vertices: "+ str(self.noOfVertices))
    print("Total number of edges:"+ str(self.noOfEdges))
    print("Start Vertex: "+ self.startVertex)
    print("Set of vertices: "+str(self.vertices))
    # print("Initial state of cloud\n" +str(self.cloud))
    print("Adjacency matrix: \n"+ str(self.graph))
  
  def initialize(self):
    # Initialize all vertices with NIL parent and very large key value
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
    # Purpose - Recalculate distances for all aj vertices to src to find shortest path
    #print("Relaxing edges for adjecent vertex " +dest)
    self.priorityQueue = dict(self.priorityQueue)
    if edgeLenSrcDist < self.priorityQueue[dest]:
      self.priorityQueue[dest] = edgeLenSrcDist
      self.dataDictParent[dest] = src
    
    self.priorityQueue = list(self.priorityQueue.items())
    self.priorityQueue.sort(key=lambda x:x[1])
  
  def printResults(self):
    # Purpose - Print Output
    print("--------------------------------")
    print("Minimum spanning tree calculated!")
    print("Parent ---> Child :: Key")
    self.mstDistanceList = dict(self.mstDistanceList)
    for (k,v) in self.dataDictParent.items():
      print (v +"--->" + k + " :: " +str(self.mstDistanceList[k]))
    print("")
    totalDist = 0
    for dist in self.mstDistanceList:
      totalDist = totalDist + self.mstDistanceList[dist]
    print("Total cost of minimum spanning tree = " +str(totalDist))
    


def main():
  print("Welcome to Prim's Minimum Spanning Tree algorithm")
  print("Choose graph input file")
  graphNum = input("1,\n2,\n3,\n4 \nInput :")
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
  g = PrimsMST()
  g.constructGraph(contents)

if __name__ == "__main__":
  main()