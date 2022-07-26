
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