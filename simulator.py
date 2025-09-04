"""
Main blockchain simulator module
Coordinates all components and provides the main simulation logic
"""

import time
import json
import logging
import argparse
import statistics
from typing import Dict, List, Optional

from config import (
    SimulationConfig, BLOCKCHAIN_CONFIGS, WORKLOAD_CONFIGS,
    LOG_CONFIG, DEFAULT_CONFIG
)
from models import SimulationStats, NetworkStats, MiningStats
from network import NetworkManager
from mining import MiningManager
from wallet import WalletManager
from trace_loader import TraceLoader

logger = logging.getLogger(__name__)


class BlockchainSimulator:
    """
    Main blockchain simulation orchestrator
    
    Coordinates all simulation components:
    - Network management
    - Mining operations
    - Wallet and transaction management
    - Statistics collection
    - Reporting
    - Trace loading and real-world data integration
    """
    
    def __init__(self, config: SimulationConfig, use_traces: bool = False, trace_file: str = None):
        self.config = config
        self.stats = SimulationStats()
        self.network_stats = NetworkStats()
        self.mining_stats = MiningStats()
        
        # Trace loading capability
        self.use_traces = use_traces
        self.trace_loader = TraceLoader() if use_traces else None
        self.trace_file = trace_file
        
        # Initialize components
        self.network_manager = NetworkManager(
            config.nodes, 
            config.neighbors, 
            self.network_stats
        )
        
        self.mining_manager = MiningManager(config, self.mining_stats)
        self.wallet_manager = WalletManager(
            config.wallets,
            config.transactions,
            config.interval
        )
        
        # Connect mining manager to network manager for block propagation
        self.mining_manager.set_block_callback(self._on_block_mined)
        
        # Enhanced network condition tracking
        self.network_congestion = 0.0
        self.block_utilization = 0.5
        self.last_network_update = time.time()
        
        # Debug: Print actual difficulty and total hashrate
        print(f"[DEBUG] DIFFICULTY: {self.config.difficulty}, HASHRATE: {self.config.miners * self.config.hashrate}")
        
        # Simulation state
        self.running = False
        self.blocks_mined = 0
        self.total_coins = 0.0
        
        # Setup logging
        self._setup_logging()
        
        logger.info("Blockchain simulator initialized")
        
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.WARNING,  # Changed to WARNING to minimize overhead
            format='%(levelname)s:%(name)s:%(message)s',
            handlers=[
                logging.FileHandler(LOG_CONFIG['file']),
                logging.StreamHandler()
            ]
        )
        
    def load_traces(self):
        """Load trace data if enabled"""
        if not self.use_traces or not self.trace_loader:
            return
            
        try:
            if self.trace_file:
                # Load specific trace file
                if self.trace_file.endswith('.json'):
                    events = self.trace_loader.load_json_trace(self.trace_file)
                elif self.trace_file.endswith('.csv'):
                    events = self.trace_loader.load_csv_trace(self.trace_file)
                else:
                    logger.warning(f"Unsupported trace file format: {self.trace_file}")
                    return
            else:
                # Load all available traces
                events = self.trace_loader.load_all_traces()
                
            logger.info(f"Loaded {len(events)} trace events")
            
        except Exception as e:
            logger.error(f"Error loading traces: {e}")
            
    def start(self):
        """Start the blockchain simulation"""
        logger.info("Starting blockchain simulation")
        self.running = True
        
        # Load traces if enabled
        if self.use_traces:
            self.load_traces()
        
        # Generate all transactions upfront
        if self.config.wallets > 0 and self.config.transactions > 0:
            logger.info("Generating all transactions upfront...")
            self.wallet_manager.start_transaction_generation(
                self._on_transaction_created
            )
            pool_size = self.mining_manager.get_pending_transaction_count()
            logger.info(f"Transaction generation complete. Pool size: {pool_size}")
            
            # Verify we have the expected number of transactions
            expected_tx = self.config.wallets * self.config.transactions
            if pool_size != expected_tx:
                logger.error(f"Expected {expected_tx} transactions, but pool has {pool_size}")
        elif self.config.wallets > 0 and self.config.transactions == 0:
            logger.info("No transactions to generate (transactions=0)")
        else:
            logger.info("No wallets specified, skipping transaction generation")
        
        # Start mining AFTER transactions are generated
        logger.info("Starting mining...")
        
        # Mark all miners as running
        for miner in self.mining_manager.miners:
            miner.running = True
            
        # Start main simulation loop
        self._simulation_loop()
        
    def stop(self):
        """Stop the blockchain simulation"""
        logger.info("Stopping blockchain simulation")
        logger.debug(f"Setting running flag to False (was {self.running})")
        self.running = False
        
        # Stop all components
        for miner in self.mining_manager.miners:
            miner.running = False
        self.wallet_manager.stop_transaction_generation()
        
        # Mark simulation as finished
        self.stats.finish()
        
    def _simulation_loop(self):
        """Main simulation loop with enhanced network monitoring - OPTIMIZED VERSION"""
        last_summary_time = time.time()
        last_network_update = time.time()
        iteration_count = 0
        
        try:
            logger.info("Starting simulation loop")
            iteration = 0
            while self.running:
                iteration += 1
                if iteration % 1000000 == 0:  # Much reduced logging frequency
                    logger.info(f"Simulation loop iteration {iteration}")
                iteration_count += 1
                    
                # Check termination conditions
                should_terminate = self._should_terminate()
                if should_terminate:
                    logger.info("Termination condition met, ending simulation")
                    break
                    
                # Try to mine a block
                block = self.mining_manager.mine_next_block()
                if block:
                    logger.info(f"Mined block {block.block_id} with {block.transaction_count} transactions")
                    
                    # Advance simulation time by the block's mining time
                    self.mining_manager.advance_simulation_time(block.time_since_last)
                    
                    # Update stats immediately after mining a block
                    self._update_stats()
                    
                    # Print summary based on print interval
                    if self.blocks_mined % self.config.print_interval == 0:
                        self._print_summary()
                else:
                    # Advance simulation time much more efficiently when no block is mined
                    # Advance by much larger amounts to speed up simulation dramatically
                    self.mining_manager.advance_simulation_time(300.0)  # Advance by 5 minutes
                    
                # Debug: Check if running flag changed
                if not self.running:
                    logger.warning(f"Running flag set to False after iteration {iteration}")
                    break
                    
                # Update network conditions much less frequently
                current_time = time.time()
                if current_time - last_network_update >= 600.0:  # Update every 10 minutes
                    self._update_network_conditions()
                    last_network_update = current_time
                
                # No sleep needed with time-based mining
                
        except KeyboardInterrupt:
            logger.info("Simulation interrupted by user")
        except Exception as e:
            logger.error(f"Error in simulation loop: {e}")
        finally:
            logger.info(f"Simulation loop ended after {iteration_count} iterations")
            self.stop()
            self._print_final_summary()
            
    def _update_network_conditions(self):
        """Update network conditions based on current state"""
        # Calculate network congestion based on pending transactions
        pending_tx_count = self.mining_manager.get_pending_transaction_count()
        max_tx_per_block = self.config.blocksize
        
        if max_tx_per_block > 0:
            self.network_congestion = min(1.0, pending_tx_count / (max_tx_per_block * 2))
        else:
            self.network_congestion = 0.0
            
        # Calculate block utilization based on recent blocks
        recent_blocks = self.mining_manager.blocks[-10:] if self.mining_manager.blocks else []
        if recent_blocks:
            avg_tx_count = sum(block.transaction_count for block in recent_blocks) / len(recent_blocks)
            self.block_utilization = min(1.0, avg_tx_count / max_tx_per_block) if max_tx_per_block > 0 else 0.5
        else:
            self.block_utilization = 0.5
            
        # Update wallet manager with new network conditions
        self.wallet_manager.update_network_conditions(self.network_congestion, self.block_utilization)
        
        logger.debug(f"Network conditions updated: congestion={self.network_congestion:.2f}, utilization={self.block_utilization:.2f}")
        
    def _should_terminate(self) -> bool:
        """Check if simulation should terminate"""
        # Check if pool is empty and we have mined at least some blocks
        pending_tx = self.mining_manager.get_pending_transaction_count()
        
        # Terminate if pool is empty and we have mined at least some blocks
        # This matches the professor's behavior - stop when all transactions are processed
        total_expected_transactions = self.config.wallets * self.config.transactions
        
        # Case 1: There are transactions to process and pool is empty
        if (self.config.wallets > 0 and 
            pending_tx == 0 and 
            self.blocks_mined > 0 and
            total_expected_transactions > 0):
            logger.info(f"All transactions processed - Blocks: {self.blocks_mined}, Pool: {pending_tx}")
            return True
            
        # Debug: Log why termination didn't happen
        if self.config.wallets > 0 and pending_tx == 0 and self.blocks_mined > 0:
            logger.debug(f"Termination check - Wallets: {self.config.wallets}, Transactions: {self.config.transactions}, Total expected: {total_expected_transactions}, Pool: {pending_tx}, Blocks: {self.blocks_mined}")
            
        # Case 2: Block count limit reached (for both transaction and non-transaction scenarios)
        if self.config.blocks and self.blocks_mined >= self.config.blocks:
            logger.info(f"Reached target block count: {self.blocks_mined}")
            return True
            
        return False
        
    def _all_transactions_processed(self) -> bool:
        """Check if all wallet transactions have been processed"""
        if self.config.wallets == 0:
            return True
            
        # Check if all transactions have been generated
        total_expected = self.config.wallets * self.config.transactions
        total_generated = sum(
            wallet.transactions_sent for wallet in self.wallet_manager.wallets.values()
        )
        
        # Check if all transactions have been mined (pool is empty)
        pool_empty = self.mining_manager.get_pending_transaction_count() == 0
        
        # Debug logging
        logger.debug(f"Transaction check - Expected: {total_expected}, Generated: {total_generated}, Pool empty: {pool_empty}")
        
        # Both conditions must be true
        return total_generated >= total_expected and pool_empty
        
    def _on_transaction_created(self, transaction):
        """Callback when a new transaction is created"""
        # Add to mining pool
        self.mining_manager.add_transaction(transaction)
        
        # Broadcast to network
        self.network_manager.broadcast_transaction(transaction)
        
        # Debug logging
        pool_size = self.mining_manager.get_pending_transaction_count()
        logger.debug(f"Transaction {transaction.tx_id} added to pool. Pool size: {pool_size}")
        
    def _on_block_mined(self, block):
        """Callback when a new block is mined"""
        # Broadcast block to network
        self.network_manager.broadcast_block(block)
        
        # Process confirmed transactions
        # Use the stored transaction objects if available
        if hasattr(block, 'transaction_objects') and block.transaction_objects:
            for transaction in block.transaction_objects:
                self.wallet_manager.process_confirmed_transaction(transaction)
        else:
            # Fallback to looking up transactions by ID
            for tx_id in block.transactions:
                transaction = self.mining_manager.get_transaction_by_id(tx_id)
                if transaction:
                    self.wallet_manager.process_confirmed_transaction(transaction)
        
        logger.debug(f"Block {block.block_id} broadcast to network with {block.transaction_count} transactions")
        
    def _update_stats(self):
        """Update simulation statistics"""
        old_blocks = self.blocks_mined
        self.blocks_mined = self.mining_manager.get_block_count()
        
        if self.blocks_mined != old_blocks:
            logger.info(f"Block count updated: {old_blocks} -> {self.blocks_mined}")
            
        self.total_coins = sum(
            block.miner_reward for block in self.mining_manager.blocks
        )
        
        # Calculate actual total transactions (not assuming full blocks)
        total_transactions = sum(
            block.transaction_count for block in self.mining_manager.blocks
        )
        
        # Update simulation stats
        self.stats.total_blocks = self.blocks_mined
        self.stats.total_transactions = total_transactions
        self.stats.total_coins = self.total_coins
        self.stats.network_stats = self.network_stats
        self.stats.mining_stats = self.mining_stats
        
        # Debug: Log current state
        logger.debug(f"Stats updated - Blocks: {self.blocks_mined}, Total transactions: {total_transactions}, Total coins: {self.total_coins}")
        
    def _print_summary(self):
        """Print periodic simulation summary in compact format"""
        # Calculate metrics using simulation time instead of real time
        simulation_time = self.mining_manager.get_simulation_time()
        
        # Calculate average block time based on simulation time
        if self.blocks_mined > 1:
            avg_block_time = simulation_time / self.blocks_mined
        else:
            avg_block_time = simulation_time
            
        # Calculate transactions per second based on simulation time
        total_transactions = sum(block.transaction_count for block in self.mining_manager.blocks)
        # Use simulation time for TPS calculation, not real time
        # When there are no transactions, TPS should be 0
        if total_transactions == 0:
            tps = 0.0
        else:
            tps = total_transactions / simulation_time if simulation_time > 0 else 0
        
        # Calculate inflation percentage using simplified formula
        if self.blocks_mined == 1:
            inflation = 0.0  # First block has 0% inflation
        else:
            # Calculate inflation based on block reward and current supply
            reward_per_block = self.mining_manager.get_block_reward()
            blocks_per_year = 365 * 24 * 3600 / self.config.blocktime  # seconds per year / block time
            circulating_supply = max(self.total_coins, 1)  # Avoid division by zero
            
            # Use a more reasonable calculation that matches professor's pattern
            inflation = (reward_per_block * blocks_per_year) / circulating_supply * 100
        
        # Calculate ETA based on remaining work
        pending_tx = self.mining_manager.get_pending_transaction_count()
        
        # If there are pending transactions, calculate ETA based on TPS
        if pending_tx > 0 and tps > 0:
            eta_seconds = pending_tx / tps
        else:
            # If no pending transactions, check if simulation should terminate soon
            total_expected_transactions = self.config.wallets * self.config.transactions
            if (self.config.wallets > 0 and 
                self.blocks_mined > 0 and
                total_expected_transactions > 0):
                # Simulation should terminate when pool is empty, so ETA should be small
                eta_seconds = 0
            else:
                # Calculate ETA based on remaining blocks (for non-transaction scenarios)
                total_blocks = self.config.blocks or 525600  # Default to 10 years worth of blocks
                remaining_blocks = total_blocks - self.blocks_mined
                if remaining_blocks > 0 and avg_block_time > 0:
                    eta_seconds = remaining_blocks * avg_block_time
                else:
                    eta_seconds = 0
            
        # Get network stats
        network_stats = self.network_manager.get_network_stats()
        total_hashrate = self.mining_manager.get_total_hashrate()
        
        # Format output exactly like the professor's example
        # Use simulation time for timestamp
        # Show total coins (C) instead of chain length
        # Format numbers like professor's output (K for thousands)
        def format_number(num):
            if num >= 1000:
                return f"{num/1000:.0f}K"
            return str(num)
        
        print(f"[{simulation_time:.2f}] Sum B:{self.blocks_mined}/{self.config.blocks or 0} "
              f"{(self.blocks_mined/(self.config.blocks or 1)*100):.1f}% "
              f"abt:{avg_block_time:.2f}s tps:{tps:.2f} infl:{inflation:.2f}% "
              f"ETA:{eta_seconds:.2f}s Diff:{self.mining_manager.get_current_difficulty()/1e9:.1f}B "
              f"H:{total_hashrate/1e6:.0f}M Tx:{total_transactions} C:{format_number(self.total_coins)} "
              f"Pool:{pending_tx} NMB:{self.network_stats.total_network_data/(1024*1024):.2f} "
              f"IO:{network_stats['total_connections']}")
        
    def _print_final_summary(self):
        """Print final simulation summary in compact format"""
        # Calculate final metrics using simulation time
        simulation_time = self.mining_manager.get_simulation_time()
        total_transactions = sum(block.transaction_count for block in self.mining_manager.blocks)
        avg_block_time = simulation_time / self.blocks_mined if self.blocks_mined > 0 else 0
        tps = total_transactions / simulation_time if simulation_time > 0 else 0
        if self.blocks_mined == 1:
            inflation = 0.0  # First block has 0% inflation
        else:
            # Calculate inflation based on block reward and current supply
            reward_per_block = self.mining_manager.get_block_reward()
            blocks_per_year = 365 * 24 * 3600 / self.config.blocktime  # seconds per year / block time
            circulating_supply = max(self.total_coins, 1)  # Avoid division by zero
            
            # Use a more reasonable calculation that matches professor's pattern
            inflation = (reward_per_block * blocks_per_year) / circulating_supply * 100
        
        # Get final stats
        network_stats = self.network_manager.get_network_stats()
        total_hashrate = self.mining_manager.get_total_hashrate()
        pending_tx = self.mining_manager.get_pending_transaction_count()
        
        # Print final summary in compact format
        def format_number(num):
            if num >= 1000:
                return f"{num/1000:.0f}K"
            return str(num)
        
        print(f"[******] End B:{self.blocks_mined}/{self.config.blocks or 0} "
              f"100.0% abt:{avg_block_time:.2f}s tps:{tps:.2f} infl:{inflation:.2f}% "
              f"Diff:{self.mining_manager.get_current_difficulty()/1e9:.1f}B "
              f"H:{total_hashrate/1e6:.0f}M Tx:{total_transactions} C:{format_number(self.total_coins)} "
              f"Pool:{pending_tx} NMB:{self.network_stats.total_network_data/(1024*1024):.2f} "
              f"IO:{network_stats['total_connections']}")
        
    def get_simulation_stats(self) -> Dict:
        """Get comprehensive simulation statistics"""
        return {
            'config': self.config.to_dict(),
            'stats': self.stats.to_dict(),
            'network_stats': self.network_manager.get_network_stats(),
            'wallet_stats': self.wallet_manager.get_all_wallet_stats(),
            'fee_stats': self.wallet_manager.get_fee_statistics(),
            'trace_stats': self.trace_loader.get_trace_statistics() if self.use_traces else None
        }
        
    def export_results(self, filename: str):
        """Export simulation results to file"""
        results = self.get_simulation_stats()
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
            
        logger.info(f"Results exported to {filename}")


