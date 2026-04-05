import time, Main, ListGen, csv

def Test():
    testInputVals = [[100, 250, 0.01], [1000, 250, 0.01], [100, 2500, 0.01], [100, 250, 0.1], [10, 250, 0.01], [100, 25, 0.01], [100, 250, 0.001]]
    testNames = ["Control", "High Pop", "High Gen", "High Mut", "Low Pop", "Low Gen", "Low Mut"]
    testResults = []
    ListGen.Generate([1590, 6])
    for x in range(0, len(testInputVals)):
        inputVals = testInputVals[x]
        name = testNames[x]
        startTime = time.time()
        output = Main.Run(inputVals)
        fitOverTime = output[0]
        greedyFit = output[1]
        timeDuration = time.time() - startTime
        testResults.append([name, inputVals, fitOverTime, greedyFit, timeDuration])

    csv_filepath = "Data/Aglo Parameter Test Results.csv"

    # Define the field names (headers)
    fieldnames = ["Name", "Input Values", "Fitness over Time", "Greedy Algorithm Fitness", "Duration of Run"]

    data = []
    data.append(fieldnames)

    for test in testResults:
        name, inputVals, fitOverTime, greedyFit, timeDuration = test
        data.append([name, inputVals, fitOverTime, greedyFit, timeDuration])

    # Writing to CSV
    with open(csv_filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    testInputVals = [[1590, 6], [996, 6], [1590, 3], [3180, 6], [1590, 12]]
    testNames = ["Control", "Low Aca", "Low Ratio", "High Aca", "High Ratio"]
    testResults = []
    for x in range(0, len(testInputVals)):
        inputVals = testInputVals[x]
        name = testNames[x]
        startTime = time.time()
        ListGen.Generate(inputVals)
        output = Main.Run([100, 250, 0.01])
        fitOverTime = output[0]
        greedyFit = output[1]
        timeDuration = time.time() - startTime
        testResults.append([name, inputVals, fitOverTime, greedyFit, timeDuration])

    csv_filepath = "Data/Input Value Test Results.csv"

    # Define the field names (headers)
    fieldnames = ["Name", "Input Values", "Fitness over Time", "Greedy Algorithm Fitness", "Duration of Run"]

    # Writing to CSV
    with open(csv_filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(testResults)

Test()