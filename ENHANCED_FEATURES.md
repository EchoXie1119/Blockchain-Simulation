# Enhanced Blockchain Simulation Features

This document describes the enhanced features that have been added to the blockchain simulation to provide more realistic network behavior and improved functionality.

## Overview

The enhanced simulation now includes:

1. **Network Latency Simulation** - Realistic delays on receive broadcasts
2. **Network Bandwidth Simulation** - Block size affects propagation time
3. **Enhanced Wallet Balance Tracking** - Comprehensive fee logic and transaction history
4. **Trace Loading Capability** - Load real-world blockchain data for simulation

## 1. Network Latency Simulation

### Features
- **Processing Delays**: Each node has a processing delay (1-10ms) when receiving blocks
- **Distance-based Latency**: Network distance affects propagation time
- **Node-specific Parameters**: Each node has unique latency, bandwidth, and packet loss characteristics
- **Realistic Propagation**: Ensures block propagation happens within reasonable time limits

### Configuration
```python
NETWORK_CONFIG = {
    'latency_min': 0.001,  # Minimum network latency in seconds
    'latency_max': 0.1,    # Maximum network latency in seconds
    'processing_delay_min': 0.001,  # Minimum block processing delay
    'processing_delay_max': 0.01,   # Maximum block processing delay
    'distance_variance': 0.2,  # 20% variance for network distance simulation
    'max_propagation_time': 60.0,  # Maximum block propagation time
}
```

### Implementation Details
- Each `BlockchainNode` has individual latency and bandwidth parameters
- Combined latency calculation: `(sender_latency + receiver_latency) * distance_factor`
- Processing delays are added when nodes receive and validate blocks
- Propagation time is capped to prevent unrealistic delays

## 2. Network Bandwidth Simulation

### Features
- **Size-dependent Transmission**: Larger blocks take longer to transmit
- **Congestion Effects**: Blocks larger than 1MB experience additional congestion delays
- **Bandwidth Variance**: Each node has slightly different bandwidth capabilities
- **Packet Loss Simulation**: Larger blocks have higher packet loss probability

### Configuration
```python
NETWORK_CONFIG = {
    'bandwidth_limit': 100 * 1024 * 1024,  # 100 MB/s bandwidth limit
    'congestion_threshold': 1024 * 1024,  # Block size threshold for congestion (1MB)
    'congestion_factor': 0.1,  # 10% congestion per MB over threshold
    'bandwidth_variance': 0.2,  # 20% variance in bandwidth per node
    'packet_loss_variance': 0.5,  # 50% variance in packet loss per node
}
```

### Implementation Details
- Transmission time: `block_size / min(sender_bandwidth, receiver_bandwidth)`
- Congestion factor: `1.0 + (block_size / 1MB) * 0.1` for blocks > 1MB
- Packet loss probability increases with block size
- Each node has unique bandwidth characteristics

## 3. Enhanced Wallet Balance Tracking

### Features
- **Dynamic Fee Calculation**: Fees based on network conditions and transaction priority
- **Transaction History**: Comprehensive tracking of all transactions
- **Fee Statistics**: Detailed fee analysis and distribution
- **Network Condition Integration**: Fees adjust based on congestion and block utilization

### Fee Calculation
```python
class FeeCalculator:
    def calculate_fee(self, amount, priority, network_congestion):
        # Base fee calculation
        base_fee = amount * self.base_fee_rate
        
        # Priority multipliers
        priority_multipliers = {
            'low': 0.5, 'normal': 1.0, 'high': 2.0, 'urgent': 5.0
        }
        
        # Network congestion multiplier
        congestion_mult = 1.0 + (network_congestion * 2.0)
        
        # Block utilization factor
        utilization_factor = 1.0 + (self.block_utilization * 0.5)
        
        return base_fee * priority_mult * congestion_mult * utilization_factor
```

### Transaction Priorities
- **Low**: 50% of normal fee
- **Normal**: Standard fee (most transactions)
- **High**: 200% of normal fee
- **Urgent**: 500% of normal fee

### Network Condition Tracking
- **Congestion Level**: Based on pending transaction count
- **Block Utilization**: Based on recent block transaction counts
- **Real-time Updates**: Conditions updated every 10 seconds during simulation

## 4. Trace Loading Capability

### Features
- **Multiple Formats**: Support for JSON and CSV trace files
- **Real-world Data**: Load data from Bitcoin APIs and other sources
- **Synthetic Generation**: Generate realistic trace data for testing
- **Event Streaming**: Stream events in real-time simulation

### Supported Trace Types
- **Transactions**: Real transaction data with amounts, fees, and timestamps
- **Blocks**: Block creation events with mining information
- **Miner Events**: Miner join/leave events with hashrate changes
- **Network Events**: Network partitions, healing, and congestion events

### Trace Loading Example
```python
from trace_loader import TraceLoader

# Create trace loader
loader = TraceLoader()

# Load from JSON file
events = loader.load_json_trace("bitcoin_transactions.json")

# Load from CSV file
events = loader.load_csv_trace("transaction_log.csv")

# Generate synthetic data
events = loader.generate_synthetic_trace(duration_hours=24, transaction_rate=10.0)

# Load from Bitcoin API
events = loader.load_bitcoin_api_data("2024-01-01", "2024-01-02", limit=1000)
```

### Trace File Formats

