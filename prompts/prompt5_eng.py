# LPG_sem에 대한 설명 prompt

prompt = """
Convert a given article into Neo4j format. 

You must not lie. Convert only true nodes and edges.
You need to find keywords of the given input article and convert them into Nodes.
Then you need to make Edges which represent the relationships between the Nodes you made.
Here is a brief description of the Neo4j format; you can find additional information on the internet. 

Nodes are represented by enclosing them in parentheses (). 
A Node's label is represented by "(:label)". Find the noun form keyword for a given article and set it as the label.
By prefixing label with some letters, create a variable that can refer to a Node. (Ex: "(a:label)" )
Properties of a Node can be represented by curly braces {{}}. (Ex: "(a:label {{property: 'property value'}})" )
List all the nodes first.

Edges are represented by enclosing them in []. 
Edges can specify labels, variables, and properties in the same way as Nodes. (Ex: "[var:label {{property: 'property value'}}]" )
A label of the edge should be easy and precise. 
Use the label '따라서' to represent two nodes in a causal relationship.
Put the tense or time information in the property section.
Edges are directional, so you should specify a start Node and an end Node. 
For example, if an edge is directed from node a to node b, it would be expressed as "(a)-[var:label {{property: 'property value'}}]->(b)".
List all the edges in the given format. 
"""
