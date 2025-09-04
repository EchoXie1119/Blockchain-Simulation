#!/usr/bin/env python3
"""
Performance test script for blockchain simulation
Tests the optimized simulation with a small workload
"""

import time
import subprocess
import sys

def test_simulation_performance():
    """Test the performance of the optimized simulation"""
    
    # Test command with reasonable parameters
    cmd = [
        "python3", "sim-blockchain.py",
        "--miners", "2",
        "--hashrate", "1e6", 
        "--nodes", "2",
        "--neighbors", "1",
        "--blocktime", "600",
        "--blocksize", "4096",
        "--wallets", "2",
        "--transactions", "0",
        "--interval", "10.0",
        "--print", "10",  # Print every 10 blocks instead of 1440
        "--reward", "50",
        "--halving", "210000",
        "--years", "0.1"  # Test with 0.1 years instead of 10 years
    ]
    
    print("Testing optimized blockchain simulation performance...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 80)
    
    start_time = time.time()
    
    try:
        # Run the simulation
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Simulation completed in {duration:.2f} seconds")
        
        if result.returncode == 0:
            print("✅ Simulation completed successfully!")
            print(f"Output length: {len(result.stdout)} characters")
            
            # Count blocks mined
            lines = result.stdout.split('\n')
            block_lines = [line for line in lines if 'Sum B:' in line]
            print(f"Blocks mined: {len(block_lines)}")
            
            if block_lines:
                print("Sample output:")
                for i, line in enumerate(block_lines[:3]):  # Show first 3 blocks
                    print(f"  {line}")
                if len(block_lines) > 3:
                    print(f"  ... and {len(block_lines) - 3} more blocks")
                    
        else:
            print("❌ Simulation failed!")
            print(f"Return code: {result.returncode}")
            print("Error output:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("❌ Simulation timed out after 5 minutes!")
        print("This indicates the simulation is still too slow.")
        
    except Exception as e:
        print(f"❌ Error running simulation: {e}")

if __name__ == "__main__":
    test_simulation_performance() 