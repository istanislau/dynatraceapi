from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

# Datas
dates_past = pd.to_datetime(xl("L3:W3"), dayfirst=True)
dates_future = pd.to_datetime(xl("X3:AI3"), dayfirst=True)

# Dados de CPU
cpu_matrix = np.array(xl("L4:W100")).astype(float)

# Datas para regressão
X_past = dates_past.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
X_future = dates_future.map(pd.Timestamp.toordinal).values.reshape(-1, 1)

# Listas de saída
projection_matrix = []
slope_list = []
r2_list = []

# Loop por linha
for row in cpu_matrix:
    if np.isnan(row).all():
        projection_matrix.append([np.nan] * len(X_future))
        slope_list.append(np.nan)
        r2_list.append(np.nan)
        continue

    model = LinearRegression()
    model.fit(X_past, row)
    forecast = model.predict(X_future)

    # Clipping: entre 0% e 100%
    forecast_clipped = np.clip(forecast, 0, 100)

    # R² da regressão
    r_squared = model.score(X_past, row)

    projection_matrix.append(forecast_clipped.tolist())
    slope_list.append(model.coef_[0])
    r2_list.append(r_squared)

# Retorna os 3 blocos:
# previsões, slope, e R²
projection_matrix, slope_list, r2_list