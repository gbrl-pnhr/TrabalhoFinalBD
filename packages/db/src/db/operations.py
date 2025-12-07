import random
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime, timedelta
from pathlib import Path
from faker import Faker
from yoyo import read_migrations, get_backend
from .config import logger, settings

SEEDS_DIR = Path(__file__).resolve().parents[2] / "seeds"
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=30)

MENU_ITEMS = {
    1: ("Bruschetta Clássica", 25.00, "Entrada"),
    2: ("Carpaccio de Carne", 32.00, "Entrada"),
    3: ("Dadinhos de Tapioca", 22.00, "Entrada"),
    4: ("Salada Caprese", 28.00, "Entrada"),
    5: ("Filé Mignon ao Poivre", 85.00, "Prato Principal"),
    6: ("Risoto de Camarão", 78.00, "Prato Principal"),
    7: ("Salmão Grelhado", 72.00, "Prato Principal"),
    8: ("Espaguete à Carbonara", 55.00, "Prato Principal"),
    9: ("Nhoque ao Sugo", 48.00, "Prato Principal"),
    10: ("Bife de Chorizo", 89.00, "Prato Principal"),
    11: ("Petit Gâteau", 24.00, "Sobremesa"),
    12: ("Tiramisu", 26.00, "Sobremesa"),
    13: ("Pudim de Leite", 18.00, "Sobremesa"),
    14: ("Mousse de Chocolate", 20.00, "Sobremesa"),
    15: ("Água com Gás", 6.00, "Bebida"),
    16: ("Refrigerante Lata", 8.00, "Bebida"),
    17: ("Suco Natural", 12.00, "Bebida"),
    18: ("Cerveja Artesanal", 18.00, "Bebida"),
    19: ("Vinho Tinto Taça", 25.00, "Bebida"),
    20: ("Caipirinha", 22.00, "Bebida"),
}

STAFF_COUNT_WAITERS = 5
STAFF_COUNT_CHEFS = 5
CUSTOMER_COUNT = 50
TABLE_COUNT = 10

fake = Faker("pt_BR")
Faker.seed(42)
random.seed(42)


def escape_sql_string(val: str) -> str:
    return str(val).replace("'", "''")


def generate_001_infrastructure(output_dir: Path):
    filepath = output_dir / "001_seed_infrastructure.sql"
    logger.debug(f"Generating {filepath.name}...")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("-- 001_seed_infrastructure.sql\n")
        f.write("-- Tables (Mesa), Staff (Garcom/Cozinheiro), and Menu (Prato)\n")
        f.write("-- Using RESTART IDENTITY to reset IDs to 1\n\n")

        f.write(
            "TRUNCATE TABLE mesa, garcom, cozinheiro, prato RESTART IDENTITY CASCADE;\n\n"
        )

        # MESA
        f.write("INSERT INTO mesa (numero, capacidade, localizacao) VALUES\n")
        rows = []
        for i in range(1, TABLE_COUNT + 1):
            cap = random.choice([2, 4, 6, 8])
            loc = random.choice(["Interna", "Externa", "Varanda"])
            rows.append(f"({i}, {cap}, '{loc}')")
        f.write(",\n".join(rows) + ";\n\n")

        # GARCOM
        f.write("INSERT INTO garcom (nome, cpf, salario, turno, comissao) VALUES\n")
        w_rows = []
        for i in range(1, STAFF_COUNT_WAITERS + 1):
            name = escape_sql_string(fake.name())
            cpf = fake.cpf().replace(".", "").replace("-", "")
            salario = random.choice([1500.00, 1800.00, 2000.00])
            turno = random.choice(["Manhã", "Noite"])
            comissao = 5.00
            w_rows.append(f"('{name}', '{cpf}', {salario}, '{turno}', {comissao})")
        f.write(",\n".join(w_rows) + ";\n\n")
        f.write("INSERT INTO cozinheiro (nome, cpf, salario, especialidade) VALUES\n")
        c_rows = []
        for i in range(1, STAFF_COUNT_CHEFS + 1):
            name = escape_sql_string(fake.name())
            cpf = fake.cpf().replace(".", "").replace("-", "")
            salario = random.choice([2500.00, 3200.00, 4000.00])
            spec = random.choice(["Massas", "Grelhados", "Sobremesas"])
            c_rows.append(f"('{name}', '{cpf}', {salario}, '{spec}')")
        f.write(",\n".join(c_rows) + ";\n\n")
        f.write("INSERT INTO prato (nome, preco, categoria) VALUES\n")
        d_rows = []
        for d_id, (name, price, cat) in sorted(MENU_ITEMS.items()):
            d_rows.append(f"('{escape_sql_string(name)}', {price}, '{cat}')")
        f.write(",\n".join(d_rows) + ";\n\n")


