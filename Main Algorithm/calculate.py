import networkx as nx
# import matplotlib.pyplot as plt
from numpy import *
import numpy as np
import scipy as sp


class Calculate(object):
    def __init__(self):
        pass

    def top_ten(self, rank_):
        rank_top = sorted(rank_.items(), key=lambda d: d[1], reverse=True)
        top = []
        for i in range(10):
            top.append(rank_top[i])
        print(top)
        return dict(top)

    def load(self):
        article_list = open('topfourcites.txt', encoding="utf8").read()
        article_list = article_list.replace('\n   ', '\t')
        article_list = article_list.split('\n')
        cite_list = [ab[3:] for ab in article_list if ab[:2] == "CR"]
        cite_list = [[c for c in cite.split('\t')] for cite in cite_list]

        cite_dict = {}
        edge_dict = {}

        for cites in cite_list:
            cite_list = []
            for cite in cites:
                split = cite.split(', ')
                try:
                    id = split[0].upper().replace(' ', ' ').replace('.', '') + ' ' + split[1]
                    ids = id.split()
                    for i in ids:
                        if len(i) > 2:
                            new = i[0].upper() + i[1:].lower()
                            id = id.replace(i, new)
                except:
                    pass
                else:

                    if id not in cite_list:
                        if id in cite_dict:
                            cite_dict[id] = cite_dict[id] + 1
                        else:
                            cite_dict[id] = 1

                        if len(cite_list) > 0:
                            for cite in cite_list:
                                if (id, cite) in edge_dict:
                                    edge_dict[(id, cite)] = edge_dict[(id, cite)] + 1
                                elif (cite, id) in edge_dict:
                                    edge_dict[(cite, id)] = edge_dict[(cite, id)] + 1
                                else:
                                    edge_dict[(id, cite)] = 1
                        cite_list.append(id)
                        # print(id)

        import networkx as nx

        G = nx.DiGraph()
        counter = 0
        for edge in edge_dict:
            if edge_dict[edge] > 3 and cite_dict[edge[0]] >= 8 and cite_dict[edge[1]] >= 8:
                G.add_edge(edge[0], edge[1], weight=edge_dict[edge])
                counter = counter + 1
                # print(counter)

        for node in G:
            G.add_node(node, freq=cite_dict[node])

        in_degree_c = nx.in_degree_centrality(G)
        sorted_by_value = sorted(in_degree_c.items(), key=lambda kv: kv[1])

        pr = nx.pagerank(G, alpha=0.85)
        sorted_by_value = sorted(pr.items(), key=lambda kv: kv[1])

        G2 = G.to_undirected()
        entrality = nx.eigenvector_centrality(G2)
        sorted_by_value = sorted(entrality.items(), key=lambda kv: kv[1])
        return G, G2

    def degree(self, figure):
        '''return in_result, out_result of each node in the figure'''
        out_result = {node: 0
                     for node in figure}
        in_result = {node: 0
                     for node in figure}
        # print(figure[1])
        for i in figure:
            # print(type(i))
            for j in figure[i]:
                in_result[j] += 1
                out_result[i] += 1
        mean1 = average(list(in_result.values()))
        var1 = np.std(list(in_result.values()))
        mean2 = average(list(out_result.values()))
        var2 = np.std(list(out_result.values()))
        for i in figure:
            in_result[i] = (in_result[i]-mean1) / var1
            out_result[i] = (out_result[i]-mean2) /var2
        return in_result, out_result

    def eigenvector_centrality(self, figure):
        '''return eigenvector_centrality of each node in figure'''
        # centrality = nx.eigenvector_centrality_numpy(figure)
        # import scipy as sp
        nodelist = list(figure)
        length = len(figure)
        index = dict(zip(nodelist, range(length)))

        M = np.zeros((length, length))
        for i in figure:
            for j in figure[i]:
                M[index[i]][index[j]] = 1
                M[index[j]][index[i]] = 1
        u = 1/length
        red_eig_vects = np.zeros(length)
        for i in range(length):
            red_eig_vects[i] = u
        red_eig_vects = mat(red_eig_vects).T
        for i in range(200):
            red_eig_vects = M * red_eig_vects
            red_eig_vects /= linalg.norm(red_eig_vects)
        return dict(zip(figure, red_eig_vects))

    def page_rank(self, figure, itera):
        length = len(figure)
        out_d = np.zeros([length])
        nodelist = list(figure)
        index = dict(zip(nodelist, range(length)))
        for i in figure:
            for j in figure[i]:
                out_d[index[i]] += 1
        length = len(figure)
        nodelist = list(figure)
        out_mat = np.zeros((length, length))
        for i in range(length):
            out_mat[i][i] = out_d[i]
        out_mat[out_mat != 0] = 1 / out_mat[out_mat != 0]
        index = dict(zip(nodelist, range(length)))
        M = np.zeros((length, length))
        for i in figure:
            for j in figure[i]:
                M[index[i]][index[j]] = 1
        _P = out_d * M
        w_ = np.array(1 / length)
        w = mat(w_.repeat(length)).T
        d = np.zeros([length])
        for i in range(length):
            if out_d[i] == 0:
                d[i] = 1
        P = _P + w*d
        e = mat(np.ones(length)).T
        v = w_.repeat(length)
        G = 0.85 * P + 0.15 * e * v
        pai = v
        for i in range(itera):
            pai = pai*G
            pai = pai/np.linalg.norm(pai)
        return dict(zip(figure, pai.T))

    def writedata(self,figure, num):
        DG = nx.DiGraph()
        edges = list(G.edges)
        for i, j in edges:
            if j in figure.keys():
                DG.add_edge(i, j)
        if num == 1:
            name = 'in_degree_file.gexf'
        elif num == 2:
            name = 'out_degree_file.gexf'
        elif num == 3:
            name = 'centrality_file.gexf'
        else:
            name = 'page_rank_file.gexf'
        nx.write_gexf(DG, name)

if __name__ == '__main__':

    Main = Calculate()
    G,_ = Main.load()
    in_, out_ = Main.degree(G)
    centrality = Main.eigenvector_centrality(G)
    rank = Main.page_rank(G, 100)
    top = Main.top_ten(rank)
    print(type(top))
    # Main.writedata(top,3)
    print('finish')







