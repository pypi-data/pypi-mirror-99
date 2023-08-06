from nomnomdata.engine.components import Connection, Parameter, ParameterGroup
from nomnomdata.engine.parameters import (
    Boolean,
    Code,
    CodeDialectType,
    Enum,
    Int,
    Password,
    String,
    Text,
)

# TODO implement max for String, uncomment max values here
AWSTokenConnection = Connection(
    connection_type_uuid="AWS5D-TO99M",
    description="AWS Access Key Information.",
    alias="AWS:Token",
    categories=["aws", "access", "credentials"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=String(),
                name="aws_access_key_id",
                display_name="Access Key ID",
                description="First part of the Access Key.",
                required=True,
            ),
            Parameter(
                type=String(),
                name="aws_secret_access_key",
                display_name="Secret Access Key",
                description="Second part of the Access Key.",
                required=True,
            ),
            Parameter(
                type=String(),
                name="region",
                display_name="Region",
                description="Specify the AWS region that the session will be created within.",
                required=True,
            ),
            name="secret_info",
            display_name="Secret Info",
        ),
    ],
)

AWSS3BucketConnection = Connection(
    connection_type_uuid="AWSS3-BKH32",
    alias="AWS:S3:Bucket+Token",
    description="AWS Bucket Name and connection credentials.",
    categories=["aws", "bucket", "storage"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=String(),
                name="bucket",
                display_name="Bucket",
                description="Name of the Bucket",
                required=True,
            ),
            Parameter(
                type=String(),
                name="endpoint_url",
                display_name="S3 Endpoint URL",
                description="S3 Endpoint url for non-AWS hosted buckets.",
            ),
            Parameter(
                type=String(),
                name="prefix",
                display_name="Folder Path Prefix",
                description="Path prefix to apply towards any requests to this bucket.",
            ),
            Parameter(
                type=String(),
                name="s3_temp_space",
                display_name="S3 Temporary Path",
                description="Folder in which Tasks using this Connection may create temporary files. A folder named temp in the root of the bucket will be used if left blank.",
            ),
            name="bucket_info",
            display_name="Bucket Info",
        ),
        ParameterGroup(
            Parameter(
                type=String(),
                name="access_key_id",
                display_name="Access Key ID",
                description="First part of the Access Key.",
                required=True,
            ),
            Parameter(
                type=String(),
                name="secret_access_key",
                display_name="Secret Access Key",
                description="Second part of the Access Key.",
                required=True,
            ),
            name="secret_info",
            display_name="Secret Info",
        ),
    ],
)

FTPConnection = Connection(
    alias="FTP",
    description="FTP, FTPS or SFTP configuration.",
    connection_type_uuid="FTP92-TS0BZ",
    categories=["ftp", "sftp", "ftps"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="type",
                display_name="FTP Type",
                description="Type of FTP authentication to use",
                type=Enum(choices=["FTP", "FTPS Explicit", "SFTP"]),
                required=True,
            ),
            name="authentication_parameters",
            display_name="Authentication Parameters",
        ),
        ParameterGroup(
            Parameter(
                name="host_name",
                display_name="Hostname",
                description="DNS Host name of the server.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="port",
                display_name="FTP Port",
                description="Port 21 is the typical port for FTP and explicitly negotiated FTPS. Port 22 is the typical port for SFTP.",
                type=Int(min=1, max=65535),
                required=True,
                default=21,
            ),
            Parameter(
                name="username",
                display_name="Username",
                type=String(),
                required=False,
            ),
            Parameter(
                name="password",
                display_name="Password",
                type=String(),
                required=False,
            ),
            Parameter(
                name="ssh_key",
                display_name="SSH Private Key",
                description="This field is only used for key based SFTP authentication.",
                type=String(),
                required=False,
            ),
            name="server_parameters",
            display_name="Server Parameters",
        ),
    ],
)

