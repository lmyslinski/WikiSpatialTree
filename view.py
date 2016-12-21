import pickle
from Tkinter import Tk, Frame, BOTH, Scrollbar, StringVar
import ttk

from preprocessing.builder import Dataset


def get_roots(g):
    roots = []
    for vertex in g.vertices():
        # BUG override - the child count is necessary due to graph tool not removing some nodes NO_MATTER_WHAT(WTF?)
        if get_parent_count(g, vertex) == 0 and get_child_count(g, vertex) > 0:
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
        self.TopFrame = Frame(parent)
        self.parent = parent
        self.datasets = datasets
        self.initUI()
        self.g = load_graph()
        self.create_tree()

    def newselection(self, event):
        self.chosenDatasetName = self.chooseCombo.get()
        self.chosenDataset = self.datasets[self.chosenDatasetName]

    def buildGraph(self):
        print("graph")

    def reduce(self):
        print("reducing")

    def initUI(self):
        self.parent.title("Wikipedia Category Tree")
        self.center_window()
        self.TopFrame.pack()
        self.pack(fill=BOTH, expand=1)
        # Top Frame
        self.chooseLabel = ttk.Label(self.TopFrame, text="Dataset", font=("Helvetica", 12))
        self.graphLabel = ttk.Label(self.TopFrame, text="Input graph", font=("Helvetica", 12))
        self.graphStatus = ttk.Label(self.TopFrame, text="Ok, present", font=("Helvetica", 12))

        self.buildGraphButton = ttk.Button(self.TopFrame, text='Generate input graph', command=self.buildGraph)
        self.reduceButton = ttk.Button(self.TopFrame, text='Generate output graph', command=self.reduce)

        self.childCountLabel = ttk.Label(self.TopFrame, text="Min Child count:", font=("Helvetica", 12))
        self.childCount = ttk.Entry(self.TopFrame)
        self.articleCountLabel = ttk.Label(self.TopFrame, text="Min Article count:", font=("Helvetica", 12))
        self.articleCount = ttk.Entry(self.TopFrame)

        self.chosenDatasetName = StringVar()
        self.chosenDatasetName.set("simple")
        self.chosenDataset = self.datasets["simple"]
        self.chooseCombo = ttk.Combobox(self.TopFrame, textvariable=self.chosenDatasetName, state='readonly')
        self.chooseCombo['values'] = ("simple", "polish")
        self.chooseCombo.bind("<<ComboboxSelected>>", self.newselection)
        self.chooseLabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.chooseCombo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.graphLabel.grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.graphStatus.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.buildGraphButton.grid(row=0, column=4, sticky="w", padx=5, pady=5)

        self.childCountLabel.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.childCount.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.articleCountLabel.grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.articleCount.grid(row=1, column=3, sticky="w", padx=5, pady=5)
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
    datasets = {}
    datasets["simple"] = Dataset("simple", 'data/simple/categories', 'data/simple/simple-20120104-titlecat.twr',
                                 'data/simple/simple-20120104-pagecount.twr',
                                 'data/simple/simple-20120104-catlinks.twr','\t')
    datasets["polish"] = Dataset("polish", 'data/polish/simple-20120104-cattreeid.twr',
                                 'data/polish/simple-20120104-titlecat.twr',
                                 'data/polish/simple-20120104-pagecount.twr',
                                 'data/polish/simple-20120104-catlinks.twr',' ')

    App(root, datasets)
    root.mainloop()


if __name__ == '__main__':
    main()
