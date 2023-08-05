# AgentConnectorTransportStats

Statistics related to the transfer of data through the AgentConnector. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active_connections** | **int** | The number of currently active connections.  | 
**target_number_connections** | **int** | The number of connections which should be in an active state. Note that this may be less than active_connections if the AgentConnector is currently applying configuration changes. It may be more than active_connections if there is a connectivity issue, or connections are first starting.  | 
**connection_start_count** | **int** | The number of times connections have been started  | 
**connection_stop_count** | **int** | The number of times connections have stopped  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


