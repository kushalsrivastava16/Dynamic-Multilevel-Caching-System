# Dynamic-Multilevel-Caching-System
# Project Overview
This project implements a Dynamic Multilevel Caching System designed to efficiently manage data across multiple cache levels. The system supports various cache management features, including:

Multiple Cache Levels with different sizes and eviction policies.
Eviction Policies: Least Recently Used (LRU) and Least Frequently Used (LFU).
Dynamic Cache Level Management: Cache levels can be added or removed dynamically at runtime.
Efficient Data Retrieval: The system retrieves data from the highest-priority cache and promotes data between cache levels when necessary.
Performance Optimizations: Ensures efficient lookups and minimizes cache misses.
# Features
Multiple Cache Levels:
Cache levels can be added dynamically with different sizes and eviction policies.
Data is first retrieved from the highest-priority cache level (L1), and if not found, it is searched in lower levels (L2, L3, etc.).
Eviction Policies:
Least Recently Used (LRU): Evicts the least recently accessed item.
Least Frequently Used (LFU): Evicts the least frequently accessed item.
Data Retrieval and Insertion:
If data is found in lower cache levels, it is moved up to higher levels (e.g., from L2 to L1).
New data is always inserted at L1, and if the cache is full, items are evicted based on the cache's eviction policy.
Dynamic Cache Level Management:
You can add or remove cache levels at runtime, specifying the size and eviction policy for each level.
# Bonus Features (Optional):
Concurrency: The system can be extended to support concurrent reads and writes to the cache (not implemented in the current version).
#System Requirements
Python 3.x

# How to Run the Project
Clone the Repository:

git clone <your-repository-url>
cd dynamic-multilevel-cache-system
Run the Script: You can run the script from the command line:


python cache_system.py
Example Usage:

The following demonstrates the main functionalities of the system:

cache_system = DynamicMultilevelCache()

Add two cache levels with LRU and LFU eviction policies
cache_system.addCacheLevel(3, 'LRU')  # L1 cache with size 3 and LRU policy
cache_system.addCacheLevel(2, 'LFU')  # L2 cache with size 2 and LFU policy

Insert key-value pairs
cache_system.put("A", "1")
cache_system.put("B", "2")
cache_system.put("C", "3")

Retrieve data from L1
print(cache_system.get("A"))  # Outputs: 1

Insert more data and trigger eviction in L1
cache_system.put("D", "4")  # Evicts the least recently used item in L1

Retrieve data and promote from L2 to L1
print(cache_system.get("C"))  # Outputs: 3 and moves "C" from L2 to L1

Display the current state of all cache levels
cache_system.displayCache()
Methods
addCacheLevel(size: int, evictionPolicy: str): void:

Adds a new cache level with the specified size and eviction policy (either 'LRU' or 'LFU').
get(key: str): str | None:

Retrieves the data corresponding to the given key from the cache system. If the key is not found, it returns None.
put(key: str, value: str): void:

Inserts the key-value pair into the L1 cache. If L1 is full, it evicts an item according to its eviction policy.
removeCacheLevel(level: int): void:

Removes a cache level by specifying its index (L1 = 0, L2 = 1, etc.).
displayCache(): void:

Prints the current state of each cache level, showing the keys and values stored in each level.
#Example Output
Cache miss for key: C, fetching from memory...
Cache Level 1: [('A', '1'), ('D', '4'), ('C', '3')]
Cache Level 2: [('B', '2')]

# Key Design Decisions
LRU and LFU Policies: The system uses OrderedDict for LRU to automatically maintain the access order of items, while LFU uses a manual count mechanism to track access frequencies.
Cache Promotion: Data retrieved from lower cache levels is promoted to higher levels (L1) for better future access speed.
Efficiency: The cache system uses efficient lookups and minimal data movement to maintain performance.
# Assumptions
The cache levels are indexed starting from L1 as level 0.
When a cache level is full, the eviction policies are strictly applied, and items are evicted based on the policy.
In case of cache misses, the system simulates fetching the value from a backend or main memory.
# Testing
Test cases are provided in the main function within the cache_system.py file. Additional test cases can be added to validate the correctness of different functionalities such as eviction policies, dynamic cache management, and promotion across cache levels.

# Future Improvements
Concurrency Support: Implement thread-safety using locks to allow concurrent access to the cache system.
More Eviction Policies: Add support for additional eviction policies (e.g., MRU, FIFO).
Persistent Storage: Optionally, integrate persistent storage to save cache states.
# License
This project is licensed under the MIT License - see the LICENSE file for details
