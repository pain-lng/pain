# PML Examples

Примеры использования PML (Pain Markup Language) в различных сценариях.

## 1. Простой конфиг

**config.pml:**

```pml
app:
	name: "My Application"
	version: "1.0.0"
	debug: false
	port: 8080
```

**Использование в Pain:**

```pain
fn main():
    let config = pml_load_file("config.pml")
    let app_name = config.app.name
    let port = config.app.port
    print("Starting " + app_name + " on port " + to_string(port))
```

## 2. UI структура

**ui/main_window.pml:**

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

**Использование в Pain:**

```pain
fn main():
    let doc = pml_load_file("ui/main_window.pml")
    let window = doc.window
    let title = window.title
    let width = window.width
    let height = window.height
    print("Window: " + title + " (" + to_string(width) + "x" + to_string(height) + ")")
```

## 3. Список элементов

**items.pml:**

```pml
items:
	- "apple"
	- "banana"
	- "orange"
```

**Использование в Pain:**

```pain
fn main():
    let doc = pml_load_file("items.pml")
    let items = doc.items
    # items is a List
    print("Items loaded: " + to_string(len(items)))
```

## 4. Вложенные структуры

**database.pml:**

```pml
database:
	host: "localhost"
	port: 5432
	credentials:
		username: "admin"
		password: "secret"
	options:
		ssl: true
		timeout: 30
```

## 5. Парсинг строки

```pain
fn main():
    let pml_source = "title: \"Hello\"\nwidth: 400\nheight: 300"
    let doc = pml_parse(pml_source)
    print("Parsed PML successfully!")
```

## 6. Комментарии

```pml
# Application configuration
app:
	name: "My App"  # Application name
	version: "1.0.0"
	# Debug mode
	debug: false
```

