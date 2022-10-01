# Main File


from bendy import bendy


testFile = "data/5032225.gpx"

testRoad = bendy.Road()
testRoad.load(testFile)

testRoad.show()