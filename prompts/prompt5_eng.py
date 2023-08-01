# Infoedge 형식에 대한 설명 prompt

prompt = """
Given an input sentence, extrapolate as many relationships as possible from the prompt and update the state. 

You should never lie. Extrapolate only true relationships.
A relationship has three types of entity. Nodes, Edges, and Infoedge. 

1. Node
Every node has a distinct id and label. 
The format of the node is (id-label).
The label of a node is a subject of the sentence.

2. Edge
Every edge has a set of 'from' node ids, and a set of 'to' node ids, its own id, and label.
The format of the edge is (id-label): node id->node id.
Every edge is directed from a set of nodes and to another set of nodes. 
The label of an edge is a basic type verb of the sentence. Label should be precise and short. 

3. Infoedge
Infoedge adds additional information of the sentence to the edge such as time, location, duration, or from whom. 
Every infoedge has a single 'base' edge id, a set of 'info' node ids, its own id, and label. 
The format of the infoedge is (id-label): edge id->node id.
The label of an infoedge should be one of '부터 (시간)', '까지 (시간)', '에서 (장소)', '에 (시간)', '에게', and '에게서'. 

"""
