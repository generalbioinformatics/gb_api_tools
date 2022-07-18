# Table of Contents

* [ceres\_tools](#ceres_tools)
  * [check\_graphql\_config](#ceres_tools.check_graphql_config)
  * [get\_graphql\_template](#ceres_tools.get_graphql_template)
  * [run\_graphql\_query](#ceres_tools.run_graphql_query)
  * [recursive\_key\_count](#ceres_tools.recursive_key_count)
  * [check\_graphql\_json](#ceres_tools.check_graphql_json)
  * [flatten\_json](#ceres_tools.flatten_json)
  * [extract\_sequences\_from\_result\_list](#ceres_tools.extract_sequences_from_result_list)

<a name="ceres_tools"></a>
# ceres\_tools

<a name="ceres_tools.check_graphql_config"></a>
#### check\_graphql\_config

```python
check_graphql_config(config_file)
```

check_graphql_config tests whether the URL and Java-Web-Token (JWT)
combination provided in the configuration file are able to generate
a succesful API response. If these credentials are invalid this script
will log an error message and cause the script to error.

**Example**:

  N.B. This example will not validate but demonstrates the template needed for
  a configuration file.
  config_file = "./examples/config.examples.json"
  check_graphql_config(config_file)
  

**Arguments**:

- `config_file` _str_ - The path to the configuration file

<a name="ceres_tools.get_graphql_template"></a>
#### get\_graphql\_template

```python
get_graphql_template(query)
```

get_graphql_template Reads a file and returns the contents
as a string.

**Example**:

  template_path = "./examples/example_query.graphql"
  template_query = get_graphql_template(template_path)
  

**Arguments**:

- `query` _str_ - Path to a file containing a graphql query
  

**Returns**:

- `str` - A string containing the template graphql query

<a name="ceres_tools.run_graphql_query"></a>
#### run\_graphql\_query

```python
run_graphql_query(query, variables, config_file)
```

run_graphql_query _summary_

**Example**:

  template_path = "./examples/example_query.graphql"
  template_query = get_graphql_template(template_path)
  config_file = "./examples/config.examples.json"
  check_graphql_config(config_file)
  variables = {
- `"input"` - ["C3TIE2"],
- `"limit"` - 100,
- `"offset"` - 0
  }
  response = run_graphql_query(
  template_query,
  variables,
  config_file
  )
  

**Arguments**:

- `query` _str_ - A string containing a graphql queries
- `variables` _dict_ - A dictionary containing any variables required by
  the graphql query
- `config_file` _str_ - The filepath of the config file
  

**Returns**:

- `requests.Response()` - A requests.Response() object.

<a name="ceres_tools.recursive_key_count"></a>
#### recursive\_key\_count

```python
recursive_key_count(data)
```

recursive_key_count Recursively yields the length of all
lists in a nested dictionary type structure. Used for checking
that the length of lists does not exceed the predefined limit.

**Arguments**:

- `data` _dict_ - A nested dictionary
  

**Yields**:

  (str, int): Yields a tuple with the field key and the number of values below
  that key level within

<a name="ceres_tools.check_graphql_json"></a>
#### check\_graphql\_json

```python
check_graphql_json(json_data, limit)
```

check_graphql_json Checks whether any fields within
a nested dictionary type structure exceed a specified limit.
If any fields do exceed the limit a warning message is logged.

**Example**:

  template_path = "./examples/example_query.graphql"
  template_query = get_graphql_template(template_path)
  config_file = "./examples/config.examples.json"
  check_graphql_config(config_file)
  variables = {
- `"input"` - ["C3TIE2"],
- `"limit"` - 100,
- `"offset"` - 0
  }
  response = run_graphql_query(
  template_query,
  variables,
  config_file
  )
  limit = 100
  json_data = json.loads(response.text)
  check_graphql_json(json_data, limit)
  

**Arguments**:

- `json_data` _dict_ - A nested dictionary containing the json-like results
  from a graphql query.
- `limit` _int_ - The expected maximum number of fields expected
  in a nested dictionary values field.

<a name="ceres_tools.flatten_json"></a>
#### flatten\_json

```python
flatten_json(data, parent_result_list=None, parent_key=None)
```

flatten_json returns a list of dictionaries. This function will recursively
search through a nested dictionary object flattening out the results
so that they can be converted into a pandas dataframe.

**Arguments**:

- `data` _dict_ - _description_
- `parent_result_list` _list, optional_ - Used recursively - do not use. Defaults to None.
- `parent_key` _str, optional_ - Used recursively - do not use. Defaults to None.
  

**Example**:

  template_path = "./examples/example_query.graphql"
  template_query = get_graphql_template(template_path)
  config_file = "./examples/config.examples.json"
  check_graphql_config(config_file)
  variables = {
- `"input"` - ["C3TIE2"],
- `"limit"` - 100,
- `"offset"` - 0
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
  

**Raises**:

- `Exception` - If the input type is not a dictionary
  

**Returns**:

- `list` - A list of dictionaries containing flattened data.

<a name="ceres_tools.extract_sequences_from_result_list"></a>
#### extract\_sequences\_from\_result\_list

```python
extract_sequences_from_result_list(result_list)
```

extract_sequences_from_result_list returns a list of SeqRecord objects.
Parses the results list produced by flatten_json() and searches for anything
that looks like a sequence based on its keys and values.

**Example**:

  template_path = "./examples/example_query.graphql"
  template_query = get_graphql_template(template_path)
  config_file = "./examples/config.examples.json"
  check_graphql_config(config_file)
  variables = {
- `"input"` - ["C3TIE2"],
- `"limit"` - 100,
- `"offset"` - 0
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
  sequence_list = extract_sequences_from_result_list(results_list)
  

**Arguments**:

- `result_list` _list_ - A list of dictionaries produced by flatten_json().
  

**Returns**:

- `list` - A list of Bio.SeqRecord objects.

