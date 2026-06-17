import os
import sys
import subprocess
import json
import webbrowser
import threading
from .core.discovery import get_plugins
from .core import server

def handle_args(args):
    """Main CLI entry logic for the tkbpy framework"""
    if not args:
        print("\n🌟 tkbpy Framework")
        print("Usage: tkbpy [myproject | run | doctor | -add]")
        print("Example: tkbpy myproject MyShop mui")
        print("Example: tkbpy -add database ShopDB\n")
        return

    cmd = args[0]

    # 1. Component Adder (-add database)
    if cmd == "-add":
        if len(args) < 3:
            print("❌ Usage: tkbpy -add database <name>")
            return
        sub_cmd = args[1]
        name = args[2]
        if sub_cmd == "database":
            add_database(name)

    # 2. Project Creator (myproject)
    elif cmd == "myproject":
        project_name = args[1] if len(args) > 1 else "my_app"
        ui_framework = args[2] if len(args) > 2 else "default"
        create_project(project_name, ui_framework)

    # 3. Server Runner (run)
    elif cmd == "run":
        run_server()

    # 4. Diagnostics (doctor)
    elif cmd == "doctor":
        run_doctor()
    
    else:
        print(f"❌ Unknown command: {cmd}")

def create_project(name, ui):
    """Generates folders, static assets, venv, and UI-specific templates"""
    print(f"🚀 Initializing new tkbpy project: {name}...")
    
    ui_choice = ui.lower()
    templates_dir = os.path.join(name, "templates")
    static_dir = os.path.join(name, "static")

    # --- 1. Folder Scaffolding ---
    for folder in [name, static_dir, templates_dir]:
        os.makedirs(folder, exist_ok=True)

    # --- 2. Generate Auto-Linked Static Files ---
    with open(os.path.join(static_dir, "style.css"), "w") as f:
        f.write(f"/* Custom CSS for {name} */\nbody {{ margin: 0; }}")
    
    with open(os.path.join(static_dir, "main.js"), "w") as f:
        f.write(f"// Custom JavaScript for {name}\nconsole.log('{name} is ready!');")

    # --- 3. Setup Virtual Environment ---
    print("📦 Creating virtual environment (env)...")
    subprocess.run([sys.executable, "-m", "venv", os.path.join(name, "env")])

    # --- 4. UI Framework Assets & Logic ---
    css_assets = ""
    ui_display = "Default"

    if "bootstrap" in ui_choice:
        print("🎨 Bootstrap is added!")
        css_assets = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">'
        ui_display = "Bootstrap"
    elif "tailwind" in ui_choice:
        print("🎨 Tailwind CSS is added!")
        css_assets = '<script src="https://cdn.tailwindcss.com"></script>'
        ui_display = "Tailwind CSS"
    elif "chakra" in ui_choice:
        print("⚡ Chakra UI is added!")
        css_assets = '<script src="https://unpkg.com/@chakra-ui/react@2.8.2/dist/chakra-ui.min.js"></script>'
        ui_display = "Chakra UI"
    elif "material" in ui_choice or "mui" in ui_choice:
        print("💎 Material UI is added!")
        css_assets = '<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" />'
        ui_display = "Material UI"
    else:
        print("🎨 Default CSS theme is added!")

    # --- 5. Master Template with Auto-Links ---
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - tkbpy</title>
    {css_assets}
    <link rel="stylesheet" href="/static/style.css">
    <style>
        body {{ 
            background-color: #f0f9ff; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0; 
            font-family: 'Roboto', 'Inter', sans-serif; 
        }}
        .card {{ 
            background: white; 
            padding: 3.5rem; 
            border-radius: 24px; 
            box-shadow: 0 20px 25px rgba(0,0,0,0.1); 
            text-align: center; 
            border-top: 10px solid #0ea5e9; 
            max-width: 450px;
        }}
        h1 {{ color: #0369a1; margin: 15px 0 10px 0; font-size: 2.4rem; }}
        p {{ color: #64748b; font-size: 1.15rem; }}
        .badge {{ 
            background: #e0f2fe; 
            color: #0369a1; 
            padding: 5px 14px; 
            border-radius: 9999px; 
            font-size: 0.8rem; 
            font-weight: 800; 
            text-transform: uppercase;
        }}
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">{ui_display} Mode</span>
        <h1>Successfully!</h1>
        <p>Now build everything in <strong>{name}</strong>.</p>
    </div>
    <script src="/static/main.js"></script>
</body>
</html>"""

    # --- 6. Write Project Files ---
    with open(os.path.join(templates_dir, "index.html"), "w") as f:
        f.write(html_content)
    with open(f"{name}/app.py", "w") as f:
        f.write("from tkbpy.core.server import start\nif __name__ == '__main__': start()")
    with open(f"{name}/tkbpy.json", "w") as f:
        json.dump({"project": name, "ui": ui_choice, "status": "active"}, f, indent=4)

    print(f"\n✅ Success! Project structure for '{name}' is ready.")
    print(f"👉 Run: cd {name} && tkbpy run")

def add_database(db_name):
    """Adds universal database support and prints confirmation"""
    if not os.path.exists("tkbpy.json"):
        print("❌ Error: Run this command inside a tkbpy project folder.")
        return

    os.makedirs("database", exist_ok=True)
    db_script = f"""# tkbpy Universal DB Connector
import sqlite3
import os

def get_connection():
    db_path = os.path.join(os.path.dirname(__file__), '{db_name}.db')
    try:
        return sqlite3.connect(db_path)
    except Exception as e:
        print(f"❌ DB Error: {{e}}")
        return None
"""
    with open("database/db_config.py", "w") as f:
        f.write(db_script)
    
    with open("tkbpy.json", "r+") as f:
        data = json.load(f)
        data["database"] = db_name
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    
    print("Database is added")

def run_server():
    """Starts dev server and triggers browser auto-launch"""
    print("🚀 Starting tkbpy engine...")
    threading.Timer(1.2, lambda: webbrowser.open("http://localhost:8000")).start()
    server.start()

def run_doctor():
    """Environment health check"""
    print("\n🩺 tkbpy Doctor")
    print("-" * 35)
    is_venv = sys.prefix != sys.base_prefix
    print(f"Environment: {'✔️ Active' if is_venv else '❌ NOT ACTIVE'}")
    print(f"Static Folder: {'✔️ Detected' if os.path.exists('static') else '❌ Missing'}")
    print(f"Database:    {'✔️ Configured' if os.path.exists('database/db_config.py') else '❌ None'}")
    print("-" * 35 + "\n")

def handle_args_from_terminal():
    handle_args(sys.argv[1:])