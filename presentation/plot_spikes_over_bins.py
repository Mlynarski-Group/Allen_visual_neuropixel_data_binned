import matplotlib.pyplot as plt


def plot_spikes(times, unit_order=None, ax=None, color="red"):
    if unit_order is None:
        unit_order = sorted(times["unit_id"].unique())
    unit_to_y = {unit_id: idx for idx, unit_id in enumerate(unit_order)}
    y = times["unit_id"].map(unit_to_y).to_numpy() + 0.5
    x = times["time_since_stimulus_presentation_onset"].to_numpy()

    if ax is None:
        _, ax = plt.subplots(figsize=(12, 6))

    ax.scatter(x, y, s=100, marker="|", color=color)
    ax.set_xlabel("Time since stimulus onset (s)")
    ax.set_ylabel("Unit index")
    ax.set_ylim(0, len(unit_order))
    ax.set_yticks([idx + 0.5 for idx in range(len(unit_order))])
    ax.set_yticklabels([str(unit_id) for unit_id in unit_order])
    return ax, unit_order


def plot_binned(spike, unit_order=None, ax=None):
    first_presentation = spike.isel(presentation_id=0)
    if unit_order is None:
        unit_order = list(first_presentation["unit_id"].to_numpy())
    first_presentation = first_presentation.sel(unit_id=unit_order)
    data = first_presentation.transpose("unit_id", "time").values

    if ax is None:
        _, ax = plt.subplots(figsize=(12, 6))

    time_values = first_presentation["time"].to_numpy()
    if len(time_values) > 1:
        dt = float(time_values[1] - time_values[0])
    else:
        dt = 0.0
    time_min = float(time_values.min()) - dt / 2.0
    time_max = float(time_values.max()) + dt / 2.0

    ax.imshow(
        data,
        aspect="auto",
        interpolation="nearest",
        cmap="Greys",
        extent=[
            time_min,
            time_max,
            0,
            data.shape[0],
        ],
        origin="lower",
    )
    ax.set_title("Spike raster bins (first presentation)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Unit index")
    ax.set_yticks([idx + 0.5 for idx in range(len(unit_order))])
    ax.set_yticklabels([str(unit_id) for unit_id in unit_order])
    return ax, unit_order


def main(spike, times):
    unit_order = sorted(times["unit_id"].unique())

    fig, ax = plt.subplots(figsize=(12, 6))
    plot_binned(spike, unit_order=unit_order, ax=ax)
    plot_spikes(times, unit_order=unit_order, ax=ax, color="red")

    time_values = spike["time"].to_numpy()
    if len(time_values) > 1:
        dt = float(time_values[1] - time_values[0])
    else:
        dt = 0.0
    time_min = float(time_values.min()) - dt / 2.0
    time_max = float(time_values.max()) + dt / 2.0
    ax.set_xlim(time_min, time_max)
    # ax.set_xticks(time_values)
    ax.set_title("Spike raster bins with spike times overlay")

    fig.tight_layout()
    fig.savefig("spikes_over_bins.png", dpi=200)