GenericDatabaseConnection = Connection(
    alias="Generic:Database",
    description="Basic database access information.",
    connection_type_uuid="GNC8L-BG2T3",
    categories=["generic", "database"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="hostname",
                display_name="Hostname",
                description="DNS name used to connect to the database server or endpoint.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="port",
                display_name="Port",
                description="TCP Port used to connect. Port 3306 is the typical port for MySQL.",
                type=Int(min=1, max=65535),
                required=True,
                default=3306,
            ),
            Parameter(
                name="database",
                display_name="Database Name",
                description="Name of the database to connect to.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="db_engine",
                display_name="Database Type",
                description="Type of database to connect to.",
                type=Enum(choices=["mysql", "postgres"]),
                required=True,
                default="mysql",
            ),
            Parameter(
                name="username",
                display_name="Username",
                type=String(),
                required=False,
            ),
            Parameter(
                name="password",
                display_name="Password",
                type=String(),
                required=False,
            ),
            name="db_parameters",
            display_name="Database Parameters",
        ),
    ],
)

GoogleCloudConnection = Connection(
    alias="Google:ServiceAccount",
    description="Google Service Account Key JSON",
    connection_type_uuid="GOOGLE-SERVICE-ACCOUNT",
    categories=["google", "service"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="json",
                display_name="Service Account Keyfile JSON",
                description="Contents of the Keyfile which should be valid JSON",
                type=Text(),
                required=True,
            ),
            name="google_parameters",
            display_name="Google Parameters",
        ),
    ],
)


HunterIOToken = Connection(
    alias="Hunter.io:APIKey",
    description="API key used to connect to Hunter.io",
    connection_type_uuid="HTR10-API3B",
    categories=["hunter.io", "api", "key"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="api_key",
                display_name="API Key",
                description="API Key used to connect to Hunter.io.",
                type=Password(min=32, max=64),
                required=True,
            ),
            name="API Information",
            display_name="API Information",
        ),
    ],
)


LookerConnection = Connection(
    alias="Looker:Host+Credentials",
    description="Authentication and endpoint information for accessing the Rest API on a Looker server.",
    connection_type_uuid="LKR38-BKOTZ",
    categories=["looker", "api"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="client_id",
                display_name="Client ID",
                description="Client ID portion of the API3 key associated with a user account on a Looker server.",
                type=String(),
                # max=256,
                required=True,
            ),
            Parameter(
                name="client_secret",
                display_name="Client Secret",
                description="Client Secret portion of the API3 key associated with a user account on a Looker server.",
                type=String(),
                # max=256,
                required=True,
            ),
            Parameter(
                name="looker_url",
                display_name="Looker API Host URL",
                description="URL with the DNS name and port number used to reach a Looker server's API endpoint.",
                type=String(),
                # max=512,
                required=True,
            ),
            name="looker_info",
            display_name="Looker Information",
        ),
    ],
)

RedshiftDatabaseConnection = Connection(
    alias="Redshift Database",
    description="Redshift database access information.",
    connection_type_uuid="AWSDB-RSCON",
    categories=["AWS", "redshift", "database"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="hostname",
                display_name="Hostname",
                description="DNS name used to connect to the cluster endpoint.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="port",
                display_name="Port",
                description="TCP Port used to connect. Port 5439 is the typical port for Redshift clusters.",
                type=Int(min=1150, max=65535),
                required=True,
                default=5439,
            ),
            Parameter(
                name="database",
                display_name="Database Name",
                description="Name of the database to connect to within the cluster.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="db_engine",
                display_name="Database Type",
                description="Don't change this field value.",
                type=String(),
                required=True,
                default="redshift",
            ),
            Parameter(
                name="username",
                display_name="Username",
                type=String(),
                required=False,
            ),
            Parameter(
                name="password",
                display_name="Password",
                type=String(),
                required=False,
            ),
            name="db_parameters",
            display_name="Database Parameters",
        ),
    ],
)

SlackAPIConnection = Connection(
    alias="Slack:API:Token",
    description="Slack API token.",
    connection_type_uuid="SLKTK-O2B8D",
    categories=["API", "Slack"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="token",
                display_name="Token",
                description="Token string used to connect to Slack REST API's.",
                type=String(),
                required=True,
            ),
            name="slack_parameters",
            display_name="Slack Parameters",
        ),
    ],
)


