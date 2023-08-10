import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_distribution = dict()
    page_links = corpus[page]
    if not page_links:
        for page in corpus:
            prob_distribution[page] = 1 / len(corpus)
    else:
        prob_all = (1 - damping_factor) / len(corpus)
        prob_link = damping_factor / len(page_links) + prob_all
        for page in corpus:
            if page in page_links:
                prob_distribution[page] = prob_link
            else:
                prob_distribution[page] = prob_all
    
    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = dict().fromkeys(corpus.keys(), 0)
    cur_page = random.choice(list(corpus))
    for _ in range(n):
        page_ranks[cur_page] += 1
        prob_distribution = transition_model(corpus, cur_page, damping_factor)
        cur_page = random.choices(list(prob_distribution.keys()), list(prob_distribution.values()))[0]
    
    for page in page_ranks:
        page_ranks[page] /= n
    
    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = dict().fromkeys(corpus.keys(), 1 / len(corpus))
    accuracy_achieved = False
    while not accuracy_achieved:
        accuracy_achieved = True
        for page in corpus:
            prob_link = 0
            for prev_page in corpus:
                # No link from prev_page => treat as it has links to all pages including itself
                if len(corpus[prev_page]) == 0:
                    prob_link += page_ranks[prev_page] / len(corpus)
                elif page in corpus[prev_page]:
                    prob_link += page_ranks[prev_page] / len(corpus[prev_page])
            
            new_rank = (1 - damping_factor) / len(corpus) + damping_factor * prob_link
            if accuracy_achieved and abs(page_ranks[page] - new_rank) > 0.001:
                accuracy_achieved = False
            page_ranks[page] = new_rank

    return page_ranks


if __name__ == "__main__":
    main()
