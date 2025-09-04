#!/bin/bash

# Blockchain Simulation Commands - NONE Workload Only
# Run this in one terminal for NONE workload simulations
# CS595 Summer 2025 - PROJECT#2

mkdir -p results

echo "Starting NONE workload simulations for 10 years..."

# =====================
# NONE workload (No user transactions, mining only)
# =====================

# BTC - NONE (10 years = 525,600 blocks)
echo "Running BTC NONE (10 years)..."
time python3 sim-blockchain.py \
    --chain BTC \
    --workload NONE \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 600 \
    --blocksize 4096 \
    --wallets 0 \
    --transactions 0 \
    --interval 10.0 \
    --print 144 \
    --reward 50 \
    --halving 210000 \
    --years 10 \
    --export results/btc_none.json > results/btc_none.txt 2>&1

# BCH - NONE (10 years = 525,600 blocks)
echo "Running BCH NONE (10 years)..."
time python3 sim-blockchain.py \
    --chain BCH \
    --workload NONE \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 600 \
    --blocksize 128000 \
    --wallets 0 \
    --transactions 0 \
    --interval 10.0 \
    --print 144 \
    --reward 12.5 \
    --halving 210000 \
    --years 10 \
    --export results/bch_none.json > results/bch_none.txt 2>&1

# LTC - NONE (10 years = 2,102,400 blocks)
echo "Running LTC NONE (10 years)..."
time python3 sim-blockchain.py \
    --chain LTC \
    --workload NONE \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 150 \
    --blocksize 4096 \
    --wallets 0 \
    --transactions 0 \
    --interval 10.0 \
    --print 144 \
    --reward 50 \
    --halving 840000 \
    --years 10 \
    --export results/ltc_none.json > results/ltc_none.txt 2>&1

# DOGE - NONE (10 years = 5,256,000 blocks)
echo "Running DOGE NONE (10 years)..."
time python3 sim-blockchain.py \
    --chain DOGE \
    --workload NONE \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 60 \
    --blocksize 4096 \
    --wallets 0 \
    --transactions 0 \
    --interval 10.0 \
    --print 144 \
    --reward 10000 \
    --halving 0 \
    --years 10 \
    --export results/doge_none.json > results/doge_none.txt 2>&1

# MEMO - NONE (10 years = 96,464,840 blocks)
echo "Running MEMO NONE (10 years)..."
time python3 sim-blockchain.py \
    --chain MEMO \
    --workload NONE \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 3.27 \
    --blocksize 32000 \
    --wallets 0 \
    --transactions 0 \
    --interval 10.0 \
    --print 144 \
    --reward 51.8457072 \
    --halving 9644000 \
    --years 10 \
    --export results/memo_none.json > results/memo_none.txt 2>&1

echo "NONE workload simulations completed!"
echo "Results saved in results/ directory"
echo "Check individual .txt files for detailed output" 