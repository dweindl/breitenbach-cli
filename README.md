# CLI for breitenbach time mgmt system

Simplifying checking in and out.

## Installation

Install requirements

    sudo apt install firefox-geckodriver
    pip install -r requirements.txt

Provide login information in `~/.breitenbach.yaml`:

```yaml
login_url: https://url-of-your-login-page
username: your-username
password: your-password
```

## Usage

Start time recording:

    ./breitenbach.py --checkin

Stop time recording:

    ./breitenbach.py --checkout

