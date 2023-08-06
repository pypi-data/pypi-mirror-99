import pandas as pd

from ovretl.shipment_orchestration_utils.shipment_daily_workload import (
    total_tasks_weight,
    shipment_total_workflows_weight,
    shipments_remaining_days,
    shipments_timelines,
    estimated_remaining_daily_workload,
    daily_tasks_total_weight_on_shipment,
    shipments_daily_workload_timelines,
)
import datetime


def test_total_task_weight():
    tasks_df = pd.DataFrame(data={"shipment_id": ["1", "2", "2", "1"], "weight": [1, 2, 3, 5]})
    result_should_be = pd.DataFrame(data={"shipment_id": ["1", "2"], "total_tasks_weight": [6, 5]}).set_index(
        "shipment_id"
    )
    result = total_tasks_weight(tasks_df)
    pd.testing.assert_frame_equal(result, result_should_be)


def test_daily_tasks_total_weight_on_shipment():
    today_date = datetime.date(2020, 12, 28)
    other_date = datetime.date(2001, 1, 1)
    tasks_df = pd.DataFrame(
        data={
            "shipment_id": ["1", "1", "2", "2", "1"],
            "status": ["done", "to_do", "to_do", "to_do", "to_do"],
            "due_date": [other_date, today_date, today_date, other_date, today_date],
            "done_date": [today_date, today_date, today_date, other_date, today_date],
            "weight": [1, 2, 3, 4, 5],
        }
    )
    result_should_be = 8
    result = daily_tasks_total_weight_on_shipment(tasks_df.loc[tasks_df["shipment_id"] == "1", :], today_date)
    assert result_should_be == result


def test_shipment_total_workflows_weight():
    sh_df = pd.DataFrame(data={"shipment_id": ["1", "2", "1", "2"], "total_workflow_weight": [1, 2, 3, 4],})
    result_should_be = pd.DataFrame(data={"shipment_id": ["1", "2"], "total_workflows_weight": [4, 6]})
    result = shipment_total_workflows_weight(sh_df)
    pd.testing.assert_frame_equal(result, result_should_be)


def test_shipment_remaining_days():
    today = datetime.datetime(2020, 12, 28)
    day_before_1 = datetime.datetime(2020, 12, 27)
    day_before_2 = datetime.datetime(2020, 12, 26)
    sh_df = pd.DataFrame(
        data={
            "shipment_id": ["1", "2", "3"],
            "workflow_id": ["1", "2", "3"],
            "total_transit_time": [10, 10, 10],
            "created_at": [today, day_before_1, day_before_2],
            "shipment_status": ["awaiting_booking", "booked", "booked"],
            "freight_method": ["air", "ocean", "ocean"],
            "freight_type": ["air", "ocean", "ocean"],
            "foresea_name": ["BATD", "BATE", "BATE"],
            "incoterm": ["fob", "ddp", "ddp"],
            "delivery_date": [None, None, None],
            "arrival_date": [None, None, None],
        }
    )
    timelines = shipments_timelines(sh_df)
    result_should_be = pd.DataFrame(
        data={
            "shipment_id": ["1", "2", "3"],
            "workflow_id": ["1", "2", "3"],
            "total_transit_time": [10, 10, 10],
            "created_at": [today, day_before_1, day_before_2],
            "shipment_status": ["awaiting_booking", "booked", "booked"],
            "freight_method": ["air", "ocean", "ocean"],
            "freight_type": ["air", "ocean", "ocean"],
            "foresea_name": ["BATD", "BATE", "BATE"],
            "incoterm": ["fob", "ddp", "ddp"],
            "delivery_date": [None, None, None],
            "arrival_date": [None, None, None],
            "remaining_days": [9, 8, 7],
        }
    )
    result = shipments_remaining_days(sh_df, today.date(), timelines)
    pd.testing.assert_frame_equal(result, result_should_be)


def test_shipments_timelines_with_transit_time():
    day_1 = datetime.datetime(2020, 12, 28)
    day_2 = datetime.datetime(2020, 12, 29)
    day_3 = datetime.datetime(2020, 12, 30)
    day_4 = datetime.datetime(2020, 12, 31)
    day_5 = datetime.datetime(2021, 1, 1)
    sh_df = pd.DataFrame(
        data={
            "shipment_id": ["1", "2"],
            "total_transit_time": [2, 3],
            "created_at": [day_1, day_3],
            "delivery_date": [None, None],
            "arrival_date": [None, None],
        }
    )
    result_should_be = pd.DataFrame(
        data={"shipment_id": ["1", "1", "2", "2", "2"], "dates": [day_1, day_2, day_3, day_4, day_5]}
    )
    result_should_be.loc[:, ["dates"]] = result_should_be["dates"].dt.date
    print("result_should_be")
    print(result_should_be)
    result = shipments_timelines(active_shipments_data_df=sh_df)
    print("result")
    print(result)
    pd.testing.assert_frame_equal(result, result_should_be)


