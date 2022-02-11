from website.models import Customer

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import ( 
    ComplexField, 
    CorsOptions, 
    SearchIndex, 
    ScoringProfile, 
    SearchFieldDataType, 
    SimpleField, 
    SearchableField 
)

index_name = "alexweb0208"
# Get the service endpoint and API key from the environment
endpoint = "https://alexweb.search.windows.net"
key = "3CCEAA43AD7871914F54499BFC4EB6F1"

# Create a client
credential = AzureKeyCredential(key)


client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

def createIndex():
    return
    searchIndexClient = SearchIndexClient(endpoint=endpoint, index_name=index_name, credential=credential)

    fields = [
      SimpleField(name="Id", type=SearchFieldDataType.String, key=True, sortable=True),
      SearchableField(name="GivenName", type=SearchFieldDataType.String, sortable=True),
      SearchableField(name="Surname", type=SearchFieldDataType.String, sortable=True),
      SearchableField(name="City", type=SearchFieldDataType.String,sortable=True),
      SearchableField(name="Streetaddress", type=SearchFieldDataType.String,sortable=True),
      SearchableField(name="NationalId", type=SearchFieldDataType.String,sortable=True),
      SearchableField(name="Telephone", type=SearchFieldDataType.String,sortable=True),
      ]
    cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
    scoring_profiles = []

    index = SearchIndex(name=index_name, fields=fields, scoring_profiles=scoring_profiles, cors_options=cors_options)

    result = searchIndexClient.create_index(index)                      


def addDocuments():
    return
    docs = []
    for customer in Customer.query.all():
      d = {
        "Id" : str(customer.Id),
        "GivenName": customer.GivenName,
        "Surname": customer.Surname,
        "City": customer.City,
        "Streetaddress": customer.Streetaddress,
        "NationalId": customer.NationalId,
        "Telephone": customer.Telephone
      }
      docs.append(d)
    result = client.upload_documents(documents=docs)

def merge_document(Id:str, GivenName:str, Surname:str, City:str, Streetaddress:str, NationalId:str, Telephone:str):
    result = client.merge_documents(documents=[{"Id":Id, "GivenName":GivenName, "Surname":Surname, "City":City, "Streetaddress":Streetaddress, "NationalId":NationalId, "Telephone":Telephone}])
    print(f"AZURE Merge {GivenName} {Surname}, Updated document")

def upload_new_document(Id:str, GivenName:str, Surname:str, City:str, Streetaddress:str, NationalId:str, Telephone:str):
    DOCUMENT = {
        'Id': Id,
        'GivenName': GivenName,
        'Surname': Surname,
        'City': City,
        'Streetaddress': Streetaddress,
        'NationalId': NationalId,
        'Telephone': Telephone
    }
    result = client.upload_documents(documents=[DOCUMENT])
    print(f"AZURE Added {GivenName} {Surname}, Added new document")

def delete_document(Id:str):
    result = client.delete_documents(documents=[{"Id": Id}])
    print(f"AZURE Deleted Id:{Id}, deleted document")