SMTPConnection = Connection(
    alias="SMTP Connection",
    description="SMTP Server Configuration",
    connection_type_uuid="EMAIL-SMTP",
    categories=["SMTP", "TLS", "Email"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="user",
                display_name="Username",
                description="Username to authenticate with",
                type=String(),
                # max=1024,
                required=True,
            ),
            Parameter(
                name="password",
                display_name="Password",
                description="Password to authenticate with",
                type=String(),
                # max=64,
                required=True,
            ),
            Parameter(
                name="host",
                display_name="Hostname",
                description="Host, url, or IP to connect to",
                type=String(),
                # max=512,
                required=True,
            ),
            Parameter(
                name="port",
                display_name="Port",
                description="Port Number",
                type=String(),
                # max=5,
                required=True,
            ),
            Parameter(
                name="tls",
                display_name="TLS Enabled",
                type=Boolean(),
                default=False,
            ),
            name="server_parameters",
            display_name="Server Parameters",
        ),
    ],
)

SnowflakeDatabaseConnection = Connection(
    alias="Snowflake Database",
    description="Snowflake database access information.",
    connection_type_uuid="SNFK3-WHC0N",
    categories=["Snowflake", "Database"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="user",
                display_name="User",
                description="Login name for the user.",
                type=String(max=256),
                required=True,
            ),
            Parameter(
                name="password",
                display_name="Password",
                description="Password for the user.",
                type=String(max=64),
                required=True,
            ),
            Parameter(
                name="account",
                display_name="Account",
                description="Name of your account (provided by Snowflake). For more details, see https://docs.snowflake.com/en/user-guide/python-connector-api.html#label-account-format-info.",
                type=String(max=256),
                required=True,
            ),
            Parameter(
                name="warehouse",
                display_name="Warehouse",
                description="Name of the default warehouse to use. You can include USE WAREHOUSE in your SQL to change the warehouse.",
                type=String(max=256),
                required=False,
            ),
            Parameter(
                name="database",
                display_name="Database",
                description="Name of the default database to use. You can include USE DATABASE in your SQL to change the database.",
                type=String(max=256),
                required=False,
            ),
            Parameter(
                name="role",
                display_name="Role Name",
                description="Name of the default role to use. After login, you can include USE ROLE in your SQL to change the role.",
                type=String(max=256),
                required=False,
            ),
            name="db_parameters",
            display_name="Database Parameters",
        ),
    ],
)

SSHPrivateKeyConnection = Connection(
    alias="SSH Private Key",
    description="Private Key for SSH Authentication and Encryption.",
    connection_type_uuid="PVKEY-SSH01",
    categories=["SSH", "RSA", "Key"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="ssh_key",
                display_name="SSH Private Key",
                description="Private key string.",
                type=Text(),
                required=True,
            ),
            name="authentication_parameters",
            display_name="Authentication Parameters",
        ),
    ],
)

SSHHostConnection = Connection(
    alias="SSH Host",
    description="Remote Server SSH Session.",
    connection_type_uuid="SSH01-HOST1",
    categories=["SSH", "Secure", "Shell"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="hostname",
                display_name="Hostname",
                description="DNS name of the host machine.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="port",
                display_name="Port",
                description="TCP Port used for the secure shell connection. Port 22 is the typical port for SSH.",
                type=Int(min=1, max=65535),
                required=True,
                default=22,
            ),
            Parameter(
                name="username",
                display_name="Username",
                type=String(),
                required=True,
            ),
            Parameter(
                name="password",
                display_name="Password",
                description="Optional.  Used for password based authentication.",
                type=String(),
                required=False,
            ),
            Parameter(
                name="connect_timeout",
                display_name="TCP Connection Timeout",
                description="Optional.  Amount of seconds to wait for a successful TCP connection.",
                type=Int(),
                required=False,
            ),
            Parameter(
                name="private_key",
                display_name="Private Key",
                description="Optional.  Used for private key authentication and encryption.",
                type=Text(),
                required=False,
            ),
            name="server_parameters",
            display_name="Server Parameters",
        ),
    ],
)

