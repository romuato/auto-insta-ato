"""
generate.py
------------
Genere le contenu d'UN post :
  - une legende (caption) via GPT-4o-mini  (tres bon marche)
  - une image via DALL-E 3                  (~0,04 $ l'image)

Resultat ecrit dans le dossier ./output :
  - output/image.png
  - output/caption.txt
  - output/meta.json   (infos pour l'etape de publication)

Lancement :  python generate.py
"""

import os
import json
import base64
import datetime
import pathlib

from dotenv import load_dotenv
from openai import OpenAI

import content_plan as cp

load_dotenv()

OUTPUT_DIR = pathlib.Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

_cle = os.environ.get("OPENAI_API_KEY", "").strip()
if not _cle:
    raise SystemExit(
        "\n[generate] Il me manque ma cle OpenAI (mon 'cerveau') !\n"
        "Ajoutez OPENAI_API_KEY=sk-... dans le fichier .env, puis relancez-moi.\n"
    )
client = OpenAI(api_key=_cle)


def _graine_du_jour() -> int:
    """Numero qui change chaque jour ET selon le creneau (matin/soir) pour 2 posts/jour."""
    today = datetime.date.today()
    base = today.timetuple().tm_yday  # 1..366
    # POST_SLOT permet de differencier le 2e post du jour (0 = unique/matin, 1 = soir)
    slot = int(os.environ.get("POST_SLOT", "0"))
    return base * 2 + slot


def generer_legende(categorie: dict) -> str:
    marque = cp.MARQUE
    hashtags = " ".join(marque["hashtags_fixes"])

    system = (
        "Tu es un community manager expert qui redige des publications Instagram "
        "performantes en francais pour des PME."
    )
    user = f"""
Marque : {marque['nom']} — {marque['activite']}.
Audience : {marque['audience']}.
Ton : {marque['ton']}.

Categorie du post : {categorie['titre']}.
Consigne : {categorie['consigne']}

Redige UNE publication Instagram complete et prete a publier :
- Une accroche forte des la premiere ligne (avec 1 emoji max au debut).
- Un corps clair et aere (utilise des sauts de ligne et 2-4 emojis pertinents).
- Termine par cet appel a l'action : "{marque['appel_action']}"
- N'ecris PAS les hashtags (je les ajoute moi-meme).
- Pas de guillemets autour du texte, pas de titre "Legende :", juste le texte du post.
- Longueur : 80 a 150 mots maximum.
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.9,
    )
    texte = resp.choices[0].message.content.strip()
    return f"{texte}\n\n.\n.\n.\n{hashtags}"


def generer_image(categorie: dict) -> bytes:
    prompt = (
        f"{categorie['style_image']}. "
        f"Theme : {cp.MARQUE['activite']}. "
        "Image carree pour Instagram, tres haute qualite, sans texte ni lettres, "
        "sans logo, composition propre et professionnelle."
    )
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        quality="medium",
        n=1,
    )
    return base64.b64decode(resp.data[0].b64_json)


def main():
    graine = _graine_du_jour()
    categorie = cp.categorie_du_jour(graine)
    print(f"[generate] Categorie choisie : {categorie['titre']} (graine={graine})")

    print("[generate] Generation de la legende...")
    legende = generer_legende(categorie)

    print("[generate] Generation de l'image (DALL-E 3)...")
    image_bytes = generer_image(categorie)

    (OUTPUT_DIR / "image.png").write_bytes(image_bytes)
    (OUTPUT_DIR / "caption.txt").write_text(legende, encoding="utf-8")
    (OUTPUT_DIR / "meta.json").write_text(
        json.dumps(
            {
                "categorie": categorie["cle"],
                "date": datetime.datetime.now().isoformat(timespec="seconds"),
                "image": "output/image.png",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print("[generate] OK -> dossier output/ (image.png, caption.txt, meta.json)")


if __name__ == "__main__":
    main()