def generate_002_customers(output_dir: Path):
    filepath = output_dir / "002_seed_customers.sql"
    logger.debug(f"Generating {filepath.name}...")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("-- 002_seed_customers.sql\n\n")
        f.write("TRUNCATE TABLE cliente RESTART IDENTITY CASCADE;\n\n")

        f.write("INSERT INTO cliente (nome, telefone, email) VALUES\n")
        rows = []
        for i in range(1, CUSTOMER_COUNT + 1):
            name = escape_sql_string(fake.name())
            email = f"cliente{i}@exemplo.com"
            phone = fake.phone_number()[:15]
            rows.append(f"('{name}', '{phone}', '{email}')")
        f.write(",\n".join(rows) + ";\n")


def generate_003_orders(output_dir: Path, orders_list: list):
    filepath = output_dir / "003_seed_orders.sql"
    logger.debug(f"Generating {filepath.name}...")
    current_order_id = 1000
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("-- 003_seed_orders.sql\n")
        f.write("-- Pedido and Item_Pedido\n\n")
        f.write("TRUNCATE TABLE pedido, item_pedido RESTART IDENTITY CASCADE;\n")
        f.write("ALTER TABLE pedido ALTER COLUMN id_pedido RESTART WITH 1000;\n\n")
        curr_date = START_DATE
        while curr_date <= END_DATE:
            is_weekend = curr_date.weekday() >= 4
            daily_orders = (
                random.randint(20, 30) if is_weekend else random.randint(10, 18)
            )
            day_orders_sql = []
            day_items_sql = []
            for _ in range(daily_orders):
                o_id = current_order_id
                current_order_id += 1
                cust_id = random.randint(1, CUSTOMER_COUNT)
                table_id = random.randint(1, TABLE_COUNT)
                waiter_id = random.randint(1, STAFF_COUNT_WAITERS)
                if random.random() < 0.4:
                    h = random.randint(11, 14)
                else:
                    h = random.randint(18, 22)
                m = random.randint(0, 59)
                dt_str = curr_date.replace(hour=h, minute=m).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                status = "FECHADO"
                if curr_date.date() == END_DATE.date() and random.random() < 0.3:
                    status = "ABERTO"
                num_items = random.randint(1, 5)
                selected_dishes = random.choices(list(MENU_ITEMS.keys()), k=num_items)
                total_amount = 0.0
                people_count = random.randint(1, 4)
                if status == "FECHADO":
                    orders_list.append(
                        {
                            "id": o_id,
                            "customer_id": cust_id,
                            "items": list(set(selected_dishes)),
                        }
                    )
                for d_id in selected_dishes:
                    name, price, _ = MENU_ITEMS[d_id]
                    qty = 1
                    total_amount += price
                    obs = "NULL"
                    if random.random() < 0.1:
                        obs = "'Sem cebola'" if "Salada" in name else "'Bem passado'"
                    day_items_sql.append(f"({o_id}, {d_id}, {qty}, {obs})")
                day_orders_sql.append(
                    f"('{dt_str}', {total_amount:.2f}, {cust_id}, {table_id}, {waiter_id}, '{status}', {people_count})"
                )

            if day_orders_sql:
                f.write(f"-- Pedidos for {curr_date.date()}\n")
                f.write(
                    "INSERT INTO pedido (data_pedido, valor_total, id_cliente, id_mesa, id_funcionario, status, quantidade_pessoas) VALUES\n"
                )
                f.write(",\n".join(day_orders_sql) + ";\n")

                f.write(
                    "INSERT INTO item_pedido (id_pedido, id_prato, quantidade, observacao) VALUES\n"
                )
                f.write(",\n".join(day_items_sql) + ";\n\n")

            curr_date += timedelta(days=1)


def generate_004_reviews(output_dir: Path, orders_list: list):
    filepath = output_dir / "004_seed_reviews.sql"
    logger.debug(f"Generating {filepath.name}...")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("-- 004_seed_reviews.sql\n\n")
        f.write("TRUNCATE TABLE avaliacao RESTART IDENTITY CASCADE;\n\n")
        f.write(
            "INSERT INTO avaliacao (id_cliente, id_prato, id_pedido, nota, comentario) VALUES\n"
        )
        review_rows = []
        if not orders_list:
            return

        orders_to_review = random.sample(orders_list, k=int(len(orders_list) * 0.7))

        for order in orders_to_review:
            if not order["items"]:
                continue
            dish_id = random.choice(order["items"])
            rating = random.choices([1, 2, 3, 4, 5], weights=[5, 5, 15, 40, 35])[0]

            comments_map = {
                5: [
                    "Incrível!",
                    "Adorei, muito bom.",
                    "Sabor inigualável.",
                    "Perfeito, recomendo.",
                ],
                4: ["Muito bom.", "Gostei, mas demorou um pouco.", "Saboroso."],
                3: ["Razoável.", "Nada de especial.", "Ok."],
                2: [
                    "Frio e sem sal.",
                    "Não gostei do atendimento.",
                    "Caro para o que oferece.",
                ],
                1: ["Terrível.", "Nunca mais volto.", "Pior experiência."],
            }
            comment = random.choice(comments_map[rating])
            review_rows.append(
                f"({order['customer_id']}, {dish_id}, {order['id']}, {rating}, '{comment}')"
            )
        if review_rows:
            f.write(",\n".join(review_rows) + ";\n")


