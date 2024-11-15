### Documentation du Jeu "Monstres & Cie Game"

"Monstres & Cie Game" est un jeu de rythme développé avec Python et Pygame. Le joueur contrôle un personnage qui doit éviter des obstacles en sautant. Le jeu est interactif et propose plusieurs fonctionnalités, notamment un contrôle via Arduino, un leaderboard, et l'enregistrement des données de jeu. L'objectif principal est de maximiser son score en évitant les obstacles le plus longtemps possible.

Le jeu s’ouvre sur un menu principal où le joueur peut démarrer une nouvelle partie ou consulter le classement des meilleurs scores (leaderboard). Si un Arduino est connecté, il est automatiquement détecté et permet de contrôler la hauteur du personnage à l’aide d’un potentiomètre (ne fonctionne pas toujours). Sinon, le jeu utilise les touches du clavier, notamment la barre d’espace pour effectuer les sauts. Un indicateur dans le menu informe de la disponibilité de la connexion Arduino.

Pendant la partie, le personnage avance doit éviter des obstacles en mouvement. Chaque obstacle évité ajoute un point au score. La partie se termine quand le joueur touche un obstacle. Une pause peut être activée à tout moment pour interrompre temporairement le jeu. À la fin d'une partie, les données du joueur, son score, et la durée de la session sont enregistrés dans un fichier CSV dédié.

Le leaderboard présente les meilleurs scores des différents joueurs. Les fichiers CSV sont lus pour extraire les scores les plus élevés, qui sont triés et affichés. Ce tableau permet aux joueurs de comparer leurs performances avec celles des autres. Une interface simple permet de revenir facilement au menu principal depuis n’importe quelle page.

Le jeu est conçu pour être accessible, avec une gestion automatique de la connexion Arduino et des modes de contrôle adaptés. Les données collectées comprennent le pseudo, le sexe, l’âge, la main dominante, le score, et la durée de la partie.

Démo jeu : https://youtu.be/4xGVq6NUdqs