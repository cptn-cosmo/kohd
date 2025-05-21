# kohd_glyphs.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Mapping of letters to their positions (node index and letter index within node)
LETTER_NODES = {
    'A': (0, 0), 'B': (0, 1), 'C': (0, 2),
    'D': (1, 0), 'E': (1, 1), 'F': (1, 2),
    'G': (2, 0), 'H': (2, 1), 'I': (2, 2),
    'J': (3, 0), 'K': (3, 1), 'L': (3, 2),
    'M': (4, 0), 'N': (4, 1), 'O': (4, 2),
    'P': (5, 0), 'Q': (5, 1), 'R': (5, 2),
    'S': (6, 0), 'T': (6, 1), 'U': (6, 2),
    'V': (7, 0), 'W': (7, 1), 'X': (7, 2),
    'Y': (8, 0), 'Z': (8, 1),
}

# Node coordinates in 3x3 grid (row, col)
NODE_COORDS = [
    (0, 0), (0, 1), (0, 2),
    (1, 0), (1, 1), (1, 2),
    (2, 0), (2, 1), (2, 2)
]

def get_node_pos(index):
    row, col = NODE_COORDS[index]
    return col * 3, -row * 3

def draw_node(ax, index, charge=False, ground=False, ring=False):
    x, y = get_node_pos(index)
    radius = 0.8 if not ring else 1.0
    ax.add_patch(patches.Circle((x, y), radius, edgecolor='white', facecolor='none', linewidth=2))

    if charge:
        ax.plot([x - 1.2, x - 0.6], [y, y], color='cyan', lw=2)  # charge line
    if ground:
        ax.plot([x + 0.6, x + 1.2], [y, y], color='yellow', lw=2)  # ground line

def draw_trace(ax, src_idx, dst_idx, dots):
    x1, y1 = get_node_pos(src_idx)
    x2, y2 = get_node_pos(dst_idx)
    ax.plot([x1, x2], [y1, y2], color='white', lw=1)

    # Draw subnodes (dots) along line
    for i, dot in enumerate(dots):
        dx = x1 + (x2 - x1) * (i + 1) / (len(dots) + 1)
        dy = y1 + (y2 - y1) * (i + 1) / (len(dots) + 1)
        ax.add_patch(patches.Circle((dx, dy), 0.15, facecolor='white'))

def generate_kohd_word(word, save_path):
    word = ''.join(filter(str.isalpha, word.upper()))
    if len(word) < 1:
        return

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-3, 9)
    ax.set_ylim(-9, 3)

    used_nodes = []
    path_nodes = []
    subnodes = []

    # Build node path and subnode dot count
    for i, letter in enumerate(word):
        if letter not in LETTER_NODES:
            continue
        node_idx, letter_idx = LETTER_NODES[letter]

        if i == 0:
            path_nodes.append(node_idx)
            subnodes.append([])
        else:
            if node_idx != path_nodes[-1]:
                path_nodes.append(node_idx)
                subnodes.append([letter_idx + 1])  # 0-based index => dot count
            else:
                # If on same node, add dot on previous trace
                subnodes[-1].append(letter_idx + 1)

    # Draw nodes
    for i, node_idx in enumerate(path_nodes):
        ring = path_nodes.count(node_idx) > 1 and path_nodes.index(node_idx) != i
        draw_node(ax, node_idx,
                  charge=(i == 0),
                  ground=(i == len(path_nodes) - 1),
                  ring=ring)
        used_nodes.append(node_idx)

    # Draw traces
    for i in range(len(path_nodes) - 1):
        draw_trace(ax, path_nodes[i], path_nodes[i + 1], subnodes[i + 1])

    fig.patch.set_facecolor('black')
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.2, dpi=300)
    plt.close()
