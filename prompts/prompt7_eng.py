# LPG_rea에 대한 설명 prompt
# --(:AND)-->? / --(:OR)-->? / -[:따라서]-> / -[:는]- / -- (상관관계) / --> (포함관계)
prompt = """
Basically, convert a given article into Neo4j format. 

You must not lie. Convert only true nodes and edges.
You need to find keywords of the given input article and convert them into Nodes.
Then you need to make Edges which represent the relationships between the Nodes you made.
Here is a brief description of the Neo4j format; you can find additional information on the internet. 

Nodes are represented by enclosing them in parentheses (). 
A Node's label is represented by "(:label)". Find the noun form keyword for a given article and set it as the label.
By prefixing label with some letters, create a variable that can refer to a Node. (Ex: "(a:label)" )
Properties of a Node can be represented by curly braces {{}}. (Ex: "(a:label {{property: 'property value'}})" )
Try to avoid using properties and make another node instead. 
There are two special nodes '(:AND)' and '(:OR)' to bind multiple nodes and connect them to another node.
List all the nodes of keywords first.

Edges are represented by enclosing them in []. 
Edges can specify labels, variables, and properties in the same way as Nodes. (Ex: "[var:label]" )
A label of the edge should be one of '따라서' or '는'.
Use the label '따라서' to represent two nodes in a causal relationship as "(a)-[:따라서]->(b)".
Use the label '는' to represent that two nodes are equal. For example, "(a)-[:는]-(b)".
You don't need to put label.
"(a)--(b)" means that node a and node b are related.
"(a)-->(b)" means that node b is included in the node a.
Put the tense or time information in the property section.
List all the edges in the given format. 
"""


# Edges are directional, so you should specify a start Node and an end Node. 
# For example, if an edge is directed from node a to node b, it would be expressed as "(a)-[var:label {{property: 'property value'}}]->(b)".

