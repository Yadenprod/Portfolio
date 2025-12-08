"""
Скрипт для автоматизации диалога Sandboxie
Запускайте когда диалог "Запустить в песочнице" уже открыт
"""
import time
from pywinauto import Desktop


def automate_dialog(sandbox_name: str = "okno2", enable_uac: bool = True):
    """
    Автоматизирует диалог Sandboxie
    
    Args:
        sandbox_name: Имя песочницы для выбора
        enable_uac: Поставить ли галочку UAC
    """
    print(f"Ищем диалог Sandboxie...")
    
    desktop = Desktop(backend="uia")
    
    # Ищем диалог
    dialog = None
    for attempt in range(10):
        try:
            windows = desktop.windows()
            for win in windows:
                try:
                    title = win.window_text()
                    if "Запустить в песочнице" in title or "Run Sandboxed" in title:
                        dialog = win
                        print(f"Найден диалог: {title}")
                        break
                except:
                    continue
            if dialog:
                break
            time.sleep(1)
        except:
            time.sleep(1)
    
    if not dialog:
        print("Диалог не найден!")
        return False
    
    # Выбираем песочницу из списка
    print(f"Выбираем песочницу: {sandbox_name}")
    selected = False
    
    try:
        # Ищем ListBox с песочницами
        for child in dialog.descendants():
            try:
                control_type = str(child.element_info.control_type)
                if "ListBox" in control_type or "List" in control_type:
                    # Нашли список
                    print(f"Найден список песочниц")
                    
                    # Ищем нужный элемент в списке
                    for item in child.descendants():
                        try:
                            if item.window_text() == sandbox_name:
                                item.click_input()
                                print(f"✓ Выбрана песочница: {sandbox_name}")
                                selected = True
                                time.sleep(0.5)
                                break
                        except:
                            continue
                    
                    if selected:
                        break
            except:
                continue
    except Exception as e:
        print(f"Ошибка выбора песочницы: {e}")
    
    if not selected:
        print("⚠ Песочница не выбрана, используем по умолчанию")
    
    # Ставим галочку UAC
    if enable_uac:
        print("Ищем чекбокс UAC...")
        uac_found = False
        
        try:
            for child in dialog.descendants():
                try:
                    text = child.window_text()
                    control_type = str(child.element_info.control_type)
                    
                    if ("UAC" in text or "Администратор" in text or "администратор" in text.lower()) and "CheckBox" in control_type:
                        print(f"Найден чекбокс: {text}")
                        
                        # Проверяем состояние
                        try:
                            state = child.get_toggle_state()
                            if state == 0:  # Не отмечен
                                child.click_input()
                                print("✓ Поставлена галочка UAC")
                                uac_found = True
                            else:
                                print("✓ Галочка UAC уже стоит")
                                uac_found = True
                        except:
                            # Если get_toggle_state не работает, просто кликаем
                            child.click_input()
                            print("✓ Кликнули по чекбоксу UAC")
                            uac_found = True
                        
                        time.sleep(0.5)
                        break
                except:
                    continue
        except Exception as e:
            print(f"Ошибка при работе с UAC: {e}")
        
        if not uac_found:
            print("⚠ Чекбокс UAC не найден")
    
    # Нажимаем OK
    print("Ищем кнопку OK...")
    ok_clicked = False
    
    try:
        for child in dialog.descendants():
            try:
                text = child.window_text()
                control_type = str(child.element_info.control_type)
                
                if text == "OK" and "Button" in control_type:
                    child.click_input()
                    print("✓ Нажата кнопка OK")
                    ok_clicked = True
                    time.sleep(0.5)
                    break
            except:
                continue
    except Exception as e:
        print(f"Ошибка при нажатии OK: {e}")
    
    if not ok_clicked:
        print("⚠ Кнопка OK не найдена")
        return False
    
    print("✓ Диалог автоматизирован успешно!")
    return True


if __name__ == "__main__":
    import sys
    
    print("="*60)
    print("Автоматизация диалога Sandboxie")
    print("="*60)
    print()
    print("ИНСТРУКЦИЯ:")
    print("1. Откройте диалог 'Запустить в песочнице' вручную")
    print("2. Запустите этот скрипт")
    print("3. Скрипт автоматически выберет песочницу и поставит галочку UAC")
    print()
    
    sandbox = input("Введите имя песочницы (по умолчанию okno2): ").strip() or "okno2"
    
    print()
    print("Ожидание 3 секунды... Откройте диалог СЕЙЧАС!")
    time.sleep(3)
    
    success = automate_dialog(sandbox, enable_uac=True)
    
    if success:
        print()
        print("✓ Успешно!")
    else:
        print()
        print("✗ Не удалось автоматизировать диалог")
    
    input("\nНажмите Enter для выхода...")

