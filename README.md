# api-playground
Messing about with APIs

## Interacting with GitHub

You need to create a Github Access Token in:

 - https://github.com/settings/tokens

Create a token with `repo` actions ticked and copy it and set the environment variable:

```
export GITHUB_ACCESS_TOKEN=...your...token...
```

### Basic usage, listing repositories

```
import os
from apiplay.github_api import GitHub

github = GitHub(os.environ['GITHUB_ACCESS_TOKEN'])
print(github.api_get('/user').json())

my_repos = github.users.get("agstephens").repos.all()
print(len(list(my_repos)))

for _ in my_repos: 
    print(_)
```

### Creating a release of a package

```
from apiplay.github_api import GitHub

github = GitHub(os.environ['GITHUB_ACCESS_TOKEN'])

owner, repo, tag_name, release_name, tag_body = 'agstephens', 'api-playground', '1.0.0', 'v1.0.0', 'First release'
github.create_release(owner, repo, tag_name, release_name, tag_body)

```