HubspotConnection = Connection(
    connection_type_uuid="HBSPT-APITK",
    alias="Hubspot:Subdomain+Credentials",
    description="API token to connect to Hubspot.",
    categories=["Hubspot", "API", "Domain"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=String(),
                name="token",
                display_name="API Token",
                description="Enter your Hubspot API-key",
                required=True,
            ),
            name="hubspot_params",
            display_name="Hubspot Parameters",
        ),
    ],
)

GoodDataConnection = Connection(
    connection_type_uuid="GC29M-VU5MG",
    alias="GoodData:Credentials",
    description="GoodData Credentials",
    categories=["GoodData", "Domain", "Username", "Password"],
    parameter_groups=[
        ParameterGroup(
            Parameter(type=String(), name="email", display_name="Email", required=True),
            Parameter(
                type=String(), name="password", display_name="Password", required=True
            ),
            Parameter(type=String(), name="domain", display_name="Domain", required=True),
            name="gooddata_params",
            display_name="GoodData Parameters",
        ),
    ],
)

FacebookConnection = Connection(
    connection_type_uuid="FB83P-AD8BP",
    alias="Facebook:Access Token",
    description="Facebook Access Token",
    categories=["facebook", "token", "social media"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=String(),
                name="access_token",
                display_name="Access Token",
                required=True,
            ),
            name="facebook_params",
            display_name="Facebook Parameters",
        ),
    ],
)

ZendeskConnection = Connection(
    connection_type_uuid="Z3GK9-XPGG3",
    alias="Zendesk:Subdomain+Credentials",
    description="E-mail address, password and subdomain used to access Zendesk data.",
    categories=["Zendesk", "Username", "Password"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=String(),
                name="email",
                display_name="E-Mail Address",
                description="E-mail address of the user account with access the to Zendesk data.",
                required=True,
            ),
            Parameter(
                type=String(),
                name="password",
                display_name="Password",
                description="Zendesk password associated with the e-mail address.",
                required=True,
            ),
            Parameter(
                type=String(),
                name="subdomain",
                display_name="Subdomain",
                description="Specify the subdomain associated with your Zendesk data.  For example, if your domain is yourserver.zendesk.com, type in just yourserver.",
                required=True,
            ),
            name="zendesk_params",
            display_name="Zendesk Parameters",
        ),
    ],
)

SingularConnection = Connection(
    connection_type_uuid="SNG1E-P9VDW",
    alias="Singular:API:Token",
    description="Singular API token",
    categories=[
        "Singular",
        "API",
    ],
    parameter_groups=[
        ParameterGroup(
            Parameter(type=String(), name="token", display_name="Token", required=True),
            name="singular_params",
            display_name="Singular Parameters",
        ),
    ],
)

AppAnnieConnection = Connection(
    connection_type_uuid="APP1E-T0NXM",
    alias="AppAnnie:API:Token",
    description="App Annie API token.",
    categories=["mobile attribution", "app annie", "API"],
    parameter_groups=[
        ParameterGroup(
            Parameter(type=String(), name="token", display_name="Token", required=True),
            name="app_annie_params",
            display_name="App Annie Params",
        ),
    ],
)

RedisConnection = Connection(
    connection_type_uuid="REDIS-CNCTN",
    alias="Redis Credentials",
    description="Hostname, port and optional password used to access Redis.",
    categories=["Redis"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=String(),
                name="host",
                display_name="Host",
                description="DNS name of server hosting Redis.",
                required=True,
            ),
            Parameter(
                type=Int(min=1, max=65535),
                name="port",
                display_name="Port",
                description="TCP Port that Redis is listening on. Port 6379 is typical.",
                required=True,
                default=6379,
            ),
            Parameter(
                type=Password(),
                name="password",
                display_name="Password",
                description="Optional password for authentication.",
                required=False,
            ),
            name="redis_params",
            display_name="Redis Parameters",
            description="",
        )
    ],
)

