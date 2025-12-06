import requests
import logging
from typing import Optional, Dict, Any

# Configure logging for the frontend
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("frontend.api")


class APIClient:
    """
    Singleton client to handle HTTP requests to the FastAPI backend.
    """

    BASE_URL = "http://localhost:8000/api/v1"
    TIMEOUT = 5

    @staticmethod
    def _handle_response(response: requests.Response) -> Optional[Any]:
        """
        Helper to parse response or log errors.
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e} - Response: {response.text}")
            return None
        except requests.exceptions.ConnectionError:
            logger.error("Connection Error: Backend seems to be down.")
            return None
        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            return None

    @classmethod
    def get(cls, endpoint: str, params: Optional[Dict] = None) -> Optional[Any]:
        """
        Generic GET request.
        """
        url = f"{cls.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=cls.TIMEOUT)
            return cls._handle_response(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

    @classmethod
    def post(cls, endpoint: str, data: Dict) -> Optional[Any]:
        """
        Generic POST request.
        """
        url = f"{cls.BASE_URL}{endpoint}"
        try:
            response = requests.post(url, json=data, timeout=cls.TIMEOUT)
            return cls._handle_response(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None