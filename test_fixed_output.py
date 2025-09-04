#!/usr/bin/env python3
"""
Test script to verify the fixed output format matches professor's expectations
"""

import time
import subprocess
import sys

def test_fixed_output():
    """Test the fixed output format"""
    
    # Test command with your original parameters but smaller time frame
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
        "--print", "10",  # Print every 10 blocks
        "--reward", "50",
        "--halving", "210000",
        "--years", "0.1"  # Test with 0.1 years
    ]
    
    print("Testing fixed output format...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 80)
    
    start_time = time.time()
    
    try:
        # Run the simulation
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Simulation completed in {duration:.2f} seconds")
        
        if result.returncode == 0:
            print("✅ Simulation completed successfully!")
            
            # Analyze output format
            lines = result.stdout.split('\n')
            block_lines = [line for line in lines if 'Sum B:' in line]
            
            print(f"\nFound {len(block_lines)} block output lines")
            
            if block_lines:
                print("\nSample output lines:")
                for i, line in enumerate(block_lines[:5]):  # Show first 5 blocks
                    print(f"  {line}")
                    
                # Check format consistency
                print(f"\nFormat analysis:")
                sample_line = block_lines[0]
                parts = sample_line.split()
                
                print(f"  Timestamp format: {parts[0]}")
                print(f"  Block count format: {parts[2]}")
                print(f"  Average block time: {parts[4]}")
                print(f"  Difficulty format: {parts[8]}")
                print(f"  Hashrate format: {parts[9]}")
                
                # Verify key format elements
                if '[0.' in parts[0] or '[1.' in parts[0] or '[2.' in parts[0]:
                    print("  ✅ Timestamp format looks correct")
                else:
                    print("  ❌ Timestamp format issue")
                    
                if 'abt:' in parts[4]:
                    print("  ✅ Average block time format correct")
                else:
                    print("  ❌ Average block time format issue")
                    
                if 'Diff:' in parts[8]:
                    print("  ✅ Difficulty format correct")
                else:
                    print("  ❌ Difficulty format issue")
                    
                if 'H:' in parts[9]:
                    print("  ✅ Hashrate format correct")
                else:
                    print("  ❌ Hashrate format issue")
                    
        else:
            print("❌ Simulation failed!")
            print(f"Return code: {result.returncode}")
            print("Error output:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("❌ Simulation timed out after 5 minutes!")
        
    except Exception as e:
        print(f"❌ Error running simulation: {e}")

if __name__ == "__main__":
    test_fixed_output() 