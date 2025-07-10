import streamlit as st
from google_play_scraper import reviews_all
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import torch
import pandas as pd
import re

# Streamlit Başlığı
st.title("🎮 Google Play Yorum Analizi ve Fake Review Tespiti")

# Kullanıcıdan Package Name Al
package_name = st.text_input("Google Play Package Name", value="com.flatgames.patrolofficer")

if st.button("Yorumları Çek ve Analiz Et"):

    with st.spinner("Yorumlar çekiliyor ve analiz ediliyor..."):

        reviews = reviews_all(
            package_name,
            lang='tr',
            country='tr',
            sleep_milliseconds=0
        )

        tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-uncased")
        model = AutoModel.from_pretrained("dbmdz/bert-base-turkish-uncased")

        fake_examples = [
            "Bu oyun harika, kesinlikle mükemmel!",
            "Çok kötü, berbat, iğrenç bir oyun.",
            "İdare eder, ortalama bir oyun"
        ]

        def has_repeated_phrases(text, threshold=3):
            text_clean = re.sub(r'[^\w\s]', '', text.lower())
            words = text_clean.split()
            word_counts = Counter(words)
            most_common = word_counts.most_common(1)
            return most_common and most_common[0][1] >= threshold

        def get_embedding(text):
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                outputs = model(**inputs)
            return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

        fake_embeddings = [get_embedding(text) for text in fake_examples]

        results_list = []

        for review in reviews:
            content = review['content']
            review_embedding = get_embedding(content)
            similarities = [cosine_similarity([review_embedding], [fake_emb])[0][0] for fake_emb in fake_embeddings]
            max_similarity = max(similarities)
            repetitive = has_repeated_phrases(content)

            is_fake = 'Fake' if max_similarity > 0.85 or repetitive else 'Genuine'

            results_list.append({
                'review': content,
                'fake_label': is_fake,
                'max_similarity': round(max_similarity, 4),
                'repetitive': repetitive
            })

        df = pd.DataFrame(results_list)
        st.success("✅ Analiz tamamlandı!")

        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Sonuçları İndir (CSV)", data=csv, file_name="reviews_analysis.csv", mime="text/csv")
