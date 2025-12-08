"""
Менеджер для запуска нескольких экземпляров RakLite с разными прокси
"""
import subprocess
import os
import time
import json
from pathlib import Path
from typing import List, Dict, Optional
import threading


class RakLiteManager:
    """Управление экземплярами RakLite"""
    
    def __init__(self, raklite_path: str = "RakLite"):
        self.raklite_path = Path(raklite_path)
        self.processes: Dict[int, subprocess.Popen] = {}
        self.instances_dir = Path("instances")
        self.instances_dir.mkdir(exist_ok=True)
        
    def launch_instance(
        self,
        instance_id: int,
        server_ip: str,
        server_port: int,
        nickname: str,
        proxy: Optional[Dict[str, str]] = None,
        script: Optional[str] = None
    ) -> subprocess.Popen:
        """
        Запускает экземпляр RakLite
        
        Args:
            instance_id: Уникальный ID экземпляра
            server_ip: IP сервера
            server_port: Порт сервера
            nickname: Никнейм игрока
            proxy: Словарь с прокси {'host': ..., 'port': ..., 'username': ..., 'password': ...}
            script: Имя скрипта для запуска (register.lua, login.lua, farm.lua)
        
        Returns:
            subprocess.Popen объект процесса
        """
        # Создаем директорию для экземпляра
        instance_dir = self.instances_dir / f"instance_{instance_id}"
        instance_dir.mkdir(exist_ok=True)
        
        # Копируем необходимые файлы (или создаем символические ссылки)
        # Для Windows используем mklink, для Linux - ln -s
        if os.name == 'nt':  # Windows
            # Создаем символические ссылки на библиотеки
            scripts_dir = instance_dir / "scripts"
            scripts_dir.mkdir(exist_ok=True)
            
            # Копируем libs
            libs_source = self.raklite_path / "scripts" / "libs"
            libs_target = scripts_dir / "libs"
            if not libs_target.exists():
                if os.name == 'nt':
                    os.system(f'mklink /D "{libs_target}" "{libs_source}"')
                else:
                    os.symlink(libs_source, libs_target)
        
        # Настройка прокси
        env = os.environ.copy()
        if proxy:
            if proxy.get('username') and proxy.get('password'):
                proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
            else:
                proxy_url = f"http://{proxy['host']}:{proxy['port']}"
            
            env['HTTP_PROXY'] = proxy_url
            env['HTTPS_PROXY'] = proxy_url
            env['http_proxy'] = proxy_url
            env['https_proxy'] = proxy_url
        
        # Путь к исполняемому файлу
        client_exe = self.raklite_path / "RakSAMP Lite.exe"
        
        if not client_exe.exists():
            raise FileNotFoundError(f"RakSAMP Lite.exe не найден в {self.raklite_path}")
        
        # Запускаем процесс
        process = subprocess.Popen(
            [str(client_exe)],
            env=env,
            cwd=str(instance_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        self.processes[instance_id] = process
        
        # Сохраняем информацию об экземпляре
        instance_info = {
            'instance_id': instance_id,
            'server_ip': server_ip,
            'server_port': server_port,
            'nickname': nickname,
            'proxy': proxy,
            'script': script,
            'pid': process.pid,
            'started_at': time.time()
        }
        
        info_file = instance_dir / "instance_info.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(instance_info, f, indent=2, ensure_ascii=False)
        
        print(f"[{instance_id}] Запущен экземпляр RakLite")
        print(f"  Никнейм: {nickname}")
        print(f"  Сервер: {server_ip}:{server_port}")
        if proxy:
            print(f"  Прокси: {proxy['host']}:{proxy['port']}")
        print(f"  PID: {process.pid}")
        
        return process
    
    def stop_instance(self, instance_id: int):
        """Останавливает экземпляр"""
        if instance_id in self.processes:
            process = self.processes[instance_id]
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            del self.processes[instance_id]
            print(f"[{instance_id}] Экземпляр остановлен")
    
    def stop_all(self):
        """Останавливает все экземпляры"""
        for instance_id in list(self.processes.keys()):
            self.stop_instance(instance_id)
    
    def get_status(self) -> Dict:
        """Возвращает статус всех экземпляров"""
        status = {}
        for instance_id, process in self.processes.items():
            status[instance_id] = {
                'pid': process.pid,
                'running': process.poll() is None,
                'returncode': process.returncode
            }
        return status


def load_accounts(file_path: str) -> List[Dict]:
    """Загружает аккаунты из файла"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_proxies(file_path: str) -> List[Dict]:
    """Загружает прокси из файла"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """Основная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Менеджер RakLite')
    parser.add_argument('--server-ip', default='127.0.0.1', help='IP сервера')
    parser.add_argument('--server-port', type=int, default=7777, help='Порт сервера')
    parser.add_argument('--accounts', default='accounts.json', help='Файл с аккаунтами')
    parser.add_argument('--proxies', default='proxies.json', help='Файл с прокси')
    parser.add_argument('--script', default='farm.lua', help='Скрипт для запуска')
    parser.add_argument('--delay', type=int, default=5, help='Задержка между запусками (сек)')
    parser.add_argument('--count', type=int, help='Количество экземпляров (если не указано - все)')
    
    args = parser.parse_args()
    
    # Загружаем данные
    accounts = load_accounts(args.accounts) if Path(args.accounts).exists() else []
    proxies = load_proxies(args.proxies) if Path(args.proxies).exists() else []
    
    if not accounts:
        print("Создайте файл accounts.json с аккаунтами")
        return
    
    # Создаем менеджер
    manager = RakLiteManager()
    
    try:
        # Запускаем экземпляры
        count = args.count or len(accounts)
        for i in range(min(count, len(accounts))):
            account = accounts[i]
            proxy = proxies[i % len(proxies)] if proxies else None
            
            manager.launch_instance(
                instance_id=i + 1,
                server_ip=args.server_ip,
                server_port=args.server_port,
                nickname=account.get('username', f'Bot_{i+1}'),
                proxy=proxy,
                script=args.script
            )
            
            if i < count - 1:
                time.sleep(args.delay)
        
        print(f"\nЗапущено {count} экземпляров")
        print("Нажмите Ctrl+C для остановки всех экземпляров")
        
        # Ждем завершения
        while True:
            time.sleep(1)
            # Проверяем статус
            status = manager.get_status()
            running = sum(1 for s in status.values() if s['running'])
            if running == 0:
                print("Все экземпляры завершены")
                break
    
    except KeyboardInterrupt:
        print("\nОстановка всех экземпляров...")
        manager.stop_all()


if __name__ == "__main__":
    main()

