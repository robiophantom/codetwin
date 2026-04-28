from codetwin.AST import AST


class FlattenedTree:
    def __init__(self, ast):
        self.flattened = ast.preorder()
        self.flattened.sort(key=lambda node: node.weight, reverse=True)
        self.removed = set()

    def nodes(self):
        self.removed = set()

        for node in self.flattened:
            if node in self.removed:
                continue
            yield node

    def remove(self, node):
        self.removed.update(node.preorder())

    def __len__(self):
        return len(self.flattened)


class Checker:
    def __init__(self, path1, path2, ast1, ast2, threshold=5):
        self.path1 = path1
        self.path2 = path2
        self.flattened1 = FlattenedTree(ast1)
        self.flattened2 = FlattenedTree(ast2)

        self.threshold = threshold
        self.similarity = 0
        self.overlapping_ranges = []

    def check(self):
        """
        Check the similarities of two ASTs.

        Iterates flattened1 nodes from largest to smallest subtree.  When a
        matching subtree is found in flattened2, the node (and all its
        descendants) is counted once.  Child nodes whose parent was already
        matched are skipped to avoid double-counting.
        """
        # Build a lookup of flattened2 nodes grouped by (weight, fingerprint)
        flattened2_dict = {}
        for node in self.flattened2.nodes():
            key = (node.weight, node.fingerprint)
            flattened2_dict.setdefault(key, []).append(node)
        for key in flattened2_dict:
            flattened2_dict[key] = iter(flattened2_dict[key])

        # Track IDs of matched flattened1 nodes so descendants are skipped
        matched = set()
        num_of_same_nodes = 0

        for node in self.flattened1.nodes():
            # Nodes are sorted by weight descending; stop once below threshold
            if node.weight < self.threshold:
                break

            # If a parent was already matched, propagate and skip this child
            if id(node.parent) in matched:
                matched.add(id(node))
                continue

            key = (node.weight, node.fingerprint)
            if key in flattened2_dict:
                match = next(flattened2_dict[key], None)
                if match is not None:
                    num_of_same_nodes += node.weight
                    matched.add(id(node))
                    self.overlapping_ranges.append({
                        "A_start_pos": node.start_pos,
                        "A_end_pos": node.end_pos,
                        "B_start_pos": match.start_pos,
                        "B_end_pos": match.end_pos,
                    })

        self.similarity = num_of_same_nodes / min(len(self.flattened1), len(self.flattened2))
