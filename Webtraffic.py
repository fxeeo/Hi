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
import shutil
from rich.console import Console
from rich.prompt import Prompt

# HTTP requests and HTML parsing
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Initialize rich console
console = Console()

# --- Dependency Management ---

def install_dependencies():
    """Checks for and installs required modules if they are missing."""
    required_modules = ["rich", "requests", "beautifulsoup4"]
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
    Simulates organic traffic to a given URL using requests and BeautifulSoup.
    """
    try:
        # -- Setup Session --
        session = requests.Session()

        # Rotate User-Agent
        user_agent = random.choice(USER_AGENTS)
        session.headers.update({'User-Agent': user_agent})

        # Add realistic headers
        session.headers.update({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive'
        })

        # Proxy setup (placeholder)
        proxy_location = random.choice(list(PROXIES.keys()))
        proxy = PROXIES[proxy_location]
        if "YOUR_" in proxy:
            console.print(f"[yellow]Warning: Using placeholder proxy for {proxy_location}. Please update PROXIES in the script.[/yellow]")
        else:
            session.proxies = {"http": proxy, "https": proxy}

        # -- Make Initial Request --
        console.print(f"[cyan]Visiting:[/cyan] {url}")
        response = session.get(url, timeout=15)
        response.raise_for_status()

        # Simulate reading the page
        time.sleep(random.uniform(5, 10))

        # -- Parse HTML and Find Internal Link --
        soup = BeautifulSoup(response.content, 'html.parser')

        internal_links = []
        parsed_url = urlparse(url)
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Join relative URLs with the base URL
            absolute_link = urljoin(url, href)
            # Check if the link is on the same domain
            if urlparse(absolute_link).netloc == parsed_url.netloc:
                internal_links.append(absolute_link)

        if internal_links:
            # "Click" a random internal link
            next_page = random.choice(internal_links)
            console.print(f"[cyan]Navigating to:[/cyan] {next_page}")

            time.sleep(random.uniform(2, 5)) # Delay before "clicking"

            next_response = session.get(next_page, timeout=15)
            next_response.raise_for_status()

            # Simulate reading the second page
            time.sleep(random.uniform(5, 10))
        else:
            console.print("[yellow]No internal links found to navigate to.[/yellow]")

        return True

    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]An error occurred during the web request: {e}[/bold red]")
        return False
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
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
    console.print("[bold magenta]Pydroid 3 Note:[/bold magenta] This script is lightweight and should work well on Pydroid 3.")
    console.print("-" * 60)

def get_user_input():
    """Gets the target URL from the user."""
    url = Prompt.ask("[bold cyan]Enter website URL[/bold cyan]")
    return url

def main():
    """Main function to run the script."""
    install_dependencies()
    display_banner()

    target_url = get_user_input()

    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    while True:
        console.print(f"\n[cyan]Adding organic traffic to[/cyan] [bold green]{target_url}[/bold green]...")

        success = simulate_traffic(target_url)

        if success:
            console.print("\n[bold green]Successfully added organic traffic![/bold green]")
        else:
            console.print("\n[bold red]Failed to add organic traffic.[/bold red]")

        # Wait for a random interval before the next run
        delay = random.randint(30, 90)
        with console.status(f"[bold yellow]Waiting for {delay} seconds before the next run...", spinner="dots") as status:
            for i in range(delay, 0, -1):
                status.update(f"[bold yellow]Waiting for {i} seconds before the next run...[/bold yellow]")
                time.sleep(1)

if __name__ == "__main__":
    main()
