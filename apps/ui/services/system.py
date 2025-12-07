import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
import logging
from typing import Dict, Any, Optional
from apps.ui.services.api_client import APIClient
from apps.ui.utils.exceptions import APIConnectionError

logger = logging.getLogger("frontend.services.system")


class SystemService:
    """
    Service layer for system-level operations (Health checks, Versioning, etc).
    Adheres to SRP by separating infrastructure checks from business logic.
    """

    def __init__(self):
        self.client = APIClient()

    def get_health_status(self) -> Optional[Dict[str, Any]]:
        """
        Queries the backend health check endpoint.

        Returns:
            Optional[Dict[str, Any]]: The health payload (e.g. {"status": "ok"})
            if successful, None if the connection fails.
        """
        try:
            return self.client.get("/health")
        except APIConnectionError:
            logger.warning("Backend health check failed: Connection Error")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during health check: {e}")
            return None