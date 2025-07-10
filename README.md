# 🎮 Google Play Review Analyzer

Bu proje, Google Play Store'daki bir mobil oyunun yorumlarını otomatik olarak çekip analiz eden bir **Yapay Zeka Destekli İnceleme Analiz Sistemidir**.

## 🚀 Özellikler

- 🔍 Google Play yorumlarını tam kapsamlı çekme
- 🤖 **BERT (Türkçe)** ile duygu analizi
- 🛡️ **Fake review detection** (embedding similarity + tekrarlayan kelime analizi)
- 📊 Analiz sonuçlarını tablo olarak gösterme ve CSV olarak indirme
- 🖥️ Streamlit arayüzü ile kolay kullanım

## 🛠️ Kullanılan Teknolojiler

- Python 3.x
- `google-play-scraper`
- `transformers` (Hugging Face)
- `scikit-learn`
- `pandas`
- `Streamlit`

## ⚙️ Kurulum

```bash
# Gerekli kütüphaneleri yükle
pip install streamlit google-play-scraper transformers scikit-learn pandas

# Uygulamayı çalıştır
streamlit run app.py
```

## 📄 Kullanım

1. Google Play'den analiz etmek istediğin oyunun **Package Name**’ini al (ör: `com.flatgames.patrolofficer`).
2. Streamlit arayüzünde Package Name’i gir ve **Analiz Et** butonuna bas.
3. Yorumları gör, CSV olarak indir.

## 📌 Notlar

- **Fake detection** için iki yaklaşım birleştirilmiştir:
  - Cosine Similarity (BERT embedding)
  - Tekrarlayan kelime analizi
- Model: `dbmdz/bert-base-turkish-uncased`

## 📂 Çıktılar

- `reviews_analysis.csv` → Analiz edilmiş yorumlar ve fake/genuine etiketi.

## 📝 Lisans

MIT License

---

Made with ❤️ by **Murat Kömürcü**
