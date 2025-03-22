#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据处理工具

这个脚本提供了一系列用于数据处理的实用函数。
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any, Union, Optional


class DataProcessor:
    """数据处理类，提供各种数据转换和分析功能。"""
    
    def __init__(self, data_dir: str = "./data"):
        """
        初始化数据处理器。
        
        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.log_file = os.path.join(data_dir, "process_log.txt")
    
    def log(self, message: str) -> None:
        """
        记录处理日志。
        
        Args:
            message: 日志消息
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
        
        print(log_message)
    
    def csv_to_json(self, csv_file: str, json_file: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        将CSV文件转换为JSON格式。
        
        Args:
            csv_file: CSV文件路径
            json_file: 输出JSON文件路径（可选）
            
        Returns:
            包含数据的字典列表
        """
        self.log(f"正在将CSV文件 '{csv_file}' 转换为JSON")
        
        if not json_file:
            base_name = os.path.splitext(os.path.basename(csv_file))[0]
            json_file = os.path.join(self.data_dir, f"{base_name}.json")
        
        data = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                for row in csv_reader:
                    data.append(row)
            
            with open(json_file, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False, indent=2)
            
            self.log(f"成功转换CSV到JSON，保存至 '{json_file}'")
            return data
        
        except Exception as e:
            error_msg = f"转换CSV到JSON出错: {str(e)}"
            self.log(error_msg)
            raise RuntimeError(error_msg)
    
    def json_to_csv(self, json_file: str, csv_file: Optional[str] = None) -> str:
        """
        将JSON文件转换为CSV格式。
        
        Args:
            json_file: JSON文件路径
            csv_file: 输出CSV文件路径（可选）
            
        Returns:
            CSV文件保存路径
        """
        self.log(f"正在将JSON文件 '{json_file}' 转换为CSV")
        
        if not csv_file:
            base_name = os.path.splitext(os.path.basename(json_file))[0]
            csv_file = os.path.join(self.data_dir, f"{base_name}.csv")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data or not isinstance(data, list):
                raise ValueError("JSON文件必须包含对象数组")
            
            # 获取所有可能的字段名
            fieldnames = set()
            for item in data:
                if isinstance(item, dict):
                    fieldnames.update(item.keys())
            
            fieldnames = sorted(list(fieldnames))
            
            with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for item in data:
                    if isinstance(item, dict):
                        writer.writerow(item)
            
            self.log(f"成功转换JSON到CSV，保存至 '{csv_file}'")
            return csv_file
        
        except Exception as e:
            error_msg = f"转换JSON到CSV出错: {str(e)}"
            self.log(error_msg)
            raise RuntimeError(error_msg)
    
    def filter_data(self, data: List[Dict[str, Any]], 
                    filter_func: callable) -> List[Dict[str, Any]]:
        """
        根据过滤函数筛选数据。
        
        Args:
            data: 要筛选的数据列表
            filter_func: 过滤函数，接收一个字典并返回布尔值
            
        Returns:
            过滤后的数据列表
        """
        self.log(f"正在过滤数据，开始于 {len(data)} 条记录")
        filtered = [item for item in data if filter_func(item)]
        self.log(f"过滤完成，得到 {len(filtered)} 条记录")
        return filtered
    
    def sort_data(self, data: List[Dict[str, Any]], 
                  key_func: callable, reverse: bool = False) -> List[Dict[str, Any]]:
        """
        对数据进行排序。
        
        Args:
            data: 要排序的数据列表
            key_func: 排序键函数，接收一个字典并返回排序键
            reverse: 是否倒序排序
            
        Returns:
            排序后的数据列表
        """
        self.log(f"正在对 {len(data)} 条记录进行排序")
        result = sorted(data, key=key_func, reverse=reverse)
        self.log("排序完成")
        return result


def main():
    """主函数，演示数据处理功能。"""
    processor = DataProcessor()
    
    # 创建示例CSV文件
    sample_data = [
        {"id": "1", "name": "张三", "age": "25", "city": "北京"},
        {"id": "2", "name": "李四", "age": "30", "city": "上海"},
        {"id": "3", "name": "王五", "age": "28", "city": "广州"}
    ]
    
    sample_csv = os.path.join(processor.data_dir, "sample.csv")
    os.makedirs(processor.data_dir, exist_ok=True)
    
    with open(sample_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "age", "city"])
        writer.writeheader()
        for row in sample_data:
            writer.writerow(row)
    
    print(f"创建了示例CSV文件: {sample_csv}")
    
    # 演示CSV转JSON
    json_data = processor.csv_to_json(sample_csv)
    
    # 演示数据过滤
    filtered_data = processor.filter_data(
        json_data, 
        lambda x: int(x["age"]) > 25
    )
    print("过滤后的数据:", filtered_data)
    
    # 演示数据排序
    sorted_data = processor.sort_data(
        json_data,
        lambda x: x["name"]
    )
    print("排序后的数据:", sorted_data)


if __name__ == "__main__":
    main()
