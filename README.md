# PerMeA

## How to get data
From wikidata: https://www.wikidata.org/wiki/Wikidata:Data_access
> Use `?flavor=...` with a value from `full` (default), `simple` or `dump` to get more or less info

## A note on formats
To handle Linked Data the main format is RDF with its different implementations
- RDF/XML `.xml` the first and default one in specifications (used as synonim for RDF)
- Turtle `.ttl` is a more compact format
- JSON-LD `.json` json based
- N-Triples and Notation-3
These formats handle a single entity description

To handle multiple graphs/entities
RDF/XML
	

xml or pretty-xml
	

Was the default format, rdflib < 6.0.0

JSON-LD
	

json-ld
	

There are further options for compact syntax and other JSON-LD variants

N-Triples
	

ntriples, nt or nt11
	

nt11 is exactly like nt, only utf8 encoded

Notation-3
	

n3
	

N3 is a superset of Turtle that also caters for rules and a few other thingsTurtle `.ttl`
- 