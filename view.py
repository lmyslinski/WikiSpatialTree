# coding=utf-8
import pickle
from Tkinter import Tk, Frame, BOTH, Scrollbar, StringVar, IntVar, Listbox, END
import ttk

from app import TreeReducer
from preprocessing.builder import Dataset


def get_roots(g):
    roots = []
    for vertex in g.vertices():
        if get_parent_count(g, vertex) == 0:
            roots.append(vertex)
    return sorted(roots, key=lambda x: g.vp.title[x], reverse=True)


def get_parent_count(g, vertex):
    return [g.vertex(x.source()) for x in filter(lambda y: y.target() == vertex, list(vertex.all_edges()))].__len__()


def get_child_count(g, vertex):
    return g.vp.child_count[vertex]


def get_children(g, vertex):
    return sorted([g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, list(vertex.all_edges()))],
                  key=lambda z: g.vp.title[z], reverse=True)


class App(Frame):
    def __init__(self, parent, datasets):
        Frame.__init__(self, parent, padx=5, pady=5)
        self.graphStatusText = StringVar()
        self.top_frame = Frame(parent)
        self.right_frame = Frame(parent)
        self.parent = parent
        self.datasets = datasets

        self.tr = None
        self.g = None
        self.operation = StringVar()
        self.chosenDatasetName = StringVar()
        self.childCount = IntVar()
        self.articleCount = IntVar()
        self.search_text = StringVar()
        self.chosenDataset = self.datasets["simple"]
        self.tr = TreeReducer(self.chosenDataset)
        self.isGraphPresent = False
        self.initUI()

    def validate_buttons(self):
        if self.isGraphPresent:
            self.reduceButton.state(["!disabled"])
            self.centralityButton.state(["!disabled"])
        else:
            self.reduceButton.state(["disabled"])
            self.centralityButton.state(["disabled"])

    def newselection(self, event):
        self.chosenDatasetName = self.chooseCombo.get()
        self.chosenDataset = self.datasets[self.chosenDatasetName]
        self.tr = TreeReducer(self.chosenDataset)
        self.isGraphPresent = False
        self.validate_buttons()

    def load_graph(self):
        with open('data/' + self.chosenDatasetName + '/graph.pickle', 'rb') as handle:
            self.g = pickle.load(handle)
            self.create_tree()
            self.isGraphPresent = TreeReducer.isGraphPresent(self.tr)
            self.validate_buttons()

    def load_final_graph(self):
        with open('data/' + self.chosenDatasetName + '/graph_final.pickle', 'rb') as handle:
            self.g = pickle.load(handle)
            self.create_tree()
            self.isGraphPresent = TreeReducer.isGraphPresent(self.tr)
            self.validate_buttons()

    def reduce(self):
        self.tr = TreeReducer(self.chosenDataset)
        self.tr.g = self.g
        self.tr.remove_unconnected_categories()
        self.tr.reduce_to_single_parent()
        self.tr.remove_matched_categories()
        self.tr.calculate_children_count()
        self.tr.merge_by_criteria(5, 10)
        self.tr.delete_just_to_be_sure()
        self.g = self.tr.g
        print list(self.g.vertices()).__len__()
        self.create_tree()
        print ("Reduction done")
        with open('data/' + self.chosenDatasetName + '/graph_final.pickle', 'wb') as handle:
            pickle.dump(self.g, handle)

    def calculate_centrality(self):
        self.tr.g = self.g
        self.tr.calculate_centrality()
        self.g = self.tr.g
        with open('data/' + self.chosenDatasetName + '/graph_final.pickle', 'wb') as handle:
            pickle.dump(self.g, handle)

        self.create_tree()

    def selectItem(self, event):
        self.articles_box.delete(0, END)
        self.merged_categories_box.delete(0, END)
        self.rejected_parents_box.delete(0, END)
        curItem = self.tree.focus()
        if curItem is not '':
            id = self.tree.item(curItem)['values'][3]
            for merged_category in sorted(self.g.vp.merged_categories[id]):
                self.merged_categories_box.insert(END, merged_category)

            for rejected_parent in sorted(self.g.vp.rejected_parents[id]):
                self.rejected_parents_box.insert(END, rejected_parent)

            for article in sorted(self.g.vp.articles[id]):
                self.articles_box.insert(END, article)

    def initUI(self):
        self.parent.title("Wikipedia Category Tree")
        self.center_window()
        self.top_frame.pack()
        self.right_frame.pack()
        self.pack(fill=BOTH, expand=1)
        self.chooseLabel = ttk.Label(self.top_frame, text="Dataset", font=("Helvetica", 12))

        self.reduceButton = ttk.Button(self.top_frame, text='Reduce', command=self.reduce)
        self.loadButton = ttk.Button(self.top_frame, text='Load graph', command=self.load_graph)
        self.load_final_button = ttk.Button(self.top_frame, text='Load final graph', command=self.load_final_graph)
        self.centralityButton = ttk.Button(self.top_frame, text='Calculate centrality',
                                           command=self.calculate_centrality)

        self.childCountLabel = ttk.Label(self.top_frame, text="Min Child count:", font=("Helvetica", 12))
        self.childCountInput = ttk.Entry(self.top_frame, textvariable=self.childCount)
        self.articleCountLabel = ttk.Label(self.top_frame, text="Min Article count:", font=("Helvetica", 12))
        self.articleCountInput = ttk.Entry(self.top_frame, textvariable=self.articleCount)

        self.chooseCombo = ttk.Combobox(self.top_frame, textvariable=self.chosenDatasetName, state='readonly')
        self.chooseCombo['values'] = ("simple", "polish")
        self.chooseCombo.bind("<<ComboboxSelected>>", self.newselection)
        self.chooseLabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.chooseCombo.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        self.childCountLabel.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.childCountInput.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.articleCountLabel.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.articleCountInput.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.reduceButton.grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.loadButton.grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.load_final_button.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.centralityButton.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        # self.searchLabel.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Tree with sidebar


        # Tree
        self.tree = ttk.Treeview(self, columns=(1, 2, 3, 4, 5))
        self.tree.heading("#0", text="Category")
        self.tree.column("#0", width=100)
        self.tree.heading("#1", text="No. children")
        self.tree.column("#1", width=80)
        self.tree.heading("#2", text="No. articles")
        self.tree.column("#2", width=80)
        self.tree.heading("#3", text="Centrality")
        self.tree.column("#3", width=80)
        self.tree.heading("#4", text="ID")
        self.tree.column("#4", width=20)
        self.tree_scrollbar = Scrollbar(self)
        self.articles_box_scrollbar = Scrollbar(self)
        self.merged_categories_scrollbar = Scrollbar(self)
        self.rejected_parents_scrollbar = Scrollbar(self)
        self.tree.grid(row=0, column=0, sticky="nesw", columnspan=2, rowspan=6)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=6)
        self.rowconfigure(3, weight=4)
        # self.rowconfigure(1, weight=1)
        self.tree_scrollbar.config(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree.bind('<ButtonRelease-1>', self.selectItem)
        self.tree.bind('<KeyRelease-Down>', self.selectItem)
        self.tree.bind('<KeyRelease-Up>', self.selectItem)

        self.tree_scrollbar.grid(row=0, column=1, sticky='ns', rowspan=6)

        self.article_box_label = ttk.Label(self, text="Articles", font=("Helvetica", 12))
        self.article_box_label.grid(row=0, column=2)

        self.articles_box = Listbox(self)
        self.articles_box.grid(row=1, column=2, sticky='ns', padx=(5, 0))

        self.articles_box.configure(yscrollcommand=self.articles_box_scrollbar.set)
        self.articles_box_scrollbar.config(command=self.articles_box.yview)
        self.articles_box_scrollbar.grid(row=1, column=3, sticky='ns')

        self.merged_categories_label = ttk.Label(self, text="Merged categories", font=("Helvetica", 12))
        self.merged_categories_label.grid(row=2, column=2)

        self.rejected_parents = ttk.Label(self, text="Rejected parents", font=("Helvetica", 12))
        self.rejected_parents.grid(row=4, column=2)

        self.merged_categories_box = Listbox(self)
        self.merged_categories_box.grid(row=3, column=2, sticky='ns', padx=(5, 0))

        self.rejected_parents_box = Listbox(self)
        self.rejected_parents_box.grid(row=5, column=2, sticky='ns', padx=(5, 0))

        self.merged_categories_box.configure(yscrollcommand=self.merged_categories_scrollbar.set)
        self.merged_categories_scrollbar.config(command=self.merged_categories_box.yview)
        self.merged_categories_scrollbar.grid(row=3, column=3, sticky='ns')

        self.rejected_parents_box.configure(yscrollcommand=self.rejected_parents_scrollbar.set)
        self.rejected_parents_scrollbar.config(command=self.rejected_parents_box.yview)
        self.rejected_parents_scrollbar.grid(row=5, column=3, sticky='ns')

        # Set state
        self.childCount.set(5)
        self.articleCount.set(10)
        self.validate_buttons()

    def center_window(self):
        w = 800
        h = 600
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def create_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        roots = get_roots(self.g)
        [self.add_children(root, "", 0) for root in roots]

    def add_children(self, parent, parent_id, depth):
        if depth < 4:
            id = self.tree.insert(parent_id, 0, text=str(self.g.vp.title[parent]), values=(
                str(self.g.vp.child_count[parent]),
                str(self.g.vp.articles[parent].__len__()),
                "%2f" % self.g.vp.harmonic_centrality[parent],
                parent))

            self.tree.item(id, open=True)
            children = get_children(self.g, parent)
            for child in children:
                if child != parent:
                    self.add_children(child, id, depth + 1)


def main():
    root = Tk()
    datasets = {"simple": Dataset("simple", 'data/simple/categories', 'data/simple/simple-20120104-titlecat.twr',
                                  'data/simple/simple-20120104-catlinks.twr',
                                  'data/simple/simple-20120104-pagetitle.twr',
                                  '\t', "Articles"),
                "polish": Dataset("polish", 'data/polish/simple-20120104-cattreeid.twr',
                                  'data/polish/simple-20120104-titlecat.twr',
                                  'data/polish/simple-20120104-catlinks.twr',
                                  'data/polish/simple-20120104-pagetitle.twr',
                                  ' ', "Kategorie")}

    App(root, datasets)
    root.mainloop()


if __name__ == '__main__':
    main()
