import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os
import io
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
from IPython.display import Image
import base64

@st.cache_data
def execute_notebook(notebook_path):
    with io.open(notebook_path, mode="r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    
    ep = ExecutePreprocessor(timeout=None, kernel_name="python3")

    try:
        ep.preprocess(nb, {"metadata": {"path": ""}})
    except CellExecutionError as e:
        msg = f"Error executing the notebook: {notebook_path}\n\n"
        msg += str(e)
        raise RuntimeError(msg)

    return nb

notebook1 = execute_notebook("C:/Users/visha/OneDrive/Documents/GitHub/CoAuthorViz_Dashboard/cluster_analysis.ipynb")

def get_output_by_tag(notebook, tag):
    for cell in notebook['cells']:
        if 'tags' in cell['metadata'] and tag in cell['metadata']['tags']:
            if cell['cell_type'] == 'markdown':
                # Return the source of markdown cell as output
                return ''.join(cell['source'])
            elif cell['cell_type'] == 'code' and cell['outputs']:
                # Check for 'text' or 'data' in the output of the code cell
                output = cell['outputs'][0]
                if 'text' in output:
                    return ''.join(output['text'])
                elif 'data' in output:
                    return output['data']
    return None

def main():
    st.title("Writers Clustering Dashboard")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Sentence and API level Clustering", "Sequential Clustering"])

    if page == "Overview":
        st.write("This dashboard provides insights into the clustering of writers based on their interactions with GPT-3.")
        
        st.write("The clustering is divided into two parts/notebooks:")
        st.write("1. Sentence and API level Clustering: Clustering based on sentence-level and API metrics.")
        st.write("2. Sequential Clustering: Clustering based on sequential data and process mining.")

        st.header("Overview")
        # Display the total numbers
        st.subheader("Total number of writing sessions")
        text1_data = get_output_by_tag(notebook1, 'len_data')
        if text1_data is not None:
            if isinstance(text1_data, dict) and 'text/plain' in text1_data:
                # Extracts the 'text/plain' content if the output is a dictionary
                st.write(text1_data['text/plain'])
            else:
                st.write(text1_data)
        else:
            st.write("No output found for the cell with tag 'len_data'.")


        st.subheader("Total number of writers")
        text2_data = get_output_by_tag(notebook1, 'unique_writers')
        if text2_data is not None:
            if isinstance(text2_data, dict) and 'text/plain' in text2_data:
                # Extracts the 'text/plain' content if the output is a dictionary
                st.write(text2_data['text/plain'])
            else:
                st.write(text2_data)
        else:
            st.write("No output found for the cell with tag 'unique_writers'.")

        st.subheader("Total number of argumentative writings")
        text3_data = get_output_by_tag(notebook1, 'argumentative')
        if text3_data is not None:
            if isinstance(text3_data, dict) and 'text/plain' in text3_data:
                # Extracts the 'text/plain' content if the output is a dictionary
                st.write(text3_data['text/plain'])
            else:
                st.write(text3_data)
        else:
            st.write("No output found for the cell with tag 'argumentative'.")

        st.subheader("Total number of creative writings")
        text4_data = get_output_by_tag(notebook1, 'creative')
        if text4_data is not None:
            if isinstance(text4_data, dict) and 'text/plain' in text4_data:
                # Extracts the 'text/plain' content if the output is a dictionary
                st.write(text4_data['text/plain'])
            else:
                st.write(text4_data)
        else:
            st.write("No output found for the cell with tag 'creative'.")

        st.subheader("Total number of 'sequential clusters'")
        st.write('total_sequential_clusters')

        st.subheader("Distribution of writers across the three clusters")
        visualization1_data = get_output_by_tag(notebook1, 'cluster_dist')
        if visualization1_data is not None:
            visualization1_data_png = visualization1_data['image/png']
            visualization1_decoded_png = base64.b64decode(visualization1_data_png)
            st.image(visualization1_decoded_png, caption='Clusters Visualization', use_column_width=True)

        st.write("Cluster 0 (Balanced Collaborators): 603")
        st.write("Cluster 1 (GPT-3 Reliant Writers): 270")
        st.write("Cluster 2 (Independent Creators): 573")

        st.subheader("Writing Type Distribution Across Clusters")
        visualization2_data = get_output_by_tag(notebook1, 'writing_type_dist')

        if visualization2_data is not None:
            plot_data = visualization2_data['application/vnd.plotly.v1+json']
            fig = go.Figure()
            # Add all traces to the figure
            for trace in plot_data['data']:
                fig.add_trace(go.Bar(trace))
            # Set layout properties
            fig.update_layout(plot_data['layout'])
            st.plotly_chart(fig, use_container_width=True)
        
        st.write("Balanced Collaborators lean more towards argumentative writing, GPT-3 Reliant Writers use it for both argumentative and creative writing, and Independent Creators have a strong inclination towards creative writing with minimal GPT-3 usage.")

    elif page == "Sentence and API level Clustering":
        st.header("Sentence and API level Clustering: Clustering based on sentence-level and API metrics")
        st.subheader("Details about each cluster")
        text5_data = get_output_by_tag(notebook1, 'cluster_details')
        if text5_data is not None:
            if isinstance(text5_data, dict) and 'text/plain' in text5_data:
                # Extracts the 'text/plain' content if the output is a dictionary
                st.write(text5_data['text/plain'])
            else:
                st.write(text5_data)
        else:
            st.write("No output found for the cell with tag 'cluster_details'.")
        
        # Insert visualizations from the first notebook
        st.subheader("Clusters Visualization 2D")
        visualization3_data = get_output_by_tag(notebook1, 'cluster_2d')
        if visualization3_data is not None:
            visualization3_data_png = visualization3_data['image/png']
            visualization3_decoded_png = base64.b64decode(visualization3_data_png)
            st.image(visualization3_decoded_png, caption='Clusters Visualization 2D', use_column_width=True)
        else:
            st.write("No output found for the cell with tag 'cluster_2d'.")

        st.subheader("Clusters Visualization 3D")
        visualization4_data = get_output_by_tag(notebook1, 'cluster_3d')
        if visualization4_data is not None:
            visualization4_data_png = visualization4_data['image/png']
            visualization4_decoded_png = base64.b64decode(visualization4_data_png)
            st.image(visualization4_decoded_png, caption='Clusters Visualization 2D', use_column_width=True)
        else:
            st.write("No output found for the cell with tag 'cluster_2d'.")

        st.subheader("Radar Chart")
        visualization5_data = get_output_by_tag(notebook1, 'radar_chart')
        if visualization5_data is not None:
            visualization5_data_png = visualization5_data['image/png']
            visualization5_decoded_png = base64.b64decode(visualization5_data_png)
            st.image(visualization5_decoded_png, caption='Radar Chart', use_column_width=True)
        else:
            st.write("No output found for the cell with tag 'Radar Chart'.")

        st.subheader("Cluster Comparison Parallel Coordinates Plot")
        visualization6_data = get_output_by_tag(notebook1, 'line_chart')

        if visualization6_data is not None:
            plot_data = visualization6_data['application/vnd.plotly.v1+json']
            fig = go.Figure()
            # Add all traces to the figure
            for trace in plot_data['data']:
                fig.add_trace(go.Parcoords(trace))
            # Set layout properties
            fig.update_layout(plot_data['layout'])
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Bar Chart for Argumentative and Creative Writings per Cluster/Cluster Groups")
        visualization7_data = get_output_by_tag(notebook1, 'writers_per_cluster')

        if visualization7_data is not None:
            plot_data = visualization7_data['application/vnd.plotly.v1+json']
            fig = go.Figure()
            # Add all traces to the figure
            for trace in plot_data['data']:
                fig.add_trace(go.Bar(trace))
            # Set layout properties
            fig.update_layout(plot_data['layout'])
            st.plotly_chart(fig, use_container_width=True)

        # Display the charts in columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Pie Chart for writing type distribution ('Balanced Collaborators' and 'GPT-3 Reliant Writers')")
            visualization8_data = get_output_by_tag(notebook1, 'writing_type_pie')
            if visualization8_data is not None:
                visualization8_data_png = visualization8_data['image/png']
                visualization8_decoded_png = base64.b64decode(visualization8_data_png)
                st.image(visualization8_decoded_png, caption='Pie Chart for writing type distribution', use_column_width=True)
            else:
                st.write("No output found for the cell with tag 'writing_type_pie'.")

        with col2:
            st.subheader("Pie Chart for writing type distribution ('Balanced Collaborators' and 'Independent Creators')")
            visualization9_data = get_output_by_tag(notebook1, 'writing_type_pie1')
            if visualization9_data is not None:
                visualization9_data_png = visualization9_data['image/png']
                visualization9_decoded_png = base64.b64decode(visualization9_data_png)
                st.image(visualization9_decoded_png, caption='Pie Chart for writing type distribution', use_column_width=True)
            else:
                st.write("No output found for the cell with tag 'writing_type_pie1'.")

        st.subheader("Scatter Plot for Worker Clusters by Writing Type and Prompt Code")
        visualization10_data = get_output_by_tag(notebook1, 'worker_cluster_viz')

        if visualization10_data is not None:
            plot_data = visualization10_data['application/vnd.plotly.v1+json']
            fig = go.Figure()
            # Add all traces to the figure
            for trace in plot_data['data']:
                fig.add_trace(go.Scatter(trace))
            # Set layout properties
            fig.update_layout(plot_data['layout'])
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Sequential Clustering":
        st.header("Sequential Clustering: Clustering based on key-stroke level data and process mining")

        # Insert visualizations from the second notebook
        st.subheader("t-SNE Visualization")
        # fig = px.scatter(tsne_data, x="x_axis", y="y_axis", color="Cluster")
        # st.plotly_chart(fig)

        st.subheader("UMAP Visualization")
        # fig = px.scatter(umap_data, x="x_axis", y="y_axis", color="Cluster")
        # st.plotly_chart(fig)

        st.subheader("Dendrogram")
        # fig = px.dendrogram(dendrogram_data, labels=your_labels)
        # st.plotly_chart(fig)

        st.subheader("Petri Net Visualization")
        # Display the Petri net, or display an image of the Petri net using st.image()

if __name__ == "__main__":
    main()