def test_shipments_timelines_with_tracking_dates():
    day_1 = datetime.datetime(2020, 12, 28)
    day_2 = datetime.datetime(2020, 12, 29)
    day_3 = datetime.datetime(2020, 12, 30)
    day_4 = datetime.datetime(2020, 12, 31)
    day_5 = datetime.datetime(2021, 1, 1)
    sh_df = pd.DataFrame(
        data={
            "shipment_id": ["1", "2"],
            "total_transit_time": [10, 10],
            "created_at": [day_1, day_3],
            "delivery_date": [day_1, None],
            "arrival_date": [day_1, day_4],
        }
    )
    result_should_be = pd.DataFrame(
        data={"shipment_id": ["1", "1", "2", "2", "2"], "dates": [day_1, day_2, day_3, day_4, day_5]}
    )
    result_should_be.loc[:, ["dates"]] = result_should_be["dates"].dt.date
    result = shipments_timelines(active_shipments_data_df=sh_df)
    pd.testing.assert_frame_equal(result, result_should_be)


def test_estimated_remaining_daily_workload():
    today = datetime.date(2020, 12, 28)
    sh_df = pd.DataFrame(
        data={
            "shipment_id": ["1", "2", "2"],
            "workflow_id": ["1", "2", "3"],
            "total_transit_time": [10, 12, 12],
            "created_at": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 26),
                datetime.datetime(2020, 12, 26),
            ],
            "total_workflow_weight": [1, 10, 50],
            "shipment_status": ["awaiting_booking", "booked", "booked"],
            "freight_method": ["air", "ocean", "ocean"],
            "freight_type": ["air", "ocean", "ocean"],
            "foresea_name": ["BATD", "BATE", "BATE"],
            "incoterm": ["fob", "ddp", "ddp"],
            "delivery_date": [None, None, None],
            "arrival_date": [None, None, None],
        }
    )
    timelines = shipments_timelines(sh_df)
    tasks_df = pd.DataFrame(
        data={
            "shipment_id": ["1", "2", "2", "2", "2"],
            "status": ["to_do", "to_do", "to_do", "done", "to_do"],
            "due_date": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 28),
                datetime.datetime(2020, 12, 29),
                datetime.datetime(2020, 12, 28),
                datetime.datetime(2020, 12, 30),
            ],
            "weight": [1, 6, 3, 3, 3],
        }
    )
    result_should_be = pd.DataFrame(
        data={
            "shipment_id": ["1", "2"],
            "total_workflows_weight": [1, 60],
            "shipment_status": ["awaiting_booking", "booked"],
            "freight_method": ["air", "ocean"],
            "freight_type": ["air", "ocean"],
            "foresea_name": ["BATD", "BATE"],
            "incoterm": ["fob", "ddp"],
            "total_transit_time": [10, 12],
            "created_at": [datetime.datetime(2020, 11, 15), datetime.datetime(2020, 12, 26)],
            "delivery_date": [None, None],
            "arrival_date": [None, None],
            "remaining_days": [0, 9],
            "total_tasks_weight": [1, 15],
            "estimated_remaining_daily_workload": [0.0, 5.0],
        }
    )
    result = estimated_remaining_daily_workload(sh_df, tasks_df, today, timelines)
    pd.testing.assert_frame_equal(result, result_should_be)


