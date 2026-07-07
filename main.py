"""
main.py
--------
Lance tout en une fois sur PC (generation + publication).
Pratique pour tester ou pour le Planificateur de taches Windows.

Le mode CLOUD (GitHub Actions) n'utilise PAS ce fichier : il appelle
generate.py et publish.py separement (voir .github/workflows/daily-post.yml).

Lancement :  python main.py
"""

import generate
import publish

if __name__ == "__main__":
    print("===== ETAPE 1 : generation du contenu =====")
    generate.main()
    print("\n===== ETAPE 2 : publication =====")
    publish.main()
