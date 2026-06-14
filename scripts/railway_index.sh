#!/usr/bin/env sh
set -eu

echo "Building Railway vector index..."
python -m vector_store.indexer
echo "Vector index build complete."
