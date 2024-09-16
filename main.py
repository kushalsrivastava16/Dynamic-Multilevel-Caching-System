from collections import OrderedDict, defaultdict


class CacheLevel:
    def __init__(self, size, eviction_policy):
        self.size = size
        self.eviction_policy = eviction_policy
        self.cache = OrderedDict() if eviction_policy == 'LRU' else {}
        self.usage_count = defaultdict(int)  # For LFU eviction policy

    def get(self, key):
        if key not in self.cache:
            return None
        if self.eviction_policy == 'LRU':
            # Move the accessed item to the end to maintain order for LRU
            self.cache.move_to_end(key)
        elif self.eviction_policy == 'LFU':
            # Increase usage count for LFU policy
            self.usage_count[key] += 1
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            if self.eviction_policy == 'LRU':
                # Move the accessed item to the end to maintain order for LRU
                self.cache.move_to_end(key)
            elif self.eviction_policy == 'LFU':
                self.usage_count[key] += 1
            self.cache[key] = value
        else:
            if len(self.cache) >= self.size:
                self.evict()
            self.cache[key] = value
            if self.eviction_policy == 'LFU':
                self.usage_count[key] = 1

    def evict(self):
        if self.eviction_policy == 'LRU':
            # Evict the first item (least recently used)
            self.cache.popitem(last=False)
        elif self.eviction_policy == 'LFU':
            # Evict the least frequently used item
            least_used_key = min(self.usage_count, key=self.usage_count.get)
            self.cache.pop(least_used_key)
            del self.usage_count[least_used_key]

    def display(self):
        return list(self.cache.items())


class DynamicMultilevelCache:
    def __init__(self):
        self.cache_levels = []

    def addCacheLevel(self, size, eviction_policy):
        """Adds a new cache level."""
        new_cache = CacheLevel(size, eviction_policy)
        self.cache_levels.append(new_cache)

    def removeCacheLevel(self, level):
        """Removes the cache level at the specified index."""
        if 0 <= level < len(self.cache_levels):
            self.cache_levels.pop(level)
        else:
            print(f"Cache level {level} does not exist.")

    def get(self, key):
        """Retrieves the data for the given key from cache levels."""
        for i, cache in enumerate(self.cache_levels):
            value = cache.get(key)
            if value is not None:
                # Promote the key to higher cache levels (L1)
                for j in range(i - 1, -1, -1):
                    self.cache_levels[j].put(key, value)
                return value
        # Simulate fetching from main memory and store in L1 if not found
        print(f"Cache miss for key: {key}, fetching from memory...")
        self.put(key, f"FetchedValueFor-{key}")
        return f"FetchedValueFor-{key}"

    def put(self, key, value):
        """Inserts the key-value pair into L1 cache."""
        if len(self.cache_levels) > 0:
            self.cache_levels[0].put(key, value)

    def displayCache(self):
        """Displays the current state of all cache levels."""
        for i, cache in enumerate(self.cache_levels):
            print(f"Cache Level {i + 1}: {cache.display()}")


# Example Usage:
if __name__ == "__main__":
    # Create the cache system
    cache_system = DynamicMultilevelCache()

    # Add cache levels with different sizes and eviction policies
    cache_system.addCacheLevel(3, 'LRU')  # L1 with size 3 and LRU eviction policy
    cache_system.addCacheLevel(2, 'LFU')  # L2 with size 2 and LFU eviction policy

    # Insert data into cache
    cache_system.put("A", "1")
    cache_system.put("B", "2")
    cache_system.put("C", "3")

    # Retrieve data
    print(cache_system.get("A"))  # Outputs "1" and moves "A" to the top of L1

    # Insert more data causing eviction
    cache_system.put("D", "4")  # L1 is full, should evict the least recently used (LRU)

    # Fetch data from lower levels
    print(cache_system.get("C"))  # Fetches from L2 and promotes to L1

    # Display cache contents
    cache_system.displayCache()

    # Remove a cache level
    cache_system.removeCacheLevel(1)  # Removes L2 cache

    # Display cache contents after removal
    cache_system.displayCache()
