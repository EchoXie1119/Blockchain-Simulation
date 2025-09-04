# -Blockchain-Simulation
Built a discrete-event blockchain simulator in Python using SimPy to model how nodes, miners, transaction pools, and coin issuance interact over time.
Key Features
Event-driven simulation of blockchain mechanics
Poisson/exponential processes for mining & wallet transactions
Difficulty adjustment and halving schedules
Metrics: block time, TPS, and total coin supply
Scenarios
10-year simulations for BTC, BCH, LTC, DOGE, and MEMO (coin creation + runtime analysis)
Workload stress tests:
Small: 10 wallets × 10 transactions (interval 10.0)
Medium: 1000 wallets × 1000 transactions (interval 1.0)
Large: 1000 wallets × 1000 transactions (interval 0.01)
Takeaways
This project was a great way to practice Python simulation design, experiment with scalability trade-offs, and gain deeper insight into how blockchain networks behave under different economic and workload conditions.
