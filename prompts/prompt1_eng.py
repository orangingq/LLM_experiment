# RDF-star 형식에 대한 설명 prompt

# prompt = """
# Convert a given input sentence into the RDF-star format. 

# You should never lie. Extrapolate only true entities and relationships.
# Below are the short explanation about RDF-star format. You can find more on the internet. 

# There are entities and values.
# Entities are represented as ':Entity'.
# Values can be a string type, number, or a date, and are represented as '"Value"'.

# The basic unit of a representation is a triple.
# You can represent a relationship between entity as ' :Entity1 :Relationship :Entity2 . '.
# You can represent an attribute of the entity as ' :Entity :Attribute :Entity . ' or ' :Entity :Attribute "Value" . '.

# The main difference between RDF and RDF-star formats is the presence of 'Quoted Triples'. 
# You can refer to a triple as if it were a single entity by enclosing the triple between '<<' and '>>', like ' << :Entity :Attribute :Value >> :Relationship :Entity . '. 

# """
prompt = """
You are an excellent linguist. 
Your task is to extract all existing relations between entities in the sentences in the below triple format. 
The extracted format MUST consist of two entities and a single relation in the below triple format.

(entity:entity type - relation - entity:entity type)

Each entity should be a short and simple named entity or a noun phrase. Each relation should be a short and simple verb phrase. 
If cannot determine entity or relation or entity type, write 'none'. 
Only write entity type. Do not write relation type. 
If extracted format is not a triple, convert it to triple format. 
Do not explain your reason.

"""