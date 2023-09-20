# -*- coding: utf-8 -*-

import json


def main():
    with open("list.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    df = open("search_engine_order", "w")

    for locale in sorted(config["locales"].keys()):
        main_again(config, locale)


def main_again(config, locale):
    region = RegionState("XX", "XX")
    # locale = "en_US"
    localized_configuration = load_and_filter_configuration(region, locale, config)

    search_engine_identifiers = localized_configuration.visible_default_engines

    #print("search_engine_identifiers")
    #print(search_engine_identifiers)

    search_order = localized_configuration.search_order

    #print("search_order")
    #print(search_order)

    ordered_list = []
    unordered_rest = []

    for name in search_order:
        for search_engine in search_engine_identifiers:
            for key, my_list in my_dict.items():
                if search_engine in my_list and name == key:
                    ordered_list.append(key)

    for search_engine in search_engine_identifiers:
        for key, my_list in my_dict.items():
            if search_engine in my_list and key not in search_order:
                unordered_rest.append(key)

    default_engine = None
    if localized_configuration.search_default is not None:
        for key, my_list in my_dict.items():
            if key == localized_configuration.search_default:
                default_engine = key
                break

    print(locale + "\n" + str(ordered_list + unordered_rest) + "\n ")


def load(ids):
    if not ids:
        return []
    else:
        return load_search_engines_from_list(
            context,
            list(set(ids)),
            SearchEngine.Type.BUNDLED_ADDITIONAL,
        )


class SearchEngineListConfiguration:
    def __init__(self, visible_default_engines, search_order, search_default):
        self.visible_default_engines = visible_default_engines
        self.search_order = search_order
        self.search_default = search_default


def load_and_filter_configuration(region, locale, config):
    config_blocks = pick_configuration_blocks(locale, config)
    json_search_engine_identifiers = get_search_engine_identifiers_from_block(
        region, locale, config_blocks
    )

    search_order = get_search_order_from_block(region, config_blocks)
    search_default = get_search_default_from_block(region, config_blocks)

    return SearchEngineListConfiguration(
        apply_overrides_if_needed(region, config, json_search_engine_identifiers),
        search_order,
        search_default,
    )


def pick_configuration_blocks(locale, config):
    locales_config = config["locales"]

    language = ""
    language_tag = ""

    if len(locale) == 2:
        language = locale
        language_tag = locale
    else:
        language = locale[0:2]
        country = locale[-2:]
        language_tag = language + "-" + country

    # First try (Locale): locales/xx_XX/
    if language_tag in locales_config:
        localized_config = locales_config[language_tag]
    # Second try (Language): locales/xx/
    elif language in locales_config:
        localized_config = locales_config[language]
    # Give up, and fallback to defaults
    else:
        localized_config = None

    return [localized_config, config] if localized_config else [config]


def get_search_engine_identifiers_from_block(region, locale, config_blocks):
    # Now test if there's an override for the region (if it's set)
    json_search_engine_identifiers = get_array_from_block(
        region, "visibleDefaultEngines", config_blocks
    )
    if not json_search_engine_identifiers:
        raise Exception(
            "No visibleDefaultEngines using region {region} and locale {locale}"
        )
    return json_search_engine_identifiers


def get_search_default_from_block(region, config_blocks):
    def transform(block):
        return block.get("searchDefault")

    return get_value_from_block(region, config_blocks, transform)


def get_search_order_from_block(region, config_blocks):
    return get_array_from_block(region, "searchOrder", config_blocks)


def get_array_from_block(region, key, blocks):
    return get_value_from_block(region, blocks, lambda x: x.get(key))


def get_value_from_block(region, blocks, transform):
    regions = [region.home, "default"]

    for block in blocks:
        for region in regions:
            region_obj = block.get(region)
            # print "region_obj"
            # print region_obj
            if isinstance(region_obj, dict):
                result = transform(region_obj)
                # print result
                # print result
                if result is not None:
                    return result

    return None


def apply_overrides_if_needed(region, config, jsonSearchEngineIdentifiers):
    overrides = config.get("regionOverrides")
    searchEngineIdentifiers = []

    regionOverrides = overrides.get(region.home) if region.home in overrides else None

    for i in range(len(jsonSearchEngineIdentifiers)):
        identifier = jsonSearchEngineIdentifiers[i]
        if regionOverrides and identifier in regionOverrides:
            identifier = regionOverrides.get(identifier)
        searchEngineIdentifiers.append(identifier)

    return searchEngineIdentifiers


class RegionState:
    def __init__(self, home, current):
        self.home = home
        self.current = current

    @staticmethod
    def default():
        """
        The default region when the region of the user could not be detected.
        """
        return RegionState("XX", "XX")


my_dict = {
    "Google": ["google-b-m", "google-com-nocodes"],
    "Bing": ["bing"],
    "Azerdict": ["azerdict"],
    "Pazaruvaj": ["pazaruvaj"],
    "Rediff": ["rediff"],
    "Mapy.cz": ["mapy-cz"],
    "Seznam": ["seznam-cz"],
    "Ecosia": ["ecosia"],
    "Qwant": ["qwant"],
    "Skroutz": ["skroutz"],
    "Revoserĉo": ["reta-vortaro"],
    "MercadoLibre Argentina": ["mercadolibre-ar"],
    "MercadoLibre Chile": ["mercadolibre-cl"],
    "MercadoLibre Mexico": ["mercadolibre-mx"],
    "Elebila": ["elebila"],
    "Am Faclair Beag": ["faclair-beag"],
    "SZTAKI angol-magyar": ["sztaki-en-hu"],
    "Vatera.hu": ["vatera"],
    "leit.is": ["leit-is"],
    "Yahoo! JAPAN": ["yahoo-jp"],
    "다나와": ["danawa-kr"],
    "다음지도": ["daum-kr"],
    "Salidzini.lv": ["salidzinilv"],
    "Gule sider mobil": ["gulesider-mobile-NO"],
    "Wikiccionari (oc)": ["wiktionary-oc"],
    "Wiktionary (or)": ["wiktionary-or"],
    "LEO Eng-Tud": ["leo_ende_de"],
    "Pledari Grond": ["pledarigrond"],
    "Slovnik.sk": ["slovnik-sk"],
    "m.Ceneje.si": ["ceneje"],
    "Odpiralni Časi": ["odpiralni"],
    "Prisjakt": ["prisjakt-sv-SE"],
    "Cốc Cốc": ["coccoc"],
    "百度": ["baidu"],
    "Wikipedia": ["wikipedia"],
    "Biquipedia (an)": ["wikipedia-an"],
    "ويكيبيديا (ar)": ["wikipedia-ar"],
    "অসমীয়া ৱিকিপিডিয়া (as)": ["wikipedia-as"],
    "Wikipedia (ast)": ["wikipedia-ast"],
    "Vikipediya (az)": ["wikipedia-az"],
    "Вікіпедыя (be)": ["wikipedia-be"],
    "Уикипедия (bg)": ["wikipedia-bg"],
    "উইকিপিডিয়া (bn)": ["wikipedia-bn"],
    "Wikipedia (br)": ["wikipedia-br"],
    "Wikipedia (bs)": ["wikipedia-bs"],
    "Viquipèdia (ca)": ["wikipedia-ca"],
    "Wikipedia (es)": ["wikipedia-es"],
    "Wikipedie (cs)": ["wikipedia-cz"],
    "Wicipedia (cy)": ["wikipedia-cy"],
    "Wikipedia (da)": ["wikipedia-da"],
    "Wikipedia (de)": ["wikipedia-de"],
    "Wikipedija (dsb)": ["wikipedia-dsb"],
    "Βικιπαίδεια (el)": ["wikipedia-el"],
    "Vikipedio (eo)": ["wikipedia-eo"],
    "Wikipedia (es)": ["wikipedia-es"],
    "Vikipeedia (et)": ["wikipedia-et"],
    "Wikipedia (eu)": ["wikipedia-eu"],
    "ویکی‌پدیا (fa)": ["wikipedia-fa"],
    "Wikipédia (fr)": ["wikipedia-fr"],
    "Wikipedia (fi)": ["wikipedia-fi"],
    "Wikipedia (fy)": ["wikipedia-fy-NL"],
    "Vicipéid (ga)": ["wikipedia-ga-IE"],
    "Wikipedia (gd)": ["wikipedia-gd"],
    "Wikipedia (gl)": ["wikipedia-gl"],
    "Vikipetã (gn)": ["wikipedia-gn"],
    "વિકિપીડિયા (gu)": ["wikipedia-gu"],
    "ויקיפדיה": ["wikipedia-he"],
    "विकिपीडिया (hi)": ["wikipedia-hi"],
    "Wikipedija (hr)": ["wikipedia-hr"],
    "Wikipedija (hsb)": ["wikipedia-hsb"],
    "Wikipédia (hu)": ["wikipedia-hu"],
    "Վիքիպեդիա (hy)": ["wikipedia-hy-AM"],
    "Wikipedia (ia)": ["wikipedia-ia"],
    "Wikipedia (id)": ["wikipedia-id"],
    "Wikipedia (is)": ["wikipedia-is"],
    "Wikipedia (it)": ["wikipedia-it"],
    "Wikipedia (ja)": ["wikipedia-ja"],
    "ვიკიპედია (ka)": ["wikipedia-ka"],
    "Wikipedia (kab)": ["wikipedia-kab"],
    "Уикипедия (kk)": ["wikipedia-kk"],
    "វិគីភីឌា (km)": ["wikipedia-km"],
    "ವಿಕಿಪೀಡಿಯ (kn)": ["wikipedia-kn"],
    "Wikipedia (lij)": ["wikipedia-lij"],
    "ວິກິພີເດຍ (lo)": ["wikipedia-lo"],
    "Wikipedia (lt)": ["wikipedia-lt"],
    "Vikipedeja (ltg)": ["wikipedia-ltg"],
    "Vikipēdija (lv)": ["wikipedia-lv"],
    "വിക്കിപീഡിയ (ml)": ["wikipedia-ml"],
    "विकिपीडिया (mr)": ["wikipedia-mr"],
    "Wikipedia (ms)": ["wikipedia-ms"],
    "Wikipedia (my)": ["wikipedia-my"],
    "Wikipedia (no)": ["wikipedia-NO"],
    "विकिपीडिया (ne)": ["wikipedia-ne"],
    "Wikipedia (nl)": ["wikipedia-nl"],
    "Wikipedia (nn)": ["wikipedia-NN"],
    "Wikipèdia (oc)": ["wikipedia-oc"],
    "ଉଇକିପିଡ଼ିଆ (or)": ["wikipedia-or"],
    "Wikipedia (pa)": ["wikipedia-pa"],
    "Wikipedia (pl)": ["wikipedia-pl"],
    "Wikipedia (pt)": ["wikipedia-pt"],
    "Wikipedia (rm)": ["wikipedia-rm"],
    "Wikipedia (ro)": ["wikipedia-ro"],
    "Википедия (ru)": ["wikipedia-ru"],
    "Wikipédia (sk)": ["wikipedia-sk"],
    "Wikipedja (sl)": ["wikipedia-sl"],
    "Wikipedia (sq)": ["wikipedia-sq"],
    "Википедија (sr)": ["wikipedia-sr"],
    "Wikipedia (sv)": ["wikipedia-sv-SE"],
    "விக்கிப்பீடியா (ta)": ["wikipedia-ta"],
    "వికీపీడియా (te)": ["wikipedia-te"],
    "วิกิพีเดีย": ["wikipedia-th"],
    "Wikipedia (tr)": ["wikipedia-tr"],
    "Вікіпедія": ["wikipedia-uk"],
    "ویکیپیڈیا (ur)": ["wikipedia-ur"],
    "Vikipediya (uz)": ["wikipedia-uz"],
    "Wikipedia (vi)": ["wikipedia-vi"],
    "Wikipedia (wo)": ["wikipedia-wo"],
    "维基百科": ["wikipedia-zh-CN"],
    "Wikipedia (zh)": ["wikipedia-zh-TW"],
    "Amazon.com": ["amazondotcom"],
    "Amazon.in": ["amazon-in"],
    "Amazon.co.uk": ["amazon-co-uk"],
    "Amazon.de": ["amazon-de"],
    "Amazon.com.au": ["amazon-au"],
    "Amazon.ca": ["amazon-ca"],
    "Amazon.es": ["amazon-es"],
    "Amazon.fr": ["amazon-fr"],
    "Amazon.co.jp": ["amazon-jp"],
    "Amazon.it": ["amazon-it"],
    "Amzon.nl": ["amazon-nl"],
    "Amazon.se": ["amazon-se"],
    "Azerdict": ["azerdict"],
    "Duck Duck Go": ["ddg"],
    "eBay": [
        "ebay",
        "ebay-befr",
        "ebay-de",
        "ebay-at",
        "ebay-au",
        "ebay-ca",
        "ebay-ie",
        "ebay-co-uk",
        "ebay-es",
        "ebay-es",
        "ebay-fr",
        "ebay-it",
        "ebay-nl",
        "ebay-pl",
        "ebay-ch",
    ],
}

if __name__ == "__main__":
    main()
