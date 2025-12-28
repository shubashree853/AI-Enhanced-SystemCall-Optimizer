"""
------------------------------------------------------------
 File        : optimizer/optimizer.py
 Author      : Nandan A M
 Description : Core AI-enhanced system call optimization engine.
               Monitors syscall performance, generates AI-powered
               recommendations using Groq API, and provides real-time
               optimization strategies for system call processing.
 Created On  : 12-Dec-2025
 Version     : 1.0
------------------------------------------------------------
"""

import os
import time
import threading
import numpy as np
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import psutil
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class SyscallPerformanceRecord:
    name: str
    average_time: float
    execution_count: int
    variance: float
    peak_performance: float
    last_optimized: float
    resource_impact: Dict[str, float]
    category: str

class AISystemCallOptimizer:
    def __init__(self, performance_threshold: float = 0.05, learning_rate: float = 0.1, groq_api_key: str = None):
        self.performance_records: Dict[str, SyscallPerformanceRecord] = {}
        self.optimization_history: List[Dict] = []
        self.recommendations_dict: Dict[str, str] = {}
        self.performance_threshold = performance_threshold
        self.learning_rate = learning_rate
        self.lock = threading.Lock()
        self.global_resource_baseline = self._capture_system_resources()

        # Expanded syscall map with categories
        self.syscall_map = {
            0: {"name": "read", "category": "File I/O"},
            1: {"name": "write", "category": "File I/O"},
            2: {"name": "open", "category": "File I/O"},
            3: {"name": "close", "category": "File I/O"},
            4: {"name": "stat", "category": "File I/O"},
            5: {"name": "fstat", "category": "File I/O"},
            6: {"name": "lstat", "category": "File I/O"},
            8: {"name": "lseek", "category": "File I/O"},
            9: {"name": "mmap", "category": "Memory"},
            10: {"name": "mprotect", "category": "Memory"},
            11: {"name": "munmap", "category": "Memory"},
            13: {"name": "rt_sigaction", "category": "Signal"},
            14: {"name": "rt_sigprocmask", "category": "Signal"},
            21: {"name": "access", "category": "File I/O"},
            22: {"name": "pipe", "category": "IPC"},
            23: {"name": "select", "category": "I/O Multiplexing"},
            32: {"name": "dup", "category": "File I/O"},
            33: {"name": "dup2", "category": "File I/O"},
            39: {"name": "getpid", "category": "Process"},
            56: {"name": "clone", "category": "Process"},
            57: {"name": "fork", "category": "Process"},
            59: {"name": "execve", "category": "Process"},
            60: {"name": "exit", "category": "Process"},
            61: {"name": "wait4", "category": "Process"},
            62: {"name": "kill", "category": "Signal"},
            63: {"name": "uname", "category": "System"},
            72: {"name": "fcntl", "category": "File I/O"},
            78: {"name": "getdents", "category": "File I/O"},
            79: {"name": "getcwd", "category": "File I/O"},
            83: {"name": "mkdir", "category": "File I/O"},
            84: {"name": "rmdir", "category": "File I/O"},
            85: {"name": "creat", "category": "File I/O"},
            86: {"name": "link", "category": "File I/O"},
            87: {"name": "unlink", "category": "File I/O"},
            89: {"name": "readlink", "category": "File I/O"},
            90: {"name": "chmod", "category": "File I/O"},
            92: {"name": "chown", "category": "File I/O"},
            95: {"name": "umask", "category": "File I/O"},
            96: {"name": "gettimeofday", "category": "Time"},
            97: {"name": "getrlimit", "category": "Resource"},
            102: {"name": "getuid", "category": "User"},
            104: {"name": "getgid", "category": "User"},
            105: {"name": "setuid", "category": "User"},
            106: {"name": "setgid", "category": "User"},
            118: {"name": "fsync", "category": "File I/O"},
            137: {"name": "statfs", "category": "File System"},
            158: {"name": "arch_prctl", "category": "Architecture"},
            186: {"name": "gettid", "category": "Process"},
            202: {"name": "futex", "category": "Synchronization"},
            218: {"name": "set_tid_address", "category": "Process"},
            228: {"name": "clock_gettime", "category": "Time"},
            231: {"name": "exit_group", "category": "Process"},
            257: {"name": "openat", "category": "File I/O"},
            262: {"name": "newfstatat", "category": "File I/O"},
            293: {"name": "pipe2", "category": "IPC"}
        }

        if groq_api_key:
            self.groq_client = Groq(api_key=groq_api_key)
            print(f"Groq client initialized with API key: {groq_api_key[:5]}...")
        else:
            self.groq_client = None
            print("No Groq API key provided, falling back to rule-based strategy.")
        
        # Simulate syscall monitoring for demo purposes
        # In production, this would use eBPF on Linux
        self.refresh_interval = 5
        threading.Thread(target=self.simulate_monitoring, daemon=True).start()
        threading.Thread(target=self.resource_monitoring_thread, daemon=True).start()
        print(f"Performance data will refresh every {self.refresh_interval} seconds")

    def _capture_system_resources(self) -> Dict[str, float]:
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_io_percent': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:\\').percent
            }
        except:
            return {
                'cpu_percent': 0.0,
                'memory_percent': 0.0,
                'disk_io_percent': 0.0
            }

    def resource_monitoring_thread(self):
        while True:
            self.global_resource_baseline = self._capture_system_resources()
            time.sleep(1)

    def simulate_monitoring(self):
        """Simulate syscall monitoring for demo purposes"""
        import random
        common_syscalls = [
            'read', 'write', 'open', 'close', 'mmap', 'munmap', 'mprotect',
            'futex', 'clock_gettime', 'select', 'poll', 'epoll_wait',
            'fork', 'clone', 'execve', 'wait4', 'exit',
            'stat', 'fstat', 'lstat', 'access', 'chmod',
            'socket', 'connect', 'accept', 'send', 'recv',
            'pipe', 'dup', 'dup2', 'fcntl', 'ioctl'
        ]
        
        # Initialize with some data immediately
        for _ in range(20):
            syscall_name = random.choice(common_syscalls)
            execution_time = random.uniform(0.0001, 0.15)
            category = self._get_category_for_syscall(syscall_name)
            self.record_syscall_performance(syscall_name, execution_time, category)
        
        while True:
            time.sleep(0.3)  # Faster updates
            syscall_name = random.choice(common_syscalls)
            execution_time = random.uniform(0.0001, 0.15)
            category = self._get_category_for_syscall(syscall_name)
            self.record_syscall_performance(syscall_name, execution_time, category)

    def _get_category_for_syscall(self, syscall_name: str) -> str:
        for syscall_info in self.syscall_map.values():
            if syscall_info["name"] == syscall_name:
                return syscall_info["category"]
        return "Unknown"
    
    def get_category_for_syscall(self, syscall_name: str) -> str:
        """Public method to get category for a syscall"""
        return self._get_category_for_syscall(syscall_name)

    def record_syscall_performance(self, syscall_name: str, execution_time: float, category: str = "Unknown"):
        with self.lock:
            current_resources = self._capture_system_resources()
            resource_impact = {
                k: max(0, current_resources[k] - self.global_resource_baseline.get(k, 0))
                for k in current_resources
            }

            if syscall_name not in self.performance_records:
                self.performance_records[syscall_name] = SyscallPerformanceRecord(
                    name=syscall_name,
                    average_time=execution_time,
                    execution_count=1,
                    variance=0,
                    peak_performance=execution_time,
                    last_optimized=time.time(),
                    resource_impact=resource_impact,
                    category=category
                )
            else:
                record = self.performance_records[syscall_name]
                total_executions = record.execution_count + 1
                new_average = (
                    record.average_time * record.execution_count + execution_time
                ) / total_executions
                variance = np.var([record.average_time, execution_time])

                aggregated_impact = {
                    k: (record.resource_impact.get(k, 0) * record.execution_count +
                        resource_impact.get(k, 0)) / total_executions
                    for k in set(record.resource_impact) | set(resource_impact)
                }

                self.performance_records[syscall_name] = SyscallPerformanceRecord(
                    name=syscall_name,
                    average_time=new_average,
                    execution_count=total_executions,
                    variance=variance,
                    peak_performance=min(record.peak_performance, execution_time),
                    last_optimized=record.last_optimized,
                    resource_impact=aggregated_impact,
                    category=record.category
                )

    def generate_optimization_strategy(self) -> List[Dict[str, Any]]:
        recommendations = []
        with self.lock:
            for syscall, record in self.performance_records.items():
                if (record.average_time > self.performance_threshold or
                    any(impact > 50 for impact in record.resource_impact.values())):
                    recommendation = {
                        "syscall": syscall,
                        "current_performance": record.average_time,
                        "recommendation_type": self._get_recommendation_type(record),
                        "suggested_action": self._generate_mitigation_strategy(record),
                        "resource_impact": record.resource_impact,
                        "category": record.category
                    }
                    recommendations.append(recommendation)

            self.recommendations_dict = {rec['syscall']: rec['suggested_action'] for rec in recommendations}

            self.optimization_history.append({
                "timestamp": time.time(),
                "system_resources": self._capture_system_resources(),
                "recommendations": recommendations
            })
        return recommendations

    def _get_recommendation_type(self, record: SyscallPerformanceRecord) -> str:
        high_resource_impact = any(impact > 50 for impact in record.resource_impact.values())
        if high_resource_impact:
            return "CRITICAL_RESOURCE_BOTTLENECK"
        elif record.variance > record.average_time * 0.5:
            return "HIGH_VARIABILITY"
        elif record.average_time > self.performance_threshold * 2:
            return "SEVERE_PERFORMANCE_ISSUE"
        else:
            return "MODERATE_OPTIMIZATION"

    def _generate_mitigation_strategy(self, record: SyscallPerformanceRecord) -> str:
        if self.groq_client:
            prompt = f"""
You are an AI assistant specialized in system performance optimization. Based on the following performance data for a system call, suggest a specific and concise optimization strategy to improve its performance or reduce its resource usage. Provide a brief, actionable suggestion in plain text, in one or two sentences, without code or special formatting.

System Call: {record.name}
Category: {record.category}
Average Execution Time: {record.average_time:.4f} seconds
Variance: {record.variance:.4f}
Peak Performance: {record.peak_performance:.4f} seconds
Resource Impacts:
- CPU: {record.resource_impact.get('cpu_percent', 0):.2f}%
- Memory: {record.resource_impact.get('memory_percent', 0):.2f}%
- Disk I/O: {record.resource_impact.get('disk_io_percent', 0):.2f}%
"""
            try:
                response = self.groq_client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": "You are an AI assistant specialized in system performance optimization. Provide your suggestions in plain text without code or special formatting."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=75,
                    temperature=0.7
                )
                suggestion = response.choices[0].message.content.strip()
                if suggestion:
                    suggestion = ' '.join(suggestion.split())
                    return suggestion
            except Exception as e:
                print(f"Error generating strategy with Groq API: {e}")

        # Category-based strategies
        category_strategies = {
            "File I/O": [
                f"Implement buffered I/O for {record.name} to reduce system call frequency",
                f"Use asynchronous I/O for {record.name} operations to avoid blocking",
                f"Consider memory-mapped files instead of direct {record.name} calls"
            ],
            "Memory": [
                f"Optimize memory allocation patterns around {record.name}",
                f"Consider using huge pages to reduce {record.name} overhead",
                f"Implement memory pooling to reduce fragmentation in {record.name}"
            ],
            "Process": [
                f"Minimize {record.name} calls through process reuse",
                f"Use thread pools instead of frequent {record.name} calls",
                f"Implement process caching for {record.name} operations"
            ],
            "Synchronization": [
                f"Reduce lock contention around {record.name}",
                f"Use lock-free algorithms when possible to avoid {record.name}",
                f"Implement batching to reduce {record.name} frequency"
            ],
            "IPC": [
                f"Use shared memory instead of pipes for {record.name}",
                f"Batch messages to reduce {record.name} overhead",
                f"Consider using zero-copy techniques for {record.name}"
            ],
            "Time": [
                f"Cache time values to reduce {record.name} frequency",
                f"Use monotonic clocks for performance-sensitive code around {record.name}",
                f"Batch operations that require timestamp from {record.name}"
            ]
        }

        if record.category in category_strategies:
            strategies = category_strategies[record.category]
        else:
            strategies = [
                f"Implement advanced caching for {record.name}",
                f"Optimize memory allocation for {record.name}",
                f"Implement adaptive batching for {record.name}",
            ]

        resource_weights = {
            'cpu_percent': record.resource_impact.get('cpu_percent', 0),
            'memory_percent': record.resource_impact.get('memory_percent', 0),
            'disk_io_percent': record.resource_impact.get('disk_io_percent', 0)
        }
        max_resource_type = max(resource_weights, key=resource_weights.get)
        strategy_index = min(int(resource_weights[max_resource_type] / 20), len(strategies) - 1)
        return strategies[strategy_index]

    def get_performance_data(self) -> Dict[str, Any]:
        with self.lock:
            data = {}
            for k, v in self.performance_records.items():
                record_dict = asdict(v)
                record_dict['recommendation'] = self.recommendations_dict.get(k, '')
                data[k] = record_dict
            return data

    def get_refresh_interval(self) -> int:
        return self.refresh_interval

    def get_syscall_categories(self) -> Dict[str, List[str]]:
        categories = {}
        with self.lock:
            for syscall, record in self.performance_records.items():
                category = record.category
                if category not in categories:
                    categories[category] = []
                categories[category].append(syscall)
        return categories

    def get_syscall_details(self, syscall_name: str) -> Dict[str, Any]:
        with self.lock:
            if syscall_name in self.performance_records:
                record_dict = asdict(self.performance_records[syscall_name])
                record_dict['recommendation'] = self.recommendations_dict.get(syscall_name, '')
                return record_dict
            return {"error": "System call not found"}


# Global optimizer instance
# Try to get API key from environment or Django settings
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    try:
        from django.conf import settings
        groq_api_key = getattr(settings, 'GROQ_API_KEY', None)
    except:
        pass
syscall_optimizer = AISystemCallOptimizer(groq_api_key=groq_api_key)

