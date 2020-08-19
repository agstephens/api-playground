import json

import logging
logger = logging.getLogger('rackit.connection')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

import requests

from rackit import Connection, Resource, ResourceManager, NestedResource, RootResource


class GitHubAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        # Add the correctly formatted header to the request
        request.headers['Authorization'] = "token {}".format(self.token)
        return request


class GitHubResourceManager(ResourceManager):
    def extract_list(self, response):
        # Extract the url for the next page from the Link header
        next_page = response.links.get('next', {}).get('url')
        return response.json(), next_page


class GitHubResource(Resource):
    class Meta:
        manager_cls = GitHubResourceManager


class RepositoryManager(ResourceManager):
    def for_authenticated_user(self, **params):
        return self._fetch_all("/user/repos", params)

    def for_user(self, username, **params):
        return self._fetch_all("/user/{}/repos".format(username), params)

    def for_org(self, org, **params):
        return self._fetch_all("/orgs/{}/repos".format(org), params)


class Repository(Resource):
    class Meta:
        manager_cls = RepositoryManager
        endpoint = "/repos"
        primary_key_field = "full_name"


class User(GitHubResource):
    class Meta:
        endpoint = "/users"
        primary_key_field = "login"

    repos = NestedResource(Repository)


class GitHub(Connection):

    GITHUB_API = "https://api.github.com"
    users = RootResource(User)

    def __init__(self, token):
        # Initialise a requests session that uses the token auth
        session = requests.Session()
        session.auth = GitHubAuth(token)
        super().__init__(self.GITHUB_API, session)

    def create_release(self, owner, repo, tag_name, release_name, tag_body, 
                       draft=False, prerelease=False):
        url_path = f'/repos/{owner}/{repo}/releases' 
        content = {'tag_name': tag_name,
                   'name': release_name,
                   'body': tag_body,
                   'draft': draft,
                   'prerelease': prerelease} 

        return self.api_post(url_path, data=json.dumps(content)) 


"""
github = GitHub(GITHUB_PERSONAL_ACCESS_TOKEN)
print(github.api_get('/user').json())

my_repos = github.users.get("agstephens").repos.all()
print(len(list(my_repos)))
for _ in my_repos: print(_)


gh = github
print('Use "gh" to create a release...')


owner, repo, tag_name, release_name, tag_body = 'agstephens', 'api-playground', '1.0.0', 'v1.0.0', 'First release'

gh.create_release(owner, repo, tag_name, release_name, tag_body)
"""
