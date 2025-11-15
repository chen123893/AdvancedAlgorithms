from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Set, Iterable, Optional

# Directed, unweighted graph
class DirectedGraph:

    def __init__(self) -> None:
        self._adj: Dict[str, Set[str]] = {}

    def addVertex(self, v: str) -> None:
        if v not in self._adj:
            self._adj[v] = set()

    def addEdge(self, src: str, dst: str) -> None:
        if src not in self._adj:
            self._adj[src] = set()
        if dst not in self._adj:
            self._adj[dst] = set()
        self._adj[src].add(dst)

    def listOutgoingAdjacentVertex(self, v: str) -> Iterable[str]:
        if v not in self._adj:
            return []
        outs = list(self._adj[v])
        try:
            return sorted(outs)
        except:
            return outs

    def vertices(self) -> Iterable[str]:
        try:
            return sorted(self._adj.keys())
        except:
            return list(self._adj.keys())

    def hasVertex(self, v: str) -> bool:
        return v in self._adj

    def removeEdge(self, src: str, dst: str) -> bool:
        if src in self._adj and dst in self._adj[src]:
            self._adj[src].remove(dst)
            return True
        return False

    def followersOf(self, target: str) -> Iterable[str]:
        result = [v for v, outs in self._adj.items() if target in outs]
        try:
            return sorted(result)
        except:
            return result


# Person Entity
class Privacy(Enum):
    PUBLIC = auto()
    PRIVATE = auto()


@dataclass
class Person:
    name: str
    gender: str
    biography: str
    privacy: Privacy = Privacy.PUBLIC


# People Directory
class PeopleDirectory:
    def __init__(self) -> None:
        self._by_name: Dict[str, Person] = {}

    def add(self, p: Person) -> None:
        self._by_name[p.name] = p

    def get(self, name: str) -> Optional[Person]:
        return self._by_name.get(name)

    def all_names(self) -> Iterable[str]:
        return sorted(self._by_name.keys())

    def exists(self, name: str) -> bool:
        return name in self._by_name


# Seed data
def seed_data(dir: PeopleDirectory, g: DirectedGraph) -> None:
    samples = [
        Person("Desmond",  "F", "Coffee, cats, and code.", Privacy.PUBLIC),
        Person("Bryan",  "M", "Trail runs + TypeScript.", Privacy.PRIVATE),
        Person("Carmen",  "F", "Photographer & foodie.", Privacy.PUBLIC),
        Person("John",    "M", "Learning ML every day.", Privacy.PUBLIC),
        Person("Nicole",   "F", "Minimalist design nerd.", Privacy.PRIVATE),
        Person("Ashton", "M", "Gaming + backend APIs.", Privacy.PUBLIC),
    ]

    for p in samples:
        dir.add(p)
        g.addVertex(p.name)

    edges = [
        ("Desmond", "Carmen"),
        ("Desmond", "John"),
        ("Carmen", "Desmond"),
        ("Carmen", "Bryan"),
        ("John",   "Ashton"),
        ("Ashton","Desmond"),
        ("Bryan", "Desmond"),
        ("Bryan", "Nicole"),
        ("Nicole",  "Carmen"),
    ]

    for src, dst in edges:
        g.addEdge(src, dst)


# Validations
def input_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty.")

def choose_name(prompt: str, dir: PeopleDirectory) -> Optional[str]:
    n = input(prompt).strip()
    if not n:
        print("No input provided.")
        return None
    if not dir.exists(n):
        print(f"User '{n}' does not exist.")
        return None
    return n

def print_profile(p: Person, ignore_privacy: bool = True) -> None:
    print(f"\nName     : {p.name}")
    print(f"Gender   : {p.gender}")

    if ignore_privacy or p.privacy == Privacy.PUBLIC:
        print(f"Bio      : {p.biography}")
        print(f"Privacy  : {p.privacy.name}\n")
    else:
        print("Privacy  : PRIVATE")
        print("Details  : (hidden)\n")

def show_following(g: DirectedGraph, who: str) -> None:
    outs = list(g.listOutgoingAdjacentVertex(who))
    print(f"\n{who} follows ({len(outs)}): {', '.join(outs) if outs else '(none)'}\n")

def show_followers(g: DirectedGraph, who: str) -> None:
    ins = list(g.followersOf(who))
    print(f"\nFollowers of {who} ({len(ins)}): {', '.join(ins) if ins else '(none)'}\n")

def add_user_flow(dir: PeopleDirectory, g: DirectedGraph) -> None:
    print("\nAdd new user profile:")
    name = input_nonempty("  Name: ")
    if dir.exists(name):
        print("This name already exists.")
        return

    while True:
        gender = input("  Gender (M/F): ").strip().upper()
        if gender in ("M", "F"):
            break
        print("Invalid gender. Enter M or F only.")

    bio = input("  Bio: ").strip()
    priv_in = input("  Privacy (PUBLIC/PRIVATE): ").strip().upper() or "PUBLIC"
    privacy = Privacy.PUBLIC if priv_in != "PRIVATE" else Privacy.PRIVATE

    p = Person(name, gender, bio, privacy)
    dir.add(p)
    g.addVertex(name)
    print(f"Added {name}.\n")

def follow_flow(dir: PeopleDirectory, g: DirectedGraph) -> None:
    print("\nFollow user")
    x = choose_name("  Follower name: ", dir)
    y = choose_name("  Followed name: ", dir)
    if x and y:
        if x == y:
            print("Cannot follow yourself.\n")
            return
        g.addEdge(x, y)
        print(f"{x} now follows {y}\n")

def unfollow_flow(dir: PeopleDirectory, g: DirectedGraph) -> None:
    print("\nUnfollow user")
    x = choose_name("  Unfollower name: ", dir)
    y = choose_name("  Unfollowed name: ", dir)
    if x and y:
        if g.removeEdge(x, y):
            print(f"{x} unfollowed {y}\n")
        else:
            print("Relationship not found.\n")

def list_all_users(dir: PeopleDirectory) -> None:
    names = sorted(dir.all_names())
    print("\nAll users:")
    print(", ".join(names))
    print()


# Main Menu
def main() -> None:
    directory = PeopleDirectory()
    graph = DirectedGraph()
    seed_data(directory, graph)

    while True:
        print(
            "=== Social Graph Menu ===\n"
            "1) Display all users\n"
            "2) View profile (ignore privacy)\n"
            "3) View following\n"
            "4) View followers\n"
            "5) Add user\n"
            "6) Follow user\n"
            "7) Unfollow user\n"
            "8) View profile (respect privacy)\n"
            "9) Exit\n"
        )
        choice = input("Choose: ").strip()

        if choice == "1":
            list_all_users(directory)

        elif choice == "2":
            n = choose_name("Name: ", directory)
            if n:
                print_profile(directory.get(n), ignore_privacy=True)

        elif choice == "3":
            n = choose_name("Name: ", directory)
            if n:
                show_following(graph, n)

        elif choice == "4":
            n = choose_name("Name: ", directory)
            if n:
                show_followers(graph, n)

        elif choice == "5":
            add_user_flow(directory, graph)

        elif choice == "6":
            follow_flow(directory, graph)

        elif choice == "7":
            unfollow_flow(directory, graph)

        elif choice == "8":
            n = choose_name("Name: ", directory)
            if n:
                print_profile(directory.get(n), ignore_privacy=False)

        elif choice == "9":
            print("Successfully Exit!")
            break

        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()
