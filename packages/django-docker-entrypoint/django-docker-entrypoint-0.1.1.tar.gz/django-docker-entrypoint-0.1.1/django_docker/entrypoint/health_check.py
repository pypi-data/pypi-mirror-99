import json
import os
from urllib.request import urlopen


def health_check(silent=False) -> None:
    url = f"http://127.0.0.1:{os.getenv('DJANGO_PORT', 8000)}/" \
          f"{os.getenv('DJANGO_DOCKER_HEALTH_PATH', 'api/health-check')}" \
          f"?format=json"
    try:
        with urlopen(url) as response:
            if response.status == 200:
                response_data = json.loads(response.read())
                if not silent:
                    print(json.dumps(response_data, indent=2))
                return
            raise
    except Exception as exc:
        if not silent:
            raise exc
        exit(1)
