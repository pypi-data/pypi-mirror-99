# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcp_pilot']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=1,<2']

extras_require = \
{'bigquery': ['google-cloud-bigquery>=2,<3'],
 'build': ['google-cloud-build>=3,<4'],
 'datastore': ['google-cloud-datastore>=2,<3'],
 'dns': ['google-cloud-dns>=0,<1'],
 'monitoring': ['google-cloud-logging>=2,<3',
                'google-cloud-error-reporting>=1,<2'],
 'pubsub': ['google-cloud-pubsub>=2,<3'],
 'secret': ['google-cloud-secret-manager'],
 'sheets': ['gspread>=3,<4'],
 'speech': ['google-cloud-speech>=2,<3'],
 'storage': ['google-cloud-storage>=1,<2'],
 'tasks': ['google-cloud-tasks>=2,<3', 'google-cloud-scheduler>=2,<3']}

setup_kwargs = {
    'name': 'gcp-pilot',
    'version': '0.23.1',
    'description': 'Google Cloud Platform Friendly Pilot',
    'long_description': '![Github CI](https://github.com/flamingo-run/gcp-pilot/workflows/Github%20CI/badge.svg)\n[![Maintainability](https://api.codeclimate.com/v1/badges/0e03784af54dab4a7ebe/maintainability)](https://codeclimate.com/github/flamingo-run/gcp-pilot/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/0e03784af54dab4a7ebe/test_coverage)](https://codeclimate.com/github/flamingo-run/gcp-pilot/test_coverage)\n[![python](https://img.shields.io/badge/python-3.8-blue.svg)]()\n\n# Google Cloud Pilot\n\n## Installation\n\n`pip install gcp-pilot`\n\nSome APIs need extra packages, thus you must use `extras` to add them:\n\n- Cloud Tasks: `pip install gcp-pilot[tasks]`\n- Cloud Build: `pip install gcp-pilot[build]`\n- Cloud Storage: `pip install gcp-pilot[storage]`\n- Big Query: `pip install gcp-pilot[bigquery]`\n- Speech: `pip install gcp-pilot[speech]`\n- Sheets: `pip install gcp-pilot[sheets]`\n- Pub/Sub: `pip install gcp-pilot[pubsub]`\n- Datastore: `pip install gcp-pilot[datastore]`\n- Cloud DNS: `pip install gcp-pilot[dns]`\n- Secret Manager: `pip install gcp-pilot[secret]`\n\n\n## Usage\n\n```\nfrom gcp_pilot.resource import ResourceManager\n\ngrm = ResourceManager()\n```\n\n## Default Values\n\n### Credentials\n\n`gcp-pilot` uses [ADC](https://cloud.google.com/docs/authentication/production#automatically) to detect credentials. This means that you must have one of the following setups:\n- Environment variable `GOOGLE_APPLICATION_CREDENTIALS` pointing to the JSON file with the credentials\n- Run inside GCP (Compute Engine, Cloud Run, GKE, AppEngine), so the machine\'s credentials will be used\n\nYou can also globally set a service account using the environment variable `DEFAULT_SERVICE_ACCOUNT`, which will require impersonation.\n\n### Project\n\nWhen creating a client, a default project is defined by using the project that the credentials belongs to.\n\nClients that support managing resources from other projects can be overwritten per call.\n\n> Example: you create a `BigQuery` client using credentials from  `project_a`.\nAll calls will query datasets from `project_a`, unless another project is passed as parameter when performing the call.\n\nYou can also globally set a project using the environment variable `DEFAULT_PROJECT`\n\n### Location\n\nVery similar to default project, a default location is defined by using the project\'s location.\nThe project\'s location will exist if you ever enabled AppEngine, so you had to set a location then.\nOtherwise, no default location will be set.\n\nYou can also globally set a location using the environment variable `DEFAULT_LOCATION` and reduce the amount of API calls \nwhen creating clients.\n\n## Why Use ``gcp-pilot``\n\n_"Since Google already has a [generic API client](https://github.com/googleapis/google-api-python-client) and so many [specific clients](https://github.com/googleapis?q=python&type=&language=), why should I use this library?"_\n\nGoogle\'s has 2 types of clients:\n- **dedicated**: custom made for the APIs. They are excellent: they implement high level interaction with the API with friendly methods. The `gcp-pilot` can adds its value by handling authentication, friendly errors and parameter fallback.\n- **generic**: a single client that is capable of dynamically calling any REST API. They are a pain to use: very specific calls that must be translated from the documentation. The `gcp-pilot` comes in handy to add high-level interaction with friendly method such as `Calendar.create_event`, on top of all other vantages cited above.\n\n### Parameter Fallback\n\nMost of the API endpoints require `project_id` (sometimes even `project_number`) and `location`.\n\nSo `gcp-pilot` automatically detects these values for you, based on your credentials (although it\'ll require extra permissions and API calls).\n\nIf you use multiple projects, and your credentials is accessing other projects, you can still customize the parameters on each call to avoid the default fallback.\n\n\n### Friendly Errors\n\nMost of APIs return a generic ``HttpException`` with am embedded payload with error output, and also there\'s a couple of different structures for these payloads.\n\nSo `gcp-pilot` tries its best to convert these exceptions into more friendly ones, such as `NotFound`, `AlreadyExists` and `NotAllowed`.\n\nIt\'ll be much easier to capture these exceptions and handle them by its type.\n\n\n### Identification Features\n\n- **Authentication**: each client uses [ADC](https://cloud.google.com/docs/authentication/production#automatically),\nwhich consists on trying to detect the service account with fallbacks: SDK > Environment Variable > Metadata\n- **Impersonation**: it\'s possible to create clients with ``impersonate_account`` parameter that [impersonates](https://cloud.google.com/iam/docs/impersonating-service-accounts#allow-impersonation) another account.\n- **Delegation**: services _(eg. Google Workspace)_ that requires specific subjects are automatically delegated, sometimes even performing additional credential signatures.\n- **Region**: most GCP services requires a location to work on *(some even require specific locations)*. If not provided, the clients use the project\'s default location, as defined by App Engine.\n- **Authorization**: OIDC authorization is automatically generated for services *(eg. CloudRun)* that require authentication to be used.\n\n### Auto-Authorization\n\nSome services require specific authorizations that should be setup prior to its usage, some examples:\n- [Pub/Sub] subscribe to a topic with authenticated push;\n- [Cloud Scheduler] schedule a job to trigger a Cloud Run service;\n- [Cloud Tasks] queue a task to trigger a Cloud Run service;\n\nIn these cases, `gcp-pilot` tries its best to assure that the required permissions are properly set up\nbefore the actual request is made.\n\n### Integration\n\nSome services can be integrated, and `gcp-pilot` does just that in a seamless way by adding helper methods.\n\nExample: you can subscribe to Google Cloud Build\'s events to be notified by every build step.\n\nBy using `CloudBuild.subscribe`, the `gcp-pilot` creates a subscription (and the topic, if needed) in the Google Pub/Sub service.\n\n## Supported APIs\n\n- IAM\n   - manage service accounts\n   - manage permissions\n- Resource Manager\n   - manage projects\n   - manage permissions\n- Secret Manager\n  - manage secrets\n- Identity Aware Proxy\n   - generate OIDC token\n- Source Repositories\n   - manage repositories\n- Cloud SQL\n   - manage instances\n   - manage databases\n   - manage users\n- Cloud Storage\n   - manage buckets\n   - manage files\n- Cloud Build\n   - manage triggers\n- Cloud Functions\n  - manager functions\n  - manage permissions\n- Cloud Scheduler\n   - manage schedules\n- Cloud Tasks\n   - manage tasks & queues\n- Cloud Run\n   - read services\n   - manage domain mappings [[1]](https://cloud.google.com/run/docs/mapping-custom-domains#adding_verified_domain_owners_to_other_users_or_service_accounts)\n- BigQuery\n   - manage datasets\n   - perform queries\n- Calendar\n   - manage events\n- Google Chats\n   - build complex messages\n   - call webhook\n   - interact as bot\n- Cloud Directory\n   - manage groups\n- Cloud DNS\n   - manage DNS zones\n   - manage zone\'s registers\n- Sheets\n   - manage spreadsheets (powered by gspread)\n- Speech\n   - recognize speech from audio\n- Datastore\n   - Object Mapping ("ORM-ish" management of documents)\n- Monitoring\n  - reporting errors\n  - logging\n',
    'author': 'Joao Daher',
    'author_email': 'joao@daher.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/flamingo-run/gcp-pilot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
