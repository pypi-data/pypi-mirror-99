# UserFileShareAccessInfoStatus

The read-only details of a UserFileShareAcessInfo.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** | The unique id of the User to which this record applies.  | 
**org_id** | **str** | The unique id of the Organisation to which this record applies.  | 
**org_name** | **str** | The name of Organisation to which this record applies.  | 
**parent_org_id** | **str** | The unique id of the parent of the Organisation to which this record applies. Omitted if the Organisation has no parent.  | [optional] 
**parent_org_name** | **str** | The name of the parent of the Organisation to which this record applies. Omitted if the Organisation has no parent.  | [optional] 
**share_id** | **str** | Unique identifier | [readonly] 
**share_name** | **str** | The file share name.  | 
**share_url** | **str** | The url of the share  | 
**access_level** | **str** | Whether the user has access, has requested access, etc. The possible values have the following meanings:   - requested: the user has requested access to this instance.   - granted: the user has access to this instance.   - none: the user has no relation to this application.  | 
**roles** | **list[str]** | The list of roles held by the user for the given share | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


