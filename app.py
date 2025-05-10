import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from io import StringIO
from tqdm import tqdm
import tempfile

st.set_page_config(layout="wide")
st.title("📈Publication Trend Analyzer (DBLP)")



uploaded_file = st.file_uploader("Upload the extracted dblp.xml file", type="xml")

keywords_default = [
    'artificial intelligence', 'machine learning', 'deep learning',
    'neural network', 'support vector machine', 'svm',
    'unsupervised', 'k-means', 'clustering', 'classification'
]
keywords_input = st.text_area("Enter keywords (comma-separated)", ", ".join(keywords_default))
keywords = [kw.strip().lower() for kw in keywords_input.split(',') if kw.strip()]

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.success("File uploaded and stored temporarily. Starting analysis...")
    
    yearly_counts = defaultdict(int)
    context = ET.iterparse(tmp_path, events=('start', 'end'))
    _, root = next(context)

    progress_bar = st.progress(0)
    count = 0
    for event, elem in context:
        if event == 'end' and elem.tag in {'article', 'inproceedings'}:
            title = elem.findtext('title')
            year = elem.findtext('year')

            if title and year:
                title_lower = title.lower()
                if any(kw in title_lower for kw in keywords):
                    yearly_counts[year] += 1

            count += 1
            if count % 10000 == 0:
                progress_bar.progress(min(count / 4000000, 1.0)) 

            elem.clear()
            root.clear()

  
    df = pd.DataFrame(sorted(yearly_counts.items()), columns=['Year', 'Count'])
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna().astype({'Year': int})
    df = df[df['Year'] >= 1990]  

    st.subheader("📊 Results")
    st.dataframe(df, use_container_width=True)

    st.subheader("📉 Trend Over Time")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['Year'], df['Count'], marker='o', color='green')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_title('AI/ML Publications per Year (Filtered by Keywords)')
    ax.grid(True)
    st.pyplot(fig)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "ai_ml_publication_trends.csv", "text/csv")
