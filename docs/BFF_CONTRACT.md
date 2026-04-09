# BFF Contract (Compatibility Module)

This document defines the Python BFF compatibility facade contract.

## Methods
- `build_login_url(request)`
- `complete_login(request)`
- `refresh_session(request)`
- `logout(request)`
- `user_info(request)`

## Token response mapping
| OIDC field | BFF result field |
|-----------|------------------|
| `access_token` | `access_token` |
| `refresh_token` | `refresh_token` |
| `expires_in` | `expires_in` |
| `id_token` | `id_token` |
| `token_type` | `token_type` |
| `scope` | `scope` |

## Security notes
- Backend-only module.
- Redaction-safe logging/observability required.
- Correlation id is included in all responses.
