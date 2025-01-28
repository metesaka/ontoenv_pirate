# ontoenv_pirate
A pirate ontology dependency manager
1. Starts from a specific graph
2. Finds all dependencies of a given graph by:
```
    deps = {ns[1] for ns in g.namespaces()}
    deps.update(str(o) for s, p, o in g.triples((None, OWL.imports, None)))
```
2. Finds dependencies of dependencies (and their dependencies ...) with the same idea using bfs
3. Along the way, tries to download the ttl file of the ontology using the URI (also downloads xml)
4. For the URIs that doesn't work, uses openai api to search web to hopefully find it (to see prompt [click here](./src/ontoenv_pirate/find_ttl_source.py)) (TODO: can also improved to consider )
5. Uses about 30k token per run (~$0.07)
6. Doesn't consider local ttl files yet

## How to run:
- generate an api key from openai
- create a file named ```.env```
- paste this to that file and save:  ```OPENAI_API_KEY=<your api key here>```
- run: 
``` 
uv run onto_deps.py
```

requires uv -> [DOWNLOAD UV](https://github.com/astral-sh/uv)

### AFTER RUNNING:
- all ontologies will be saved to ```ontologies``` folder
- downloaded ontologies with path to their files are in [this json](./down_dict.json)
- ontologies failed to be downloaded are in [this json](./no_ttl_err.json)

#### Accuracy:
- run ```test.py``` to check if downloaded ontology is really what you want
- if you run the test you'll noticed some failed tests those are because the ontology doesn't explicitly say ... a owl:Ontology, but I manually checked all and they seemed ok
- 81 ontologies will be downloaded successfully
- 57 dependencies will be failed to downloaded

