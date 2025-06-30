from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

# Datas e valores
dates_past = pd.to_datetime(xl("L3:W3"), dayfirst=True)
cpu_values = np.array(xl("L20:W20")).astype(float).flatten()

dates_future = pd.to_datetime(xl("X3:AI3"), dayfirst=True)

# Regressão
X_past = dates_past.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
X_future = dates_future.map(pd.Timestamp.toordinal).values.reshape(-1, 1)

model = LinearRegression()
model.fit(X_past, cpu_values)

forecast = model.predict(X_future)
forecast_clipped = np.clip(forecast, 0, 100)

slope = model.coef_[0]
r2 = model.score(X_past, cpu_values)

# Retorna: [linha de previsão], slope, r²
forecast_clipped.tolist(), slope, r2