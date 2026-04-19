# Documentation des classes et méthodes

Ce document décrit les classes et méthodes présentes dans le projet, avec signatures et brèves descriptions.

---

**Module : `playerClass.py`**

- **`Player`**
  - Attributs principaux : `master`, `unlocked_plants`, `selected_plant`, `suns`, `suns_earn_rate`, `suns_cooldown`, `default_suns`, `amount_living_plants`, `sum_livingplant_hp`, `killed_zombies`, `killed_bosses`.
  - `__post_init__()` -> None : initialise `suns` (IntVar), cooldowns et compteurs.
  - `select_plant(selectable_plant: PlantSelector) -> None` : sélectionne/désélectionne un `PlantSelector` si le cooldown de la plante l'autorise.
  - `add_suns(suns: int) -> None` : ajoute (ou enlève si négatif) des soleils au joueur (valeur min 0).
  - `update(current_tick: float, last_tick: float) -> None` : gère le revenu passif de soleils selon `suns_cooldown`.

---

**Module : `livingentities/livingplants/livingplantClass.py`**

- **`LivingPlant`**
  - Attributs : `master`, `plant`, `slot`, `is_invulnerable`, `name`, `health_scale`, `health`, `lane`, `x`.
  - `__post_init__()` -> None : initialise attributs dérivés et marque le slot comme pris.
  - `damage(damages: int) -> None` : applique des dégâts, respecte `is_invulnerable`, dépile si mort.
  - `kill() -> None` : supprime la plante (délègue à la lane).
  - `update(current_tick: float, last_tick: float) -> None` : méthode de ticking (vide ici, à surcharger).
  - `sous_texte(current_tick: float, last_tick: float) -> str` : texte affiché pour l'UI (nom par défaut).
  - `ui_update(current_tick: float, last_tick: float) -> dict` : retour UI (par défaut priorité 0).

- **`LivingSunflower`** (hérite `LivingPlant`)
  - `__init__(plant, slot, master)` : vérifie type `Sunflower`, initialise timers.
  - `update(current_tick, last_tick)` : génère des soleils toutes les `suns_cooldown` secondes et déclenche une animation de clignotement.
  - `sous_texte(...)` : affiche nom + cooldown restant et % de vie si endommagée.
  - `ui_update(...)` : change le fond du slot brièvement au moment de génération.

- **`LivingLandmine`**
  - `__init__(..., is_invulnerable=True)` : initialise rayon, dégâts d'explosion, countdown et flags.
  - `_explode(current_tick)` -> None : tue les zombies dans le rayon et enregistre le timestamp d'explosion.
  - `update(current_tick, last_tick)` : logique d'armement, countdown, explosion et suppression après effet visuel.
  - `sous_texte(...)` : nom + countdown si amorcée.
  - `ui_update(...)` : indique visuellement armement/explosion.

- **`LivingPeashooter`**
  - `__init__(plant, slot, master)` : vérifie type `Peashooter`, initialise cooldowns, dégâts.
  - `update(current_tick, last_tick)` : tire des pois sur les zombies en face selon `pea_launch_cooldown` et `amount_of_peas`.
  - `sous_texte(...)` : affiche nom et cooldown / % vie si endommagée.

- **`LivingWallnut`**
  - `__init__(...)` : initialise, conserve référence `wn_plant`.
  - `update(...)` : délègue à la super-classe.
  - `sous_texte(...)` : affiche nom et % vie.
  - `ui_update(...)` : change couleur selon ratio vie.

---

**Module : `livingentities/livinglawnmoyers/livinglawnmoyerClass.py`**

- **`LivingLawnmoyer`**
  - Attributs : `lawnmoyer`, `lane`, `destroys_everything`, `name`, `speed`, `x`, `key_time`, `bg`, `direction`.
  - `__post_init__()` -> None : initialise position et apparence.
  - `update(current_tick, last_tick)` -> None : déplace la tondeuse, tue les zombies rencontrés, gère le retour/fin.
  - `sous_texte()` -> str : texte d'affichage.
  - `ui_update(current_tick, last_tick)` -> dict : change la couleur d'affichage aléatoirement périodiquement.

---

**Module : `livingentities/livingzombies/livingzombieClass.py`**

