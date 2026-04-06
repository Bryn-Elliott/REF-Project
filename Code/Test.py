import time, Main, ListGen, csv, openpyxl

def Test():
    # testInputVals = [[100, 250, 0.01], [200, 250, 0.01], [100, 500, 0.01], [100, 250, 0.1], [10, 250, 0.01], [100, 25, 0.01], [100, 250, 0.001]]
    # testNames = ["Control", "High Pop", "High Gen", "High Mut", "Low Pop", "Low Gen", "Low Mut"]
    # testResults = []
    # ListGen.Generate([1590, 6])
    # for x in range(0, len(testInputVals)):
    #     inputVals = testInputVals[x]
    #     name = testNames[x]
    #     startTime = time.time()
    #     output = Main.Run(inputVals)
    #     fitOverTime = output[0]
    #     greedyFit = output[1]
    #     timeDuration = time.time() - startTime
    #     testResults.append([name, inputVals, fitOverTime, greedyFit, timeDuration])

    # csvFilepath = "Data/Aglo Parameter Test Results.csv"

    # # Define the field names (headers)
    # generalData = []
    # generalData.append(["Name", "Input Values", "Final Fitness", "Greedy Fitness", "Duration of Run"])

    fitnessData = []

    # for test in testResults:
    #     name, inputVals, fitOverTime, greedyFit, timeDuration = test
    #     generalData.append([name, inputVals, fitOverTime[-1][1], greedyFit, timeDuration])
    #     fitnessData.append(fitOverTime)

    # # Writing to CSV
    # with open(csvFilepath, mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerows(generalData)


    testInputVals = [[1590, 6], [996, 6], [1590, 3], [3180, 6], [1590, 12]]
    testNames = ["Control", "Low Aca", "Low Ratio", "High Aca", "High Ratio"]
    testResults = []
    for x in range(0, len(testInputVals)):
        inputVals = testInputVals[x]
        name = testNames[x]
        startTime = time.time()
        ListGen.Generate(inputVals)
        output = Main.Run([100, 250 , 0.01])
        fitOverTime = output[0]
        greedyFit = output[1]
        timeDuration = time.time() - startTime
        testResults.append([name, inputVals, fitOverTime, greedyFit, timeDuration])

    csvFilepath = "Data/Input Value Test Results.csv"

    generalData = []
    generalData.append(["Name", "Input Values", "Final Fitness", "Greedy Fitness", "Duration of Run"])
    
    for test in testResults:
        name, inputVals, fitOverTime, greedyFit, timeDuration = test
        generalData.append([name, inputVals, fitOverTime[-1][1], greedyFit, timeDuration])
        fitnessData.append(fitOverTime)

    # Writing to CSV
    with open(csvFilepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(generalData)
    
    csvFilepaths = ["Data/IV/Control Test Results.csv","Data/IV/Low Aca Test Results.csv","Data/IV/Low Ratio Test Results.csv","Data/IV/High Aca Test Results.csv","Data/IV/High Ratio Test Results.csv"]

    for x in range(0, len(csvFilepaths) - 1):
        with open(csvFilepaths[x], mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Generation", "Fitness"])
            writer.writerows(fitnessData[x])

Test()