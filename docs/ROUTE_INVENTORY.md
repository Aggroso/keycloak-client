# Route inventory (v1 selected scope)

Canonical source for v1 scope: `docs/SELECTED_ROUTES_AND_USE_CASES.md` (61 routes).

## Naming conventions (locked for v1)

- Python raw modules: `python/src/keycloak_client/raw/<family>.py` with `snake_case` method names.
- TypeScript raw modules: `typescript/src/raw/<family>.ts` with `camelCase` method names.
- Request/query payloads are typed models (no free-form dictionaries).
- Path parameters are kept in endpoint order in method signatures.

## Coverage summary

- Total selected operations enumerated: **61**

| Family | Operation count |
|---|---:|
| `Authentication and token` | 10 |
| `User CRUD and lifecycle` | 14 |
| `Role management` | 11 |
| `Group management` | 9 |
| `Client management` | 7 |
| `Identity providers` | 6 |
| `Realm config` | 4 |

## Family: `Authentication and token`

| HTTP | Path | Python raw mapping | TypeScript raw mapping | Request model | Response model | Status |
|---|---|---|---|---|---|---|
| `POST` | `/realms/{realm}/protocol/openid-connect/token` | `raw/auth.py::create_oidc_token` | `raw/auth.ts::createOidcToken` | `CreateOidcTokenRequest` | `CreateOidcTokenResponse` | `planned` |
| `POST` | `/realms/{realm}/protocol/openid-connect/logout` | `raw/auth.py::create_oidc_logout` | `raw/auth.ts::createOidcLogout` | `CreateOidcLogoutRequest` | `CreateOidcLogoutResponse` | `planned` |
| `GET` | `/realms/{realm}/protocol/openid-connect/userinfo` | `raw/auth.py::get_oidc_userinfo` | `raw/auth.ts::getOidcUserinfo` | `GetOidcUserinfoRequest` | `GetOidcUserinfoResponse` | `planned` |
| `GET` | `/realms/{realm}/protocol/openid-connect/certs` | `raw/auth.py::get_oidc_certs` | `raw/auth.ts::getOidcCerts` | `GetOidcCertsRequest` | `GetOidcCertsResponse` | `planned` |
| `GET` | `/realms/{realm}/.well-known/openid-configuration` | `raw/auth.py::get_well_known_openid_configuration` | `raw/auth.ts::getWellKnownOpenidConfiguration` | `GetWellKnownOpenidConfigurationRequest` | `GetWellKnownOpenidConfigurationResponse` | `planned` |
| `GET` | `/realms/{realm}/protocol/openid-connect/auth` | `raw/auth.py::get_oidc_auth` | `raw/auth.ts::getOidcAuth` | `GetOidcAuthRequest` | `GetOidcAuthResponse` | `planned` |
| `POST` | `/realms/master/protocol/openid-connect/token` | `raw/auth.py::create_master_protocol_openid_connect_token` | `raw/auth.ts::createMasterProtocolOpenidConnectToken` | `CreateMasterProtocolOpenidConnectTokenRequest` | `CreateMasterProtocolOpenidConnectTokenResponse` | `planned` |
| `POST` | `/admin/realms/{realm}/logout-all` | `raw/auth.py::create_logout_all` | `raw/auth.ts::createLogoutAll` | `CreateLogoutAllRequest` | `CreateLogoutAllResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/client-session-stats` | `raw/auth.py::get_client_session_stats` | `raw/auth.ts::getClientSessionStats` | `GetClientSessionStatsRequest` | `GetClientSessionStatsResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/keys` | `raw/auth.py::get_keys` | `raw/auth.ts::getKeys` | `GetKeysRequest` | `GetKeysResponse` | `planned` |

## Family: `User CRUD and lifecycle`

