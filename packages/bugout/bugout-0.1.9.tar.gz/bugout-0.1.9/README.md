# bugout-python
Python client library for Bugout API

## Setup
- Add variables from `sample.env` in you development environment
```bash
export BUGOUT_TIMEOUT_SECONDS=5
```

- Example of usage, just fill `token`, `group_id`, `journal_id` and `entry_id` with proper values from your account. Or remove unnecessary variables and API calls.
```python
from bugout.app import Bugout


def main():
    bugout = Bugout()

    token = ""
    group_id = ""
    journal_id = ""
    entry_id = ""

    user = bugout.get_user(token=token)
    print(f"User name is {user.username}")

    group = bugout.get_group(token=token, group_id=group_id)

    journal = bugout.get_journal(token=token, journal_id=journal_id)
    entry = bugout.get_entry(token=token, journal_id=journal.id, entry_id=entry_id)

    search_res = bugout.search(
        token=token, journal_id=journal.id, query="your query", content=False
    )
    print(f"Search results: {search_res}")


if __name__ == "__main__":
    main()
```
