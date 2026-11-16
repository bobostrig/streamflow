import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load_streamflow(filename): 
    csv_path = Path(__file__).with_name(filename)
    data = np.genfromtxt(csv_path, delimiter=",", dtype=str, skip_header=1)
    dates = data[:, 0].astype("datetime64[m]")
    flows = data[:, 1:].astype(float)
    return dates, flows

#131	2021-06-01T08:15	35.6	57

def summarize(dates, flows, sites):
    # Store one set of summary statistics for each gauge.
    summaries = {}
    # Pair each gauge name with the matching column of flow readings.
    for index, site in enumerate(sites):
        # Select all flow readings for the current gauge.
        site_flows = flows[:, index]
        # Find the row of this gauge's first maximum reading.
        max_index = np.argmax(site_flows)
        # Save the maximum, its timestamp, minimum, and average for this gauge.
        summaries[site] = {
            "max_flow_cfs": float(np.max(site_flows)),  # Highest recorded flow in cfs.
            "max_datetime": dates[max_index],  # Date and time of the maximum flow.
            "min_flow_cfs": float(np.min(site_flows)),  # Lowest recorded flow in cfs.
            "average_flow_cfs": float(np.mean(site_flows)),  # Mean flow in cfs.
        }

    # Put the CSV report beside this Python file.
    summary_path = Path(__file__).with_name("streamflow_summary.csv")
    # Open the report for writing; newline="" prevents extra blank lines in CSV files.
    with summary_path.open("w", newline="", encoding="utf-8") as summary_file:
        # Use the CSV writer to separate and escape each field correctly.
        writer = csv.writer(summary_file)
        # Write the column names as the first row of the report.
        writer.writerow(
            ["site", "max_flow_cfs", "max_datetime", "min_flow_cfs", "average_flow_cfs"]
        )
        # Write one row of statistics for every gauge.
        for site, stats in summaries.items():
            writer.writerow(
                [
                    site,  # Gauge identifier.
                    f"{stats['max_flow_cfs']:.1f}",  # Maximum flow, rounded to one decimal.
                    stats["max_datetime"],  # Timestamp of the maximum flow.
                    f"{stats['min_flow_cfs']:.1f}",  # Minimum flow, rounded to one decimal.
                    f"{stats['average_flow_cfs']:.1f}",  # Average flow, rounded to one decimal.
                ]
            )

    # Print a fixed-width header so the columns line up in the terminal.
    print(
        f"{'Site':<12}{'Max flow (cfs)':>16}{'Max date/time':>24}"
        f"{'Min flow (cfs)':>16}{'Average (cfs)':>16}"
    )
    # Print each gauge's statistics using matching column widths.
    for site, stats in summaries.items():
        print(
            f"{site:<12}{stats['max_flow_cfs']:>16.1f}"
            f"{str(stats['max_datetime']):>24}"
            f"{stats['min_flow_cfs']:>16.1f}"
            f"{stats['average_flow_cfs']:>16.1f}"
        )
    # Tell the user where the CSV report was saved.
    print(f"Summary saved to {summary_path}")
    # Return the statistics so other code can use them.
    return summaries


def plot_streamflow(dates, flows, sites):
    for index, site in enumerate(sites):
        plt.plot(dates, flows[:, index], label=site)

    plt.grid(True)
    plt.legend(title="Site Numbers")
    plt.title("Provo River Streamflow Data (2021)")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.ylabel("Flowrate (cfs)")
    plt.tight_layout()
    plt.savefig("provo_streamflow.png", dpi=150, bbox_inches="tight")
    plt.show()


def report_hours_above_threshold(flows, sites, threshold):
    print(f"Hours above {threshold:g} cfs:")
    for index, site in enumerate(sites):
        # Count readings above the threshold; each 15-minute reading represents 0.25 hours.
        hours = np.sum(flows[:, index] > threshold) * 0.25
        print(f"{site}: {hours:g} hours")


sites = ["10163000", "10155200", "10155500", "10154200", "10155000"]
dates, flows = load_streamflow("June-2021-Provo-River-Streamflow-Rates.csv")
# Ask for a flow threshold and report how long each gauge exceeds it.
threshold = float(input("Enter a flow threshold in cfs: "))
report_hours_above_threshold(flows, sites, threshold)
summarize(dates, flows, sites)
plot_streamflow(dates, flows, sites)
