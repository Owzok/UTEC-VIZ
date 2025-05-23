import pandas as pd
import numpy as np
import json
from collections import defaultdict
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

# Vao a usar nx para hacer las métricas más chéveres.

def process_faculty_data(csv_file_path):
    df = pd.read_csv(csv_file_path)
    
    df['Name'] = df['Name'].str.strip()
    df['Department'] = df['Department'].fillna('Unknown Department')
    df['ResearchAreas'] = df['ResearchAreas'].fillna('')
    df['H-index'] = pd.to_numeric(df['H-index'], errors='coerce').fillna(0)
    df['Citas'] = pd.to_numeric(df['Citas'], errors='coerce').fillna(0)
    
    nodes = []
    for idx, row in df.iterrows():
        nodes.append({
            'id': idx,
            'name': row['Name'],
            'department': row['Department'],
            'email': row['Email'] if pd.notna(row['Email']) else '',
            'research_areas': row['ResearchAreas'],
            'h_index': int(row['H-index']) if pd.notna(row['H-index']) else 0,
            'citations': int(row['Citas']) if pd.notna(row['Citas']) else 0,
            'image_url': row['Image URL'] if pd.notna(row['Image URL']) else '',
            'research_groups': row['Research'] if pd.notna(row['Research']) else ''
        })
    
    edges = []
    edge_weights = defaultdict(float)
    
    for i in range(len(df)):
        for j in range(i+1, len(df)):
            weight = 0
            edge_type = []
            
            if df.iloc[i]['Department'] == df.iloc[j]['Department']:
                weight += 0.3
                edge_type.append('department')
            
            research_i = str(df.iloc[i]['Research']) if pd.notna(df.iloc[i]['Research']) else ''
            research_j = str(df.iloc[j]['Research']) if pd.notna(df.iloc[j]['Research']) else ''
            
            if research_i and research_j:
                groups_i = set(re.findall(r'Grupo[^;]*', research_i))
                groups_j = set(re.findall(r'Grupo[^;]*', research_j))
                common_groups = groups_i.intersection(groups_j)
                if common_groups:
                    weight += 0.5 * len(common_groups)
                    edge_type.append('research_group')
            
            areas_i = str(df.iloc[i]['ResearchAreas']) if pd.notna(df.iloc[i]['ResearchAreas']) else ''
            areas_j = str(df.iloc[j]['ResearchAreas']) if pd.notna(df.iloc[j]['ResearchAreas']) else ''
            
            if areas_i and areas_j:
                try:
                    vectorizer = TfidfVectorizer(stop_words='spanish', ngram_range=(1, 2))
                    tfidf_matrix = vectorizer.fit_transform([areas_i, areas_j])
                    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                    if similarity > 0.2:
                        weight += similarity * 0.4
                        edge_type.append('research_similarity')
                except:
                    pass
            
            h_i = df.iloc[i]['H-index'] if pd.notna(df.iloc[i]['H-index']) else 0
            h_j = df.iloc[j]['H-index'] if pd.notna(df.iloc[j]['H-index']) else 0
            
            if h_i > 0 and h_j > 0:
                h_similarity = 1 - abs(h_i - h_j) / max(h_i, h_j)
                if h_similarity > 0.7:
                    weight += 0.2
                    edge_type.append('citation_similarity')
            
            if weight > 0.2:
                edges.append({
                    'source': i,
                    'target': j,
                    'weight': round(weight, 3),
                    'type': ';'.join(edge_type)
                })
    
    return nodes, edges

def calculate_network_metrics(nodes, edges):
    G = nx.Graph()
    
    for node in nodes:
        G.add_node(node['id'], **node)
    
    for edge in edges:
        G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    
    metrics = {}
    
    degree_centrality = nx.degree_centrality(G)
    
    betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
    
    closeness_centrality = nx.closeness_centrality(G, distance='weight')
    
    pagerank = nx.pagerank(G, weight='weight')
    
    clustering = nx.clustering(G, weight='weight')
    
    for node in nodes:
        node_id = node['id']
        node['degree_centrality'] = round(degree_centrality.get(node_id, 0), 3)
        node['betweenness_centrality'] = round(betweenness_centrality.get(node_id, 0), 3)
        node['closeness_centrality'] = round(closeness_centrality.get(node_id, 0), 3)
        node['pagerank'] = round(pagerank.get(node_id, 0), 3)
        node['clustering'] = round(clustering.get(node_id, 0), 3)
        node['degree'] = G.degree(node_id)
    
    return nodes, G

def export_for_d3(nodes, edges, output_file='faculty_network.json'):

    departments = list(set([node['department'] for node in nodes]))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    dept_colors = {dept: colors[i % len(colors)] for i, dept in enumerate(departments)}
    
    for node in nodes:
        node['color'] = dept_colors[node['department']]
        node['size'] = max(5, min(25, node['degree'] * 3 + node['h_index']))
    
    network_data = {
        'nodes': nodes,
        'edges': edges,
        'departments': departments,
        'department_colors': dept_colors,
        'stats': {
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'departments_count': len(departments)
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(network_data, f, ensure_ascii=False, indent=2)
    
    return network_data

if __name__ == "__main__":
    print("Processing faculty data...")
    nodes, edges = process_faculty_data('p1_persons_data.csv')
    
    print(f"Created {len(nodes)} nodes and {len(edges)} edges")
    
    print("Calculating network metrics...")
    nodes_with_metrics, graph = calculate_network_metrics(nodes, edges)
    
    print("Exporting data for D3 visualization...")
    network_data = export_for_d3(nodes_with_metrics, edges)
    
    print("Data processing complete!")
    print(f"Output saved to: faculty_network.json")
    
    print("\n=== NETWORK INSIGHTS ===")
    top_collaborators = sorted(nodes_with_metrics, key=lambda x: x['degree'], reverse=True)[:5]
    print("\nTop 5 Collaborators (Highest Degree):")
    for i, node in enumerate(top_collaborators, 1):
        print(f"{i}. {node['name']} - Degree: {node['degree']}, Department: {node['department']}")
    
    top_bridges = sorted(nodes_with_metrics, key=lambda x: x['betweenness_centrality'], reverse=True)[:5]
    print("\nTop 5 Bridges Between Departments (Highest Betweenness):")
    for i, node in enumerate(top_bridges, 1):
        print(f"{i}. {node['name']} - Betweenness: {node['betweenness_centrality']}, Department: {node['department']}")
    
    top_influential = sorted(nodes_with_metrics, key=lambda x: x['pagerank'], reverse=True)[:5]
    print("\nTop 5 Most Influential (Highest PageRank):")
    for i, node in enumerate(top_influential, 1):
        print(f"{i}. {node['name']} - PageRank: {node['pagerank']}, H-index: {node['h_index']}")
    
    dept_count = {}
    for node in nodes_with_metrics:
        dept = node['department']
        dept_count[dept] = dept_count.get(dept, 0) + 1
    
    print("\nDepartment Distribution:")
    for dept, count in sorted(dept_count.items(), key=lambda x: x[1], reverse=True):
        print(f"- {dept}: {count} faculty members")