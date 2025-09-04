#!/usr/bin/env python3
"""
Example script demonstrating enhanced blockchain simulation features

This script shows:
1. Network latency simulation with delays on receive broadcasts
2. Network bandwidth simulation based on block size
3. Enhanced wallet balance tracking with dynamic fee logic
4. Trace loading from real-world data
"""

import time
import json
from simulator import BlockchainSimulator
from config import SimulationConfig, BLOCKCHAIN_CONFIGS, WORKLOAD_CONFIGS
from trace_loader import TraceLoader

def demonstrate_enhanced_network_simulation():
    """Demonstrate enhanced network simulation features"""
    print("=" * 60)
    print("ENHANCED NETWORK SIMULATION DEMONSTRATION")
    print("=" * 60)
    
    # Create configuration for Bitcoin with medium workload
    config = SimulationConfig(
        nodes=15,  # More nodes for better network simulation
        neighbors=4,  # More neighbors per node
        miners=8,
        hashrate=1000,
        blocktime=600,  # Bitcoin block time
        difficulty=600 * 8 * 1000,  # blocktime * miners * hashrate
        reward=50,
        halving=210000,
        wallets=100,  # Medium workload
        transactions=50,
        interval=2.0,
        blocksize=4000,
        blocks=100,  # Simulate 100 blocks
        years=1.0,
        print_interval=10,
        debug=False
    )
    
    # Create simulator with enhanced features
    simulator = BlockchainSimulator(config, use_traces=False)
    
    print("Starting enhanced network simulation...")
    print("Features enabled:")
    print("- Network latency simulation with processing delays")
    print("- Bandwidth simulation based on block size")
    print("- Dynamic fee calculation based on network conditions")
    print("- Enhanced wallet balance tracking")
    print("- Network congestion monitoring")
    
    try:
        simulator.start()
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
    finally:
        simulator.stop()
        
    return simulator.get_simulation_stats()

def demonstrate_trace_loading():
    """Demonstrate trace loading capabilities"""
    print("\n" + "=" * 60)
    print("TRACE LOADING DEMONSTRATION")
    print("=" * 60)
    
    # Create trace loader
    trace_loader = TraceLoader()
    
    # Generate synthetic trace data
    print("Generating synthetic trace data...")
    synthetic_events = trace_loader.generate_synthetic_trace(
        duration_hours=1,  # 1 hour of data
        transaction_rate=5.0  # 5 transactions per second
    )
    
    # Save trace to file
    trace_filename = "example_trace.json"
    trace_loader.save_trace(synthetic_events, trace_filename)
    print(f"Saved {len(synthetic_events)} events to {trace_filename}")
    
    # Load trace back
    print("Loading trace data...")
    loaded_events = trace_loader.load_json_trace(trace_filename)
    print(f"Loaded {len(loaded_events)} events from {trace_filename}")
    
    # Show trace statistics
    stats = trace_loader.get_trace_statistics()
    print(f"Trace statistics: {stats}")
    
    # Convert some events to transactions
    transactions = []
    for event in loaded_events[:10]:  # First 10 events
        tx = trace_loader.convert_to_transaction(event)
        if tx:
            transactions.append(tx)
            print(f"Converted transaction: {tx.tx_id} ({tx.amount:.6f} + {tx.fee:.6f} fee)")
    
    return trace_loader

def demonstrate_dynamic_fees():
    """Demonstrate dynamic fee calculation"""
    print("\n" + "=" * 60)
    print("DYNAMIC FEE CALCULATION DEMONSTRATION")
    print("=" * 60)
    
    from wallet import FeeCalculator
    
    # Create fee calculator
    fee_calc = FeeCalculator()
    
    # Test fee calculation with different conditions
    test_amount = 1.0  # 1 coin transaction
    test_priorities = ['low', 'normal', 'high', 'urgent']
    
    print("Fee calculation for 1.0 coin transaction:")
    print("-" * 50)
    
    for priority in test_priorities:
        # Test different network congestion levels
        for congestion in [0.0, 0.25, 0.5, 0.75, 1.0]:
            fee = fee_calc.calculate_fee(test_amount, priority, congestion)
            print(f"Priority: {priority:8} | Congestion: {congestion*100:3.0f}% | Fee: {fee:.6f}")
        print()
    
    # Get fee estimates
    print("Fee estimates for different network conditions:")
    estimates = fee_calc.get_fee_estimate(test_amount, 'normal')
    for condition, fee in estimates.items():
        print(f"  {condition}: {fee:.6f}")

def demonstrate_network_conditions():
    """Demonstrate network condition monitoring"""
    print("\n" + "=" * 60)
    print("NETWORK CONDITION MONITORING DEMONSTRATION")
    print("=" * 60)
    
    # Create a simple simulation to show network conditions
    config = SimulationConfig(
        nodes=10,
        neighbors=3,
        miners=5,
        hashrate=1000,
        blocktime=600,
        difficulty=600 * 5 * 1000,
        reward=50,
        halving=210000,
        wallets=50,
        transactions=20,
        interval=1.0,
        blocksize=2000,
        blocks=20,  # Just 20 blocks for quick demo
        years=1.0,
        print_interval=5,
        debug=False
    )
    
    simulator = BlockchainSimulator(config)
    
    print("Running simulation to demonstrate network condition monitoring...")
    print("Network conditions will be updated every 10 seconds during simulation.")
    
    try:
        simulator.start()
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
    finally:
        simulator.stop()
        
    # Show final network conditions
    final_stats = simulator.get_simulation_stats()
    network_stats = final_stats['network_stats']
    
    print("\nFinal Network Conditions:")
    print(f"  Total nodes: {network_stats['node_count']}")
    print(f"  Total connections: {network_stats['total_connections']}")
    print(f"  Average neighbors: {network_stats['average_neighbors']:.1f}")
    print(f"  Total blocks stored: {network_stats['total_blocks_stored']}")
    print(f"  Average propagation time: {network_stats['network_stats']['average_propagation_time']:.3f}s")
    print(f"  Total network data: {network_stats['network_stats']['total_network_data'] / (1024*1024):.1f} MB")

def main():
    """Main demonstration function"""
    print("BLOCKCHAIN SIMULATION ENHANCED FEATURES DEMONSTRATION")
    print("=" * 80)
    
    try:
        # Demonstrate enhanced network simulation
        network_stats = demonstrate_enhanced_network_simulation()
        
        # Demonstrate trace loading
        trace_loader = demonstrate_trace_loading()
        
        # Demonstrate dynamic fees
        demonstrate_dynamic_fees()
        
        # Demonstrate network condition monitoring
        demonstrate_network_conditions()
        
        print("\n" + "=" * 80)
        print("DEMONSTRATION COMPLETE")
        print("=" * 80)
        print("\nEnhanced features demonstrated:")
        print("✓ Network latency simulation with processing delays")
        print("✓ Bandwidth simulation based on block size")
        print("✓ Dynamic fee calculation based on network conditions")
        print("✓ Enhanced wallet balance tracking")
        print("✓ Network congestion monitoring")
        print("✓ Trace loading from various sources")
        print("✓ Real-time network condition updates")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 