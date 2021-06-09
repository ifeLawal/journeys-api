from models import create_all_tables, drop_table_with_name


def create_ontheset_tables():
    create_all_tables(engine_name="ontheset")


def drop_ontheset_table(table_name):
    drop_table_with_name(engine_name="ontheset", table_name=table_name)
