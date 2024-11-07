NWCOR = "North-West Corner Method"
VOGEL = "Vogel's Approximation Method"
RUSSELL = "Russell's Approximation Method"

class Transportation:
    nOfSrs : int
    nOfDest : int
    moveCosts : list
    supply : list
    demand : list

    def __init__(self, numberOfSources: int, numberOfDestinations: int) -> None:
        self.nOfSrs = numberOfSources
        self.nOfDest = numberOfDestinations
        self.moveCosts = [[] for _ in range(self.nOfSrs)]

    def inputMoveCosts(self) -> None:
        for i in range(self.nOfSrs):
            print("Enter move costs for S{}: ".format(i + 1), end='')
            temp = list(map(int, input().split()))
            if len(temp) != self.nOfDest:
                print("Error: wrong number of costs given!")
                exit()
            if sorted(temp)[0] < 0:
                print("Error: negative cost given!")
                exit()
            self.moveCosts[i] = temp.copy()
            temp.clear()
        self.supply = list(map(int, input("Enter supply for sources S{} - S{}: ".format(1, self.nOfSrs)).split()))
        if len(self.supply) != self.nOfSrs:
            print("Error: incorrect number of instances of supply!")
            exit()
        self.demand = list(map(int, input("Enter demand for destinations D{} - D{}: ".format(1, self.nOfDest)).split()))
        if len(self.demand) != self.nOfDest:
            print("Error: incorrect number of instances of demand!")
            exit()
    
    def northWestCornerMethod(self) -> list:
        result = [[0 for _ in range(self.nOfDest)] for _ in range(self.nOfSrs)]
        n, m = 0, 0
        supply = self.supply.copy()
        demand = self.demand.copy()
        while n < self.nOfSrs - 1 or m < self.nOfDest - 1:
            if supply[n] < demand[m]:
                demand[m] -= supply[n]
                result[n][m] = supply[n]
                supply[n] = 0
                n = min(self.nOfSrs - 1, n + 1)
            else:
                supply[n] -= demand[m]
                result[n][m] = demand[m]
                demand[m] = 0
                m = min(self.nOfDest - 1, m + 1)
        result[n][m] = max(supply[n], demand[m])
        return result

    def vogelApproximationMethod(self) -> list:
        result = [[0 for _ in range(self.nOfDest)] for _ in range(self.nOfSrs)]
        supply = self.supply.copy()
        demand = self.demand.copy()
        moveCosts = self.moveCosts.copy()
        while sum(supply) > 0 and sum(demand) > 0:
            row_penalties = []
            col_penalties = []
            # Calculate row penalties
            for i in range(self.nOfSrs):
                if supply[i] > 0:
                    temp_arr = []
                    for j in range(self.nOfDest):
                        if demand[j] > 0:
                            temp_arr.append(moveCosts[i][j])
                    temp_arr = sorted(temp_arr)[:2]
                    row_penalties.append((abs(temp_arr[0] - temp_arr[1]) if len(temp_arr) > 1 else 1e9, i))
                    temp_arr.clear()
                else:
                    continue
            # Calculate column penalties
            for j in range(self.nOfDest):
                if demand[j] > 0:
                    temp_arr = []
                    for i in range(self.nOfSrs):
                        if supply[i] > 0:
                            temp_arr.append(moveCosts[i][j])
                    temp_arr = sorted(temp_arr)[:2]
                    col_penalties.append((abs(temp_arr[0] - temp_arr[1]) if len(temp_arr) > 1 else 1e9, j))
                    temp_arr.clear()
                else:
                    continue
            max_row_penalty = max(row_penalties, key=lambda x: x[0])
            max_col_penalty = max(col_penalties, key=lambda x: x[0])
            # Find missing indecies by finding min in known row/column
            if max_row_penalty[0] > max_col_penalty[0]:
                row = max_row_penalty[1]
                col = min([(moveCosts[row][j] if demand[j] > 0 else 1e9, j) for j in range(self.nOfDest)])[1]
            else:
                col = max_col_penalty[1]
                row = min([(moveCosts[i][col] if supply[i] > 0 else 1e9, i) for i in range(self.nOfSrs)])[1]
            # Allocate resources
            allocation = min(supply[row], demand[col])
            result[row][col] = allocation
            supply[row] -= allocation
            demand[col] -= allocation

        return result

    def russellApproximationMethod(self) -> list:
        result = [[0 for _ in range(self.nOfDest)] for _ in range(self.nOfSrs)]
        demand = self.demand.copy()
        supply = self.supply.copy()
        moveCosts = [[self.moveCosts[i][j] for j in range(self.nOfDest)] for i in range(self.nOfSrs)]
        while sum(supply) > 0 and sum(demand) > 0:
            # Find opportunity costs for rows and columns
            row_costs = []
            for i in range(self.nOfSrs):
                if supply[i] > 0:
                    temp_arr = []
                    for j in range(self.nOfDest):
                        if demand[j] > 0:
                            temp_arr.append(moveCosts[i][j])
                        else:
                            temp_arr.append(-1)
                    row_costs.append(sorted(temp_arr)[-1])
                else:
                    row_costs.append(-1)
            col_costs = []
            for j in range(self.nOfDest):
                if demand[j] > 0:
                    temp_arr = []
                    for i in range(self.nOfSrs):
                        if supply[i] > 0:
                            temp_arr.append(moveCosts[i][j])
                        else:
                            temp_arr.append(-1)
                    col_costs.append(sorted(temp_arr)[-1])
                else:
                    col_costs.append(-1)
            # Calculate values for costTable to take opportinity costs
            # into account
            costTable = moveCosts.copy()
            for i in range(self.nOfSrs):
                for j in range(self.nOfDest):
                    if supply[i] > 0 and demand[j] > 0:
                        costTable[i][j] -= row_costs[i] + col_costs[j]
                    else:
                        costTable[i][j] = 1e9
            # Find min value in costTable while keeping track of empty supplies and demand
            min_values = []
            for i in range(self.nOfSrs):
                if supply[i] > 0:
                    temp_arr = []
                    for j in range(self.nOfDest):
                        if demand[j] > 0:
                            temp_arr.append((costTable[i][j], i, j))
                        else:
                            temp_arr.append((1e9, i, j))
                    min_values.append(sorted(temp_arr, key=lambda x: x[0])[0])
                else:
                    continue
            min_val = sorted(min_values, key=lambda x: x[0])[0]
            # Allocate to route - min in cost table
            row = min_val[1]
            col = min_val[2]
            allocation = min(supply[row], demand[col])
            supply[row] -= allocation
            demand[col] -= allocation
            result[row][col] = allocation
        return result
            

    def calculateTotalCost(self, allocationTable: list) -> int:
        total = 0
        for i in range(self.nOfSrs):
            for j in range(self.nOfDest):
                total += self.moveCosts[i][j] * allocationTable[i][j]
        return total

    def printTable(self, methodName : str, table : list):
        print('-' * (len(methodName) + 1))
        print(methodName + ":")
        print('-' * (len(methodName) + 1))
        print('S\\D', end='\t')
        for j in range(self.nOfDest):
            print("D{}".format(j + 1), end='\t')
        print('')
        for i in range(self.nOfSrs):
            print("S{}".format(i + 1), end='\t')
            for j in range(self.nOfDest):
                print(table[i][j], end='\t')
            print('')
        total_string = "Total cost: {}".format(self.calculateTotalCost(table))
        print("=" * (len(total_string) + 2))
        print(total_string)

    


if __name__ == "__main__":
    tr = Transportation(4, 5)
    tr.inputMoveCosts()
    
    tr.printTable(NWCOR, tr.northWestCornerMethod())
    tr.printTable(VOGEL, tr.vogelApproximationMethod())
    tr.printTable(RUSSELL, tr.russellApproximationMethod())