- **`LivingZombie`**
  - Attributs : `zombie`, `x`, `lane`, `master`, `is_boss`, `name`, `health_scale`, `health`, `attack_damage`, `attack_range`, `attack_cooldown`, `speed`, `last_attacked`.
  - `__post_init__()` -> None : initialise valeurs dérivées.
  - `damage(damage: int)` -> None : retire des PV.
  - `kill()` -> None : met la vie à 0.
  - `update(current_tick, last_tick)` -> None : déplace le zombie, gère attaques contre plantes et condition de fin (atteindre la maison).
  - `sous_texte(current_tick, last_tick)` -> str : affiche nom + % vie et cooldown d'attaque si en attaque.
  - `ui_update(...)` -> dict : retourne configuration UI (vide par défaut).
  - `is_alive` (property) -> bool : propriété (implémentation actuelle retourne True si health == 0 — conserver note de bug si nécessaire).

- **`PlantEater`** (hérite `LivingZombie`)
  - Attributs : `consumes_plants`, `eating_cooldown`, `last_meal`.
  - `update(...)` -> None : peut consommer une plante entière selon `eating_cooldown`, sinon inflige des dégâts.

---

**Module : `events/eventClass.py`**

- **`Event`** (base)
  - Attributs : `game`, `name`, `priority`, `state` (int interne), `debug_stats`, `_ui_conf`.
  - `enable()` / `pause()` / `disable()` -> None : change l'état et appelle hooks `_on_enable/_on_pause/_on_disable`.
  - `_on_enable()/_on_pause()/_on_disable()` : hooks par défaut qui loggent.
  - `update(current_tick, last_tick)` -> None : si activé, appelle `_ui_update`.
  - `_ui_update(board, current_tick, last_tick)` -> None : construit `ui_conf` (par défaut vide).
  - `ui_conf` (property + setter) -> dict : accès au mapping UI selon l'état.

- **`DisplayText`** (`events/event_display_text.py`)
  - `LETTERS` : mapping glyphes (incomplet).
  - `__init__(game, event_name, text, text_slide_speed, direction, starting_x, state='disabled')` : initialise texte et paramètres.
  - `update(current_tick, last_tick)` -> None : fait défiler le texte (implémentation minimale).
  - `_ui_update(board, current_tick, last_tick)` -> None : construit la configuration UI des lettres (placeholder).

- **`Waves`** (`events/event_waves.py`)
  - Grande classe gérant la génération de vagues de zombies.
  - `__init__(...)` : paramètres de fréquence, timers, statistiques debug (`debug_stats`).
  - `update(current_tick, last_tick)` -> None : logique de contrôle de vague, spawn des zombies (utilise `LivingZombie` et `PlantEater`).
  - `make_zombie_stack() -> list[Zombie]` : construit une pile gloutonne de zombies pour la vague courante.
  - Plusieurs helpers `_update_<stat>` pour remplir `debug_stats`.
  - `_on_enable()` -> None : hook d'activation, log et gestion du `grace_period`.
  - `_sort_zombie_by_hp(val: Zombie) -> int` : fonction de tri par PV.

- **`InvokeZombie`** (`events/event_invoke_zombie.py`)
  - `__init__(game, event_name, zombie, interval, state='disabled')` : prend un `Zombie` ou liste de `Zombie` et un intervalle.
  - `_on_enable()` : choisit une voie aléatoire de spawn.
  - `update(current_tick, last_tick)` : spawn périodiquement un zombie sur une lane aléatoire et met à jour `_ui_update`.
  - `_ui_update(board, current_tick, last_tick)` : met en évidence le slot d'apparition prochain.

- **`Seizure`** (`events/event_seizure.py`)
  - Evènement test qui peint un slot aléatoire périodiquement via `_ui_update`.

- **`LaunchGame`** (`events/event_start_game.py`)
  - `_on_enable()` : active `event_waves` puis se désactive.

- **`TerminateGame`** (`events/event_end_game.py`)
  - `has_ended` flag.
  - `_on_enable()` : désactive `event_waves`, libère les tondeuses et arrête le jeu.

---

**Module : `entities/plantsClass.py`**