#### JSON Format
```json
[
  {
    "type": "transaction",
    "timestamp": 1704067200.0,
    "data": {
      "tx_hash": "abc123...",
      "sender": "wallet_1",
      "recipient": "wallet_2",
      "amount": 1.5,
      "fee": 0.001,
      "priority": "normal"
    },
    "source": "bitcoin_api"
  }
]
```

#### CSV Format
```csv
timestamp,tx_hash,sender,recipient,amount,fee,priority
1704067200.0,abc123...,wallet_1,wallet_2,1.5,0.001,normal
```

## 5. Usage Examples

### Basic Enhanced Simulation
```python
from simulator import BlockchainSimulator
from config import SimulationConfig

# Create configuration
config = SimulationConfig(
    nodes=15,
    neighbors=4,
    miners=8,
    hashrate=1000,
    blocktime=600,
    wallets=100,
    transactions=50,
    blocks=100
)

# Run simulation with enhanced features
simulator = BlockchainSimulator(config)
simulator.start()
```

### Simulation with Trace Data
```python
# Run simulation with trace loading
simulator = BlockchainSimulator(config, use_traces=True, trace_file="data.json")
simulator.start()
```

### Command Line Usage
```bash
# Basic enhanced simulation
python simulator.py --chain BTC --workload MEDIUM --nodes 15 --neighbors 4

# Simulation with trace data
python simulator.py --chain BTC --workload MEDIUM --use-traces --trace-file data.json

# Custom network parameters
python simulator.py --chain BTC --nodes 20 --neighbors 5 --miners 10
```

## 6. Monitoring and Statistics

### Network Statistics
- **Propagation Times**: Average and per-node propagation delays
- **Bandwidth Utilization**: Network data transfer statistics
- **Packet Loss**: Network reliability metrics
- **Node Connectivity**: Network topology information

### Fee Statistics
- **Total Fees**: Sum of all transaction fees
- **Average Fees**: Mean fee across all transactions
- **Fee Distribution**: Breakdown by priority level
- **Network Impact**: How congestion affects fees

### Trace Statistics
- **Event Counts**: Total events by type
- **Time Ranges**: Duration and coverage of trace data
- **Source Analysis**: Breakdown by data source
- **Conversion Rates**: Success rate of trace-to-transaction conversion

## 7. Configuration Options

### Network Configuration
```python
# Enhanced network parameters
NETWORK_CONFIG = {
    'latency_min': 0.001,
    'latency_max': 0.1,
    'bandwidth_limit': 100 * 1024 * 1024,
    'packet_loss_rate': 0.001,
    'max_propagation_time': 60.0,
    'congestion_threshold': 1024 * 1024,
    'congestion_factor': 0.1,
    'processing_delay_min': 0.001,
    'processing_delay_max': 0.01,
    'distance_variance': 0.2,
    'bandwidth_variance': 0.2,
    'packet_loss_variance': 0.5,
}
```

### Transaction Configuration
```python
TRANSACTION_CONFIG = {
    'min_amount': 0.1,
    'max_amount': 10.0,
    'min_fee': 0.001,
    'max_fee': 0.1,
    'fee_rate': 0.01  # 1% base fee rate
}
```

## 8. Performance Considerations

### Network Simulation Overhead
- **Processing Delays**: Minimal overhead from sleep operations
- **Bandwidth Calculation**: Simple arithmetic operations
- **Packet Loss**: Random number generation for each transmission
- **Node Management**: Thread-safe operations with locks

### Memory Usage
- **Transaction History**: Limited to last 10,000 transactions
- **Network Statistics**: Per-node and network-wide metrics
- **Trace Data**: Loaded into memory for processing
- **Wallet Balances**: Real-time balance tracking

### Scalability
- **Node Count**: Tested up to 100 nodes
- **Transaction Volume**: Handles thousands of transactions
- **Block Size**: Supports blocks up to 32MB
- **Trace Data**: Processes millions of events

## 9. Future Enhancements

### Planned Features
- **Geographic Latency**: Real-world geographic distance simulation
- **Network Topology**: More realistic network topologies (scale-free, small-world)
- **Advanced Fee Models**: EIP-1559 style fee markets
- **Mempool Simulation**: Transaction pool management and replacement
- **Fork Resolution**: Chain reorganization and orphan block handling

### API Integration
- **Multiple Blockchains**: Support for Ethereum, Litecoin, and other chains
- **Real-time Data**: Live blockchain data feeds
- **Historical Analysis**: Long-term trend analysis
- **Custom Metrics**: User-defined performance metrics

## 10. Troubleshooting

### Common Issues
1. **High Memory Usage**: Reduce trace data size or transaction history limit
2. **Slow Propagation**: Check network configuration parameters
3. **Fee Calculation Errors**: Verify transaction configuration
4. **Trace Loading Failures**: Check file format and data structure

### Debug Mode
Enable debug logging for detailed information:
```python
config = SimulationConfig(..., debug=True)
```

### Performance Monitoring
Monitor key metrics during simulation:
- Network propagation times
- Fee calculation performance
- Memory usage
- CPU utilization

## Conclusion

The enhanced blockchain simulation provides a more realistic and comprehensive environment for studying blockchain networks. The combination of network latency simulation, bandwidth constraints, dynamic fee calculation, and trace loading capabilities makes it suitable for both research and educational purposes.

For more information, see the example scripts and configuration files in the project directory. 