from datetime import datetime

import schedule

import app.components.uavs.uavs_remote_controller as uavs_remote_controller

from app.lib.mongodb import mongodb
from app.components.uavs.get_uav_data import get_uav_data


def start_missions_statuses_check():
    schedule.every(10).seconds.do(_job)


def _job():
    _check_missions_that_should_start()

    _check_missions_that_are_going_to_starting_if_they_reach_it()

    _check_missions_that_are_going_to_destination_if_they_reach_it()

    _check_missions_that_reached_destination_if_they_should_complete_or_return()

    _check_missions_that_are_returning_to_starting_if_they_reach_it()


def _check_missions_that_should_start():
    missions = list(
        mongodb["missions"]
        .find({"status": "pending", "start_date": {"$lte": datetime.now()}})
        .sort("start_date", -1)
    )

    for mission in missions:
        missions_of_same_uav_that_are_still_not_completed = list(
            mongodb["missions"].find(
                {
                    "uav": mission["uav"],
                    "id": {"$ne": mission["id"]},
                    "status": {"$ne": "completed"},
                }
            )
        )

        if len(missions_of_same_uav_that_are_still_not_completed) != 0:
            continue

        if mission["record_video"]:
            # start video recording
            pass

        uav_data = get_uav_data(mission["uav"])

        lat = uav_data["gps"]["lat"]
        lon = uav_data["gps"]["lon"]

        RADIUS = 5

        close_to_starting_point = (
            abs(lat - mission["starting_point"]["lat"]) > RADIUS
            or abs(lon - mission["starting_point"]["lon"]) > RADIUS
        )

        if not close_to_starting_point:
            uavs_remote_controller.goto(
                mission["uav"], mission["starting_point"], mission["avg_speed"]
            )

            mongodb["missions"].update_one(
                {"id": mission["id"]},
                {
                    "$set": {
                        "status": "going to starting",
                        "real_starting_date": datetime.now(),
                    }
                },
            )
        else:
            uavs_remote_controller.goto(
                mission["uav"], mission["destination_point"], mission["avg_speed"]
            )

            mongodb["missions"].update_one(
                {"id": mission["id"]},
                {
                    "$set": {
                        "status": "going to destination",
                        "real_starting_date": datetime.now(),
                    }
                },
            )


def _check_missions_that_are_going_to_starting_if_they_reach_it():
    missions = list(mongodb["missions"].find({"status": "going to starting"}))

    for mission in missions:
        uav_data = get_uav_data(mission["uav"])

        lat = uav_data["gps"]["lat"]
        lon = uav_data["gps"]["lon"]

        RADIUS = 5

        if (
            abs(lat - mission["starting_point"]["lat"]) <= RADIUS
            or abs(lon - mission["starting_point"]["lon"]) <= RADIUS
        ):
            uavs_remote_controller.goto(
                mission["uav"], mission["destination_point"], mission["avg_speed"]
            )

            mongodb["missions"].update_one(
                {"id": mission["id"]},
                {
                    "$set": {
                        "status": "going to destination",
                    }
                },
            )


def _check_missions_that_are_going_to_destination_if_they_reach_it():
    missions = list(mongodb["missions"].find({"status": "going to destination"}))

    for mission in missions:
        uav_data = get_uav_data(mission["uav"])

        lat = uav_data["gps"]["lat"]
        lon = uav_data["gps"]["lon"]

        RADIUS = 5

        if (
            abs(lat - mission["destination_point"]["lat"]) <= RADIUS
            or abs(lon - mission["destination_point"]["lon"]) <= RADIUS
        ):
            mongodb["missions"].update_one(
                {"id": mission["id"]},
                {
                    "$set": {
                        "status": "reached destination",
                        "reaching_destination_date": datetime.now(),
                    }
                },
            )


def _check_missions_that_reached_destination_if_they_should_complete_or_return():
    missions = list(mongodb["missions"].find({"status": "reached destination"}))

    for mission in missions:
        if mission["should_return"]:
            uavs_remote_controller.goto(
                mission["uav"], mission["starting_point"], mission["avg_speed"]
            )

            mongodb["missions"].update_one(
                {"id": mission["id"]},
                {"$set": {"status": "returning to starting"}},
            )
        else:
            _complete_mission(mission)


def _check_missions_that_are_returning_to_starting_if_they_reach_it():
    missions = list(mongodb["missions"].find({"status": "returning to starting"}))

    for mission in missions:
        uav_data = get_uav_data(mission["uav"])

        lat = uav_data["gps"]["lat"]
        lon = uav_data["gps"]["lon"]

        RADIUS = 5

        if (
            abs(lat - mission["starting_point"]["lat"]) <= RADIUS
            or abs(lon - mission["starting_point"]["lon"]) <= RADIUS
        ):
            _complete_mission(mission)


def _complete_mission(mission):
    uavs_remote_controller.land(mission["uav"])

    datenow = datetime.now()
    real_starting_date = mission["real_starting_date"]

    diff = datenow - real_starting_date

    actual_duration_in_hours = diff.days * 24 + diff.seconds  # 3600

    mongodb["missions"].update_one(
        {"id": mission["id"]},
        {
            "$set": {
                "status": "completed",
                "success": True,
                "completion_date": datenow,
                "actual_duration_in_hours": actual_duration_in_hours,
            }
        },
    )

    if mission["record_video"]:
        # stop video recording
        pass
