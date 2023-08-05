# AgentConnectorStatus

Status information pertaining to a Connector. Note that stats will only be returned if explicitly requested. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**application_services** | [**list[ApplicationService]**](ApplicationService.md) | The list of application services associated with this agent | [optional] 
**service_account_id** | **str** | Service account user GUID used to deploy the connector | [optional] 
**info** | [**AgentConnectorInfo**](AgentConnectorInfo.md) |  | [optional] 
**stats** | [**AgentConnectorStats**](AgentConnectorStats.md) |  | [optional] 
**local_authentication** | [**AgentLocalAuthInfo**](AgentLocalAuthInfo.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


