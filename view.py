import pickle
from Tkinter import Tk, Frame, BOTH, Scrollbar
import ttk


def get_roots(g):
    roots = []
    for vertex in g.vertices():
        if get_parent_count(g, vertex) == 0:
            roots.append(vertex)
    return sorted(roots, key=lambda x: g.vp.title[x], reverse=True)


def get_parent_count(g, vertex):
    return [g.vertex(x.source()) for x in filter(lambda y: y.target() == vertex, list(vertex.all_edges()))].__len__()


def get_children(g, vertex):
    return sorted([g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, list(vertex.all_edges()))],
                  key=lambda z: g.vp.title[z], reverse=True)


def load_graph():
    with open('graph_final.pickle', 'rb') as handle:
        return pickle.load(handle)


class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, padx=5, pady=5)
        self.parent = parent
        self.tree = ttk.Treeview(self)
        self.scrollbar = Scrollbar(self)
        self.initUI()
        self.g = load_graph()
        self.create_tree()

    def initUI(self):
        self.parent.title("Wikipedia Category Tree")
        self.center_window()
        self.pack(fill=BOTH, expand=1)
        self.tree.grid(row=0, column=0, sticky="nesw")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.scrollbar.config(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

    def center_window(self):
        w = 800
        h = 600
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def create_tree(self):
        self.tree.heading("#0", text="Category")
        roots = get_roots(self.g)
        [self.add_children(root, "") for root in roots]

    def add_children(self, parent, parent_id):
        id = self.tree.insert(parent_id, 0, text=str(self.g.vp.title[parent]))
        self.tree.item(id, open=True)
        children = get_children(self.g, parent)
        for child in children:
            self.add_children(child, id)


def main():
    root = Tk()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
