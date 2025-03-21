#!/usr/bin/env python3
"""
This script analyzes and visualizes benchmark results from pyperplan runs,
comparing A* and GBFS with different heuristics.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import numpy as np
from pathlib import Path
import os

def load_results(csv_file):
    """Load benchmark results from CSV file"""
    df = pd.read_csv(csv_file)
    
    # Convert non-numeric values to NaN
    for col in ['expanded_nodes', 'plan_length']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Add comparative metrics
    df['algorithm_heuristic'] = df['search'] + '_' + df['heuristic']
    
    return df

def plot_success_rates(df, output_dir):
    """Plot success rates by algorithm and heuristic"""
    plt.figure(figsize=(12, 6))
    
    # Group by algorithm and heuristic
    success_rates = df.groupby(['search', 'heuristic'])['success'].mean().reset_index()
    success_rates['success_percent'] = success_rates['success'] * 100
    
    # Create DataFrame for plotting
    pivot_df = success_rates.pivot(index='heuristic', columns='search', values='success_percent')
    
    # Plot with A* in red tones and GBFS in blue-green tones
    colors = {'astar': '#E63946', 'gbf': '#1D7A8C'}
    ax = pivot_df.plot(kind='bar', figsize=(12, 6), color=colors)
    plt.title('Success Rate by Algorithm and Heuristic', fontsize=14)
    plt.ylabel('Success Rate (%)', fontsize=12)
    plt.xlabel('Heuristic', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%')
    
    plt.savefig(os.path.join(output_dir, 'success_rates.png'), dpi=300, bbox_inches='tight')
    plt.close()

def plot_runtime_comparison(df, output_dir):
    """Plot runtime comparison for successful runs"""
    plt.figure(figsize=(12, 6))
    
    # Filter successful runs
    success_df = df[df['success'] == True].copy()
    
    # Group by algorithm and heuristic
    runtime_avg = success_df.groupby(['search', 'heuristic'])['runtime'].mean().reset_index()
    
    # Create DataFrame for plotting
    pivot_df = runtime_avg.pivot(index='heuristic', columns='search', values='runtime')
    
    # Plot with A* in red tones and GBFS in blue-green tones
    colors = {'astar': '#E63946', 'gbf': '#1D7A8C'}
    ax = pivot_df.plot(kind='bar', figsize=(12, 6), color=colors)
    plt.title('Average Runtime by Algorithm and Heuristic (Successful Runs)', fontsize=14)
    plt.ylabel('Runtime (seconds)', fontsize=12)
    plt.xlabel('Heuristic', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    for container in ax.containers:
        ax.bar_label(container, fmt='%.3f')
    
    plt.savefig(os.path.join(output_dir, 'runtime_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()

def plot_plan_length_comparison(df, output_dir):
    """Plot plan length comparison for successful runs"""
    plt.figure(figsize=(12, 6))
    
    # Filter successful runs
    success_df = df[df['success'] == True].copy()
    
    # Group by algorithm and heuristic
    length_avg = success_df.groupby(['search', 'heuristic'])['plan_length'].mean().reset_index()
    
    # Create DataFrame for plotting
    pivot_df = length_avg.pivot(index='heuristic', columns='search', values='plan_length')
    
    # Plot with A* in red tones and GBFS in blue-green tones
    colors = {'astar': '#E63946', 'gbf': '#1D7A8C'}
    ax = pivot_df.plot(kind='bar', figsize=(12, 6), color=colors)
    plt.title('Average Plan Length by Algorithm and Heuristic', fontsize=14)
    plt.ylabel('Plan Length (steps)', fontsize=12)
    plt.xlabel('Heuristic', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f')
    
    plt.savefig(os.path.join(output_dir, 'plan_length_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()

def plot_expanded_nodes_comparison(df, output_dir):
    """Plot expanded nodes comparison for successful runs"""
    plt.figure(figsize=(12, 6))
    
    # Filter successful runs
    success_df = df[df['success'] == True].copy()
    
    # Group by algorithm and heuristic
    nodes_avg = success_df.groupby(['search', 'heuristic'])['expanded_nodes'].mean().reset_index()
    
    # Create DataFrame for plotting
    pivot_df = nodes_avg.pivot(index='heuristic', columns='search', values='expanded_nodes')
    
    # Plot with A* in red tones and GBFS in blue-green tones
    colors = {'astar': '#E63946', 'gbf': '#1D7A8C'}
    ax = pivot_df.plot(kind='bar', figsize=(12, 6), color=colors)
    plt.title('Average Expanded Nodes by Algorithm and Heuristic', fontsize=14)
    plt.ylabel('Expanded Nodes (log scale)', fontsize=12)
    plt.xlabel('Heuristic', fontsize=12)
    plt.yscale('log')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Custom formatting for log scale
    for container in ax.containers:
        labels = [f'{int(v)}' if not np.isnan(v) else '' for v in container.datavalues]
        ax.bar_label(container, labels=labels)
    
    plt.savefig(os.path.join(output_dir, 'expanded_nodes_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()

def plot_domain_comparison(df, output_dir):
    """Plot performance by domain"""
    domains = df['domain'].unique()
    
    plt.figure(figsize=(14, 8))
    
    # Success rate by domain
    domain_success = df.groupby(['domain', 'search', 'heuristic'])['success'].mean().reset_index()
    
    # Filter to focus on key algorithms and heuristics
    key_configs = [
        ('astar', 'hmax'),
        ('gbf', 'hmax'),
        ('astar', 'blind'),
        ('astar', 'landmark'),
        ('gbf', 'landmark')
    ]
    
    filtered_data = domain_success[
        domain_success.apply(
            lambda row: (row['search'], row['heuristic']) in key_configs, 
            axis=1
        )
    ]
    
    # Create new column for plotting
    filtered_data['algorithm_heuristic'] = filtered_data['search'] + '_' + filtered_data['heuristic']
    
    # Plot
    plt.figure(figsize=(14, 8))
    # Create a custom palette with red tones for A* and blue-green tones for GBFS
    palette = {
        'astar_hmax': '#E63946',     # red
        'astar_blind': '#F9ADA0',    # light red
        'astar_landmark': '#C1121F', # dark red
        'gbf_hmax': '#1D7A8C',       # teal
        'gbf_landmark': '#40A9BF'     # light blue
    }
    
    chart = sns.barplot(
        data=filtered_data, 
        x='domain', 
        y='success', 
        hue='algorithm_heuristic',
        palette=palette
    )
    
    plt.title('Success Rate by Domain for Different Algorithms', fontsize=14)
    plt.ylabel('Success Rate', fontsize=12)
    plt.xlabel('Domain', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Algorithm_Heuristic', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_dir, 'domain_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()

def plot_runtime_by_domain(df, output_dir):
    """Plot runtime comparison across domains for all algorithm-heuristic combinations"""
    plt.figure(figsize=(16, 10))
    
    # Filter for successful runs only
    success_df = df[df['success'] == True].copy()
    success_df['algorithm_heuristic'] = success_df['search'] + '_' + success_df['heuristic']
    
    # Group by domain and algorithm_heuristic
    runtime_by_domain = success_df.groupby(['domain', 'algorithm_heuristic'])['runtime'].mean().reset_index()
    
    # Create a custom color palette for algorithm-heuristic combinations
    # A* variants in red tones, GBFS variants in blue-green tones
    unique_combos = runtime_by_domain['algorithm_heuristic'].unique()
    
    # Generate color palette
    colors = {}
    for combo in unique_combos:
        if combo.startswith('astar'):
            # Red tones for A*
            if 'hmax' in combo:
                colors[combo] = '#E63946'  # Strong red for A* with hmax
            elif 'hadd' in combo:
                colors[combo] = '#F4A582'  # Medium red for A* with hadd
            elif 'hff' in combo:
                colors[combo] = '#D6604D'  # Light red for A* with hff
            else:
                colors[combo] = '#B2182B'  # Dark red for other A* variants
        else:  # gbf
            # Blue-green tones for GBFS
            if 'hmax' in combo:
                colors[combo] = '#1D7A8C'  # Strong teal for GBFS with hmax
            elif 'hadd' in combo:
                colors[combo] = '#4393C3'  # Medium blue for GBFS with hadd
            elif 'hff' in combo:
                colors[combo] = '#2166AC'  # Light blue for GBFS with hff
            else:
                colors[combo] = '#053061'  # Dark blue for other GBFS variants
    
    # Create the plot
    ax = sns.barplot(
        x='domain', 
        y='runtime', 
        hue='algorithm_heuristic', 
        data=runtime_by_domain, 
        palette=colors
    )
    
    plt.title('Average Runtime by Domain and Algorithm-Heuristic Combination', fontsize=16)
    plt.ylabel('Runtime (seconds)', fontsize=14)
    plt.xlabel('Domain', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Algorithm_Heuristic', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add text labels on top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%.3f', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'runtime_by_domain.png'), dpi=300, bbox_inches='tight')
    plt.close()

def generate_summary_report(df, output_path):
    """Generate a text report with key findings"""
    # Success rates
    success_by_alg_heuristic = df.groupby(['search', 'heuristic'])['success'].mean()
    
    # Runtime for successful runs
    runtime_data = df[df['success'] == True].groupby(['search', 'heuristic'])['runtime'].mean()
    
    # Plan length for successful runs
    plan_length_data = df[df['success'] == True].groupby(['search', 'heuristic'])['plan_length'].mean()
    
    # Nodes expanded for successful runs
    nodes_data = df[df['success'] == True].groupby(['search', 'heuristic'])['expanded_nodes'].mean()
    
    # Prepare the report
    report = ["# Benchmark Results Analysis\n"]
    
    report.append("## Overall Statistics\n")
    report.append(f"Total problems tested: {len(df['problem'].unique())}")
    report.append(f"Total domains tested: {len(df['domain'].unique())}")
    report.append(f"Algorithms tested: {', '.join(df['search'].unique())}")
    report.append(f"Heuristics tested: {', '.join(df['heuristic'].unique())}\n")
    
    report.append("## Success Rates\n")
    report.append("Success rate by algorithm and heuristic:\n")
    success_rates_table = success_by_alg_heuristic.reset_index()
    success_rates_table['success_percent'] = success_rates_table['success'] * 100
    report.append(success_rates_table.to_string(index=False, float_format=lambda x: f"{x:.1f}%"))
    report.append("\n")
    
    # Key focus: A* vs GBFS with h_max
    report.append("## A* vs GBFS with h_max (Key Comparison)\n")
    
    # Filter for these specific configurations
    astar_hmax = df[(df['search'] == 'astar') & (df['heuristic'] == 'hmax')]
    gbfs_hmax = df[(df['search'] == 'gbf') & (df['heuristic'] == 'hmax')]
    
    # Success rate
    astar_success = astar_hmax['success'].mean() * 100
    gbfs_success = gbfs_hmax['success'].mean() * 100
    
    report.append(f"Success Rate: A*+h_max: {astar_success:.1f}%, GBFS+h_max: {gbfs_success:.1f}%")
    
    # Runtime for successful runs
    astar_runtime = astar_hmax[astar_hmax['success'] == True]['runtime'].mean()
    gbfs_runtime = gbfs_hmax[gbfs_hmax['success'] == True]['runtime'].mean()
    
    report.append(f"Average Runtime: A*+h_max: {astar_runtime:.3f}s, GBFS+h_max: {gbfs_runtime:.3f}s")
    
    # Plan quality for successful runs
    astar_plan_length = astar_hmax[astar_hmax['success'] == True]['plan_length'].mean()
    gbfs_plan_length = gbfs_hmax[gbfs_hmax['success'] == True]['plan_length'].mean()
    
    report.append(f"Average Plan Length: A*+h_max: {astar_plan_length:.1f}, GBFS+h_max: {gbfs_plan_length:.1f}")
    
    # Expanded nodes for successful runs
    astar_nodes = astar_hmax[astar_hmax['success'] == True]['expanded_nodes'].mean()
    gbfs_nodes = gbfs_hmax[gbfs_hmax['success'] == True]['expanded_nodes'].mean()
    
    report.append(f"Average Expanded Nodes: A*+h_max: {astar_nodes:.1f}, GBFS+h_max: {gbfs_nodes:.1f}\n")
    
    # Analysis
    report.append("## Analysis\n")
    
    # Compare success rates
    if astar_success > gbfs_success:
        report.append(f"A* with h_max has a higher success rate than GBFS with h_max by {astar_success - gbfs_success:.1f} percentage points.")
    elif gbfs_success > astar_success:
        report.append(f"GBFS with h_max has a higher success rate than A* with h_max by {gbfs_success - astar_success:.1f} percentage points.")
    else:
        report.append("A* and GBFS with h_max have the same success rate.")
    
    # Compare runtime
    if not (np.isnan(astar_runtime) or np.isnan(gbfs_runtime)):
        if astar_runtime < gbfs_runtime:
            report.append(f"A* with h_max is faster than GBFS with h_max by {gbfs_runtime - astar_runtime:.3f} seconds on average.")
        elif gbfs_runtime < astar_runtime:
            report.append(f"GBFS with h_max is faster than A* with h_max by {astar_runtime - gbfs_runtime:.3f} seconds on average.")
        else:
            report.append("A* and GBFS with h_max have the same average runtime.")
    
    # Compare plan quality
    if not (np.isnan(astar_plan_length) or np.isnan(gbfs_plan_length)):
        if astar_plan_length < gbfs_plan_length:
            report.append(f"A* with h_max produces shorter plans than GBFS with h_max by {gbfs_plan_length - astar_plan_length:.1f} steps on average.")
        elif gbfs_plan_length < astar_plan_length:
            report.append(f"GBFS with h_max produces shorter plans than A* with h_max by {astar_plan_length - gbfs_plan_length:.1f} steps on average.")
        else:
            report.append("A* and GBFS with h_max produce plans of the same average length.")
    
    # Compare expanded nodes
    if not (np.isnan(astar_nodes) or np.isnan(gbfs_nodes)):
        if astar_nodes < gbfs_nodes:
            report.append(f"A* with h_max expands fewer nodes than GBFS with h_max by {gbfs_nodes - astar_nodes:.1f} nodes on average.")
        elif gbfs_nodes < astar_nodes:
            report.append(f"GBFS with h_max expands fewer nodes than A* with h_max by {astar_nodes - gbfs_nodes:.1f} nodes on average.")
        else:
            report.append("A* and GBFS with h_max expand the same number of nodes on average.")
    
    # Write the report to file
    with open(output_path, 'w') as f:
        f.write('\n'.join(report))

def main():
    parser = argparse.ArgumentParser(description="Visualize planning benchmark results")
    parser.add_argument("csv_file", help="CSV file with benchmark results")
    parser.add_argument("--output-dir", default="benchmark_analysis", help="Directory for output files")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load data
    df = load_results(args.csv_file)
    
    # Generate plots
    plot_success_rates(df, args.output_dir)
    plot_runtime_comparison(df, args.output_dir)
    plot_plan_length_comparison(df, args.output_dir)
    plot_expanded_nodes_comparison(df, args.output_dir)
    plot_domain_comparison(df, args.output_dir)
    plot_runtime_by_domain(df, args.output_dir)
    
    # Generate report
    report_path = os.path.join(args.output_dir, "benchmark_report.md")
    generate_summary_report(df, report_path)
    
    print(f"Analysis complete. Results saved to {args.output_dir}")
    print(f"Summary report: {report_path}")

if __name__ == "__main__":
    main()
