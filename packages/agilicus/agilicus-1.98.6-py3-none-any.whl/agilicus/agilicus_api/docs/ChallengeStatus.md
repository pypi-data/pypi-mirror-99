# ChallengeStatus

The status of an authentication challenge. This will provide information about its state, statistics and so on. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**state** | **str** | The current state of the challenge. The challenge may be in the following states:   - pending: waiting to issue the challenge.   - challenge_failed: the system failed to issue the challenge. This could be because there is     no mechanism to do so, communication with the device failed, and so on.   - issued: the challenge has been issued. The system is waiting for a response.   - challenge_passed: the user passed the challenge, typically by accepting a notification.   - challenge_declined: the user declined to accept the challenge. The challenge is no longer valid.   - timed_out: the challenge has timed out. The user can no longer use an answer to it to prove their     possession of a second factor.  | [optional] 
**public_challenge** | **str** | An opaque string used as the public challenge. Currently this is only used when the challenge type is webauthn. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


