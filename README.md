# C3PO-Waze

## Description
C3PO-Waze is a new feature for our favorite robot C3PO.
He is now able to tell Han and Chewie the precise odds to get from point A to point B without getting caught by the Empire's bounty hunters.
As we all know, Han loves knowing the odds.

## How to Launch
To call on C3PO's super technical path finding algorithm, follow these steps:

1. Clone the repository
```
git clone git@github.com:kallistarhoc/c3po-waze.git
```
2. Move into the directory
```
cd c3po-waze
```
3. Make sure you have python3 installed
```
$dataiku@user$ python3 --version
Python 3.11.5
```
4. Give C3PO the needed JSON files
```
python3 c3po.py millennium-falcon.json empire.json
```

Here's how the JSON files should look like:
- millennium-falcon.json
```
{
  "autonomy": 6, 
  "routes": [
    {"origin": "Tatooine", "destination": "Dagobah", "travelTime": 6 },
    {"origin": "Dagobah", "destination": "Endor", "travelTime": 4 },
    {"origin": "Dagobah", "destination": "Hoth", "travelTime": 1 },
    {"origin": "Hoth", "destination": "Endor", "travelTime": 1 },
    {"origin": "Tatooine", "destination": "Hoth", "travelTime": 6 }
  ]
}
```

- empire.json 
```
{
  "countdown": 10, 
  "bounty_hunters": [
    {"planet": "Hoth", "day": 6 }, 
    {"planet": "Hoth", "day": 7 },
    {"planet": "Hoth", "day": 8 }
  ]
}
```