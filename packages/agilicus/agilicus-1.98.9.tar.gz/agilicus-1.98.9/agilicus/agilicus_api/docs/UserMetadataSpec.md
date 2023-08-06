# UserMetadataSpec

A generic data entry for a given user. The entry is tied to specific org, application or combination. The entries type describes how to interpret the value. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** | The unique id of the User to which this record applies.  | 
**org_id** | **str** | The unique id of the Organisation to which this record applies.  | [optional] 
**app_id** | **str** | The unique id of the application to which this record applies.  | [optional] 
**name** | **str** | A descriptive name for this metadata entry | [optional] 
**data_type** | **str** | The type of data present in the configuration. This informs consumers of how to use the data present | [optional] 
**data** | **str** | The string representation of the data. This value is interpretted differently based on the data_type | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