ElasticSearchConnection = Connection(
    connection_type_uuid="ELSTC-CNCTN",
    alias="Elasticsearch Credentials",
    description="Endpoint, optional user name and password or api token.",
    categories=["Elasticsearch"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=String(),
                name="endpoint",
                display_name="Endpoint",
                description="Elasticsearch cluster endpoint URL. Formatted as: https://CLUSTER_ID.REGION.CLOUD_PLATFORM.DOMAIN:PORT",
                required=True,
            ),
            Parameter(
                type=Code(dialect=CodeDialectType.JSON),
                name="api",
                display_name="API Key",
                description="Optional. Api key to use instead of basic authentication.",
            ),
            Parameter(
                type=String(),
                name="username",
                display_name="Username",
                description="Optional. User name for basic authentication.",
            ),
            Parameter(
                type=Password(),
                name="password",
                display_name="Password",
                description="Optional. Password associated with the username.",
            ),
            name="elastic_params",
            display_name="Elasticsearch Parameters",
        )
    ],
)
MYSQLDatabaseConnection = Connection(
    alias="MySQL Database",
    description="Basic database access information.",
    connection_type_uuid="MYSQL-DTBCON",
    categories=["MySQL", "Database"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="hostname",
                display_name="Hostname",
                description="DNS name used to connect to the database server or endpoint.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="port",
                display_name="Port",
                description="TCP Port used to connect. Port 3306 is the typical port for MySQL.",
                type=Int(min=1, max=65535),
                required=True,
                default=3306,
            ),
            Parameter(
                name="database",
                display_name="Database Name",
                description="Name of the database to connect to.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="username",
                display_name="Username",
                type=String(),
                required=True,
            ),
            Parameter(
                name="password",
                display_name="Password",
                type=String(),
                required=False,
            ),
            name="db_parameters",
            display_name="Database Parameters",
        ),
    ],
)
PostgresDatabaseConnection = Connection(
    alias="Postgres Database",
    description="Basic database access information.",
    connection_type_uuid="PSTGRS-DTBCON",
    categories=["Postgres", "Database"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="hostname",
                display_name="Hostname",
                description="DNS name used to connect to the database server or endpoint.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="port",
                display_name="Port",
                description="TCP Port used to connect. Port 5432 is the typical port for Postgres.",
                type=Int(min=1, max=65535),
                required=True,
                default=5432,
            ),
            Parameter(
                name="database",
                display_name="Database Name",
                description="Name of the database to connect to.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="username",
                display_name="Username",
                type=String(),
                required=True,
            ),
            Parameter(
                name="password",
                display_name="Password",
                type=String(),
                required=False,
            ),
            name="db_parameters",
            display_name="Database Parameters",
        ),
    ],
)
SQLServerDatabaseConnection = Connection(
    alias="SQL Server Database",
    description="Basic database access information.",
    connection_type_uuid="MSSQL-DTBCN",
    categories=["Microsoft", "SQL", "Database"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="hostname",
                display_name="Hostname",
                description="DNS name used to connect to the database server or endpoint.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="port",
                display_name="Port",
                description="TCP Port used to connect. Port 1433 is the typical port for Microsoft SQL Servers.",
                type=Int(min=1, max=65535),
                required=True,
                default=1433,
            ),
            Parameter(
                name="database",
                display_name="Database Name",
                description="Name of the database to connect to.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="username",
                display_name="Username",
                type=String(),
                required=True,
            ),
            Parameter(
                name="password",
                display_name="Password",
                type=String(),
                required=False,
            ),
            name="db_parameters",
            display_name="Database Parameters",
        ),
    ],
)
IntercomConnection = Connection(
    connection_type_uuid="INTCM-APITK",
    alias="Intercom API Key",
    description="API Key to use to connect to Intercom.",
    categories=["Intercom"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=String(),
                name="token",
                display_name="API Key",
                description="Intercom API key",
                required=True,
            ),
            name="intercom_params",
            display_name="Intercom Access",
        ),
    ],
)
AppsFlyerConnection = Connection(
    connection_type_uuid="AFLYR-APITK",
    alias="AppsFlyer API Token",
    description="API token to use to connect to AppsFlyer.",
    categories=["AppsFlyer"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=String(),
                name="token",
                display_name="API Token",
                description="AppsFlyer API token.",
                required=True,
            ),
            name="appsflyer_params",
            display_name="AppsFlyer Access",
        ),
    ],
)
