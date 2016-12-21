from preprocessing import builder
import os
import re
import pickle

from preprocessing.builder import Dataset


class TreeReducer:
    def __init__(self, dataset):
        self.pattern = re.compile('|'.join(["stub[_s \ Z]",
                                            "(_-\ A)articles(_-\ Z)",
                                            "template",
                                            "wikipedia \ Z",
                                            "(_-\ A)disambiguation(_-\ Z)",
                                            "(_-\ A)(deaths-births)(_-\ Z)",
                                            "(_-\ A) \ d+s?(_BC)?(_-\ Z)",
                                            "years",
                                            "(_-\ A)century(_-\ Z)",
                                            "(_-\ A)(millennia-millennium)(_-\ Z)",
                                            "(_-\ A)(unknown-uncertain)(_-\ Z)",
                                            ". * _language_films. *",
                                            "_by_year",
                                            "_century",
                                            "_shot_in",
                                            "female_",
                                            "male_",
                                            "with_proper_names",
                                            "people_who",
                                            "Albums_with_cover_art_by_",
                                            "speaking_countries",
                                            "alumni",
                                            "_screenwriters"]))

        self.list_pattern = re.compile('|'.join([".*_by_"]))
        self.dataset = dataset
        self.deletion_list = []
        self.g = None

    def get_most_important_parent(self, vertex, parents):
        best_parent = parents[0]
        if parents.__len__() > 1:
            min_distance = 10000
            for parent in parents:
                common_links = list(
                    set(self.g.vp.category_links[vertex]).intersection(self.g.vp.category_links[parent]))
                distance = common_links.__len__()
                if distance < min_distance:
                    min_distance = distance
                    best_parent = parent
        return best_parent

    def filter_by_name(self, title):
        return re.search(self.pattern, title) is not None

    def filter_by_list_pattern(self, title):
        return re.search(self.list_pattern, title) is not None

    def get_parents_children(self, vertex, edges):
        parents = [self.g.vertex(x.source()) for x in filter(lambda y: y.target() == vertex, edges)]
        children = [self.g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, edges)]
        return parents, children

    def get_parents(self, vertex, edges):
        return [self.g.vertex(x.source()) for x in filter(lambda y: y.target() == vertex, edges)]

    def get_children(self, vertex, edges):
        return [self.g.vertex(x.target()) for x in filter(lambda y: y.target() != vertex, edges)]

    # filter parents to exclude parent-child cycles
    def get_parents_without_cycles(self, parents, children):
        return [x for x in filter(lambda p: p not in children, parents)]

    def get_leftover_edges(self, vertex, edges, parent):
        return [x for x in filter(lambda y: y.target() == vertex and y.source() != parent, edges)]

    def get_parent_edges(self, vertex, edges):
        return [x for x in filter(lambda y: y.target() == vertex, edges)]

    def get_child_edges(self, vertex, edges):
        return [x for x in filter(lambda y: y.target() != vertex, edges)]

    def merge_vertex(self, vertex, edges, parents, children):
        self.deletion_list.append(vertex)
        parent = self.get_most_important_parent(vertex, parents)
        self.g.vp.merged_categories[parent].append(vertex)
        self.g.vp.article_count[parent] += self.g.vp.article_count[vertex]
        for child in children:
            if self.g.edge(parent, child) is None:
                self.g.add_edge(parent, child, add_missing=True)
            map(self.g.remove_edge, edges)

    def match_criteria(self, vertex, child_count, article_count):
        return self.g.vp.child_count[vertex] < child_count or self.g.vp.article_count[
                                                                  vertex] < article_count or self.filter_by_name(
            self.g.vp.title[vertex])

    def match_list(self, vertex):
        return self.filter_by_list_pattern(self.g.vp.title[vertex])

    def load_graph(self):
        with open('data/' + self.dataset.name + '/graph.pickle', 'rb') as handle:
            self.g = pickle.load(handle)
            print "Graph loaded"

    def create_graph(self):
        matrix = builder.build_matrix(self.dataset)
        builder.build_graph(matrix, self.dataset)

    def isGraphPresent(self):
        return os.path.exists('data/' + self.dataset.name + '/graph.pickle')

    def mark_categories_for_deletion(self):
        for vertex in self.g.vertices():
            edges = list(vertex.all_edges())
            if edges.__len__() == 0:
                self.deletion_list.append(vertex)

    def merge_by_criteria(self, child_count, article_count):
        for vertex in self.g.vertices():
            edges = list(vertex.all_edges())
            parents, children = self.get_parents_children(vertex, edges)
            if parents.__len__() != 0 and self.match_criteria(vertex, child_count, article_count):
                self.merge_vertex(vertex, edges, parents, children)

    def reduce_to_single_parent(self):
        for vertex in self.g.vertices():
            edges = list(vertex.all_edges())
            parents, children = self.get_parents_children(vertex, edges)
            parents_without_children = self.get_parents_without_cycles(parents, children)
            if parents.__len__() > 1:
                best_parent = self.get_most_important_parent(vertex, parents_without_children)
                leftover_parent_edges = self.get_leftover_edges(vertex, edges, best_parent)
                map(self.g.remove_edge, leftover_parent_edges)

    def extract_lists(self):
        lists_root = self.g.add_vertex()
        roots = []
        self.g.vp.title[lists_root] = "Lists"

        def filter_lists(vertex):
            edges = list(vertex.all_edges())
            if self.match_list(vertex):
                parent_edges = self.get_parent_edges(vertex, edges)
                map(self.g.remove_edge, parent_edges)
                self.g.add_edge(lists_root, vertex)
            else:
                children = self.get_children(vertex, edges)
                for child in children:
                    filter_lists(child)

        # get roots
        for vertex in self.g.vertices():
            edges = list(vertex.all_edges())
            parents = self.get_parents(vertex, edges)
            if parents.__len__() == 0:
                roots.append(vertex)

        for vertex in roots:
            filter_lists(vertex)

    def delete_categories(self):
        for v in reversed(sorted(self.deletion_list)):
            self.g.remove_vertex(v)

    def run_reductions(self, child_count, article_count):
        self.deletion_list = []
        self.mark_categories_for_deletion()
        self.merge_by_criteria(child_count, article_count)
        self.reduce_to_single_parent()
        self.delete_categories()
        self.extract_lists()
        with open('data/' + self.dataset.name + '/graph_final.pickle', 'wb') as handle:
            pickle.dump(self.g, handle)
        return self.g