| HTTP | Path | Python raw mapping | TypeScript raw mapping | Request model | Response model | Status |
|---|---|---|---|---|---|---|
| `GET` | `/admin/realms/{realm}/users` | `raw/users.py::get_users` | `raw/users.ts::getUsers` | `GetUsersRequest` | `GetUsersResponse` | `planned` |
| `POST` | `/admin/realms/{realm}/users` | `raw/users.py::create_users` | `raw/users.ts::createUsers` | `CreateUsersRequest` | `CreateUsersResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/users/{user_id}` | `raw/users.py::get_users_user_id` | `raw/users.ts::getUsersUserId` | `GetUsersUserIdRequest` | `GetUsersUserIdResponse` | `planned` |
| `PUT` | `/admin/realms/{realm}/users/{user_id}` | `raw/users.py::update_users_user_id` | `raw/users.ts::updateUsersUserId` | `UpdateUsersUserIdRequest` | `UpdateUsersUserIdResponse` | `planned` |
| `DELETE` | `/admin/realms/{realm}/users/{user_id}` | `raw/users.py::delete_users_user_id` | `raw/users.ts::deleteUsersUserId` | `DeleteUsersUserIdRequest` | `DeleteUsersUserIdResponse` | `planned` |
| `PUT` | `/admin/realms/{realm}/users/{user_id}/reset-password` | `raw/users.py::update_users_user_id_reset_password` | `raw/users.ts::updateUsersUserIdResetPassword` | `UpdateUsersUserIdResetPasswordRequest` | `UpdateUsersUserIdResetPasswordResponse` | `planned` |
| `PUT` | `/admin/realms/{realm}/users/{user_id}/send-verify-email` | `raw/users.py::update_users_user_id_send_verify_email` | `raw/users.ts::updateUsersUserIdSendVerifyEmail` | `UpdateUsersUserIdSendVerifyEmailRequest` | `UpdateUsersUserIdSendVerifyEmailResponse` | `planned` |
| `PUT` | `/admin/realms/{realm}/users/{user_id}/execute-actions-email` | `raw/users.py::update_users_user_id_execute_actions_email` | `raw/users.ts::updateUsersUserIdExecuteActionsEmail` | `UpdateUsersUserIdExecuteActionsEmailRequest` | `UpdateUsersUserIdExecuteActionsEmailResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/users/{user_id}/credentials` | `raw/users.py::get_users_user_id_credentials` | `raw/users.ts::getUsersUserIdCredentials` | `GetUsersUserIdCredentialsRequest` | `GetUsersUserIdCredentialsResponse` | `planned` |
| `DELETE` | `/admin/realms/{realm}/users/{user_id}/credentials/{credentialId}` | `raw/users.py::delete_users_user_id_credentials_credentialId` | `raw/users.ts::deleteUsersUserIdCredentialsCredentialid` | `DeleteUsersUserIdCredentialsCredentialidRequest` | `DeleteUsersUserIdCredentialsCredentialidResponse` | `planned` |
| `PUT` | `/admin/realms/{realm}/users/{user_id}/disable-credential-types` | `raw/users.py::update_users_user_id_disable_credential_types` | `raw/users.ts::updateUsersUserIdDisableCredentialTypes` | `UpdateUsersUserIdDisableCredentialTypesRequest` | `UpdateUsersUserIdDisableCredentialTypesResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/users/{user_id}/sessions` | `raw/users.py::get_users_user_id_sessions` | `raw/users.ts::getUsersUserIdSessions` | `GetUsersUserIdSessionsRequest` | `GetUsersUserIdSessionsResponse` | `planned` |
| `POST` | `/admin/realms/{realm}/users/{user_id}/logout` | `raw/users.py::create_users_user_id_logout` | `raw/users.ts::createUsersUserIdLogout` | `CreateUsersUserIdLogoutRequest` | `CreateUsersUserIdLogoutResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/users/{user_id}/consents` | `raw/users.py::get_users_user_id_consents` | `raw/users.ts::getUsersUserIdConsents` | `GetUsersUserIdConsentsRequest` | `GetUsersUserIdConsentsResponse` | `planned` |

## Family: `Role management`

