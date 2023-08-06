from uplink import Consumer, get, returns, headers
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
