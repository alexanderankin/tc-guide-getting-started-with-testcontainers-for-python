import os
import pytest
from testcontainers.postgres import PostgresContainer

from customers import customers

postgres = PostgresContainer("postgres:16-alpine")


@pytest.fixture(scope="module", autouse=True)
def setup():
    postgres.start()
    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] = postgres.get_exposed_port(5432)
    os.environ["DB_USERNAME"] = postgres.POSTGRES_USER
    os.environ["DB_PASSWORD"] = postgres.POSTGRES_PASSWORD
    os.environ["DB_NAME"] = postgres.POSTGRES_DB
    customers.create_table()
    yield
    postgres.stop()


@pytest.fixture(scope="function", autouse=True)
def setup_data():
    customers.delete_all_customers()


def test_get_all_customers():
    customers.create_customer(customers.Customer(0, "Siva", "siva@gmail.com"))
    customers.create_customer(customers.Customer(0, "James", "james@gmail.com"))
    customers_list = customers.get_all_customers()
    assert len(customers_list) == 2


def test_get_customer_by_email():
    customers.create_customer(customers.Customer(0, "John", "john@gmail.com"))
    customer = customers.get_customer_by_email("john@gmail.com")
    assert customer.name == "John"
    assert customer.email == "john@gmail.com"
