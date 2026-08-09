from ortools.sat.python import cp_model
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


class sugarcaneSolver:
    def __init__(self, n: int):

        self.n = n
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

        self.x = {}

        for i in range(n):
            for j in range(n):
                self.x[(i,j)] = self.model.new_bool_var(f"x_{i}_{j}")

        

    def objective(self):
        f = 0

        for i in range(self.n):
            for j in range(self.n):
                f += self.x[(i,j)]

        return f

        
    def N(self, i:int, j:int):
        positions = []

        for p in range(self.n):
            for q in range(self.n):

                if abs(p-i) + abs(q-j) == 1:
                    positions.append((p,q))

        return positions

    def constraint(self):

        for i in range(self.n):
            for j in range(self.n):
                totalWater = 0

                for pos in self.N(i,j):
                    totalWater += 1-self.x[pos]

                self.model.add(totalWater >= self.x[(i,j)])


    def solve(self):
        status = self.solver.solve(self.model)

        return status

    def plot(self):

        grid = [ [0]*self.n for _ in range(self.n)]

        for i in range(self.n):
            for j in range(self.n):
                grid[i][j] = self.solver.value(self.x[(i,j)])

        cmap = ListedColormap(["blue", "green"])

        fig, ax = plt.subplots()

        ax.imshow(grid, cmap=cmap, vmin=0, vmax=1)

        ax.set_xticks(range(self.n))
        ax.set_yticks(range(self.n))

        ax.set_xticklabels(range(1, self.n + 1))
        ax.set_yticklabels(range(1, self.n + 1))

        ax.xaxis.tick_top()
        ax.xaxis.set_label_position("top")

        ax.set_xticks([x - 0.5 for x in range(1, self.n)], minor=True)
        ax.set_yticks([y - 0.5 for y in range(1, self.n)], minor=True)

        ax.grid(which="minor", linewidth=1)
        ax.tick_params(which="minor", bottom=False, left=False)

        fig.text(
            0.5,
            0.02,
            f"Optimal: {int(self.solver.objective_value)} sugarcane, coverage {int(self.solver.objective_value) / (self.n*self.n)}",
            ha="center"
        )

        plt.show()

o = sugarcaneSolver(5)

o.model.maximize(o.objective())
o.constraint()

print(o.solve())

o.plot()