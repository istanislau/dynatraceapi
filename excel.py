import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import timedelta

# Leitura das células (ajuste se estiverem em outras colunas/linhas)
dates = pd.to_datetime(xl("B1:Z1"), dayfirst=True)
cpu_values = np.array(xl("B2:Z2")).astype(float)

# Preparar o DataFrame vertical
df = pd.DataFrame({
    "date": dates,
    "cpu": cpu_values
})

# Converter datas para número ordinal
df["timestamp"] = df["date"].map(pd.Timestamp.toordinal).values.reshape(-1, 1)

# Regressão
model = LinearRegression()
model.fit(df["timestamp"], df["cpu"])
trend = model.predict(df["timestamp"])

# Forecast para os próximos 3 meses
future_dates = [df["date"].max() + pd.DateOffset(months=i) for i in range(1, 4)]
future_ordinals = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
forecast = model.predict(future_ordinals)

# Coeficiente de determinação (R²)
r_squared = model.score(df["timestamp"], df["cpu"])

# Gráfico
fig, ax = plt.subplots()
ax.plot(df["date"], df["cpu"], marker='o', label="Top 5% Média CPU")
ax.plot(df["date"], trend, linestyle="--", label="Tendência Linear")
ax.plot(future_dates, forecast, marker='x', color='red', label="Forecast")
ax.set_title(f"Tendência de CPU - R² = {r_squared:.2f}")
ax.set_ylabel("CPU (%)")
ax.legend()
fig.autofmt_xdate()
fig.tight_layout()
plt.show()