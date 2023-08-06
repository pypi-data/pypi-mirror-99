# OIDCAuthConfig

The OIDC configuration for authentication with OIDC connector.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auth_enabled** | **bool** | Whether the authentication is enabled. If true, users will be forced to log in before accessing any of its assets. If false, no authentication will be performed.  | 
**client_id** | **str** | The OIDC client identifier to use when logging in with this application. | 
**issuer** | **str** | The url of the OpenID Connect issuer. | 
**logout_url** | **str** | The relative http path to the logout page. | [optional] 
**scopes** | [**list[OIDCProxyScope]**](OIDCProxyScope.md) | A list of scopes to be requested on behalf of the user of the application. | [optional] 
**path_config** | [**OIDCAuthPathConfig**](OIDCAuthPathConfig.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


