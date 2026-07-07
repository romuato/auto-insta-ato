"""
publish.py
-----------
Publie le post genere (dans ./output) sur :
  1. Instagram (compte professionnel)      -> obligatoire
  2. La Page Facebook pro (ex. "A T O")    -> si FB_PAGE_ID est renseigne

via l'API officielle Meta (Graph API). Seule la Page pro est visible du public,
jamais le profil personnel de l'administrateur.

L'API exige que l'image soit accessible par une URL PUBLIQUE.
Deux modes d'hebergement sont geres automatiquement :

  1) Mode CLOUD (GitHub Actions) : URL "raw" du fichier image deja pousse
     dans le depot GitHub. Active si la variable IMAGE_URL est fournie.

  2) Mode LOCAL (PC Windows) : televersement sur Cloudinary (compte gratuit).
     Active si les variables CLOUDINARY_* sont fournies.

Variables d'environnement (voir .env.example) :
  IG_USER_ID            -> identifiant du compte Instagram professionnel
  IG_ACCESS_TOKEN       -> token d'acces Meta longue duree
  FB_PAGE_ID            -> identifiant de la Page Facebook pro (vide = pas de post FB)
  IMAGE_URL             -> (mode cloud) URL publique directe de l'image
  CLOUDINARY_CLOUD_NAME -> (mode local) nom du cloud Cloudinary
  CLOUDINARY_API_KEY    -> (mode local)
  CLOUDINARY_API_SECRET -> (mode local)
  DRY_RUN               -> "1" pour tester sans rien publier

Lancement :  python publish.py
"""

import os
import sys
import time
import pathlib

import requests
from dotenv import load_dotenv

# La console Windows utilise parfois un encodage qui ne connait pas les emojis.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

# Instagram : API "connexion Instagram" (token IGAA..., genere dans le tableau
# de bord Meta > cas d'utilisation Instagram). Passe par graph.instagram.com.
IG_GRAPH = "https://graph.instagram.com/v21.0"
# Page Facebook : API classique, token de Page. Passe par graph.facebook.com.
FB_GRAPH = "https://graph.facebook.com/v21.0"
OUTPUT_DIR = pathlib.Path(__file__).parent / "output"


def _lire_legende() -> str:
    return (OUTPUT_DIR / "caption.txt").read_text(encoding="utf-8").strip()


def _obtenir_url_image() -> str:
    """Renvoie une URL publique de l'image, selon le mode disponible."""
    # Mode CLOUD : URL deja fournie (fichier pousse sur GitHub)
    url = os.environ.get("IMAGE_URL", "").strip()
    if url:
        print(f"[publish] Mode CLOUD, image hebergee ici : {url}")
        return url

    # Mode LOCAL : televersement Cloudinary
    cloud = os.environ.get("CLOUDINARY_CLOUD_NAME", "").strip()
    key = os.environ.get("CLOUDINARY_API_KEY", "").strip()
    secret = os.environ.get("CLOUDINARY_API_SECRET", "").strip()
    if cloud and key and secret:
        return _upload_cloudinary(cloud, key, secret)

    raise RuntimeError(
        "Aucun hebergement d'image configure. Fournis soit IMAGE_URL (cloud), "
        "soit les variables CLOUDINARY_* (local)."
    )


def _upload_cloudinary(cloud: str, key: str, secret: str) -> str:
    import hashlib

    timestamp = str(int(time.time()))
    # Signature exigee par Cloudinary : sha1 des params tries + secret
    to_sign = f"timestamp={timestamp}{secret}"
    signature = hashlib.sha1(to_sign.encode()).hexdigest()

    with open(OUTPUT_DIR / "image.png", "rb") as f:
        resp = requests.post(
            f"https://api.cloudinary.com/v1_1/{cloud}/image/upload",
            data={"timestamp": timestamp, "api_key": key, "signature": signature},
            files={"file": f},
            timeout=120,
        )
    resp.raise_for_status()
    url = resp.json()["secure_url"]
    print(f"[publish] Mode LOCAL, image televersee sur Cloudinary : {url}")
    return url


# ---------------------------------------------------------------------------
# Instagram
# ---------------------------------------------------------------------------
def publier_instagram(ig_user_id: str, token: str, image_url: str, legende: str) -> str:
    # Etape 1 : creer le conteneur media
    print("[publish][IG] Creation du conteneur media...")
    r1 = requests.post(
        f"{IG_GRAPH}/{ig_user_id}/media",
        data={"image_url": image_url, "caption": legende, "access_token": token},
        timeout=120,
    )
    if not r1.ok:
        raise RuntimeError(f"Erreur creation media IG : {r1.status_code} {r1.text}")
    creation_id = r1.json()["id"]

    # Petit delai : Instagram doit telecharger l'image depuis l'URL
    time.sleep(8)

    # Etape 2 : publier le conteneur
    print("[publish][IG] Publication...")
    r2 = requests.post(
        f"{IG_GRAPH}/{ig_user_id}/media_publish",
        data={"creation_id": creation_id, "access_token": token},
        timeout=120,
    )
    if not r2.ok:
        raise RuntimeError(f"Erreur publication IG : {r2.status_code} {r2.text}")
    return r2.json()["id"]


# ---------------------------------------------------------------------------
# Page Facebook pro
# ---------------------------------------------------------------------------
def publier_facebook(page_id: str, page_token: str, image_url: str, legende: str) -> str:
    print("[publish][FB] Publication de la photo sur la Page...")
    r = requests.post(
        f"{FB_GRAPH}/{page_id}/photos",
        data={"url": image_url, "caption": legende, "access_token": page_token},
        timeout=120,
    )
    if not r.ok:
        raise RuntimeError(f"Erreur publication Facebook : {r.status_code} {r.text}")
    return r.json().get("post_id") or r.json().get("id", "?")


def main():
    ig_user_id = os.environ["IG_USER_ID"]
    token = os.environ["IG_ACCESS_TOKEN"]
    fb_page_id = os.environ.get("FB_PAGE_ID", "").strip()
    fb_page_token = os.environ.get("FB_PAGE_TOKEN", "").strip()

    legende = _lire_legende()

    # Mode test : ne poste pas reellement, affiche juste ce qui serait publie.
    if os.environ.get("DRY_RUN", "").lower() in ("1", "true", "oui"):
        print("\n===== DRY_RUN (aucune publication reelle) =====")
        print("Image :", OUTPUT_DIR / "image.png")
        print("Cibles :", "Instagram" + (" + Page Facebook" if (fb_page_id and fb_page_token) else " uniquement"))
        print("Legende :\n" + legende)
        return

    image_url = _obtenir_url_image()
    erreurs = []

    try:
        post_ig = publier_instagram(ig_user_id, token, image_url, legende)
        print(f"[publish] INSTAGRAM OK ! ID du post : {post_ig}")
    except Exception as e:
        erreurs.append(f"Instagram : {e}")

    if fb_page_id and fb_page_token:
        try:
            post_fb = publier_facebook(fb_page_id, fb_page_token, image_url, legende)
            print(f"[publish] FACEBOOK OK ! ID du post : {post_fb}")
        except Exception as e:
            erreurs.append(f"Facebook : {e}")

    if erreurs:
        raise RuntimeError(" | ".join(erreurs))


if __name__ == "__main__":
    main()
