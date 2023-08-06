# UserStatusEnum

The status of the user within the organisation. The status of a user within the organisation controls their visibility, as well as their access to various components of the system. Changing the status will change how the user interacts with the organisation and its applications. The status values have the following meanings:   * `active`: The user is a full member of the organisation. They will appear by default     in queries for the organisation's members. They will be able to log in and access     any applications for which they have permission.   * `pending`: The user has requested access to the organisation. They are waiting for     full membership to be granted by an administrator. A pending user will not show     by default in queries for the organisation's members. They can log in to view     their profile and request access to applications. A pending user can log in and     access any application to which they have been granted access. Note: this will     likely change in the future.   * `disabled`: A disabled user will not show by default in queries for the organisation's members.     The user will not be able to log in. The user will not be able to access applications, even if     they previously had access when they were not disabled. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


