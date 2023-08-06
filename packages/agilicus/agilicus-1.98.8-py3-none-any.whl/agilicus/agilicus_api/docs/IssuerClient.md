# IssuerClient

Object describing the properties of an IssuerClient
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier | [optional] [readonly] 
**issuer_id** | **str** | Unique identifier | [optional] [readonly] 
**name** | **str** | issuer client id | 
**secret** | **str** | issuer client secret | [optional] 
**application** | **str** | application associated with client | [optional] 
**org_id** | **str** | org_id associated with client | [optional] 
**restricted_organisations** | **list[str]** | List of organisation IDs which are allowed to authenticate using this client. If a user is not a member of one of these organisations, their authentication attempt will be denied. Note that this list intersects with &#x60;organisation_scope&#x60;. For example, if &#x60;organisation_scope&#x60; is &#x60;here-and-down&#x60; and this list contains two organisations below the current organisation, only those two will be allowed, despite there potentially being more sub organisations. If the list is empty, no restrictions are applied by this field. Note that other restrictions may be applied, such as by &#x60;organisation_scope&#x60;.  | [optional] 
**saml_metadata_file** | **str** | The Service Provider&#39;s metadata file required for the SAML protocol.  | [optional] 
**organisation_scope** | **str** | How to limit which organisations are allowed to authenticate using this client. Note that this interacts with &#x60;restricted_organisations&#x60;: that list, if not empty, further limits the allowed organisations. * &#x60;any&#x60; indicates that there are no restrictions. All organisations served by   the issuer will be allowed to log in using this client. * &#x60;here-only&#x60; indicates that   only the organisation referenced by &#x60;org_id&#x60; may be used. * &#x60;here-and-down&#x60; indicates that the organisation referenced by &#x60;org_id&#x60;   and its children may be used.  | [optional] [default to 'here_only']
**redirects** | **list[str]** | List of redirect uris | [optional] 
**mfa_challenge** | **str** | When to present an mfa challenge to a user upon login. If the system determines that an MFA challenge is required, and the user does not yet have a authenticatin mechanism valid for this login session, the user will be presented with the option to enrol a new mechanism. * &#x60;always&#x60; means that the user will always be required to validate against a second factor. * &#x60;user_preference&#x60; means that the whether the user is required to validate depends on the user&#39;s preferences.   A user could choose to always require MFA for their logins, or they could decide not to. Note that in this case,   other policy could override the preference to force the user to authenticate with MFA even if the user indicated   that they prefer not to. * &#x60;trust_upstream&#x60; means to always perform MFA, but that the upstream IDP will be trusted to have performed MFA if    the upstream indicates that it has done so. Otherwise, MFA will be performed by the system after the upstream    returns the to Issuer.  | [optional] [default to 'user_preference']
**single_sign_on** | **str** | Whether a client is allowed to use single sign-on * &#x60;user_preference&#x60; means that the user will have the option to &#39;remember&#39; their upstream identity selection for single sign-on. * &#x60;never&#x60; means that the given client will not allow single sign-on. The user will be required to present credentials for each login to applications with this client id.  | [optional] [default to 'never']
**attributes** | [**list[AuthenticationAttribute]**](AuthenticationAttribute.md) | A list of attributes to derive from information about the user. The user&#39;s information returned to the relying party making a request using this client will be extended with these attributes. Only one attribute for a given &#x60;attribute_name&#x60; can exist per-client at a time. Add an attribute to this list when the default attributes do not provide sufficient information for the client application, or for when the client application expects the attributes to be named differently.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


