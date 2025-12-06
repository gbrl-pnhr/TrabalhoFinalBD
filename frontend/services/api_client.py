import logging
import requests
from typing import Any, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("frontend.api_client")


class APIClient:
    """
    A wrapper class for handling HTTP requests to the Backend API.
    Handles base URL management, common headers, and error logging.
    """

    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        """
        Initialize the API Client.

        Args:
            base_url (str): The root URL of the API. Defaults to local dev server.
        """
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _handle_response(self, response: requests.Response) -> Any:
        """
        Internal method to process the response.

        Args:
            response (requests.Response): The raw HTTP response object.

        Returns:
            Any: Parsed JSON data if successful.

        Raises:
            Exception: If the status code indicates failure (4xx, 5xx).
        """
        try:
            response.raise_for_status()
            if response.status_code == 204:
                return None
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            error_msg = f"HTTP Error: {http_err}"
            try:
                detail = response.json().get("detail")
                if detail:
                    error_msg = f"API Error: {detail}"
            except Exception:
                pass

            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as err:
            logger.error(f"Unexpected Error: {err}")
            raise Exception(f"An unexpected error occurred: {err}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Perform a GET request.

        Args:
            endpoint (str): The API path (e.g., "/menu/dishes").
            params (dict, optional): Query parameters.

        Returns:
            Any: The JSON response.
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url}")
        try:
            response = requests.get(url, headers=self.headers, params=params)
            return self._handle_response(response)
        except requests.exceptions.ConnectionError:
            raise Exception("Failed to connect to the backend server. Is it running?")

    def post(self, endpoint: str, data: Dict[str, Any]) -> Any:
        """
        Perform a POST request.

        Args:
            endpoint (str): The API path.
            data (dict): The JSON payload.

        Returns:
            Any: The JSON response.
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url}")
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Perform a PATCH request.

        Args:
            endpoint (str): The API path.
            data (dict, optional): The JSON payload.

        Returns:
            Any: The JSON response.
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PATCH {url}")
        response = requests.patch(url, headers=self.headers, json=data or {})
        return self._handle_response(response)

    def delete(self, endpoint: str) -> Any:
        """
        Perform a DELETE request.

        Args:
            endpoint (str): The API path.

        Returns:
            Any: The JSON response (usually None for 204).
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response)