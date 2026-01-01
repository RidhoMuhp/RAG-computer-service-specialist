1. Definisi Project

Nama project :
👉 TechCare AI – Computer Service Specialist Chatbot

Fungsi utama chatbot:
- Menjawab diagnosa masalah laptop/PC
- Memberi estimasi service & solusi
- Memberi langkah troubleshooting awal
- Menjawab pertanyaan harga service umum
- Berperan seperti teknisi profesional
Kenapa pakai RAG?
Karena:
- Jawaban berbasis data teknis nyata
Tidak halu seperti LLM murni
2. Use Case Chatbot tidak hanya jawab, tapi:
- Tanya balik (clarifying question)
- Memberi diagnosis bertahap
- Memberi opsi solusi murah → mahal

3. Data untuk RAG
- Knowledge Teknis
    Gejala → Penyebab → Solusi
- Service Pricing (estimasi)
- SOP Teknisi
    Urutan pengecekan
    Risiko service
    Estimasi waktu pengerjaan
- FAQ Customer
    Apakah data aman?
    Berapa lama pengerjaan?
    Garansi service?

4. Format Data (simple dulu)
- .txt
- .md
- .pdf
- Atau .csv

5. Arsitektur RAG
User Question
     ↓
Embedding Query
     ↓
Vector Database (knowledge service laptop)
     ↓
Relevant Context
     ↓
LLM (GPT / Llama / Mixtral)
     ↓
Final Answer (seperti teknisi)
