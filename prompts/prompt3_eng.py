# LPG -2에 대한 설명 prompt

# prompt = """
# Convert an input article into Neo4j format based on the chain of thought.
# You must not lie. Only true nodes and edges should be converted.

# Chain of thought:

# [Step 1]: Make [5~10 Nodes] that are representing the [subjects] and [objects] of the article, using below description of the [Nodes].
# [Step 2]: Make [Edges] that are representing the [relationship between each two Nodes], using below description of the [Edges].



# Here is a brief description of the Nodes and Edges of Neo4j format; you can find additional information on the internet. 

# [Nodes]: 
# - Format: "(var:label {{property: 'property value'}})"
#     - var: variable that refers to a Node. Represented by a letter such as 'a'.
#     - label: Label is a simple noun that represents the type of the Node. 
#     - property: Property represents the properties of the Node. There can be two or more properties.
#     - property value: Each property has a property name and property value. 
    
# [Edges]:
# - Format: "(a)-[:label {{property: 'property value'}}]->(b)"
#     - Edges are directional so you should specify a start Node and an end Node. In the above example format, start Node is (a) and end Node is (b).
#     - label: Label is a basic form of the verb that represents the relationship between the two connected Nodes. A label should be easy and precise. 
#     - property: Property represents the properties of the Edge. Put the tense or time information in this property section. There can be two or more properties.
# """



prompt = """
You are a smart assistant.
Convert an input article into Neo4j format based on the chain of thought.
You must not lie. Only true nodes and edges should be converted.

Chain of thought:

[Step 1]: [Provide Nodes] that are representing the [subjects] and [objects] of the paraphrased article, using below description of the Neo4j format.
[Step 2]: [Provide Edges] that are representing the [relationship] between each two Nodes, using below description of the Neo4j format.


Here is a brief description of the Neo4j format; you can find additional information on the internet. 

Nodes are represented by enclosing them in parentheses (). 
A Node's label is represented by "(:label)".
By prefixing label with some letters, create a variable that can refer to a Node. (Ex: "(a:label)" )
Properties of a Node can be represented by curly braces {{}}. (Ex: "(a:label {{property: 'property value'}})" )
List all the nodes first.

Edges are represented by enclosing them in []. 
Edges can specify labels, variables, and properties in the same way as Nodes. (Ex: "[var:label {{property: 'property value'}}]" )
A label of the edge should be [easy] and [precise]. It should be a [basic form of the verb]. 
Put the tense or time information in the property section.
Edges are directional, so you should specify a start Node and an end Node. 
For example, if an edge is directed from node a to node b, it would be expressed as "(a)-[var:label {{property: 'property value'}}]->(b)".
List all the edges in the given format. 
"""
