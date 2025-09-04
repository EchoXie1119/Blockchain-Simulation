#!/bin/bash

# Blockchain Simulation Commands - SMALL Workload Only
# Run this in one terminal for SMALL workload simulations
# CS595 Summer 2025 - PROJECT#2
# SMALL: 10 wallets with 10 transactions each generated with interval of 10.0

mkdir -p results

echo "Starting SMALL workload simulations for 10 years..."

# =====================
# SMALL workload (10 wallets, 10 transactions each, 10.0s interval)
# =====================

# BTC - SMALL (10 years = 525,600 blocks)
echo "Running BTC SMALL (10 years)..."
time python3 sim-blockchain.py \
    --chain BTC \
    --workload SMALL \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 600 \
    --blocksize 4096 \
    --wallets 10 \
    --transactions 10 \
    --interval 10.0 \
    --print 144 \
    --reward 50 \
    --halving 210000 \
    --years 10 \
    --export results/btc_small.json > results/btc_small.txt 2>&1

# BCH - SMALL (10 years = 525,600 blocks)
echo "Running BCH SMALL (10 years)..."
time python3 sim-blockchain.py \
    --chain BCH \
    --workload SMALL \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 600 \
    --blocksize 128000 \
    --wallets 10 \
    --transactions 10 \
    --interval 10.0 \
    --print 144 \
    --reward 12.5 \
    --halving 210000 \
    --years 10 \
    --export results/bch_small.json > results/bch_small.txt 2>&1

# LTC - SMALL (10 years = 2,102,400 blocks)
echo "Running LTC SMALL (10 years)..."
time python3 sim-blockchain.py \
    --chain LTC \
    --workload SMALL \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 150 \
    --blocksize 4096 \
    --wallets 10 \
    --transactions 10 \
    --interval 10.0 \
    --print 144 \
    --reward 50 \
    --halving 840000 \
    --years 10 \
    --export results/ltc_small.json > results/ltc_small.txt 2>&1

# DOGE - SMALL (10 years = 5,256,000 blocks)
echo "Running DOGE SMALL (10 years)..."
time python3 sim-blockchain.py \
    --chain DOGE \
    --workload SMALL \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 60 \
    --blocksize 4096 \
    --wallets 10 \
    --transactions 10 \
    --interval 10.0 \
    --print 144 \
    --reward 10000 \
    --halving 0 \
    --years 10 \
    --export results/doge_small.json > results/doge_small.txt 2>&1

# MEMO - SMALL (10 years = 96,464,840 blocks)
echo "Running MEMO SMALL (10 years)..."
time python3 sim-blockchain.py \
    --chain MEMO \
    --workload SMALL \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 3.27 \
    --blocksize 32000 \
    --wallets 10 \
    --transactions 10 \
    --interval 10.0 \
    --print 144 \
    --reward 51.8457072 \
    --halving 9644000 \
    --years 10 \
    --export results/memo_small.json > results/memo_small.txt 2>&1

echo "SMALL workload simulations completed!"
echo "Results saved in results/ directory"
echo "Check individual .txt files for detailed output" 