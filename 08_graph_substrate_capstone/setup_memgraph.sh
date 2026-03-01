#!/bin/bash
# setup_memgraph.sh - Infrastructure for Week 8 Capstone

echo "🚀 Starting Memgraph Platform for the Week 8 Showdown..."

# Running Memgraph Platform (includes Lab on port 3000)
docker run -d \
  -p 7687:7687 \
  -p 3000:3000 \
  -v mg_lib:/var/lib/memgraph \
  --name clinical-graph-substrate \
  memgraph/memgraph-platform

echo "✅ Memgraph is live!"
echo "🔗 Access Visualization Lab at: http://localhost:3000"
echo "🛠️ Bolt Protocol (for Notebooks) active on: bolt://localhost:7687"