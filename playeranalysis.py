import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
df = pd.read_csv("player_stats_final.csv")
df = df.drop(columns=['team_position', 'reactions', 'player_name'])
df.rename(columns={'overall': 'overall_rating', 'rating': 'market_value'}, inplace=True)

# Define features
X_market = df[['age', 'overall_rating', 'potential', 'finishing', 'short_passing',
               'interceptions', 'standing_tackle', 'stamina']]
X_overall = df[['age', 'potential', 'finishing', 'short_passing',
                'interceptions', 'standing_tackle', 'stamina']]

y_overall = df['overall_rating']
y_market = df['market_value']

# Train-test split
X_train_o, X_test_o, y_train_o, y_test_o = train_test_split(X_overall, y_overall, test_size=0.2, random_state=42)
X_train_m, X_test_m, y_train_m, y_test_m = train_test_split(X_market, y_market, test_size=0.2, random_state=42)

# Train models
model_overall = RandomForestRegressor(n_estimators=100, random_state=42)
model_overall.fit(X_train_o, y_train_o)

model_market = RandomForestRegressor(n_estimators=100, random_state=42)
model_market.fit(X_train_m, y_train_m)

# Evaluate models
preds_o = model_overall.predict(X_test_o)
mse_overall = mean_squared_error(y_test_o, preds_o)
r2_overall = r2_score(y_test_o, preds_o)

preds_m = model_market.predict(X_test_m)
mse_market = mean_squared_error(y_test_m, preds_m)
r2_market = r2_score(y_test_m, preds_m)

# Currency rates
currency_rates = {
    'USD': 1.0, 'EUR': 0.93, 'GBP': 0.81, 'INR': 83.10, 'JPY': 155.46,
    'CNY': 7.23, 'AED': 3.67, 'NGN': 1425.50, 'BRL': 5.15, 'CAD': 1.36,
    'AUD': 1.52, 'ZAR': 18.79, 'MXN': 17.10, 'RUB': 93.25, 'PKR': 278.50,
    'BDT': 117.50, 'EGP': 47.00, 'KES': 131.40, 'TRY': 32.00, 'THB': 36.80
}

# Streamlit UI
st.title("⚽ Real-Time Football Player Performance Prediction")

# Model performance
st.subheader("📊 Model Performance")
st.markdown("**Overall Rating Prediction**")
st.write(f"• R² Score: **{r2_overall:.3f}**")
st.write(f"• Mean Squared Error: **{mse_overall:.2f}**")

st.markdown("**Market Value Prediction**")
st.write(f"• R² Score: **{r2_market:.3f}**")
st.write(f"• Mean Squared Error: **${mse_market:,.2f}**")

# Feature importance
st.subheader("📈 Feature Importance (Market Value)")
importances = model_market.feature_importances_
features = X_market.columns
indices = np.argsort(importances)

fig, ax = plt.subplots()
ax.barh(features[indices], importances[indices])
ax.set_xlabel("Importance Score")
st.pyplot(fig)

# Prediction vs Actual
st.subheader("📉 Predicted vs Actual Market Value")
fig2, ax2 = plt.subplots()
ax2.scatter(y_test_m, preds_m, alpha=0.6, color='purple')
ax2.plot([y_test_m.min(), y_test_m.max()], [y_test_m.min(), y_test_m.max()], 'r--')
ax2.set_xlabel("Actual Market Value")
ax2.set_ylabel("Predicted Market Value")
st.pyplot(fig2)

# Prediction Tabs
st.header("🧮 Make Predictions")
tab1, tab2 = st.tabs(["🎯 Predict Overall Rating", "💸 Predict Market Value"])

# === Overall Rating Tab ===
with tab1:
    st.subheader("🎯 Inputs for Overall Rating")
    age = st.slider("Age", 16, 45, 25, key="age_o")
    potential = st.slider("Potential", 40, 99, 80, key="potential_o")
    finishing = st.slider("Finishing", 0, 99, 60, key="finishing_o")
    short_passing = st.slider("Short Passing", 0, 99, 65, key="short_passing_o")
    interceptions = st.slider("Interceptions", 0, 99, 50, key="interceptions_o")
    standing_tackle = st.slider("Standing Tackle", 0, 99, 55, key="standing_tackle_o")
    stamina = st.slider("Stamina", 0, 99, 70, key="stamina_o")

    if st.button("🔮 Predict Overall Rating"):
        input_overall = pd.DataFrame({
            'age': [age],
            'potential': [potential],
            'finishing': [finishing],
            'short_passing': [short_passing],
            'interceptions': [interceptions],
            'standing_tackle': [standing_tackle],
            'stamina': [stamina]
        })
        predicted_overall = model_overall.predict(input_overall)[0]
        st.success(f"🏅 Predicted Overall Rating: **{predicted_overall:.1f}**")

# === Market Value Tab ===
with tab2:
    st.subheader("💸 Inputs for Market Value")
    age_m = st.slider("Age", 16, 45, 25, key="age_m")
    overall_rating_input = st.slider("Overall Rating", 40, 99, 75, key="overall_rating_m")
    potential_m = st.slider("Potential", 40, 99, 80, key="potential_m")
    finishing_m = st.slider("Finishing", 0, 99, 60, key="finishing_m")
    short_passing_m = st.slider("Short Passing", 0, 99, 65, key="short_passing_m")
    interceptions_m = st.slider("Interceptions", 0, 99, 50, key="interceptions_m")
    standing_tackle_m = st.slider("Standing Tackle", 0, 99, 55, key="standing_tackle_m")
    stamina_m = st.slider("Stamina", 0, 99, 70, key="stamina_m")
    currency = st.selectbox("🌍 Choose Currency", list(currency_rates.keys()))

    if st.button("💰 Predict Market Value"):
        input_market = pd.DataFrame({
            'age': [age_m],
            'overall_rating': [overall_rating_input],
            'potential': [potential_m],
            'finishing': [finishing_m],
            'short_passing': [short_passing_m],
            'interceptions': [interceptions_m],
            'standing_tackle': [standing_tackle_m],
            'stamina': [stamina_m]
        })

        all_tree_preds = np.array([tree.predict(input_market)[0] for tree in model_market.estimators_])
        mean_pred_usd = np.mean(all_tree_preds)
        std_pred_usd = np.std(all_tree_preds)

        lower_usd = mean_pred_usd - 1.96 * std_pred_usd
        upper_usd = mean_pred_usd + 1.96 * std_pred_usd

        converted_mean = mean_pred_usd * currency_rates[currency]
        converted_lower = lower_usd * currency_rates[currency]
        converted_upper = upper_usd * currency_rates[currency]

        st.success(f"💰 Predicted Market Value: **{converted_mean:,.2f} {currency}**")
        st.info(f"📊 95% Confidence Interval: {converted_lower:,.2f} - {converted_upper:,.2f} {currency}")

        result_df = input_market.copy()
        result_df['Predicted Market Value'] = converted_mean
        result_df['Lower Bound'] = converted_lower
        result_df['Upper Bound'] = converted_upper

        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Market Value Prediction as CSV",
            data=csv,
            file_name='market_value_prediction.csv',
            mime='text/csv'
        )

# Model Info
with st.expander("ℹ️ About the Model"):
    st.markdown("""
    - This app predicts a football player's **Overall Rating** and **Market Value** using separate Random Forest models.
    - It avoids data leakage by not using `overall_rating` to predict itself.
    - Market value includes a **95% confidence interval**.
    - Currency rates are approximate (2024).
    """)
# Project-Report-Real-Time-Football-Player-Performance-Prediction-
