import numpy as np
import streamlit as st
from scipy import stats
import matplotlib.pyplot as plt

st.title("Is your one result trustworthy?")

st.write("""
You run ONE study and get a p-value.

But how should you interpret that ONE result?

This app lets you:
1) Run your own study
2) Then zoom out and see how often results like yours happen
""")

# -------------------------
# Controls
# -------------------------
st.sidebar.header("Set the world")

prior_null = st.sidebar.slider(
    "How often is there actually NO effect?",
    0.0, 1.0, 0.5
)

effect_size = st.sidebar.slider(
    "Effect size (when there IS an effect)",
    0.0, 2.0, 0.5
)

n = st.sidebar.slider(
    "Sample size per group",
    5, 100, 20
)

runs = st.sidebar.slider(
    "Number of studies in the 'long run'",
    50, 1000, 300
)

# -------------------------
# Function to run one study
# -------------------------
def run_experiment():
    null_true = np.random.rand() < prior_null

    if null_true:
        group1 = np.random.normal(0, 1, n)
        group2 = np.random.normal(0, 1, n)
    else:
        group1 = np.random.normal(0, 1, n)
        group2 = np.random.normal(effect_size, 1, n)

    _, p = stats.ttest_ind(group1, group2)

    return p, null_true

# -------------------------
# Run ONE study
# -------------------------
if st.button("Run ONE study"):

    p_user, null_user = run_experiment()

    st.subheader("Your study")

    st.write(f"p-value: {p_user:.3f}")

    if p_user < 0.05:
        st.write("🎉 Significant result!")
    else:
        st.write("Not significant.")

    # Reveal truth
    st.markdown("**Hidden truth 🎭 (you don't know this in real life):**")
    if null_user:
        st.write("There was actually NO effect.")
    else:
        st.write("There WAS a real effect.")

    # -------------------------
    # Simulate MANY studies
    # -------------------------
    p_values = []
    labels = []  # for coloring

    rejections = 0
    false_positives = 0
    total_null_true = 0
    false_negatives = 0

    for _ in range(runs):
        p_sim, null_sim = run_experiment()
        p_values.append(p_sim)

        if null_sim:
            total_null_true += 1

        # classify outcomes
        if p_sim < 0.05:
            rejections += 1
            if null_sim:
                false_positives += 1
                labels.append("false_positive")
            else:
                labels.append("true_positive")
        else:
            if null_sim:
                labels.append("true_negative")
            else:
                false_negatives += 1
                labels.append("false_negative")

    # -------------------------
    # Plot p-values
    # -------------------------
    st.markdown("---")
    st.subheader("Each dot = one study")

    fig, ax = plt.subplots()

    x = np.arange(len(p_values))

    colors = []
    for lab in labels:
        if lab == "true_positive":
            colors.append("green")
        elif lab == "false_positive":
            colors.append("red")
        elif lab == "true_negative":
            colors.append("lightgray")
        else:  # false_negative
            colors.append("blue")

    ax.scatter(x, p_values, c=colors, alpha=0.7)

    # highlight user's result
    ax.axhline(y=p_user, linestyle="--")
    ax.text(len(p_values)*0.7, p_user, "Your study", fontsize=10)

    ax.axhline(y=0.05, linestyle=":", color="black")

    ax.set_ylabel("p-value")
    ax.set_xlabel("Study")
    ax.set_ylim(0, 1)

    st.pyplot(fig)

    # -------------------------
    # Legend
    # -------------------------
    st.write("""
Color key:
- 🟢 Green = real effect, correctly detected  
- 🔴 Red = false alarm (no effect, but significant)  
- 🔵 Blue = missed real effect  
- ⚪ Gray = correctly found nothing  
""")

    # -------------------------
    # Long-run results
    # -------------------------
    st.markdown("---")
    st.subheader("What’s happening across all studies?")

    st.write(f"Total studies: {runs}")
    st.write(f"No real effect: {total_null_true}")
    st.write(f"Real effect present: {runs - total_null_true}")

    st.markdown("---")

    st.write(f"Significant results: {rejections}")
    st.write(f"False alarms: {false_positives}")
    st.write(f"Missed real effects: {false_negatives}")

    if rejections > 0:
        error_rate = false_positives / rejections
        st.write(f"→ Among significant results, {error_rate:.2%} are false alarms")

    overall_error = (false_positives + false_negatives) / runs
    st.write(f"Overall error rate: {overall_error:.2%}")

    # -------------------------
    # Final insight
    # -------------------------
    st.markdown("---")
    st.subheader("Now interpret YOUR result")

    st.write("""
Your study is just ONE dot on this plot.

Even if your result is significant:
- It could be a real effect (green)
- Or a false alarm (red)

The p-value alone does NOT tell you which one you have.
""")

    st.write("👉 Your result is one draw from this noisy process.")
