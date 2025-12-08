"""
Утилита для обновления списка аккаунтов в config.json
Позволяет легко добавлять/изменять аккаунты
"""
import json
import os


def load_config():
    """Загрузить текущую конфигурацию"""
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_config(config):
    """Сохранить конфигурацию"""
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def show_accounts(config):
    """Показать все аккаунты"""
    print("\n" + "="*60)
    print("Список аккаунтов:")
    print("="*60)
    for i, acc in enumerate(config['accounts']):
        print(f"{i:2d}. {acc['nickname']:20s} | {acc['sandbox']:10s} | {acc['server']}")
    print("="*60)


def add_account(config):
    """Добавить новый аккаунт"""
    print("\n" + "="*60)
    print("Добавление нового аккаунта")
    print("="*60)
    
    sandbox = input("Название песочницы (например, okno21): ")
    nickname = input("Никнейм: ")
    
    print("\nДоступные серверы: SERVER 1, SERVER 2, SERVER 3, SERVER 4, SERVER 5, SERVER 6")
    server = input("Сервер: ")
    
    new_account = {
        "sandbox": sandbox,
        "nickname": nickname,
        "server": server
    }
    
    config['accounts'].append(new_account)
    
    print(f"\n✓ Аккаунт {nickname} добавлен!")
    return config


def edit_account(config):
    """Редактировать существующий аккаунт"""
    show_accounts(config)
    
    try:
        index = int(input("\nНомер аккаунта для редактирования: "))
        
        if index < 0 or index >= len(config['accounts']):
            print("Неверный номер!")
            return config
        
        account = config['accounts'][index]
        
        print(f"\nТекущие данные:")
        print(f"Песочница: {account['sandbox']}")
        print(f"Никнейм: {account['nickname']}")
        print(f"Сервер: {account['server']}")
        print()
        
        print("Введите новые данные (оставьте пустым, чтобы не менять):")
        
        sandbox = input(f"Песочница [{account['sandbox']}]: ") or account['sandbox']
        nickname = input(f"Никнейм [{account['nickname']}]: ") or account['nickname']
        server = input(f"Сервер [{account['server']}]: ") or account['server']
        
        config['accounts'][index] = {
            "sandbox": sandbox,
            "nickname": nickname,
            "server": server
        }
        
        print(f"\n✓ Аккаунт обновлен!")
        return config
        
    except ValueError:
        print("Неверный ввод!")
        return config


def delete_account(config):
    """Удалить аккаунт"""
    show_accounts(config)
    
    try:
        index = int(input("\nНомер аккаунта для удаления: "))
        
        if index < 0 or index >= len(config['accounts']):
            print("Неверный номер!")
            return config
        
        account = config['accounts'][index]
        
        confirm = input(f"Удалить аккаунт '{account['nickname']}'? (y/n): ")
        
        if confirm.lower() in ['y', 'yes', 'д', 'да']:
            del config['accounts'][index]
            print(f"\n✓ Аккаунт удален!")
        else:
            print("Отменено")
        
        return config
        
    except ValueError:
        print("Неверный ввод!")
        return config


def bulk_add_accounts(config):
    """Массовое добавление аккаунтов"""
    print("\n" + "="*60)
    print("Массовое добавление аккаунтов")
    print("="*60)
    print("Формат: nickname,sandbox,server")
    print("Пример: Player1,okno1,SERVER 1")
    print("Введите 'done' когда закончите")
    print()
    
    while True:
        line = input(">>> ")
        
        if line.lower() == 'done':
            break
        
        try:
            parts = [p.strip() for p in line.split(',')]
            
            if len(parts) != 3:
                print("Ошибка: нужно 3 значения через запятую!")
                continue
            
            nickname, sandbox, server = parts
            
            new_account = {
                "sandbox": sandbox,
                "nickname": nickname,
                "server": server
            }
            
            config['accounts'].append(new_account)
            print(f"✓ Добавлен: {nickname}")
            
        except Exception as e:
            print(f"Ошибка: {e}")
    
    return config


def import_from_file(config):
    """Импорт аккаунтов из текстового файла"""
    print("\n" + "="*60)
    print("Импорт аккаунтов из файла")
    print("="*60)
    
    filename = input("Имя файла (например, Аккаунты.txt): ")
    
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден!")
        return config
    
    print("\nФормат файла (выберите):")
    print("1. nickname,sandbox,server")
    print("2. nickname:password (для окон okno1, okno2, ... и SERVER 1)")
    
    format_choice = input("Формат (1/2): ")
    
    added = 0
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            if not line or line.startswith('#'):
                continue
            
            try:
                if format_choice == "1":
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) == 3:
                        nickname, sandbox, server = parts
                        config['accounts'].append({
                            "sandbox": sandbox,
                            "nickname": nickname,
                            "server": server
                        })
                        added += 1
                
                elif format_choice == "2":
                    if ':' in line:
                        nickname = line.split(':')[0].strip()
                        sandbox = f"okno{i}"
                        server = "SERVER 1"
                        config['accounts'].append({
                            "sandbox": sandbox,
                            "nickname": nickname,
                            "server": server
                        })
                        added += 1
            
            except Exception as e:
                print(f"Ошибка в строке {i}: {e}")
        
        print(f"\n✓ Импортировано аккаунтов: {added}")
    
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
    
    return config


def main():
    """Главная функция"""
    
    print("="*60)
    print("Управление аккаунтами RADMIR")
    print("="*60)
    
    config = load_config()
    
    if not config:
        print("\nОШИБКА: config.json не найден!")
        print("Создайте базовый config.json сначала")
        input("Нажмите Enter для выхода...")
        return
    
    while True:
        print("\n" + "="*60)
        print("Меню:")
        print("="*60)
        print("1. Показать все аккаунты")
        print("2. Добавить аккаунт")
        print("3. Редактировать аккаунт")
        print("4. Удалить аккаунт")
        print("5. Массовое добавление")
        print("6. Импорт из файла")
        print("7. Изменить общий пароль")
        print("8. Сохранить и выйти")
        print("9. Выйти без сохранения")
        print()
        
        choice = input("Выбор: ")
        
        if choice == "1":
            show_accounts(config)
        
        elif choice == "2":
            config = add_account(config)
        
        elif choice == "3":
            config = edit_account(config)
        
        elif choice == "4":
            config = delete_account(config)
        
        elif choice == "5":
            config = bulk_add_accounts(config)
        
        elif choice == "6":
            config = import_from_file(config)
        
        elif choice == "7":
            new_password = input("Новый общий пароль: ")
            config['common_password'] = new_password
            print("✓ Пароль обновлен!")
        
        elif choice == "8":
            save_config(config)
            print("\n✓ Конфигурация сохранена!")
            print("Можно запускать main.py")
            break
        
        elif choice == "9":
            confirm = input("Выйти без сохранения? (y/n): ")
            if confirm.lower() in ['y', 'yes', 'д', 'да']:
                print("Изменения не сохранены")
                break
        
        else:
            print("Неверный выбор!")
    
    input("\nНажмите Enter для выхода...")


if __name__ == "__main__":
    main()

