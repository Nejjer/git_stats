import subprocess
import re
from datetime import datetime, timedelta
import os

# Функция для выполнения команды git и получения результата
def run_git_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Git command failed: {result.stderr}")
    return result.stdout

# Функция для подсчёта изменений строк в указанной директории
def count_lines_of_changes(directory):
    # Проверяем, существует ли директория
    if not os.path.isdir(directory):
        raise ValueError(f"Директория {directory} не существует.")

    # Определим дату 1 год назад от текущей даты
    one_year_ago = datetime.now() - timedelta(days=365)

    # Преобразуем её в формат, который git понимает
    since_date = one_year_ago.strftime('%Y-%m-%d')

    # Получаем список изменений за последний год в указанной директории
    git_log_command = [
        "git", "log", "--since", since_date, "--pretty=format:", "--numstat", "--", directory, ":!package-lock.json"
    ]

    # Выполняем команду git
    log_output = run_git_command(git_log_command)

    # Разбираем вывод, чтобы подсчитать изменения
    added_lines = 0
    removed_lines = 0

    for line in log_output.splitlines():
        # Пример вывода git log: "3       2       file.py"
        # Первая цифра - добавленные строки, вторая - удалённые строки
        match = re.match(r"(\d+)\s+(\d+)\s+", line)
        if match:
            added_lines += int(match.group(1))
            removed_lines += int(match.group(2))

    return added_lines, removed_lines

if __name__ == "__main__":
    # Указываем директорию, которую нужно анализировать (например, "src" или любую другую)
    directory = "./"

    try:
        added, removed = count_lines_of_changes(directory)
        print(f"Изменено строк в директории {directory} за последний год: {added + removed} всего, {added} добавлено, {removed} удалено")
    except Exception as e:
        print(f"Ошибка: {e}")
