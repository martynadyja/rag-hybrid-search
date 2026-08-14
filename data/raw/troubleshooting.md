# CloudSync Troubleshooting

## Files Are Not Syncing

If files are not syncing, check the following in order:
1. Whether the desktop app is running (icon in the system tray)
2. Whether there is an internet connection
3. Whether the storage limit for the current plan has been exceeded
4. Whether the file name contains disallowed characters: `< > : " / \ | ? *`

## 401 Unauthorized Error on API Calls

A `401 Unauthorized` error most commonly means an expired or invalid API key. Check
that the key is being passed in the `Authorization: Bearer <key>` header without extra
spaces or characters. If the key has been revoked in the panel, generate a new one.

## File Version Conflict

When the same file is modified on two devices at the same time without an internet
connection, CloudSync creates two versions of the file at the next sync: the original
and a copy with the suffix `(conflict - device name)`. The user must manually merge the
changes.

## Slow Syncing of Large Files

For files larger than 1 GB, it is recommended to enable delta sync in
Settings > Advanced > Delta Sync. This feature only transfers the changed portions of
a file instead of uploading the entire file again.