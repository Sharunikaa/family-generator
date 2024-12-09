import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt

class FamilyTreeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Family Tree Generator")
        self.root.geometry("800x600")

        self.family_tree = nx.DiGraph()  # Using DiGraph to specify direction
        self.persons = {}  # Dictionary to store person data: name, age, relationship
        self.user_name = tk.StringVar()
        self.user_age = tk.StringVar()
        self.grandparent_side = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Create a style for consistent UI
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")  # Frame background color
        self.style.configure("TLabel", background="#f0f0f0")  # Label background color
        self.style.configure("TButton", background="#4CAF50", foreground="black")  # Button colors

        # Page 1
        self.page1 = ttk.Frame(self.root, style="TFrame")
        ttk.Label(self.page1, text="Your Information", font=("Helvetica", 16, "bold"), style="TLabel").pack(pady=10)
        ttk.Label(self.page1, text="Name:", font=("Helvetica", 12), style="TLabel").pack()
        ttk.Entry(self.page1, textvariable=self.user_name, font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(self.page1, text="Age:", font=("Helvetica", 12), style="TLabel").pack()
        ttk.Entry(self.page1, textvariable=self.user_age, font=("Helvetica", 12)).pack(pady=5)
        ttk.Button(self.page1, text="Next", command=self.show_page2, style="TButton").pack(pady=10)

        # Page 2
        self.page2 = ttk.Frame(self.root, style="TFrame")
        ttk.Label(self.page2, text="Relative's Information", font=("Helvetica", 16, "bold"), style="TLabel").pack(pady=10)

        self.relative_type = tk.StringVar()
        relative_types = ["Father", "Mother", "Sibling", "Grandfather", "Grandmother", "Uncle", "Aunt", "Daughter", "Son"]
        for r_type in relative_types:
            if r_type in ["Grandfather", "Grandmother"]:
                ttk.Label(self.page2, text=f"Select {r_type}'s Side:", font=("Helvetica", 12), style="TLabel").pack()
                ttk.Radiobutton(self.page2, text="Mother's Side", variable=self.grandparent_side, value="Mother", style="TButton").pack(pady=5)
                ttk.Radiobutton(self.page2, text="Father's Side", variable=self.grandparent_side, value="Father", style="TButton").pack(pady=5)
            else:
                ttk.Radiobutton(self.page2, text=r_type, variable=self.relative_type, value=r_type, style="TButton").pack(pady=5)

        ttk.Button(self.page2, text="Next", command=self.show_page3, style="TButton").pack(pady=10)
        ttk.Button(self.page2, text="Back", command=self.show_page1, style="TButton").pack(pady=10)

        # Page 3
        self.page3 = ttk.Frame(self.root, style="TFrame")
        ttk.Label(self.page3, text="Enter Relative's Information", font=("Helvetica", 16, "bold"), style="TLabel").pack(pady=10)

        self.relative_name_var = tk.StringVar()
        ttk.Label(self.page3, text="Name:", font=("Helvetica", 12), style="TLabel").pack()
        ttk.Entry(self.page3, textvariable=self.relative_name_var, font=("Helvetica", 12)).pack(pady=5)

        self.relative_age_var = tk.StringVar()
        ttk.Label(self.page3, text="Age:", font=("Helvetica", 12), style="TLabel").pack()
        ttk.Entry(self.page3, textvariable=self.relative_age_var, font=("Helvetica", 12)).pack(pady=5)

        ttk.Button(self.page3, text="Add Relative", command=self.add_relative, style="TButton").pack(pady=10)
        ttk.Button(self.page3, text="Finish", command=self.generate_tree, style="TButton").pack(pady=10)
        ttk.Button(self.page3, text="Back", command=self.show_page2, style="TButton").pack(pady=10)

        self.show_page1()

        # Center the window on the screen
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_coordinate = (screen_width - width) // 2
        y_coordinate = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    def show_page1(self):
        self.page2.grid_forget()
        self.page3.grid_forget()
        self.page1.grid(row=0, column=0, sticky="nsew")

    def show_page2(self):
        self.page1.grid_forget()
        self.page3.grid_forget()
        self.page2.grid(row=0, column=0, sticky="nsew")

    def show_page3(self):
        self.page1.grid_forget()
        self.page2.grid_forget()
        self.page3.grid(row=0, column=0, sticky="nsew")

    def add_relative(self):
        user_name = self.user_name.get()
        user_age = int(self.user_age.get())

        relative_name = self.relative_name_var.get()
        relative_age = int(self.relative_age_var.get())

        if not self.family_tree:  # If family_tree is empty, user is considered as the root node
            self.family_tree.add_node(user_name)
            self.persons[user_name] = {"age": user_age, "relationship": "Self"}
        else:
            relationship = self.relative_type.get()
            if relationship in ["Grandfather", "Grandmother"]:
                grandparent_side = self.grandparent_side.get()
                if grandparent_side == "Mother":
                    parent = [p for p, d in self.persons.items() if d["relationship"] == "Mother"]
                else:
                    parent = [p for p, d in self.persons.items() if d["relationship"] == "Father"]
                if parent:
                    self.family_tree.add_edge(parent[0], relative_name)
            else:
                self.persons[relative_name] = {"age": relative_age, "relationship": relationship}
                parents = [p for p, d in self.persons.items() if d["relationship"] in ["Mother", "Father"]]
                if parents:
                    for parent in parents:
                        self.family_tree.add_edge(parent, relative_name)

        print(f"Added {relative_name}, Age: {relative_age}")

    def generate_tree(self):
        pos = self.custom_layout()  # Calculate custom layout
        nx.draw(self.family_tree, pos, with_labels=True, node_size=700, font_size=8, font_color='black', arrows=True)
        plt.title("Family Tree")
        plt.show()

    def custom_layout(self):
        pos = {}

        root = [n for n, d in self.family_tree.nodes(data=True) if d.get("relationship") == "Self"]
        siblings = [n for n, d in self.family_tree.nodes(data=True) if d.get("relationship") == "Sibling"]
        parents = [n for n, d in self.family_tree.nodes(data=True) if d.get("relationship") in ["Mother", "Father"]]
        grandparents = [n for n, d in self.family_tree.nodes(data=True) if d.get("relationship") in ["Grandfather", "Grandmother"]]

        levels = {0: root, 1: siblings + parents, 2: grandparents}

        if root:  # Check if root list is not empty
            root_pos = {root[0]: (0, 0)}
            pos.update(root_pos)

        for level, nodes in levels.items():
            if nodes:  # Ensure nodes list has a non-zero length
                if level == 0 and 'me' in nodes:  # Ensuring 'me' node is included in position dictionary
                    pos['me'] = (0, 0)
                elif level == 1:
                    angle = 360 / len(nodes)
                    for i, node in enumerate(nodes):
                        x = 2 * (level) * (len(nodes) // 2) * (0.7 if level == 2 else 1) * (1 if i % 2 == 0 else -1)
                        y = 2 * (level) * (len(nodes) // 2) * (0.7 if level == 2 else 1) * (1 if i % 2 == 0 else -1)
                        pos[node] = (x, y)
                elif level == 2:
                    angle = 360 / len(nodes)
                    for i, node in enumerate(nodes):
                        x = 4 * (level) * (len(nodes) // 2) * (0.7 if level == 2 else 1) * (1 if i % 2 == 0 else -1)
                        y = 4 * (level) * (len(nodes) // 2) * (0.7 if level == 2 else 1) * (1 if i % 2 == 0 else -1)
                        pos[node] = (x, y)

        return pos




if __name__ == "__main__":
    root = tk.Tk()
    app = FamilyTreeGenerator(root)
    root.mainloop()
