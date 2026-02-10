from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "combined_statistics.csv"
SESSIONS_TABLE_PATH = BASE_DIR / "data" / "sessions.csv"
FIG_DIR = BASE_DIR / "figures"


def _load_data():
    df = pd.read_csv(DATA_PATH)
    df["n_units"] = pd.to_numeric(df["n_units"], errors="coerce").fillna(0).astype(int)
    df["n_presentations"] = (
        pd.to_numeric(df["n_presentations"], errors="coerce").fillna(0).astype(int)
    )
    return df

def _load_session_types():
    sessions = pd.read_csv(SESSIONS_TABLE_PATH, usecols=["id", "session_type"])
    return sessions.rename(columns={"id": "session_id"})

def _structure_order(df, value_col):
    totals = (
        df.groupby("brain_structure", as_index=False)[value_col]
        .sum()
        .sort_values(value_col, ascending=False)
    )
    return totals["brain_structure"].tolist()

def _stimulus_order(df, value_col):
    totals = (
        df.groupby("stimulus_type", as_index=False)[value_col]
        .sum()
        .sort_values(value_col, ascending=False)
    )
    return totals["stimulus_type"].tolist()

def _session_order_by_type(df, value_col):
    sessions = _load_session_types()
    totals = df.groupby("session_id", as_index=False)[value_col].sum()
    merged = totals.merge(sessions, on="session_id", how="left")
    merged["session_type"] = merged["session_type"].fillna("unknown")
    priority_map = {"brain_observatory_1.1": 0, "functional_connectivity": 1}
    merged["session_type_order"] = (
        merged["session_type"].map(priority_map).fillna(2).astype(int)
    )
    merged = merged.sort_values(["session_type_order", value_col],
                                ascending=[True, False])
    return merged["session_id"].tolist()

def plot_units_per_structure_by_stimulus_stacked(df):
    fig, ax = plt.subplots(figsize=(18, 8))
    order = _structure_order(df, "n_units")
    stim_order = _stimulus_order(df, "n_units")
    pivot = df.pivot_table(
        index="brain_structure",
        columns="stimulus_type",
        values="n_units",
        aggfunc="sum",
        fill_value=0,
    ).reindex(order)
    pivot = pivot.reindex(columns=stim_order, fill_value=0)
    pivot.plot(kind="bar", stacked=True, ax=ax, width=0.9)
    ax.set_title("Units per Brain Structure (stacked by Stimulus Type)")
    ax.set_xlabel("Brain Structure")
    ax.set_ylabel("Units")
    ax.legend(loc="upper right", title="Stimulus Type")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "units_per_structure_by_stimulus_stacked.png", dpi=200)
    plt.close(fig)

def plot_presentations_per_structure_by_stimulus_stacked(df):
    fig, ax = plt.subplots(figsize=(18, 8))
    order = _structure_order(df, "n_presentations")
    stim_order = _stimulus_order(df, "n_presentations")
    pivot = df.pivot_table(
        index="brain_structure",
        columns="stimulus_type",
        values="n_presentations",
        aggfunc="sum",
        fill_value=0,
    ).reindex(order)
    pivot = pivot.reindex(columns=stim_order, fill_value=0)
    pivot.plot(kind="bar", stacked=True, ax=ax, width=0.9)
    ax.set_title("Presentations per Brain Structure (stacked by Stimulus Type)")
    ax.set_xlabel("Brain Structure")
    ax.set_ylabel("Presentations")
    ax.legend(loc="upper right", title="Stimulus Type")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "presentations_per_structure_by_stimulus_stacked.png",
                dpi=200)
    plt.close(fig)

def plot_units_per_structure_by_stimulus_multibar(df):
    fig, ax = plt.subplots(figsize=(18, 8))
    order = _structure_order(df, "n_units")
    stim_order = _stimulus_order(df, "n_units")
    pivot = df.pivot_table(
        index="brain_structure",
        columns="stimulus_type",
        values="n_units",
        aggfunc="sum",
        fill_value=0,
    ).reindex(order)
    pivot = pivot.reindex(columns=stim_order, fill_value=0)
    pivot.plot(kind="bar", ax=ax, width=0.9)
    ax.set_title("Units per Brain Structure (grouped by Stimulus)")
    ax.set_xlabel("Brain Structure")
    ax.set_ylabel("Units")
    ax.legend(loc="upper right", title="Stimulus Type")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "units_per_structure_by_stimulus_multibar.png", dpi=200)
    plt.close(fig)

def plot_presentations_per_structure_by_stimulus_multibar(df):
    fig, ax = plt.subplots(figsize=(18, 8))
    order = _structure_order(df, "n_presentations")
    stim_order = _stimulus_order(df, "n_presentations")
    pivot = df.pivot_table(
        index="brain_structure",
        columns="stimulus_type",
        values="n_presentations",
        aggfunc="sum",
        fill_value=0,
    ).reindex(order)
    pivot = pivot.reindex(columns=stim_order, fill_value=0)
    pivot.plot(kind="bar", ax=ax, width=0.9)
    ax.set_title("Presentations per Brain Structure (grouped by Stimulus)")
    ax.set_xlabel("Brain Structure")
    ax.set_ylabel("Presentations")
    ax.legend(loc="upper right", title="Stimulus Type")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "presentations_per_structure_by_stimulus_multibar.png",
                dpi=200)
    plt.close(fig)

