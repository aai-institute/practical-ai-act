from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup
from mkdocs.structure.pages import Page

_nav_graph = {}


def _resolve(relative_url: str, current_url: str) -> str:
    """
    Resolves a URL (containing `../` segments) relative to the current URL.
    """

    # Split the current URL into parts
    current_parts = current_url.rstrip("/").split("/")
    # Split the relative URL into parts
    relative_parts = relative_url.split("/")

    # Handle the case where the relative URL starts with ".."
    while relative_parts and relative_parts[0] == "..":
        if current_parts:
            current_parts.pop()
        relative_parts.pop(0)

    # Join the remaining parts to form the resolved URL
    result = "/".join(current_parts + relative_parts)
    if not result.startswith("/"):
        result = "/" + result
    return result


def _extract_internal_links(page: Page) -> list[str]:
    """
    Extracts internal link URLs from the given HTML content.
    """

    links = []

    soup = BeautifulSoup(page.content, "html.parser")

    for link in soup.find_all("a", href=True):
        href = link["href"]
        # Ignore anchors and external links
        if href.startswith("#") or href.startswith("http"):
            continue
        links.append(_resolve(href, page.url))
    return links


def on_post_page(output, /, *, page: Page, config):
    key = page.url
    if not key.startswith("/"):
        key = "/" + key
    _nav_graph[key] = _extract_internal_links(page)


def _to_mermaid(graph: dict[str, list[str]]) -> str:
    """
    Converts the navigation graph to Mermaid format for visualization.
    """

    LEVEL_SEPARATOR = "#"

    def _node_name(url: str) -> str:
        """
        Converts a URL to a node name for Mermaid.
        """
        return url.replace("/", LEVEL_SEPARATOR).strip(LEVEL_SEPARATOR) or "root"

    def _node_title(url: str) -> str:
        return "\n↳ ".join(url.rstrip("/").split("/"))[2:] or "root"

    def _subgraph_id(node: str) -> str:
        """
        Converts a URL to a subgraph ID for Mermaid.
        """
        return node.split(LEVEL_SEPARATOR, 1)[0] if LEVEL_SEPARATOR in node else None

    # Build a Mermaid flowchart
    mermaid = "flowchart TD\n"

    all_nodes = set(graph.keys()) | {
        node for targets in graph.values() for node in targets
    }

    # Add subgraphs for each node
    subgraphs = defaultdict(list)
    for node in all_nodes:
        subgraph_id = _subgraph_id(_node_name(node))
        if subgraph_id:
            subgraphs[subgraph_id].append(node)

    for subgraph_id, nodes in subgraphs.items():
        mermaid += f"  subgraph {subgraph_id}\n"
        for node in nodes:
            mermaid += f'    {_node_name(node)}["{node}"]\n'
        mermaid += "  end\n"
        mermaid += "\n"

    # Add all nodes without a subgraph id
    for node in all_nodes:
        if not _subgraph_id(node):
            mermaid += f'  {_node_name(node)}["{_node_title(node)}"]\n'
            mermaid += "\n"

    # Add edges to the flowchart
    for node, targets in graph.items():
        for to_node in targets:
            mermaid += f"  {_node_name(node)} --> {_node_name(to_node)}\n"

    # Style definitions
    mermaid += "classDef default text-align:left;\n"

    return mermaid


def on_post_build(*, config):
    Path("nav_graph.mmd").write_text(_to_mermaid(_nav_graph))
