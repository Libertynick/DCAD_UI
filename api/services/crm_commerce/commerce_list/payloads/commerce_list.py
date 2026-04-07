from datetime import datetime


class PayloadsCommerceList:

    @staticmethod
    def get_commerce_list_payload():
        today = datetime.now().strftime("%Y-%m-%d")

        return {
            "filter": {
                "personId": "dcffde2d-976b-482b-e4ac-08db660d9281",
                "contractorINN": "7705238125",
                "date": {
                    "from": today,
                    "to": today
                },
                "onlyOrders": True,
                "onlyEndUserPQ": False,
                "onlyWithPaidStorage": False,
                "deliverFullSetOnly": False
            },
            "paging": {
                "pageNumber": 1,
                "pageSize": 50,
                "sortField": "date",
                "sortOrder": "desc"
            }
        }