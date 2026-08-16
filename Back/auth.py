def getCredentials():
    #### Modules ####
    import os
    import webbrowser as wb
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import Flow
    #### Params ####
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    SCOPES = [
        "https://www.googleapis.com/auth/googlehealth.activity_and_fitness.readonly"
    ]

    credentials = None
    ####
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    if not credentials or not credentials.valid:
        flow = Flow.from_client_secrets_file(
            "client_secret.json",
            scopes=SCOPES,
            redirect_uri="http://localhost:8080/"
        )

        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt = 'consent'
        )

        wb.open(authorization_url)

        redirect_response = input(
            "Paste the full localhost URL from your browser here: "
        )

        flow.fetch_token(
            authorization_response=redirect_response
        )

        credentials = flow.credentials

        with open("token.json", "w") as token_file:
            token_file.write(credentials.to_json())

    return credentials  
        # print("Authentication successful")
        # print("Valid:", credentials.valid)
        # print("Expired:", credentials.expired)
        # print("Scopes:", credentials.scopes)