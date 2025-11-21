# PML v0.1 Specification — Pain Markup Language

PML (Pain Markup Language) — это минималистичный декларативный формат данных, разработанный для:
- описания UI-структур в Pain
- хранения конфигураций
- работы с древовидными данными
- использования внутри C++/Rust/Pain-рантайма

PML вдохновлён YAML, но избавлен от его сложностей. PML использует строгие правила, обеспечивая предсказуемость, простоту парсинга и высокую производительность.

## Основные концепции

PML описывает данные через комбинацию:
- **SCALAR** — простые значения (строки, числа, булевы, null)
- **MAP** — словари (ключ-значение)
- **LIST** — списки

Структура определяется уровнем вложенности, выраженным табуляцией.

## Правила синтаксиса PML

### 1. Отступы

Уровень вложенности определяется **только TAB**.

- 1 TAB = 1 уровень
- Пробелы в начале строки запрещены
- Смешивание табов и пробелов не допускается

Пример:

```pml
window:
	title: "Demo"
	width: 400
```

### 2. Комментарии

Комментарии начинаются с `#`, всё после символа — игнорируется.

```pml
width: 400  # ширина окна
# Это полный комментарий
title: "Hello"
```

### 3. Пары "ключ: значение"

Формат: `ключ: значение`

- Пробел после двоеточия обязателен
- Ключ — строка без пробелов
- Значение может быть на той же строке или на следующей (с отступом)

Примеры:

```pml
title: "Hello"
width: 400
mode: prod
```

### 4. Скаляры

Поддерживаемые типы:

| Тип | Пример |
|-----|--------|
| string | `"Hello"` или `hello` |
| int | `123` |
| float | `3.14` |
| bool | `true`, `false` |
| null | `null` |

**Правила строк:**

- Если строка содержит пробелы, `:`, `#` → обязательны кавычки
- В остальных случаях — опционально
- Поддерживаются escape-последовательности: `\n`, `\t`, `\r`, `\\`, `\"`, `\'`

Примеры:

```pml
caption: "Clicks: 0"
mode: release
path: "C:/Program Files/Pain"
message: "Line 1\nLine 2"
```

### 5. MAP (словари)

MAP создаётся ключом с двоеточием:

```pml
window:
	title: "Pain Demo"
	width: 400
	height: 300
```

Значение после `:` может быть пустым → значит MAP или LIST начинается на следующем уровне:

```pml
config:
	database:
		host: "localhost"
		port: 5432
```

### 6. LIST (списки)

Список определяется ключом + блоком `-`:

```pml
children:
	- type: label
	  text: "Hello"
	- type: button
	  text: "OK"
	  on_click: on_ok
```

Каждый `-` может содержать:
- SCALAR
- MAP (как в примере выше)

Список скаляров:

```pml
items:
	- "apple"
	- "banana"
	- "orange"
```

LIST всегда находится под MAP-ключом.

## AST (внутреннее представление PML)

Рекомендуемая структура:

```rust
enum PmlNodeKind {
    Scalar,
    Map,
    List,
}

struct PmlNode {
    kind: PmlNodeKind,
    scalar: Option<String>,                    // если SCALAR
    map: Option<HashMap<String, PmlNode>>,     // если MAP
    list: Option<Vec<PmlNode>>,                // если LIST
}
```

## Ограничения PML v0.1

Для упрощения парсинга:

- ❌ Нет многострочных строк
- ❌ Нет inline списков `[a, b]`
- ❌ Нет inline map `{a: 1}`
- ❌ Нет YAML-ссылок (`&alias`, `*alias`)
- ❌ Нет типов `!!str`, `!!int`
- ❌ Нет явных тэгов
- ❌ Нет имён пространств, как в XML

PML — минимальный, строгий, простой.

## Примеры использования

### Простой конфиг

```pml
app:
	name: "My App"
	version: "1.0.0"
	debug: false
```

### UI структура

```pml
window:
	id: main_window
	title: "Pain Demo"
	width: 400
	height: 300
	layout:
		type: vbox
		spacing: 8
		padding: 12
		children:
			- type: label
			  id: label_counter
			  text: "Clicks: 0"
			- type: button
			  id: button_click
			  text: "Click me"
			  on_click: on_btn_click
```

### Использование в Pain

```pain
fn main():
    let doc = pml_load_file("ui/main_window.pml")
    let window = doc.window
    let title = window.title
    print("Window: " + title)
```

Или через парсинг строки:

```pain
fn main():
    let pml_source = "title: \"Hello\"\nwidth: 400"
    let doc = pml_parse(pml_source)
    print("Parsed PML successfully!")
```

## API Reference

### `pml_load_file(path: str) -> dynamic`

Загружает и парсит PML файл, возвращает распарсенное значение.

**Параметры:**
- `path` — путь к PML файлу

**Возвращает:**
- `dynamic` — распарсенное PML дерево (обычно Object с полями)

**Пример:**

```pain
let config = pml_load_file("config.pml")
```

### `pml_parse(source: str) -> dynamic`

Парсит PML строку и возвращает распарсенное значение.

**Параметры:**
- `source` — PML исходный код

**Возвращает:**
- `dynamic` — распарсенное PML дерево

**Пример:**

```pain
let doc = pml_parse("title: \"Hello\"\nwidth: 400")
```

## Roadmap

### v0.2 (позже)
- inline строки `"строка"` без ограничений
- escape-последовательности (расширенная поддержка)
- nullable значения (`key:` → `null`)

### v0.3
- anchors? (под вопросом)
- мини-шаблоны
- include-директивы `!include`

## Парсер PML — базовый алгоритм

1. Разбить текст на строки
2. Игнорировать пустые и комментарии
3. Определить `indent_level` по табам
4. Поддерживать стек узлов для вложенности
5. Если строка содержит `-` → LIST
6. Если строка содержит `key:` → MAP
7. Если справа есть значение → SCALAR
8. Строить дерево `PmlNode`

Весь парсер ≈ 250–350 строк.

