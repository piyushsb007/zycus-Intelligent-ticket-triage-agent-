# Task 4 · Production Considerations

## 1. Failure Modes

### Wrong ticket classification

**Problem:** A new or unusual ticket may be matched to the wrong historical ticket.

**Detect:** Monitor low similarity scores and customer corrections.

**Mitigate:** Send low-confidence tickets for manual review and update the ticket dataset regularly.

### Wrong knowledge-base article

**Problem:** Retrieval may return an unrelated KB document.

**Detect:** Log retrieved documents and review poor matches.

**Mitigate:** Improve chunking, add product filters, and tune retrieval settings.

### Incomplete account summary

**Problem:** Missing account fields may lead to an inaccurate health brief.

**Detect:** Validate required fields before generating the summary.

**Mitigate:** Show “Unknown” for missing values and flag incomplete records.

---

## 2. Latency vs Quality

I chose **TF-IDF + cosine similarity** for ticket classification because it is fast, lightweight, and deterministic. A larger embedding model could improve semantic accuracy but would increase startup time and inference latency.

If latency became the main requirement, I would remove LLM evaluation from the request path, cache retrieval results, and reduce retrieval depth.

---

## 3. Data Sensitivity

Ticket and account data may contain PII such as names or email addresses.

The main application processes data locally and does not send ticket or account content to an external LLM during normal API inference. The Groq model is used only for the evaluation harness.

For production, I would mask emails, phone numbers, and customer identifiers before sending any data to an external service.

---

## 4. Scaling to 10× Volume

The first bottleneck would be the **in-memory TF-IDF ticket index**, which would increase RAM usage and startup time.

To scale further, I would persist vector indexes to disk, run multiple FastAPI workers, use a dedicated vector database, and replace brute-force similarity search with an approximate nearest-neighbor index.

Overall, the current design is suitable for the assignment dataset and small production workloads, while the above changes would support significantly larger ticket volumes.
