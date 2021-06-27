f = open("./txt_Spreads/2017.txt", "r")


L = 0
W = 0
N = 0
total = 0
teams = 0
for line in f.readlines():
    splitLine = line.split()
    for element in splitLine:
        if (element == "L"):
            L = L + 1
        elif (element == "W"):
            W = W + 1
        elif (element == "N"):
            N = N + 1
    for i in range(len(splitLine)):
        if (splitLine[i] == "PSR:"):
            teams = teams + 1
            games = splitLine[i+1].split("-")
            for i in range(len(games)):
                total = total + int(games[i])
print ("L: " + str(L) + "\nW: " + str(W) + "\nN: " + str(N) + "\nTotal: " + str(total) + "\nTeams: " + str(teams))
