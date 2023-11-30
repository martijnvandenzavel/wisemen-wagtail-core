# Wisemen Wagtail Core

An installable wrapper around Wagtail with sensible defaults, most used packages and in-house developed tools.

After setting up your repository and initialising both your Virtualenv and your Poetry project, install via:

```shell
poetry add git+https://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@github.com/Timusan/wisemen-wagtail-core.git@<desired-version-tag>
```

Then initialize your site with:

```shell
wisemen start <your_site_name>
```

And follow the onscreen instructions.

## Forked packages

The core uses some forked versions of Django/Wagtail packages due to implementation details or slow upstream update cycles.

- **Wagtail Orderable** (https://github.com/elton2048/wagtail-orderable) forked on https://github.com/Timusan/wagtail-orderable
-> Fixed JS issues as mentioned in https://github.com/elton2048/wagtail-orderable/issues/48
- **Wagtail Localize** (https://github.com/wagtail/wagtail-localize/) forked on https://github.com/Timusan/wagtail-localize
-> Removed sync button to mitigate sync translation restart as mentioned in https://github.com/wagtail/wagtail-localize/issues/607
- **Wagtail Columnblocks** (https://github.com/squareweave/wagtailcolumnblocks) forked on https://github.com/Timusan/wagtailcolumnblocks
-> Making compatible with Wagtail 4 and 5
-> **We should abandon this package!**
- **Wagtail SEO** (https://github.com/coderedcorp/wagtail-seo) forked on https://github.com/Timusan/wagtail-seo
-> Allow for Wagtail 5
- **Wagtail Video** (https://github.com/neon-jungle/wagtailvideos) forked on https://github.com/Timusan/wagtailvideos
-> Allow for transcoding to Boto3 (S3) storage


### Wisemen Django **mandatory** settings

#### Core specific

- `WISEMEN_HOMEPAGE_MODEL` - The homepage model to use, defined in the following format: `app_label.model_name`
- `PRERENDERED_IMAGE_RENDITIONS` - A list of Wagtail renditions strings that should be generated on each additiopn or alteration of an Image 

#### Others

- `DEBUG`: Debug mode, `True` or `False`
- `DEBUG_PROPAGATE_EXCEPTIONS`: Propagate exceptions, `True` or `False`
- `SECRET_KEY`: Generated secret key used as encryption based for JWT tokens, cookies, ...
- `ALLOWED_HOSTS`: List of allowed hosts, space separated
- `FILE_CACHE_LOCATION`: Location of the file cache, default: `/tmp`
- `PROJECT_DIR`: Location of the actual project directory inside the app on disk, containing your settings files, URL file, ea (used for static file dump, etc)
- `WAGTAILADMIN_BASE_URL`: Base URL of the Wagtail admin, default: `admin`
- `AWS_ACCESS_KEY_ID`: AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: AWS secret access key
- `AWS_STORAGE_BUCKET_NAME`: AWS storage bucket name
- `AWS_S3_PRIVATE_STORAGE_BASE`: AWS S3 private storage base (eg. `private`)
- `AWS_S3_PUBLIC_STORAGE_BASE`: AWS S3 public storage base (eg. `public`)
- `AWS_PROVIDER`: AWS provider, `scw` or `do`
- `AWS_S3_REGION_NAME`: AWS region name, eg. `ams1` (for DigitalOcean) or `nl-ams` (for Scaleway)
- `AWS_S3_ENDPOINT_URL`: AWS endpoint URL, eg. `https://<bucket-name>.ams1.digitaloceanspaces.com` (for DigitalOcean) or `https://s3.nl-ams.scw.cloud` (for Scaleway)
- `CORS_ALLOWED_ORIGINS`: List of allowed origins for CORS, space separated
- `DATABASE_NAME`: PostgreSQL database name
- `DATABASE_USER`: PostgreSQL database user
- `DATABASE_PASSWORD`: PostgreSQL database password
- `DATABASE_HOST`: PostgreSQL database host
- `DATABASE_PORT`: PostgreSQL database port
- `SITE_MODULE_NAME`: Django site module to use
- `EMAIL_BACKEND`: The preferred email backend to use, eg. `django.core.mail.backends.smtp.EmailBackend`, see Email handling for more information
- `REDIS_QUEUE`: Redis queue to use, eg. `default`
- `REDIS_HOST`: Redis host to use, eg. `localhost`
- `REDIS_PORT`: Redis port to use, eg. `6379`
- `REDIS_DB`: Redis database to use, eg. `0`
- `WS_PROTOCOL`: The websocket protocol to use, `ws` or `wss`

### Wisemen Django **optional** settings:

n/a

### Authentication

Authentication is handled by Django Allauth in tandem with Django Rest Framework SimpleJWT.
A custom Allauth AccountAdaptor is provided to allow for async email flow and different templating.
Session determination is done by the Allauth set access and refresh cookies.

### Middleware

- `wisemen.middleware.DisableCSRFMiddleware` - disables CSRF protection for all requests. Useful for API endpoints.

### Storage backends

- `wisemen.storage_backends.PrivateMediaStorage` - private media storage backend, which requires authentication to access files.

### Rest Framework

The Django REST Framework is configured to use the following settings:
- JWT authentication with blacklisting refresh tokens and a grace period on them (see Rest Framework SimpleJWT with Grace Period app below)
- Password reset flow provided by the `django_rest_passwordreset` package
- Default pagination of 10 items per page

### Email handling

Email can be sent using the `wisemen.mail.send_mail` function.
One backend is provided:
- `wisemen.email_backends.MailGunBackend` - sends emails using Mailgun's API. Requires the following settings:
  - `MAILGUN_API_PATH`: Mailgun domain
  - `MAILGUN_API_KEY`: Mailgun API key

When using MailTrap for sandboxed email testing, Django's default SMTP email backend (`django.core.mail.backends.smtp.EmailBackend`) can be used.
Since this is an SMTP backend, you can simply configure it using the `EMAIL_*` settings:
- `EMAIL_HOST`: `smtp.mailtrap.io`
- `EMAIL_PORT`: `2525`
- `EMAIL_HOST_USER`: MailTrap username
- `EMAIL_HOST_PASSWORD`: MailTrap password
- `EMAIL_USE_TLS`: `True`

### Serializers

There are a handful of serializers provided for use with the Django REST Framework:

- `wisemen.serializers.ImageSerializer`: serializes Wagtail images including an optional rendition.

### Signals

- `image_renditions`: A signal triggering when saving a new image. It will pre-generate all renditions for the image using a background task. 

### Panels

- `seo`: A panel which can be added to Page models and provides the default SEO fields as well as a choice to disable the slug field.

### Fields

- `ChoiceArrayField`: A field which uses PostgreSQL's native array field to store a list of choices.

### Included apps

Besides helpers and other utilities, Wisemen Django also includes a few apps.

#### Rest Framework SimpleJWT with Grace Period

This is an app that adds a configurable grace period to a refresh token.
Once such a token is blacklisted (on first use), it will still be usable for the set grace period.
After that, the token will be permanently added to the blacklist.

#### Redirect

This app provides an API URL to be used to consult if a given URL has a redirect configured.
Redirects can be configured using Wagtail's admin interface.

#### Multilingual Sitemap

Will take over the functionality of the default sitemap and add in all available languages.

## Contributing

If you would like to contribute to this project to add updates or new features, please follow the following steps:

1. Clone this repository
2. Create a virtual environment: `python3.11 -m venv venv`
3. Install the development packages: `pip install -r requirements-dev.txt`
4. Install the test project: `wisemen testproject` - Be sure to **not** change the name, as `testproject` is ignored by Git.
5. Go into your `testproject` directory
6. Make sure you have a database called `testproject` in your PostgreSQL install
7. Enable the `.envrc` environment
8. Run the migrations: `python manage.py migrate`

Optionally you can also create a superuser and run the server.
You are now ready to make changes to the models in the `wisemen` app and test them in the `testproject` app.
Since the Wisemen core is installed in editable mode, any migrations done in the `testproject` of the `wisemen` package will end up in the original `wisemen` directory and are ready to be build and committed.
So after making changes to existing models or adding new ones, you can simply run `./manage.py makemigrations wisemen` from the `testproject` directory.
The migrations will be created in the `wisemen` directory and can be committed from there.