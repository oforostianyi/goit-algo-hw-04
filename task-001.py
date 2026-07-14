import argparse
import os
import shutil
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли з вихідної директорії до нової, сортуючи їх за розширенням."
    )
    parser.add_argument("source_dir", help="Шлях до вихідної директорії")
    parser.add_argument(
        "dest_dir",
        nargs="?",
        default="dist",
        help="Шлях до директорії призначення (за замовчуванням: dist)"
    )
    return parser.parse_args()


def collect_files_recursive(directory_path):
    files = []
    try:
        for entry in os.listdir(directory_path):
            full_path = os.path.join(directory_path, entry)
            if os.path.isdir(full_path):
                files.extend(collect_files_recursive(full_path))
            elif os.path.isfile(full_path):
                files.append(full_path)
    except PermissionError as e:
        print(f"Помилка доступу до директорії '{directory_path}': {e}", file=sys.stderr)
    except Exception as e:
        print(f"Неочікувана помилка при обробці директорії '{directory_path}': {e}", file=sys.stderr)
    return files


def copy_files_to_destination(files, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)

    for src_file in files:
        try:
            ext = os.path.splitext(src_file)[1].lower()
            folder_name = ext.lstrip('.') if ext else "no_extension"

            dest_subdir = os.path.join(dest_dir, folder_name)
            os.makedirs(dest_subdir, exist_ok=True)

            dest_file_path = os.path.join(dest_subdir, os.path.basename(src_file))

            # Обробка конфлікту імен файлів у цільовій папці
            if os.path.exists(dest_file_path):
                base, file_ext = os.path.splitext(os.path.basename(src_file))
                counter = 1
                while True:
                    new_name = f"{base}_{counter}{file_ext}"
                    dest_file_path = os.path.join(dest_subdir, new_name)
                    if not os.path.exists(dest_file_path):
                        break
                    counter += 1

            shutil.copy2(src_file, dest_file_path)
        except PermissionError as e:
            print(f"Помилка доступу до файлу '{src_file}': {e}", file=sys.stderr)
        except Exception as e:
            print(f"Неочікувана помилка при копіюванні файлу '{src_file}': {e}", file=sys.stderr)


def main():
    args = parse_arguments()
    source_dir = args.source_dir
    dest_dir = args.dest_dir

    if not os.path.isdir(source_dir):
        print(f"Помилка: вихідна директорія '{source_dir}' не існує або недоступна.", file=sys.stderr)
        sys.exit(1)

    files_list = collect_files_recursive(source_dir)
    copy_files_to_destination(files_list, dest_dir)
    print(f"Успішно скопійовано {len(files_list)} файлів у '{dest_dir}'.")


if __name__ == "__main__":
    main()
