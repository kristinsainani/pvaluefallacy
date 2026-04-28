import numpy as np
import streamlit as st
from scipy import stats

st.title("Does p < 0.05 mean your result is real?")

st.write("""
In any one study, the effect is either real or it isn’t.

But when you see p < 0.05, you don’t know which case you're in.

This app shows what fraction of 'significant' results are actually real.
""")

# -------------------------
# Controls
# -------------------------
st.sidebar.header("Set the world")

prior_real = st.sidebar.slider(
    "How often are effects actually real?",
    0.0, 1.0, 0.3
)

effect_size = st.sidebar.slider(
    "Effect size (when real)",
    0.0, 2.0, 0.5
)

n = st.sidebar.slider(
    "Sample size per group",
    5, 100, 20
)

runs = st.sidebar.slider(
    "Number of studies",
    50, 2000, 500
)

# -------------------------
# Simulation function
# -------------------------
def run_experiment():
    real = np.random.rand() < prior_real

    if real:
        group1 = np.random.normal(0, 1, n)
        group2 = np.random.normal(effect_size, 1, n)
    else:
        group1 = np.random.normal(0, 1, n)
        group2 = np.random.normal(0, 1, n)

    _, p = stats.ttest_ind(group1, group2)
    return p, real

# -------------------------
# Run simulation
# -------------------------
if st.button("Run studies"):

    claims = 0
    true_discoveries = 0
    false_alarms = 0

    for _ in range(runs):
        p, real = run_experiment()

        if p < 0.05:
            claims += 1
            if real:
                true_discoveries += 1
            else:
                false_alarms += 1

    st.markdown("---")
    st.subheader("What happened")

    st.write(f"Total studies: {runs}")
    st.write(f"Significant results (p < 0.05): {claims}")

    st.write(f"Real discoveries: {true_discoveries}")
    st.write(f"False alarms: {false_alarms}")

    if claims > 0:
        prob_real = true_discoveries / claims
        st.markdown(f"## 👉 Chance a 'significant' result is real: {prob_real:.2%}")

    st.markdown("---")

    st.write("""
p < 0.05 does NOT mean:

❌ “There is a 95% chance this result is real”

Instead:

✔ It tells you how surprising your data would be if nothing were happening.

---

To know how often significant results are real, you need to consider:

- How often effects are actually real
- How strong they are
- How much data you collect
""")
