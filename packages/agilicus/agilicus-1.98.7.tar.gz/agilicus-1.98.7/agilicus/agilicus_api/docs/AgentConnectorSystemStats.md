# AgentConnectorSystemStats

Information about the AgentConnector itself, as well as the system on which it runs. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**os_version** | **str** | The version of the operating system on which the AgentConnector is running. | 
**os_uptime** | **int** | The length of time, in seconds, the operating system has been running. | 
**agent_uptime** | **int** | The length of time, in seconds, the AgentConnector has been running. If the AgentConnector restarts, this value will reset to zero.  | 
**agent_version** | **str** | The version of software currently running for this AgentConnector. This includes both the version number and the commit reference from which it was built.  | 
**agent_release_train** | **str** | The release train followed by the AgentConnector. It uses this when checking for updates to determine which version of the AgentConnector should be installed.  | [optional] 
**agent_connector_id** | **str** | The identifier of the AgentConnector publishing these statistics. The AgentConnector publishes this information in order to ensure that an AgentConnector does not accidentally publish to the wrong endpoint.  | 
**agent_connector_org_id** | **str** | The organisation identifier of the AgentConnector publishing these statistics. The AgentConnector publishes this information in order to ensure that an AgentConnector does not accidentally publish to the wrong endpoint.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


