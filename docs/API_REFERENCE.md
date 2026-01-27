# Справочник API PageIndex

## Основные модули

### `pageindex.core.llm`

Отвечает за взаимодействие с API LLM (OpenAI) и извлечение JSON.

#### `ChatGPT_API(model: str, prompt: str, api_key: Optional[str] = None, ...) -> str`
Вызывает API OpenAI Chat Completion и возвращает содержимое ответа в виде строки.
- **model**: Название модели (например, "gpt-4o").
- **prompt**: Пользовательский промпт.
- **Returns**: Содержимое ответа или "Error" в случае ошибки.

#### `ChatGPT_API_async(model: str, prompt: str, ...) -> str`
Асинхронный вызов API OpenAI Chat Completion.

#### `extract_json(content: str) -> Union[Dict, List]`
Надежно извлекает и парсит JSON из строки, обрабатывая распространенные проблемы форматирования LLM (например, markdown-блоки кода или лишние запятые).

#### `count_tokens(text: Optional[str], model: str = "gpt-4o") -> int`
Подсчитывает количество токенов в текстовой строке, используя библиотеку `tiktoken`.

---

### `pageindex.core.pdf`

Утилиты для извлечения текста и обработки PDF.

#### `extract_text_from_pdf(pdf_path: str) -> str`
Извлекает весь текст из PDF-файла, используя PyPDF2.

#### `get_page_tokens(pdf_path: Union[str, BytesIO], model: str, pdf_parser: str) -> List[Tuple[str, int]]`
Извлекает текст и количество токенов для каждой страницы.
- **pdf_parser**: "PyPDF2" или "PyMuPDF".
- **Returns**: Список кортежей `(текст_страницы, количество_токенов)`.

#### `get_text_of_pages(pdf_path: str, start_page: int, end_page: int, tag: bool = True) -> str`
Получает текст из указанного диапазона страниц (нумерация с 1). Опционально оборачивает каждую страницу в теги `<start_index_N>`.

---

### `pageindex.core.tree`

Манипуляции с древовидной структурой и рекурсивные операции.

#### `list_to_tree(data: List[Dict]) -> List[Dict]`
Преобразует плоский список узлов с ключами 'structure' в dot-нотации (например, '1.1', '1.2.1') во вложенный словарь-дерево.

#### `structure_to_list(structure: Structure) -> List[Node]`
Разворачивает дерево в плоский список всех узлов (включая узлы-контейнеры).

#### `get_leaf_nodes(structure: Structure) -> List[Node]`
Получает список всех листовых узлов (узлов без потомков).

#### `generate_summaries_for_structure(structure: Structure, model: Optional[str]) -> Structure`
Асинхронная функция для генерации резюме (summary) для всех узлов в структуре с использованием LLM.

---

### `pageindex.config`

Управление конфигурацией.

#### `PageIndexConfig`
Pydantic-модель, определяющая схему конфигурации со значениями по умолчанию и валидацией.
- **model**: Модель LLM (по умолчанию: "gpt-4o")
- **max_page_num_each_node**: Макс. страниц на узел (по умолчанию: 5)
- **if_add_node_id**: Добавлять ID к узлам (по умолчанию: True)

#### `ConfigLoader`
Загружает конфигурацию из `config.yaml` (переменная окружения или текущая директория) и валидирует её через `PageIndexConfig`.
