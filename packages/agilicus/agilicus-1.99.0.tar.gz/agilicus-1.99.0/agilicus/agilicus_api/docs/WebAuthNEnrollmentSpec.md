# WebAuthNEnrollmentSpec

The contents of the WebAuthN challenge enrollment.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** | Unique identifier | 
**relying_party_id** | **str** | Unique identifier | 
**attestation_format** | **str** | The format of the attestation statement for this challenge. | [optional] 
**attestation_conveyance** | **str** | The relying parties attestation conveyance preference. | [optional] 
**user_verification** | **str** | A WebAuthn Relying Party may require user verification for some of its operations but not for others, and may use this type to express its needs.  | [optional] [default to 'discouraged']

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


