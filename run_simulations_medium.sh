#!/bin/bash

# Blockchain Simulation Commands - MEDIUM Workload Only
# Run this in one terminal for MEDIUM workload simulations
# CS595 Summer 2025 - PROJECT#2
# MEDIUM: 1000 wallets with 1000 transactions each generated with interval of 1.0

mkdir -p results

echo "Starting MEDIUM workload simulations for 10 years..."

# =====================
# MEDIUM workload (1000 wallets, 1000 transactions each, 1.0s interval)
# =====================

# BTC - MEDIUM (10 years = 525,600 blocks)
echo "Running BTC MEDIUM (10 years)..."
time python3 sim-blockchain.py \
    --chain BTC \
    --workload MEDIUM \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 600 \
    --blocksize 4096 \
    --wallets 1000 \
    --transactions 1000 \
    --interval 1.0 \
    --print 144 \
    --reward 50 \
    --halving 210000 \
    --years 10 \
    --export results/btc_medium.json > results/btc_medium.txt 2>&1

# BCH - MEDIUM (10 years = 525,600 blocks)
echo "Running BCH MEDIUM (10 years)..."
time python3 sim-blockchain.py \
    --chain BCH \
    --workload MEDIUM \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 600 \
    --blocksize 128000 \
    --wallets 1000 \
    --transactions 1000 \
    --interval 1.0 \
    --print 144 \
    --reward 12.5 \
    --halving 210000 \
    --years 10 \
    --export results/bch_medium.json > results/bch_medium.txt 2>&1

# LTC - MEDIUM (10 years = 2,102,400 blocks)
echo "Running LTC MEDIUM (10 years)..."
time python3 sim-blockchain.py \
    --chain LTC \
    --workload MEDIUM \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 150 \
    --blocksize 4096 \
    --wallets 1000 \
    --transactions 1000 \
    --interval 1.0 \
    --print 144 \
    --reward 50 \
    --halving 840000 \
    --years 10 \
    --export results/ltc_medium.json > results/ltc_medium.txt 2>&1

# DOGE - MEDIUM (10 years = 5,256,000 blocks)
echo "Running DOGE MEDIUM (10 years)..."
time python3 sim-blockchain.py \
    --chain DOGE \
    --workload MEDIUM \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 60 \
    --blocksize 4096 \
    --wallets 1000 \
    --transactions 1000 \
    --interval 1.0 \
    --print 144 \
    --reward 10000 \
    --halving 0 \
    --years 10 \
    --export results/doge_medium.json > results/doge_medium.txt 2>&1

# MEMO - MEDIUM (10 years = 96,464,840 blocks)
echo "Running MEMO MEDIUM (10 years)..."
time python3 sim-blockchain.py \
    --chain MEMO \
    --workload MEDIUM \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 3.27 \
    --blocksize 32000 \
    --wallets 1000 \
    --transactions 1000 \
    --interval 1.0 \
    --print 144 \
    --reward 51.8457072 \
    --halving 9644000 \
    --years 10 \
    --export results/memo_medium.json > results/memo_medium.txt 2>&1

echo "MEDIUM workload simulations completed!"
echo "Results saved in results/ directory"
echo "Check individual .txt files for detailed output" 