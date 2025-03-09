from collections import deque

def waterJugProblem(capacity1, capacity2, goal):
    queue = deque()
    visited = set()

    queue.append((0, 0))
    visited.add((0, 0))

    actions = []

    while queue:
        jug1, jug2 = queue.popleft()
        actions.append((jug1, jug2))
        if jug1 == goal or jug2 == goal:
            print("Solution Found Successfully!")
            for action in actions:
                print(action)
            return True

        rules = [
           (capacity1, jug2), 
           (jug1, capacity2), 
           (0, jug2), 
           (jug1, 0), 
           (capacity1, abs(jug2-(capacity1-jug1))),
           (abs(jug1-(capacity2-jug2)), capacity2),
           (jug1+jug2, 0),
           (0, jug1+jug2),
        ] 

        for state in rules:
            if state not in visited:
                visited.add(state)
                queue.append(state)

    print("No Solution found")
    return False

jug1Capacity = 4
jug2Capacity = 3
target = 2          

waterJugProblem(jug1Capacity, jug2Capacity, target)