def run_workload_simulation(chain_name: str, workload_type: str = None, difficulty: float = None, 
                          use_traces: bool = False, trace_file: str = None, args: argparse.Namespace = None) -> Dict:
    """
    Run a complete workload simulation for a specific blockchain
    
    Args:
        chain_name: Name of the blockchain (BTC, BCH, LTC, DOGE, MEMO)
        workload_type: Type of workload (NONE, SMALL, MEDIUM, LARGE)
        difficulty: Custom difficulty setting
        use_traces: Whether to use trace data
        trace_file: Specific trace file to load
        args: Command line arguments (to override workload defaults)
        
    Returns:
        Dictionary containing simulation results
    """
    # Get blockchain configuration
    if chain_name not in BLOCKCHAIN_CONFIGS:
        raise ValueError(f"Unknown blockchain: {chain_name}")
        
    chain_config = BLOCKCHAIN_CONFIGS[chain_name]
    
    # Get workload configuration
    if workload_type and workload_type not in WORKLOAD_CONFIGS:
        raise ValueError(f"Unknown workload: {workload_type}")
        
    workload_config = WORKLOAD_CONFIGS.get(workload_type, WORKLOAD_CONFIGS['NONE'])
    
    # Use command line arguments if provided, otherwise use workload defaults
    wallets = args.wallets if args and hasattr(args, 'wallets') else workload_config['wallets']
    transactions = args.transactions if args and hasattr(args, 'transactions') else workload_config['transactions']
    interval = args.interval if args and hasattr(args, 'interval') else workload_config['interval']
    
    # Create simulation configuration
    config = SimulationConfig(
        nodes=DEFAULT_CONFIG['nodes'],
        neighbors=DEFAULT_CONFIG['neighbors'],
        miners=DEFAULT_CONFIG['miners'],
        hashrate=DEFAULT_CONFIG['hashrate'],
        blocktime=chain_config['block_time'],
        difficulty=difficulty or (chain_config['block_time'] * DEFAULT_CONFIG['miners'] * DEFAULT_CONFIG['hashrate']),
        reward=chain_config['reward'],
        halving=chain_config['halving'],
        wallets=wallets,
        transactions=transactions,
        interval=interval,
        blocksize=chain_config['max_tx_per_block'],
        blocks=DEFAULT_CONFIG['blocks'],
        years=1.0,
        print_interval=DEFAULT_CONFIG['print'],
        debug=DEFAULT_CONFIG['debug']
    )
    
    # Create and run simulator
    simulator = BlockchainSimulator(config, use_traces, trace_file)
    
    try:
        simulator.start()
    except KeyboardInterrupt:
        logger.info("Simulation interrupted")
    finally:
        simulator.stop()
        
    return simulator.get_simulation_stats()


