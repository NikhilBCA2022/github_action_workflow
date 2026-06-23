# ============================================================
#   Campus Navigation System
#   DSA Mini Project — BCA, CSE1022
#
#   DSA Topics Used:
#   1. ARRAY       — store all campus locations
#   2. STACK       — navigation history (go back)
#   3. QUEUE       — visit wishlist (planned stops)
#   4. TREE        — campus map hierarchy (Zone → Building → Room)
# ============================================================

# ── COLOUR HELPERS ──────────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def banner(text): print(f"\n{BOLD}{CYAN}{'═'*55}{RESET}\n{BOLD}{CYAN}  {text}{RESET}\n{CYAN}{'═'*55}{RESET}")
def ok(text):     print(f"  {GREEN}✔  {text}{RESET}")
def info(text):   print(f"  {YELLOW}➜  {text}{RESET}")
def err(text):    print(f"  {RED}✘  {text}{RESET}")
def head(text):   print(f"\n{BOLD}{YELLOW}  ── {text} ──{RESET}")


# ════════════════════════════════════════════════════════════
#  DSA 1 — ARRAY
#  What  : A fixed list of all campus locations.
#  Why   : Arrays give us fast O(1) access by index number.
#          Useful to list all places and pick one by number.
# ════════════════════════════════════════════════════════════
CAMPUS_LOCATIONS = [
    # index : (name,               zone,          type)
    (0,  "Main Gate",           "Entrance",    "Gate"),
    (1,  "Admin Block",         "Admin Zone",  "Office"),
    (2,  "Library",             "Academic",    "Library"),
    (3,  "Computer Lab",        "Academic",    "Lab"),
    (4,  "Physics Lab",         "Academic",    "Lab"),
    (5,  "Canteen",             "Facilities",  "Food"),
    (6,  "Auditorium",          "Events",      "Hall"),
    (7,  "Sports Ground",       "Sports",      "Ground"),
    (8,  "Boys Hostel",         "Residential", "Hostel"),
    (9,  "Girls Hostel",        "Residential", "Hostel"),
    (10, "Medical Centre",      "Facilities",  "Medical"),
    (11, "Parking Area",        "Entrance",    "Parking"),
]

def show_all_locations():
    head("ALL CAMPUS LOCATIONS  (Array — index access)")
    print(f"  {'#':<5} {'Location':<22} {'Zone':<16} {'Type'}")
    print("  " + "─" * 56)
    for idx, name, zone, ltype in CAMPUS_LOCATIONS:
        print(f"  {idx:<5} {name:<22} {zone:<16} {ltype}")

def get_location(idx):
    """Array access — O(1), direct index lookup."""
    if 0 <= idx < len(CAMPUS_LOCATIONS):
        return CAMPUS_LOCATIONS[idx]
    return None


# ════════════════════════════════════════════════════════════
#  DSA 2 — STACK
#  What  : Remembers where you HAVE BEEN (history).
#  Why   : Stack = LIFO (Last In, First Out).
#          Like the Back button — most recent visit pops first.
#  Real analogy: Browser history, Ctrl+Z undo.
# ════════════════════════════════════════════════════════════
class NavigationHistory:

    def __init__(self):
        self._stack = []          # Python list used as a stack

    def visit(self, location):
        """PUSH — add location to top of stack."""
        self._stack.append(location)
        ok(f"Visited  →  {location[1]}  (pushed to history stack)")

    def go_back(self):
        """POP — remove & return the last visited location."""
        if self._stack:
            place = self._stack.pop()
            info(f"Going back from  →  {place[1]}")
            return place
        err("No history to go back to!")
        return None

    def current(self):
        """PEEK — look at top without removing."""
        if self._stack:
            return self._stack[-1]
        return None

    def show(self):
        head("NAVIGATION HISTORY  (Stack — newest first)")
        if not self._stack:
            info("You haven't visited anywhere yet.")
            return
        for place in reversed(self._stack):     # newest first
            print(f"  📍  {place[1]}  ({place[2]})")

    def size(self):
        return len(self._stack)


