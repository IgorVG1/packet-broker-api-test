# fix_swagger.py
import json


def fix_swagger_file():
    with open('swagger.json', 'r', encoding='utf-8') as f:
        swagger = json.load(f)

    # Удаляем пустые массивы parameters из paths
    for path, methods in swagger.get('paths', {}).items():
        if 'parameters' in methods and isinstance(methods['parameters'], list) and len(methods['parameters']) == 0:
            del methods['parameters']

    # Сохраняем исправленный файл
    with open('swagger_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(swagger, f, ensure_ascii=False, indent=2)

    print("Swagger файл исправлен. Сохранен как swagger_fixed.json")

    # Выводим список исправленных путей
    print("\nИсправленные пути:")
    for path, methods in swagger.get('paths', {}).items():
        if 'parameters' not in methods:
            print(f"✓ {path}")


if __name__ == "__main__":
    fix_swagger_file()