def main():
    """Main entry point for the simulator"""
    parser = argparse.ArgumentParser(description='Blockchain Simulation')
    
    # Basic configuration
    parser.add_argument('--chain', choices=['BTC', 'BCH', 'LTC', 'DOGE', 'MEMO'], 
                       default='BTC', help='Blockchain to simulate')
    parser.add_argument('--workload', choices=['NONE', 'SMALL', 'MEDIUM', 'LARGE'], 
                       default='NONE', help='Workload type')
    parser.add_argument('--difficulty', type=float, help='Custom difficulty setting')
    
    # Network configuration
    parser.add_argument('--nodes', type=int, default=10, help='Number of network nodes')
    parser.add_argument('--neighbors', type=int, default=3, help='Neighbors per node')
    
    # Mining configuration
    parser.add_argument('--miners', type=int, default=5, help='Number of miners')
    parser.add_argument('--hashrate', type=float, default=1000, help='Hashrate per miner')
    
    # Block configuration
    parser.add_argument('--blocktime', type=float, default=600, help='Block time in seconds')
    parser.add_argument('--blocksize', type=int, default=4096, help='Block size in transactions')
    parser.add_argument('--reward', type=float, default=50, help='Block reward')
    parser.add_argument('--halving', type=int, default=210000, help='Halving interval')
    
    # Transaction configuration
    parser.add_argument('--wallets', type=int, default=0, help='Number of wallets')
    parser.add_argument('--transactions', type=int, default=0, help='Transactions per wallet')
    parser.add_argument('--interval', type=float, default=1.0, help='Transaction generation interval')
    
    # Simulation parameters
    parser.add_argument('--blocks', type=int, help='Number of blocks to mine')
    parser.add_argument('--years', type=float, default=1.0, help='Simulation duration in years')
    parser.add_argument('--print', type=int, default=144, help='Print interval')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    # Trace loading
    parser.add_argument('--use-traces', action='store_true', help='Use trace data for simulation')
    parser.add_argument('--trace-file', type=str, help='Specific trace file to load')
    
    # Output
    parser.add_argument('--output', type=str, help='Output file for results')
    parser.add_argument('--export', type=str, help='Export file for results (alias for --output)')
    
    args = parser.parse_args()
    
    # Create configuration
    config = SimulationConfig.from_args(args)
    
    # Create and run simulator
    simulator = BlockchainSimulator(config, args.use_traces, args.trace_file)
    
    try:
        simulator.start()
    except KeyboardInterrupt:
        logger.info("Simulation interrupted by user")
    finally:
        simulator.stop()
        
    # Export results if requested
    if args.output:
        simulator.export_results(args.output)
    elif args.export:
        simulator.export_results(args.export)
        
    return simulator.get_simulation_stats()


if __name__ == "__main__":
    main() 