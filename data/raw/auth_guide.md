# CloudSync Authentication Guide

## Logging In

Users log into CloudSync using their email address and password. The platform also
supports SSO (Single Sign-On) for Business and Enterprise plans, with support for
SAML 2.0 and OAuth 2.0 protocols.

## Password Reset

Users can reset their password via the "Forgot password" link on the login page.
Clicking the link sends an email with a reset token that is valid for 30 minutes from
the moment it is generated. After that time, the token expires and a new one must be
generated.

Passwords must meet the following requirements:
- minimum 10 characters
- at least one uppercase letter
- at least one digit
- at least one special character

## API Keys

Each account can generate up to 5 active API keys at a time. Keys are generated in the
Settings > Developer > API Keys panel. Each key can be scoped with permissions:
read-only, read and write, or full administrative access.

API keys must be passed in the `Authorization: Bearer <key>` header. Keys have no
default expiration date, but rotation every 90 days is recommended.

## Two-Factor Authentication (2FA)

2FA is mandatory for all administrator accounts on Business and Enterprise plans.
Supported methods include TOTP apps (Google Authenticator, Authy) and hardware keys
compliant with the FIDO2/WebAuthn standard. SMS is not supported as a 2FA method for
security reasons.

## Sessions

A user session automatically expires after 14 days of inactivity. Enterprise plan
administrators can shorten this window in the security policy management panel, down
to a minimum of 1 hour.