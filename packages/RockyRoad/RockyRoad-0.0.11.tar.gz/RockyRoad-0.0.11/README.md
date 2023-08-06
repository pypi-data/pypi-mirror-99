# RockyRoad

This package provides a Python wrapper for the RockyRoad API.

RockyRoad is a part of the PyPi repository and can be installed via

    pip install RockyRoad

    export OCP_APIM_SUBSCRIPTION_KEY="INSERT_YOUR_SUBSCRIPTION_KEY"


Usage Example:

    from rockyroad.rockyroad import RockyRoad

    rr = RockyRoad(base_url="INSERT_URL_FOR_API")

    api_response = rr.get_hello_world()
    print(api_response)

    api_response = rr.get_alert_requests()
    print(api_response)

