import sys
from pathlib import Path
import streamlit as st
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
import logging
from typing import Dict, Any, Optional
from apps.ui.services.api_client import APIClient
from apps.ui.utils.exceptions import APIConnectionError

logger = logging.getLogger("frontend.services.system")


class SystemService:
    """
    Service layer for system-level operations.
    """

    def __init__(self):
        self.client = APIClient()

    @st.cache_data(ttl=30, show_spinner=False)
    def get_health_status(_self) -> Optional[Dict[str, Any]]:
        """
        Queries the backend health check endpoint.
        Cached to prevent flickering on every rerun.
        """
        try:
            return _self.client.get("/health")
        except APIConnectionError:
            logger.warning("Backend health check failed: Connection Error")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during health check: {e}")
            return None