# NewsRAG

This repository follows the development of a personal project focused on the study of **Python applied to Data and Artificial Intelligence**, with a focus on **data collection, data quality, and NLP/RAG applications**.

The idea of the project is to build, step by step, a pipeline capable of:
- Automatically collecting news articles
- Evaluating the quality of the collected data
- Preparing this data for use in language models
- Allowing, in the future, chatbot interaction based on the ingested content

The project is under continuous evolution and documents both technical decisions and learnings throughout the process.

---

## 🎯 Project Objective

- Automatically collect news (initially via RSS).
- Respect scraping best practices (robots.txt, rate limit).
- Store data in a structured format (JSON).
- Measure **ingestion quality** through objective metrics.
- Prepare data for future stages:
  - Processing and cleaning
  - Semantic evaluation
  - Retrieval-Augmented Generation (RAG)

---

## 🛠️ Technologies Used (so far)

- **Python 3.11**
- **feedparser** — RSS feed parsing
- **trafilatura** — download and text extraction
- **Conda** — environment management
- **Git/GitHub** — versioning and project documentation

---

## 📌 Current Project Status

✔ Initial ingestion pipeline implemented  
✔ News collection via RSS  
✔ Access verification via `robots.txt`  
✔ Text extraction from pages  
✔ Structured saving in JSON  
✔ Generation of ingestion quality metrics:
  - failed downloads
  - robots.txt blocks
  - empty extractions
  - fallback usage
  - text length statistics

✔ Execution reports saved in JSON for auditing and future comparison  

---

## 📊 Current Structure
NewsRAG/
├─ data/
│  └─ raw/           # Raw collected data
├─ scripts/
│  ├─ data_ingest.py
│  └─ utils.py
├─ reports/          # Generated ingestion reports
├─ environment.yml
├─ README.md
└─ .gitignore


---

## 🚀 Next Steps

- Processing and cleaning of collected texts
- Definition of simple semantic quality criteria
- Text chunking
- Embedding generation
- Initial structuring of a RAG pipeline
- Exploration via notebooks

---

## ⚙️ How to Run (current)

> Instructions will be refined as the project evolves.

1. Create the Conda environment:
Bash

conda env create -f environment.yml
conda activate newsrag-env

2. Run the ingestion script:
Bash

python scripts/data_ingest.py


### 👨‍💻 About Me
I am a Systems Analysis and Development student, focusing on Data and Artificial Intelligence. This project is a personal initiative to apply theoretical concepts, learn industry tools (Python, Git, data pipelines), and document my learning process in a practical and transparent way.