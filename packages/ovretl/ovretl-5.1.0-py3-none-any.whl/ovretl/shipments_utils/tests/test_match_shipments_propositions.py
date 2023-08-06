from datetime import datetime

import numpy as np
import pandas as pd
from ovretl.shipments_utils.match_shipments_propositions import match_shipments_propositions
from pandas.util.testing import assert_frame_equal


def test_match_shipments_propositions():
    shipments_df = pd.DataFrame(data={"id": [1, 2], "status": ["booked", "finished"], "transit_time": [2, 3]})
    propositions_df = pd.DataFrame(
        data={
            "id": [1, 2, 3, 4],
            "created_at": [datetime(2020, 5, 2), datetime(2020, 5, 1), datetime(2020, 5, 1), datetime(2020, 5, 4),],
            "shipment_id": [1, 1, 2, 2],
            "status": ["purchase_ready", "sent", "new", "new"],
            "purchase_ready_date": [0, 0, 0, 0],
            "sent_date": [0, 0, 0, 0],
            "accepted_date": [0, 0, 0, 0],
            "transit_time": [0, 0, 0, 0],
            "transit_time_door_to_port": [0, 0, 0, 0],
            "transit_time_port_to_door": [0, 0, 0, 0],
            "kronos_state": [np.nan, "sent", "auto", "auto"],
        }
    )
    result = match_shipments_propositions(shipments_df=shipments_df, propositions_df=propositions_df)
    result_should_be = pd.DataFrame(
        data={
            "shipment_id": [1, 2],
            "shipment_status": ["booked", "finished"],
            "proposition_id": [2, 4],
            "proposition_status": ["sent", "new"],
            "purchase_ready_date": [0, 0],
            "sent_date": [0, 0],
            "accepted_date": [0, 0],
            "transit_time": [0, 0],
            "transit_time_door_to_port": [0, 0],
            "transit_time_port_to_door": [0, 0],
            "kronos_state": ["sent", "auto"],
        }
    )
    assert_frame_equal(result, result_should_be)
