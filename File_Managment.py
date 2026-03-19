from pathlib import Path
import shutil

BASE_PATH = Path(__file__).resolve().parent


def resolve_path(path_text: str) -> Path:
    path = Path(path_text.strip()).expanduser()
    return path if path.is_absolute() else BASE_PATH / path


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(BASE_PATH))
    except ValueError:
        return str(path)


def normalize_target(source: Path, new_name: str) -> Path:
    target = Path(new_name.strip())
    target = target if target.is_absolute() else source.parent / target
    return target


def list_folders(root: Path | None = None) -> list[Path]:
    root = root or BASE_PATH
    return sorted([item for item in root.iterdir() if item.is_dir()], key=lambda item: item.name.lower())


def list_files(root: Path | None = None) -> list[Path]:
    root = root or BASE_PATH
    return sorted([item for item in root.rglob('*') if item.is_file()], key=lambda item: str(item).lower())


def get_dashboard_stats() -> dict[str, int]:
    return {'folders': len(list_folders()), 'files': len(list_files())}


def create_folder(path_text: str) -> Path:
    folder = resolve_path(path_text)
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def rename_folder(path_text: str, new_name: str) -> tuple[Path, Path]:
    source = resolve_path(path_text)
    if not source.is_dir():
        raise FileNotFoundError(f"Folder not found: {display_path(source)}")
    target = normalize_target(source, new_name)
    source.rename(target)
    return source, target


def remove_folder(path_text: str) -> Path:
    folder = resolve_path(path_text)
    if not folder.is_dir():
        raise FileNotFoundError(f"Folder not found: {display_path(folder)}")
    shutil.rmtree(folder)
    return folder


def create_file(path_text: str) -> Path:
    file_path = resolve_path(path_text)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch(exist_ok=False)
    return file_path


def rename_file(path_text: str, new_name: str) -> tuple[Path, Path]:
    source = resolve_path(path_text)
    if not source.is_file():
        raise FileNotFoundError(f"File not found: {display_path(source)}")
    target = normalize_target(source, new_name)
    source.rename(target)
    return source, target


def remove_file(path_text: str) -> Path:
    file_path = resolve_path(path_text)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {display_path(file_path)}")
    file_path.unlink()
    return file_path


def write_file_content(path_text: str, content: str) -> Path:
    file_path = resolve_path(path_text)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')
    return file_path


def read_file_content(path_text: str) -> str:
    file_path = resolve_path(path_text)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {display_path(file_path)}")
    return file_path.read_text(encoding='utf-8')


def append_file_content(path_text: str, content: str) -> Path:
    file_path = resolve_path(path_text)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {display_path(file_path)}")
    with open(file_path, 'a', encoding='utf-8') as handle:
        handle.write(content)
    return file_path


def print_items(title: str, items: list[Path]) -> None:
    print(f"\n{title}")
    print('-' * len(title))
    if not items:
        print('No items found.')
        return
    for index, item in enumerate(items, start=1):
        print(f"{index}. {display_path(item)}")


def run_cli() -> None:
    actions = {
        '1': lambda: create_folder(input('Folder path: ')),
        '2': lambda: print_items('Folders', list_folders()),
        '3': lambda: rename_folder(input('Folder path: '), input('New name/path: ')),
        '4': lambda: remove_folder(input('Folder path: ')),
        '5': lambda: create_file(input('File path: ')),
        '6': lambda: print_items('Files', list_files()),
        '7': lambda: rename_file(input('File path: '), input('New name/path: ')),
        '8': lambda: remove_file(input('File path: ')),
        '9': lambda: write_file_content(input('File path: '), input('Write content: ')),
        '10': lambda: print(read_file_content(input('File path: '))),
        '11': lambda: append_file_content(input('File path: '), input('Append content: ')),
    }
    menu = (
        '\nFILE MANAGEMENT SYSTEM\n'
        '1. Create Folder\n2. Show Folders\n3. Rename Folder\n4. Delete Folder\n'
        '5. Create File\n6. Show Files\n7. Rename File\n8. Remove File\n'
        '9. Write File\n10. Read File\n11. Append File\n12. Exit\n'
    )
    while True:
        print(menu)
        choice = input('Choose 1-12: ').strip()
        if choice == '12':
            print('Goodbye!')
            break
        try:
            result = actions[choice]()
            if isinstance(result, tuple):
                print('Success:', ' -> '.join(display_path(p) for p in result))
            elif isinstance(result, Path):
                print(f"Success: {display_path(result)}")
        except KeyError:
            print('Invalid option.')
        except Exception as err:
            print(f'Error: {err}')
        input('\nPress Enter to continue...')


if __name__ == '__main__':
    run_cli()