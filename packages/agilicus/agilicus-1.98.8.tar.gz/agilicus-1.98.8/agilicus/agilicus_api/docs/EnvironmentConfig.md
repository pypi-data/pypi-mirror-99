# EnvironmentConfig

Environment config's properties
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier | [optional] [readonly] 
**app_id** | **str** | Unique identifier | [optional] [readonly] 
**environment_name** | **str** | Unique identifier | [optional] [readonly] 
**maintenance_org_id** | **str** | The Organisation which is responsibile for maintaining this Environment.  | 
**config_type** | **str** | configuration type | 
**mount_domain** | **str** | mount user domain | [optional] 
**mount_username** | **str** | mount username | [optional] 
**mount_password** | **str** | mount password | [optional] 
**mount_hostname** | **str** | mount hostname | [optional] 
**mount_share** | **str** | mount share | [optional] 
**mount_src_path** | **str** | source mount path | [optional] 
**mount_path** | **str** | destination mount path | [optional] 
**file_store_uri** | **str** | files API URI where configuration is located | [optional] 
**env_config_vars** | [**list[EnvironmentConfigVar]**](EnvironmentConfigVar.md) | It stores an array of env_config_var objects(key &amp; value pairs) in API. It provides environment variables to build configmaps and secrets directly.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


