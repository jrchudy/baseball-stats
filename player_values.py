import csv

# dictionary of player stats
# key = playeer name
# value = player's stat row[]
battingStatsDict = {}

# dictionary of player values
# key = player name
# value = adjusted value
battingValuesDict = {}

with open('batting2016.csv', 'rb') as battingFile:
    battingReader = csv.reader(battingFile)
    i = 0
    for row in battingReader:
        if i == 0:
            i += 1
            continue

        key = row[1].split('\\')[0]
        if key.find('*') > -1:
            key = key.split('*')[0]
        battingStatsDict[key] = row
    battingFile.closed

# ['Rk', 'Name', 'Age', 'Tm', 'Lg', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'BA', 'OBP', 'SLG', 'OPS', 'OPS+', 'TB', 'GDP', 'HBP', 'SH', 'SF', 'IBB', 'Pos Summary']
# indices in battingStatsDict[x]:
# R = 8                     [2]
# 1B = 9 - (10 + 11 + 12)   [1]
# 2B = 10                   [2]
# 3B = 11                   [3]
# HR = 12                   [4]
# RBI = 13                  [2]
# SB = 14                   [2]
# CS = 15                   [-2]
# BB = 16                   [0.5]
# SO = 17                   [-1]
# GDP = 24                  [-0.5]

# {
#   stat: [index, modifier]
# }
battingTransform = {
    'R': [8, 2],
    '1B': [None, 1],
    '2B': [10, 2],
    '3B': [11, 3],
    'HR': [12, 4],
    'RBI': [13, 2],
    'SB': [14, 2],
    'CS': [15, -2],
    'BB': [16, 0.5],
    'SO': [17, -1],
    'GDP': [24, -0.5]
}

for key1 in battingStatsDict.iteritems():
    playerName = key1[0]
    # array of stat values
    statRow = key1[1]
    battingValuesDict[playerName] = 0

    for key2 in battingTransform.iteritems():
        stat = key2[0]
        index = key2[1][0]
        modifier = key2[1][1]
        if stat == '1B':
            value1B = float(statRow[9]) - (float(statRow[10]) + float(statRow[11]) + float(statRow[12]))
            battingValuesDict[playerName] += value1B
            continue
        battingValuesDict[playerName] += float(statRow[index]) * modifier

    # print battingValuesDict[playerName]

# dictionary of player stats
# key = player name
# value = player's stat row
fieldingStatsDict = {}

with open('fielding2016.csv', 'rb') as fieldingFile:
    fieldingReader = csv.reader(fieldingFile)
    i = 0
    for row in fieldingReader:
        if i == 0:
            i += 1
            continue

        key = row[1].split('\\')[0]
        fieldingStatsDict[key] = row
    fieldingFile.closed

# ['Rk', 'Name', 'Age', 'Tm', 'Lg', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 'Fld%', 'Rtot', 'Rtot/yr', 'Rdrs', 'Rdrs/yr', 'RF/9', 'RF/G', 'Pos Summary']
# indices in fieldingStatsDict[x]:
# E = 12                               [-1]
# OFA = if indexOf('OF') in 21 { 11 }  [1]

for key1 in fieldingStatsDict.iteritems():
    playerName = key1[0]
    # array of stat values
    statRow = key1[1]
     # calculate errors value
    fieldingValue = (float(statRow[12]) * -1)

    #add OFA assists if OF in position summary
    if statRow[21].find('OF'):
        fieldingValue += float(statRow[11])


    if not playerName in battingValuesDict:
        battingValuesDict[playerName] = 0

    battingValuesDict[playerName] += fieldingValue

    if battingValuesDict[playerName] > 700:
        print (playerName, ": ", battingValuesDict[playerName])
