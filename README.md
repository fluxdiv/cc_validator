# cc_validator

A githook that validates commit messages follow a (modified) [conventional commit spec](https://www.conventionalcommits.org/en/v1.0.0/)

## Requirements

- python3
- git
- curl

## Setup

### Option 1)
Run the [installation script](/installer.py) from your repo's root
```
curl -fsSL https://raw.githubusercontent.com/fluxdiv/cc_validator/main/installer.py | python3
```
This does the following:
- Verifies the repo is a git repo
- Checks whether git hooks have already been set up
- If they have, the hook will be setup the same way
- If not, a `~/my_repo_root/.githooks/` dir is created, and is added to the repo's git config via `git config core.hooksPath .githooks`
- The [commit-msg hook](/commit-msg) is created/copied and set as executable
- Setup complete, commits will not be allowed unless they follow the spec
---
### Option 2)
Setup the hook manually:
- Create a `.githooks` directory in the root of your repo
- Create a `.githooks/commit-msg` file
- Copy the contents of the [commit-msg hook](/commit-msg) into the file
- Set as executable `chmod a+x .githooks/commit-msg`
- Set the repo's git config to use it `git config core.hooksPath .githooks`
- Setup complete
