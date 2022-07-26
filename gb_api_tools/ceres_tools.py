import json
import logging
import os
import sys
from datetime import datetime

import requests
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

DATE = datetime.now()
FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


def check_graphql_config(config_file):
    """check_graphql_config tests whether the URL and Java-Web-Token (JWT)
    combination provided in the configuration file are able to generate
    a succesful API response. If these credentials are invalid this script
    will log an error message and cause the script to error.

    Example:
    ```python
# N.B. This example will not validate but demonstrates the template needed for 
# a configuration file.
config_file = "./examples/config.examples.json"
check_graphql_config(config_file)
    ```

    Args:...
        config_file (str): The path to the configuration file
    """
    logger.info("Checking that Graphql configuration is valid")
    with open(config_file) as json_file:
        config = json.load(json_file)
    headers = {"authorization": "Bearer {}".format(config["token"])}
    authentication_url = config["graphql"].replace("/graphql", "/auth/me")
    try:
        response = requests.get(authentication_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        logger.error(
            "Unable to validate config. Receiving {} error".format(response.status_code)
        )
        logger.debug(error)
        sys.exit(1)
    return


def get_graphql_template(query):
    """get_graphql_template Reads a file and returns the contents
    as a string.

    Example:
    ```python
query = "./examples/example_query.graphql"
template_query = get_graphql_template(query)
    ```

    Args:
        query (str): Path to a file containing a graphql query 

    Returns:
        str: A string containing the template graphql query
    """
    file_path = os.path.dirname(os.path.abspath(query))
    file_name = os.path.basename(query)
    with open("{0}/{1}".format(file_path, file_name), "r") as f:
        query_template = f.read()
    return query_template


def run_graphql_query(query, variables, config_file):
    """run_graphql_query Sumbits the GraphQL query to the Ceres
    endpoint and returns a request.Response() object.

    Example:
    ```python
template_path = "./examples/example_query.graphql"
template_query = get_graphql_template(template_path)
config_file = "./examples/config.examples.json"
check_graphql_config(config_file)

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
    ```

    Args:
        query (str): A string containing a graphql queries
        variables (dict): A dictionary containing any variables required by
        the graphql query
        config_file (str): The filepath of the config file

    Returns:
        requests.Response(): A requests.Response() object.
    """
    with open(config_file) as json_file:
        config = json.load(json_file)
    headers = {"authorization": "Bearer {}".format(config["token"])}
    logger.debug(query)
    try:
        response = requests.post(
            config["graphql"],
            json={"query": query, "variables": variables},
            headers=headers,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        logger.error(
            "Unable to submit Graphql request. Receiving {} error".format(
                response.status_code
            )
        )
        logger.debug(error)
        logger.warning(query)
        logger.warning(variables)
        sys.exit(1)
    return response


def recursive_key_count(data):
    """recursive_key_count Recursively yields the length of all 
    lists in a nested dictionary type structure. Used for checking
    that the length of lists does not exceed the predefined limit.

    Args:
        data (dict): A nested dictionary

    Yields:
        (str, int): Yields a tuple with the field key and the number of values below
        that key level within
    """
    for key, value in data.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    yield from recursive_key_count(item)
            yield (key, len(value))
        elif isinstance(value, dict):
            yield from recursive_key_count(value)


def check_graphql_json(json_data, limit):
    """check_graphql_json Checks whether any fields within
    a nested dictionary type structure exceed a specified limit.
    If any fields do exceed the limit a warning message is logged.

    Example:
    ```python
template_path = "./examples/example_query.graphql"
template_query = get_graphql_template(template_path)
config_file = "./examples/config.examples.json"
check_graphql_config(config_file)
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
    ```

    Args:
        json_data (dict): A nested dictionary containing the json-like results
        from a graphql query.
        limit (int): The expected maximum number of fields expected
        in a nested dictionary values field.
    """
    counter = 0
    error_fields = set()
    for result in recursive_key_count(json_data):
        if int(result[1]) == int(limit):
            counter += 1
            error_fields.add(result[0])
    if counter > 1:
        error_fields_string = ", ".join(error_fields)
        warning_message = "{} fields including {} have the same number of \
results as the query limit of {}. This may result in missing data. You may \
want to consider increasing the upper limit to a higher value".format(
            counter, error_fields_string, limit
        )
        logger.warning(warning_message)
    else:
        logger.info("No fields in the returned JSON data exceed the upper limit")


def flatten_json(data, parent_result_list=None, parent_key=None):
    """flatten_json returns a list of dictionaries. This function will recursively
    search through a nested dictionary object flattening out the results
    so that they can be converted into a pandas dataframe.

    Args:
        data (dict): A nested dictionary returned from a Ceres.
        parent_result_list (list, optional): Used recursively - do not use. Defaults to None.
        parent_key (str, optional): Used recursively - do not use. Defaults to None.

    Example:
    ```python
template_path = "./examples/example_query.graphql"
template_query = get_graphql_template(template_path)
config_file = "./examples/config.examples.json"
check_graphql_config(config_file)
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
    ```

    Raises:
        Exception: If the input type is not a dictionary

    Returns:
        list: A list of dictionaries containing flattened data.
    """
    if not isinstance(data, dict):
        raise Exception(
            "Incorrect input data type {}. Expected dict.".format(type(data))
        )
    if not parent_result_list:
        parent_result_list = [{}]
    for key, value in data.items():
        if not isinstance(value, (dict, list)):
            new_result_list = []
            for result in parent_result_list:
                if parent_key:
                    new_key = "{}.{}".format(parent_key, key)
                    str_result = {new_key: value}
                else:
                    str_result = {key: value}
                output_result = {**result, **str_result}
                new_result_list.append(output_result)
            parent_result_list = new_result_list
    for key, value in data.items():
        if parent_key:
            new_key = "{}.{}".format(parent_key, key)
        else:
            new_key = key
        if isinstance(value, list):
            if not value:
                continue
            new_result_list = []
            for item in value:
                new_parent_result = flatten_json(item, parent_result_list, new_key)
                new_result_list.extend(new_parent_result)
            parent_result_list = new_result_list
        if isinstance(value, dict):
            new_result_list = flatten_json(value, parent_result_list, new_key)
            parent_result_list = new_result_list
    if not parent_result_list:
        logger.warning("No data in json response")
    return parent_result_list


def extract_sequences_from_result_list(result_list):
    """extract_sequences_from_result_list returns a list of SeqRecord objects.
    Parses the results list produced by flatten_json() and searches for anything
    that looks like a sequence based on its keys and values.

    Example:
    ```python
template_path = "./examples/example_query.graphql"
template_query = get_graphql_template(template_path)
config_file = "./examples/config.examples.json"
check_graphql_config(config_file)
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
sequence_list = extract_sequences_from_result_list(results_list)
    ```

    Args:
        result_list (list): A list of dictionaries produced by flatten_json().

    Returns:
        list: A list of Bio.SeqRecord objects. 
    """
    all_seq_dict = {}
    for result in result_list:
        # If a result in the reqult dictionary contains keys with the
        # expected keys for a protein sequence then create a new dictionary
        # composed of seq identifiers as keys and sequences as values.
        if ("sequence.sequence" in str(result.keys())) and (
            "sequence.header" in str(result.keys())
        ):
            seq_dict = {}
            for key, value in result.items():
                if "sequence.sequence" in key:
                    seq_value = value
                if "sequence.header" in key:
                    seq_key = value
            seq_dict = {seq_key: seq_value}
            all_seq_dict = {**all_seq_dict, **seq_dict}

    if all_seq_dict.keys():
        logger.info(
            "{} sequence/s identified in query result".format(len(all_seq_dict.keys()))
        )
    else:
        logger.warning("Unable to identify any sequences in result")
        return
    seq_output = []
    for key, value in all_seq_dict.items():
        record = SeqRecord(Seq(value), id=key, description="")
        seq_output.append(record)
    return seq_output

