#!/bin/bash

# Blockchain Simulation Commands - LARGE Workload Only
# Run this in one terminal for LARGE workload simulations
# CS595 Summer 2025 - PROJECT#2
# LARGE: 1000 wallets with 1000 transactions each generated with interval of 0.01

mkdir -p results

echo "Starting LARGE workload simulations for 10 years..."

# =====================
# LARGE workload (1000 wallets, 1000 transactions each, 0.01s interval)
# =====================

# BTC - LARGE (10 years = 525,600 blocks)
echo "Running BTC LARGE (10 years)..."
time python3 sim-blockchain.py \
    --chain BTC \
    --workload LARGE \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 600 \
    --blocksize 4096 \
    --wallets 1000 \
    --transactions 1000 \
    --interval 0.01 \
    --print 144 \
    --reward 50 \
    --halving 210000 \
    --years 10 \
    --export results/btc_large.json > results/btc_large.txt 2>&1

# BCH - LARGE (10 years = 525,600 blocks)
echo "Running BCH LARGE (10 years)..."
time python3 sim-blockchain.py \
    --chain BCH \
    --workload LARGE \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 600 \
    --blocksize 128000 \
    --wallets 1000 \
    --transactions 1000 \
    --interval 0.01 \
    --print 144 \
    --reward 12.5 \
    --halving 210000 \
    --years 10 \
    --export results/bch_large.json > results/bch_large.txt 2>&1

# LTC - LARGE (10 years = 2,102,400 blocks)
echo "Running LTC LARGE (10 years)..."
time python3 sim-blockchain.py \
    --chain LTC \
    --workload LARGE \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 150 \
    --blocksize 4096 \
    --wallets 1000 \
    --transactions 1000 \
    --interval 0.01 \
    --print 144 \
    --reward 50 \
    --halving 840000 \
    --years 10 \
    --export results/ltc_large.json > results/ltc_large.txt 2>&1

# DOGE - LARGE (10 years = 5,256,000 blocks)
echo "Running DOGE LARGE (10 years)..."
time python3 sim-blockchain.py \
    --chain DOGE \
    --workload LARGE \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 60 \
    --blocksize 4096 \
    --wallets 1000 \
    --transactions 1000 \
    --interval 0.01 \
    --print 144 \
    --reward 10000 \
    --halving 0 \
    --years 10 \
    --export results/doge_large.json > results/doge_large.txt 2>&1

# MEMO - LARGE (10 years = 96,464,840 blocks)
echo "Running MEMO LARGE (10 years)..."
time python3 sim-blockchain.py \
    --chain MEMO \
    --workload LARGE \
    --nodes 10 \
    --neighbors 3 \
    --miners 5 \
    --hashrate 1000 \
    --blocktime 3.27 \
    --blocksize 32000 \
    --wallets 1000 \
    --transactions 1000 \
    --interval 0.01 \
    --print 144 \
    --reward 51.8457072 \
    --halving 9644000 \
    --years 10 \
    --export results/memo_large.json > results/memo_large.txt 2>&1

echo "LARGE workload simulations completed!"
echo "Results saved in results/ directory"
echo "Check individual .txt files for detailed output" 