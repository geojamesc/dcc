import requests
from IPython.display import display, Markdown
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
import pprint


def get_data(awardNumber):

    _transport = RequestsHTTPTransport(
        url='https://api.datacite.org/graphql',
        use_json=True,
    )

    client = Client(
        transport=_transport,
        fetch_schema_from_transport=True,
    )

    # Generate the GraphQL query: find all outputs of FREYA grant award (https://cordis.europa.eu/project/id/777523) from funder (EU) to date
    #query_params = {
    #    "funderId" : "https://doi.org/10.13039/501100000780",
    #    "funderAwardQuery" : "fundingReferences.awardNumber:777523",
    #    "maxWorks" : 200
    #}

    query_params = {
        "funderId" : "https://doi.org/10.13039/501100000780",
        "funderAwardQuery" : "fundingReferences.awardNumber:{0}".format(awardNumber),
        "maxWorks" : 200
    }

    # TODO - modify the qgl to remove funder as per the nb since this does not seem to work...
    query = gql("""query getGrantOutputsForFunderAndAward($funderId: ID!, $funderAwardQuery: String!, $maxWorks: Int!)
    {
    funder(id: $funderId) {
      name
      works(query: $funderAwardQuery, first: $maxWorks) {
          totalCount
          nodes {
            id
            formattedCitation(style: "vancouver")
            titles {
              title
            }
            descriptions {
              description
            }
            types {
              resourceType
            }
            dates {
              date
              dateType
            }
            versionOfCount
            rights {
              rights
              rightsIdentifier
              rightsUri
            }
            creators {
              id
              name
            }
            fundingReferences {
              funderIdentifier
              funderName
              awardNumber
              awardTitle
            }
            citationCount
            viewCount
            downloadCount
          }
        }
      }
    }
    """)

    return client.execute(query, variable_values=json.dumps(query_params))


def main():
    # 777523 is what is in the provided notebook
    # 773701 and 767814 are id`s of other projects on https://cordis.europa.eu/ that returns a result but there are
    #  zero works in the resultset so the notebooks won`t produce anything meaningful
    # 821964 is a EO(!) example that returns a resultset and which has 26 works so will produce
    #  meaningfule results in the notebook
    award_numbers = [
        '777523',
        '821964'
    ]

    print('award_number, count_of_works, can_viz_in_notebook')
    for award_number in award_numbers:
        can_viz_in_notebook = True

        try:
            data = get_data(award_number)
            count_of_works = data['funder']['works']['totalCount']
            if count_of_works == 0:
                can_viz_in_notebook = False
            print(award_number, count_of_works, can_viz_in_notebook)
        except Exception as ex:
            print('PROBLEM - Exception Raised when getting data:')
            print(ex)







if __name__ == "__main__":
    main()
