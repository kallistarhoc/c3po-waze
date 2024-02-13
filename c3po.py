#!/usr/bin/env python3
import json
from time import sleep
import sys
from collections import defaultdict
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class C3PO:
    def __init__(self, millenniumFalconJsonFilePath: str):
        with open(millenniumFalconJsonFilePath) as f:
            data = json.load(f)
            self.autonomy = data["autonomy"]
            self.routes = data["routes"]
            self.routes_to_endor = self.find_routes_to_endor()

    def giveMeTheOdds(self, empireJsonFilePath: str):
        with open(empireJsonFilePath) as f:
            data = json.load(f)
            self.countdown = data["countdown"]
            self.empire = data["bounty_hunters"]
            return self.calculateOdds()

    def find_routes(
        self,
        graph: dict,
        start: str,
        end: str,
        path: list = [],
        visited: set = set(),
        total_time: int = 0,
    ):
        path = path + [start]
        if start == end:
            return [{"path": path, "travel_time": total_time}]
        if start not in graph:
            return []
        return [
            new_path
            for node, travel_time in graph[start]
            if node not in visited
            for new_path in self.find_routes(
                graph,
                node,
                end,
                path,
                visited.union({node}),
                total_time + travel_time,
            )
        ]

    def find_routes_to_endor(self):
        graph = defaultdict(list)
        for route in self.routes:
            graph[route["origin"]].append((route["destination"], route["travelTime"]))

        all_routes = self.find_routes(graph, "Tatooine", "Endor")
        return all_routes

    def get_valid_routes(
        self,
        routes: dict,
        current_planet: str,
        current_day: str,
        current_fuel: int,
        autonomy: int,
    ):
        return [
            route
            for route in routes
            if route["origin"] == current_planet
            and route["travelTime"] <= current_fuel
            and route["travelTime"] <= autonomy
            and current_day + route["travelTime"] <= self.countdown
        ]

    def is_bounty_hunter_present(self, planet: str, day: int):
        return any(
            bounty["planet"] == planet and bounty["day"] == day
            for bounty in self.empire
        )

    def r2d2_logging(self, message: str):
        logger.info(message)

    def path_loop(self, path: dict):
        current_day = 0
        current_fuel = self.autonomy
        current_planet = path["path"][0]
        odds = 0
        bounty_encounters = 0
        counter = 1
        while counter:
            self.r2d2_logging(
                f"Start Day {current_day}: {current_planet} - {current_fuel} fuel"
            )
            sleep(1)
            if self.is_bounty_hunter_present(current_planet, current_day):
                self.r2d2_logging(
                    "Bounty hunter on the planet... tread carefully young padawan"
                )
                bounty_encounters += 1
                if bounty_encounters == 1:
                    odds += 1 / 10
                if bounty_encounters > 1:
                    odds += 9 ** (bounty_encounters - 1) / 10 ** (bounty_encounters)
            next_planet = path["path"][counter]
            next_planet_travel_time = next(
                route["travelTime"]
                for route in self.routes
                if route["origin"] == current_planet
                and route["destination"] == next_planet
            )
            if next_planet_travel_time > current_fuel:
                self.r2d2_logging(f"Day {current_day}: refueling on {current_planet}")
                current_day += 1
                current_fuel = self.autonomy
                continue
            if self.is_bounty_hunter_present(next_planet, current_day + 1):
                self.r2d2_logging("Bounty hunters on the next planet...")
                if current_day + 1 < self.countdown:
                    self.r2d2_logging(
                        f"... let's wait a day on {current_planet} to avoid them, we have time"
                    )
                    current_day += 1
                    continue
                else:
                    self.r2d2_logging(
                        f"... we don't have time to wait, we must go to {next_planet}, we'll have to face the odds"
                    )
            self.r2d2_logging(f"Day {current_day}: traveling to {next_planet}")
            current_planet = next_planet
            current_fuel -= next_planet_travel_time
            current_day += next_planet_travel_time
            counter += 1
            if current_planet == "Endor":
                return 1 - odds
            if counter == len(path["path"]):
                return 0
        return 0

    def calculateOdds(self):
        odds = []
        valid_paths = []
        for path in self.routes_to_endor:
            if path["travel_time"] < self.countdown:
                valid_paths.append(path)
        if not valid_paths:
            return 0
        if len(valid_paths) >= 1:
            for path in valid_paths:
                odds.append(self.path_loop(path))
        return max(odds)


if __name__ == "__main__":
    c3po = C3PO(sys.argv[1])
    res = c3po.giveMeTheOdds(sys.argv[2])
    if res != 0:
        print("the odds are in our favor - {:0.2f}".format(res))
    else:
        print("never tell me the odds - 0")
