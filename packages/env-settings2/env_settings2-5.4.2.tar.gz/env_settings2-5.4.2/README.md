# iLens Environment Settings

## Installation
```bash
pip install git+https://gitlab-pm.knowledgelens.com/iudeen/ilens-env-settings.git
```

## How to use?
To get started, ensure you have set system environments or create .env file in your project root.

```python
from ilens_env_settings import get_env_settings

# to load from system env
env_settings = get_env_settings()

# to load from local .env at root
env_settings_local = get_env_settings(use_local=True)

# to load from local .env at different location
env_settings_local_other = get_env_settings(use_local=True, env_file='<path_to_file>')
```

`get_env_settings` returns a class object containing all the required environment variables.

To access an environment variable
```python
app_env = env_settings.APP_ENV

# to get all as a dictionary
env_settings.dict()
```

[Sample `.env` file](assets/.env)
