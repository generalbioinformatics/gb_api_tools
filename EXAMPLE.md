
# Example


## Create a `config.json`

Using a text editor create a `config.json` file containing your unique Java-Web-Token (JWT).

For example, modify the example file `./examples/example_query.graphql` with your own details:

```json
{
    "graphql":"http://ceres.app.intra/graphql",
    "token":"InsertYourApiTokenHere"
}
```

## Test your setup

To run this test you will need to create two local files. You can copy the files linked below and modify as appropriate:
- [config.examples.json](https://github.com/generalbioinformatics/gb_api_tools/blob/master/examples/config.examples.json)
- [example_query.graphql](https://github.com/generalbioinformatics/gb_api_tools/blob/master/examples/example_query.graphql)

```python

from gb_api_tools.ceres_tools import check_graphql_config, get_graphql_template, run_graphql_query, check_graphql_json, flatten_json
import pandas as pd
import json

config_file = "config.json"
# Tests whether the config is valid, if not will return an exception
check_graphql_config(config_file)
template_path = "example_query.graphql"
template_query = get_graphql_template(template_path)
variables = {
"input": ["C3TIE2"],
"limit": 100,
"offset": 0
}
response = run_graphql_query(
template_query,
variables,
config_file
)
limit = 100
json_data = json.loads(response.text)
check_graphql_json(json_data, limit)
results_list = flatten_json(json_data)
df = pd.DataFrame(results_list)
print(df)
```

This script should print the table below:

+----+---------------------------------------+---------------------------------------------+--------------------------+---------------------------+--------------------------+
|    | data.proteins.id                      | data.proteins.pref_name                     | data.proteins.alt_name   | data.proteins.gene_name   | data.proteins.synonyms   |
+====+=======================================+=============================================+==========================+===========================+==========================+
|  0 | http://identifiers.org/uniprot/C3TIE2 | Phospho-2-dehydro-3-deoxyheptonate aldolase |                          | aroG                      | aroG_2                   |
+----+---------------------------------------+---------------------------------------------+--------------------------+---------------------------+--------------------------+