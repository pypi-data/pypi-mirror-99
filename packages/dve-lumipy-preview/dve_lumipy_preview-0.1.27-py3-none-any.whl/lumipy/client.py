import io
import json

import pandas as pd
import requests
from time import sleep

from lumipy.client_auth.connect import connect
from lumipy.query.query import Query
from lumipy.common.string_utils import indent_str

from typing import Dict, Union, Optional, Callable


def _validate_response(response: requests.Response, endpoint_label):
    # Custom logic before .raise_for_status so we can unwrap the failure and report query errors.
    if not response.ok:
        # Inform the user
        print(
            f"Request to {endpoint_label} failed with status code "
            f"{response.status_code}, reason: '{response.reason}'."
        )
        # noinspection PyBroadException
        try:
            detail = json.loads(response.content)['detail']
            print(indent_str(f"Details:\n{indent_str(detail, n=4)}", n=4))
        except Exception:
            pass

        # Now throw
        response.raise_for_status()

    if response.content is None or len(response.content) == 0:
        raise ValueError(
            f"Request to {endpoint_label} returned status code: {response.status_code} but returned no content."
        )


def _validate_query(query):
    if not isinstance(query, Query) and not isinstance(query, str):
        raise ValueError(
            f"Query must be supplied as {type(str)} or {type(Query)} object. Was {type(query)}"
        )

    # If user supplies just a string, use the default parameters
    if isinstance(query, str):
        return Query(sql_str=query)
    else:
        return query


