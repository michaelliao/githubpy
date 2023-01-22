githubpy
========

### Welcome

githubpy is a simple Python3 client for GitHub's REST API. It's all contained in one easy-to-use file.

Sample code:

```
>>> from github import GitHub
>>> gh = GitHub(token='your-github-token')
>>> gh.users('michaelliao').get()
{'id': 470058, 'name': 'Michael Liao', ... }
```

Requirement:

Python 3.x

Python 2 is not supported.

### Call APIs

All APIs are dynamic calls. You can construct an API call by GitHub's [REST API](https://docs.github.com/en/rest).

For example, according to GitHub API doc of how to [get a user](https://docs.github.com/en/rest/users/users#get-a-user):

```
GET /users/{username}
```

Note the `{username}` variable. You can make a call in Python like this:

```
>>> gh.users('michaelliao').get()
{'id': 470058, 'name': 'Michael Liao', ... }
```

This returns a dict, but it can also be treated like an object:

```
>>> u['name']
'Michael Liao'
>>> u.name
'Michael Liao'
```

Another example of how to [list repository issues](https://docs.github.com/en/rest/issues/issues#list-repository-issues):

```
GET /repos/{owner}/{repo}/issues
Query parameters:
  state: open, closed, all
  assignee: username or *
  sort: created, updated, comments
  direction: asc, desc
  page: 1, 2, 3, ...
  per_page: 30
  ...
```

Python keywords can filter for `open` issues assigned to `michaelliao`:

```
>>> gh.repos('michaelliao')('githubpy').issues \
      .get(state='open', assignee='michaelliao')
```

### Using POST, PUT, PATCH, and DELETE

[Create an issue](https://docs.github.com/en/rest/issues/issues#create-an-issue):

```
POST /repos/{owner}/{repo}/issues
Body json:
{
  "title": "Found a bug",
  "body": "Having a problem with this.",
  "assignees": ["michaelliao"]
}
```

Python code to create an issue:

```
>>> issue = dict(title='Found a bug', body='Having a problem with this.', assignees=["michaelliao"])
>>> gh.repos('michaelliao')('githubpy').issues \
      .post(issue)
```

Remember, all APIs are dynamic calls, so you won't need update this SDK if GitHub add new APIs!

### Authentication

Anonymous API call:

```
>>> gh = GitHub()
```

Authentication with GitHub token:

```
>>> gh = GitHub(token='ghp_...')
```

Personal token can be generated from `Settings` - `Developer settings` - `Personal access tokens`.

OAuth authentication is a bit complicated:

**Step 1:** Redirect user to the generated URL:

```
>>> gh = GitHub(client_id='1234', client_secret='secret')
>>> print gh.authorize_url(state='a-random-string')
'https://github.com/login/oauth/authorize?client_id=1234'
```

**Step 2:** GitHub redirects back to your site with the parameters `code` and `state` (optional). Then get an access token:

```
>>> code = request.input('code')
>>> state = request.input('state')
>>> t = gh.get_access_token(code, state)
>>> print(t.token_type, t.scope, t.access_token)
'bearer', 'repo, user', 'abc1234567xyz'
```

**Step 3:** Using access token as authentication to call APIs:

```
>>> gh = GitHub(token='abc1234567xyz')
```


### Errors

An `ApiError` is raised if something wrong. 
There are sub-classes of `ApiError`:

- `ApiAuthError`: OAuth failed.
- `ApiForbiddenError`: 403 response.
- `ApiNotFoundError`: 404 response.
- `ApiConflictError`: 409 response.

```
try:
    gh.user.emails.delete('email@example.com')
except ApiNotFoundError as e:
    print(e.code, e.url, str(e))
```

NOTE: You may get `ApiNotFoundError` (404 Not Found) even if the URL is correct, but authentication fails. According to GitHub's API docs:

> Requests that require authentication will return 404, instead of 403, 
> in some places. This is to prevent the accidental leakage of private 
> repositories to unauthorized users.


### Rate Limiting

You can check rate limits after any API call:

```
>>> u = gh.users('michaelliao').get()
>>> gh.x_ratelimit_limit
5000
>>> gh.x_ratelimit_remaining
4999
```


### Licensing

githubpy is distributed under [GPLv3](LICENSE).


### Sample

- Get user and repo info: [sample_basic.py](sample_basic.py)
- Get, upload, update and delete content: [sample_content.py](sample_content.py)
- Get, create and update issues: [sample_issue.py](sample_issue.py)

### Enjoy!
