# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

Changes for the upcoming release can be found in the `changelog.d` directory in
this repository.

Do **NOT** add changelog entries here! This changelog is managed by
[towncrier](https://github.com/hawkowl/towncrier) and is compiled at release
time.

.. towncrier release notes start

1.18.0 (2021-03-18)
====================

Features
--------

- Apply 'blacklist' to any token from the same line of refreshed tokens as any invalidated token, where token ids are available.
  Avoid storing whole auth tokens when JWT_TOKEN_ID setting is set to 'require'.
  Please see notes in docs on migrating from JWT_TOKEN_ID 'allow' (the default) to 'require' (recommended). ([#84](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/84))


1.17.3 (2020-12-14)
====================

Bugfixes
--------

- Improve error handling for tokens with an unrecognized key identifier (`kid`). ([#78](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/78))
- Fixed JWT creation status codes from 200 to 201 ([#80](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/80))


Misc
----

- Add obtain_token management command ([#62](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/62))


1.17.2 (2020-09-20)
====================

Features
--------

- If the authentication header cant be parsed, fall back to
  cookies or allow other handlers. ([#71](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/71))


1.17.1 (2020-08-25)
====================

Bugfixes
--------

- Improve error handling for invalid tokens. ([#77](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/77))


1.17.0 (2020-08-14)
====================

Features
--------

- Default to including a token ID claim (`jti`) in all tokens.
  For tokens resulting from refresh, also include the token ID of the original token in the chain of refreshes as `orig_jti`. ([#69](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/69))


Improved Documentation
----------------------

- Add explanation for blacklisting feature to the documentation. ([#61](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/61))
- When the Authorization header is sent with a different prefix other than default it raises error. 
  It should return None and continue toward the other authentication middleware. ([#65](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/65))
- Added a section about protecting views properly using the appropriate decorator for function based view and variable for class based views. ([#67](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/67))


1.16.2 (2020-06-26)
====================

Bugfixes
--------

- Allow use without blacklist app being installed. ([#51](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/51))
- Fix Python 2 regression in model translations not being unicode
  aware, and use lazy gettext in the models so they can be imported
  before the translation system has been is initialised. ([#54](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/54))
- Use `got_or_create` on blacklist token creation instead of a database
  uniqueness on the token parameter to make blacklist functionality work
  on MySQL. ([#58](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/58))


1.16.1 (2020-04-30)
====================

Features
--------

- Use DRF's JSON encoder for JWT tokens, to allow for encoding e.g. users that have UUID primary keys. ([#50](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/50))


Bugfixes
--------

- Run `mkdocs` with Python 3.6 until it [adds support for newer versions of Python](https://github.com/mkdocs/mkdocs/issues/1531). ([#49](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/49))


1.16.0 (2020-04-23)
====================

Features
--------

- * Support multiple algorithms and keys

    Existing code made key rollovers or algorithm changes hard and
    basically required a breaking change: Once any of `JWT_ALGORITHM`,
    `JWT_SECRET_KEY`, or `JWT_PRIVATE_KEY`/`JWT_PUBLIC_KEY` were
    changed, existing tokens were rendered invalid.

    We now support `JWT_ALGORITHM`, `JWT_SECRET_KEY`, and
    `JWT_PUBLIC_KEY` optionally being a list, where all members are
    accepted as valid.

    When `JWT_SECRET_KEY` is a list, the first member is used for
    signing and all others are accepted for verification.

  * Support multiple keys with key ids

    We also support identifing keys by key id (`kid` header): When a JWT
    carries a key id, we can identify immediately if it is known and
    only need to make at most one verification attempt.

    To configure keys with ids, `JWT_SECRET_KEY`, `JWT_PRIVATE_KEY` and
    `JWT_PUBLIC_KEY` can now also be a dict in the form

    ```
    { "kid1": key1, "kid2": key2, ... }
    ```

    When a JWT does not carry a key id (`kid` header), the default is to
    fall back to trying all keys if keys are named (defined as a dict).
    Setting `JWT_INSIST_ON_KID: True` avoids this fallback and requires
    any JWT to be validated to carry a key id _if_ key IDs are used

    *NOTE: For python < 3.7, use a `collections.OrderedDict` object
    instead of a dict*

  * Require cryptographic dependencies of PyJWT

    We changed the PyJWT requirement to include support for RSA by
    default. This was done to improve the user experience, but will lead
    to cryptography support be installed where not already present.

    See: https://pyjwt.readthedocs.io/en/latest/installation.html#cryptographic-dependencies-optional ([#33](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/33))


Bugfixes
--------

- Fix deprecation warnings in Django 3 caused by imports of `ugettext` and `force_text`. ([#45](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/45))
- Remove the tests that reload the settings module.
  For some reason, `pytest`'s `monkeypatch` was failing to mock settings
  when executed after these tests. Since these tests tested runtime
  behavior that would have been caught by users on startup anyway,
  it's easier to remove them than fix them. ([#48](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/48))


Misc
----

- Add the manual deploy stage until te Travis build is fixed ([#48](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/48))


1.15.2 (2020-03-30)
====================

Bugfixes
--------

- Added new encrypted PyPI API token for travis deployment. ([#39](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/39))
- Fixed issues when the `JWT_GET_USER_SECRET_KEY` method is overridden,
  * If the payload contains a non-existent user, a validation error will be raised (same as when the method is not overridden).
  * The `jwt_get_secret_key` will now use the `JWT_PAYLOAD_GET_USERNAME_HANDLER` configuration. ([#41](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/41))


1.15.1 (2020-03-12)
====================

Bugfixes
--------

- Added check in authentication if blacklist app is installed before checking if any Blacklisted tokens exist ([#35](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/35))
- Security: Disallow refresh token for blacklisted tokens. ([#37](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/37))


1.15.0 (2020-02-19)
====================

Features
--------

- Blacklisting allows the user to blacklist his own token. ([#27](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/27))


Deprecations and Removals
-------------------------

- Drop support for Python 3.3 and 3.4 ([#27](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/27))


Misc
----

- changed occurrences of `smart_text` to `smart_str` since it was deprecated in Django 3.X ([#28](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/28))


1.14.0 (2020-01-29)
====================

Features
--------

- Impersonation allows the service to perform actions on the client’s behalf. A typical use case would be troubleshooting. We can act like the user who submitted an issue without requiring its login credentials. ([#26](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/26))
- added `JWT_AUTH_COOKIE_*` settings paralleling Django's
  `SESSION_COOKIE_*` which are used for `JWT_AUTH_COOKIE` and
  `JWT_IMPERSONATION_COOKIE`

  This changes the default `Secure` attribute from `False` to
  `True`. Users wishing to use JWT cookies over http (as in no TLS/SSL)
  need to set `JWT_AUTH_COOKIE_SECURE` to `False.`

  This change is intentional to follow common best common practice.

  With Django versions >= 2.1.0, the `Samesite` attribute is set to
  `Lax` by default. ([#29](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/29))


Improved Documentation
----------------------

- Document compatibility with Python 3.7. ([#23](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/23))
- Add support for Django 3.0, Python 3.8 and `djangorestframework` 3.11 ([#24](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/24))


Misc
----

- * Run the test suite against the `demo` project. The same project can be used for local development as well.
  * Add the `serve` environment to `tox` that starts the `demo` project's development server. To use it, run: `$ tox -e serve` ([#24](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/24))


1.13.4 (2019-12-13)
====================

Bugfixes
--------

- Remove serialization on response data in `BaseJSONWebTokenAPIView` because it 
  breaks custom response payload handlers which add extra data to the response 
  payload. This change aligns this fork more closely with the original and makes 
  it easier to use this fork as a drop-in replacement for the original. Also 
  change the ReponsePayload from a `namedtuple` to a dictionary because 
  `namedtuple` is not JSON serializable ([#22](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/22))


1.13.3 (2019-10-17)
====================

Features
--------

- - Added support for djangorestframework 3.10 ([#18](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/18))
- Allow control of setting the `user_id` in the payload with `JWT_PAYLOAD_INCLUDE_USER_ID`. ([#20](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/20))


1.13.2 (2019-08-26)
====================

Bugfixes
--------

- Use pk to get profile's id in `rest_framework_jwt.utils.jwt_create_payload`. ([#15](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/15))


1.13.1 (2019-08-23)
====================

Bugfixes
--------

- Pass `request` to `django.contrib.auth.authenticate`. ([#14](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/14))


1.13.0 (2019-04-23)
=====================

Features
--------

- Added `on_delete` to `tests.models.UserProfile.user` required by Django 2.2,
  and added Django 2.x, Python 3.7 and djangorestframework 3.9 to the support matrix. ([#9](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/9))


1.12.10 (2018-12-21)
====================

No significant changes.


1.12.9 (2018-12-21)
====================

Misc
----

- Fixed inconsistent View names. ([#7](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/7))


1.12.8 (2018-12-21)
====================

Misc
----

- Updated docs. Drop support for Django < 1.8 and DRF < 3.7.x. ([#6](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/6))


1.12.7 (2018-12-17)
====================

Misc
----

- Switch to Travis CI build stages ([#3](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/3))


1.12.3 (2018-12-13)
====================

Misc
----

- Project restructuring according to SDS code style and conventions. ([#2](https://github.com/Styria-Digital/django-rest-framework-jwt/pull/2))
