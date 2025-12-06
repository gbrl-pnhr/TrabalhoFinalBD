from typing import List
from pathlib import Path
import logging
from backend.modules.staff.chefs.models import ChefCreate, ChefResponse

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent / "queries"

class ChefRepository:
    """Repository for accessing 'cozinheiro' table data."""

    def __init__(self, db_connection):
        self.conn = db_connection

    def create_chef(self, chef: ChefCreate) -> ChefResponse:
        """Register a new chef."""
        sql_file = QUERY_PATH / "insert.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            logger.info(f"Creating chef: {chef.name}")
            try:
                cur.execute(
                    query,
                    {
                        "name": chef.name,
                        "cpf": chef.cpf,
                        "salary": chef.salary,
                        "specialty": chef.specialty,
                    },
                )
                row = cur.fetchone()
                self.conn.commit()

                if not row:
                    raise Exception("Failed to insert chef")

                return ChefResponse(
                    id=row["id_funcionario"],
                    name=row["nome"],
                    cpf=row["cpf"],
                    salary=row["salario"],
                    specialty=row["especialidade"],
                )
            except Exception as e:
                self.conn.rollback()
                logger.error(f"Error creating chef: {e}")
                raise e

    def get_all_chefs(self) -> List[ChefResponse]:
        """Fetch all chefs."""
        query = "SELECT id_funcionario, nome, cpf, salario, especialidade FROM cozinheiro ORDER BY nome;"

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return [
                ChefResponse(
                    id=row["id_funcionario"],
                    name=row["nome"],
                    cpf=row["cpf"],
                    salary=row["salario"],
                    specialty=row["especialidade"],
                )
                for row in rows
            ]