#!/usr/bin/env python3
import json
import random
import sys


class C3PO:
    def __init__(self, millenniumFalconJsonFilePath):
        with open(millenniumFalconJsonFilePath) as f:
            data = json.load(f)
            self.autonomy = data["autonomy"]
            self.routes = data["routes"]

    def giveMeTheOdds(self, empireJsonFilePath):
        with open(empireJsonFilePath) as f:
            data = json.load(f)
            countdown = data["countdown"]

            return self.calculateOdds(countdown)

    def calculateOdds(self, countdown):
        current_day = 0
        current_planet = "Tatooine"
        current_fuel = self.autonomy

        while current_day < countdown:
            print(f"Start Day {current_day}: {current_planet} - {current_fuel} fuel")
            # check si le vaisseau a assez d'autonomie pour les routes disponibles depuis la planète actuelle
            valid_routes = [
                route
                for route in self.routes
                if route["origin"] == current_planet
                and route["travelTime"] <= current_fuel
            ]

            if not valid_routes:
                # soit pas de route possible soit pas assez de fuel, on refuel 1 jour
                # TODO: gérer le cas où il n'y a pas de route possible
                current_day += 1
                current_fuel += 1
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
                current_planet = route["destination"]
            if current_planet == "Endor":
                return 1
            current_fuel -= route["travelTime"]
            current_day += route["travelTime"]
            print(f"End Day {current_day}: {current_planet} - {current_fuel} fuel")
        return 0


if __name__ == "__main__":
    c3po = C3PO(sys.argv[1])
    res = c3po.giveMeTheOdds(sys.argv[2])
    if res != 0:
        print(f"the odds are in our favor - {res}")
    else:
        print("never tell me the odds - 0")
