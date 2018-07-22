

article_list=open('topfourcites.txt', encoding="utf8").read()
article_list=article_list.replace('\n   ','\t')
article_list=article_list.split('\n')
cite_list=[ab[3:] for ab in article_list if ab[:2]=="CR"]
cite_list=[[c for  c in cite.split('\t')] for cite in cite_list]




cite_dict={}
edge_dict={}

for cites in cite_list:
    cite_list=[]
    for cite in cites:
        split=cite.split(', ')
        try:
            id=split[0].upper().replace(' ',' ').replace('.','')+' '+split[1]
            ids=id.split()
            for i in ids:
                if len(i)>2:
                    new=i[0].upper()+i[1:].lower() 
                    id=id.replace(i,new)
        except: 
            print ('Eror with ',split)
        else:
            
            if id not in cite_list:
                if id in cite_dict:
                    cite_dict[id]=cite_dict[id]+1
                else:
                    cite_dict[id]=1
                    
                if len(cite_list)>0:
                    for cite in cite_list:
                        if (id,cite) in edge_dict:
                            edge_dict[(id,cite)]=edge_dict[(id,cite)]+1
                        elif (cite,id) in edge_dict:
                            edge_dict[(cite,id)]=edge_dict[(cite,id)]+1
                        else:
                            edge_dict[(id,cite)]=1
                cite_list.append(id)
                print(id)


import networkx as nx
G=nx.DiGraph()
counter=0
for edge in edge_dict:
    if edge_dict[edge]>3 and cite_dict[edge[0]]>=8 and cite_dict[edge[1]]>=8 :
        G.add_edge(edge[0],edge[1],weight=edge_dict[edge])
        counter=counter+1
        print(counter)
        
for node in G:    
    G.add_node(node,freq=cite_dict[node])
    
in_degree_c = nx.in_degree_centrality(G)
sorted_by_value = sorted(in_degree_c.items(), key=lambda kv: kv[1])

pr = nx.pagerank(G, alpha=0.85)
sorted_by_value = sorted(pr.items(), key=lambda kv: kv[1])

G2 = G.to_undirected()
entrality = nx.eigenvector_centrality(G2)
sorted_by_value = sorted(entrality.items(), key=lambda kv: kv[1])

