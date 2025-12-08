# def endRotation(graph, n):
#     # n is an endpoint: degree = 1
#     g = copy.deepcopy(graph)
#     bead = g[n]
#     node_pos = {b.position for b in g}

#     # get the only neighbor
#     nbr = next(iter(bead.neighbors))
#     nx, ny = nbr.position

#     # potential new positions: all 4 directions around the neighbor
#     candidates = [(nx+dx, ny+dy) for dx,dy in DIRECTIONS]

#     # cannot stay on top of neighbor or collide with any bead
#     valid = [p for p in candidates if p != bead.position and p not in node_pos]

#     # If no valid moves, return unchanged
#     if not valid:
#         return g

#     bead.position = random.choice(valid)
#     return g

# def cornerFlip(graph, n):
#     g = copy.deepcopy(graph)
#     bead = g[n]
#     node_pos = {b.position for b in g}

#     # must have 2 neighbors
#     if len(bead.neighbors) != 2:
#         return g

#     a, b = list(bead.neighbors)

#     ax, ay = a.position
#     bx, by = b.position
#     nx, ny = bead.position

#     # must be orthogonal: (a-n) and (b-n) must not be colinear
#     if (ax == nx and bx == nx) or (ay == ny and by == ny):
#         # neighbors are colinear → no corner → no flip
#         return g

#     # geometry of corner flip:
#     new_pos = (ax + bx - nx, ay + by - ny)

#     # new position must be empty
#     if new_pos in node_pos:
#         return g

#     bead.position = new_pos
#     return g
