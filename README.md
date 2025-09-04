# Blockchain Simulation Project

## Overview

This project implements a comprehensive blockchain simulation system for CS595 Summer 2025 - PROJECT#2. The simulation models various aspects of blockchain networks including mining, transaction processing, network propagation, and wallet management.

## Features

### 🏗️ **Network & Blocks**
- **Peer Nodes**: Create N peer nodes, each maintaining a set of stored block IDs
- **Network Topology**: Randomly connect each node to M distinct peers
- **Block Structure**: Each block has a header (1,024 bytes) + (# transactions × 256 bytes)
- **Block Propagation**: When a node stores a new block, it broadcasts to neighbors
- **Network Statistics**: Track I/O requests and network data transfer
- **Network Latency & Bandwidth**: Simulated network delays and bandwidth limitations

### ⛏️ **Mining & Difficulty**
- **Multiple Miners**: Spawn K miner processes, each with hashrate H
- **Exponential Mining Time**: Expected time per block ~ Exp(total_hashrate / difficulty)
- **Difficulty Adjustment**: After every 2,016 blocks, retarget based on actual vs target block time
- **Halving & Coin Issuance**: Issue R coins per block, halve every H blocks (default 210,000)

### 💰 **Transactions & Wallets**
- **Wallet Management**: Generate W wallet processes
- **Transaction Generation**: Each wallet sends X transactions at interval I seconds
- **Block Filling**: Include up to B transactions from pool (FIFO) plus mining reward
- **Balance Tracking**: Monitor wallet balances and transaction history
- **Fee Logic**: Transaction fees are included and tracked

### 📊 **Reporting & Monitoring**
- **Real-time Statistics**: Print summaries every P blocks (default 144)
- **Comprehensive Metrics**: Track blocks, transactions, coins, network data, I/O requests
- **Debug Mode**: Print every block with --debug flag
- **Export Results**: Save simulation results to JSON files

## Project Structure

```
proj2-xie/
├── sim-blockchain.py      # Main entry point
├── config.py              # Configuration and constants
├── models.py              # Data structures and models
├── network.py             # Network management and propagation
├── mining.py              # Mining operations and difficulty adjustment
├── wallet.py              # Wallet management and transaction generation
├── simulator.py           # Main simulation orchestrator
├── README.md              # This file
└── requirements.txt       # Python dependencies
```

### Module Descriptions

#### `config.py`
- **Purpose**: Centralized configuration management
- **Contains**: Blockchain configurations, workload settings, constants
- **Key Features**: Predefined configurations for BTC, BCH, LTC, DOGE, MEMO

#### `models.py`
- **Purpose**: Data structures and models
- **Contains**: Block, Transaction, Wallet, and statistics classes
- **Key Features**: Comprehensive data models with serialization support

#### `network.py`
- **Purpose**: Network simulation and block propagation
- **Contains**: BlockchainNode, NetworkManager classes
- **Key Features**: Network latency, bandwidth simulation, packet loss

#### `mining.py`
- **Purpose**: Mining operations and difficulty management
- **Contains**: Miner, MiningManager classes
- **Key Features**: Multi-threaded mining, difficulty adjustment, halving

#### `wallet.py`
- **Purpose**: Wallet management and transaction generation
- **Contains**: WalletManager class
- **Key Features**: Balance tracking, transaction generation, fee handling

#### `simulator.py`
- **Purpose**: Main simulation orchestrator
- **Contains**: BlockchainSimulator class
- **Key Features**: Coordinates all components, manages simulation lifecycle

## Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Setup
```bash
# Navigate to the project directory
cd proj2-xie

# Make the script executable if you have permission issues
chmod +x sim-blockchain.py

# Test the installation
python3 sim-blockchain.py --help
```

## Usage

### Command-Line Interface

The simulator supports the following command-line arguments as specified in the project requirements:

#### **Network & Blocks**
- `--nodes N`: Create N peer nodes, each maintaining a set of stored block IDs
- `--neighbors M`: Randomly connect each node to M distinct peers

#### **Mining & Difficulty**
- `--miners K`: Spawn K miner processes
- `--hashrate H`: Each miner has hashrate H
- `--blocktime T`: Target block time in seconds
- `--difficulty D`: Custom difficulty setting (optional)
- `--reward R`: Issue R coins per block (default 50)
- `--halving H`: Halve reward every H blocks (default 210000)

#### **Transactions & Wallets**
- `--wallets W`: Generate W wallet processes
- `--transactions X`: Each wallet sends X transactions
- `--interval I`: Transaction generation interval in seconds
- `--blocksize B`: Include up to B transactions from pool (FIFO)

#### **Simulation Control**
- `--blocks L`: Run until L blocks have been mined or until all txs are processed
- `--years Y`: Simulation duration in years (alternative to --blocks)
- `--print P`: Print summary every P blocks (default 144)
- `--debug`: Enable debug mode (print every block)

#### **Output & Export**
- `--export FILE`: Export results to JSON file
- `--output FILE`: Output file for results (alias for --export)

### Basic Usage Examples

```bash
# Run with default settings (BTC, no transactions)
python3 sim-blockchain.py

# Run with custom parameters
python3 sim-blockchain.py --nodes 10 --miners 5 --blocks 100

# Run with transaction workload
python3 sim-blockchain.py --wallets 10 --transactions 100 --interval 1.0

# Run with specific blockchain configuration
python3 sim-blockchain.py --chain BTC --workload SMALL --years 1

# Run with debug mode
python3 sim-blockchain.py --debug --blocks 10

# Export results
python3 sim-blockchain.py --export results/output.json
```

## Required Workloads (Project Requirements)

### 2.5 Workloads to Evaluate - 10 Year Simulations

This section provides all necessary commands to run blockchain simulations for 10 years with different workloads as required for CS595 Project #2.

#### Simulation Parameters

**Default Parameters (explicitly specified):**
- `--nodes 10`: 10 peer nodes in the network
- `--neighbors 3`: 3 neighbors per node
- `--miners 5`: 5 miner processes
- `--hashrate 1000`: 1000 hashes per second per miner
- `--print 144`: Print summary every 144 blocks (default)

**Blockchain-Specific Parameters (auto-configured):**
Each blockchain has its own configuration that is automatically applied:

| Blockchain | Block Time | Reward | Halving | Max TX/Block |
|------------|------------|--------|---------|--------------|
| BTC        | 600s       | 50     | 210000  | 4000         |
| BCH        | 600s       | 12.5   | 210000  | 128000       |
| LTC        | 150s       | 50     | 840000  | 4000         |
| DOGE       | 60s        | 10000  | None    | 4000         |
| MEMO       | 3.27s      | 51.8457072 | 9644000 | 32000    |

**Workload Types:**
- **NONE**: No user transactions (mining only)
- **SMALL**: 10 wallets, 10 transactions each, 10.0s interval
- **MEDIUM**: 1000 wallets, 1000 transactions each, 1.0s interval  
- **LARGE**: 1000 wallets, 1000 transactions each, 0.01s interval

#### 1. NONE Workload (No User Transactions)

**Bitcoin (BTC)**
```bash
python3 sim-blockchain.py --chain BTC --workload NONE --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/btc_none.json
```

**Bitcoin Cash (BCH)**
```bash
python3 sim-blockchain.py --chain BCH --workload NONE --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/bch_none.json
```

**Litecoin (LTC)**
```bash
python3 sim-blockchain.py --chain LTC --workload NONE --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/ltc_none.json
```

**Dogecoin (DOGE)**
```bash
python3 sim-blockchain.py --chain DOGE --workload NONE --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/doge_none.json
```

**MEMO**
```bash
python3 sim-blockchain.py --chain MEMO --workload NONE --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/memo_none.json
```

#### 2. SMALL Workload (10 wallets, 10 transactions each, 10.0s interval)

**Bitcoin (BTC)**
```bash
python3 sim-blockchain.py --chain BTC --workload SMALL --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/btc_small.json
```

**Bitcoin Cash (BCH)**
```bash
python3 sim-blockchain.py --chain BCH --workload SMALL --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/bch_small.json
```

**Litecoin (LTC)**
```bash
python3 sim-blockchain.py --chain LTC --workload SMALL --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/ltc_small.json
```

**Dogecoin (DOGE)**
```bash
python3 sim-blockchain.py --chain DOGE --workload SMALL --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/doge_small.json
```

**MEMO**
```bash
python3 sim-blockchain.py --chain MEMO --workload SMALL --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/memo_small.json
```

#### 3. MEDIUM Workload (1000 wallets, 1000 transactions each, 1.0s interval)

**Bitcoin (BTC)**
```bash
python3 sim-blockchain.py --chain BTC --workload MEDIUM --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/btc_medium.json
```

**Bitcoin Cash (BCH)**
```bash
python3 sim-blockchain.py --chain BCH --workload MEDIUM --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/bch_medium.json
```

**Litecoin (LTC)**
```bash
python3 sim-blockchain.py --chain LTC --workload MEDIUM --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/ltc_medium.json
```

**Dogecoin (DOGE)**
```bash
python3 sim-blockchain.py --chain DOGE --workload MEDIUM --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/doge_medium.json
```

**MEMO**
```bash
python3 sim-blockchain.py --chain MEMO --workload MEDIUM --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/memo_medium.json
```

#### 4. LARGE Workload (1000 wallets, 1000 transactions each, 0.01s interval)

**Bitcoin (BTC)**
```bash
python3 sim-blockchain.py --chain BTC --workload LARGE --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/btc_large.json
```

**Bitcoin Cash (BCH)**
```bash
python3 sim-blockchain.py --chain BCH --workload LARGE --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/bch_large.json
```

**Litecoin (LTC)**
```bash
python3 sim-blockchain.py --chain LTC --workload LARGE --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/ltc_large.json
```

**Dogecoin (DOGE)**
```bash
python3 sim-blockchain.py --chain DOGE --workload LARGE --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/doge_large.json
```

**MEMO**
```bash
python3 sim-blockchain.py --chain MEMO --workload LARGE --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/memo_large.json
```

#### Running All Simulations

**Option 1: Use the Shell Scripts**
```bash
# Run NONE workload simulations
chmod +x run_simulations_none.sh
./run_simulations_none.sh

# Run SMALL workload simulations
chmod +x run_simulations_small.sh
./run_simulations_small.sh

# Run MEDIUM workload simulations
chmod +x run_simulations_medium.sh
./run_simulations_medium.sh

# Run LARGE workload simulations
chmod +x run_simulations_large.sh
./run_simulations_large.sh
```

**Option 2: Run All Blockchains with One Workload Type**
```bash
# Run all blockchains with NONE workload
python3 sim-blockchain.py --chain ALL --workload NONE --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/all_none.json

# Run all blockchains with SMALL workload
python3 sim-blockchain.py --chain ALL --workload SMALL --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/all_small.json

# Run all blockchains with MEDIUM workload
python3 sim-blockchain.py --chain ALL --workload MEDIUM --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/all_medium.json

# Run all blockchains with LARGE workload
python3 sim-blockchain.py --chain ALL --workload LARGE --nodes 10 --neighbors 3 --miners 5 --hashrate 1000 --print 144 --years 10 --export results/all_large.json
```

#### Expected Blocks per Year

Based on block times, here's how many blocks each blockchain will generate in 10 years:

| Blockchain | Block Time | Blocks per Year | Blocks per 10 Years |
|------------|------------|-----------------|---------------------|
| BTC        | 600s       | 52,560          | 525,600             |
| BCH        | 600s       | 52,560          | 525,600             |
| LTC        | 150s       | 210,240         | 2,102,400           |
| DOGE       | 60s        | 525,600         | 5,256,000           |
| MEMO       | 3.27s      | 9,646,484       | 96,464,840          |

#### Performance Notes

- **NONE workload**: Fastest, only mining operations (5-30 minutes per blockchain)
- **SMALL workload**: Moderate, 100 total transactions (10-60 minutes per blockchain)
- **MEDIUM workload**: Slower, 1 million transactions (30-180 minutes per blockchain)
- **LARGE workload**: Slowest, 1 million transactions with high frequency (60-360 minutes per blockchain)

**Total**: 20 simulations (5 blockchains × 4 workloads)
**Duration**: 10 years each simulation
**Output**: JSON files with detailed results in `results/` directory

#### Results Analysis

After running all simulations, you can analyze the JSON output files to compare:
- Total coins created
- Simulation time taken
- Transaction throughput
- Network performance
- Mining efficiency

## Blockchain Configurations

| Chain | Block Reward | Halving Schedule | Block Time | Block Size Limit | Max TX per Block |
|-------|-------------|------------------|------------|------------------|------------------|
| Bitcoin (BTC) | 50 BTC | 210K blocks | 600 sec | 1 MB base | 4K TX |
| Bitcoin Cash (BCH) | 12.5 BCH | 210K blocks | 600 sec | 32 MB | 128K TX |
| Litecoin (LTC) | 50 LTC | 840K blocks | 150 sec | 1 MB | 4K TX |
| Dogecoin (DOGE) | 10,000 DOGE | None (static) | 60 sec | 1 MB | 4K TX |
| MEMO | 51.8457072 MEMO | 9644K blocks | 3.27 sec | 8 MB | 32K TX |

## Output Format

### Real-time Summary
```
[timestamp] Sum B:blocks/totalBlocks complete% abt:avg_block_time(s) tps:confirmed_tx_per_sec infl:inflation% ETA:seconds Diff:difficulty Hash:block_hash Tx:total_tx C:coins Pool:pending_tx NMB:network_MB IO:io_requests
```

### Final Summary
```
[******] End B:blocks abt:avg_block_time(s) tps:confirmed_tx_per_sec Tx:total_tx C:coins NMB:network_MB IO:io_requests
```

### Example Output
```
[1703123456.7] Sum B:144/52560 complete%27.4 abt:600.12s tps:6.67 infl:100.00% ETA:315072.0s Diff:3000000.00 Hash:a1b2c3d4 Tx:576000 C:7200.00 Pool:0 NMB:1.23 IO:432
[******] End B:52560 abt:600.15s tps:6.66 Tx:210240000 C:2628000.00 NMB:450.67 IO:157680
```

## Requirements Implementation Status

### ✅ **Fully Implemented**

#### 2.1 Network & Blocks
- ✅ Nodes (--nodes N): Create N peer nodes, each maintaining a set of stored block IDs
- ✅ Randomly connect each node to --neighbors M distinct peers
- ✅ Block structure: Each block has a header (1,024 bytes) + (# transactions × 256 bytes)
- ✅ Track block ID, timestamp, time-since-last-block, transaction count, and size
- ✅ Block propagation: When a node stores a new block, it broadcasts it to neighbors
- ✅ Increment global io_requests counter per send; add block size to network_data
- ✅ Ignore duplicates

#### 2.2 Mining & Difficulty
- ✅ Miners (--miners K, --hashrate H): Spawn K miner processes, each with hashrate H
- ✅ Expected time per block ∼ Exp(total_hashrate / difficulty)
- ✅ Difficulty (--blocktime T, --difficulty D optional): If D not set, initialize to T × (K × H)
- ✅ After every 2,016 blocks, retarget: new_diff = old_diff × (target_blocktime / actual_avg_blocktime)
- ✅ Halving & coin issuance (--reward R, default 50): Issue R coins per block
- ✅ Every --halving H blocks (default 210000), halve the reward
- ✅ After 35 halvings, reward → 0

#### 2.3 Transactions & Wallets
- ✅ Wallets (--wallets W, --transactions X, --interval I): Generate W wallet processes
- ✅ Each sends X transactions into a global unconfirmed-pool at interval I seconds
- ✅ Block filling: On block creation, include up to --blocksize B transactions from the pool (FIFO)
- ✅ Plus the mining reward transaction
- ✅ Termination: If --blocks L is specified, run until L blocks have been mined
- ✅ If --blocks omitted, run until all wallet transactions have been confirmed

#### 2.4 Reporting & CLI Options
- ✅ --print P (default 144): Print a summary every P blocks
- ✅ With --debug, print every block
- ✅ Summaries include all required metrics: time, blocks, completion%, avg_block_time, tps, inflation%, ETA, difficulty, hash, transactions, coins, pool, network_MB, io_requests
- ✅ Final summary with all required metrics

#### 2.5 Workloads to Evaluate
- ✅ Run BTC, BCH, LTC, DOGE, and MEMO for 10 years with no user transactions
- ✅ Report the number of coins created and simulation time taken
- ✅ Run with SMALL, MEDIUM, and LARGE workloads
- ✅ Support for running multiple simulations simultaneously

### 🎯 **Extra Credit Features Implemented**

#### Network Simulation
- ✅ Simulate network latency by adding delays on receive broadcasts
- ✅ Ensure that block propagation happens within the blocktime
- ✅ Simulate network bandwidth by taking into account block size
- ✅ Simulating larger block sizes takes longer to propagate

#### Advanced Features
- ✅ Track per-wallet balances and include fee logic
- ✅ Comprehensive transaction fee handling
- ✅ Network partition simulation capabilities
- ✅ Miner join/leave simulation

## Performance Considerations

### Simulation Time Estimates
- **10-year simulations** may take 10-60 minutes depending on blockchain configuration
- **MEMO simulations** (3.27s block time) will be fastest
- **Bitcoin simulations** (600s block time) will take longest
- **Large workloads** (1000 wallets × 1000 transactions) may take 30-120 minutes

### Resource Usage
- **Memory**: ~100MB for small simulations, ~1GB for large workloads
- **CPU**: Single-threaded simulation, can run multiple instances simultaneously
- **Storage**: Log files and export files may grow to several MB

### Optimization Tips
- Use `--debug` only for small simulations
- Run multiple simulations in parallel on different CPU cores
- Use `--export` to save results for later analysis
- Monitor system resources during large simulations

## Troubleshooting

### Common Issues

1. **Simulation takes too long**: 
   - Check if difficulty is too high relative to hashrate
   - Use smaller block counts for testing
   - Consider using faster blockchains (MEMO, DOGE) for quick tests

2. **Memory issues with large workloads**:
   - Reduce number of wallets or transactions
   - Use smaller block sizes
   - Monitor system memory usage

3. **Network propagation issues**:
   - Check if network latency is too high
   - Verify node connectivity
   - Use debug mode to trace block propagation

### Debug Mode
Use `--debug` flag for detailed logging:
```bash
python3 sim-blockchain.py --debug --blocks 10
```

### Log Files
Simulation logs are saved to `blockchain_simulation.log` for detailed debugging.

## Contributing

1. Follow the modular architecture
2. Add comprehensive logging
3. Include unit tests for new features
4. Update documentation
5. Maintain backward compatibility

## License

This project is part of CS595 Summer 2025 - PROJECT#2.

## Contact

For questions or issues, please refer to the course materials or contact the instructor.

## Quick Verification Workloads (Very Fast Test)

The following commands are designed for **very fast testing and verification**. Each command uses high hashrate, low blocktime, and a 1-year simulation window so you can quickly check that all features work. Each simulation's output is saved to a separate file in the `results/` directory.

**All commands use:**
- `--miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100`
- `--print 1 --reward 1000 --halving 10000 --years 1`
- `--export results/...json > results/...txt 2>&1` (output and logs)
- Use `time` to measure real runtime

### NONE Workload (No User Transactions)
```bash
# BTC - NONE
mkdir -p results
time python3 sim-blockchain.py --chain BTC --workload NONE --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 0 --transactions 0 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/btc_none.json > results/btc_none.txt 2>&1

# BCH - NONE
time python3 sim-blockchain.py --chain BCH --workload NONE --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 0 --transactions 0 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/bch_none.json > results/bch_none.txt 2>&1

# LTC - NONE
time python3 sim-blockchain.py --chain LTC --workload NONE --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 0 --transactions 0 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/ltc_none.json > results/ltc_none.txt 2>&1

# DOGE - NONE
time python3 sim-blockchain.py --chain DOGE --workload NONE --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 0 --transactions 0 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/doge_none.json > results/doge_none.txt 2>&1

# MEMO - NONE
time python3 sim-blockchain.py --chain MEMO --workload NONE --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 0 --transactions 0 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/memo_none.json > results/memo_none.txt 2>&1
```

### SMALL Workload (10 wallets, 10 transactions each)
```bash
# BTC - SMALL
time python3 sim-blockchain.py --chain BTC --workload SMALL --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 10 --transactions 10 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/btc_small.json > results/btc_small.txt 2>&1

# BCH - SMALL
time python3 sim-blockchain.py --chain BCH --workload SMALL --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 10 --transactions 10 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/bch_small.json > results/bch_small.txt 2>&1

# LTC - SMALL
time python3 sim-blockchain.py --chain LTC --workload SMALL --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 10 --transactions 10 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/ltc_small.json > results/ltc_small.txt 2>&1

# DOGE - SMALL
time python3 sim-blockchain.py --chain DOGE --workload SMALL --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 10 --transactions 10 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/doge_small.json > results/doge_small.txt 2>&1

# MEMO - SMALL
time python3 sim-blockchain.py --chain MEMO --workload SMALL --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 10 --transactions 10 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/memo_small.json > results/memo_small.txt 2>&1
```

### MEDIUM Workload (1000 wallets, 1000 transactions each)
```bash
# BTC - MEDIUM
time python3 sim-blockchain.py --chain BTC --workload MEDIUM --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 1000 --transactions 1000 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/btc_medium.json > results/btc_medium.txt 2>&1

# BCH - MEDIUM
time python3 sim-blockchain.py --chain BCH --workload MEDIUM --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 1000 --transactions 1000 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/bch_medium.json > results/bch_medium.txt 2>&1

# LTC - MEDIUM
time python3 sim-blockchain.py --chain LTC --workload MEDIUM --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 1000 --transactions 1000 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/ltc_medium.json > results/ltc_medium.txt 2>&1

# DOGE - MEDIUM
time python3 sim-blockchain.py --chain DOGE --workload MEDIUM --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 1000 --transactions 1000 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/doge_medium.json > results/doge_medium.txt 2>&1

# MEMO - MEDIUM
time python3 sim-blockchain.py --chain MEMO --workload MEDIUM --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 1000 --transactions 1000 --interval 1.0 --print 1 --reward 1000 --halving 10000 --years 1 --export results/memo_medium.json > results/memo_medium.txt 2>&1
```

### LARGE Workload (1000 wallets, 1000 transactions each, 0.01s interval)
```bash
# BTC - LARGE
time python3 sim-blockchain.py --chain BTC --workload LARGE --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 1000 --transactions 1000 --interval 0.01 --print 1 --reward 1000 --halving 10000 --years 1 --export results/btc_large.json > results/btc_large.txt 2>&1

# BCH - LARGE
time python3 sim-blockchain.py --chain BCH --workload LARGE --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 1000 --transactions 1000 --interval 0.01 --print 1 --reward 1000 --halving 10000 --years 1 --export results/bch_large.json > results/bch_large.txt 2>&1

# LTC - LARGE
time python3 sim-blockchain.py --chain LTC --workload LARGE --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 1000 --transactions 1000 --interval 0.01 --print 1 --reward 1000 --halving 10000 --years 1 --export results/ltc_large.json > results/ltc_large.txt 2>&1

# DOGE - LARGE
time python3 sim-blockchain.py --chain DOGE --workload LARGE --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 1000 --transactions 1000 --interval 0.01 --print 1 --reward 1000 --halving 10000 --years 1 --export results/doge_large.json > results/doge_large.txt 2>&1

# MEMO - LARGE
time python3 sim-blockchain.py --chain MEMO --workload LARGE --miners 5 --hashrate 1e8 --nodes 2 --neighbors 1 --blocktime 10 --blocksize 100 --wallets 1000 --transactions 1000 --interval 0.01 --print 1 --reward 1000 --halving 10000 --years 1 --export results/memo_large.json > results/memo_large.txt 2>&1
```

**Note:** These settings are for quick verification only. For real experiments, use realistic parameters as described in the project requirements. 
