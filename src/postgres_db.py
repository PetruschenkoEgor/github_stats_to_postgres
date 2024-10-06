import psycopg2


class PostgresDB:
    """ Обеспечивает взаимодействие с базой данных Postgres """

    def __init__(self, database_name: str) -> None:
        self.__database_name = database_name

    def create_database(self, params: dict) -> None:
        """ Создание базы данных """
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f'DROP DATABASE IF EXISTS {self.__database_name}')
            cur.execute(f'CREATE DATABASE {self.__database_name}')

        conn.close()

    def drop_database(self, params: dict) -> None:
        """ Удаление базы данных """
        conn = psycopg2.connect(dbname='postgres', **params)
        with conn.cursor() as cur:
            cur.execute(f'DROP DATABASE IF EXISTS {self.__database_name}')

    def create_table(self, params: dict) -> None:
        """ Создание таблицы """
        conn = psycopg2.connect(dbname=self.__database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS repositories (
                    id serial PRIMARY KEY,
                    name_repos varchar NOT NULL,
                    login varchar NOT NULL,
                    watchers int,
                    forks int,
                    subscribers int,
                    visibility varchar(10),
                    url varchar
                )
            """)

        conn.commit()
        conn.close()

    def insert_data(self, params: dict, repos: list[dict]) -> None:
        """ Добавление данных в таблицу """
        conn = psycopg2.connect(dbname=self.__database_name, **params)
        with conn.cursor() as cur:
            for repo in repos:
                cur.execute("""
                    INSERT INTO repositories (name_repos, login, watchers, forks, subscribers, visibility, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (repo['name'], repo['owner']['login'], repo['watchers'], repo['forks'], repo['subscribers_count'],
                 repo['visibility'], repo['svn_url'])
                    )

        conn.commit()
        conn.close()

    @staticmethod
    def export_to_json(data: list[tuple]) -> list[dict[str, int]]:
        """ Экспорт данных в формат JSON """
        list_json = []

        for rep in data:
            repository = dict()
            repository['id'] = rep[0]
            repository['name_repos'] = rep[1]
            repository['login'] = rep[2]
            repository['watchers'] = rep[3]
            repository['forks'] = rep[4]
            repository['subscribers'] = rep[5]
            repository['visibility'] = rep[6]
            repository['url'] = rep[7]
            list_json.append(repository)

        return list_json

    def get_data(self, params: dict) -> list[tuple]:
        """ Получение данных из таблицы """
        try:
            conn = psycopg2.connect(dbname=self.__database_name, **params)
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM repositories
                """)
                data = cur.fetchall()
                return data

        except Exception as e:
            print(f"Ошибка при работе с БД: {e}")

        finally:
            if conn:
                conn.close()
