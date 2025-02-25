import weaviate

# The URL for your Weaviate instance
weaviate_url = "https://5jdanhltdkd3op8dnvgcq.c0.us-east1.gcp.weaviate.cloud"

# Replace with your Weaviate Cloud credentials
username = "jhanu2809@gmail.com"  # Replace this with your Weaviate username
password = "Jhanu@28092004"  # Replace this with your Weaviate password

# Authenticate with Weaviate
client = weaviate.Client(
    url=weaviate_url,
    auth_client_secret=weaviate.AuthClientPassword(
        username=username,
        password=password
    )
)

# Now, you can proceed with your Weaviate operations.
# Add your Weaviate-related code here.
if client.is_ready():
    print("Weaviate is connected and ready!")
else:
    print("Weaviate is not ready. Please check the connection.")
