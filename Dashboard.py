import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os
import io
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
import ast
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

# Set the working directory
os.chdir('C:/Users/visha/OneDrive/Documents/GitHub/CoAuthorViz_Dashboard')

notebook1 = execute_notebook("cluster_analysis.ipynb")
notebook2 = execute_notebook("cluster_analysis_new.ipynb")

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
    st.title("Welcome to the Writers Clustering Dashboard for an Educator")
    st.write("Here, you'll find insights drawn from our data, as well as interactive visualizations to explore. "
             "If you have any questions or feedback, please visit the FAQ and Feedback sections at the last page.")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Educator View", "Advanced View", "Feedback and FAQ"])

    if page == "Overview":
        st.write("This dashboard provides insights into the two types of clustering of writers based on their interactions with GPT-3. "
                 "The first clustering(basic) is based on sentence level and API metrics and the second clustering is based on sequence of the user "
                 "behaviour(advance).")
        
        st.write("The dashboard is divided into two parts:")
        st.write("1. Educator View: Basic Visualizations and Details. (Mainly contains about the first clustering)")
        st.write("2. Advanced View: Technical Visualizations and Details. (Mainly contains about the second clustering)")

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

        st.subheader("Total number of sequential clusters('-1' is noise)")
        text7_data = get_output_by_tag(notebook2, 'len_clusters_dict')
        if text7_data is not None:
            if isinstance(text7_data, dict) and 'text/plain' in text7_data:
                # Extracts the 'text/plain' content if the output is a dictionary
                st.write(text7_data['text/plain'])
            else:
                st.write(text7_data)
        else:
            st.write("No output found for the cell with tag 'len_clusters_dict'.")

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
        
        st.write("Balanced Collaborators lean more towards argumentative writing, "
                 "GPT-3 Reliant Writers use it for both argumentative and creative writing, "
                 "and Independent Creators have a strong inclination towards creative writing with minimal GPT-3 usage.")

    elif page == "Educator View":
        st.header("Educator View: Basic Visualizations and Details")
        st.write("In this section, we provide a simplified overview of the data, "
                 "aimed at providing educators with key insights without overwhelming them with technical details.")
        
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
        
        # Display the charts in columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Clusters Visualization 2D")
            visualization3_data = get_output_by_tag(notebook1, 'cluster_2d')
            if visualization3_data is not None:
                visualization3_data_png = visualization3_data['image/png']
                visualization3_decoded_png = base64.b64decode(visualization3_data_png)
                st.image(visualization3_decoded_png, caption='Clusters Visualization 2D', use_column_width=True)
            else:
                st.write("No output found for the cell with tag 'cluster_2d'.")

        with col2:
            st.subheader("Clusters Visualization 3D")
            visualization4_data = get_output_by_tag(notebook1, 'cluster_3d')
            if visualization4_data is not None:
                visualization4_data_png = visualization4_data['image/png']
                visualization4_decoded_png = base64.b64decode(visualization4_data_png)
                st.image(visualization4_decoded_png, caption='Clusters Visualization 2D', use_column_width=True)
            else:
                st.write("No output found for the cell with tag 'cluster_2d'.")

        st.write("It's just an overview of clusters in 2D/3D to show approximate sizes and distribution of the 3 clusters.")
        
        st.subheader("Radar Chart")
        visualization5_data = get_output_by_tag(notebook1, 'radar_chart')
        if visualization5_data is not None:
            visualization5_data_png = visualization5_data['image/png']
            visualization5_decoded_png = base64.b64decode(visualization5_data_png)
            st.image(visualization5_decoded_png, caption='Radar Chart', use_column_width=True)
        else:
            st.write("No output found for the cell with tag 'Radar Chart'.")

        st.write("It just compares the metrics between the 3 clusters. For example, GPT-3 Reliant writers modify GPT-3 suggestions "
                 "more that the Balanced Collaborators.")

        st.subheader("Recommendations for Educators")

        st.subheader("Independent Creators")
        st.write("Students in this group mainly generate their content independently. After assessing their writing quality, "
                "if you feel their work could benefit from the additional support of AI, you can introduce the potential benefits of using GPT-3. "
                "It could be used as a brainstorming tool, or to aid in revising and editing their work. However, this should be done after "
                "you have a clear understanding of their writing quality and capabilities.")

        st.subheader("GPT-3 Reliant Writers")
        st.write("For students in this group, the goal should be to help them become more confident and independent in their writing. "
                "These students rely heavily on GPT-3, so it's important to encourage their development in terms of their own writing skills. "
                "While they can continue to use GPT-3 for inspiration and editing, the focus should be on reducing their reliance on the AI for the majority of their work.")

        st.subheader("Balanced Collaborators")
        st.write("Students in this group are using GPT-3 in a balanced manner, combining their own writing with AI suggestions. "
                "Ensure you continue encouraging this balanced approach. Depending on their writing quality, they might benefit from exercises that "
                "allow them to experiment with both independent writing and AI-supported writing. For example, you could suggest they first write a draft independently, "
                "then use GPT-3 to help revise and improve their work.")

        st.subheader("Overall Suggestions")
        st.write("To help all students make the most of AI tools like GPT-3, it's important to provide clear guidance on when and how to use these tools. "
                "It's also helpful to discuss the limitations of AI and the importance of human input in the writing process. "
                "Always remember, the goal is not to depend on the AI, but to use it as a tool to enhance learning and creativity.")

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
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Pie Chart for writing type distribution ('Balanced Collaborators' and 'GPT-3 Reliant Writers')")
            visualization8_data = get_output_by_tag(notebook1, 'writing_type_pie')
            if visualization8_data is not None:
                visualization8_data_png = visualization8_data['image/png']
                visualization8_decoded_png = base64.b64decode(visualization8_data_png)
                st.image(visualization8_decoded_png, caption='Pie Chart for writing type distribution (Count:Number of Writings)', use_column_width=True)
            else:
                st.write("No output found for the cell with tag 'writing_type_pie'.")

        with col4:
            st.subheader("Pie Chart for writing type distribution ('Balanced Collaborators' and 'Independent Creators')")
            visualization9_data = get_output_by_tag(notebook1, 'writing_type_pie1')
            if visualization9_data is not None:
                visualization9_data_png = visualization9_data['image/png']
                visualization9_decoded_png = base64.b64decode(visualization9_data_png)
                st.image(visualization9_decoded_png, caption='Pie Chart for writing type distribution (Count:Number of Writings)', use_column_width=True)
            else:
                st.write("No output found for the cell with tag 'writing_type_pie1'.")

        st.write("Now, after looking at the 'Creative' and 'Argumentative' writings distribution, "
                 "we can know that sometimes writers tends to belong to a particular cluster for a particular writing type.")

        st.subheader("Bar Plot for showing cluster switching behaviour per writing type")
        visualization10_data = get_output_by_tag(notebook1, 'worker_cluster_viz1')

        if visualization10_data is not None:
            plot_data = visualization10_data['application/vnd.plotly.v1+json']
            fig = go.Figure()
            # Add all traces to the figure
            for trace in plot_data['data']:
                fig.add_trace(go.Bar(trace))
            # Set layout properties
            fig.update_layout(plot_data['layout'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No output found for the cell with tag 'worker_cluster_viz1'.")

        text6_data = get_output_by_tag(notebook1, 'writer_type_details1')
        if text6_data is not None:
            if isinstance(text6_data, dict) and 'text/plain' in text6_data:
                # Extracts the 'text/plain' content if the output is a dictionary
                st.write(text6_data['text/plain'])
            else:
                st.write(text6_data)
        else:
            st.write("No output found for the cell with tag 'writer_type_details1'.")

    elif page == "Advanced View":
        st.header("Advanced View: Technical Visualizations and Details")
        st.write("In this section, we delve into more complex analysis of the data. "
                 "Here you'll find advanced visualizations such as Scatter and UMAP plots, as well as in-depth details about each sequential cluster.")

        st.write("""**Note: the scatter plot is on first clustering only, i.e., clustering based on metrics. "
                 "After the scatter plot, everything is regarding sequential clustering.**""")

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
        else:
            st.write("No output found for the cell with tag 'worker_cluster_viz'.")

        text7_data = get_output_by_tag(notebook1, 'writer_type_details2')
        if text7_data is not None:
            if isinstance(text7_data, dict) and 'text/plain' in text7_data:
                # Extracts the 'text/plain' content if the output is a dictionary
                st.write(text7_data['text/plain'])
            else:
                st.write(text7_data)
        else:
            st.write("No output found for the cell with tag 'writer_type_details2'.")

        st.subheader("UMAP Ensembled Visualization")
        visualization13_data = get_output_by_tag(notebook2, 'UMAP_ensembled')

        if visualization13_data is not None:
            visualization13_data_png = visualization13_data['image/png']
            visualization13_decoded_png = base64.b64decode(visualization13_data_png)
            st.image(visualization13_decoded_png, caption='UMAP_ensembled Plot', use_column_width=True)
        else:
            st.write("No output found for the cell with tag 'UMAP_ensembled'.")

        st.write("Here, I combined the clustering results from DBSCAN(Density-Based clustering) "
                 "& K-Means Clustering and applied a majority vote function to get the final clusters. "
                 "It's just an overview of clusters to show approximate sizes and distribution.")

        st.subheader("Details about each cluster")
        st.write("Select a cluster from the dropdown menu to view its details. "
             "These details include the most common DiGraph, Process Model, and a translation of the model. "
             "This information can help you understand the common patterns within each cluster. ")
        st.write("NOTE: The drop-down menu is arranged in a decreasing order of cluster size, you can "
             "view the largest/smallest cluster by selecting the top and the bottom.")
        text6_data = get_output_by_tag(notebook2, 'clusters_dict')

        if text6_data is not None:
            if isinstance(text6_data, dict) and 'text/plain' in text6_data:
                # Convert the 'text/plain' content from a string to a dictionary
                clusters = ast.literal_eval(text6_data['text/plain'])
        
                # Sort the clusters dictionary by count in descending order
                clusters = dict(sorted(clusters.items(), key=lambda item: item[1]['count'], reverse=True))
        
                # Display the clusters in a dropdown menu
                cluster_to_display = st.selectbox('Select a cluster', list(clusters.keys()))
                st.write(f"Cluster {cluster_to_display}:")
                st.write("Count:")
                st.write(clusters[cluster_to_display]['count'])
                st.write("Most common DiGraph:")
                st.write(clusters[cluster_to_display]['most_common_digraph'])
                st.write("Most common Process Model:")
                st.write(clusters[cluster_to_display]['most_common_process_model'])
                st.write("Translation:")
                st.write(clusters[cluster_to_display]['translation'])
            else:
                st.write(text6_data)
        else:
            st.write("No output found for the cell with tag 'cluster_details'.")

        st.subheader("Terms and symbols used in the process models:")

        st.markdown("""
        - 'prompt': Initial Idea or prompt.
        - 'user': User's own input without the help of GPT-3.
        - 'gpt3-call': Using the GPT-3 suggestion as it is.
        - 'modify-gpt3': Modifying GPT-3 suggestion and using it.
        - 'empty-call': Calling GPT-3 suggestion but cancelling it.""", unsafe_allow_html=True)

        st.markdown("""
        - `-> : Represents the sequence or order of actions.`
        - `X : Groups actions together and represents a choice between them.`
        - `tau : Symbolizes a silent action, which doesn't directly impact but maintains the flow of the process.`
        - `+ : Used for a non-deterministic choice between actions, i.e., any of the actions can be chosen without any predefined order.`
        - `* : Denotes a loop, indicating that the enclosed actions can be repeated multiple times in sequence.`""", unsafe_allow_html=True)
        
        st.subheader("Examples of Practical Application")
        st.write("The results of this clustering can be used in many ways in an educational setting. For example, "
             "if the clustering reveals groups of students with similar learning behaviors, you might consider "
             "tailoring your teaching strategies to better suit each group. Alternatively, you could use this "
             "information to identify students who may need additional support or resources.")
        
        st.header("Extra Clusterings")
        # Display the charts in columns
        col5, col6 = st.columns(2)

        with col5:
            st.subheader("Hierarchical Clustering Dendrogram")
            visualization14_data = get_output_by_tag(notebook2, 'HCdendogram')

            if visualization14_data is not None:
                visualization14_data_png = visualization14_data['image/png']
                visualization14_decoded_png = base64.b64decode(visualization14_data_png)
                st.image(visualization14_decoded_png, caption='Hierarchical Clustering Dendrogram', use_column_width=True)
            else:
                st.write("No output found for the cell with tag 'HCdendogram'.")

        with col6:
            st.subheader("Hierarchical Clustering of Petri Nets")
            visualization15_data = get_output_by_tag(notebook2, 'Petridendogram')

            if visualization15_data is not None:
                visualization15_data_png = visualization15_data['image/png']
                visualization15_decoded_png = base64.b64decode(visualization15_data_png)
                st.image(visualization15_decoded_png, caption='Petri Nets Dendrogram', use_column_width=True)
            else:
                st.write("No output found for the cell with tag 'Petridendogram'.")
        
    elif page == "Feedback and FAQ":
        st.header("Feedback")
    
        # Create a feedback form
        name = st.text_input("Name")
        feedback = st.text_area("What did you think of the dashboard? Do you have any suggestions for improvements?")
        if st.button("Submit"):
            st.write("Thank you for your feedback!")

        st.subheader("Additional Resources(FAQ)")
        st.write("For a more detailed report on our methods and findings, please contact us at [email address]. "
             "We can provide you with full reports, additional resources, and more in-depth explanations of our work.")

if __name__ == "__main__":
    main()