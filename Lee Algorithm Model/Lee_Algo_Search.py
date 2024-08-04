from collections import deque

# Read the map from the file
with open('Lee Algorithm Model/round_3.txt', 'r') as file:
    map_data = [list(line.strip()) for line in file]

# Define the visibility range
visibility_range = 10

dx = [-1, -1, -1, 0, 0, 1, 1, 1]
dy = [-1, 0, 1, -1, 1, -1, 0, 1]

# Find the starting point
targets = []
start_row, start_col = None, None
for row in range(len(map_data)):
    for col in range(len(map_data[row])):
        if map_data[row][col] == 'T':
            targets.append((row, col))
        elif map_data[row][col] == 'S':
            start_row, start_col = row, col


# Define a helper function to check if a cell is within bounds and not an obstacle


def is_valid_cell(row, col):
    return 0 <= row < len(map_data) and 0 <= col < len(map_data[row]) and map_data[row][col] != 'W'

# Define a helper function to check if a cell is passable considering obstacles
# Define a helper function to check if a cell is a target


def is_target_cell(row, col):
    return (row, col) in targets


def is_passable_cell(row, col, visibility):
    if map_data[row][col] == 'W':
        return False
    if visibility == 1:
        return True
    for i in range(8):
        for j in range(1, visibility):
            new_row = row + dx[i] * j
            new_col = col + dy[i] * j
            if not is_valid_cell(new_row, new_col):
                return False
            if map_data[new_row][new_col] == 'W':
                return False
            new_row += dx[i]
            new_col += dy[i]
    return True


# Perform Lee Algorithm with obstacle handling
def perform_lee_algorithm(start_row, start_col):
    queue = deque([(start_row, start_col)])
    visited = set([(start_row, start_col)])
    distances = [[float('inf')] * len(map_data[row])
                 for row in range(len(map_data))]
    parent = {}

    distances[start_row][start_col] = 0

    while queue:
        current_row, current_col = queue.popleft()

        # Explore the neighboring cells
        for i in range(8):
            for j in range(1, visibility_range + 1):
                new_row = current_row + dx[i] * j
                new_col = current_col + dy[i] * j

                if is_valid_cell(new_row, new_col) and (new_row, new_col) not in visited:
                    if is_passable_cell(new_row, new_col, j):
                        queue.append((new_row, new_col))
                        visited.add((new_row, new_col))
                        distances[new_row][new_col] = distances[current_row][current_col] + 1
                        parent[(new_row, new_col)] = (current_row, current_col)

                        if is_target_cell(new_row, new_col):
                            return new_row, new_col, distances, parent


# Trace back the optimal path from the start to the target
def trace_path(start_row, start_col, target_row, target_col, parent):
    path = []
    current_row, current_col = target_row, target_col

    while (current_row, current_col) != (start_row, start_col):
        path.append((current_row, current_col))
        current_row, current_col = parent[(current_row, current_col)]

    path.append((start_row, start_col))
    path.reverse()
    return path


# Perform the algorithm to find and trace paths to all targets
# Perform the algorithm to find and trace paths to all targets
while targets:
    target_row, target_col, distances, parent = perform_lee_algorithm(
        start_row, start_col)
    if target_row is None or target_col is None:
        break

    path = trace_path(start_row, start_col, target_row, target_col, parent)

    # Trace back the optimal path and mark it as 'P'
    current_row, current_col = target_row, target_col
    while (current_row, current_col) != (start_row, start_col):
        if map_data[current_row][current_col] == 'T':
            map_data[current_row][current_col] = 'X'
        else:
            map_data[current_row][current_col] = 'P'
        current_row, current_col = parent[(current_row, current_col)]
    map_data[start_row][start_col] = 'S'

    # Update the starting point and remove the reached target from the list
    start_row, start_col = target_row, target_col
    targets.remove((target_row, target_col))

# Save the final map with the optimal paths to a text file
with open('Lee Algorithm Model/result_Round3.txt', 'w') as file:
    for row in map_data:
        file.write(' '.join(row) + '\n')
