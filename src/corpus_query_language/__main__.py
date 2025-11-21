"""Command-line interface for Corpus Query Language."""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import NoReturn

from corpus_query_language.core.core import CQLEngine

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_corpus(corpus_path: Path) -> list[dict[str, str]]:
    """Load a corpus from a JSON file.

    Args:
        corpus_path: Path to the JSON corpus file.

    Returns:
        The corpus as a list of dictionaries.

    Raises:
        FileNotFoundError: If the corpus file does not exist.
        json.JSONDecodeError: If the corpus file is not valid JSON.
    """
    if not corpus_path.exists():
        msg = f"Corpus file not found: {corpus_path}"
        raise FileNotFoundError(msg)

    with corpus_path.open(encoding="utf-8") as f:
        return json.load(f)


def main() -> NoReturn:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Corpus Query Language - Query annotated text corpora"
    )
    parser.add_argument("query", type=str, help="CQL query to execute")
    parser.add_argument("corpus", type=Path, help="Path to JSON corpus file")
    parser.add_argument(
        "-m",
        "--mode",
        choices=["match", "findall"],
        default="findall",
        help="Query mode: 'match' returns boolean, 'findall' returns all matches",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug mode"
    )

    args = parser.parse_args()

    # Set logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    try:
        # Load corpus
        corpus = load_corpus(args.corpus)
        logger.info(f"Loaded corpus with {len(corpus)} tokens")

        # Create engine
        engine = CQLEngine()

        # Execute query
        if args.mode == "match":
            result = engine.match(
                corpus, args.query, verbose=args.verbose, debug=args.debug
            )
            print(f"Match: {result}")
            sys.exit(0 if result else 1)
        else:
            results = engine.findall(
                corpus, args.query, verbose=args.verbose, debug=args.debug
            )
            print(f"Found {len(results)} matches:")
            for start, end in results:
                print(f"  [{start}:{end}]")
            sys.exit(0)

    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in corpus file: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
