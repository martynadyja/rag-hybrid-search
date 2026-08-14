# CloudSync API Limits

## Rate Limiting by Plan

| Plan       | Request limit           |
|------------|--------------------------|
| Free       | No API access            |
| Pro        | 60 requests/minute       |
| Business   | 600 requests/minute      |
| Enterprise | 10000 requests/minute    |

When the limit is exceeded, the API returns a `429 Too Many Requests` error code along
with a `Retry-After` header indicating the number of seconds until the limit resets.

## Request Size Limits

The maximum size of a single file upload via the API is 5 GB for the Pro plan and
50 GB for Business and Enterprise plans. Files larger than the limit must be split into
parts (chunked upload) using the `/v1/uploads/multipart` endpoint.

## Webhooks

Business and Enterprise plan accounts can subscribe to webhooks for events such as
`file.created`, `file.updated`, `file.deleted`, and `user.invited`. Webhooks are sent
with up to 3 retry attempts in case of failure, at intervals of 30, 60, and 120 seconds.

## API Versioning

The current API version is `v1`. Versions are maintained for a minimum of 18 months
after the release of the next major version.