| HTTP | Path | Python raw mapping | TypeScript raw mapping | Request model | Response model | Status |
|---|---|---|---|---|---|---|
| `GET` | `/admin/realms/{realm}/roles` | `raw/roles.py::get_roles` | `raw/roles.ts::getRoles` | `GetRolesRequest` | `GetRolesResponse` | `planned` |
| `POST` | `/admin/realms/{realm}/roles` | `raw/roles.py::create_roles` | `raw/roles.ts::createRoles` | `CreateRolesRequest` | `CreateRolesResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/roles/{role_name}` | `raw/roles.py::get_roles_role_name` | `raw/roles.ts::getRolesRoleName` | `GetRolesRoleNameRequest` | `GetRolesRoleNameResponse` | `planned` |
| `PUT` | `/admin/realms/{realm}/roles/{role_name}` | `raw/roles.py::update_roles_role_name` | `raw/roles.ts::updateRolesRoleName` | `UpdateRolesRoleNameRequest` | `UpdateRolesRoleNameResponse` | `planned` |
| `DELETE` | `/admin/realms/{realm}/roles/{role_name}` | `raw/roles.py::delete_roles_role_name` | `raw/roles.ts::deleteRolesRoleName` | `DeleteRolesRoleNameRequest` | `DeleteRolesRoleNameResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/users/{user_id}/role-mappings/realm` | `raw/roles.py::get_users_user_id_role_mappings` | `raw/roles.ts::getUsersUserIdRoleMappings` | `GetUsersUserIdRoleMappingsRequest` | `GetUsersUserIdRoleMappingsResponse` | `planned` |
| `POST` | `/admin/realms/{realm}/users/{user_id}/role-mappings/realm` | `raw/roles.py::create_users_user_id_role_mappings` | `raw/roles.ts::createUsersUserIdRoleMappings` | `CreateUsersUserIdRoleMappingsRequest` | `CreateUsersUserIdRoleMappingsResponse` | `planned` |
| `DELETE` | `/admin/realms/{realm}/users/{user_id}/role-mappings/realm` | `raw/roles.py::delete_users_user_id_role_mappings` | `raw/roles.ts::deleteUsersUserIdRoleMappings` | `DeleteUsersUserIdRoleMappingsRequest` | `DeleteUsersUserIdRoleMappingsResponse` | `planned` |
| `POST` | `/admin/realms/{realm}/groups/{group_id}/role-mappings/realm` | `raw/roles.py::create_groups_group_id_role_mappings` | `raw/roles.ts::createGroupsGroupIdRoleMappings` | `CreateGroupsGroupIdRoleMappingsRequest` | `CreateGroupsGroupIdRoleMappingsResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/groups/{group_id}/role-mappings/realm` | `raw/roles.py::get_groups_group_id_role_mappings` | `raw/roles.ts::getGroupsGroupIdRoleMappings` | `GetGroupsGroupIdRoleMappingsRequest` | `GetGroupsGroupIdRoleMappingsResponse` | `planned` |
| `DELETE` | `/admin/realms/{realm}/groups/{group_id}/role-mappings/realm` | `raw/roles.py::delete_groups_group_id_role_mappings` | `raw/roles.ts::deleteGroupsGroupIdRoleMappings` | `DeleteGroupsGroupIdRoleMappingsRequest` | `DeleteGroupsGroupIdRoleMappingsResponse` | `planned` |

## Family: `Group management`

| HTTP | Path | Python raw mapping | TypeScript raw mapping | Request model | Response model | Status |
|---|---|---|---|---|---|---|
| `GET` | `/admin/realms/{realm}/groups` | `raw/groups.py::get_groups` | `raw/groups.ts::getGroups` | `GetGroupsRequest` | `GetGroupsResponse` | `planned` |
| `POST` | `/admin/realms/{realm}/groups` | `raw/groups.py::create_groups` | `raw/groups.ts::createGroups` | `CreateGroupsRequest` | `CreateGroupsResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/groups/{group_id}` | `raw/groups.py::get_groups_group_id` | `raw/groups.ts::getGroupsGroupId` | `GetGroupsGroupIdRequest` | `GetGroupsGroupIdResponse` | `planned` |
| `PUT` | `/admin/realms/{realm}/groups/{group_id}` | `raw/groups.py::update_groups_group_id` | `raw/groups.ts::updateGroupsGroupId` | `UpdateGroupsGroupIdRequest` | `UpdateGroupsGroupIdResponse` | `planned` |
| `DELETE` | `/admin/realms/{realm}/groups/{group_id}` | `raw/groups.py::delete_groups_group_id` | `raw/groups.ts::deleteGroupsGroupId` | `DeleteGroupsGroupIdRequest` | `DeleteGroupsGroupIdResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/groups/{group_id}/members` | `raw/groups.py::get_groups_group_id_members` | `raw/groups.ts::getGroupsGroupIdMembers` | `GetGroupsGroupIdMembersRequest` | `GetGroupsGroupIdMembersResponse` | `planned` |
| `PUT` | `/admin/realms/{realm}/users/{user_id}/groups/{group_id}` | `raw/groups.py::update_users_user_id_groups_group_id` | `raw/groups.ts::updateUsersUserIdGroupsGroupId` | `UpdateUsersUserIdGroupsGroupIdRequest` | `UpdateUsersUserIdGroupsGroupIdResponse` | `planned` |
| `DELETE` | `/admin/realms/{realm}/users/{user_id}/groups/{group_id}` | `raw/groups.py::delete_users_user_id_groups_group_id` | `raw/groups.ts::deleteUsersUserIdGroupsGroupId` | `DeleteUsersUserIdGroupsGroupIdRequest` | `DeleteUsersUserIdGroupsGroupIdResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/group-by-path/{path}` | `raw/groups.py::get_group_by_path_path` | `raw/groups.ts::getGroupByPathPath` | `GetGroupByPathPathRequest` | `GetGroupByPathPathResponse` | `planned` |

## Family: `Client management`

