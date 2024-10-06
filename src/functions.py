import requests


def get_repos_stats(owner: str, repo: list[str]) -> list[dict] | None:
    """ Собирает статистику по репозиториям заданного пользователя на GitHab,
     принимает на вход имя пользователя и названия репозиториев """
    repos_stat = []

    for rep in repo:
        url = f"https://api.github.com/repos/{owner}/{rep}"
        headers = {"Accept": "application/vnd.github+json"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos_stat.append(response.json())
        else:
            print(f"Error: {response.status_code}")

    return repos_stat
