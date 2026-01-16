"""
Benchmark script for comparing CPU (NumPy) vs GPU (CuPy) noise processing.
Generates comparison graphs using matplotlib.
"""

import time
import json
import os
import numpy as np

# Try to import cupy
try:
    import cupy as cp

    HAS_CUPY = True
except ImportError:
    HAS_CUPY = False
    print("CuPy not available. GPU benchmarks will be skipped.")

try:
    import matplotlib.pyplot as plt

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Matplotlib not available. Graphs will not be generated.")

# Test image size
IMG_SIZE = (1024, 1024, 3)
ITERATIONS = 10


def create_test_image():
    return np.random.randint(0, 255, IMG_SIZE, dtype=np.uint8)


# CPU implementations (NumPy)
def cpu_gaussian(img, value):
    peak = 1 - value
    return np.random.normal(img / 30 * peak) / peak * 100


def cpu_speckle(img, value):
    noise = np.random.normal(loc=1, scale=value, size=img.shape)
    return np.clip(img * noise, 0, 255).astype(np.uint8)


def cpu_uniform(img, value):
    noise = np.random.uniform(-value, value, img.shape)
    return np.clip(img + noise, 0, 255).astype(np.uint8)


# GPU implementations (CuPy)
def gpu_gaussian(img, value):
    peak = 1 - value
    img_gpu = cp.asarray(img)
    result = cp.random.normal(img_gpu / 30 * peak) / peak * 100
    return cp.asnumpy(result)


def gpu_speckle(img, value):
    img_gpu = cp.asarray(img, dtype=cp.float32)
    noise = cp.random.normal(loc=1, scale=value, size=img_gpu.shape)
    result = cp.clip(img_gpu * noise, 0, 255)
    return cp.asnumpy(result).astype(np.uint8)


def gpu_uniform(img, value):
    img_gpu = cp.asarray(img, dtype=cp.float32)
    noise = cp.random.uniform(-value, value, img_gpu.shape)
    result = cp.clip(img_gpu + noise, 0, 255)
    return cp.asnumpy(result).astype(np.uint8)


def benchmark_function(func, img, value, iterations):
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func(img, value)
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / len(times)


def run_benchmarks():
    print(f"Running benchmarks with {ITERATIONS} iterations per test...")
    print(f"Image size: {IMG_SIZE}")
    print("-" * 50)

    img = create_test_image()
    value = 0.5

    results = {"cpu": {}, "gpu": {}, "speedup": {}}

    noise_types = [
        ("gaussian", cpu_gaussian, gpu_gaussian if HAS_CUPY else None),
        ("speckle", cpu_speckle, gpu_speckle if HAS_CUPY else None),
        ("uniform", cpu_uniform, gpu_uniform if HAS_CUPY else None),
    ]

    for name, cpu_fn, gpu_fn in noise_types:
        print(f"\nBenchmarking {name}...")

        # CPU benchmark
        cpu_time = benchmark_function(cpu_fn, img, value, ITERATIONS)
        results["cpu"][name] = cpu_time
        print(f"  CPU: {cpu_time * 1000:.2f}ms")

        # GPU benchmark
        if gpu_fn:
            # Warmup
            gpu_fn(img, value)
            gpu_time = benchmark_function(gpu_fn, img, value, ITERATIONS)
            results["gpu"][name] = gpu_time
            speedup = cpu_time / gpu_time
            results["speedup"][name] = speedup
            print(f"  GPU: {gpu_time * 1000:.2f}ms")
            print(f"  Speedup: {speedup:.1f}x")
        else:
            results["gpu"][name] = None
            results["speedup"][name] = None

    return results


def generate_graph(results):
    if not HAS_MATPLOTLIB:
        print("Cannot generate graph: matplotlib not installed")
        return

    noise_types = list(results["cpu"].keys())
    cpu_times = [results["cpu"][n] * 1000 for n in noise_types]
    gpu_times = [
        results["gpu"][n] * 1000 if results["gpu"][n] else 0 for n in noise_types
    ]
    speedups = [
        results["speedup"][n] if results["speedup"][n] else 0 for n in noise_types
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(
        "CPU vs GPU Noise Processing Benchmark", fontsize=16, fontweight="bold"
    )

    # Bar chart - Execution time
    x = np.arange(len(noise_types))
    width = 0.35

    bars1 = ax1.bar(
        x - width / 2, cpu_times, width, label="CPU (NumPy)", color="#e94560"
    )
    bars2 = ax1.bar(
        x + width / 2, gpu_times, width, label="GPU (CuPy)", color="#0f3460"
    )

    ax1.set_ylabel("Time (ms)", fontsize=12)
    ax1.set_xlabel("Noise Type", fontsize=12)
    ax1.set_title("Execution Time Comparison", fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels([n.capitalize() for n in noise_types])
    ax1.legend()
    ax1.grid(axis="y", alpha=0.3)

    # Bar values
    for bar in bars1:
        ax1.annotate(
            f"{bar.get_height():.1f}",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            ha="center",
            va="bottom",
            fontsize=10,
        )
    for bar in bars2:
        if bar.get_height() > 0:
            ax1.annotate(
                f"{bar.get_height():.1f}",
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                ha="center",
                va="bottom",
                fontsize=10,
            )

    # Speedup chart
    colors = ["#16213e" if s >= 20 else "#0f3460" for s in speedups]
    bars3 = ax2.bar(
        noise_types, speedups, color=colors, edgecolor="#e94560", linewidth=2
    )
    ax2.axhline(y=20, color="#e94560", linestyle="--", label="20x Target")
    ax2.set_ylabel("Speedup (x times faster)", fontsize=12)
    ax2.set_xlabel("Noise Type", fontsize=12)
    ax2.set_title("GPU Speedup over CPU", fontsize=14)
    ax2.set_xticklabels([n.capitalize() for n in noise_types])
    ax2.legend()
    ax2.grid(axis="y", alpha=0.3)

    for bar, s in zip(bars3, speedups):
        ax2.annotate(
            f"{s:.1f}x",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold",
        )

    plt.tight_layout()

    output_path = "benchmark_results.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"\nGraph saved to: {output_path}")
    plt.close()


def save_results(results):
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Results saved to: benchmark_results.json")


if __name__ == "__main__":
    print("=" * 50)
    print("NOISE PROCESSING BENCHMARK")
    print("=" * 50)

    results = run_benchmarks()

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)

    if HAS_CUPY:
        avg_speedup = sum(s for s in results["speedup"].values() if s) / len(
            [s for s in results["speedup"].values() if s]
        )
        print(f"Average GPU speedup: {avg_speedup:.1f}x")

        if avg_speedup >= 20:
            print("✓ TARGET ACHIEVED: 20x speedup or better!")
        else:
            print(f"⚠ Target: 20x, Achieved: {avg_speedup:.1f}x")

    save_results(results)
    generate_graph(results)