def plot_units_per_session_by_structure_stimulus(df):
    stim_types = sorted(df["stimulus_type"].dropna().unique())
    session_order = _session_order_by_type(df, "n_units")
    structure_order = _structure_order(df, "n_units")
    n_rows = len(stim_types)
    fig, axes = plt.subplots(n_rows, 1, figsize=(18, 4 * n_rows))
    if n_rows == 1:
        axes = [axes]

    for i, (ax, stim) in enumerate(zip(axes, stim_types)):
        sub = df[df["stimulus_type"] == stim]
        pivot = sub.pivot_table(
            index="session_id",
            columns="brain_structure",
            values="n_units",
            aggfunc="sum",
            fill_value=0,
        ).reindex(session_order)
        pivot = pivot.reindex(columns=structure_order, fill_value=0)
        pivot.plot(kind="bar", stacked=True, ax=ax, width=0.9, legend=False)
        if i == 0:
            upper_title = "Units per Session (stacked by Brain Structure)\n"
        else:
            upper_title = ""
        ax.set_title(f"{upper_title}{stim}")
        ax.set_ylabel("Units")
        ax.set_xlabel("Session")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right", fontsize=6, ncol=6,
               title="Brain Structure")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "units_per_session_by_structure_stimulus.png", dpi=200)
    plt.close(fig)

def plot_presentations_per_session_by_structure_stimulus(df):
    stim_types = sorted(df["stimulus_type"].dropna().unique())
    session_order = _session_order_by_type(df, "n_presentations")
    structure_order = _structure_order(df, "n_presentations")
    n_rows = len(stim_types)
    fig, axes = plt.subplots(n_rows, 1, figsize=(18, 4 * n_rows))
    if n_rows == 1:
        axes = [axes]

    for i, (ax, stim) in enumerate(zip(axes, stim_types)):
        sub = df[df["stimulus_type"] == stim]
        pivot = sub.pivot_table(
            index="session_id",
            columns="brain_structure",
            values="n_presentations",
            aggfunc="sum",
            fill_value=0,
        ).reindex(session_order)
        pivot = pivot.reindex(columns=structure_order, fill_value=0)
        pivot.plot(kind="bar", stacked=True, ax=ax, width=0.9, legend=False)
        if i == 0:
            upper_title = "Presentations per Session (stacked by Brain Structure)\n"
        else:
            upper_title = ""
        ax.set_title(f"{upper_title}{stim}")
        ax.set_ylabel("Presentations")
        ax.set_xlabel("Session")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right", fontsize=6, ncol=6)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "presentations_per_session_by_structure_stimulus.png",
                dpi=200)
    plt.close(fig)

def plot_units_per_session_by_structure(df):
    fig, ax = plt.subplots(figsize=(18, 8))
    session_order = (
        df.groupby("session_id", as_index=False)["n_units"]
        .sum()
        .sort_values("n_units", ascending=False)["session_id"]
        .tolist()
    )
    structure_order = _structure_order(df, "n_units")
    pivot = df.pivot_table(
        index="session_id",
        columns="brain_structure",
        values="n_units",
        aggfunc="sum",
        fill_value=0,
    ).reindex(session_order)
    pivot = pivot.reindex(columns=structure_order, fill_value=0)
    pivot.plot(kind="bar", stacked=True, ax=ax, width=0.9)
    ax.set_title("Units per Session (stacked by Brain Structure) - All Stimuli")
    ax.set_xlabel("Session")
    ax.set_ylabel("Units")
    ax.legend(loc="upper right", fontsize=6, ncol=6)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "units_per_session_by_structure.png", dpi=200)
    plt.close(fig)

def plot_presentations_per_stimulus(df):
    sessions = _load_session_types()
    per_session = (
        df.groupby(["session_id", "stimulus_type"], as_index=False)["n_presentations"]
        .sum()
    )
    per_session = per_session[per_session["n_presentations"] > 0]
    merged = per_session.merge(sessions, on="session_id", how="left")
    merged["session_type"] = merged["session_type"].fillna("unknown")

    counts = (
        merged.groupby(["stimulus_type", "session_type"], as_index=False)["session_id"]
        .nunique()
        .rename(columns={"session_id": "n_sessions"})
    )
    stim_order = (
        counts.groupby("stimulus_type", as_index=False)["n_sessions"]
        .sum()
        .sort_values("n_sessions", ascending=False)["stimulus_type"]
        .tolist()
    )
    pivot = counts.pivot_table(
        index="stimulus_type",
        columns="session_type",
        values="n_sessions",
        aggfunc="sum",
        fill_value=0,
    ).reindex(stim_order)

    fig, ax = plt.subplots(figsize=(12, 6))
    pivot.plot(kind="bar", stacked=True, ax=ax, width=0.9)
    ax.set_title("Sessions per Stimulus")
    ax.set_xlabel("Stimulus Type")
    ax.set_ylabel("Sessions")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "sessions_per_stimulus.png", dpi=200)
    plt.close(fig)

def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = _load_data()

    plot_units_per_structure_by_stimulus_stacked(df)
    plot_presentations_per_structure_by_stimulus_stacked(df)

    plot_units_per_structure_by_stimulus_multibar(df)
    plot_presentations_per_structure_by_stimulus_multibar(df)

    plot_units_per_session_by_structure_stimulus(df)
    plot_units_per_session_by_structure(df)
    plot_presentations_per_session_by_structure_stimulus(df)

    plot_presentations_per_stimulus(df)

if __name__ == "__main__":
    main()
