#!/usr/bin/env python3

import json
import gpxpy
import gpxpy.gpx

def load_data(fname, mode="ANALOG"):
    """ Load the JSON extracted from https://papasys.com/mode-map/ """

    data = {}

    with open(fname) as f:
        map_data = json.load(f)

    for marker in map_data["map_markers"].values():
        if marker["marker_category"] == mode:
            lat, lng = marker["latlng"].split(',')
            data[marker["title"]] = {
                    "note": marker["info_window_content"],
                    "latitude": float(lat),
                    "longitude": float(lng)
            }


    return data

def main():

    map_data = load_data("mode-map.json")
    gpx = gpxpy.gpx.GPX()

    for key, value in map_data.items():
        waypoint = gpxpy.gpx.GPXWaypoint()
        gpx.waypoints.append(waypoint)
        waypoint.name = key
        waypoint.latitude = value["latitude"]
        waypoint.longitude = value["longitude"]
        waypoint.symbol = "Tall Tower"
        waypoint.comment = value["note"]
        waypoint.description = value["note"]
        waypoint.type = "Repeater Site"

    print('Created GPX:', gpx.to_xml())
    with open("papa-analog.gpx", "w") as f:
        f.write(gpx.to_xml())

if __name__ == "__main__":
    main()
