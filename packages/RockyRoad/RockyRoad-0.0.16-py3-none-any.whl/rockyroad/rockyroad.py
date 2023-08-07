from uplink import Consumer, get, post, delete, returns, headers, Body, json
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

        api_response = rr.get_alert_requests_by_creator_email('user@acme.com')
        print(api_response)

        api_response = rr.add_alert_request(new_alert_request_json)
        print(api_response)

        api_response = rr.delete_alert_request(brand, alert_request_id)
        print(api_response)

        api_response = rr.get_alert_reports()
        print(api_response)

        api_response = rr.get_alert_reports_by_creator_email('user@acme.com')
        print(api_response)

    """

    @returns.json
    @get("/")
    def get_hello_world(self):
        """This call will return Hello World."""

    @returns.json
    @get("/alert_requests")
    def get_alert_requests(self):
        """This call will return detailed alert request information for all users."""

    @returns.json
    @get("/alert_requests/{creator_email}")
    def get_alert_requests_by_creator_email(self, creator_email):
        """This call will return detailed alert request information for the creator's email specified in the URI."""

    @returns.json
    @json
    @post("/alert_requests")
    def add_alert_request(self, new_alert_request: Body):
        """This call will create an alert request with the specified parameters."""

    @returns.json
    @json
    @delete("/alert_requests/{brand}/{alert_request_id}")
    def delete_alert_request(self, brand: str, alert_request_id: int):
        """This call will create an alert request with the specified parameters."""

    @returns.json
    @get("/alert_reports")
    def get_alert_reports(self):
        """This call will return detailed alert report information for all users."""

    @returns.json
    @get("/alert_reports/{creator_email}")
    def get_alert_reports_by_creator_email(self, creator_email):
        """This call will return detailed alert report information for the creator's email specified in the URI."""
