# LPG -2에 대한 설명 prompt

prompt = """
Convert a given input sentence into Neo4j format. 

You must not lie. Only true nodes and edges should be converted.
Here is a brief description of the Neo4j format; you can find additional information on the internet. 

Nodes are represented by enclosing them in parentheses (). 
A Node's label is represented by "(number:label)".
Number is a unique id of each node.
Properties of a Node can be represented by curly braces {{}}. (Ex: "(1:label {{property: 'property value'}})" )
List all the nodes first.

Edges are represented by enclosing them in []. 
Edges can specify labels and properties in the same way as Nodes. (Ex: "[:label {{property: 'property value'}}]" )
A label of the edge should be easy and precise. It should be a basic form of the verb. 
Put the tense or time information in the property section.
Edges are directional, so you should specify a start Node and an end Node. 
For example, if an edge is directed from node id 1 to node id 2, it would be expressed as "(1)-[:label {{property: 'property value'}}]->(2)".
List all the edges in the given format. 
"""