# ════════════════════════════════════════════════════════════
#  DSA 3 — QUEUE
#  What  : A wishlist of places you PLAN TO VISIT next.
#  Why   : Queue = FIFO (First In, First Out).
#          The first place you add is the first you visit.
#  Real analogy: A to-do list, ticket counter line.
# ════════════════════════════════════════════════════════════
class VisitWishlist:

    def __init__(self):
        self._queue = []          # Python list used as a queue

    def add(self, location):
        """ENQUEUE — add to the back of the queue."""
        self._queue.append(location)
        ok(f"Added to wishlist  →  {location[1]}  (enqueued)")

    def next_stop(self):
        """DEQUEUE — remove & return from the front."""
        if self._queue:
            place = self._queue.pop(0)
            info(f"Next planned stop  →  {place[1]}")
            return place
        err("Wishlist is empty!")
        return None

    def show(self):
        head("VISIT WISHLIST  (Queue — will visit in this order)")
        if not self._queue:
            info("Your wishlist is empty. Add places to plan your route!")
            return
        for i, place in enumerate(self._queue, 1):
            arrow = "→ next!" if i == 1 else ""
            print(f"  {i}.  🎯  {place[1]}  ({place[2]})  {CYAN}{arrow}{RESET}")


# ════════════════════════════════════════════════════════════
#  DSA 4 — TREE
#  What  : Campus map organised as a hierarchy.
#  Why   : Tree = parent → children relationships.
#          Campus → Zones → Buildings → Rooms.
#  Real analogy: A folder structure on your computer.
# ════════════════════════════════════════════════════════════
class TreeNode:
    """One node in the campus tree."""
    def __init__(self, name, node_type=""):
        self.name      = name
        self.node_type = node_type   # Zone / Building / Room
        self.children  = []          # list of child TreeNodes

    def add_child(self, child_node):
        self.children.append(child_node)
        return child_node            # return so we can chain


def build_campus_tree():
    """
    Build the campus tree manually.
    Structure:
      Campus
      ├── Entrance Zone
      │   ├── Main Gate
      │   └── Parking Area
      ├── Admin Zone
      │   └── Admin Block
      │       ├── Principal Office
      │       ├── Exam Cell
      │       └── Accounts Dept
      ├── Academic Zone
      │   ├── Library
      │   │   ├── Reference Section
      │   │   └── Reading Hall
      │   ├── Computer Lab
      │   │   ├── Lab 1 (Python)
      │   │   └── Lab 2 (Networks)
      │   └── Physics Lab
      ├── Facilities Zone
      │   ├── Canteen
      │   │   ├── Veg Counter
      │   │   └── Snacks Corner
      │   └── Medical Centre
      ├── Events Zone
      │   └── Auditorium
      │       ├── Main Stage
      │       └── Green Room
      ├── Sports Zone
      │   └── Sports Ground
      │       ├── Cricket Field
      │       └── Basketball Court
      └── Residential Zone
          ├── Boys Hostel
          │   ├── Block A
          │   └── Block B
          └── Girls Hostel
              ├── Block C
              └── Block D
    """
    root = TreeNode("🏫 Campus", "Root")

    # ── Entrance ─────────────────────────────────────────
    entrance = root.add_child(TreeNode("🚪 Entrance Zone", "Zone"))
    entrance.add_child(TreeNode("Main Gate", "Gate"))
    entrance.add_child(TreeNode("Parking Area", "Parking"))

    # ── Admin ─────────────────────────────────────────────
    admin = root.add_child(TreeNode("🏢 Admin Zone", "Zone"))
    admin_blk = admin.add_child(TreeNode("Admin Block", "Building"))
    admin_blk.add_child(TreeNode("Principal Office", "Room"))
    admin_blk.add_child(TreeNode("Exam Cell", "Room"))
    admin_blk.add_child(TreeNode("Accounts Dept", "Room"))

    # ── Academic ──────────────────────────────────────────
    academic = root.add_child(TreeNode("📚 Academic Zone", "Zone"))
    library = academic.add_child(TreeNode("Library", "Building"))
    library.add_child(TreeNode("Reference Section", "Room"))
    library.add_child(TreeNode("Reading Hall", "Room"))
    comp_lab = academic.add_child(TreeNode("Computer Lab", "Building"))
    comp_lab.add_child(TreeNode("Lab 1 — Python", "Room"))
    comp_lab.add_child(TreeNode("Lab 2 — Networks", "Room"))
    academic.add_child(TreeNode("Physics Lab", "Building"))

    # ── Facilities ────────────────────────────────────────
    facilities = root.add_child(TreeNode("🍽 Facilities Zone", "Zone"))
    canteen = facilities.add_child(TreeNode("Canteen", "Building"))
    canteen.add_child(TreeNode("Veg Counter", "Room"))
    canteen.add_child(TreeNode("Snacks Corner", "Room"))
    facilities.add_child(TreeNode("Medical Centre", "Building"))

    # ── Events ────────────────────────────────────────────
    events = root.add_child(TreeNode("🎭 Events Zone", "Zone"))
    audi = events.add_child(TreeNode("Auditorium", "Building"))
    audi.add_child(TreeNode("Main Stage", "Room"))
    audi.add_child(TreeNode("Green Room", "Room"))

    # ── Sports ────────────────────────────────────────────
    sports = root.add_child(TreeNode("⚽ Sports Zone", "Zone"))
    ground = sports.add_child(TreeNode("Sports Ground", "Building"))
    ground.add_child(TreeNode("Cricket Field", "Room"))
    ground.add_child(TreeNode("Basketball Court", "Room"))

    # ── Residential ───────────────────────────────────────
    residential = root.add_child(TreeNode("🏠 Residential Zone", "Zone"))
    boys = residential.add_child(TreeNode("Boys Hostel", "Building"))
    boys.add_child(TreeNode("Block A", "Room"))
    boys.add_child(TreeNode("Block B", "Room"))
    girls = residential.add_child(TreeNode("Girls Hostel", "Building"))
    girls.add_child(TreeNode("Block C", "Room"))
    girls.add_child(TreeNode("Block D", "Room"))

    return root


