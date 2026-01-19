# 📄 NewsRAG – Data Contract
## Phase 1: Raw Ingestion

This document defines the formal data contract for the **raw ingestion layer** of the NewsRAG project. It serves as the technical agreement to ensure the data foundation is solid, auditable, and reproducible.

---

## 1. Purpose
This contract exists to:
- Formalize what "raw data" means within this project.
- Ensure **reprocessability**: if the pipeline fails downstream, the original data is preserved.
- Prevent **logic drift** (silent changes in data structure over time).

> **Design Principle:** Raw data must be honest, not perfect. Errors, gaps, and failures are signals—not bugs to be hidden.

---

## 2. Scope
This phase focuses exclusively on **data collection**, not interpretation.

- **Data Source:** RSS feeds (e.g., NASA RSS).
- **Current Focus:** Structured news-like content.
- **Output Format:** Individual JSON files.
- **Storage Location:** `data/raw/`
- **Quality Monitoring:** Ingestion metrics saved as external reports in `reports/`.

---

## 3. Definition of "Raw Data"
In this project, **raw data** is defined as data gathered by the ingestion code **without runtime errors**, regardless of perceived completeness or quality.

### Acceptance Rules
A raw article is considered valid when all of the following conditions are met:

* [x] The URL is allowed by `robots.txt`.
* [x] The page download does not raise an exception and returns content (or None if extraction fails, see fallback rules).
* [x] A JSON file is successfully written to disk.
* [x] The `context` field may contain:
  - Extracted article text
  - RSS description fallback
  - `null` if extraction fails completely

---

## 4. Data Schema
Each raw JSON file must follow this structure:

```json
{
  "title": "string",
  "url": "string",
  "source": "string",
  "date": "string",
  "context": "string | null"
}
```
### Field Definitions

| Field | Description | Example |
| :--- | :--- | :--- |
| **title** | Title provided by the RSS feed entry | "Mars Rover Update" |
| **url** | Canonical link to the original article | "https://nasa.gov/news/..." |
| **source** | Logical source name (e.g., NASA) | "NASA" |
| **date** | Publication date as provided (unnormalized) | "Fri, 09 Jan 2026..." |
| **context** | Extracted article text or fallback | "Full extracted content..." |

---

## 5. Storage and Naming Convention
Files are stored immutably to ensure no data is overwritten.

- **Location:** `data/raw/`
- **Naming Pattern:** `[sanitized_title]_[timestamp].json`
- **Format:** UTF-8 encoded JSON.

---

## 6. Ingestion Quality Metrics
Each run generates a metrics report for auditing purposes, containing:

* **total_urls**: Number of URLs processed in this run.
* **robots_blocked**: Number of URLs skipped due to `robots.txt` restrictions.
* **download_failed**: Number of articles that could not be downloaded.
* **extraction_empty**: Number of articles where text extraction returned no content.
* **fallback_used**: Number of articles where the RSS description was used as a fallback.
* **texts_with_content**: Number of articles with any non-empty text content.
* **avg_text_length**: Average length of extracted text across all articles with content.
* **min_text_length**: Minimum length of extracted text.
* **max_text_length**: Maximum length of extracted text.

---

## 7. Ethical Constraints
Every URL is checked against the source's `robots.txt`. If access is disallowed, the event is logged in metrics and the article is skipped. This is a **hard constraint**, not a best-effort rule.

---

## 8. Out of Scope (Phase 1)
The following operations belong to later stages of the pipeline:
* Text cleaning/normalization.
* Language detection.
* Embedding generation.
* Chunking or Vector storage.
* Semantic filtering.