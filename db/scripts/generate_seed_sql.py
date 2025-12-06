import os
import random
from datetime import datetime, timedelta
from faker import Faker

OUTPUT_DIR = "db/seeds"
START_DATE = datetime(2025, 11, 1)
END_DATE = datetime(2025, 12, 5)

fake = Faker("pt_BR")
Faker.seed(42)
random.seed(42)

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
STAFF_COUNT_CHEFS = 3
CUSTOMER_COUNT = 75
TABLE_COUNT = 20

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def escape_sql_string(val):
    return str(val).replace("'", "''")

def generate_002_infrastructure():
    filepath = os.path.join(OUTPUT_DIR, "002_seed_infrastructure.sql")
    print(f"Generating {filepath}...")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("-- 002_seed_infrastructure.sql\n")
        f.write("-- Tables (Mesa), Staff (Garcom/Cozinheiro), and Menu (Prato)\n\n")
        f.write("-- Mesa\n")
        f.write(
            "INSERT INTO mesa (id_mesa, numero, capacidade, localizacao) VALUES\n"
        )
        rows = []
        for i in range(1, TABLE_COUNT + 1):
            cap = random.choice([2, 4, 6, 8])
            loc = random.choice(["Interna", "Externa", "Varanda"])
            rows.append(f"({i}, {i}, {cap}, '{loc}')")
        f.write(",\n".join(rows) + ";\n\n")
        f.write("-- Garcom\n")
        f.write("INSERT INTO garcom (id_funcionario, nome, cpf, salario, turno, comissao) VALUES\n")
        w_rows = []
        for i in range(1, STAFF_COUNT_WAITERS + 1):
            name = escape_sql_string(fake.name())
            cpf = fake.cpf().replace(".", "").replace("-", "")
            salario = random.choice([1500.00, 1800.00, 2000.00])
            turno = random.choice(["Manhã", "Noite"])
            comissao = 5.00
            w_rows.append(f"({i}, '{name}', '{cpf}', {salario}, '{turno}', {comissao})")
        f.write(",\n".join(w_rows) + ";\n\n")
        f.write("-- Cozinheiro\n")
        f.write("INSERT INTO cozinheiro (id_funcionario, nome, cpf, salario, especialidade) VALUES\n")
        c_rows = []
        for i in range(1, STAFF_COUNT_CHEFS + 1):
            name = escape_sql_string(fake.name())
            cpf = fake.cpf().replace(".", "").replace("-", "")
            salario = random.choice([2500.00, 3200.00, 4000.00])
            spec = random.choice(["Massas", "Grelhados", "Sobremesas"])
            c_rows.append(f"({i}, '{name}', '{cpf}', {salario}, '{spec}')")
        f.write(",\n".join(c_rows) + ";\n\n")
        f.write("-- Prato\n")
        f.write(
            "INSERT INTO prato (id_prato, nome, preco, categoria) VALUES\n"
        )
        d_rows = []
        for d_id, (name, price, cat) in MENU_ITEMS.items():
            d_rows.append(
                f"({d_id}, '{escape_sql_string(name)}', {price}, '{cat}')"
            )
        f.write(",\n".join(d_rows) + ";\n\n")

def generate_003_customers():
    filepath = os.path.join(OUTPUT_DIR, "003_seed_customers.sql")
    print(f"Generating {filepath}...")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("-- 003_seed_customers.sql\n\n")
        f.write("INSERT INTO cliente (id_cliente, nome, telefone, email) VALUES\n")
        rows = []
        for i in range(1, CUSTOMER_COUNT + 1):
            name = escape_sql_string(fake.name())
            email = f"cliente{i}@exemplo.com"
            phone = fake.phone_number()[:15]
            rows.append(f"({i}, '{name}', '{phone}', '{email}')")
        f.write(",\n".join(rows) + ";\n")

def generate_004_orders(orders_list):
    """
    Generates orders and order items.
    Populates orders_list with dicts for review generation.
    """
    filepath = os.path.join(OUTPUT_DIR, "004_seed_orders.sql")
    print(f"Generating {filepath}...")
    current_order_id = 1000
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("-- 004_seed_orders.sql\n")
        f.write("-- Pedido and Item_Pedido\n\n")
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
                status = "CLOSED"
                if curr_date.date() == END_DATE.date():
                    if random.random() < 0.3:
                        status = "OPEN"
                num_items = random.randint(1, 5)
                selected_dishes = random.choices(list(MENU_ITEMS.keys()), k=num_items)
                total_amount = 0.0
                people_count = random.randint(1, 4)
                if status == "CLOSED":
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
                    f"({o_id}, '{dt_str}', {total_amount:.2f}, {cust_id}, {table_id}, {waiter_id}, '{status}', {people_count})"
                )
            if day_orders_sql:
                f.write(f"-- Pedidos for {curr_date.date()}\n")
                f.write(
                    "INSERT INTO pedido (id_pedido, data_pedido, valor_total, id_cliente, id_mesa, id_funcionario, status, quantidade_pessoas) VALUES\n"
                )
                f.write(",\n".join(day_orders_sql) + ";\n")
                f.write(
                    "INSERT INTO item_pedido (id_pedido, id_prato, quantidade, observacao) VALUES\n"
                )
                f.write(",\n".join(day_items_sql) + ";\n\n")
            curr_date += timedelta(days=1)

def generate_005_reviews(orders_list):
    filepath = os.path.join(OUTPUT_DIR, "005_seed_reviews.sql")
    print(f"Generating {filepath}...")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("-- 005_seed_reviews.sql\n\n")
        f.write(
            "INSERT INTO avaliacao (id_cliente, id_prato, id_pedido, nota, comentario) VALUES\n"
        )
        review_rows = []
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
        f.write(",\n".join(review_rows) + ";\n")

def generate_006_reset_sequences():
    filepath = os.path.join(OUTPUT_DIR, "006_reset_sequences.sql")
    print(f"Generating {filepath}...")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("-- 006_reset_sequences.sql\n")
        f.write("-- Reset auto-increment sequences after manual ID insertion\n\n")
        tables_to_reset = [
            ("cliente", "id_cliente"),
            ("mesa", "id_mesa"),
            ("prato", "id_prato"),
            ("garcom", "id_funcionario"),
            ("cozinheiro", "id_funcionario"),
            ("pedido", "id_pedido"),
        ]
        for table, col in tables_to_reset:
            f.write(
                f"SELECT setval(pg_get_serial_sequence('{table}', '{col}'), (SELECT MAX({col}) FROM {table}));\n"
            )
        f.write(
            f"SELECT setval(pg_get_serial_sequence('item_pedido', 'id_item_pedido'), (SELECT MAX(id_item_pedido) FROM item_pedido));\n"
        )
        f.write(
            f"SELECT setval(pg_get_serial_sequence('avaliacao', 'id_avaliacao'), (SELECT MAX(id_avaliacao) FROM avaliacao));\n"
        )

def main():
    ensure_dir(OUTPUT_DIR)
    orders_list = []
    generate_002_infrastructure()
    generate_003_customers()
    generate_004_orders(orders_list)
    generate_005_reviews(orders_list)
    generate_006_reset_sequences()
    print("Done! Seed files created in 'db/seeds/'.")

if __name__ == "__main__":
    main()