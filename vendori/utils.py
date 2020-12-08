import requests

TRACK_CONSUMER_KEY = "sZYxu5P0TpBPAwTC6gLagfUNrqPy4Hfk"


def track_dhl(tracking_no):
    DHL_ENDPOINT = "https://api-eu.dhl.com/track/shipments"

    headers = {
        "DHL-API-Key": TRACK_CONSUMER_KEY
    }

    dhl_params = {
        "trackingNumber": tracking_no,
    }

    response = requests.get(DHL_ENDPOINT, headers=headers, params=dhl_params)
    shipment_data = response.json()["shipments"]
    awb_history = []
    for shipment in shipment_data:

        shipment_events = shipment["events"]
        events = []
        for event in shipment_events:
            time = event["timestamp"]
            desc = event["description"]
            address = event["location"]["address"]
            events.append({"time": time.replace("T", " "), "desc": desc, "address": address.get("addressLocality")})

        shipping_dict = {
            "shipment_id": shipment["id"],
            "shipment_service": shipment["service"],
            "shipment_origin": shipment["origin"]["address"].get("addressLocality"),
            "shipment_destination": shipment["destination"]["address"].get("addressLocality"),
            "shipment_status_time": shipment["status"]["timestamp"].replace("T", " "),
            "shipment_status_location": shipment["status"]["location"]["address"].get("addressLocality"),
            "shipment_status_status": shipment["status"]["status"],
            "shipment_events_list": events
        }
        awb_history.append(shipping_dict)

    return awb_history