def print_tree(node, prefix="", is_last=True):
    """
    Recursively print the tree with neat connectors.
    This is a DFS (Depth-First Search) traversal.
    """
    connector = "└── " if is_last else "├── "
    # colour by level
    if node.node_type == "Root":
        label = f"{BOLD}{CYAN}{node.name}{RESET}"
    elif node.node_type == "Zone":
        label = f"{BOLD}{YELLOW}{node.name}{RESET}"
    elif node.node_type == "Building":
        label = f"{GREEN}{node.name}{RESET}"
    else:
        label = f"  {node.name}"

    print(f"  {prefix}{connector}{label}")

    child_prefix = prefix + ("    " if is_last else "│   ")
    for i, child in enumerate(node.children):
        print_tree(child, child_prefix, i == len(node.children) - 1)


def search_tree(node, query, results=None):
    """Search tree nodes whose name contains the query string."""
    if results is None:
        results = []
    if query.lower() in node.name.lower():
        results.append(node)
    for child in node.children:
        search_tree(child, query, results)
    return results


# ════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ════════════════════════════════════════════════════════════
def run():
    history  = NavigationHistory()
    wishlist = VisitWishlist()
    tree     = build_campus_tree()

    banner("Campus Navigation System")
    print(f"  {BOLD}DSA Mini Project  —  BCA CSE1022{RESET}")
    print(f"  Topics: Array  ·  Stack  ·  Queue  ·  Tree\n")

    while True:
        print(f"\n{BOLD}  ╔══════════════════════════════════╗{RESET}")
        print(f"{BOLD}  ║          MAIN MENU               ║{RESET}")
        print(f"{BOLD}  ╠══════════════════════════════════╣{RESET}")
        print(f"{BOLD}  ║{RESET}  1.  View All Locations  {CYAN}(Array){RESET}  {BOLD}║{RESET}")
        print(f"{BOLD}  ║{RESET}  2.  Visit a Location    {CYAN}(Stack){RESET}  {BOLD}║{RESET}")
        print(f"{BOLD}  ║{RESET}  3.  Go Back             {CYAN}(Stack){RESET}  {BOLD}║{RESET}")
        print(f"{BOLD}  ║{RESET}  4.  View History        {CYAN}(Stack){RESET}  {BOLD}║{RESET}")
        print(f"{BOLD}  ║{RESET}  5.  Add to Wishlist     {CYAN}(Queue){RESET}  {BOLD}║{RESET}")
        print(f"{BOLD}  ║{RESET}  6.  Visit Next in List  {CYAN}(Queue){RESET}  {BOLD}║{RESET}")
        print(f"{BOLD}  ║{RESET}  7.  View Wishlist       {CYAN}(Queue){RESET}  {BOLD}║{RESET}")
        print(f"{BOLD}  ║{RESET}  8.  Browse Campus Map   {CYAN}(Tree) {RESET}  {BOLD}║{RESET}")
        print(f"{BOLD}  ║{RESET}  9.  Search Campus Map   {CYAN}(Tree) {RESET}  {BOLD}║{RESET}")
        print(f"{BOLD}  ║{RESET}  10. Where am I now?              {BOLD}║{RESET}")
        print(f"{BOLD}  ║{RESET}  0.  Exit                         {BOLD}║{RESET}")
        print(f"{BOLD}  ╚══════════════════════════════════╝{RESET}")

        choice = input(f"\n  {CYAN}Enter choice: {RESET}").strip()

        # ── 1: VIEW ALL LOCATIONS (Array) ───────────────────
        if choice == "1":
            show_all_locations()

        # ── 2: VISIT A LOCATION (Stack push) ────────────────
        elif choice == "2":
            show_all_locations()
            try:
                num = int(input(f"\n  {CYAN}Enter location number to visit: {RESET}"))
                place = get_location(num)
                if place:
                    history.visit(place)
                else:
                    err("Invalid number. Try again.")
            except ValueError:
                err("Please enter a valid number.")

        # ── 3: GO BACK (Stack pop) ───────────────────────────
        elif choice == "3":
            head("GO BACK  (Stack — pop last location)")
            prev = history.go_back()
            if prev:
                current = history.current()
                if current:
                    ok(f"Now at  →  {current[1]}")
                else:
                    info("You are back at the starting point.")

        # ── 4: VIEW HISTORY (Stack display) ─────────────────
        elif choice == "4":
            history.show()
            info(f"Total places visited: {history.size()}")

        # ── 5: ADD TO WISHLIST (Queue enqueue) ───────────────
        elif choice == "5":
            show_all_locations()
            try:
                num = int(input(f"\n  {CYAN}Enter location number to add to wishlist: {RESET}"))
                place = get_location(num)
                if place:
                    wishlist.add(place)
                else:
                    err("Invalid number. Try again.")
            except ValueError:
                err("Please enter a valid number.")

        # ── 6: VISIT NEXT IN WISHLIST (Queue dequeue) ────────
        elif choice == "6":
            head("VISIT NEXT PLANNED STOP  (Queue — dequeue)")
            place = wishlist.next_stop()
            if place:
                history.visit(place)   # also pushes to history stack

        # ── 7: VIEW WISHLIST (Queue display) ─────────────────
        elif choice == "7":
            wishlist.show()

        # ── 8: BROWSE CAMPUS MAP (Tree) ──────────────────────
        elif choice == "8":
            head("CAMPUS MAP  (Tree — DFS traversal)")
            print()
            print_tree(tree)
            print()
            info("Tree shows:  Campus → Zone → Building → Room")

        # ── 9: SEARCH CAMPUS MAP (Tree search) ───────────────
        elif choice == "9":
            head("SEARCH CAMPUS MAP  (Tree — node search)")
            query = input(f"  {CYAN}Enter place name to search: {RESET}").strip()
            if query:
                results = search_tree(tree, query)
                if results:
                    ok(f"Found {len(results)} result(s) for '{query}':")
                    for r in results:
                        print(f"    🔍  {r.name}  [{r.node_type}]")
                else:
                    err(f"No location found matching '{query}'")
            else:
                err("Please type something to search.")

        # ── 10: WHERE AM I ───────────────────────────────────
        elif choice == "10":
            head("WHERE AM I NOW?")
            current = history.current()
            if current:
                ok(f"You are currently at  →  {current[1]}")
                info(f"Zone: {current[2]}  |  Type: {current[3]}")
            else:
                info("You are at the starting point (not visited anywhere yet).")

        # ── 0: EXIT ──────────────────────────────────────────
        elif choice == "0":
            banner("Thank You!")
            print(f"  {BOLD}Campus Navigation System — BCA CSE1022{RESET}")
            print(f"  DSA Topics Used: Array · Stack · Queue · Tree\n")
            break

        else:
            err("Please enter a number between 0 and 10.")


if __name__ == "__main__":
    run()