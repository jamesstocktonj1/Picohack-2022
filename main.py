# Main File


from bendy.bendy import Bendy

testFiles = [
    "data/HatchetLane.gpx",
    "data/HatchetLane2.gpx",
    "data/NoName.gpx",
    "data/NorthLane.gpx",
    "data/PalaceLane.gpx",
    "data/YewTreeHeathRoad.gpx",
]

for f in testFiles:
    testRoad = Bendy()
    testRoad.load(f)

    #testRoad.show_significant()
    testRoad.show_bend()
    #testRoad.show()