class Client:
    """WebApi Client for sending requests to Luminesce and getting results back as Pandas DataFrames.

    """

    def __init__(self, secrets_path: Optional[str] = None, retry_wait=0.5, max_retries=5):
        """__init__ method of the Luminesce Web API client class.

        Args:
            secrets_path (Optional[str]): path to secrets file containing authentication data. Optional - if not
            specified the client will get the auth data from env variables.
        """
        if secrets_path is not None:
            with open(secrets_path, 'r') as s:
                json_str = "".join(s.read().split())
                secrets = json.loads(json_str)
        else:
            secrets = {}

        self.token, self.base_url = connect(secrets)
        self.retry_wait = retry_wait
        self.max_retries = max_retries

    def headers(self) -> Dict[str, str]:
        """Build a dictionary of header values for sendng with Luminesce API calls. Includes the bearer token.

        Returns:
            Dict[str,str]: dictionary of headers for requests to Luminesce.
        """
        return {
            "accept": "text/plain",
            "Content-Type": "text/plain",
            "Authorization": f"Bearer {self.token}"
        }

    def _process_request(self, request: Callable, label):
        response = request()
        retry_count = 0
        while response.status_code == 429:
            if retry_count == self.max_retries:
                raise ValueError(f"Max number of retries ({retry_count}) exceeded.")
            # Wait and try again
            sleep(self.retry_wait)
            response = request()
            retry_count += 1

        _validate_response(response, label)
        return response

    def entitlement_resources_catalog(self) -> pd.DataFrame:
        """Get the entitlement resources catalog as a dataframe.

        Entitlement resources catalog gives information on services that have run recently that you are entitled to
        but may not necessarily be running now.

        Returns:
            DataFrame: dataframe containing entitlement resources information.
        """

        result = self._process_request(
            lambda: requests.get(
                f"{self.base_url}/EntitlementResources",
                headers=self.headers()
            ),
            label='entitlement resources catalog'
        )
        return pd.DataFrame(result.json())

    def table_field_catalog(self) -> pd.DataFrame:
        """Get the table field catalog as a DataFrame.

        The table field catalog contains a row describing each field on each provider you have access to.

        Returns:
            DataFrame: dataframe containing table field catalog information.
        """
        result = self._process_request(
            lambda: requests.get(
                f"{self.base_url}/Catalog",
                headers=self.headers()
            ),
            label='table field catalog'
        )
        return pd.DataFrame(result.json())

    def services(self) -> pd.DataFrame:
        """Get information of services that are currently running and that you have access to.

        Returns:
            DataFrame: dataframe containing running services information.
        """
        result = self._process_request(
            lambda: requests.get(
                f"{self.base_url}/Services",
                headers=self.headers()
            ),
            label='services catalog'
        )
        return pd.DataFrame(result.json())

    def query_and_fetch(self, query: Union[str, Query]):
        """Send a query to Luminesce and get it back as a pandas dataframe.

        Args:
            query (Union[str, Query]): query to be sent to Luminesce

        Returns:
            DataFrame: result of the query as a pandas dataframe.
        """
        lm_query = _validate_query(query)
        result = self._process_request(
            lambda: requests.put(
                f"{self.base_url}/Sql/csv",
                params=lm_query.params,
                data=lm_query.sql_str,
                headers=self.headers()
            ),
            label='query and fetch'
        )
        return pd.read_csv(io.StringIO(result.content.decode()))

    def start_query(self, query: Union[str, Query]):
        """Send an asynchronous query to Luminesce. Starts the query but does not wait and fetch the result.

        Args:
            query (Union[str, Query]): query to be sent to Luminesce

        Returns:
            str: string containing the execution ID

        """
        lm_query = _validate_query(query)
        result = self._process_request(
            lambda: requests.put(
                f"{self.base_url}/SqlBackground",
                params=lm_query.params,
                data=lm_query.sql_str,
                headers=self.headers()
            ),
            "start query"
        )
        return result.json()['executionId']

    def get_status(self, execution_id):
        """Get the status of a Luminesce query

        Args:
            execution_id (str): unique execution ID of the query.

        Returns:
            Dict[str, str]: dictionary containing information on the query status.
        """
        result = self._process_request(
            lambda: requests.get(
                f"{self.base_url}/SqlBackground/{execution_id}",
                headers=self.headers()
            ),
            label="get query status"
        )
        return result.json()

    def delete_query(self, execution_id):
        """Deletes a Luminesce query.

        Args:
            execution_id (str): unique execution ID of the query.

        Returns:
            Dict[str, str]: dictionary containing information on the deletion.

        """
        result = self._process_request(
            lambda: requests.delete(
                f"{self.base_url}/SqlBackground/{execution_id}",
                headers=self.headers()
            ),
            label="delete query"
        )
        return result.json()

    def get_result(self, execution_id, sort_by=None, filter_str=None, page_size=100000):
        """Gets the result of a completed luminesce query and returns it as a pandas dataframe.

        Args:
            execution_id (str): execution ID of the query.
            sort_by (str): string represting a sort to apply to the result before downloading it.
            filter_str (str): string representing a filter to apply to the result before downloading it.
            page_size (int, Optional): page size when getting the result via pagination. Default = 100000.

        Returns:
            DataFrame: result of the query as a pandas dataframe.

        """

        fetch_parameters = {'limit': page_size}
        if sort_by is not None:
            fetch_parameters['sortBy'] = sort_by
        if filter_str is not None:
            fetch_parameters['filter'] = filter_str

        page = 0
        chunks = []
        print('Fetching data... 📡')
        while True:
            result = self._process_request(
                lambda: requests.get(
                    f"{self.base_url}/SqlBackground/{execution_id}/{'csv'}",
                    headers=self.headers(),
                    params=fetch_parameters
                ),
                label="get result"
            )

            chunk = pd.read_csv(io.StringIO(result.content.decode()))

            fetch_parameters['page'] = page
            print(f"  Page {page:3d} downloaded ({chunk.shape[0]} rows).")
            page += 1

            chunks.append(chunk)
            if chunk.shape[0] < fetch_parameters['limit']:
                break
        print("Data fetch finished")
        return pd.concat(chunks)

    def start_history_query(self):
        """Start a query that get data on queries that have run historically

        Returns:
            str: execution ID of the history query
        """

        result = self._process_request(
            lambda: requests.get(
                f"{self.base_url}/History",
                headers=self.headers()
            ),
            label='query history'
        )
        return result.json()['executionId']

    def get_history_status(self, ex_id: str):
        """Get the status of a history query

        Args:
            ex_id (str): execution ID to check status for

        Returns:
            Dict[str,str]: dictionary containing the information from the status response json
        """
        result = self._process_request(
            lambda: requests.get(
                f"{self.base_url}/History/{ex_id}",
                headers=self.headers()
            ),
            label='get history query status'
        )
        return result.json()

    def get_history_result(self, ex_id):
        """Get result of history query

        Args:
            ex_id: execution ID to get the result for

        Returns:
            DataFrame: pandas dataframe containing the history query result.
        """
        result = self._process_request(
            lambda: requests.get(
                f"{self.base_url}/History/{ex_id}/json",
                headers=self.headers()
            ),
            label='get query history result'
        )
        return pd.DataFrame(result.json())

    def get_atlas(self):
        """Build an atlas object containing information on all the providers you have access to.

        Returns:
            Atlas: the constructed atlas.
        """
        from lumipy.navigation.field_definition import FieldDefinition
        from lumipy.navigation.provider_definition import ProviderDefinition
        from lumipy.navigation.atlas import Atlas

        table_field = self.table_field_catalog()
        table_field = table_field[~table_field.FieldName.isna()]
        entitlement_resources = self.entitlement_resources_catalog()

        # todo: infrastructure for direct providers
        providers_df = entitlement_resources[
            entitlement_resources.Type.apply(
                lambda x: x in ['DataProvider']
            )
        ]
        provider_descriptions = []
        for _, p_row in providers_df.iterrows():
            fields_df = table_field[table_field['TableName'] == p_row.Name]
            fields = [FieldDefinition.from_row(row) for _, row in fields_df.iterrows() if row.DataType is not None]

            if len([f for f in fields if f.field_type == 'Column']) == 0:
                continue

            provider = ProviderDefinition(
                table_name=p_row.Name,
                description=p_row.Description,
                provider_type=p_row.Type,
                category=p_row.Category,
                last_ping_at=p_row.LastPingAt,
                documentation=p_row.DocumentationLink,
                fields=fields,
                client=self
            )

            provider_descriptions.append(provider)

        return Atlas(
            provider_descriptions,
            atlas_type='All available providers'
        )
