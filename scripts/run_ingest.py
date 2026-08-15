"""Runs the full ingest pipeline: load -> chunk -> embed -> index."""

import argparse
from dotenv import load_dotenv
load_dotenv()

from app.ingestion.loader import load_directory
from app.ingestion.chunking import fixed_size_chunking, structure_aware_chunking
from app.ingestion.index_builder import build_indexes

def main(data_dir: str, strategy: str):
    docs = load_directory(data_dir)
    print(f"Loaded {len(docs)} documents from {data_dir}.")

    strategy_fn = {"fixed_size": fixed_size_chunking, "structure_aware": structure_aware_chunking}[strategy]
    all_chunks = []
    for doc in docs:
        all_chunks.extend(strategy_fn(doc))
    print(f"Generated {len(all_chunks)} chunks using the strategy '{strategy}'.")

    stats = build_indexes(all_chunks)
    print(f"Indexed: {stats}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="data/raw")
    parser.add_argument("--strategy", default="structure_aware",
                        choices=["fixed_size", "structure_aware"])
    args = parser.parse_args()
    main(args.data_dir, args.strategy)