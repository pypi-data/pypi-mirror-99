# Policy

A policy describes how to evaluate a set of conditions in order to enforce a set of actions. A policy engine is the component that evaluates the set of policy rules and a set of input that determines the outcome. Each policy rule is evaluated in priority order. If all the conditions in the policy rule evaluate to `true` the rule's action is taken, otherwise the next policy rule is evaluated. If none of the policy rules evaluate to `true` then the policy's `default_action` is taken. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**MetadataWithId**](MetadataWithId.md) |  | [optional] 
**spec** | [**PolicySpec**](PolicySpec.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


