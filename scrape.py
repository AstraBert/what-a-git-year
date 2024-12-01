import requests

def fetch_contribution_details(username, token):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {token}"}

    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          commitContributionsByRepository {
            repository {
              name
            }
            contributions(first: 100) {
              nodes {
                occurredAt
                commitCount
              }
            }
          }
          pullRequestContributionsByRepository {
            repository {
              name
            }
            contributions(first: 100) {
              nodes {
                occurredAt
                pullRequest {
                  title
                  url
                }
              }
            }
          }
          issueContributionsByRepository {
            repository {
              name
            }
            contributions(first: 100) {
              nodes {
                occurredAt
                issue {
                  title
                  url
                }
              }
            }
          }
        }
      }
    }
    """
    variables = {"username": username}

    response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")


def parse_contribution_details(contrib_dets):
    commits_repos = []
    pull_reqs_repos = []
    issues_repos = []
    commits = 0
    issues = 0
    prs = 0
    # Process the data for better readability
    if contrib_dets:
        user_contributions = contrib_dets["data"]["user"]["contributionsCollection"]
        for repo in user_contributions["commitContributionsByRepository"]:
            repo_name = repo["repository"]["name"]
            commits_repos.append(repo_name)
            for commit in repo["contributions"]["nodes"]:
                commits+=commit['commitCount']
        for repo in user_contributions["pullRequestContributionsByRepository"]:
            repo_name = repo["repository"]["name"]
            pull_reqs_repos.append(repo_name)
            for pr in repo["contributions"]["nodes"]:
                prs+=1
        for repo in user_contributions["issueContributionsByRepository"]:
            repo_name = repo["repository"]["name"]
            issues_repos.append(repo_name)
            for issue in repo["contributions"]["nodes"]:
                issues+=1
    return f"- 🚀 You created **{commits} commits** in {len(set(commits_repos))} personal repositories\n\n- ⤴️ You created **{prs} pull requests** in {len(set(pull_reqs_repos))} repositories\n\n- 🪲 You created **{issues} issues** in {len(set(issues_repos))} repositories\n\n"
