# -*- coding: utf-8 -*-
"""
AI Paper Collector
==================
A command-line tool to gather academic papers for building AI training datasets.
Authored by: QQuante (Quante ParaDevs)
"""

import os
import re
import time
import argparse
import logging
import requests
import arxiv
import semanticscholar as sch

HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def setup_logging(log_path):
    """Configures file and stream logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def sanitize_filename(filename):
    """Removes invalid characters from a string to make it a valid filename."""
    filename = filename.encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def search_arxiv(query, max_papers, download_folder, state):
    """Searches and downloads papers from the arXiv repository."""
    logging.info("--- Starting arXiv Search ---")
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_papers,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        for result in client.results(search):
            if state['download_count'] >= state['total_max']:
                logging.info("Target number of papers reached. Stopping arXiv search.")
                break

            try:
                title = sanitize_filename(result.title)
                filepath = os.path.join(download_folder, f"{title}.pdf")
                
                if not os.path.exists(filepath):
                    logging.info(f"Downloading from arXiv: '{result.title}'")
                    result.download_pdf(dirpath=download_folder, filename=f"{title}.pdf")
                    logging.info(f"-> Saved as {filepath}")
                    state['download_count'] += 1
                    time.sleep(2)
                else:
                    logging.info(f"-> Already exists, skipping: {filepath}")

            except Exception as e:
                logging.error(f"Failed to download paper '{result.title}' from arXiv. Reason: {e}")

    except Exception as e:
        logging.error(f"An unexpected error occurred during arXiv search: {e}")

def search_semantic_scholar(query, max_papers, download_folder, state):
    """Searches and downloads papers from Semantic Scholar."""
    logging.info("--- Starting Semantic Scholar Search ---")
    try:
        s2 = sch.SemanticScholar()
        results = s2.search_paper(query)
        
        for paper in results:
            if state['download_count'] >= state['total_max']:
                logging.info("Target number of papers reached. Stopping Semantic Scholar search.")
                break

            if paper.openAccessPdf and 'url' in paper.openAccessPdf and paper.openAccessPdf['url']:
                try:
                    title = sanitize_filename(paper.title)
                    filepath = os.path.join(download_folder, f"{title}.pdf")
                    
                    if not os.path.exists(filepath):
                        logging.info(f"Downloading from Semantic Scholar: '{paper.title}'")
                        pdf_url = paper.openAccessPdf['url']
                        
                        response = requests.get(pdf_url, headers=HTTP_HEADERS, timeout=30)
                        response.raise_for_status()

                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        logging.info(f"-> Saved as {filepath}")
                        state['download_count'] += 1
                        time.sleep(2)
                    else:
                        logging.info(f"-> Already exists, skipping: {filepath}")

                except requests.exceptions.RequestException as e:
                    logging.warning(f"Failed to download '{paper.title}'. Reason: {e}")
                    logging.warning(f"  - Attempted URL: {paper.openAccessPdf.get('url')}")
                except Exception as e:
                    logging.error(f"An unexpected error occurred processing paper '{paper.title}': {e}")
            elif paper.openAccessPdf:
                logging.warning(f"'{paper.title}' listed as Open Access, but no PDF URL was provided. Skipping.")

    except Exception as e:
        logging.error(f"A critical error occurred while searching Semantic Scholar: {e}")


# --- Main Execution ---
def main():
    """Main function to parse arguments and run the download process."""
    parser = argparse.ArgumentParser(
        description="AI Paper Collector - A tool to gather academic papers for AI training.",
        epilog="Authored by QQuante"
    )
    parser.add_argument('-q', '--query', type=str, required=True, help="Search query for finding papers.")
    parser.add_argument('-m', '--max-papers', type=int, default=100, help="Maximum number of papers to download.")
    parser.add_argument('-o', '--output-dir', type=str, default='corpus', help="Directory to save papers and logs.")
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    log_file_path = os.path.join(args.output_dir, 'collection_log.txt')
    setup_logging(log_file_path)

    logging.info("=" * 50)
    logging.info("AI Paper Collector Initialized")
    logging.info(f"Query: '{args.query}'")
    logging.info(f"Maximum papers: {args.max_papers}")
    logging.info(f"Output directory: {args.output_dir}")
    logging.info("-" * 50)

    download_state = {'download_count': 0, 'total_max': args.max_papers}

    search_semantic_scholar(args.query, args.max_papers, args.output_dir, download_state)
    
    if download_state['download_count'] < args.max_papers:
        remaining_needed = args.max_papers - download_state['download_count']
        search_arxiv(args.query, remaining_needed, args.output_dir, download_state)

    logging.info("=" * 50)
    logging.info("Collection Complete")
    logging.info(f"Total papers downloaded: {download_state['download_count']}")
    logging.info(f"Output saved in '{args.output_dir}'")
    logging.info(f"Log file available at '{log_file_path}'")
    logging.info("=" * 50)


if __name__ == "__main__":
    main() 