def test_shipments_daily_workload_timelines():
    today = datetime.date(2020, 12, 28)
    sh_df = pd.DataFrame(
        data={
            "created_at": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 26),
                datetime.datetime(2020, 12, 26),
            ],
            "shipment_id": [1, 2, 2],
            "workflow_id": ["1", "2", "3"],
            "total_transit_time": [10, 13, 13],
            "total_workflow_weight": [1, 10, 50],
            "shipment_status": ["awaiting_booking", "booked", "booked"],
            "freight_method": ["air", "ocean", "ocean"],
            "freight_type": ["air", "ocean", "ocean"],
            "foresea_name": ["BATD", "BATE", "BATE"],
            "incoterm": ["fob", "ddp", "ddp"],
            "delivery_date": [None, None, None],
            "arrival_date": [None, None, None],
        }
    )
    tasks_df = pd.DataFrame(
        data={
            "shipment_id": [1, 2, 2, 2, 2, 2, 2],
            "status": ["to_do", "to_do", "to_do", "done", "to_do", "to_do", "done"],
            "due_date": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 28),
                datetime.datetime(2020, 12, 29),
                datetime.datetime(2020, 12, 27),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 27),
            ],
            "updated_at": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 28),
                datetime.datetime(2020, 12, 29),
                datetime.datetime(2020, 12, 26),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 27),
            ],
            "done_date": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 28),
                datetime.datetime(2020, 12, 29),
                datetime.datetime(2020, 12, 26),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 27),
            ],
            "weight": [1, 1, 3, 3, 3, 10, 10],
        }
    )
    dates_sh_1 = pd.date_range(start=datetime.date(2020, 11, 15), periods=10)
    dates_sh_2 = pd.date_range(start=datetime.date(2020, 12, 26), periods=13)
    shipment_1_workload = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    shipment_2_workload = [3.0, 10.0, 1.0, 6.0, 16.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]
    result_should_be_1 = pd.DataFrame(
        data={"shipment_id": 1, "dates": dates_sh_1, "daily_workload": shipment_1_workload,}
    )
    result_should_be_2 = pd.DataFrame(
        data={"shipment_id": 2, "dates": dates_sh_2, "daily_workload": shipment_2_workload,}
    )
    result_should_be = pd.concat([result_should_be_1, result_should_be_2], ignore_index=True)
    result_should_be["dates"] = result_should_be["dates"].dt.date
    result = shipments_daily_workload_timelines(active_shipments_data_df=sh_df, tasks_df=tasks_df, today=today,)
    pd.testing.assert_frame_equal(result, result_should_be)


def test_shipments_daily_workload_timelines_with_tracking_dates():
    today = datetime.date(2020, 12, 28)
    sh_df = pd.DataFrame(
        data={
            "created_at": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 26),
                datetime.datetime(2020, 12, 26),
            ],
            "shipment_id": [1, 2, 2],
            "workflow_id": ["1", "2", "3"],
            "total_transit_time": [10, 13, 13],
            "total_workflow_weight": [1, 10, 50],
            "shipment_status": ["awaiting_booking", "booked", "booked"],
            "freight_method": ["air", "ocean", "ocean"],
            "freight_type": ["air", "ocean", "ocean"],
            "foresea_name": ["BATD", "BATE", "BATE"],
            "incoterm": ["fob", "ddp", "ddp"],
            "delivery_date": [datetime.datetime(2020, 11, 23), None, None],
            "arrival_date": [None, datetime.datetime(2021, 1, 6), datetime.datetime(2021, 1, 6),],
        }
    )
    tasks_df = pd.DataFrame(
        data={
            "shipment_id": [1, 2, 2, 2, 2, 2, 2],
            "status": ["to_do", "to_do", "to_do", "done", "to_do", "to_do", "done"],
            "due_date": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 28),
                datetime.datetime(2020, 12, 29),
                datetime.datetime(2020, 12, 27),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 27),
            ],
            "updated_at": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 28),
                datetime.datetime(2020, 12, 29),
                datetime.datetime(2020, 12, 26),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 27),
            ],
            "done_date": [
                datetime.datetime(2020, 11, 15),
                datetime.datetime(2020, 12, 28),
                datetime.datetime(2020, 12, 29),
                datetime.datetime(2020, 12, 26),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 30),
                datetime.datetime(2020, 12, 27),
            ],
            "weight": [1, 1, 3, 3, 3, 10, 10],
        }
    )
    dates_sh_1 = pd.date_range(start=datetime.date(2020, 11, 15), periods=10)
    dates_sh_2 = pd.date_range(start=datetime.date(2020, 12, 26), periods=13)
    shipment_1_workload = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    shipment_2_workload = [3.0, 10.0, 1.0, 6.0, 16.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]
    result_should_be_1 = pd.DataFrame(
        data={"shipment_id": 1, "dates": dates_sh_1, "daily_workload": shipment_1_workload}
    )
    result_should_be_2 = pd.DataFrame(
        data={"shipment_id": 2, "dates": dates_sh_2, "daily_workload": shipment_2_workload,}
    )
    result_should_be = pd.concat([result_should_be_1, result_should_be_2], ignore_index=True)
    result_should_be["dates"] = result_should_be["dates"].dt.date
    result = shipments_daily_workload_timelines(active_shipments_data_df=sh_df, tasks_df=tasks_df, today=today,)
    pd.testing.assert_frame_equal(result, result_should_be)
