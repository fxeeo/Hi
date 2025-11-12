# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------
# Disclaimers:
# 1. This tool is for educational and testing purposes only.
# 2. The user is responsible for complying with the terms of service of any website they choose to test.
# 3. The developer assumes no liability for any misuse of this tool.
# ----------------------------------------------------------------------------------------------------------------

import time
import random
import subprocess
import sys
import importlib
from rich.console import Console
from rich.prompt import Prompt

# Selenium and undetected-chromedriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize rich console
console = Console()

# --- Dependency Management ---

def install_dependencies():
    """Checks for and installs required modules if they are missing."""
    required_modules = ["rich", "selenium", "undetected_chromedriver", "setuptools"]
    for module in required_modules:
        try:
            importlib.import_module(module)
        except ImportError:
            console.print(f"[yellow]Module '{module}' not found. Installing...[/yellow]")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                console.print(f"[green]Module '{module}' installed successfully.[/green]")
            except subprocess.CalledProcessError:
                console.print(f"[red]Failed to install '{module}'. Please install it manually.[/red]")
                sys.exit(1)

# --- Configuration ---

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

PROXIES = {
    "Dubai": "http://YOUR_DUBAI_PROXY_HERE",
    "Canada": "http://YOUR_CANADA_PROXY_HERE",
    "Germany": "http://YOUR_GERMANY_PROXY_HERE"
}

# --- Functions ---

def simulate_traffic(url):
    """
    Simulates organic traffic to a given URL using Selenium and undetected_chromedriver.
    """
    # -- Setup Chrome options --
    options = uc.ChromeOptions()

    # Rotate User-Agent
    user_agent = random.choice(USER_AGENTS)
    options.add_argument(f'--user-agent={user_agent}')

    # Set a realistic viewport size
    options.add_argument('--window-size=1920,1080')

    # Add realistic headers to mimic a real browser
    options.add_argument('--accept-language=en-US,en;q=0.9')
    options.add_argument('--sec-fetch-site=none')
    options.add_argument('--sec-fetch-mode=navigate')
    options.add_argument('--sec-fetch-user=?1')
    options.add_argument('--sec-fetch-dest=document')

    # Proxy setup (placeholder)
    proxy_location = random.choice(list(PROXIES.keys()))
    proxy = PROXIES[proxy_location]
    if "YOUR_" in proxy:
        console.print(f"[yellow]Warning: Using placeholder proxy for {proxy_location}. Please update PROXIES in the script.[/yellow]")
    else:
        options.add_argument(f'--proxy-server={proxy}')

    try:
        # Initialize WebDriver
        # If Chrome is not in a standard location, you may need to specify the path:
        # driver = uc.Chrome(options=options, browser_executable_path='/path/to/your/chrome')
        with uc.Chrome(options=options) as driver:
            driver.get(url)

            # Wait for page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Simulate human-like behavior
            time.sleep(random.uniform(3, 7))  # Initial delay

            # Scroll down the page
            scroll_height = driver.execute_script("return document.body.scrollHeight")
            for i in range(0, scroll_height, random.randint(300, 600)):
                driver.execute_script(f"window.scrollTo(0, {i});")
                time.sleep(random.uniform(0.5, 1.5))

            time.sleep(random.uniform(2, 5)) # Final delay before closing

        return True

    except TypeError as e:
        if "binary location must be a string" in str(e).lower():
            console.print("[bold red]Error: Chrome browser not found.[/bold red]")
            console.print("[yellow]Please make sure Google Chrome is installed and in your system's PATH,[/yellow]")
            console.print("[yellow]or specify the path using 'browser_executable_path' in the script.[/yellow]")
            return False
        else:
            console.print(f"[bold red]An unexpected TypeError occurred: {e}[/bold red]")
            return False
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
        return False

def display_banner():
    """Displays the tool's banner and ethical use disclaimer."""
    console.print("[bold cyan]╔══════════════════════════════════════════════════╗[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]      [bold white]Organic Web Traffic Simulator[/bold white]      [bold cyan]║[/bold cyan]")
    console.print("[bold cyan]╚══════════════════════════════════════════════════╝[/bold cyan]")
    console.print("[italic yellow]A tool for safe and ethical traffic simulation.[/italic yellow]\n")
    console.print("[bold red]Disclaimer:[/bold red]", "This tool is for educational and testing purposes only.")
    console.print("The user is responsible for complying with the terms of service of any website they test.")
    console.print("The developer assumes no liability for any misuse of this tool.\n")
    console.print("[bold magenta]Pydroid 3 Note:[/bold magenta] Ensure you have a compatible Chrome/Chromium browser installed and accessible for Selenium to function correctly.")
    console.print("-" * 60)

def main():
    """Main function to run the script."""
    install_dependencies()
    display_banner()

    target_url = "https://promotect.xo.je/"

    while True:
        console.print(f"\n[cyan]Adding organic traffic to[/cyan] [bold green]{target_url}[/bold green]...")

        success = simulate_traffic(target_url)

        if success:
            console.print("\n[bold green]Successfully added organic traffic![/bold green]")
        else:
            console.print("\n[bold red]Failed to add organic traffic.[/bold red]")

        # Wait for a random interval before the next run
        delay = random.randint(30, 90)
        console.print(f"\n[yellow]Waiting for {delay} seconds before the next run...[/yellow]")
        time.sleep(delay)

if __name__ == "__main__":
    main()
