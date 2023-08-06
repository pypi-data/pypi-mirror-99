import agilicus
import operator

from . import context
from .general_helpers import find_object
from .input_helpers import get_org_from_input_or_ctx
from .input_helpers import update_if_not_none
from .input_helpers import pop_item_if_none
from .input_helpers import build_updated_model
from .output.table import (
    column,
    mapped_column,
    metadata_column,
    spec_column,
    subtable,
    format_table,
)


def _build_updated_issuer(issuer, new_values):
    issuer_dict = issuer.to_dict()
    update_if_not_none(issuer_dict, new_values)

    # The clients aren't needed for updates
    issuer_dict.pop("clients", None)

    oidc_upstreams = issuer_dict.get("oidc_upstreams", [])
    for upstream in oidc_upstreams:
        pop_item_if_none(upstream)

    return agilicus.Issuer(**issuer_dict)


def _get_issuer(ctx, id, client, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    issuer = client.issuers_api.get_issuer(id, org_id=org_id)

    return issuer


def query(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    kwargs["org_id"] = org_id
    query_results = apiclient.issuers_api.list_issuers(**kwargs)
    if query_results:
        return query_results.issuer_extensions
    return


def format_issuers_for_garbage_collection(ctx, issuers):
    columns = [
        column("id"),
        column("issuer"),
        mapped_column("org_id", "org id"),
        column("enabled"),
    ]
    return format_table(ctx, issuers, columns)


def show(ctx, issuer_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    return _get_issuer(ctx, issuer_id, apiclient, **kwargs).to_dict()


def show_well_known(ctx, issuer_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.issuers_api.get_wellknown_issuer_info(issuer_id, **kwargs).to_dict()


def format_well_known_issuer_info(ctx, info):
    columns = [
        column("issuer_id"),
        column("supported_mfa_methods"),
    ]
    return format_table(ctx, info, columns)


def list_well_known(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.issuers_api.list_wellknown_issuer_info(**kwargs).well_known_info


def add(ctx, issuer, org_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    issuer_model = agilicus.Issuer(issuer=issuer, org_id=org_id)
    return apiclient.issuers_api.create_issuer(issuer_model).to_dict()


def _update_issuer(ctx, issuer_id, updater, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    issuer = _get_issuer(ctx, issuer_id, apiclient, **kwargs)

    if not issuer:
        print(f"Cannot find issuer {issuer_id}")
        return

    issuer = _build_updated_issuer(issuer, kwargs)

    return updater(apiclient.issuers_api, issuer_id, issuer).to_dict()


def update_root(ctx, issuer_id, **kwargs):
    return _update_issuer(ctx, issuer_id, agilicus.IssuersApi.replace_root, **kwargs)


def update_extension(ctx, issuer_id, **kwargs):
    return _update_issuer(ctx, issuer_id, agilicus.IssuersApi.replace_issuer, **kwargs)


def delete(ctx, issuer_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.issuers_api.delete_root(issuer_id, **kwargs)


def update_managed_upstreams(ctx, issuer_id, name, status, org_id=None, **kwargs):
    token = context.get_token(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    apiclient = context.get_apiclient(ctx, token)
    issuer = _get_issuer(ctx, issuer_id, apiclient, org_id=org_id, **kwargs)

    if not issuer:
        print(f"Cannot find issuer {issuer_id}")
        return

    for upstream in issuer.managed_upstreams:
        if upstream.name == name:
            upstream.enabled = status
            return apiclient.issuers_api.replace_issuer(
                issuer_id, issuer, **kwargs
            ).to_dict()
    print(f"{name} is not a managed upstream. Options are:")
    print([x.name for x in issuer.managed_upstreams])
    return


def update_oidc_upstreams(
    ctx,
    issuer_id,
    name,
    icon,
    issuer_uri,
    client_id,
    client_secret,
    issuer_external_host,
    username_key,
    user_id_key,
    email_key,
    email_verification_required,
    request_user_info,
    auto_create_status,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = kwargs.pop("org_id", None)
    issuer = _get_issuer(ctx, issuer_id, apiclient, org_id=org_id, **kwargs)

    if not issuer:
        print(f"Cannot find issuer {issuer_id}")
        return

    for upstream in issuer.oidc_upstreams:
        if upstream.name == name:
            if icon is not None:
                upstream.icon = icon
            if issuer_uri is not None:
                upstream.issuer = issuer_uri
            if client_id is not None:
                upstream.client_id = client_id
            if client_secret is not None:
                upstream.client_secret = client_secret
            if issuer_external_host is not None:
                upstream.issuer_external_host = issuer_external_host
            if username_key is not None:
                upstream.username_key = username_key
            if user_id_key is not None:
                upstream.user_id_key = user_id_key
            if email_key is not None:
                upstream.email_key = email_key
            if email_verification_required is not None:
                upstream.email_verification_required = email_verification_required
            if request_user_info is not None:
                upstream.request_user_info = request_user_info
            if auto_create_status is not None:
                upstream.auto_create_status = auto_create_status
            return apiclient.issuers_api.replace_issuer(
                issuer_id, issuer, **kwargs
            ).to_dict()
    print(f"{name} is not an oidc upstream")
    return


def add_oidc_upstreams(
    ctx,
    issuer_id,
    name,
    icon,
    issuer_uri,
    client_id,
    client_secret,
    issuer_external_host,
    username_key,
    user_id_key,
    email_key,
    email_verification_required,
    request_user_info,
    auto_create_status,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    issuer = _get_issuer(ctx, issuer_id, apiclient, **kwargs)

    if not issuer:
        print(f"Cannot find issuer {issuer_id}")
        return

    upstream = agilicus.OIDCUpstreamIdentityProvider(
        name,
        icon,
        issuer_uri,
        client_id,
        client_secret,
        issuer_external_host,
        username_key,
        email_key,
        email_verification_required,
        request_user_info,
        user_id_key,
        auto_create_status,
    )
    issuer.oidc_upstreams.append(upstream)
    kwargs.pop("org_id", None)
    return apiclient.issuers_api.replace_issuer(issuer_id, issuer, **kwargs).to_dict()


def delete_oidc_upstreams(ctx, issuer_id, name, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    issuer = _get_issuer(ctx, issuer_id, apiclient, org_id=org_id, **kwargs)

    if not issuer:
        print(f"Cannot find issuer {issuer_id}")
        return

    for upstream in issuer.oidc_upstreams:
        if upstream.name == name:
            issuer.oidc_upstreams.remove(upstream)
            apiclient.issuers_api.replace_issuer(issuer_id, issuer, **kwargs)
            return

    print(f"{name} is not an oidc upstream")
    return


def query_clients(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    query_results = apiclient.issuers_api.list_clients(**kwargs)
    if query_results:
        return query_results.clients
    return


def show_client(ctx, client_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    return apiclient.issuers_api.get_client(client_id, **kwargs).to_dict()


def _get_metadata_contents(metadata_file, metadata_text):
    if metadata_text is not None:
        return metadata_text

    if not metadata_file:
        return None

    with open(metadata_file, "r") as metadata_input:
        return metadata_input.read()


def add_client(
    ctx,
    issuer_id,
    name,
    metadata_file,
    metadata_text,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    client_model = agilicus.IssuerClient(issuer_id=issuer_id, name=name, **kwargs)
    client_model.saml_metadata_file = _get_metadata_contents(
        metadata_file, metadata_text
    )
    return apiclient.issuers_api.create_client(client_model).to_dict()


def _get_client(ctx, apiclient, client_id, **kwargs):
    apiclient = context.get_apiclient(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    client = apiclient.issuers_api.get_client(client_id, org_id=org_id)

    # Note: the api raises a 404 if it's not found

    return client


def update_client(
    ctx,
    client_id,
    metadata_file,
    metadata_text,
    **kwargs,
):
    apiclient = context.get_apiclient(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    client = _get_client(ctx, apiclient, client_id, **kwargs)

    client_dict = client.to_dict()
    update_if_not_none(client_dict, kwargs)
    client_model = agilicus.IssuerClient(**client_dict)
    client_model.saml_metadata_file = _get_metadata_contents(
        metadata_file, metadata_text
    )
    return apiclient.issuers_api.replace_client(client_id, client_model).to_dict()


def delete_client(ctx, client_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    return apiclient.issuers_api.delete_client(client_id, **kwargs)


def _add_to_client_list_and_replace(ctx, client_id, list_name, value, **kwargs):
    apiclient = context.get_apiclient(ctx)

    client = _get_client(ctx, apiclient, client_id, **kwargs)
    items = getattr(client, list_name) or []
    if value in items:
        return client.to_dict()

    items.append(value)
    setattr(client, list_name, items)
    return apiclient.issuers_api.replace_client(client.id, client).to_dict()


def _remove_from_client_list_and_replace(ctx, client_id, list_name, value, **kwargs):
    apiclient = context.get_apiclient(ctx)

    client = _get_client(ctx, apiclient, client_id, **kwargs)
    items = getattr(client, list_name) or []
    if value not in items:
        return client.to_dict()

    items.remove(value)
    setattr(client, list_name, items)
    return apiclient.issuers_api.replace_client(client.id, client).to_dict()


def add_redirect(ctx, client_id, redirect_url, **kwargs):
    return _add_to_client_list_and_replace(
        ctx, client_id, "redirects", redirect_url, **kwargs
    )


def delete_redirect(ctx, client_id, redirect_url, **kwargs):
    return _remove_from_client_list_and_replace(
        ctx, client_id, "redirects", redirect_url, **kwargs
    )


def add_restricted_organisation(ctx, client_id, restricted_org_id, **kwargs):
    return _add_to_client_list_and_replace(
        ctx, client_id, "restricted_organisations", restricted_org_id, **kwargs
    )


def delete_restricted_organisation(ctx, client_id, restricted_org_id, **kwargs):
    return _remove_from_client_list_and_replace(
        ctx, client_id, "restricted_organisations", restricted_org_id, **kwargs
    )


def format_policy_table(ctx, policies):
    columns = [
        metadata_column("id"),
        spec_column("name"),
        spec_column("issuer_id"),
        spec_column("org_id"),
        spec_column("supported_mfa_methods"),
        spec_column("default_action"),
    ]
    return format_table(ctx, policies, columns)


def format_policy_rules_table(ctx, policies):
    conditions_column = [
        column("condition_type"),
        column("operator"),
        column("field"),
        column("value"),
        column("input_is_list"),
    ]
    rules_columns = [
        metadata_column("id"),
        spec_column("action"),
        subtable(ctx, "conditions", conditions_column, subobject_name="spec"),
    ]
    columns = [
        metadata_column("id", out_name="policy id"),
        spec_column("default_action"),
        subtable(ctx, "rules", rules_columns, subobject_name="spec"),
    ]
    return format_table(ctx, policies, columns)


def format_policy_groups_table(ctx, policies):
    groups_columns = [
        metadata_column("id"),
        spec_column("name"),
        spec_column("rule_ids"),
    ]
    columns = [
        metadata_column("id", out_name="policy id"),
        spec_column("default_action"),
        subtable(ctx, "policy_groups", groups_columns, subobject_name="spec"),
    ]
    return format_table(ctx, policies, columns)


def list_auth_policies(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    query_results = apiclient.issuers_api.list_policies(**kwargs)
    return query_results.authentication_policies


def add_auth_policy(ctx, issuer_id, default_action, supported_mfa_methods, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    spec = agilicus.PolicySpec(
        issuer_id=issuer_id,
        default_action=default_action,
        supported_mfa_methods=[*supported_mfa_methods],
        **kwargs,
    )
    model = agilicus.Policy(spec=spec)
    return apiclient.issuers_api.create_policy(model).to_dict()


def update_auth_policy(ctx, policy_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    policy = _get_auth_policy(apiclient, policy_id, kwargs["org_id"])
    policy.spec = build_updated_model(agilicus.PolicySpec, policy.spec, kwargs)
    for rule in policy.spec.rules:
        for condition in rule["spec"].get("conditions", []):
            pop_item_if_none(condition)
    return apiclient.issuers_api.replace_policy(policy_id, policy).to_dict()


def reset_auth_policy(ctx, issuer_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    model = agilicus.ResetPolicyRequest(org_id=kwargs["org_id"])
    return apiclient.issuers_api.reset_to_default_policy(issuer_id, model).to_dict()


def _get_auth_policy(apiclient, policy_id, org_id):
    return apiclient.issuers_api.get_policy(policy_id, org_id=org_id)


def get_auth_policy(ctx, policy_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return _get_auth_policy(apiclient, policy_id, org_id).to_dict()


def delete_auth_policy(ctx, policy_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.issuers_api.delete_policy(policy_id, org_id=org_id)


# Rules


def add_auth_policy_rule(ctx, policy_id, action, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    spec = agilicus.PolicyRuleSpec(action=action, conditions=[], **kwargs)
    model = agilicus.PolicyRule(spec=spec)
    return apiclient.issuers_api.create_policy_rule(policy_id, model).to_dict()


def update_auth_policy_rule(ctx, policy_id, policy_rule_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    policy_rule = _get_auth_policy_rule(
        apiclient, policy_id, policy_rule_id, kwargs["org_id"]
    )
    policy_rule.spec = build_updated_model(
        agilicus.PolicyRuleSpec, policy_rule.spec, kwargs
    )

    for condition in policy_rule.spec.conditions or []:
        pop_item_if_none(condition)

    return apiclient.issuers_api.replace_policy_rule(
        policy_id, policy_rule_id, policy_rule
    ).to_dict()


def _get_auth_policy_rule(apiclient, policy_id, policy_rule_id, org_id):
    return apiclient.issuers_api.get_policy_rule(
        policy_id, policy_rule_id, org_id=org_id
    )


def get_auth_policy_rule(ctx, policy_id, policy_rule_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return _get_auth_policy_rule(apiclient, policy_id, policy_rule_id, org_id).to_dict()


def delete_auth_policy_rule(ctx, policy_id, policy_rule_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.issuers_api.delete_policy_rule(
        policy_id, policy_rule_id, org_id=org_id
    )


def convert_condition_list_to_dict(conditions):
    retval = {}
    for index, cond in enumerate(conditions):
        retval[cond.condition_type] = index
    return retval


def add_auth_policy_condition(ctx, policy_id, policy_rule_id, condition_type, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    policy_rule = _get_auth_policy_rule(
        apiclient, policy_id, policy_rule_id, kwargs["org_id"]
    )
    kwargs.pop("org_id", None)

    condition_dict = convert_condition_list_to_dict(policy_rule.spec.conditions)
    index = condition_dict.get(condition_type, None)
    if index is not None:
        policy_rule.spec.conditions[index] = build_updated_model(
            agilicus.PolicyCondition, policy_rule.spec.conditions[index], kwargs
        )
    else:
        new_cond = agilicus.PolicyCondition(condition_type=condition_type, **kwargs)
        policy_rule.spec.conditions.append(new_cond)

    return apiclient.issuers_api.replace_policy_rule(
        policy_id, policy_rule_id, policy_rule
    ).to_dict()


def delete_auth_policy_condition(
    ctx, policy_id, policy_rule_id, condition_type, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    policy_rule = _get_auth_policy_rule(
        apiclient, policy_id, policy_rule_id, kwargs["org_id"]
    )
    for cond in policy_rule.spec.conditions:
        if cond.condition_type == condition_type:
            policy_rule.spec.conditions.remove(cond)
            return apiclient.issuers_api.replace_policy_rule(
                policy_id, policy_rule_id, policy_rule
            ).to_dict()
    return None


def add_auth_policy_group(ctx, policy_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    policy = _get_auth_policy(apiclient, policy_id, kwargs["org_id"])
    insertion_index = kwargs.pop("insertion_index", None)
    if insertion_index is None or insertion_index < 0:
        insertion_index = len(policy.spec.policy_groups)

    kwargs.pop("org_id")
    group_spec = agilicus.PolicyGroupSpec(**kwargs)
    policy.spec.policy_groups.insert(
        insertion_index, agilicus.PolicyGroup(spec=group_spec)
    )
    return apiclient.issuers_api.replace_policy(policy_id, policy).to_dict()


def delete_auth_policy_group(ctx, policy_id, policy_group_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    policy = _get_auth_policy(apiclient, policy_id, kwargs["org_id"])
    for group in policy.spec.policy_groups:
        if group.metadata.id == policy_group_id:
            policy.spec.policy_groups.remove(group)
            return apiclient.issuers_api.replace_policy(policy_id, policy).to_dict()
    # ID not found return original object
    return policy.to_dict()


def format_attributes(ctx, attributes):
    columns = [
        column("attribute_name"),
        mapped_column("internal_attribute_path", "attribute_path"),
    ]
    return format_table(ctx, attributes, columns)


def set_attribute_mapping(
    ctx,
    client_id,
    attribute_name,
    attribute_path,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    client = _get_client(ctx, apiclient, client_id, **kwargs)
    attributes = client.attributes
    attr = find_object(attributes, "attribute_name", attribute_name)
    if not attr:
        attr = agilicus.AuthenticationAttribute(
            attribute_name=attribute_name, internal_attribute_path=attribute_path
        )
    else:
        attributes.remove(attr)
        attr.internal_attribute_path = attribute_path

    attributes.append(attr)

    return apiclient.issuers_api.replace_client(client.id, client).attributes


def delete_attribute_mapping(
    ctx,
    client_id,
    attribute_name,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    client = _get_client(ctx, apiclient, client_id, **kwargs)
    attributes = client.attributes
    attr = find_object(attributes, "attribute_name", attribute_name)
    if not attr:
        return client.attributes

    attributes.remove(attr)
    return apiclient.issuers_api.replace_client(client.id, client).attributes


def format_issuer_upstreams(ctx, info):
    columns = [
        column("name"),
        column("issuer"),
        column("upstream_type"),
        column("icon"),
        column("auto_create_status"),
    ]
    return format_table(ctx, info, columns)


def list_issuer_upstreams(ctx, issuer_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.issuers_api.get_upstreams(issuer_id, **kwargs).upstreams


def format_local_auth_upstreams(ctx, info):
    columns = [
        column("name"),
        column("upstream_id"),
        column("issuer"),
        column("upstream_type"),
        column("icon"),
        column("auto_create_status"),
    ]
    return format_table(ctx, info, columns, getter=operator.itemgetter)


def update_local_auth_upstream(
    ctx,
    issuer_id,
    name,
    upstream_id=None,
    issuer=None,
    icon=None,
    auto_create_status=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = kwargs.pop("org_id", None)
    issuer_obj = _get_issuer(ctx, issuer_id, apiclient, org_id=org_id, **kwargs)

    if not issuer_obj:
        print(f"Cannot find issuer {issuer_id}")
        return

    for upstream in issuer_obj.local_auth_upstreams:
        if upstream.name == name:
            if upstream_id is not None:
                upstream.upstream_id = upstream_id
            if icon is not None:
                upstream.icon = icon
            if issuer is not None:
                upstream.issuer = issuer
            if auto_create_status is not None:
                upstream.auto_create_status = auto_create_status
            return apiclient.issuers_api.replace_issuer(
                issuer_id, issuer_obj, **kwargs
            ).to_dict()
    print(f"{name} is not a local authentication upstream")
    return


def add_local_auth_upstream(
    ctx,
    issuer_id,
    name,
    upstream_id=None,
    issuer=None,
    icon=None,
    auto_create_status=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    issuer_obj = _get_issuer(ctx, issuer_id, apiclient, **kwargs)

    if not issuer_obj:
        print(f"Cannot find issuer {issuer_id}")
        return

    upstream = agilicus.LocalAuthUpstreamIdentityProvider(
        name=name,
        issuer=issuer,
        upstream_type="local_auth",
        icon=icon,
        auto_create_status=auto_create_status,
        upstream_id=upstream_id,
    )

    issuer_obj.local_auth_upstreams.append(upstream)

    kwargs.pop("org_id", None)
    return apiclient.issuers_api.replace_issuer(
        issuer_id, issuer_obj, **kwargs
    ).to_dict()


def delete_local_auth_upstream(ctx, issuer_id, name, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    issuer = _get_issuer(ctx, issuer_id, apiclient, org_id=org_id, **kwargs)

    if not issuer:
        print(f"Cannot find issuer {issuer_id}")
        return

    for upstream in issuer.local_auth_upstreams:
        if upstream.name == name:
            issuer.local_auth_upstreams.remove(upstream)
            apiclient.issuers_api.replace_issuer(issuer_id, issuer, **kwargs)
            return

    print(f"{name} is not a local authentication upstream")
    return
