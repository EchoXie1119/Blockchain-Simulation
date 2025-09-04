import os
import json

# Blockchain config for static info
BLOCKCHAIN_CONFIGS = {
    'btc':  { 'name': 'Bitcoin (BTC)',        'reward': '50 BTC',         'halving': '210K blocks',  'block_time': '600 sec',  'block_size': '1 MB base', 'max_tx': '4K TX' },
    'bch':  { 'name': 'Bitcoin Cash (BCH)',   'reward': '12.5 BCH',       'halving': '210K blocks',  'block_time': '600 sec',  'block_size': '32 MB',     'max_tx': '128K TX' },
    'ltc':  { 'name': 'Litecoin (LTC)',       'reward': '50 LTC',         'halving': '840K blocks',  'block_time': '150 sec',  'block_size': '1 MB',      'max_tx': '4K TX' },
    'doge': { 'name': 'Dogecoin (DOGE)',      'reward': '10 000 DOGE (static)', 'halving': 'None',     'block_time': '60 sec',   'block_size': '1 MB',      'max_tx': '4K TX' },
    'memo': { 'name': 'MEMO',                 'reward': '51.8457072 MEMO','halving': '9644K blocks', 'block_time': '3.27 sec', 'block_size': '8 MB',      'max_tx': '32K TX' },
}

# Find all result JSON files
results_dir = 'results'
files = [f for f in os.listdir(results_dir) if f.endswith('.json')]

# Prepare table header
header = [
    'Chain', 'Block Reward', 'Halving Schedule', 'Block Time', 'Block Size Limit', 'Max TX per Block',
    'Coins Created', 'Blocks Mined', 'Sim Time (s)'
]
rows = []

for fname in sorted(files):
    path = os.path.join(results_dir, fname)
    with open(path) as f:
        data = json.load(f)
    
    # Handle the case where data is a list containing a dictionary
    if isinstance(data, list) and len(data) > 0:
        data = data[0]
    
    # Try to get chain key from filename
    for key in BLOCKCHAIN_CONFIGS:
        if key in fname.lower():
            info = BLOCKCHAIN_CONFIGS[key]
            break
    else:
        info = {k: '?' for k in BLOCKCHAIN_CONFIGS['btc']}
    
    # Extract stats
    stats = data.get('stats', data)
    coins = stats.get('total_coins') or stats.get('simulation_stats',{}).get('total_coins') or '?'
    blocks = stats.get('blocks_mined') or stats.get('simulation_stats',{}).get('total_blocks') or '?'
    sim_time = data.get('simulation_time') or stats.get('simulation_time') or '?'
    
    # Format
    row = [
        info['name'], info['reward'], info['halving'], info['block_time'], info['block_size'], info['max_tx'],
        f"{coins:.2f}" if isinstance(coins, (int,float)) else coins,
        f"{blocks}" if blocks != '?' else '?',
        f"{sim_time:.2f}" if isinstance(sim_time, (int,float)) else sim_time
    ]
    rows.append(row)

# Print markdown table
print('| ' + ' | '.join(header) + ' |')
print('|' + '|'.join(['-'*len(h) for h in header]) + '|')
for row in rows:
    print('| ' + ' | '.join(row) + ' |') 