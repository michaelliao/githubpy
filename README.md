githubpy
========

### Welcome

githubpy is a simple Python SDK for GitHub API v3. It is small, single-file and easy-to-use.

Sample code:

```
>>> gh = GitHub()
>>> gh.users('michaelliao').get()
{'public_repos': 11, 'public_gists': 0, 'name': u'Michael Liao', ... }
```

### Call APIs

According to GitHub API doc of how to [get a single user](http://developer.github.com/v3/users/#get-a-single-user):

```
GET /users/:user
```

Python code:

```
>>> gh.users('michaelliao').get()
{'public_repos': 11, 'name': u'Michael Liao', ...}
```

Returns dict object but also treat as object:

```
>>> u['name']
u'Michael Liao'
>>> u.name
u'Michael Liao'
```

Another example of how to [list issues for a repository](http://developer.github.com/v3/issues/#list-issues-for-a-repository):

```
GET /repos/:owner/:repo/issues
Parameters
  milestone
    Integer Milestone number
    none for Issues with no Milestone.
    * for Issues with any Milestone.
  state
    open, closed, default: open
  assignee
    String User login
    none for Issues with no assigned User.
    * for Issues with any assigned User.
  ...
```

Python code for get 'open' issues which assigned to 'michaelliao':

```
>>> gh.repos('michaelliao')('githubpy').issues.get(state='open', assignee='michaelliao')
```

### Using POST, PUT, PATCH and DELETE

[Create an issue](http://developer.github.com/v3/issues/#create-an-issue):

```
POST /repos/:owner/:repo/issues
Input
  title
    Required string
  body
    Optional string
  assignee
    Optional string - Login for the user that this issue should be assigned to.
  ...
```

Python code to create an issue:

```
>>> gh.repos('michaelliao')('githubpy').issues.post(title='sample issue', body='found a bug')
```

### Authentication

Anonymous API call:

```
>>> gh = GitHub()
```

Basic authentication using username and password:

```
>>> gh = GitHub(username='loginname', password='your-password')
```

OAuth authentication is a bit complicated:

Step 1: redirect user to the generated URL:

```
>>> gh = GitHub(client_id='your-client-id', client_secret='your-client-secret', redirect_uri=None, scope=None)
>>> print gh.authorize_url(state='a-random-string')
'https://github.com/login/oauth/authorize?client_id=12345678'
```

Step 2: GitHub redirects back to your site with parameter 'code' and 'state' (optional). Then get an access token:

```
>>> code = request.input('code')
>>> state = request.input('state')
>>> print gh.get_access_token(code, state)
'abc1234567xyz'
```

Step 3: Using access token as authentication to call APIs:

```
>>> gh = GitHub(access_token='abc1234567xyz')
```

### Rate Limiting

You can find rate limiting after API call:

```
>>> u = gh.user('michaelliao').get()
>>> gh.x_ratelimit_limit
5000
>>> gh.x_ratelimit_remaining
4999

### Enjoy!
