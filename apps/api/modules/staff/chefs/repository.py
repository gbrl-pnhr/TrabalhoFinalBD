from typing import List
from pathlib import Path
import logging
from packages.common.src.models.chef_models import ChefCreate, ChefResponse

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent / "queries"

class ChefRepository:
    """Repository for accessing 'cozinheiro' table data."""

    def __init__(self, db_connection):
        self.conn = db_connection

    def create_chef(self, chef: ChefCreate) -> ChefResponse:
        """Register a new chef."""
        sql_file = QUERY_PATH / "create.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            logger.info(f"Creating chef: {chef.nome}")
            try:
                cur.execute(
                    query,
                    {
                        "name": chef.nome,
                        "cpf": chef.cpf,
                        "salary": chef.salario,
                        "specialty": chef.especialidade,
                    },
                )
                row = cur.fetchone()
                self.conn.commit()

                if not row:
                    raise Exception("Failed to insert chef")

                return ChefResponse(
                    id=row["id_funcionario"],
                    nome=row["nome"],
                    cpf=row["cpf"],
                    salario=row["salario"],
                    especialidade=row["especialidade"],
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
                    nome=row["nome"],
                    cpf=row["cpf"],
                    salario=row["salario"],
                    especialidade=row["especialidade"],
                )
                for row in rows
            ]