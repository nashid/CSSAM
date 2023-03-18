from tree_sitter import Language, Parser
import ast
# import astpretty
import re
import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt
# import nxviz

PY_LANGUAGE = Language('../build/my-languages.so', 'python')
parser = Parser()
parser.set_language(PY_LANGUAGE)

data_flow = ['identifier', 'integer', 'float', 'true', 'false', 'none']


def parse_py(node):
    if node == None:
        return
    print(node)
    for child in node.children:
        parse_py(child)

def getIDL(code, node, idl):
    if node == None:
        return idl
    if node.type == 'call':
        if node.children[0].type != 'attribute':
            idl.append(code[node.children[0].start_byte:node.children[0].end_byte])
            return idl
    for i in node.children:
        if i.type in data_flow:
            idl.append(code[i.start_byte:i.end_byte])
        elif i.type == 'string':
            idl.append(code[i.start_byte+1:i.end_byte-1])
        else:
            getIDL(code,i,idl)
    return idl
def callgetIDL(code, node, idl):
    if node == None:
        return idl
    for i in node.children:
        if i.type in data_flow:
            idl.append(code[i.start_byte:i.end_byte])
        elif i.type == 'string':
            idl.append(code[i.start_byte+1:i.end_byte-1])
        else:
            getIDL(code,i,idl)
    return idl


def parse_tree(code, parent_node ,node, G):
    if node == None:
        return G
    #将字符串合并为一整个节点，而不是每个单词一个节点
    if node.type == 'string':
        G.add_edge(parent_node.type, node.type,weight=0.6)
        G.add_edge(node.type, code[node.children[0].start_byte+1: node.children[-1].end_byte-1],weight=0.6)
        return G

    if parent_node and node:
        node_1 = parent_node.type
        node_2 = node.type
        if node_1 == 'identifier':
            node_1 = code[parent_node.start_byte:parent_node.end_byte]
        if node_2 == 'identifier':
            node_2 = code[node.start_byte:node.end_byte]
        G.add_edge(node_1, node_2,weight=0.6)
    if node.type == 'assignment'or node.type == 'call':
        tmp = []
        count = 1
        if node.type == 'call':
            idl = callgetIDL(code, node, tmp)
        else:
            idl = getIDL(code, node, tmp)

        fid = idl[:count]
        idl = idl[count:]
        #print(fid)
        print(idl)
        #print(node.children[0])
        for id in idl:
            G.add_edge(id,fid[0],weight=0.4)

    if not node.children and node.type != 'identifier':
        G.add_edge(node.type, code[node.start_byte:node.end_byte],weight=0.6)
    #print(stri+str(node.type))
    #stri += '    '

    for child in node.children:
        G = parse_tree(code, node, child, G)
    return G

if __name__ == '__main__':
    code ="def resource_patch(context, data_dict):\n\t_check_access('resource_patch', context, data_dict)\n\tshow_context = {'model': context['model'], 'session': context['session'], 'user': context['user'], 'auth_user_obj': context['auth_user_obj']}\n\tresource_dict = _get_action('resource_show')(show_context, {'id': _get_or_bust(data_dict, 'id')})\n\tpatched = dict(resource_dict)\n\tpatched.update(data_dict)\n\treturn _update.resource_update(context, patched)\n"


    tree = parser.parse(bytes(code, "utf8"))
    # print(tree.root_node.children[0])
    parse_py(tree.root_node)
    # print(tree.root_node)
    # print(tree.root_node.children)
    # print(tree.root_node.children[0].children)
    # print(tree.root_node.children[0].children[1].start_byte)
    G = nx.DiGraph()
    Gr = parse_tree(code ,None ,tree.root_node, G)
    # options = {
    #     'node_size': 1000,
    #     'width': 2,
    # }
    # print(list(G.edges))
    # plt.figure(figsize=(8, 6))
    # nx.draw(Gr, with_labels=True, **options)
    #
    # plt.savefig('example.png', dpi=600, format='png')
    # plt.show()
    elarge = [(u, v) for (u, v, d) in Gr.edges(data=True) if d["weight"] > 0.5]
    esmall = [(u, v) for (u, v, d) in Gr.edges(data=True) if d["weight"] <= 0.5]

    #pos = nx.planar_layout(G, scale=1, center=None, dim=2)
    #pos = nx.kamada_kawai_layout(G, dist=None, pos=None, weight='weight', scale=1, center=None, dim=2)
    #pos = nx.shell_layout(Gr,scale=1)  # positions for all nodes
    pos = nx.random_layout(Gr)
    # nodes
    nx.draw_networkx_nodes(Gr, pos, node_size=300)

    # edges
    nx.draw_networkx_edges(Gr, pos, edgelist=elarge, width=1)
    nx.draw_networkx_edges(
        Gr, pos, edgelist=esmall, width=1, alpha=0.5, edge_color="b", style="dashed"
    )
    # labels
    nx.draw_networkx_labels(Gr, pos, font_size=10, font_family="sans-serif")

    plt.axis("off")
    plt.savefig('example.png', dpi=600, format='png')
    plt.show()