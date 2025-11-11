#!/usr/bin/env python3
"""
Простой скрипт для запуска FastAPI сервера с ngrok туннелем
"""

import subprocess
import sys
import time
import os
import signal

def kill_port(port):
    """Убивает процесс на порту"""
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            result = subprocess.run(
                ['lsof', '-ti', f':{port}'],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        # Сначала пробуем мягко
                        os.kill(int(pid), signal.SIGTERM)
                        time.sleep(1)
                        # Потом жестко если не помогло
                        os.kill(int(pid), signal.SIGKILL)
                        print(f"✓ Остановлен процесс {pid} на порту {port}")
                    except ProcessLookupError:
                        pass  # Процесс уже завершен
                    except:
                        pass
                time.sleep(2)
            else:
                break  # Порт свободен
        except:
            pass
    
    # Финальная проверка через lsof
    try:
        result = subprocess.run(
            ['lsof', '-ti', f':{port}'],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print(f"⚠ Порт {port} все еще занят после попыток освобождения")
            return False
    except:
        pass
    return True

def run_ngrok(port):
    """Запускает ngrok туннель"""
    try:
        # Проверяем, установлен ли ngrok
        subprocess.run(['ngrok', 'version'], capture_output=True, check=True)
        
        print(f"Запуск ngrok туннеля на порт {port}...")
        ngrok_process = subprocess.Popen(
            ['ngrok', 'http', str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(3)  # Даем ngrok время запуститься
        
        # Получаем публичный URL
        try:
            import requests
            max_retries = 5
            for i in range(max_retries):
                time.sleep(2)  # Даем ngrok время запуститься
                response = requests.get('http://localhost:4040/api/tunnels', timeout=3)
                if response.status_code == 200:
                    tunnels = response.json().get('tunnels', [])
                    if tunnels:
                        public_url = tunnels[0]['public_url']
                        # Сохраняем URL в файл
                        with open('ngrok_url.txt', 'w') as f:
                            f.write(public_url)
                        
                        print(f"\n{'='*60}")
                        print(f"✓ Публичный URL: {public_url}")
                        print(f"✓ URL сохранен в файл: ngrok_url.txt")
                        print(f"{'='*60}\n")
                        print(f"Пример curl запроса:")
                        print(f"curl -X POST {public_url}/predict \\")
                        print(f"  -H 'Content-Type: application/json' \\")
                        print(f"  -d '{{\"text\":\"I feel great today!\",\"use_per_label_thresholds\":false}}'")
                        print(f"\n{'='*60}\n")
                        return ngrok_process, public_url
        except Exception as e:
            print(f"⚠ Не удалось получить URL от ngrok API: {e}")
            print("Проверьте http://localhost:4040 вручную")
        
        return ngrok_process, None
    except FileNotFoundError:
        print("⚠ ngrok не найден. Установите: https://ngrok.com/download")
        return None, None
    except Exception as e:
        print(f"⚠ Ошибка запуска ngrok: {e}")
        return None, None

def run_server(port=8000):
    """Запускает FastAPI сервер"""
    print(f"Запуск FastAPI сервера на порту {port}...")
    server_process = subprocess.Popen(
        [sys.executable, '-m', 'uvicorn', 'app_psych:app', '--host', '0.0.0.0', '--port', str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return server_process

def main():
    port = 8000
    
    # Убиваем процесс на порту если занят
    print(f"Проверка и освобождение порта {port}...")
    if not kill_port(port):
        print(f"⚠ Не удалось освободить порт {port}. Используется другой порт.")
        # Можно попробовать другой порт или выйти
        # Для простоты продолжаем - uvicorn сам выберет свободный порт
    
    # Запускаем ngrok
    ngrok_process, public_url = run_ngrok(port)
    
    # Запускаем сервер
    print(f"\nЗапуск сервера на порту {port}...")
    server_process = run_server(port)
    
    # Ждем немного для запуска
    time.sleep(3)
    
    # Проверяем, что сервер запустился
    try:
        import requests
        health_check = requests.get(f'http://localhost:{port}/health', timeout=2)
        if health_check.status_code == 200:
            print(f"✓ Сервер успешно запущен на порту {port}")
        else:
            print(f"⚠ Сервер запущен, но health check не прошел")
    except:
        print(f"⚠ Не удалось проверить health сервера")
    
    print("\n" + "="*60)
    print("Сервер запущен. Нажмите Ctrl+C для остановки.")
    if public_url:
        print(f"\n📌 Публичный URL: {public_url}")
        print(f"📁 URL сохранен в: ngrok_url.txt")
    print("="*60 + "\n")
    
    try:
        # Ждем завершения
        server_process.wait()
    except KeyboardInterrupt:
        print("\n\nОстановка сервера...")
        server_process.terminate()
        if ngrok_process:
            ngrok_process.terminate()
        print("✓ Сервер остановлен")

if __name__ == "__main__":
    main()

