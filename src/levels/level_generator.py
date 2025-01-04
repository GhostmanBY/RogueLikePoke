from level import Level

def generar_nivel(stage, level, enemies_min, enemies_max):
    nivel = Level(stage, level)
    if enemies_max and enemies_min:
        enemigos = nivel.generar_enemigos(enemies_min, enemies_max)
    events = nivel.generar_eventos()
    return nivel, enemigos, events
