import heapq

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
    closed_set = set()

    # Initialize the starting node with a cost of 0
    start_node = (0, start_pos, [])
    heapq.heappush(open_set, start_node)

    while open_set:
        # Pop the node with the lowest cost from the open set
        current_cost, current_pos, current_path = heapq.heappop(open_set)

        # Check if the current position is the target
        if current_pos == target_pos:
            return current_path

        # Add the current position to the closed set
        closed_set.add(current_pos)

        # Explore the neighboring cells
        for movement in movements:
            new_row = current_pos[0] + movement[0]
            new_col = current_pos[1] + movement[1]
            new_pos = (new_row, new_col)

            # Check if the new position is within the grid boundaries
            if new_row >= 0 and new_row < num_rows and new_col >= 0 and new_col < num_cols:
                # Check if the new position is passable (not an obstacle)
                if grid_data[new_row][new_col] != 'W':
                    # Calculate the cost to reach the new position
                    new_cost = current_cost + 1

                    # Calculate the heuristic value for the new position
                    new_heuristic = heuristic(new_pos, target_pos)

                    # Calculate the total estimated cost for the new position
                    new_total_cost = new_cost + new_heuristic

                    # Check if the new position is already in the closed set
                    if new_pos in closed_set:
                        continue

                    # Check if the new position is already in the open set
                    is_in_open_set = False
                    for i, (cost, pos, path) in enumerate(open_set):
                        if pos == new_pos:
                            is_in_open_set = True
                            if new_cost < cost:
                                # Update the cost and path for the new position
                                open_set[i] = (new_cost, new_pos,
                                               current_path + [new_pos])
                                heapq.heapify(open_set)
                            break
                    if not is_in_open_set:
                        # Add the new position to the open set
                        heapq.heappush(
                            open_set, (new_total_cost, new_pos, current_path + [new_pos]))

    # No path found
    return None


# Find the optimal path
optimal_path = find_path(start_pos, target_pos, grid_data)

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
with open('A Star Model/Result_data_1.txt', 'w') as file:
    for row in grid_data:
        file.write(' '.join(row) + '\n')

for row in grid_data:
    print(' '.join(row))
