import os
import pathlib
from urllib.parse import urlparse

from oauth2client import client, tools, transport
from oauth2client.file import Storage

from . import context

CREDS_FILENAME = "{}/access"
TOKENS_FILENAME = "{}/tokens"


def get_store_from_ctx(ctx, token=False):
    return get_store(context.get_issuer(ctx), context.get_client_id(ctx), token=token)


def get_store(issuer, client_id, token=False):
    """ Return a oauth2client.file.Storage object """
    home_dir = os.path.join(os.path.expanduser("~"), ".config", "agilicus")
    issuer_dir = urlparse(issuer).netloc

    if token:
        creds_file = TOKENS_FILENAME.format(client_id)
    else:
        creds_file = CREDS_FILENAME.format(client_id)

    store_dir = os.path.join(home_dir, issuer_dir)
    store_file = os.path.join(store_dir, creds_file)
    pathlib.Path(os.path.dirname(store_file)).mkdir(
        mode=0o0700, parents=True, exist_ok=True
    )
    pathlib.Path(store_file).touch(mode=0o0600, exist_ok=True)
    return Storage(store_file)


def delete_credentials_with_ctx(ctx):
    store = get_store_from_ctx(ctx)
    store.delete()


def delete_credentials(issuer, client_id):
    store = get_store(issuer, client_id)
    store.delete()


def get_credentials_from_ctx(ctx, refresh=None):
    return get_credentials(
        context.get_issuer(ctx),
        context.get_client_id(ctx),
        context.get_cacert(ctx),
        context.get_scopes(ctx),
        context.get_auth_local_webserver(ctx),
        refresh=refresh,
    )


def get_credentials(
    issuer, client_id, cacert, agilicus_scopes, auth_local_webserver, refresh=None
):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    store = get_store(issuer, client_id)
    crd = store.get()

    # Configure the ouath2 flow to trust the api if a certificate is
    # provided.
    http = None

    # Unfortunately, cacert is a boolean or a string. Some libraries
    # accept a boolean or a string, but httplib2 does not.
    if isinstance(cacert, str):
        http = transport.get_http_object(ca_certs=cacert)
        # Dex is redirecting us. Let it go through.
    else:
        http = transport.get_http_object()
    http.follow_redirects = True
    http.follow_all_redirects = True

    if crd and crd.access_token_expired:
        try:
            crd.refresh(http)
            return crd
        except client.HttpAccessTokenRefreshError:
            crd = None

    if crd and refresh:
        crd.refresh(http)
        return crd

    if not crd:
        client_info = {}
        client_info["client_id"] = client_id
        client_info["auth_uri"] = issuer + "/auth"
        client_info["token_uri"] = issuer + "/token"

        scopes = [
            "openid",
            "profile",
            "email",
            "federated:id",
            "offline_access",
        ]
        if agilicus_scopes:
            scopes += agilicus_scopes
        client_info["redirect_uri"] = ["http://localhost:4200"]

        constructor_kwargs = {
            "redirect_uri": client_info["redirect_uri"],
            "auth_uri": client_info["auth_uri"],
            "token_uri": client_info["token_uri"],
        }

        flow = client.OAuth2WebServerFlow(
            client_info["client_id"],
            client_secret="",
            scope=scopes,
            pkce=True,
            **constructor_kwargs,
        )

        flow.user_agent = "agilicus-sdk"
        kwargs = {}
        # kwargs = ['--auth_host_port', '5000', '5001', '5002', '5003', '5004',
        #          '--auth_host_name', 'localhost']
        kwargs = [
            "--auth_host_port",
            "4200",
            "4201",
            "4202",
            "4203",
            "4204",
            "--auth_host_name",
            "localhost",
        ]
        flags = tools.argparser.parse_args(kwargs)
        flags.noauth_local_webserver = not auth_local_webserver

        credentials = tools.run_flow(flow, store, flags, http=http)
        return credentials

    return crd
