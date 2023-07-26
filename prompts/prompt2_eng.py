# Neo4j 형식에 대한 설명 prompt

prompt = """
Convert a given input sentence into Neo4j format. 
You must not lie. Only true nodes and edges should be converted.
Here is a brief description of the Neo4j format; you can find additional information on the internet. 

Nodes are represented by enclosing them in parentheses (). 
A Node's label is represented by "(:label)".
By prefixing label with some letters, you can create a variable that can refer to a Node. (Ex: "(a:label)" )
Properties of a Node can be represented by curly braces {{}}. (Ex: "(a:label {{property: 'property value'}})" )

Edges are represented by enclosing them in []. 
Edges can specify labels, variables, and properties in the same way as Nodes. (Ex: "[var:label {{property: 'property value'}}]" )
Edges are directional, and you can specify a start Node and an end Node. 
For example, if an edge is directed from node a to node b, it would be expressed as "(a)-[var:label {{property: 'property value'}}]->(b)".

"""
