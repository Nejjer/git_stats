import subprocess
from collections import defaultdict

# Функция для выполнения команды git и получения результата
def run_git_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

# Функция для получения информации о коммитах за последний год
def get_commits():
    # Получаем список всех коммитов за последний год с данными о коммите, авторе и изменениях
    command = [
        'git', 'log', '--since="1 year ago"', '--pretty=format:%H|%ae', '--numstat', '--', ':!package-lock.json'
    ]
    commits = run_git_command(command).splitlines()
    return commits

# Функция для парсинга данных коммитов и подсчёта строк
def count_lines(commits):
    authors = defaultdict(lambda: {'added': 0, 'removed': 0})

    current_commit_author = None

    for line in commits:
        # Если строка содержит информацию о коммите (хэш и email)
        if '|' in line:
            commit_hash, author_email = line.split('|')
            current_commit_author = author_email
        elif line.strip():  # Если строка не пустая (данные о добавленных/удалённых строках)
            parts = line.split()
            if len(parts) == 3:
                try:
                    added, removed, _ = parts
                    added = int(added) if added.isdigit() else 0
                    removed = int(removed) if removed.isdigit() else 0

                    # Суммируем количество добавленных и удалённых строк для автора
                    authors[current_commit_author]['added'] += added
                    authors[current_commit_author]['removed'] += removed
                except ValueError:
                    continue  # Если строки не удалось распарсить, пропускаем их

    return authors

# Основная функция
def main():
    commits = get_commits()
    authors = count_lines(commits)

    # Сортируем авторов по количеству добавленных строк в порядке убывания
    sorted_authors = sorted(authors.items(), key=lambda x: x[1]['added'], reverse=True)

    # Составляем результат, который будет возвращен
    result = []
    for author, stats in sorted_authors:
        total_changed_lines = stats['added'] + stats['removed']
        print('===============================')
        print(author)
        print('total_changed_lines -', total_changed_lines)
        print('added -', stats['added'])
        print('removed -', stats['removed'])
        result.append({
            'author': author,
            'total_changed_lines': total_changed_lines,
            'added': stats['added'],
            'removed': stats['removed']
        })

    return result

if __name__ == "__main__":
    main()