| HTTP | Path | Python raw mapping | TypeScript raw mapping | Request model | Response model | Status |
|---|---|---|---|---|---|---|
| `GET` | `/admin/realms/{realm}/clients` | `raw/clients.py::get_clients` | `raw/clients.ts::getClients` | `GetClientsRequest` | `GetClientsResponse` | `planned` |
| `POST` | `/admin/realms/{realm}/clients` | `raw/clients.py::create_clients` | `raw/clients.ts::createClients` | `CreateClientsRequest` | `CreateClientsResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/clients/{client_id}` | `raw/clients.py::get_clients_client_id` | `raw/clients.ts::getClientsClientId` | `GetClientsClientIdRequest` | `GetClientsClientIdResponse` | `planned` |
| `PUT` | `/admin/realms/{realm}/clients/{client_id}` | `raw/clients.py::update_clients_client_id` | `raw/clients.ts::updateClientsClientId` | `UpdateClientsClientIdRequest` | `UpdateClientsClientIdResponse` | `planned` |
| `DELETE` | `/admin/realms/{realm}/clients/{client_id}` | `raw/clients.py::delete_clients_client_id` | `raw/clients.ts::deleteClientsClientId` | `DeleteClientsClientIdRequest` | `DeleteClientsClientIdResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/clients/{client_id}/client-secret` | `raw/clients.py::get_clients_client_id_client_secret` | `raw/clients.ts::getClientsClientIdClientSecret` | `GetClientsClientIdClientSecretRequest` | `GetClientsClientIdClientSecretResponse` | `planned` |
| `POST` | `/admin/realms/{realm}/clients/{client_id}/client-secret` | `raw/clients.py::create_clients_client_id_client_secret` | `raw/clients.ts::createClientsClientIdClientSecret` | `CreateClientsClientIdClientSecretRequest` | `CreateClientsClientIdClientSecretResponse` | `planned` |

## Family: `Identity providers`

| HTTP | Path | Python raw mapping | TypeScript raw mapping | Request model | Response model | Status |
|---|---|---|---|---|---|---|
| `GET` | `/admin/realms/{realm}/identity-provider/instances` | `raw/identityProviders.py::get_identity_provider_instances` | `raw/identityProviders.ts::getIdentityProviderInstances` | `GetIdentityProviderInstancesRequest` | `GetIdentityProviderInstancesResponse` | `planned` |
| `POST` | `/admin/realms/{realm}/identity-provider/instances` | `raw/identityProviders.py::create_identity_provider_instances` | `raw/identityProviders.ts::createIdentityProviderInstances` | `CreateIdentityProviderInstancesRequest` | `CreateIdentityProviderInstancesResponse` | `planned` |
| `GET` | `/admin/realms/{realm}/identity-provider/instances/{alias}` | `raw/identityProviders.py::get_identity_provider_instances_alias` | `raw/identityProviders.ts::getIdentityProviderInstancesAlias` | `GetIdentityProviderInstancesAliasRequest` | `GetIdentityProviderInstancesAliasResponse` | `planned` |
| `PUT` | `/admin/realms/{realm}/identity-provider/instances/{alias}` | `raw/identityProviders.py::update_identity_provider_instances_alias` | `raw/identityProviders.ts::updateIdentityProviderInstancesAlias` | `UpdateIdentityProviderInstancesAliasRequest` | `UpdateIdentityProviderInstancesAliasResponse` | `planned` |
| `DELETE` | `/admin/realms/{realm}/identity-provider/instances/{alias}` | `raw/identityProviders.py::delete_identity_provider_instances_alias` | `raw/identityProviders.ts::deleteIdentityProviderInstancesAlias` | `DeleteIdentityProviderInstancesAliasRequest` | `DeleteIdentityProviderInstancesAliasResponse` | `planned` |
| `POST` | `/admin/realms/{realm}/identity-provider/import-config` | `raw/identityProviders.py::create_identity_provider_import_config` | `raw/identityProviders.ts::createIdentityProviderImportConfig` | `CreateIdentityProviderImportConfigRequest` | `CreateIdentityProviderImportConfigResponse` | `planned` |

## Family: `Realm config`

| HTTP | Path | Python raw mapping | TypeScript raw mapping | Request model | Response model | Status |
|---|---|---|---|---|---|---|
| `GET` | `/admin/realms` | `raw/realms.py::get` | `raw/realms.ts::get` | `GetRequest` | `GetResponse` | `planned` |
| `POST` | `/admin/realms` | `raw/realms.py::create` | `raw/realms.ts::create` | `CreateRequest` | `CreateResponse` | `planned` |
| `GET` | `/admin/realms/{realm}` | `raw/realms.py::get_2` | `raw/realms.ts::get2` | `Get2Request` | `Get2Response` | `planned` |
| `PUT` | `/admin/realms/{realm}` | `raw/realms.py::update` | `raw/realms.ts::update` | `UpdateRequest` | `UpdateResponse` | `planned` |

## Validation results

- Mapped operations: `61` / `61` expected.
- Python mapping exists for every operation: `yes`.
- TypeScript mapping exists for every operation: `yes`.
- Duplicate method names within a family: `none` after deterministic suffixing.
