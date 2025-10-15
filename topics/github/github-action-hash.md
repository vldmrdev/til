_I find it strange that gists are separated from the main github profile, so I'll add the script here._


"It is a good manner to pin GitHub Actions versions by commit hash. GitHub tags are mutable so they have a substantial security and reliability risk."

Inspired by https://github.com/suzuki-shunsuke/pinact :joy:

```python
import requests


def git_action_sha(action: str) -> str:
    github_api = "https://api.github.com/repos"
    # check action name
    try:
        owner_repo, ref = action.split("@", 1)
        owner, repo = owner_repo.split("/", 1)
    except ValueError:
        return "invalid action name (must be like owner/repo@ref)"

    # check owner exist
    url = f"{github_api}/{owner}/{repo}"
    r = requests.get(url)
    if r.status_code != 200:
        return f"owner '{owner}' or repository '{repo}' doesn't exist"

    # search as tag
    url = f"{github_api}/{owner}/{repo}/git/refs/tags/{ref}"
    r = requests.get(url)
    if r.status_code == 200:
        obj = r.json()["object"]
        if obj["type"] == "commit":
            return obj["sha"]
        elif obj["type"] == "tag":  # annotated tag
            tag_resp = requests.get(obj["url"])
            if tag_resp.status_code == 200:
                return tag_resp.json()["object"]["sha"]
            else:
                return f"Failed request ({tag_resp.status_code})"

    # search as branch
    url = f"{github_api}/{owner}/{repo}/git/refs/heads/{ref}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()["object"]["sha"]

    return f"Error: ref '{ref}' doesn't found (status: {r.status_code})"


if __name__ == "__main__":
    # get actions hash for secure you actions
    ACTIONS = [
        "actions/checkout@v5",
        "actions/setup-python@v6",
        "docker/login-action@v3",
    ]

    for action_name in ACTIONS:
        sha = git_action_sha(action_name)
        print(f"{action_name}: {sha}")
```