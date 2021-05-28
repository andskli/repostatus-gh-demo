from flask import Flask, render_template
from ddbcache import DDBCache
from github import Github


app = Flask(__name__)
ddb = DDBCache(table_name='repostatus_cache')
gh = Github()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/repo/<path:repo_slug>")
def repo(repo_slug):
    r = {
        'repo_slug': repo_slug,
        'data': {}
    }
    cached = ddb.get(repo_slug)
    if cached:
        app.logger.debug("Found repo in DDB cache")
        r['data'] = cached
    else:
        app.logger.debug("Couldn't find repo in cache")
        try:
            repo = gh.get_repo(r['repo_slug'])
            r['data']['stargazers_count'] = repo.stargazers_count
            r['data']['watchers_count'] = repo.watchers_count
            r['data']['open_issues_count'] = repo.open_issues_count
            print("REPO DATA: ", r['data'])
            print("PUTTING: ", r['repo_slug'], r['data'])
            ddb.put(r['repo_slug'], r['data'])
        except Exception as e:
            print(e)
    return render_template('repo.html', repo=r)


if __name__ == '__main__':
    app.run()
