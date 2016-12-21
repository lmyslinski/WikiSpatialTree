import pickle
from Tkinter import Tk, Frame, BOTH, Scrollbar, StringVar, IntVar
import ttk

from app import TreeReducer
from preprocessing.builder import Dataset


def get_roots(g):
    roots = []
    for vertex in g.vertices():
        # BUG override - the child count is necessary due to graph tool not removing some nodes NO_MATTER_WHAT(WTF?)
        if get_parent_count(g, vertex) == 0:
            roots.append(vertex)
    return sorted(roots, key=lambda x: g.vp.title[x], reverse=True)


def get_parent_count(g, vertex):
    return [g.vertex(x.source()) for x in filter(lambda y: y.target() == vertex, list(vertex.all_edges()))].__len__()


def get_child_count(g, vertex):
    return [g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, list(vertex.all_edges()))].__len__()


def get_children(g, vertex):
    return sorted([g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, list(vertex.all_edges()))],
                  key=lambda z: g.vp.title[z], reverse=True)


def load_graph():
    with open('graph_final.pickle', 'rb') as handle:
        return pickle.load(handle)


class App(Frame):
    def __init__(self, parent, datasets):
        Frame.__init__(self, parent, padx=5, pady=5)
        self.graphStatusText = StringVar()
        self.TopFrame = Frame(parent)
        self.parent = parent
        self.datasets = datasets

        self.tree_reducer = None
        self.operation = StringVar()
        self.chosenDatasetName = StringVar()
        self.childCount = IntVar()
        self.articleCount = IntVar()
        self.chosenDataset = self.datasets["simple"]
        self.tree_reducer = TreeReducer(self.chosenDataset)
        self.isGraphPresent = TreeReducer.isGraphPresent(self.tree_reducer)
        self.initUI()

    def newselection(self, event):
        self.chosenDatasetName = self.chooseCombo.get()
        self.chosenDataset = self.datasets[self.chosenDatasetName]
        self.tree_reducer = TreeReducer(self.chosenDataset)
        self.isGraphPresent = TreeReducer.isGraphPresent(self.tree_reducer)
        if self.isGraphPresent:
            self.reduceButton.state(["!disabled"])
            self.graphStatusText.set("Ok, graph present")
        else:
            self.reduceButton.state(["disabled"])
            self.graphStatusText.set("Graph not found")

    def buildGraph(self):
        self.operation.set("Creating input graph...")
        self.tree_reducer.create_graph()
        self.isGraphPresent = TreeReducer.isGraphPresent(self.tree_reducer)
        if self.isGraphPresent:
            self.reduceButton.state(["!disabled"])
            self.graphStatusText.set("Ok, graph present")

    def reduce(self):
        self.tree.delete(*self.tree.get_children())
        self.tree_reducer = TreeReducer(self.chosenDataset)
        self.tree_reducer.load_graph()
        self.g = self.tree_reducer.run_reductions(self.childCount, self.articleCount)
        self.create_tree()

    def initUI(self):
        self.parent.title("Wikipedia Category Tree")
        self.center_window()
        self.TopFrame.pack()
        self.pack(fill=BOTH, expand=1)
        # Top Frame
        self.chooseLabel = ttk.Label(self.TopFrame, text="Dataset", font=("Helvetica", 12))
        self.graphLabel = ttk.Label(self.TopFrame, text="Input graph", font=("Helvetica", 12))
        self.graphStatus = ttk.Label(self.TopFrame, textvariable=self.graphStatusText, font=("Helvetica", 12))

        self.buildGraphButton = ttk.Button(self.TopFrame, text='Generate input graph', command=self.buildGraph)
        self.reduceButton = ttk.Button(self.TopFrame, text='Generate output graph', command=self.reduce)

        self.childCountLabel = ttk.Label(self.TopFrame, text="Min Child count:", font=("Helvetica", 12))
        self.childCountInput = ttk.Entry(self.TopFrame, textvariable=self.childCount)
        self.articleCountLabel = ttk.Label(self.TopFrame, text="Min Article count:", font=("Helvetica", 12))
        self.articleCountInput = ttk.Entry(self.TopFrame, textvariable=self.articleCount)

        self.chosenDatasetName = StringVar()
        self.chooseCombo = ttk.Combobox(self.TopFrame, textvariable=self.chosenDatasetName, state='readonly')
        self.chooseCombo['values'] = ("simple", "polish")
        self.chooseCombo.bind("<<ComboboxSelected>>", self.newselection)
        self.chooseLabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.chooseCombo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.graphLabel.grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.graphStatus.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.buildGraphButton.grid(row=0, column=4, sticky="w", padx=5, pady=5)

        self.childCountLabel.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.childCountInput.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.articleCountLabel.grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.articleCountInput.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        self.reduceButton.grid(row=1, column=4, sticky="w", padx=5, pady=5)

        # Tree
        self.tree = ttk.Treeview(self)
        self.scrollbar = Scrollbar(self)
        self.tree.grid(row=1, column=0, sticky="nesw", columnspan=2)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.scrollbar.config(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1, sticky='ns')

        # Set state
        self.chosenDatasetName.set("simple")
        self.childCount.set(5)
        self.articleCount.set(10)
        if self.isGraphPresent:
            self.reduceButton.state(["!disabled"])
            self.graphStatusText.set("Ok, graph present")
        else:
            self.reduceButton.state(["disabled"])
            self.graphStatusText.set("Graph not found")

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
    datasets = {"simple": Dataset("simple", 'data/simple/categories', 'data/simple/simple-20120104-titlecat.twr',
                                  'data/simple/simple-20120104-pagecount.twr',
                                  'data/simple/simple-20120104-catlinks.twr', '\t'),
                "polish": Dataset("polish", 'data/polish/simple-20120104-cattreeid.twr',
                                  'data/polish/simple-20120104-titlecat.twr',
                                  'data/polish/simple-20120104-pagecount.twr',
                                  'data/polish/simple-20120104-catlinks.twr', ' ')}

    App(root, datasets)
    root.mainloop()


if __name__ == '__main__':
    main()
