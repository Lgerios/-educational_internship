import pandas as pd

START = pd.Timestamp("2026-01-01")
END = pd.Timestamp("2026-04-01")  
sessions = pd.read_csv("Sessions_analytics.csv", encoding="utf-8-sig", parse_dates=["session_start", "session_end"])
orders = pd.read_csv("Orders_analytics.csv", encoding="utf-8-sig", parse_dates=["order_datetime"])
items = pd.read_csv("Order_items_analytics.csv", encoding="utf-8-sig")
models = pd.read_csv("Shoe_models_analytics.csv", encoding="utf-8-sig")


for frame, columns in [(sessions, ["device_type", "traffic_source"]), (orders, ["order_status"])]:
    for column in columns:
        frame[column] = frame[column].astype(str).str.strip().str.lower()


sessions = sessions[(sessions.session_start >= START) & (sessions.session_start < END)]
orders = orders[(orders.order_datetime >= START) & (orders.order_datetime < END)]
completed = orders[orders.order_status == "completed"]
completed_items = items[items.order_id.isin(completed.order_id)]

# 5.1 Конверссия по типу устройства
visitors = sessions.groupby("device_type").user_id.nunique() 
buyers_orders = completed.merge(sessions[["session_id", "device_type"]], on="session_id")
buyers = buyers_orders.groupby("device_type").user_id.nunique() 
conversion = (buyers / visitors).fillna(0).sort_values(ascending=False)
print("5.1 конверсия по устройствам:\n", conversion.round(4).to_string())
print("ОТВЕТ 5.1:", conversion.idxmax(), "\n")

#5.2 Медианое время до первой покупки (минуты <= 7 суток)
first_visit = sessions.groupby("user_id").session_start.min()
first_purchase = completed.groupby("user_id").order_datetime.min()
delta = (first_purchase - first_visit).dropna()
delta = delta[(delta >= pd.Timedelta(0)) & (delta <= pd.Timedelta(days=7))]
median_minutes = delta.dt.total_seconds().div(60).median()
print(f"5.2 пользователей учтено: {len(delta)}")
print("ОТВЕТ 5.2:", round(median_minutes, 2), "мин\n")

# 5.3 Удержание в феврале по каналам
first_session = sessions.sort_values("session_start").groupby("user_id").first()
january_users = first_session[(first_session.session_start >= "2026-01-01") & (first_session.session_start < "2026-02-01")]
february_users = set(sessions[(sessions.session_start >= "2026-02-01") & (sessions.session_start < "2026-03-01")].user_id)
january_users = january_users.assign(returned=january_users.index.isin(february_users))
retention = january_users.groupby("traffic_source").returned.mean().sort_values(ascending=False)
print("5.3 удержание:\n", retention.round(4).to_string())
print("ОТВЕТ 5.3:", retention.idxmax(), "\n")

# 5.4 Выбросы по стоимости заказа (IQR)
order_cost = completed_items.groupby("order_id").item_total.sum()
q1, q3 = order_cost.quantile(0.25), order_cost.quantile(0.75)
iqr = q3 - q1
low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
remaining = order_cost[(order_cost >= low) & (order_cost <= high)]
print(f"5.4 Q1={q1}, Q3={q3}, границы=[{low}; {high}], всего заказов={len(order_cost)}")
print("ОТВЕТ 5.4:", len(remaining), "\n")

#  5.5 Корреляция Пирсона: скидка и количество
correlation = completed_items.discount_percent.corr(completed_items.quantity)
print("ОТВЕТ 5.5:", f"{correlation:.3f}", "\n")

# 5.6 Категория с максимумом проданных пар 
by_category = completed_items.merge(models[["model_id", "category"]], on="model_id") \
    .groupby("category").quantity.sum().sort_values(ascending=False)
print("5.6 пары по категориям:\n", by_category.to_string())
print("ОТВЕТ 5.6:", by_category.idxmax())
