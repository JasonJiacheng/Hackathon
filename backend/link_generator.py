def generate_links(category, color):
    query = f"{color} {category}".replace(" ", "+")

    return {
        "asos": f"https://www.asos.com/search/?q={query}",
        "hm": f"https://www2.hm.com/en_gb/search-results.html?q={query.replace('+', '%20')}",
        "zara": f"https://www.zara.com/uk/en/search?searchTerm={query.replace('+', '%20')}"
    }
