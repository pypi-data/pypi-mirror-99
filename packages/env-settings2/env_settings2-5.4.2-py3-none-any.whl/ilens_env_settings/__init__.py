"""
------------------------------------------------DO NOT EDIT-------------------------------------------------

The following file is an utility to load environment configuration for the application to use.

Any modifications to the module should be requested to DevOps team.

All variables will be read from system environment and fallback to .env file in the root directory of your project.
"""
import sys
from typing import Optional, Any

from pydantic import BaseSettings, ValidationError


class EnvironmentSettings(BaseSettings):
    def __init__(self, **values: Any):
        super().__init__(**values)

    @property
    def __version__(self):
        return 'V5.4.2'

    # Global application environment
    APP_ENV: str = "dev"

    # Mongo Details
    MONGO_URI: Optional[str]

    # Kairos Details
    KAIROS_URI: Optional[str]

    # MQTT Details
    MQTT_HOST: Optional[str]
    MQTT_PORT: Optional[int] = 1883
    MQTT_AUTH: Optional[bool] = False
    MQTT_USERNAME: Optional[str]
    MQTT_PASSWORD: Optional[str]

    # Redis Details
    REDIS_HOST: Optional[str]
    REDIS_PORT: Optional[int]

    # KAFKA Details
    KAFKA_HOST: Optional[str]
    KAFKA_PORT: Optional[int]

    # Postgres Details
    POSTGRES_URI: Optional[str]

    # Base Proxy for all services
    BASE_PROXY: Optional[str]

    # Security aspects
    SECURITY_IP_CHECK: bool = True
    SECURITY_USER_CHECK: bool = True
    SECURITY_AGENT_CHECK: bool = True


def get_env_settings(use_local=False, env_file='.env'):
    """
    The function loads all the environmental variables and makes it available as a class object.
    :return: env_settings
    """
    try:
        if use_local:
            env_settings = EnvironmentSettings(
                _env_file=env_file,
                _env_file_encoding='utf-8')
        else:
            env_settings = EnvironmentSettings()
        return env_settings
    except ValidationError as e:
        print(e.json())
        sys.exit(1)
    except Exception as e:
        print(e.args)
        sys.exit(1)
