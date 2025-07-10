# 👋 Welcome, and thanks for your interest!

We're excited that you're considering joining our mission to fight phishing and protect users online.  
This technical challenge is part of our selection process to find **super developers** who enjoy building smart, scalable systems.

We truly appreciate the time and effort you're about to invest — good luck and have fun!

# 🕵️ Domain Scanner – Technical Challenge

Build a **queue‑based pipeline** that scans domains, collects evidence, and writes results in MongoDB.  
**Focus areas**: async queues with `saq`, Playwright automation, clean Docker setup, and robust logging.

---

## 🛣 Processing Flow

Implement **three queues**. Each queue must log its key steps to `stdout` (Python `logging`).

### 1️⃣ `resolve` queue  
**Input**: `domain: str`, `wildcard: bool`  

| Step | Requirement |
|------|-------------|
| 1.1 | Perform an A / AAAA lookup for the *root* domain. |
| 1.2 | If `wildcard=True`, generate a small word‑list (`www`, `mail`, `login`, `admin`, `api`) and resolve each sub‑domain **once** (no retries for sub‑domains). |
| 1.3 | **If at least one hostname resolves** → enqueue **`http_check`** for every resolved hostname and **stop retrying** for that hostname. |
| 1.4 | **If the root domain does *not* resolve** → re‑enqueue the same task with a delay of **5 minutes** (`saq.enqueue_in`) so it keeps trying until it resolves. |
| 1.5 | Log every attempt (`INFO`) and any exception (`ERROR`). |

Example enqueue (immediately or delayed):

```python
# immediate for next queue
saq.enqueue("http_check", hostname)

# retry current task in 5 minutes
saq.enqueue_in(300, "resolve", domain, wildcard)
```

### 2️⃣ `http_check` queue  
**Input**: `hostname: str`  

| Step | Requirement |
|------|-------------|
| 2.1 | Send a GET request to `http://{hostname}` (or follow 30x to HTTPS) using **`curl_cffi`**. |
| 2.2 | Set *Chrome‑like* headers & UA (imitate current stable Chromium UA string). *Extra points*: add additional realistic headers (`sec-ch-ua`, `sec-fetch-site`, etc.). |
| 2.3 | Timeout: 10 s. |
| 2.4| **Success criteria**: status code in 200–399. On success, enqueue **`browser_capture`**. |
| 2.5 | On failure, log reason and exit (do **not** retry the request automatically). |

### 3️⃣ `browser_capture` queue  
**Input**: `hostname: str`  

| Step | Requirement |
|------|-------------|
| 3.1 | Use Playwright (Chromium, headless) to load the URL. |
| 3.2 | Wait `load` event (max 15 s). |
| 3.3 | Take full‑page screenshot and save under `/evidence/{hostname}.png` (or Base64). |
| 3.4 | Extract final URL and page title. |
| 3.5 | **Persist** the consolidated result in MongoDB (`scans` collection):<br>`{hostname, screenshot_path, title, final_url, scanned_at}` |
| 3.6 | Log completion. |

---

## 🎯 API Spec

`POST /scan`

```jsonc
{
  "domain": "example.com",
  "wildcard": true
}
```

The endpoint should enqueue the `resolve` task and respond with:

```jsonc
{
  "status": "queued",
  "scan_id": "<uuid-or-random-id>"
}
```

---

## 🐳 Local Run

```bash
docker-compose up --build
```

---

## 📝 Deliverables

1. Public repo link  
2. Short **DECISIONS.md** (or section in README) explaining any design deviations  
3. Sample execution log demonstrating retries & queue hand‑offs  
4. Time spent estimate  

---