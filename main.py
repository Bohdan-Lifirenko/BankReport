import pandas as pd

if __name__ == "__main__":
    # Читання першої таблиці (firms) з CSV
    df_firms = pd.read_csv('data/firms.csv')

    # Читання другої таблиці (fin_values) з CSV
    df_fin_values = pd.read_csv('data/fin_values.csv')

    print("df_firms column types:")
    print(df_firms.dtypes)

    print("df_firms info:")
    print(df_firms.info())

    # Перевірка даних
    print("Початок firms:")
    print(df_firms.head())  # Показати перші 5 рядків

    print("\nКінець firms:")
    print(df_firms.tail())

    print("\nрядки, стовпці:")
    print(df_firms.shape)

    print("\nназви стовпців")
    print(df_firms.columns)

    print("\n name до сортування:")
    print(df_firms["name"].head())

    print("Відсортовано по name:")
    df_firms.sort_values(by="name", ascending=True)
    print(df_firms["name"].head())  # Показати перші 5 рядків

    print("\nТаблиця fin_values:")
    print(df_fin_values.head())

    # Об'єднання таблиць за 'tax_id' (один-до-багатьох, як LEFT JOIN)
    # Це створить нову таблицю, де для кожного рядка з firms буде кілька рядків з fin_values
    merged_df = pd.merge(df_firms, df_fin_values, on='tax_id', how='left')

    print("\nОб'єднана таблиця:")
    print(merged_df.head())
