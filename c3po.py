#!/usr/bin/env python3
import json
import random
from time import sleep
import sys
from math import ceil


class C3PO:
    def __init__(self, millenniumFalconJsonFilePath):
        with open(millenniumFalconJsonFilePath) as f:
            data = json.load(f)
            self.autonomy = data["autonomy"]
            self.routes = data["routes"]

    def giveMeTheOdds(self, empireJsonFilePath):
        with open(empireJsonFilePath) as f:
            data = json.load(f)
            self.countdown = data["countdown"]
            bounty_hunters = data["bounty_hunters"]

            return self.calculateOdds(bounty_hunters)

    def get_valid_routes(
        self, routes, current_planet, current_day, current_fuel, autonomy
    ):
        # check si le vaisseau a assez d'autonomie pour les routes disponibles
        # depuis la planète actuelle et si on arrive à destination
        # avant la fin du countdown
        return [
            route
            for route in routes
            if route["origin"] == current_planet
            and route["travelTime"] <= current_fuel
            and route["travelTime"] <= autonomy
            and current_day + route["travelTime"] <= self.countdown
        ]

    def calculateOdds(self, empire):
        current_day = 0
        current_planet = "Tatooine"
        current_fuel = self.autonomy
        bounty_encounters = 0
        odds = 0

        while current_day < self.countdown:
            print(f"Start Day {current_day}: {current_planet} - {current_fuel} fuel")
            sleep(1)

            if any(
                bounty["planet"] == current_planet and bounty["day"] == current_day
                for bounty in empire
            ):
                print("Bounty hunter on the planet... tread carefully young padawan")
                bounty_encounters += 1
                if bounty_encounters == 1:
                    odds += 1 / 10
                if bounty_encounters > 1:
                    odds += 9 ** (bounty_encounters - 1) / 10 ** (bounty_encounters)

            valid_routes = self.get_valid_routes(
                self.routes, current_planet, current_day, current_fuel, self.autonomy
            )
            if not valid_routes:
                # soit pas de route possible soit pas assez de fuel, on refuel 1 jour
                # TODO: gérer le cas où il n'y a pas de route possible
                print(f"Refueling for the day...")
                current_day += 1
                current_fuel = self.autonomy
                continue
            else:
                # select soit la route qui amène à Endor soit une autre route random
                route = next(
                    (
                        route
                        for route in valid_routes
                        if route["destination"] == "Endor"
                    ),
                    random.choice(valid_routes),
                )
            print(
                f"End Day {current_day}: {current_planet} - Destination: {route['destination']} - Fuel needed: {route['travelTime']} - Current fuel: {current_fuel}"
            )
            current_planet = route["destination"]
            current_fuel -= route["travelTime"]
            current_day += route["travelTime"]
            if current_planet == "Endor":
                return 1 - odds
        return 0


if __name__ == "__main__":
    c3po = C3PO(sys.argv[1])
    res = c3po.giveMeTheOdds(sys.argv[2])
    if res != 0:
        print("the odds are in our favor - {:0.2f}".format(res))
    else:
        print("never tell me the odds - 0")
