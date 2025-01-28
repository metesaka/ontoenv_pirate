import rdflib
import os
import pickle
from ontoenv_pirate import download_dependencies


# Ensure ontology storage directory exists
os.makedirs("ontologies", exist_ok=True)

# Load or initialize downloaded ontologies
if os.path.exists("ontologies/ontologies.pkl"):
    with open("ontologies/ontologies.pkl", "rb") as f:
        downloaded = pickle.load(f)
else:
    downloaded = set()

start = {"name": rdflib.URIRef("http://brick.mines.edu/anon/"), "location": "building.ttl"}

errors = download_dependencies(start, downloaded)

with open("ontologies/ontologies.pkl", "wb") as f:
    pickle.dump(downloaded, f)

with open("ontologies/errors.pkl", "wb") as f:
    pickle.dump(errors, f)

down_dict = {item[0][1]: item[1][1] for item in downloaded}
err_dict = {item[0][1]: item[1][1] for item in errors}
find_dep_err = {} # ontologies that we couldn't find the dependencies for (but we have ttl)
no_ttl_err = {} # ontologies that we couldn't find the ttl file for
for item in err_dict:
    if err_dict[item]:
        find_dep_err[item] = err_dict[item]
    else:
        no_ttl_err[item] = None


import json
# with open("find_dep_err.json", "w") as f:
#     json.dump(find_dep_err, f, indent=4)

with open("no_ttl_err.json", "w") as f:
    json.dump(no_ttl_err, f, indent=4)

with open("down_dict.json", "w") as f:
    json.dump(down_dict, f, indent=4)