def generate_seeds() -> None:
    output_dir = SEEDS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    orders_list = []
    logger.info(f"Generating seeds in: {output_dir}")

    generate_001_infrastructure(output_dir)
    generate_002_customers(output_dir)
    generate_003_orders(output_dir, orders_list)
    generate_004_reviews(output_dir, orders_list)
    generate_005_reset_sequences(output_dir)

    logger.info("Seed files generated successfully.")


def create_database_if_not_exists() -> None:
    target_db_name = settings.DB_NAME
    try:
        conn = psycopg2.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database="postgres",
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (target_db_name,)
        )
        exists = cursor.fetchone()
        if not exists:
            logger.info(f"Database '{target_db_name}' does not exist. Creating it...")
            cursor.execute(f"CREATE DATABASE {target_db_name}")
            logger.info(f"Database '{target_db_name}' created successfully.")
        else:
            logger.debug(f"Database '{target_db_name}' already exists.")
        cursor.close()
        conn.close()
    except Exception as e:
        logger.warning(f"Could not create database (check permissions): {e}")


def apply_migrations() -> None:
    create_database_if_not_exists()
    logger.info("Starting database migration process...")
    db_url = settings.database_url
    try:
        backend = get_backend(db_url)
        migrations_dir = Path(__file__).resolve().parents[2] / "migrations"
        if not migrations_dir.exists():
            logger.error(f"Migrations directory not found at: {migrations_dir}")
            return
        migrations = read_migrations(str(migrations_dir))
        to_apply = backend.to_apply(migrations)
        if not to_apply:
            logger.info("Database is already up to date.")
            return
        logger.info(f"Applying {len(to_apply)} migrations...")
        backend.apply_migrations(to_apply)
        logger.info("Migrations applied successfully.")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise


def reset_database() -> None:
    logger.info("Starting database reset process...")
    db_url = settings.database_url
    try:
        backend = get_backend(db_url)
        migrations_dir = Path(__file__).resolve().parents[2] / "migrations"
        migrations = read_migrations(str(migrations_dir))
        logger.info("Checking for applied migrations to rollback...")
        to_rollback = backend.to_rollback(migrations)
        if to_rollback:
            logger.info(
                f"Rolling back {len(to_rollback)} migrations. This will destroy data."
            )
            backend.rollback_migrations(to_rollback)
            logger.info("Rollback complete.")
        else:
            logger.info("No migrations found to rollback. Database is clean.")
        logger.info("Re-applying all migrations...")
        to_apply = backend.to_apply(migrations)
        if to_apply:
            backend.apply_migrations(to_apply)
            logger.info(f"Applied {len(to_apply)} migrations successfully.")
        else:
            logger.info("No migrations to apply.")

        logger.info("Database reset successfully.")
    except Exception as e:
        logger.error(f"Database reset failed: {e}")
        raise


def get_db_connection() -> psycopg2.extensions.connection:
    try:
        conn = psycopg2.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            dbname=settings.DB_NAME,
        )
        conn.autocommit = False
        return conn
    except Exception as e:
        logger.critical(f"Failed to connect to DB: {e}")
        raise


def apply_seeds() -> None:
    seed_dir = SEEDS_DIR
    if not seed_dir.exists():
        logger.error(f"Seed directory not found: {seed_dir}")
        logger.error("Run generate_seeds first.")
        raise ValueError("Seed directory missing")
    files = sorted([f for f in seed_dir.glob("*.sql")])
    if not files:
        logger.warning("No .sql files found in seeds directory.")
        return
    conn = get_db_connection()
    cursor = conn.cursor()
    logger.info(f"Found {len(files)} seed files. Starting application...")
    try:
        for filepath in files:
            logger.info(f"Executing {filepath.name}...")
            sql_content = filepath.read_text(encoding="utf-8")
            if sql_content.strip():
                cursor.execute(sql_content)
        conn.commit()
        logger.info("All seeds applied successfully!")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error applying seed {filepath.name}: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    generate_seeds()