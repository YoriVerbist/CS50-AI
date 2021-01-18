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


def transition_model(corpus: dict, page: str, damping_factor: float) -> dict:
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    chances = dict()
    for item, value in corpus.items():
        if item == page:
            all_items = len(value) + 1
            items = len(value)
            chance = damping_factor / items
            chances[item] = (1 - damping_factor) / all_items
            chance += (1 - damping_factor) / all_items
            for val in value:
                chances[val] = chance
    return chances
    

def sample_pagerank(corpus: dict, damping_factor: float, n: int) -> dict:
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample = dict()
    names = list(corpus.keys())
    page = names[random.randint(0,len(names)-1)]
    for i in range(n):
        model = transition_model(corpus, page, damping_factor)
        for item in model:
            sample[item] = model[item]
    return sample


def iterate_pagerank(corpus: dict, damping_factor: float) -> dict:
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = dict()
    n = len(corpus)
    pr = 1/n
    for key, value in corpus.items():
        rank[key] = pr
    for key, value in corpus.items():
        pr = (1 - damping_factor) / n
        sumation = 0
        links = len(value)
        for item in value:
            sumation += rank[item] / len(corpus[item])
        pr += (damping_factor * sumation)
        rank[key] = pr
    return rank


if __name__ == "__main__":
    main()
