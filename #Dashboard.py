#Dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
from sklearn.manifold import TSNE

# Read the dataframe
# Replace this with the actual dataframe you have
df = pd.read_csv('your_dataframe.csv')

# Perform clustering
# Replace this with the actual clustering code you have
clustering = AgglomerativeClustering(n_clusters=None, affinity='precomputed', linkage='average', distance_threshold=0.5)
labels = clustering.fit_predict(distance_matrix)

# Perform t-SNE for dimensionality reduction
embedding = TSNE(n_components=2, metric='precomputed').fit_transform(distance_matrix)

# Define a function to plot the dendrogram
def plot_dendrogram(model, labels):
    linkage_matrix = model.children_
    dendrogram(linkage_matrix, labels=labels, leaf_rotation=90, leaf_font_size=8)
    plt.xlabel('File Names')
    plt.ylabel('Distance')

# Start the Streamlit app
st.title('Writing Process Clustering Dashboard')

# Display the total number of clusters and students
num_clusters = len(np.unique(labels))
num_students = len(df)
st.write(f'Total number of clusters: {num_clusters}')
st.write(f'Total number of students: {num_students}')

# Create a scatter plot of the t-SNE results
scatterplot = plt.figure()
sns.scatterplot(x=embedding[:, 0], y=embedding[:, 1], hue=labels, palette='viridis', legend=None)
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.title('Clusters in 2D t-SNE Space')
st.pyplot(scatterplot)

# Plot the dendrogram
if st.checkbox('Show dendrogram'):
    plt.figure(figsize=(15, 10))
    plot_dendrogram(clustering, df['file_name'].values)
    st.pyplot(plt)

# Display individual student information
selected_student = st.selectbox('Select a student:', df['file_name'].values)
student_info = df[df['file_name'] == selected_student].iloc[0]
st.write('Student information:')
st.write(student_info)

# Display the writing process model
st.write('Writing Process Model:')
st.write(student_info['process_model'])

# Display the cluster membership
student_cluster = labels[df['file_name'].values == selected_student][0]
st.write(f'Cluster membership: Cluster {student_cluster + 1}')
