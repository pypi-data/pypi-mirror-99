from uplink import Consumer, get, post, returns, headers, Body, json
import os

try:
    key = os.environ["OCP_APIM_SUBSCRIPTION_KEY"]
except KeyError as e:
    print(
        f"""ERROR: Define the environment variable {e} with your subscription key.  For example:

    export OCP_APIM_SUBSCRIPTION_KEY="INSERT_YOUR_SUBSCRIPTION_KEY"

    """
    )
    key = None


@headers({"Ocp-Apim-Subscription-Key": key})
class RockyRoad(Consumer):
    """Provides a wrapper for the RockyRoad API.

    Usage Example:

        from rockyroad.rockyroad import RockyRoad

        rr = RockyRoad(base_url='INSERT_URL_FOR_API')

        api_response = rr.get_hello_world()
        print(api_response)

        api_response = rr.get_alert_requests()
        print(api_response)
    """

    @returns.json
    @get("")
    def get_hello_world(self):
        """Simple API test that returns json message with 'hello world'."""

    @returns.json
    @get("/alert_requests")
    def get_alert_requests(self):
        """Returns alert requests."""

    @returns.json
    @get("/alert_requests/creator/{creator_email}")
    def get_alert_requests_by(self, creator_email):
        """Returns alert requests from database by the creator's email."""

    @returns.json
    @json
    @post("/new_alert_request")
    def add_new_alert_request(self, new_alert_request: Body):
        """Adds new alert request to database."""
