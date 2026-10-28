# La relatividad especial

Charla de divulgación científica: **del universo a la vida cotidiana, con trenes, muones, GPS y PET**. Pensada para grados 10.°, 11.° y ciclo complementario (Escuela Normal de Baranoa).

La presentación incluye animaciones propias (reloj de luz, muones, órbitas GPS, escáner PET) y una página aparte con simuladores interactivos.

## Ver en línea

- Presentación: https://hayzar.github.io/relatividad-especial/
- Simuladores: https://hayzar.github.io/relatividad-especial/simuladores.html

## Controles de la presentación

| Tecla | Acción |
| --- | --- |
| `→`, `Espacio`, `Av Pág` | Diapositiva siguiente |
| `←`, `Re Pág` | Diapositiva anterior |
| `Inicio` / `Fin` | Primera / última diapositiva |
| `F` | Pantalla completa |
| `N` | Mostrar u ocultar las notas del orador |

En pantallas táctiles se avanza con un toque o deslizando. Cada diapositiva tiene enlace directo, por ejemplo `#13`.

## Contenido

1. Pregunta inicial, contexto histórico y los dos postulados
2. Reloj de luz, deducción con Pitágoras, dilatación del tiempo y contracción de la longitud
3. Muones: por qué llegan al suelo
4. GPS: cómo calcula la posición, relojes relativistas y error acumulado
5. PET: aniquilación electrón-positrón y detección de coincidencias
6. Otras aplicaciones, tres ideas para llevar, mini-reto y fuentes

## Simuladores

`simuladores.html` reúne cuatro simuladores con deslizadores: dilatación del tiempo, contracción de la longitud, muones y relojes del GPS. No necesita instalación.

## Estructura del repositorio

```
index.html          Presentación (generada con build.py)
simuladores.html    Simuladores interactivos
assets/             Imágenes (fondo y muones)
fuente/             Diapositivas originales (una por archivo) e índice deck.json
build.py            Genera index.html desde fuente/
```

## Modificar las diapositivas

Edita los archivos de `fuente/diapositivas/` y ejecuta:

```
python3 build.py
```

El script solo usa la biblioteca estándar de Python 3.

## Cifras de referencia

- c ≈ 3 × 10⁸ m/s (valor exacto: 299 792 458 m/s)
- γ = 1 / √(1 − v²/c²); a 0,8 c, γ = 5/3
- Muones a 0,999 c: γ ≈ 22; vida media propia 2,2 µs
- GPS: −7 µs/día (relatividad especial) y +45 µs/día (relatividad general) dan un adelanto neto de unos 38 µs/día, equivalente a unos 11 km de error diario si no se corrige
- PET: cada fotón de aniquilación lleva 511 keV, la energía en reposo del electrón
