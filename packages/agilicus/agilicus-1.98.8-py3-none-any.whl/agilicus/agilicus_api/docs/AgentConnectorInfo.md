# AgentConnectorInfo

Information pertaining to a Connector
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**local_authentication_enabled** | **bool** | Determines whether or not the agent will expose an endpoint for local authentication | [optional] 
**connections_info** | [**list[AgentConnectorConnectionInfo]**](AgentConnectorConnectionInfo.md) | The list of connections associated with this agent | [optional] 
**allow_list** | [**AllowMapCompiled**](AllowMapCompiled.md) |  | [optional] 
**authz_public_key** | **str** | The PEM encoded public key used for validating bearer tokens | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