- **`Plant`** (dataclass)
  - Champs : `name`, `cooldown`, `cost`, `health`, `ignore_in_hp_sum`.

- Sous-classes spécifiques :
  - **`Peashooter`** : attributs `pea_launch_cooldown`, `pea_damage`, `frozen_projectile`, `amount_of_peas`.
  - **`Sunflower`** : `suns_cooldown`, `suns_income`.
  - **`Wallnut`** : coût, vie, cooldown; `ignore_in_hp_sum=True` par défaut.
  - **`Landmine`** : `radius`, `explosion_damage`, `countdown_time`.

- `PLANTS` : dictionnaire d'instances prêtes à l'emploi (Peashooter, Sunflower, Wallnut, Landmine, etc.).

---

**Module : `entities/lawnmoyersClass.py`**

- **`Lawnmoyer`**
  - Dataclass simple : `name`, `speed`.
  - `to_string() -> str` : renvoie le nom en majuscules.

---

**Module : `entities/zombiesClass.py`**

- **`Zombie`**
  - Champs : `name`, `attack_damage`, `health`, `is_boss`, `eats_plant`, `consumes_plants`, `eating_cooldown`.
  - Constantes : `SPEED`, `attack_range`, `attack_cooldown`.
  - `to_string() -> str` : renvoie le nom en majuscules.
- `ZOMBIES` : dictionnaire d'exemples préréglés (divers niveaux et boss).

---

**Module : `gameClass.py`**

- **`Game`** (hérite de `Tk`)
  - `__init__(board_height=5, board_width=8)` : initialise `Player`, `board`, `events` (création des évènements clés).
  - `draw()` -> None : construit l'UI (board, slots, plant selectors, debug), démarre la boucle `tick`.
  - `tick(last_tick: float)` -> None : boucle principale de mise à jour : selectors, slots, player, entités vivantes, events, et schedule next tick.

---

**Module : `ui/lane.py`**

- **`Lane`**
  - Attributs : `y`, `player`, `house_frame`, `slots`, `plantes`, `zombies`, `lawnmoyer`, `lawnmoyer_released`.
  - `__post_init__()` -> None : crée le `HouseSlot` et l'initialise.
  - `release_lawnmoyer(destroys_everything=False)` -> None : transforme le `HouseSlot` en `LivingLawnmoyer` et libère l'emplacement.
  - `dig_up_plant()` -> None : récupère la plante (demi-coût) et la dépile.
  - `append_slot(slot: Slot)` -> None : ajoute un `Slot` à la lane.
  - `enfiler_zombie(zombie: LivingZombie)` -> None : ajoute un zombie dans la file.
  - `empiler_plante(plante: LivingPlant)` -> None : empile une plante et met à jour les compteurs joueur.
  - `defiler_zombie()` -> None : retire le premier zombie (incrémente kills), supprime l'objet.
  - `depiler_plante()` -> None : retire la dernière plante empilée, met à jour compteurs et slot.
  - `get_zombie() -> LivingZombie | None` : renvoie le premier zombie vivant.
  - `get_plante() -> LivingPlant | None` : renvoie la dernière plante empilée.
  - `interact_with()` -> None : logique d'interaction (poser/déterrer plante) selon sélection du joueur et soleils.
  - Propriétés : `len_zombie`, `len_plantes`, `width`.

**Module : `ui/houseslot.py`**

- **`HouseSlot`** (hérite `Button`)
  - `update_slot(current_tick, last_tick)` -> None : met à jour l'affichage selon si `taken_by` est présent.

**Module : `ui/plantselector.py`**

- **`PlantSelector`** (hérite `Button`)
  - `update_selector(current_tick, last_tick)` -> None : met à jour l'état visuel du sélecteur (cooldown, sélection, couleur selon coût disponible).

**Module : `ui/slot.py`**

- **`Slot`** (hérite `Button`)
  - `update_text(current_tick, last_tick)` -> None : met à jour le texte et la configuration visuelle du slot en combinant états plantes, zombies, tondeuse et events.
  - `_ui_update(options: dict)` -> None : applique une configuration UI complexe (ranges +N / -N, background/foreground) aux boutons.
  - `pos` (property) -> tuple[int,int] : renvoie `(y, x)`.