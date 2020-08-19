import os
import random

from apiplay.github_api import GitHub


github = None


def setup_module():
    global github
    github = GitHub(os.environ['GITHUB_ACCESS_TOKEN'])


def test_get_user_info():
    resp = github.api_get('/user').json()
    assert(resp['login'] == 'agstephens')


def test_list_repos():
    my_repos = github.users.get("agstephens").repos.all()

    assert(len(list(my_repos)) > 10)


def test_create_release():
    def get_tag():  return '.'.join([str(random.randint(0, 9)) for _ in range(3)])
    def get_body(): 
        s = [_ for _ in 'Some text or other']
        random.shuffle(s)
        return ''.join(s)
 
    tag = get_tag()
    owner, repo, tag_name, release_name, tag_body = 'agstephens', 'api-playground', tag, f'v{tag}', get_body()

    resp = github.create_release(owner, repo, tag_name, release_name, tag_body)
    assert(resp.status_code == 201)
