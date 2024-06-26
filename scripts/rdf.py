import rdflib

graph = rdflib.Graph()

graph.parse("http://www.w3.org/People/Berners-Lee/card")

for s, p, o in graph:
    assert (s, p, o) in graph

print(len(graph))
print(graph.serialize(format="rdf"))