"""
content_plan.py
----------------
Definit l'identite de la marque A T O et les categories de contenu.
C'est LE fichier a modifier pour changer le style / le sujet des posts.
"""

# ---------------------------------------------------------------------------
# 1) IDENTITE DE LA MARQUE  (modifiez librement)
# ---------------------------------------------------------------------------
MARQUE = {
    "nom": "A T O",
    "activite": "Creation de sites web et de logiciels sur mesure",
    "audience": "TPE/PME, artisans, commercants et entrepreneurs qui veulent "
                "une presence en ligne professionnelle",
    "ton": "professionnel mais accessible, concret, en francais, sans jargon inutile",
    "langue": "francais",
    "appel_action": "Contactez A T O en message prive pour votre projet de site ou logiciel.",
    # Vos hashtags fixes (ajoutes a chaque post). Max ~15-20 conseille.
    "hashtags_fixes": [
        "#creationsite", "#sitinternet", "#webdesign", "#developpementweb",
        "#logicielsurmesure", "#agencedigitale", "#siteweb", "#entrepreneur",
        "#tpe", "#pme", "#presenceenligne", "#digital",
    ],
}

# ---------------------------------------------------------------------------
# 2) CATEGORIES DE CONTENU  (rotation automatique)
#    "poids" = frequence relative (plus le chiffre est grand, plus ca sort souvent)
# ---------------------------------------------------------------------------
CATEGORIES = [
    {
        "cle": "conseil",
        "poids": 35,
        "titre": "Conseil / valeur",
        "consigne": (
            "Donne UN conseil concret et actionnable sur le web, les sites internet, "
            "le SEO, l'UX, la performance ou les logiciels metier. Format : un probleme "
            "frequent + la solution. Doit apporter de la valeur meme a qui ne devient pas client."
        ),
        "style_image": (
            "illustration moderne et epuree sur le theme du web design / developpement, "
            "couleurs sobres et professionnelles, style flat design minimaliste"
        ),
    },
    {
        "cle": "realisation",
        "poids": 25,
        "titre": "Realisation / portfolio",
        "consigne": (
            "Met en valeur le savoir-faire d'A T O comme si on presentait un projet livre "
            "(site vitrine, e-commerce ou logiciel). Reste generique (n'invente pas de faux "
            "noms de clients reels), parle des benefices obtenus pour le client."
        ),
        "style_image": (
            "mockup elegant d'un site web sur ecran d'ordinateur portable et smartphone, "
            "ambiance studio, lumiere douce, rendu professionnel haut de gamme"
        ),
    },
    {
        "cle": "preuve",
        "poids": 15,
        "titre": "Preuve / resultats",
        "consigne": (
            "Explique de maniere credible comment un bon site / logiciel ameliore concretement "
            "le business d'un client (plus de rendez-vous, gain de temps, image pro). "
            "Reste honnete et generique, sans chiffres invente comme s'ils etaient reels."
        ),
        "style_image": (
            "graphique de croissance stylise, courbe ascendante, theme business et reussite, "
            "couleurs professionnelles, design moderne"
        ),
    },
    {
        "cle": "offre",
        "poids": 15,
        "titre": "Offre / appel a l'action",
        "consigne": (
            "Presente clairement les services d'A T O (creation de sites web et logiciels sur "
            "mesure) et invite a passer a l'action. Doit donner envie de contacter sans etre agressif."
        ),
        "style_image": (
            "visuel d'appel a l'action professionnel, theme creation de site web, "
            "design moderne et engageant, couleurs de marque sobres"
        ),
    },
    {
        "cle": "tendance",
        "poids": 10,
        "titre": "Tendance / engagement",
        "consigne": (
            "Partage une reflexion ou une tendance du numerique (IA, no-code, securite, "
            "nouvelles technos web) et termine par une question ouverte pour faire reagir en commentaire."
        ),
        "style_image": (
            "illustration conceptuelle sur la technologie et l'innovation, theme futuriste sobre, "
            "style editorial moderne"
        ),
    },
]


def categorie_du_jour(graine: int):
    """
    Choisit une categorie de facon ponderee mais deterministe selon une 'graine'
    (par ex. le numero du jour de l'annee). Ainsi la rotation est reguliere et
    on ne tombe pas 5 fois de suite sur la meme categorie.
    """
    # On construit une liste "deroulee" selon les poids, puis on prend modulo la graine.
    deroule = []
    for cat in CATEGORIES:
        deroule.extend([cat] * cat["poids"])
    return deroule[graine % len(deroule)]
