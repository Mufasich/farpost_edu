import csv
import mysql.connector
from datetime import datetime, timedelta
import argparse
import pandas as pd

# Параметры подключения к БД
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'mydatabase'
}


def parse_date(date_str):
    """Парсит дату из строки в формате YYYY-MM-DD"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Некорректный формат даты. Используйте YYYY-MM-DD")


def get_daily_stats(start_date, end_date):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Запрос для получения статистики по дням
        query = """
        WITH daily_stats AS (
            SELECT 
                DATE(l.action_date) AS day,
                -- Количество новых аккаунтов
                SUM(CASE WHEN l.action = 'register' AND l.status = 'success' THEN 1 ELSE 0 END) AS new_accounts,
                -- Общее количество сообщений
                SUM(CASE WHEN l.action = 'create_message' THEN 1 ELSE 0 END) AS total_messages,
                -- Количество анонимных сообщений
                SUM(CASE WHEN l.action = 'create_message' AND l.user_id IS NULL THEN 1 ELSE 0 END) AS anonymous_messages,
                -- Количество новых тем
                SUM(CASE WHEN l.action = 'create_theme' AND l.status = 'success' THEN 1 ELSE 0 END) AS new_themes
            FROM logs l
            WHERE DATE(l.action_date) BETWEEN %s AND %s
            GROUP BY DATE(l.action_date)
        ),
        theme_counts AS (
            SELECT 
                DATE(t.created_at) AS day,
                COUNT(*) AS theme_count
            FROM themes t
            WHERE DATE(t.created_at) <= %s
            GROUP BY DATE(t.created_at)
        )
        SELECT 
            ds.day,
            ds.new_accounts,
            ds.total_messages,
            CASE 
                WHEN ds.total_messages > 0 THEN ROUND(ds.anonymous_messages * 100.0 / ds.total_messages, 2)
                ELSE 0 
            END AS anonymous_percentage,
            ds.new_themes,
            COALESCE(
                ROUND(
                    (ds.new_themes * 100.0 / NULLIF(
                        (SELECT SUM(tc2.theme_count) 
                         FROM theme_counts tc2 
                         WHERE tc2.day < ds.day), 0)
                    ), 2
                ), 0
            ) AS theme_growth_percentage
        FROM daily_stats ds
        ORDER BY ds.day;
        """

        cursor.execute(query, (start_date, end_date, end_date))
        results = cursor.fetchall()

        return results

    except mysql.connector.Error as err:
        print(f"Ошибка при работе с БД: {err}")
        return []
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


def save_to_csv(data, filename):
    try:

        df = pd.DataFrame(data)
        df.fillna(0, inplace=True)
        df['new_accounts'] = df['new_accounts'].astype(int)
        df['total_messages'] = df['total_messages'].astype(int)
        df['anonymous_percentage'] = df['anonymous_percentage'].astype(float)
        df['new_themes'] = df['new_themes'].astype(int)
        df['theme_growth_percentage'] = df['theme_growth_percentage'].astype(float)
        df.to_csv(filename, index=False, float_format='%.2f')
        print(f"Данные успешно сохранены в файл {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении в CSV: {e}")


def main():
    parser = argparse.ArgumentParser(description='Агрегация данных форума')
    parser.add_argument('--start', required=True, help='Начальная дата (YYYY-MM-DD)')
    parser.add_argument('--end', required=True, help='Конечная дата (YYYY-MM-DD)')
    parser.add_argument('--output', default='forum_stats.csv', help='Имя выходного файла')

    args = parser.parse_args()

    try:
        start_date = parse_date(args.start)
        end_date = parse_date(args.end)

        if start_date > end_date:
            raise ValueError("Начальная дата не может быть позже конечной")

        # Получаем данные из БД
        stats_data = get_daily_stats(start_date, end_date)

        if stats_data:
            # Преобразуем даты в строки для CSV
            for row in stats_data:
                row['day'] = row['day'].strftime('%Y-%m-%d')

            # Сохраняем в CSV
            save_to_csv(stats_data, args.output)

            # Выводим первые 5 строк для проверки
            print("\nПервые 5 строк данных:")
            for row in stats_data[:5]:
                print(f"{row['day']}: {row['new_accounts']} новых аккаунтов, "
                      f"{row['anonymous_percentage']}% анонимных сообщений, "
                      f"{row['theme_growth_percentage']}% прирост тем")
        else:
            print("Не удалось получить данные из БД или данные отсутствуют")

    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()