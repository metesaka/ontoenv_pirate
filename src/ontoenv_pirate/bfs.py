from collections import deque
import rdflib
from rdflib.namespace import OWL
from ontoenv_pirate import find_ttl_src
import requests
import uuid

def find_deps(graph_data:dict):
    name = graph_data['name']
    location = graph_data['location']
    g = rdflib.Graph()
    g.parse(location, format="ttl")
    
    deps = {ns[1] for ns in g.namespaces()}
    deps.update(str(o) for s, p, o in g.triples((None, OWL.imports, None)))
    deps = {str(dep) for dep in deps}
    return deps - {name}

def is_url_working(url:str):
    try:
        r = requests.get(url.strip("<>").strip("#"))
        r.raise_for_status()
        content_type = r.headers.get("Content-Type", "")
        if "text/turtle" in content_type or "application/x-turtle" in content_type:
            return True
        else:
            return False 
    except:
        return False

def is_url_xml(url:str):
    try:
        r = requests.get(url.strip("<>").strip("#"))
        r.raise_for_status()
        content_type = r.headers.get("Content-Type", "")
        if "application/xml" in content_type or "application/octet-stream" in content_type or "application/rdf+xml" in content_type:
            return True
        else:
            return False 
    except:
        return False

def can_parsed(dep:str, downloaded:set, dep_data:dict):
    try:
        r = requests.get(dep.strip("<>").strip("#"))
        r.raise_for_status()
        g = rdflib.Graph()
        g.parse(data=r.text, format="application/rdf+xml")
        file = f"ontologies/{uuid.uuid4()}.ttl"
        g.serialize(file, format="turtle")
        dep_data['location'] = file
        downloaded.add(tuple(dep_data.items()))
        del g
        return True
    except:
        return False
def download_dependencies(start:dict,downloaded:set):
    downloaded.add(tuple(start.items()))
    processed = set()
    queue = deque([start])
    errors = set()

    while queue: #bfs
        print("                                                                                              ",end="\r")
        print("Length of the queue: ",len(queue), "Length of the processed: ", len(processed) ,end="\r")
        current = queue.popleft()
        # print(current['name'])
        if tuple(current.items()) in processed:# already visited
            continue
        try:
            deps = find_deps(current) # get dependencies = owl:imports + namespaces
        except:
            # print("error finding deps")
            errors.add(tuple(current.items()))
            processed.add(tuple(current.items()))
            continue
        for dep in deps: 
            # print(dep)
            dep_data = {'name': dep, 'location': None}
            if dep_data["name"] in {item[0][1] for item in processed}:
                # print("already processed")
                continue
            if dep_data["name"] in {item[0][1] for item in downloaded}:# already downloaded to a local ttl file
                dep_data["location"] = next(item[1][1] for item in downloaded if item[0][1] == dep_data["name"])# get the location of the downloaded file
                # print("already downloaded", dep_data["location"])
            elif is_url_working(dep): # if the ontology is available online on its own link
                r = requests.get(dep.strip("<>").strip("#"))
                r.raise_for_status()
                file = f"ontologies/{uuid.uuid4()}.ttl"
                with open(file, "wb") as f: # save the file with a random name
                    f.write(r.content) 
                dep_data['location'] = file 
                downloaded.add(tuple(dep_data.items()))
            elif is_url_xml(dep) and can_parsed(dep, downloaded, dep_data): # if the ontology is available online on its own link with 
                pass
            else:
                res = find_ttl_src(dep) # ask chatgpt to find the most up-to-date version of the ontology in turtle format
                # print(res)
                if not res or res == "THE ONTOLOGY IS NOT AVAILABLE": # if the ontology is not available mark as visited
                    processed.add(tuple(dep_data.items()))
                    errors.add(tuple(dep_data.items()))
                else: # chatgpt found a link to the ontology ttl file
                    try:
                        # print("trying downloading")
                        r = requests.get(res)
                        r.raise_for_status()
                        if "text/turtle" not in r.headers.get("Content-Type", "") and "application/x-turtle" not in r.headers.get("Content-Type", ""):
                            raise Exception("Not a turtle file")
                        file = f"ontologies/{uuid.uuid4()}.ttl"
                        with open(file, "wb") as f: # save the file with a random name
                            f.write(r.content) 
                        dep_data['location'] = file 
                        downloaded.add(tuple(dep_data.items()))
                    except: # if the link is not available mark as visited (we cannot access the ontology)
                        # print("error downloading")
                        processed.add(tuple(dep_data.items()))
                        errors.add(tuple(dep_data.items()))
            
            if dep_data['location']:
                queue.append(dep_data)
        processed.add(tuple(current.items()))
    return errors