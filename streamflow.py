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
    summaries = {}
    for index, site in enumerate(sites):
        site_flows = flows[:, index]
        max_index = np.argmax(site_flows)
        summaries[site] = {
            "max_flow_cfs": float(np.max(site_flows)),
            "max_datetime": dates[max_index],
            "min_flow_cfs": float(np.min(site_flows)),
            "average_flow_cfs": float(np.mean(site_flows)),
        }

    summary_path = Path(__file__).with_name("streamflow_summary.csv")
    with summary_path.open("w", newline="", encoding="utf-8") as summary_file:
        writer = csv.writer(summary_file)
        writer.writerow(
            ["site", "max_flow_cfs", "max_datetime", "min_flow_cfs", "average_flow_cfs"]
        )
        for site, stats in summaries.items():
            writer.writerow(
                [
                    site,
                    f"{stats['max_flow_cfs']:.1f}",
                    stats["max_datetime"],
                    f"{stats['min_flow_cfs']:.1f}",
                    f"{stats['average_flow_cfs']:.1f}",
                ]
            )

    print(
        f"{'Site':<12}{'Max flow (cfs)':>16}{'Max date/time':>24}"
        f"{'Min flow (cfs)':>16}{'Average (cfs)':>16}"
    )
    for site, stats in summaries.items():
        print(
            f"{site:<12}{stats['max_flow_cfs']:>16.1f}"
            f"{str(stats['max_datetime']):>24}"
            f"{stats['min_flow_cfs']:>16.1f}"
            f"{stats['average_flow_cfs']:>16.1f}"
        )
    print(f"Summary saved to {summary_path}")
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


sites = ["10163000", "10155200", "10155500", "10154200", "10155000"]
dates, flows = load_streamflow("June-2021-Provo-River-Streamflow-Rates.csv")
summarize(dates, flows, sites)
plot_streamflow(dates, flows, sites)
