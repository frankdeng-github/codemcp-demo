#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
算法实现示例

这个模块提供了常见算法的Python实现示例。
"""

from typing import List, Any, Optional, Dict, Tuple, Callable
import time
import random


def benchmark(func: Callable) -> Callable:
    """装饰器：测量函数执行时间。"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {(end_time - start_time) * 1000:.2f} 毫秒")
        return result
    return wrapper


class SortingAlgorithms:
    """排序算法集合类。"""

    @staticmethod
    @benchmark
    def bubble_sort(arr: List[Any]) -> List[Any]:
        """
        冒泡排序实现。
        
        时间复杂度: O(n²)
        空间复杂度: O(1)
        
        Args:
            arr: 要排序的列表
            
        Returns:
            排序后的列表
        """
        n = len(arr)
        # 创建副本避免修改原列表
        result = arr.copy()
        
        for i in range(n):
            # 提前退出标志
            swapped = False
            
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
                    swapped = True
            
            # 如果内层循环未发生交换，则已排序
            if not swapped:
                break
        
        return result

    @staticmethod
    @benchmark
    def quick_sort(arr: List[Any]) -> List[Any]:
        """
        快速排序实现。
        
        时间复杂度: 平均 O(n log n)，最坏 O(n²)
        空间复杂度: O(log n)
        
        Args:
            arr: 要排序的列表
            
        Returns:
            排序后的列表
        """
        # 创建副本避免修改原列表
        result = arr.copy()
        
        def _quick_sort(arr: List[Any], low: int, high: int) -> None:
            if low < high:
                pivot_idx = _partition(arr, low, high)
                _quick_sort(arr, low, pivot_idx - 1)
                _quick_sort(arr, pivot_idx + 1, high)
        
        def _partition(arr: List[Any], low: int, high: int) -> int:
            # 选择最右边的元素作为基准
            pivot = arr[high]
            i = low - 1
            
            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1
        
        if result:
            _quick_sort(result, 0, len(result) - 1)
        
        return result

    @staticmethod
    @benchmark
    def merge_sort(arr: List[Any]) -> List[Any]:
        """
        归并排序实现。
        
        时间复杂度: O(n log n)
        空间复杂度: O(n)
        
        Args:
            arr: 要排序的列表
            
        Returns:
            排序后的列表
        """
        # 创建副本避免修改原列表
        result = arr.copy()
        
        def _merge_sort(arr: List[Any]) -> List[Any]:
            if len(arr) <= 1:
                return arr
            
            # 分割数组
            mid = len(arr) // 2
            left = _merge_sort(arr[:mid])
            right = _merge_sort(arr[mid:])
            
            # 合并已排序的子数组
            return _merge(left, right)
        
        def _merge(left: List[Any], right: List[Any]) -> List[Any]:
            result = []
            i = j = 0
            
            # 合并两个已排序的列表
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            
            # 添加剩余元素
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        
        return _merge_sort(result)


class SearchAlgorithms:
    """搜索算法集合类。"""

    @staticmethod
    @benchmark
    def linear_search(arr: List[Any], target: Any) -> Optional[int]:
        """
        线性搜索（顺序搜索）实现。
        
        时间复杂度: O(n)
        空间复杂度: O(1)
        
        Args:
            arr: 要搜索的列表
            target: 目标值
            
        Returns:
            目标值的索引，未找到则返回None
        """
        for i, item in enumerate(arr):
            if item == target:
                return i
        return None

    @staticmethod
    @benchmark
    def binary_search(arr: List[Any], target: Any) -> Optional[int]:
        """
        二分搜索实现（要求列表已排序）。
        
        时间复杂度: O(log n)
        空间复杂度: O(1)
        
        Args:
            arr: 已排序的列表
            target: 目标值
            
        Returns:
            目标值的索引，未找到则返回None
        """
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return None


class GraphAlgorithms:
    """图算法集合类。"""

    @staticmethod
    @benchmark
    def dijkstra(graph: Dict[str, Dict[str, int]], start: str) -> Dict[str, int]:
        """
        Dijkstra最短路径算法实现。
        
        时间复杂度: O(V²)，其中V是顶点数
        空间复杂度: O(V)
        
        Args:
            graph: 图的邻接表表示，例如 {'A': {'B': 1, 'C': 4}, 'B': {...}, ...}
            start: 起始顶点
            
        Returns:
            从起始顶点到所有其他顶点的最短距离
        """
        # 初始化距离字典
        distances = {vertex: float('infinity') for vertex in graph}
        distances[start] = 0
        
        # 未处理的顶点集合
        unvisited = list(graph.keys())
        
        while unvisited:
            # 找到未访问顶点中距离最小的
            current = min(unvisited, key=lambda vertex: distances[vertex])
            
            # 如果当前顶点的距离是无穷大，说明剩余顶点都不可达
            if distances[current] == float('infinity'):
                break
            
            # 从未访问集合中移除当前顶点
            unvisited.remove(current)
            
            # 检查当前顶点的邻居
            for neighbor, weight in graph[current].items():
                distance = distances[current] + weight
                
                # 如果找到更短的路径，则更新
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
        
        return distances


def main():
    """主函数，演示各种算法。"""
    print("算法演示程序\n")
    
    # 创建随机数据用于排序和搜索
    data = [random.randint(1, 1000) for _ in range(100)]
    print(f"原始数据（前10个）: {data[:10]}...\n")
    
    # 排序算法演示
    print("== 排序算法演示 ==")
    bubble_sorted = SortingAlgorithms.bubble_sort(data)
    quick_sorted = SortingAlgorithms.quick_sort(data)
    merge_sorted = SortingAlgorithms.merge_sort(data)
    
    print(f"冒泡排序结果（前10个）: {bubble_sorted[:10]}...")
    print(f"快速排序结果（前10个）: {quick_sorted[:10]}...")
    print(f"归并排序结果（前10个）: {merge_sorted[:10]}...")
    print()
    
    # 搜索算法演示
    print("== 搜索算法演示 ==")
    target = data[random.randint(0, len(data)-1)]
    print(f"搜索目标值: {target}")
    
    linear_result = SearchAlgorithms.linear_search(data, target)
    print(f"线性搜索结果: 索引 {linear_result}")
    
    # 必须使用已排序的数据进行二分搜索
    binary_result = SearchAlgorithms.binary_search(sorted(data), target)
    print(f"二分搜索结果: 索引 {binary_result}")
    print()
    
    # 图算法演示
    print("== 图算法演示 ==")
    graph = {
        'A': {'B': 2, 'C': 4},
        'B': {'A': 2, 'C': 1, 'D': 7},
        'C': {'A': 4, 'B': 1, 'D': 3},
        'D': {'B': 7, 'C': 3}
    }
    
    print("图结构:")
    for node, edges in graph.items():
        print(f"  {node} -> {edges}")
    
    shortest_paths = GraphAlgorithms.dijkstra(graph, 'A')
    print("\nDijkstra算法结果（从A出发的最短路径）:")
    for node, distance in shortest_paths.items():
        print(f"  A到{node}的最短距离: {distance}")


if __name__ == "__main__":
    main()
