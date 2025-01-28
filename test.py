import pickle
import rdflib
from rdflib.namespace import OWL, RDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open("ontologies/ontologies.pkl", "rb") as f:
    downloaded = pickle.load(f)

downloaded = {item[0][1]: item[1][1] for item in downloaded}

j,k = 0,0
for i in downloaded:
    k+=1
    try:
        g = rdflib.Graph()
        g.parse(downloaded[i], format="ttl")
        self_name = [s for s,p,o in g.triples((None, RDF.type, OWL.Ontology))]
        if len(self_name) != 1:
            self_name = [s for s,p,o in g.triples((None, RDF.type, "http://purl.org/vocommons/voaf#Vocabulary"))]
            print("FAILED (no self name):",i,downloaded[i])
        elif rdflib.URIRef(i.strip('#')) == self_name[0]:
            j+=1
            print("PASSED:",i)
        elif rdflib.URIRef(i) == rdflib.URIRef(str(self_name[0]).strip('#')):
            j+=1
            print("PASSED:",i)
        elif rdflib.URIRef(i) == self_name[0]:
            j+=1
            print("PASSED:",i)
        elif i.strip('#') == str(self_name[0]).strip('#'):
            j+=1
            print("PASSED:",i)
        elif cosine_similarity(TfidfVectorizer().fit_transform([i]), TfidfVectorizer().fit_transform([str(self_name[0])]))[0][0] > 0.99:
            j+=1
            print("PASSED (cosine):",i)
        else:
            print("FAILED (not match):",i, self_name[0])
    except:
        print("FAILED:",i)
        continue\

print(j,k)


