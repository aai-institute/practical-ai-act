import re
import warnings
import xml.etree.ElementTree as etree

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor


def _parse_roman_numeral(numeral: str) -> int:
    roman_numerals = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }
    result = 0
    last_value = 0
    for char in reversed(numeral):
        value = roman_numerals[char]
        if value < last_value:
            result -= value
        else:
            result += value
        last_value = value
    return result


class AIAReferenceProcessor(InlineProcessor):
    """Process delimited references to the AI Act into clickable links

    Supports references to Articles, Annexes, and Recitals.

    Examples (assuming the pipe ``|`` as the inline delimiter):
    - ``|Article 11|``, ``|Art. 13|``
    - ``|Annex IV|``
    - ``|Recital 7|``
    """

    ARTICLE_PATTERN = r"Art(?:\.|icle) (?P<number>\d+)"
    ANNEX_PATTERN = (
        r"Annex (?P<number>[IXV]+)"  # NOTE: Incomplete pattern for roman numerals
    )
    RECITAL_PATTERN = r"Recital (?P<number>\d+)"
    AIA_EXPLORER_URL = "https://artificialintelligenceact.eu/{type}/{number}"

    def handleMatch(self, m, data):
        el = etree.Element("a")
        el.text = m.group(1)

        href = None
        if match := re.match(self.ARTICLE_PATTERN, m.group(1)):
            href = self.AIA_EXPLORER_URL.format(
                type="article",
                number=match.group("number"),
            )
        if match := re.match(self.ANNEX_PATTERN, m.group(1)):
            href = self.AIA_EXPLORER_URL.format(
                type="annex",
                number=_parse_roman_numeral(match.group("number")),
            )
        if match := re.match(self.RECITAL_PATTERN, m.group(1)):
            href = self.AIA_EXPLORER_URL.format(
                type="recital", number=match.group("number")
            )

        if href:
            el.set("href", href)
            el.set("target", "_blank")
            el.set("rel", "noopener noreferrer")
            el.set("class", "aia-ref")
        else:
            # Unparsed reference - fallback to plain text
            el.tag = "span"
            el.set("class", "aia-ref-unparsed")
            warnings.warn(f"Unparsed AIA reference: {m.group(1)}")

        return el, m.start(0), m.end(0)


class AIAMarkdownExtension(Extension):
    """Markdown extension for working with AI Act references"""

    def extendMarkdown(self, md):
        REF_PATTERN = r"\|(.*?)\|"
        md.inlinePatterns.register(AIAReferenceProcessor(REF_PATTERN, md), "aia", 175)


def makeExtension(**kwargs):
    return AIAMarkdownExtension(**kwargs)
