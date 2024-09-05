import heapq
import time

# Read the data file
with open('A Star Model/data_1.txt', 'r') as file:
    grid_data = [list(line.strip()) for line in file]

# Define the movements (up, down, left, right, diagonal)
movements = [(-1, 0), (1, 0), (0, -1), (0, 1),
             (-1, -1), (-1, 1), (1, -1), (1, 1)]

# Find the dimensions of the grid
num_rows = len(grid_data)
num_cols = len(grid_data[0])

# Find the start and target positions
start_pos = None
target_pos = None
for i in range(num_rows):
    for j in range(num_cols):
        if grid_data[i][j] == 'S':
            start_pos = (i, j)
        elif grid_data[i][j] == 'T':
            target_pos = (i, j)

# Define a heuristic function (Euclidean distance)


def heuristic(current_pos, target_pos):
    return ((current_pos[0] - target_pos[0]) ** 2 + (current_pos[1] - target_pos[1]) ** 2) ** 0.5

# Implement the A* algorithm


def find_path(start_pos, target_pos, grid_data):
    # Initialize the open and closed sets
    open_set = []
    heapq.heappush(open_set, (0, start_pos, []))
    closed_set = set()
    costs = {start_pos: 0}

    # Maintain a dictionary to store the parent of each node
    parent_map = {start_pos: None}

    while open_set:
        current_cost, current_pos, current_path = heapq.heappop(open_set)

        if current_pos == target_pos:
            # Reconstruct path from target to start
            path = []
            while current_pos:
                path.append(current_pos)
                current_pos = parent_map.get(current_pos)
            return path[::-1]  # Reverse the path

        closed_set.add(current_pos)

        for movement in movements:
            new_row = current_pos[0] + movement[0]
            new_col = current_pos[1] + movement[1]
            new_pos = (new_row, new_col)

            if 0 <= new_row < num_rows and 0 <= new_col < num_cols:
                if grid_data[new_row][new_col] != 'W':
                    new_cost = current_cost + 1
                    new_heuristic = heuristic(new_pos, target_pos)
                    new_total_cost = new_cost + new_heuristic

                    if new_pos not in closed_set and (new_pos not in costs or new_cost < costs[new_pos]):
                        costs[new_pos] = new_cost
                        parent_map[new_pos] = current_pos
                        heapq.heappush(
                            open_set, (new_total_cost, new_pos, current_path + [current_pos]))

    # No path found
    return None


start_time = time.time()

# Find the optimal path
optimal_path = find_path(start_pos, target_pos, grid_data)

# Record the end time and calculate time taken
end_time = time.time()
time_taken = end_time - start_time

# Count the number of steps in the path
num_steps = len(optimal_path) if optimal_path else 0

# Mark the path cells and targets in the grid data
if optimal_path:
    for pos in optimal_path:
        row, col = pos
        if grid_data[row][col] == 'T':
            grid_data[row][col] = 'X'
        else:
            grid_data[row][col] = 'P'

# Print the final grid data
# Save the final grid data to a file
with open('A Star Model/Result_data_3.txt', 'w') as file:
    for row in grid_data:
        file.write(' '.join(row) + '\n')

    # Add separation lines and append time and steps information
    file.write('\n' + '-' * 40 + '\n')
    file.write(f'Time Taken: {time_taken:.2f} seconds\n')
    file.write(f'Steps Taken: {num_steps}\n')

for row in grid_data:
    print(' '.join(row))
