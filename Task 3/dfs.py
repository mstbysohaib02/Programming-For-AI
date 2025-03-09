
# Task 03 
def waterJug(cap1, cap2, goal):
    stack = [(0, 0)]
    visited = set([(0, 0)])
    parents = {}
    while stack:
        cur_state = stack.pop()
        jug1, jug2 = cur_state

        if jug1 == goal or jug2 == goal:
            actions = []
            while cur_state != (0, 0):
                actions.append(cur_state)
                cur_state = parents[cur_state]
            actions.append((0, 0))
            actions.reverse()
            return actions

        rules = [
            (cap1, jug2), 
            (jug1, cap2), 
            (0, jug2),  
            (jug1, 0),    
            (min(cap1, jug1 + jug2), max(0, jug1 + jug2 - cap1)),
            (max(0, jug1 + jug2 - cap2), min(cap2, jug1 + jug2)),
            (jug1 - min(jug1, cap2 - jug2), jug2 + min(jug1, cap2 - jug2)),
            (jug1 + min(jug2, cap1 - jug1), jug2 - min(jug2, cap1 - jug1))            
        ]

        for state in rules:
            if state not in visited:
                stack.append(state)
                visited.add(state)
                parents[state] = cur_state
    return None

jug1_cap = 5
jug2_cap = 4
goal_quantity = 3
solution = waterJug(jug1_cap, jug2_cap, goal_quantity)
print("DFS Water Jug Problem:")
if solution:
    for step in solution:
        print(step)
else:
    print("No solution found.")