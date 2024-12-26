import os
import subprocess
from py1 import main
from collections import defaultdict

# Путь к главной директории, где будет проходить обход
base_dir = os.path.expanduser('~/Work/Code')

# Функция для проверки, является ли директория git-репозиторием
def is_git_repo(directory):
    try:
        # Пытаемся выполнить команду git status в данной директории
        subprocess.check_call(['git', 'status'], cwd=directory, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# Структура для хранения данных по авторам
author_stats = defaultdict(lambda: {
    'total_changed_lines': 0,
    'added': 0,
    'removed': 0
})

# Обходим папки с глубиной 1
for root, dirs, files in os.walk(base_dir, topdown=True):
    # Проверяем, чтобы глубина обхода была 1 (т.е. не заходить в подкаталоги)
    depth = root[len(base_dir):].count(os.sep)
    if depth > 1:
        continue

    # Проверяем, является ли текущая папка Git репозиторием
    if is_git_repo(root):
        print(f"Запускаем функцию main в папке: {root}")
        # Переходим в директорию и запускаем функцию main
        os.chdir(root)
        stats_list = main()

        # Обрабатываем данные для каждого элемента в списке
        for stats in stats_list:
            author = stats['author']
            author_stats[author]['total_changed_lines'] += stats['total_changed_lines']
            author_stats[author]['added'] += stats['added']
            author_stats[author]['removed'] += stats['removed']


# Сортируем авторов по количеству измененных строк в порядке убывания
sorted_authors = sorted(author_stats.items(), key=lambda item: item[1]['total_changed_lines'], reverse=True)

# Выводим итоговую статистику по авторам
print("\nИтоговая статистика по авторам (по убыванию измененных строк):")
for author, stats in sorted_authors:
    print(f"Автор: {author}")
    print(f"  Изменено строк: {stats['total_changed_lines']}")
    print(f"  Добавлено строк: {stats['added']}")
    print(f"  Удалено строк: {stats['removed']}")
    print("-" * 30)
