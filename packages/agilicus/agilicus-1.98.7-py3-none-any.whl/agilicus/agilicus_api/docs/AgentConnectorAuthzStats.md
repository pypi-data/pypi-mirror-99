# AgentConnectorAuthzStats

Statistics related to the authorization of requests through the AgentConnector. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed** | **int** | The number of allowed requests.  | 
**allowed_app_handled** | **int** | The authz has been allowed due to the authentication handled by the application.  | 
**denied** | **int** | The number of denied requests.  | 
**token_cached_failed** | **int** | The number of times a failed lookup response was returned that had been cached.  | 
**token_cached_success** | **int** | The number of times a successful lookup response was returned that had been cached.  | 
**token_parse_failed** | **int** | The number of times a there was a failure parsing the token. This is due to missing claims in the token.  | 
**token_static_token** | **int** | The number of times a static token was used in a request.  | 
**token_bad_jti** | **int** | The number of times the token JTI was missing.  | 
**token_lookup_success** | **int** | The number of times a token introspect was performed and the result was success.  | 
**token_lookup_notfound** | **int** | The number of times a token introspect was performed and the result was not found.  | 
**token_lookup_badrequest** | **int** | The number of times a token introspect was performed and the result was a bad request  | 
**token_lookup_4xx_other** | **int** | The number of times a token introspect was performed and the result was a 4xx result that was not a 404, 410 or 400.  | 
**token_lookup_error** | **int** | The number of times a token introspect was performed and the result was an error.  | 
**token_lookup_revoked** | **int** | The number of times a token introspect was performed and the result returned was that the token has been revoked.  | 
**token_basic_auth_decode_fail** | **int** | The number of times a request was made with basic auth and the base64 decode failed.  | 
**token_basic_auth_too_long** | **int** | The number of times a request was made with basic auth and the basic auth string was too long. The maximum size permitted is 141 characters.  | 
**token_basic_auth_no_password** | **int** | The number of times a request was made with basic auth and the password was missing.  | 
**token_basic_auth_cached_success** | **int** | The number of times a request was made with basic auth and the successful result was returned from the cache.  | 
**token_basic_auth_cached_failed** | **int** | The number of times a request was made with basic auth and the failed result was returned from the cache.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


