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
            print("Solution Found")
            for action in actions:
                print(action)
            return True

        rules = [
            (capacity1, jug2) if jug1 < capacity1 else None,  # Rule 1: Fill the 4-gallon jug
            (jug1, capacity2) if jug2 < capacity2 else None,  # Rule 2: Fill the 3-gallon jug
            (jug1 - min(jug1, capacity2 - jug2), jug2 + min(jug1, capacity2 - jug2)) if jug1 > 0 else None,  # Rule 3: Pour from jug1 to jug2
            (jug1 + min(jug2, capacity1 - jug1), jug2 - min(jug2, capacity1 - jug1)) if jug2 > 0 else None,  # Rule 4: Pour from jug2 to jug1
            (0, jug2) if jug1 > 0 else None,  # Rule 5: Empty 4-gallon jug
            (jug1, 0) if jug2 > 0 else None,  # Rule 6: Empty 3-gallon jug
            (capacity1, jug2 - (capacity1 - jug1)) if jug1 + jug2 >= capacity1 and jug2 > 0 else None,  # Rule 7: Pour into jug1 until full
            (jug1 - (capacity2 - jug2), capacity2) if jug1 + jug2 >= capacity2 and jug1 > 0 else None,  # Rule 8: Pour into jug2 until full
            (jug1 + jug2, 0) if jug1 + jug2 <= capacity1 else None,  # Rule 9: Pour all from jug2 into jug1
            (0, jug1 + jug2) if jug1 + jug2 <= capacity2 else None  # Rule 10: Pour all from jug1 into jug2
        ]

        for state in rules:
            if state and state not in visited:
                visited.add(state)
                queue.append(state)
    
    print("No Solution found")
    return False

jug1Capacity = 4
jug2Capacity = 3
target = 2

waterJugProblem(jug1Capacity, jug2Capacity, target)

