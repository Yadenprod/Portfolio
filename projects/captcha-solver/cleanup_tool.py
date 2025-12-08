#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Утилита для очистки временных файлов и кэша
"""

import os
import time
import glob
from datetime import datetime, timedelta
from typing import List

class CleanupTool:
    """Инструмент для очистки временных файлов"""
    
    def __init__(self, max_age_hours: int = 24):
        self.max_age_hours = max_age_hours
        self.patterns_to_clean = [
            "temp_captcha_*.png",
            "dtp_block_*.png",
            "*.tmp",
            "*.log"
        ]
        self.directories_to_clean = [
            "cache",
            "temp", 
            "logs",
            "screenshots"
        ]
    
    def clean_old_files(self, dry_run: bool = False) -> List[str]:
        """Очистка старых файлов"""
        removed_files = []
        expire_time = datetime.now() - timedelta(hours=self.max_age_hours)
        
        print(f"🧹 Очистка файлов старше {self.max_age_hours} часов...")
        
        # Очищаем файлы по паттернам
        for pattern in self.patterns_to_clean:
            files = glob.glob(pattern)
            for file_path in files:
                try:
                    if os.path.isfile(file_path):
                        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                        if file_time < expire_time:
                            if dry_run:
                                print(f"   🗑️ Будет удален: {file_path}")
                            else:
                                os.remove(file_path)
                                print(f"   ✅ Удален: {file_path}")
                            removed_files.append(file_path)
                except Exception as e:
                    print(f"   ❌ Ошибка удаления {file_path}: {e}")
        
        # Очищаем директории
        for dir_name in self.directories_to_clean:
            if os.path.exists(dir_name):
                removed_files.extend(self._clean_directory(dir_name, expire_time, dry_run))
        
        return removed_files
    
    def _clean_directory(self, directory: str, expire_time: datetime, dry_run: bool) -> List[str]:
        """Очистка директории"""
        removed_files = []
        
        try:
            for root, dirs, files in os.walk(directory):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    try:
                        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                        if file_time < expire_time:
                            if dry_run:
                                print(f"   🗑️ Будет удален: {file_path}")
                            else:
                                os.remove(file_path)
                                print(f"   ✅ Удален: {file_path}")
                            removed_files.append(file_path)
                    except Exception as e:
                        print(f"   ❌ Ошибка удаления {file_path}: {e}")
        except Exception as e:
            print(f"   ❌ Ошибка обхода директории {directory}: {e}")
        
        return removed_files
    
    def get_disk_usage(self) -> dict:
        """Получение информации об использовании диска"""
        current_dir = os.getcwd()
        
        # Размер временных файлов
        temp_size = 0
        temp_count = 0
        
        for pattern in self.patterns_to_clean:
            files = glob.glob(pattern)
            for file_path in files:
                try:
                    if os.path.isfile(file_path):
                        temp_size += os.path.getsize(file_path)
                        temp_count += 1
                except Exception:
                    pass
        
        # Размер кэша
        cache_size = 0
        cache_count = 0
        
        if os.path.exists("cache"):
            for root, dirs, files in os.walk("cache"):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    try:
                        cache_size += os.path.getsize(file_path)
                        cache_count += 1
                    except Exception:
                        pass
        
        return {
            "temp_files_count": temp_count,
            "temp_files_size_mb": temp_size / (1024 * 1024),
            "cache_files_count": cache_count,
            "cache_files_size_mb": cache_size / (1024 * 1024),
            "total_size_mb": (temp_size + cache_size) / (1024 * 1024)
        }
    
    def show_cleanup_report(self):
        """Показать отчет о состоянии файлов"""
        print("📊 Отчет о временных файлах:")
        print("=" * 50)
        
        usage = self.get_disk_usage()
        
        print(f"📁 Временные файлы: {usage['temp_files_count']} ({usage['temp_files_size_mb']:.2f} MB)")
        print(f"💾 Файлы кэша: {usage['cache_files_count']} ({usage['cache_files_size_mb']:.2f} MB)")
        print(f"📊 Общий размер: {usage['total_size_mb']:.2f} MB")
        
        # Показываем старые файлы
        print(f"\n🕐 Файлы старше {self.max_age_hours} часов:")
        old_files = self.clean_old_files(dry_run=True)
        
        if old_files:
            print(f"   🗑️ К удалению: {len(old_files)} файлов")
        else:
            print("   ✅ Старых файлов не найдено")

def main():
    """Основная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Очистка временных файлов ГИБДД чекера")
    parser.add_argument("--hours", type=int, default=24, help="Возраст файлов в часах для удаления")
    parser.add_argument("--dry-run", action="store_true", help="Показать что будет удалено без удаления")
    parser.add_argument("--report", action="store_true", help="Показать отчет о файлах")
    
    args = parser.parse_args()
    
    cleaner = CleanupTool(max_age_hours=args.hours)
    
    if args.report:
        cleaner.show_cleanup_report()
    else:
        removed_files = cleaner.clean_old_files(dry_run=args.dry_run)
        
        if removed_files:
            print(f"\n✅ {'Будет удалено' if args.dry_run else 'Удалено'}: {len(removed_files)} файлов")
        else:
            print("\n✅ Нет файлов для удаления")

if __name__ == "__main__":
    main() 