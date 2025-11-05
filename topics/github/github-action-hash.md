_I find it strange that gists are separated from the main github profile, so I'll add the script here._


"It is a good manner to pin GitHub Actions versions by commit hash. GitHub tags are mutable so they have a substantial security and reliability risk."

Inspired by https://github.com/suzuki-shunsuke/pinact :joy:

```python
import requests

def git_action_sha(action: str) -> str:
    github_api = "https://api.github.com/repos"
    if "@" not in action:
        return "invalid action name (must contain '@')"

    action_part, ref = action.split("@", 1)
    parts = action_part.split("/")

    if len(parts) < 2:
        return "invalid action name (must be owner/repo[/path]@ref)"
    
    # consider case for repos like github/codeql-action/init@v4
    owner = parts[0]
    repo = parts[1]


    repo_url = f"{github_api}/{owner}/{repo}"
    r = requests.get(repo_url)
    if r.status_code != 200:
        return f"repository '{owner}/{repo}' not found (HTTP {r.status_code})"

    # try release
    release_url = f"{github_api}/{owner}/{repo}/releases/tags/{ref}"
    r = requests.get(release_url)
    if r.status_code == 200:
        commit_ref = r.json()["target_commitish"]
        commit_url = f"{github_api}/{owner}/{repo}/commits/{commit_ref}"
        cr = requests.get(commit_url)
        if cr.status_code == 200:
            return cr.json()["sha"]
        else:
            return f"failed to resolve commit for '{commit_ref}' (HTTP {cr.status_code})"

    # try commits
    commit_url = f"{github_api}/{owner}/{repo}/commits/{ref}"
    r = requests.get(commit_url)
    if r.status_code == 200:
        return r.json()["sha"]

    return f"ref '{ref}' not found in '{owner}/{repo}' (HTTP {r.status_code})"


if __name__ == "__main__":
    ACTIONS = [
        "actions/checkout@v5",
        "github/codeql-action/analyze@v4",
        "github/codeql-action/init@v4",
    ]

    for action_name in ACTIONS:
        sha = git_action_sha(action_name)
        print(f"{action_name}: {sha}")
```