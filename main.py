from src.functions import get_repos_stats
from src.postgres_db import PostgresDB
from src.config import config


def main():
    repos_stat = get_repos_stats('PetruschenkoEgor', ['youtube_project', 'SkyBank'])

    postgres = PostgresDB('repository')
    conf = config()
    postgres.create_database(conf)
    postgres.create_table(conf)
    postgres.insert_data(conf, repos_stat)
    data = postgres.get_data(conf)
    to_json = postgres.export_to_json(data)
    return to_json


if __name__ == '__main__':
    print(main())
