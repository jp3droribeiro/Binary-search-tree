import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import os  

os.system('streamlit run binary_search_tree.py --server.port $PORT')

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, root, key):
        if root is None:
            return Node(key)
        if key < root.key:
            root.left = self._insert(root.left, key)
        elif key > root.key:
            root.right = self._insert(root.right, key)
        return root

    def inorder_traversal(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, root, result):
        if root:
            self._inorder_traversal(root.left, result)
            result.append(root.key)
            self._inorder_traversal(root.right, result)

    def postorder_traversal(self):
        result = []
        self._postorder_traversal(self.root, result)
        return result

    def _postorder_traversal(self, root, result):
        if root:
            self._postorder_traversal(root.left, result)
            self._postorder_traversal(root.right, result)
            result.append(root.key)

    def preorder_traversal(self):
        result = []
        self._preorder_traversal(self.root, result)
        return result

    def _preorder_traversal(self, root, result):
        if root:
            result.append(root.key)
            self._preorder_traversal(root.left, result)
            self._preorder_traversal(root.right, result)

    def breadth_first_traversal(self):
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            if node:
                result.append(node.key)
                queue.append(node.left)
                queue.append(node.right)
        return result

    def plot_tree(self):
        # adjust the size
        num_nodes = self.count_nodes(self.root)
        plt.figure(figsize=(max(8, num_nodes * 0.5), max(6, num_nodes * 0.3)))

        # Subplot
        plt.subplot(1, 2, 1)
        graph = nx.Graph()
        self._build_tree_graph(graph, self.root)
        pos = self._generate_positions(graph)
        labels = {node: node.key for node in graph.nodes()}
        nx.draw(graph, pos, labels=labels, with_labels=True, node_size=700, node_color="skyblue", font_size=8)
        plt.title('Árvore de Busca Binária')
        

        plt.axis('off') 
    
        plt.subplot(1, 2, 2)
        in_order = self.inorder_traversal()
        post_order = self.postorder_traversal()
        pre_order = self.preorder_traversal()
        breadth_first = self.breadth_first_traversal()

        plt.text(0.5, 0.9, 'Em-ordem: ' + str(in_order), ha='center', va='center', fontsize=10, bbox=dict(alpha=0.5), transform=plt.gca().transAxes)
        plt.text(0.5, 0.8, 'Pós-ordem: ' + str(post_order), ha='center', va='center', fontsize=10, bbox=dict(alpha=0.5), transform=plt.gca().transAxes)
        plt.text(0.5, 0.7, 'Pré-ordem: ' + str(pre_order), ha='center', va='center', fontsize=10, bbox=dict( alpha=0.5), transform=plt.gca().transAxes)
        plt.text(0.5, 0.6, 'Largura: ' + str(breadth_first), ha='center', va='center', fontsize=10, bbox=dict( alpha=0.5), transform=plt.gca().transAxes)
        plt.title('Resultados dos Percursos')
        
        # Remover os eixos
        
        plt.axis('off')  # Oculta os eixos x e y

        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()  # Fecha a figura após salvar
        return buf

    def count_nodes(self, root):
        """Contabiliza o número de nós na árvore."""
        if root is None:
            return 0
        return 1 + self.count_nodes(root.left) + self.count_nodes(root.right)

    def _build_tree_graph(self, graph, root):
        if root:
            graph.add_node(root)
            if root.left:
                graph.add_edge(root, root.left)
                self._build_tree_graph(graph, root.left)
            if root.right:
                graph.add_edge(root, root.right)
                self._build_tree_graph(graph, root.right)

    def _generate_positions(self, graph):
        pos = {}
        queue = [(self.root, 0, 0)]

        while queue:
            node, depth, offset = queue.pop(0)
            if node not in pos:
                pos[node] = (offset, -depth)

            if node.left:
                queue.append((node.left, depth + 1, offset - 1))
            if node.right:
                queue.append((node.right, depth + 1, offset + 1))

        return pos


# streamlit interface

st.set_page_config(
    page_title="Árvore de Busca Binária",
    page_icon="2",
    initial_sidebar_state='expanded',
    
)

st.title("Árvore de Busca Binária")

input_sequence = st.text_input("Digite a sequência de números separados por espaço:")
submit = st.button("Inserir na Árvore")

if submit:
    elements = list(map(int, input_sequence.split()))
    arvore = BinarySearchTree()
    
    for element in elements:
        arvore.insert(element)

    st.write("Árvore gerada:")
    buf = arvore.plot_tree()
    st.image(buf)


##1