import logging
import requests
from typing import Any, Dict, Optional
from config import settings
from utils.exceptions import (
    APIConnectionError,
    ResourceNotFoundError,
    ValidationError,
    AppError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("frontend.api_client")


class APIClient:
    """
    A wrapper class for handling HTTP requests to the Backend API.
    """

    def __init__(self):
        """Initialize the API Client using settings."""
        self.base_url = settings.API_BASE_URL.rstrip("/")
        self.timeout = settings.API_TIMEOUT
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @staticmethod
    def _handle_response(response: requests.Response) -> Any:
        """
        Internal method to process the response.
        Raises specific typed exceptions based on status codes.
        """
        try:
            response.raise_for_status()
            if response.status_code == 204:
                return None
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            status = response.status_code
            try:
                error_detail = response.json().get("detail", str(http_err))
            except Exception:
                error_detail = str(http_err)

            logger.error(f"API Error ({status}): {error_detail}")

            if status == 404:
                raise ResourceNotFoundError(f"Resource not found: {error_detail}")
            elif status in (400, 422):
                raise ValidationError(f"Validation error: {error_detail}")
            else:
                raise AppError(f"Server error ({status}): {error_detail}")
        except Exception as err:
            logger.error(f"Unexpected Error processing response: {err}")
            raise AppError(f"An unexpected error occurred: {err}")

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
            response = requests.get(
                url, headers=self.headers, params=params, timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.ConnectionError as e:
            logger.critical(f"Connection failed: {url}")
            raise APIConnectionError("Backend unreachable", original_error=e)

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
        try:
            response = requests.post(
                url, headers=self.headers, json=data, timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.ConnectionError as e:
            raise APIConnectionError("Backend unreachable", original_error=e)

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
        try:
            response = requests.patch(
                url, headers=self.headers, json=data or {}, timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.ConnectionError as e:
            raise APIConnectionError("Backend unreachable", original_error=e)

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
        try:
            response = requests.delete(url, headers=self.headers, timeout=self.timeout)
            return self._handle_response(response)
        except requests.exceptions.ConnectionError as e:
            raise APIConnectionError("Backend unreachable", original_error=e)