githubpy
========

### Welcome

githubpy is a simple Python SDK for GitHub's API v3. It's all contained in one easy-to-use file.

It runs on Python 2 (2.6 and above) and Python 3 (3.3 and above).

Sample code:

```
>>> gh = GitHub()
>>> gh.users('michaelliao').get()
{'public_repos': 11, 'name': u'Michael Liao', ... }
```

Requirement:

Python 2.6, 2.7, 3.3, 3.4


### Call APIs

All APIs are dynamic calls. You can construct an API call by GitHub's API doc.

For example, according to GitHub API doc of how to [get a single user](http://developer.github.com/v3/users/#get-a-single-user):

```
GET /users/:user
```

Note the `:user` variable. You can make a call in Python like this:

```
>>> gh.users('michaelliao').get()
{'public_repos': 11, 'name': u'Michael Liao', ...}
```

This returns a dict, but it can also be treated like an object:

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

Python keywords can filter for `open` issues assigned to `michaelliao`:

```
>>> gh.repos('michaelliao')('githubpy').issues \
      .get(state='open', assignee='michaelliao')
```


### Using POST, PUT, PATCH, and DELETE

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
>>> gh.repos('michaelliao')('githubpy').issues \
      .post(title='sample issue', body='found a bug')
```

Remember, all APIs are dynamic calls...so you won't need update this SDK if GitHub add new APIs!


### Authentication

Anonymous API call:

```
>>> gh = GitHub()
```

Basic authentication using username and password:

```
>>> gh = GitHub(username='«loginname»', password='«your-password»')
```

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
>>> print gh.get_access_token(code, state)
'abc1234567xyz'
```

**Step 3:** Using access token as authentication to call APIs:

```
>>> gh = GitHub(access_token='abc1234567xyz')
```


### Errors

An `ApiError` is raised if something wrong. 
There are 2 sub-classes: `ApiAuthError` and `ApiNotFoundError`.

```
try:
    gh.user.emails.delete('email@example.com')
except ApiNotFoundError as e:
    print e, e.request, e.response
```

NOTE: You may get `ApiNotFoundError` (404 Not Found) even if the URL is correct, but authentication fails. According to GitHub's API docs:

    Requests that require authentication will return 404, instead of 403, 
    in some places. This is to prevent the accidental leakage of private 
    repositories to unauthorized users.


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

githubpy is distributed under [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0.txt). See LICENSE file.


### Enjoy!
