def same_brand(product1, product2):
    # Edits: removed 'ultra', 'panasonic national' -> 'panasonic, incs etc
    brand_list = [
        "Acer", "Admiral", "AGA AB", "Aiwa", "Akai", "Alba", "Amstrad", "Andrea Electronics", "Apex Digital", "Apple",
        "Arcam", "Arise India", "Audiovox", "AWA", "Baird", "Bang & Olufsen", "Beko", "BenQ", "Binatone", "Blaupunkt",
        "BPL", "Brionvega", "Bush", "Canadian General Electric", "CGE", "Changhong", "ChiMei", "Compal Electronics",
        "Conar Instruments", "Continental Edison", "Cossor", "Craig", "Curtis Mathes", "Daewoo", "Dell",
        "Delmonico International Corporation", "DuMont Laboratories", "Durabrand", "Dynatron", "EKCO", "Electrohome",
        "Element Electronics", "Emerson Radio & Phonograph", "EMI", "English Electric",
        "English Electric Valve Company","Farnsworth", "Ferguson Electronics", "Ferranti", "Finlux", "Fisher "                                                                                             "Electronics",
        "Fujitsu", "Funai", "Geloso", "General Electric", "General Electric Company", "GoldStar", "Goodmans Industries", "Google",
        "Gradiente", "Graetz", "Grundig", "Haier", "Hallicrafters", "Hannspree", "Heath Company", "Heathkit",
        "Hinari Domestic Appliances", "Hisense", "Hitachi", "HMV", "Hoffman Television", "Itel", "ITT Corporation", "Jensen Loudspeakers",
        "JVC", "Kenmore", "Kent Television", "Kloss Video", "Kogan", "Kolster-Brandes", "Konka", "Lanix", "Le.com",
        "LG", "Loewe", "Luxor", "Magnavox", "Marantz", "Marconiphone","Matsui", "Memorex", "Metz", "Micromax", "Mitsubishi", "Mivar", "Motorola", "Muntz", "Murphy Radio",
        "NEC", "Nokia", "Nordmende", "Onida", "Orion", "Packard Bell",
        "Panasonic", "Pensonic", "Philco", "Philips", "Pioneer", "Planar Systems", "Polaroid",
        "ProLine", "ProScan", "Pye", "Pyle USA", "Quasar", "RadioShack", "Rauland-Borg", "RCA", "Realistic",
        "Rediffusion","SABA", "Salora", "Salora International", "Samsung", "Sansui", "Sanyo", "Schneider Electric", "Seiki Digital",
        "Sèleco", "Setchell Carlson", "Sharp", "Siemens", "Skyworth", "Sony", "Soyo", "Stromberg-Carlson", "Supersonic",
        "Sylvania", "Symphonic", "Tandy", "Tatung Company", "TCL", "Technics", "TECO", "Teleavia", "Telefunken",
        "Teletronics", "Thomson", "Thorn Electrical Industries", "Thorn EMI", "Toshiba", "TP Vision", "TPV Technology",
        "United States Television Manufacturing.", "Vestel", "Videocon", "Videoton", "Vizio", "Vu Televisions",
        "Walton", "Westinghouse Electric Corporation", "Westinghouse Electronics", "White-Westinghouse", "Xiaomi",
        "Zanussi", "Zenith Radio", "Zonda"
    ]
    brand_set = {brand.lower() for brand in brand_list}
    # Extract potential brand-related information from titles and attributes
    title1 = product1.get("title", "").lower()
    title2 = product2.get("title", "").lower()

    attributes1 = " ".join(product1.get("attributes", {}).values()).lower()
    attributes2 = " ".join(product2.get("attributes", {}).values()).lower()

    # Combine title and attributes to create searchable text
    combined_text1 = f"{title1} {attributes1}"
    combined_text2 = f"{title2} {attributes2}"

    brand1 = None
    brand2 = None
    # Check for any matching brand keywords in both products
    for brand in brand_set:
        if brand in combined_text1:
            brand1 = brand
        if brand in combined_text2:
            brand2 = brand
    # Return true if
    return brand1 != brand2 if brand1 is not None and brand2 is not None else False
