# AI Paper Collector

<div align="center">
  <img src="https://img.shields.io/badge/Author-QQuante-blue.svg" alt="Author: QQuante" />
  <img src="https://img.shields.io/badge/Organization-ParaDevs-lightgrey.svg" alt="Organization: ParaDevs" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT" />
</div>

<p align="center">
  A robust, command-line tool for collecting academic papers to build datasets for AI research and model training.
</p>

---

## ❯ Overview

`AI Paper Collector` is a Python-based utility designed to streamline the process of gathering a large corpus of scholarly articles. It programmatically downloads papers from two major academic indexes:

-   **Semantic Scholar**: A vast, AI-powered database of scientific literature.
-   **arXiv**: A popular open-access archive for new research papers.

This tool is built for AI researchers, data scientists, and developers who need to assemble domain-specific datasets for training models or conducting NLP research.

**Important Note:** This tool does **not** use Google Scholar. It relies on the official, public APIs provided by the services listed above.

This tool empowers AI researchers, data scientists, and developers to quickly assemble domain-specific datasets for a variety of tasks, including:

-   🤖 **Training Large Language Models (LLMs)**
-   🧠 **Natural Language Processing (NLP) Research**
-   📊 **Text Mining and Information Extraction**
-   📚 **Automated Literature Reviews**

---

## ❯ Core Features

| Feature                 | Description                                                                                              |
| ----------------------- | -------------------------------------------------------------------------------------------------------- |
| **Multi-Source Fetching** | Gathers papers from both Semantic Scholar and arXiv to maximize coverage.                                |
| **CLI Control**         | Full control through the command line. No need to edit the code to change queries or parameters.       |
| **Robust Error Handling** | Gracefully handles common issues like paywalls (`403 Forbidden`), broken links (`404 Not Found`), and bad API data. |
| **Detailed Logging**    | Creates a comprehensive `.txt` log file for each session, perfect for debugging and tracking provenance. |
| **Polite & Responsible**  | Includes built-in delays to avoid overwhelming the APIs and ensures a proper `User-Agent`.             |

---

## ❯ Installation

Follow these steps to get the tool up and running.

### 1. Clone the Repository
First, clone this repository to your local machine using git.

```bash
git clone https://github.com/qquante/ai-paper-collector.git
cd ai-paper-collector
```

### 2. Set Up a Virtual Environment (Recommended)
It is highly recommended to use a virtual environment to keep project dependencies isolated.

```bash
# Create the virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
Install all the required Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

---

## ❯ Usage Guide

The script is controlled entirely through command-line flags. Here are some practical examples.

### Basic Example: Simple Query
This is the most straightforward use case. The query is a simple string, and we will use the default values for the number of papers (100) and the output folder (`corpus`).

```bash
python collector.py --query "Generative Adversarial Networks"
```

### Advanced Example: Complex Query and Custom Outputs
Here, we define a more complex query, set a higher limit for downloaded papers, and specify a custom output directory.

-   **Query**: `'Large Language Models' AND 'ethical considerations'`
-   **Max Papers**: `500`
-   **Output Directory**: `llm_ethics_papers`

```bash
python collector.py --query "'Shor's Algorithm' OR 'Grover's Algorithm'" --max-papers 500 --output-dir "quantum_computing_papers"
```

### Understanding the Output
After the script finishes, your output directory will contain:

1.  **PDF Files**: All the papers that were successfully downloaded.
2.  **`collection_log.txt`**: A detailed log of the entire process. This file is **crucial** for understanding what happened. It lists every paper the script attempted to download, clearly marking successes, warnings (e.g., a paper listed as "open access" but with a missing URL), and errors (e.g., a 404 Not Found or 403 Forbidden error).

You can use the titles from this log to manually search for papers that the script failed to download automatically.

### All Command-Line Arguments

| Argument           | Short | Description                                                                 | Default    | Required |
| ------------------ | ----- | --------------------------------------------------------------------------- | ---------- | :------: |
| `--query`          | `-q`  | The search query for finding papers. Use quotes for multi-word phrases.     | `None`     |   Yes    |
| `--max-papers`     | `-m`  | The maximum total number of papers you want to successfully download.       | `100`      |    No    |
| `--output-dir`     | `-o`  | The directory where your downloaded papers and log file will be saved.      | `corpus`   |    No    |

---

## ❯ Case Study: Collecting Papers on Quantum Algorithms

To demonstrate a real-world use case, we ran the collector with a query focused on foundational quantum algorithms. The `quantum_computing_papers` directory included in this repository is the direct result of this run.

### The Command

The following command was executed:
```bash
python collector.py --query "'Shor's Algorithm' OR 'Grover's Algorithm'" --max-papers 15 --output-dir "quantum_computing_papers"
```

### The Outcome

-   **Target**: `15` papers
-   **Successfully Downloaded**: `15` papers
-   **Warnings Issued**: The log shows several warnings for papers that were listed as "Open Access" but had no valid URL, or were behind a paywall (403/404 errors). The script successfully logged these issues and continued searching until its target of 15 papers was met.

This is a perfect example of how the `AI Paper Collector` works. It diligently works towards its goal, intelligently skipping over problematic entries and logging them for manual review, ensuring you get the number of papers you requested.

**We encourage you to inspect the `collection_log.txt` inside the `quantum_computing_papers` folder to see a real example of the detailed output.**

---

## ❯ Contributing

Contributions are welcome! If you have suggestions for improvements, please open an issue or submit a pull request.

## ❯ License

This project is licensed under the **MIT License**. See the `LICENSE` file for full details.

<div align="center">
  Authored by QQuante
</div> 
