# is the get_data() func from localhost:8888/notebooks/user-story-single-dmp-connections.ipynb

import json
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

_transport = RequestsHTTPTransport(
    url='https://api.datacite.org/graphql',
    use_json=True,
)

client = Client(
    transport=_transport,
    fetch_schema_from_transport=True,
)


def get_data(id):
    # Generate the GraphQL query to retrieve up to 100 outputs of University of Oxford, with at least 100 views each.
    # query_params = {
    #     "id": f.value,
    #     "maxOutputs": 100,
    #     "minViews": 100
    # }

    query_params = {
        "id": id,
        "maxOutputs": 100,
        "minViews": 100
    }

    query = gql("""query getOutputs($id: ID!)
    {
     dataManagementPlan(id: $id) {
        id
        name: titles(first:1) {
          title
        }
        datasets: citations(query:"types.resourceTypeGeneral:Dataset") {
            totalCount
            nodes {
              id: doi
              name: titles(first:1)  {
                title
              }
            }
          }
          publications: citations(query:"types.resourceTypeGeneral:Text") {
            totalCount
            nodes {
              id: doi
              name: titles(first:1)  {
                title
              }
            }
          }
        producer: contributors(contributorType: "Producer") {
          id
          name
          contributorType   
        }   
        fundingReferences {
          id: funderIdentifier
          name: funderName
          award: awardUri
        }
        creators {
          id
          name
          type
          affiliation{
            id
            name
          }
        } 
        pis: contributors(contributorType: "ProjectLeader") {
          id
          name
          contributorType
          affiliation{
            id
            name
          }
        }
        curators: contributors(contributorType: "DataCurator") {
          id
          name
          type
          affiliation{
            id
            name
          }
        }
      }
    }
    """)

    return client.execute(query, variable_values=json.dumps(query_params))["dataManagementPlan"]


def main():

    # works: 'https://doi.org/10.48321/D17G67'
    # does not work: 'https://doi.org/10.5281/zenodo.4034151'

    ids = [
        'https://doi.org/10.48321/D17G67',
        'https://doi.org/10.5281/zenodo.4034151',
        'https://doi.org/10.5281/zenodo.3667513',
        'https://doi.org/10.5281/zenodo.1475830',
        'https://doi.org/10.5281/zenodo.3364522'
    ]

    status = {}

    for id in ids:
        query_ok = True
        print('TRYING: ', id)
        try:
            data = get_data(id)
            print(data)
        except Exception as ex:
            query_ok = False
            print('PROBLEM')
            print(ex)

        status[id] = query_ok

    print('Status of queries by id:')
    for i in status:
        print(i, status[i])


if __name__ == "__main__":
    main()





