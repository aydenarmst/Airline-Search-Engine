file = open("reducedAirports.csv", "r")
result = []
for line in file:
    add = True
    temp = line.split(",", 13)
    for country in result:
        if temp[3] == country[0]:
            country[1] += 1
            add = False
            break
    if add:
        result.append([temp[3], 1])

maximum = ("", 0)
for country in result:
    if country[1] > maximum[1]:
        maximum = country

print(f"{maximum[0]} has the most number of airports at {maximum[1]} airports.")