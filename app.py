import numpy as np
import streamlit as st
from scipy import stats

st.title("Are you wrong 5% of the time?")

# ---- Controls ----
prior_null = st.slider("Probability the null is true", 0.0, 1.0, 0.5)
effect_size = st.slider("Effect size (if real)", 0.0, 2.0, 0.5)
n = st.slider("Sample size per group", 5, 100, 20)
runs = st.slider("Number of experiments", 1, 500, 50)

# ---- Simulation ----
if st.button("Run experiments"):

    rejections = 0
    false_positives = 0

    for _ in range(runs):

        # Is null true?
        null_true = np.random.rand() < prior_null

        if null_true:
            group1 = np.random.normal(0, 1, n)
            group2 = np.random.normal(0, 1, n)
        else:
            group1 = np.random.normal(0, 1, n)
            group2 = np.random.normal(effect_size, 1, n)

        # t-test
        _, p = stats.ttest_ind(group1, group2)

        # decision
        if p < 0.05:
            rejections += 1
            if null_true:
                false_positives += 1

    # ---- Results ----
    st.subheader("Results")

    st.write(f"You rejected H₀ {rejections} times.")

    if rejections > 0:
        error_rate = false_positives / rejections
        st.write(f"You were wrong {false_positives} times.")
        st.write(f"Estimated probability you're wrong: {error_rate:.2%}")
    else:
        st.write("No rejections yet.")

    st.markdown("---")
    st.write("Claim: 'If p < 0.05, you're wrong only 5% of the time.'")
    st.write("Reality: It depends on how often the null is actually true.")
