"""
API for accessing files from github
"""
from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile


def get_file(owner: str, repo: str, file_path: str, token: str = "") -> str:
    """
    Gets a file from a repo
    """

    g = Github() if token == "" else Github(token)
    repo: Repository = g.get_repo(f"{owner}/{repo}")
    response: ContentFile = repo.get_contents(file_path)
    return str(response.decoded_content, "utf-8")
