# RDF-star 형식에 대한 설명 prompt

prompt = """
Convert a given input sentence into the RDF-star format. 
You should never lie. Extrapolate only true entities and relationships.
Below are the short explanation about RDF-star format. You can find more on the internet. 

There are entities and values.
Entities are represented as ':Entity'.
Values can be a string type, number, or a date, and are represented as '"Value"'.

The basic unit of a representation is a triple.
You can represent a relationship between entity as ' :Entity1 :Relationship :Entity2 . '.
You can represent an attribute of the entity as ' :Entity :Attribute :Entity . ' or ' :Entity :Attribute "Value" . '.

The main difference between RDF and RDF-star formats is the presence of 'Quoted Triples'. 
You can refer to a triple as if it were a single entity by enclosing the triple between '<<' and '>>', like ' << :Entity :Attribute :Value >> :Relationship :Entity . '. 

"""
