# Guía Completa: Cómo Mejorar una Librería de Python a Estándares Profesionales

> **Objetivo**: Aprender a transformar una librería de Python existente en un proyecto de calidad profesional, siguiendo las mejores prácticas de la industria.

---

## 📚 Tabla de Contenidos

1. [Preparación y Configuración Inicial](#1-preparación-y-configuración-inicial)
2. [Comunicación con el Mantenedor](#2-comunicación-con-el-mantenedor)
3. [Análisis del Código Existente](#3-análisis-del-código-existente)
4. [Planificación de Mejoras](#4-planificación-de-mejoras)
5. [Implementación de Mejoras](#5-implementación-de-mejoras)
6. [Testing y Calidad](#6-testing-y-calidad)
7. [Documentación](#7-documentación)
8. [CI/CD y Automatización](#8-cicd-y-automatización)
9. [Pull Request y Code Review](#9-pull-request-y-code-review)
10. [Buenas Prácticas de Colaboración](#10-buenas-prácticas-de-colaboración)

---

## 1. Preparación y Configuración Inicial

### 1.1 Fork del Repositorio

**¿Por qué?** Un fork te permite trabajar en tu propia copia sin afectar el repositorio original.

**Pasos:**

1. Ve al repositorio original en GitHub: `https://github.com/matgille/CQL`
2. Click en el botón "Fork" (esquina superior derecha)
3. Selecciona tu cuenta personal como destino del fork

**Resultado:** Ahora tienes `https://github.com/TU_USUARIO/CQL`

### 1.2 Clonar tu Fork Localmente

```bash
# Navega a la carpeta donde quieres trabajar
cd ~/proyectos/

# Clona tu fork (NO el repositorio original)
git clone https://github.com/TU_USUARIO/CQL.git
cd CQL

# Agrega el repositorio original como "upstream" (para mantener sincronizado)
git remote add upstream https://github.com/matgille/CQL.git

# Verifica tus remotes
git remote -v
# Deberías ver:
# origin    https://github.com/TU_USUARIO/CQL.git (tu fork)
# upstream  https://github.com/matgille/CQL.git (original)
```

**💡 Consejo:** Siempre trabaja en tu fork y sincroniza con upstream regularmente.

### 1.3 Configurar el Entorno de Desarrollo

```bash
# Crear entorno virtual (SIEMPRE usa entornos virtuales)
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Verificar que estás en el entorno virtual
which python  # Debería mostrar la ruta dentro de venv/

# Instalar el paquete en modo desarrollo
pip install -e .

# Instalar herramientas de desarrollo
pip install -e ".[dev]"  # Si existe esta configuración
# O manualmente:
pip install pytest pytest-cov black ruff mypy pre-commit
```

**❗ Importante:** NUNCA instales paquetes globalmente. Siempre usa un entorno virtual.

### 1.4 Crear una Rama de Trabajo

```bash
# NUNCA trabajes directamente en main/master
# Sincroniza primero con upstream
git fetch upstream
git checkout main
git merge upstream/main

# Crea una rama descriptiva
git checkout -b feature/professional-refactor

# O para una categoría específica:
# git checkout -b refactor/add-type-hints
# git checkout -b docs/improve-readme
# git checkout -b test/add-unit-tests
```

**Nomenclatura de ramas:**
- `feature/` - nuevas funcionalidades
- `refactor/` - reestructuración de código
- `fix/` - corrección de bugs
- `docs/` - mejoras en documentación
- `test/` - añadir o mejorar tests
- `chore/` - tareas de mantenimiento

---

## 2. Comunicación con el Mantenedor

### 2.1 Antes de Empezar - Abre un Issue

**¿Por qué?** Evita trabajo duplicado y asegura que tus contribuciones serán bienvenidas.

**Template de Issue:**

```markdown
**Título:** Proposal: Refactor library to professional Python standards

**Descripción:**

Hi @matgille,

I've been using the Corpus Query Language library and I think it's a great tool!
I'd like to propose a comprehensive refactoring to bring it up to modern Python
standards while maintaining full backward compatibility.

## Proposed Improvements

### Code Quality
- [ ] Add type hints (PEP 484) to all modules
- [ ] Add comprehensive docstrings (Google style)
- [ ] Replace print statements with logging
- [ ] Improve error handling and validation

### Testing
- [ ] Create test suite with pytest
- [ ] Add code coverage reporting
- [ ] Implement CI/CD with GitHub Actions

### Documentation
- [ ] Enhance README with examples and API docs
- [ ] Add CONTRIBUTING.md
- [ ] Create CHANGELOG.md

### DevOps
- [ ] Configure pre-commit hooks
- [ ] Set up Black, Ruff, and MyPy
- [ ] Add GitHub Actions for automated testing

## Benefits

1. **Better maintainability**: Type hints and docs make code easier to understand
2. **Fewer bugs**: Tests catch issues before they reach users
3. **Professional appearance**: Attracts more contributors and users
4. **Easier onboarding**: Clear docs help new contributors

## Backward Compatibility

All changes will be **100% backward compatible**. Existing code will continue
to work without any modifications.

## Timeline

I estimate this will take 2-3 weeks working part-time. I can work incrementally
and submit multiple PRs if you prefer.

Would you be interested in these improvements? I'm happy to discuss the scope
and approach before starting.

Best regards,
[Tu Nombre]
```

### 2.2 Permisos y Accesos Necesarios

**NO necesitas permisos especiales para:**
- Hacer fork
- Crear branches en tu fork
- Abrir pull requests

**SÍ necesitas permisos para:**
- Push directo a `main` (pero NO deberías hacer esto)
- Crear releases
- Modificar configuración del repositorio

**Cómo solicitarlos (si es necesario):**

```markdown
Hi @matgille,

For the refactoring work, I don't need any special permissions. I'll work on
my fork and submit pull requests.

However, if you'd like me to:
- Set up GitHub Actions (requires write access to .github/)
- Configure branch protection rules
- Set up automated releases

Then I would need collaborator access. But we can start without this and you
can apply my changes manually.

Let me know what works best for you!
```

### 2.3 Establecer Expectativas

**Preguntas importantes:**

```markdown
Before I start, I'd like to clarify a few things:

1. **Code Style**: Are you open to using Black for formatting? (opinionated but consistent)
2. **Breaking Changes**: Should I avoid them completely or are minor ones OK for v1.0?
3. **Testing Coverage**: What's your target coverage percentage? (I recommend 80%+)
4. **Review Timeline**: How often can you review PRs? (helps me plan my work)
5. **Incremental vs. Big Bang**: Would you prefer:
   - One large PR with all changes, or
   - Multiple smaller PRs (recommended)
```

---

## 3. Análisis del Código Existente

### 3.1 Entender la Estructura Actual

```bash
# Explora la estructura del proyecto
tree -L 3 -I '__pycache__|*.pyc|.git'

# O sin tree:
find . -type f -name "*.py" | head -20

# Cuenta líneas de código
find . -name "*.py" -exec wc -l {} + | sort -n

# Identifica archivos grandes (candidatos para refactor)
find . -name "*.py" -exec wc -l {} + | sort -rn | head -10
```

**Crea un mapa mental:**

```markdown
## Estructura Actual

CQL/
├── src/CQL.py                    # CLI entry point (25 líneas)
├── corpus_query_language/
│   ├── __init__.py              # Package init (5 líneas)
│   ├── core/
│   │   └── core.py              # Main engine (39 líneas)
│   ├── engine/
│   │   └── engine.py            # Query execution (165 líneas) ⚠️ COMPLEJO
│   ├── language/
│   │   ├── lexer.py             # Tokenization (102 líneas)
│   │   └── parser.py            # AST building (109 líneas)
│   └── utils/
│       └── utils.py             # Helper functions (89 líneas)
```

### 3.2 Checklist de Análisis

Crea un archivo `ANALYSIS.md` en tu directorio local:

```markdown
# Análisis del Código - CQL

## ✅ Lo que Está Bien

- [ ] Estructura modular clara
- [ ] Usa PLY (biblioteca estándar para parsing)
- [ ] Separación de responsabilidades (lexer, parser, engine)
- [ ] Funcionalidad core está implementada

## ⚠️ Áreas de Mejora

### Calidad del Código
- [ ] No hay type hints
- [ ] Docstrings incompletos o faltantes
- [ ] Uso de `print()` en lugar de `logging`
- [ ] Comentarios en francés
- [ ] Sin validación de entrada

### Testing
- [ ] No hay tests unitarios
- [ ] No hay tests de integración
- [ ] No hay medición de coverage

### Documentación
- [ ] README básico, sin ejemplos completos
- [ ] No hay CONTRIBUTING.md
- [ ] No hay CHANGELOG.md
- [ ] API no documentada

### Tooling
- [ ] No hay formatters configurados
- [ ] No hay linters
- [ ] No hay type checker
- [ ] No hay pre-commit hooks
- [ ] No hay CI/CD

### Estructura
- [ ] No usa src/ layout
- [ ] requirements.txt tiene dependencias innecesarias
- [ ] pyproject.toml incompleto

## 🎯 Prioridades

1. **ALTA**: Type hints, tests, documentación
2. **MEDIA**: Tooling, CI/CD, estructura
3. **BAJA**: Optimizaciones de rendimiento
```

### 3.3 Ejecuta Análisis Automático

```bash
# Instala herramientas de análisis
pip install radon vulture bandit safety

# Complejidad ciclomática (identifica código complejo)
radon cc . -a -nb

# Código no usado
vulture .

# Vulnerabilidades de seguridad
bandit -r .

# Dependencias con vulnerabilidades conocidas
safety check

# Guarda el reporte
radon cc . -a -nb > reports/complexity.txt
vulture . > reports/dead_code.txt
```

**Interpreta los resultados:**

```
radon cc output:
- A-B: Excelente, fácil de mantener
- C: Aceptable, pero considerar refactor
- D-F: Complejo, DEBE refactorizarse
```

---

## 4. Planificación de Mejoras

### 4.1 Crea un Plan de Trabajo

**Archivo:** `REFACTOR_PLAN.md`

```markdown
# Plan de Refactorización - CQL v0.1.0

## Objetivos

Transformar CQL en una librería de Python de calidad profesional manteniendo
100% backward compatibility.

## Fases del Trabajo

### Fase 1: Fundamentos (Semana 1)
**Objetivo:** Establecer base para calidad de código

- [ ] Configurar pyproject.toml completo
- [ ] Crear requirements-dev.txt
- [ ] Agregar .gitignore profesional
- [ ] Configurar Black, Ruff, MyPy
- [ ] Agregar pre-commit hooks

**PR:** "Setup: Configure development tools and standards"

### Fase 2: Code Quality (Semana 1-2)
**Objetivo:** Mejorar legibilidad y mantenibilidad

- [ ] Agregar type hints a utils.py
- [ ] Agregar type hints a lexer.py
- [ ] Agregar type hints a parser.py
- [ ] Agregar type hints a engine.py
- [ ] Agregar type hints a core.py
- [ ] Reemplazar prints con logging
- [ ] Traducir comentarios a inglés
- [ ] Mejorar docstrings (Google style)

**PR:** "Refactor: Add type hints and improve documentation"

### Fase 3: Testing (Semana 2)
**Objetivo:** Asegurar correctitud del código

- [ ] Crear estructura tests/
- [ ] Escribir tests para utils
- [ ] Escribir tests para core
- [ ] Escribir tests para engine
- [ ] Configurar pytest y coverage
- [ ] Alcanzar 80%+ coverage

**PR:** "Test: Add comprehensive test suite with pytest"

### Fase 4: Documentación (Semana 2-3)
**Objetivo:** Facilitar uso y contribución

- [ ] Reescribir README completo
- [ ] Crear CONTRIBUTING.md
- [ ] Crear CHANGELOG.md
- [ ] Agregar ejemplos de uso
- [ ] Documentar API completa

**PR:** "Docs: Enhance documentation and examples"

### Fase 5: DevOps (Semana 3)
**Objetivo:** Automatizar calidad y testing

- [ ] Configurar GitHub Actions
- [ ] Setup matrix testing (multiple Python versions)
- [ ] Agregar badges al README
- [ ] Configurar codecov

**PR:** "CI: Add GitHub Actions and automated testing"

### Fase 6: Pulido Final (Semana 3)
**Objetivo:** Detalles finales

- [ ] Review completo del código
- [ ] Optimizar imports
- [ ] Verificar todos los tests pasan
- [ ] Actualizar versión a 0.1.0
- [ ] Crear release notes

**PR:** "Release: v0.1.0 - Professional Python standards"

## Criterios de Éxito

- [ ] 100% type hints coverage
- [ ] 80%+ test coverage
- [ ] Todos los tests pasan
- [ ] MyPy sin errores
- [ ] Black/Ruff sin warnings
- [ ] CI/CD completamente funcional
- [ ] Documentación completa
- [ ] Backward compatibility verificada

## Métricas

| Métrica | Antes | Objetivo | Actual |
|---------|-------|----------|--------|
| Type hints | 0% | 100% | - |
| Test coverage | 0% | 80%+ | - |
| Docstrings | 30% | 100% | - |
| CI/CD | ❌ | ✅ | - |
```

### 4.2 Estima Tiempo y Esfuerzo

```markdown
## Estimación de Esfuerzo

| Tarea | Complejidad | Tiempo Estimado | Prioridad |
|-------|-------------|-----------------|-----------|
| Type hints | Media | 8-10 horas | Alta |
| Tests | Alta | 12-15 horas | Alta |
| Documentación | Baja | 6-8 horas | Alta |
| CI/CD setup | Media | 4-6 horas | Media |
| Tooling config | Baja | 2-3 horas | Alta |
| Code review iteraciones | - | 5-8 horas | - |

**Total:** 37-50 horas (~1-2 semanas a tiempo parcial)
```

### 4.3 Identifica Riesgos

```markdown
## Riesgos y Mitigación

| Riesgo | Impacto | Probabilidad | Mitigación |
|--------|---------|--------------|------------|
| Breaking changes accidentales | Alto | Media | Tests exhaustivos, revisión cuidadosa |
| Mantenedor no responde | Medio | Baja | Trabajo incremental, comunicación proactiva |
| Conflictos con otras PRs | Bajo | Media | Sincronizar frecuentemente con upstream |
| Time boxing excedido | Bajo | Media | Priorizar tareas, trabajo incremental |
```

---

## 5. Implementación de Mejoras

### 5.1 Configuración Inicial del Proyecto

#### 5.1.1 Crear `.gitignore`

```bash
# Descarga un .gitignore completo para Python
curl https://www.toptal.com/developers/gitignore/api/python,pycharm,vscode,macos,linux,windows > .gitignore

# O crea uno manualmente con lo esencial
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Virtual environments
venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.swp

# PLY generated
parser.out
parsetab.py

# OS
.DS_Store
EOF
```

#### 5.1.2 Configurar `pyproject.toml`

```bash
# Si no existe, créalo
touch pyproject.toml
```

```toml
[build-system]
requires = ["setuptools>=68.0", "setuptools-scm>=8.0"]
build-backend = "setuptools.build_meta"

[project]
name = "corpus-query-language"
version = "0.1.0"
description = "A powerful CQL engine for linguistic corpus queries"
readme = "README.md"
requires-python = ">=3.9"
license = { text = "CC-BY-NC-SA-4.0" }
authors = [
    { name = "Matthias Gille Levenson", email = "matthias.gille-levenson@ens-lyon.fr" }
]
keywords = ["corpus", "linguistics", "nlp", "cql"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "ply>=3.11",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.7.0",
    "ruff>=0.0.287",
    "mypy>=1.5.0",
    "pre-commit>=3.3.3",
]

[project.urls]
Homepage = "https://github.com/matgille/CQL"
Repository = "https://github.com/matgille/CQL"
Issues = "https://github.com/matgille/CQL/issues"

[tool.black]
line-length = 100
target-version = ["py39", "py310", "py311", "py312"]

[tool.ruff]
line-length = 100
select = ["E", "F", "W", "I", "N", "UP"]
ignore = ["E501"]  # Line too long (Black handles this)

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "ply.*"
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "--cov=corpus_query_language",
    "--cov-report=term-missing",
    "--cov-report=html",
]
```

**💡 Explicación de cada sección:**

- `[build-system]`: Cómo construir el paquete
- `[project]`: Metadatos del proyecto
- `[project.optional-dependencies]`: Dependencias de desarrollo
- `[tool.black]`: Configuración del formateador
- `[tool.ruff]`: Configuración del linter
- `[tool.mypy]`: Configuración del type checker
- `[tool.pytest.ini_options]`: Configuración de tests

#### 5.1.3 Crear `requirements-dev.txt`

```bash
cat > requirements-dev.txt << 'EOF'
# Install production dependencies
-r requirements.txt

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.1

# Code quality
black>=23.7.0
ruff>=0.0.287
mypy>=1.5.0
pre-commit>=3.3.3

# Documentation
sphinx>=7.1.0
sphinx-rtd-theme>=1.3.0
EOF
```

#### 5.1.4 Limpiar `requirements.txt`

```bash
# Debe contener SOLO las dependencias de producción
cat > requirements.txt << 'EOF'
# Production dependencies only
ply>=3.11
EOF
```

**❗ Principio importante:**
- `requirements.txt` = lo que necesitan los USUARIOS
- `requirements-dev.txt` = lo que necesitan los DESARROLLADORES

### 5.2 Agregar Type Hints

**Proceso incremental por archivo:**

#### 5.2.1 Ejemplo: `utils.py`

**ANTES:**
```python
import re
import json

def build_grammar(debug, query):
    """Build an AST from a query."""
    MyLexer = lexer.Lexer()
    MyLexer.tokenize(query, debug=debug)
    MyParser = parser.Parser(MyLexer, debug=debug)
    return MyParser.ast

def simple_match(query, text_token):
    """Check if a query matches a token."""
    annotation, equality, regexp = query
    compiled_regexp = re.compile(fr"^{regexp}$")
    if re.match(compiled_regexp, text_token[annotation]):
        if equality == "=":
            return True
        else:
            return False
    else:
        if equality == "!=":
            return True
        else:
            return False
```

**DESPUÉS:**
```python
import re
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Type aliases para claridad
QueryTuple = tuple[str, str, str]
AnnotatedToken = dict[str, str]


def build_grammar(debug: bool, query: str) -> list[Any]:
    """Build an Abstract Syntax Tree from a CQL query.

    Args:
        debug: If True, outputs detailed parsing information.
        query: The CQL query string to parse.

    Returns:
        The Abstract Syntax Tree as a list of query elements.

    Raises:
        ValueError: If the query is empty or invalid.

    Examples:
        >>> ast = build_grammar(False, "[lemma='test']")
        >>> isinstance(ast, list)
        True
    """
    if not query or not query.strip():
        msg = "Query string cannot be empty"
        raise ValueError(msg)

    logger.debug(f"Building grammar for query: {query}")

    lexer_instance = lexer.Lexer()
    lexer_instance.tokenize(query, debug=debug)

    parser_instance = parser.Parser(lexer_instance, debug=debug)

    if debug:
        logger.debug(f"Generated AST: {parser_instance.ast}")

    return parser_instance.ast


def simple_match(query: QueryTuple, text_token: AnnotatedToken) -> bool:
    """Check if a simple query matches a token.

    This function compares a query tuple (annotation, operator, pattern)
    against a text token using regex matching.

    Args:
        query: A tuple containing (annotation_name, operator, regex_pattern).
               The operator can be '=' (equals) or '!=' (not equals).
        text_token: A dictionary of annotations for a single token.

    Returns:
        True if the query matches the token, False otherwise.

    Raises:
        KeyError: If the annotation is not present in the token.
        ValueError: If the query tuple is malformed.

    Examples:
        >>> token = {"lemma": "test", "pos": "NOUN"}
        >>> simple_match(("lemma", "=", "test"), token)
        True
        >>> simple_match(("lemma", "!=", "other"), token)
        True
    """
    if len(query) != 3:
        msg = f"Query tuple must have 3 elements, got {len(query)}"
        raise ValueError(msg)

    annotation, equality, regexp = query

    if annotation not in text_token:
        msg = f"Annotation '{annotation}' not found in token: {text_token}"
        raise KeyError(msg)

    # Compile the regex pattern with anchors
    try:
        compiled_regexp = re.compile(rf"^{regexp}$")
    except re.error as e:
        msg = f"Invalid regex pattern '{regexp}': {e}"
        raise ValueError(msg) from e

    # Check if the pattern matches
    token_value = text_token[annotation]
    matches = bool(re.match(compiled_regexp, token_value))

    # Apply equality operator
    if equality == "=":
        return matches
    if equality == "!=":
        return not matches

    msg = f"Invalid equality operator: {equality}"
    raise ValueError(msg)
```

**✨ Mejoras aplicadas:**

1. **Type hints**: `debug: bool`, `query: str`, `-> list[Any]`
2. **Type aliases**: `QueryTuple`, `AnnotatedToken` para claridad
3. **Logging**: Reemplaza `print()` con `logger.debug()`
4. **Validación**: Verifica entrada antes de procesar
5. **Docstrings**: Formato Google con Args, Returns, Raises, Examples
6. **Error handling**: Excepciones específicas con mensajes claros
7. **Simplicidad**: Elimina `if/else` innecesarios (`return matches` directamente)

#### 5.2.2 Proceso de Agregar Type Hints

**Paso a paso:**

```bash
# 1. Ejecuta MyPy para ver qué falta
mypy src/corpus_query_language/utils/utils.py
# Verás errores como:
# error: Function is missing a return type annotation
# error: Argument 1 has incompatible type

# 2. Agrega type hints gradualmente
# Empieza con los tipos más simples
def import_corpus(path: str) -> list:  # Primer paso
def import_corpus(path: str) -> list[dict]:  # Segundo paso
def import_corpus(path: str) -> list[dict[str, str]]:  # Final

# 3. Usa `reveal_type()` para investigar tipos complejos
from typing import reveal_type
reveal_type(MyParser.ast)  # MyPy te dirá el tipo

# 4. Para tipos complejos, usa `Any` temporalmente
from typing import Any
def complex_function() -> Any:  # Mejorar después
    ...

# 5. Verifica cada archivo
mypy src/corpus_query_language/utils/utils.py
# No errors! ✅
```

**🎯 Prioridad de archivos:**

1. `utils.py` (más simple)
2. `lexer.py` (usa PLY, puede necesitar `Any`)
3. `parser.py` (similar a lexer)
4. `core.py` (usa los anteriores)
5. `engine.py` (el más complejo)

### 5.3 Agregar Logging

**Proceso de migración print → logging:**

```bash
# 1. Busca todos los prints
grep -rn "print(" src/

# 2. Por cada archivo, agrega el logger al inicio
```

**Template:**

```python
"""Module docstring."""

import logging

logger = logging.getLogger(__name__)  # __name__ = nombre del módulo


# Reemplazos:
# print("Debug info")           → logger.debug("Debug info")
# print("Processing...")        → logger.info("Processing...")
# print("Warning!")             → logger.warning("Warning!")
# print("ERROR!")               → logger.error("ERROR!")
# print(f"Value: {x}")          → logger.debug(f"Value: {x}")
```

**Ejemplos de conversión:**

```python
# ANTES
if debug:
    print(f"Token: {tok}")
    print(f"AST length: {ast_length}")

# DESPUÉS
if debug:
    logger.debug(f"Token: {tok}")
    logger.debug(f"AST length: {ast_length}")
```

```python
# ANTES
def t_error(self, t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# DESPUÉS
def t_error(self, t: Any) -> None:
    """Handle lexing errors."""
    logger.error(f"Illegal character '{t.value[0]}' at position {t.lexpos}")
    t.lexer.skip(1)
```

### 5.4 Mejorar Docstrings

**Formato Google Style:**

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """One-line summary (imperative mood, ends with period).

    Optional longer description. Explain the purpose, behavior,
    and any important implementation details.

    Args:
        param1: Description of param1. Include type info if not
                obvious from type hints.
        param2: Description of param2. Can be multi-line if needed.

    Returns:
        Description of return value. Be specific about structure
        if returning complex types.

    Raises:
        ValueError: When and why this exception is raised.
        KeyError: When and why this exception is raised.

    Examples:
        >>> function_name(arg1, arg2)
        expected_output

        >>> # More complex example
        >>> result = function_name(complex_arg)
        >>> assert result == expected

    Note:
        Optional notes about edge cases, performance, etc.
    """
    ...
```

**Checklist para cada docstring:**

- [ ] One-line summary en modo imperativo ("Calculate", no "Calculates")
- [ ] Descripción más larga si es necesario
- [ ] Todos los parámetros documentados
- [ ] Valor de retorno documentado
- [ ] Todas las excepciones documentadas
- [ ] Al menos un ejemplo funcional
- [ ] Notas sobre edge cases si aplican

**Herramienta útil:**

```bash
# Genera esqueletos de docstrings automáticamente
pip install pyment

# Procesa un archivo
pyment -w -o google myfile.py
```

### 5.5 Traducir Comentarios

```bash
# Encuentra comentarios en francés
grep -rn "# .*[àâäéèêëïîôùûü]" src/

# Traduce uno por uno con contexto
```

**Ejemplos:**

```python
# ANTES
# On teste si on est en bout de texte.
if len(corpus) == text_index and tree_index != ast_length:
    # Si on matche la longueur de notre arbre
    ...

# DESPUÉS
# Check if we've reached the end of the text
if len(corpus) == text_index and tree_index != ast_length:
    # If we've matched the entire AST length
    ...
```

### 5.6 Crear Archivo `__main__.py`

**Para hacer el paquete ejecutable:**

```python
"""Command-line interface for Corpus Query Language."""

import argparse
import json
import logging
import sys
from pathlib import Path

from corpus_query_language.core.core import CQLEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_corpus(corpus_path: Path) -> list[dict[str, str]]:
    """Load a corpus from a JSON file."""
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus file not found: {corpus_path}")

    with corpus_path.open(encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Corpus Query Language - Query annotated text corpora"
    )
    parser.add_argument("query", type=str, help="CQL query to execute")
    parser.add_argument("corpus", type=Path, help="Path to JSON corpus file")
    parser.add_argument(
        "-m", "--mode",
        choices=["match", "findall"],
        default="findall",
        help="Query mode"
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true")

    args = parser.parse_args()

    try:
        corpus = load_corpus(args.corpus)
        engine = CQLEngine()

        if args.mode == "match":
            result = engine.match(corpus, args.query, verbose=args.verbose)
            sys.exit(0 if result else 1)
        else:
            results = engine.findall(corpus, args.query, verbose=args.verbose)
            sys.exit(0)

    except Exception as e:
        logger.exception(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Uso:**

```bash
# Después de instalar
python -m corpus_query_language "[lemma='rey']" corpus.json

# O con el entry point configurado en pyproject.toml
cql "[lemma='rey']" corpus.json
```

---

## 6. Testing y Calidad

### 6.1 Estructura de Tests

```bash
# Crea la estructura
mkdir -p tests
touch tests/__init__.py
touch tests/conftest.py
```

**Estructura recomendada:**

```
tests/
├── __init__.py
├── conftest.py              # Fixtures compartidas
├── test_core.py            # Tests para core/
├── test_engine.py          # Tests para engine/
├── test_lexer.py           # Tests para language/lexer.py
├── test_parser.py          # Tests para language/parser.py
├── test_utils.py           # Tests para utils/
└── integration/            # Tests de integración
    ├── __init__.py
    └── test_end_to_end.py
```

### 6.2 Crear Fixtures

**`tests/conftest.py`:**

```python
"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def sample_corpus():
    """Provide a sample annotated corpus for testing."""
    return [
        {
            "word": "Da",
            "lemma": "dar",
            "pos": "VERB",
            "morph": "Mood=Imp"
        },
        {
            "word": "paz",
            "lemma": "paz",
            "pos": "NOUN",
            "morph": "Gender=Masc"
        },
        {
            "word": "rey",
            "lemma": "rey",
            "pos": "NOUN",
            "morph": "Gender=Masc"
        },
    ]


@pytest.fixture
def empty_corpus():
    """Provide an empty corpus."""
    return []


@pytest.fixture
def single_token_corpus():
    """Provide a single-token corpus."""
    return [
        {"word": "test", "lemma": "test", "pos": "NOUN", "morph": ""}
    ]


@pytest.fixture
def cql_engine():
    """Provide a CQLEngine instance."""
    from corpus_query_language.core.core import CQLEngine
    return CQLEngine()
```

### 6.3 Escribir Tests

**Principios:**

1. **AAA Pattern**: Arrange, Act, Assert
2. **Un test, un concepto**
3. **Nombres descriptivos**
4. **Tests independientes**

**`tests/test_core.py`:**

```python
"""Tests for the core CQLEngine class."""

import pytest
from corpus_query_language.core.core import CQLEngine


class TestCQLEngine:
    """Test suite for CQLEngine class."""

    def test_engine_initialization(self):
        """Test that CQLEngine can be initialized."""
        # Arrange & Act
        engine = CQLEngine()

        # Assert
        assert engine is not None

    def test_findall_basic_lemma_query(self, cql_engine, sample_corpus):
        """Test findall with a basic lemma query."""
        # Arrange
        query = "[lemma='rey']"

        # Act
        results = cql_engine.findall(sample_corpus, query, verbose=False)

        # Assert
        assert len(results) == 1
        assert results[0] == (2, 3)  # Index del token 'rey'

    def test_findall_no_match(self, cql_engine, sample_corpus):
        """Test findall when there are no matches."""
        # Arrange
        query = "[lemma='notfound']"

        # Act
        results = cql_engine.findall(sample_corpus, query, verbose=False)

        # Assert
        assert len(results) == 0
        assert results == []

    def test_findall_empty_corpus(self, cql_engine, empty_corpus):
        """Test findall with an empty corpus."""
        # Arrange
        query = "[lemma='test']"

        # Act
        results = cql_engine.findall(empty_corpus, query, verbose=False)

        # Assert
        assert results == []

    def test_findall_invalid_empty_query(self, cql_engine, sample_corpus):
        """Test findall with an invalid/empty query."""
        # Arrange
        query = ""

        # Act & Assert
        with pytest.raises(ValueError, match="Query cannot be empty"):
            cql_engine.findall(sample_corpus, query, verbose=False)

    def test_match_found(self, cql_engine, sample_corpus):
        """Test match when pattern is found."""
        # Arrange
        query = "[lemma='rey']"

        # Act
        result = cql_engine.match(sample_corpus, query, verbose=False)

        # Assert
        assert result is True

    def test_match_not_found(self, cql_engine, sample_corpus):
        """Test match when pattern is not found."""
        # Arrange
        query = "[lemma='notfound']"

        # Act
        result = cql_engine.match(sample_corpus, query, verbose=False)

        # Assert
        assert result is False

    @pytest.mark.parametrize("query,expected_count", [
        ("[pos='NOUN']", 2),
        ("[pos='VERB']", 1),
        ("[lemma='rey' & pos='NOUN']", 1),
        ("[morph='Gender=Masc']", 2),
    ])
    def test_findall_various_queries(
        self, cql_engine, sample_corpus, query, expected_count
    ):
        """Test findall with various query types."""
        # Act
        results = cql_engine.findall(sample_corpus, query, verbose=False)

        # Assert
        assert len(results) == expected_count
```

**Técnicas avanzadas:**

```python
# Parametrización para múltiples casos
@pytest.mark.parametrize("input,expected", [
    ("case1", result1),
    ("case2", result2),
])
def test_multiple_cases(input, expected):
    assert function(input) == expected

# Test de excepciones
def test_raises_error():
    with pytest.raises(ValueError, match="specific message"):
        function_that_raises()

# Mocking
from unittest.mock import Mock, patch

def test_with_mock():
    with patch('module.function') as mock_func:
        mock_func.return_value = "mocked"
        assert function_using_it() == "expected"

# Fixtures con setup/teardown
@pytest.fixture
def resource():
    # Setup
    r = create_resource()
    yield r
    # Teardown
    r.cleanup()
```

### 6.4 Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Con verbose
pytest -v

# Con coverage
pytest --cov=corpus_query_language --cov-report=html

# Solo un archivo
pytest tests/test_core.py

# Solo un test
pytest tests/test_core.py::TestCQLEngine::test_findall_basic_lemma_query

# Con markers
pytest -m "not slow"

# Parar en el primer fallo
pytest -x

# Ver print statements
pytest -s

# Modo debug interactivo
pytest --pdb
```

### 6.5 Medir Coverage

```bash
# Generar reporte
pytest --cov=corpus_query_language --cov-report=html --cov-report=term

# Abrir reporte HTML
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows

# Ver qué líneas no están cubiertas
coverage report -m
```

**Meta de coverage:**
- ✅ 80-90%: Excelente
- ⚠️ 60-80%: Aceptable
- ❌ <60%: Mejorar

**No necesitas 100%:**
- Logging statements
- Error handling de casos extremos
- Código deprecated

### 6.6 Pre-commit Hooks

```bash
# Instalar
pip install pre-commit

# Crear configuración
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.11
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
EOF

# Instalar los hooks
pre-commit install

# Ejecutar manualmente en todos los archivos
pre-commit run --all-files
```

**Ahora, cada commit ejecutará automáticamente:**
1. Black (formateo)
2. Ruff (linting)
3. MyPy (type checking)
4. Validaciones básicas

---

## 7. Documentación

### 7.1 README Profesional

**Estructura recomendada:**

```markdown
# Nombre del Proyecto

[Badges]

Descripción corta y atractiva (1-2 líneas)

## Overview

Explicación más detallada del propósito y características.

### Key Features

- Feature 1
- Feature 2
- Feature 3

## Installation

### From PyPI
\```bash
pip install package-name
\```

### From Source
\```bash
git clone ...
\```

## Quick Start

Ejemplo mínimo que funcione:

\```python
import package

# Código funcional
\```

## Usage

### Basic Usage
### Advanced Usage
### API Reference

## Documentation

Links a docs completas si existen.

## Development

Cómo configurar entorno de desarrollo.

## Contributing

Link a CONTRIBUTING.md

## License

Información de licencia

## Citation

Cómo citar el proyecto

## Changelog

Link a CHANGELOG.md
```

**Badges útiles:**

```markdown
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://github.com/USER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/USER/REPO/actions)
[![Coverage](https://codecov.io/gh/USER/REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/USER/REPO)
```

### 7.2 CONTRIBUTING.md

**Template completo:**

```markdown
# Contributing to [Project Name]

Thank you for your interest in contributing!

## Code of Conduct

[Link or inline]

## How to Contribute

### Reporting Bugs

- Use GitHub Issues
- Search existing issues first
- Provide reproduction steps
- Include error messages

### Suggesting Enhancements

- Open an issue with tag "enhancement"
- Explain the use case
- Provide examples

### Pull Requests

1. Fork the repository
2. Create a branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests
5. Run tests (`pytest`)
6. Format code (`black .`)
7. Commit (`git commit -m 'Add amazing feature'`)
8. Push (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Setup

\```bash
git clone https://github.com/YOUR_USERNAME/REPO.git
cd REPO
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pre-commit install
\```

## Code Standards

### Style Guide

- Follow PEP 8
- Use Black for formatting
- Maximum line length: 100
- Use type hints

### Documentation

- Add docstrings to all public functions
- Use Google style
- Include examples

### Testing

- Write tests for new features
- Maintain >80% coverage
- Use pytest

### Commit Messages

- Use present tense
- Use imperative mood
- First line ≤72 characters
- Reference issues

Examples:
\```
Add feature X
Fix bug in Y
Update documentation for Z
\```

## Questions?

Open an issue with tag "question"
```

### 7.3 CHANGELOG.md

**Sigue [Keep a Changelog](https://keepachangelog.com/):**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Feature X
- Feature Y

### Changed
- Improved Z

### Fixed
- Bug in W

## [0.1.0] - 2024-01-15

### Added
- Initial release
- Feature A
- Feature B

### Changed
- Refactored C

## [0.0.1] - 2024-01-01

### Added
- Basic functionality

[Unreleased]: https://github.com/user/repo/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/user/repo/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/user/repo/releases/tag/v0.0.1
```

**Categorías:**
- `Added` - nuevas features
- `Changed` - cambios en funcionalidad existente
- `Deprecated` - features que se eliminarán
- `Removed` - features eliminadas
- `Fixed` - bug fixes
- `Security` - vulnerabilidades

---

## 8. CI/CD y Automatización

### 8.1 GitHub Actions

**`.github/workflows/ci.yml`:**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run tests
        run: |
          pytest --cov=corpus_query_language --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  lint:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Check formatting
        run: black --check src tests

      - name: Lint
        run: ruff check src tests

      - name: Type check
        run: mypy src
```

**Explicación:**

- **Test job**: Ejecuta tests en múltiples OS y versiones de Python
- **Lint job**: Verifica calidad de código
- **Matrix strategy**: Prueba todas las combinaciones
- **Coverage upload**: Sube cobertura a Codecov

### 8.2 Badges en README

Después de configurar CI/CD:

```markdown
[![CI](https://github.com/USER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/USER/REPO/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/USER/REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/USER/REPO)
```

### 8.3 Configurar Codecov

1. Ve a https://codecov.io/
2. Conecta tu repositorio GitHub
3. Copia el token
4. En GitHub: Settings → Secrets → New repository secret
5. Nombre: `CODECOV_TOKEN`, Valor: [tu token]

---

## 9. Pull Request y Code Review

### 9.1 Preparar el Pull Request

```bash
# Antes de abrir PR, asegúrate de que todo esté limpio

# 1. Sincroniza con upstream
git fetch upstream
git rebase upstream/main

# 2. Ejecuta todos los checks
black src tests
ruff check --fix src tests
mypy src
pytest --cov=corpus_query_language

# 3. Revisa los cambios
git diff main

# 4. Squash commits si hay muchos pequeños (opcional)
git rebase -i HEAD~5  # Últimos 5 commits

# 5. Push a tu fork
git push origin feature/professional-refactor
```

### 9.2 Template de Pull Request

**En GitHub, crea el PR con este template:**

```markdown
## Description

Brief summary of changes (1-2 sentences).

Fixes #123 (si aplica)

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Changes Made

Detailed list of all changes:

### Code Quality
- Added type hints to all modules (100% coverage)
- Replaced print statements with logging
- Improved error handling with specific exceptions
- Translated French comments to English

### Testing
- Created comprehensive test suite with pytest
- Achieved 85% code coverage
- Added integration tests

### Documentation
- Rewrote README with examples and API docs
- Created CONTRIBUTING.md
- Added CHANGELOG.md

### DevOps
- Configured pre-commit hooks
- Set up GitHub Actions CI/CD
- Added Black, Ruff, and MyPy configurations

## Testing

Describe how you tested these changes:

- [ ] All existing tests pass
- [ ] Added new tests for new features
- [ ] Tested on Python 3.9, 3.10, 3.11, 3.12
- [ ] Tested on Linux, Windows, macOS
- [ ] Manual testing of CLI

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added for new features
- [ ] All tests pass locally
- [ ] Changes are backward compatible

## Screenshots (if applicable)

Before/After comparisons, CLI output, etc.

## Additional Notes

Any other context, concerns, or discussion points.

## Breaking Changes

None. All changes are fully backward compatible.

## Migration Guide (if applicable)

N/A - No migration needed.
```

### 9.3 Durante Code Review

**Responder a comentarios:**

```markdown
# Buena respuesta
> Por qué cambiaste esto de X a Y?

Buena pregunta! Lo cambié porque:
1. Y es más eficiente (benchmark adjunto)
2. Y sigue mejor las convenciones de Python (PEP 8)
3. Y facilita testing (ejemplo adjunto)

¿Prefieres que use X por alguna razón específica?

# Mala respuesta
> Por qué cambiaste esto?

Porque es mejor.  # ❌ No explicativo
```

**Hacer cambios solicitados:**

```bash
# 1. Crea commits separados para cambios del review
git add archivo_modificado.py
git commit -m "Address review: Improve error messages"

# 2. Push
git push origin feature/professional-refactor

# 3. Responde en el PR
"✅ Fixed in commit abc1234"
```

**Etiquetar al revisor:**

```markdown
@matgille I've addressed all your comments. Could you take another look?

Changes made:
- Improved docstrings as requested
- Added edge case tests
- Simplified the logic in parser.py

Thanks for the feedback!
```

### 9.4 Después de Aprobación

```bash
# El mantenedor hará merge, pero si te piden squash:

# 1. Squash todos los commits
git rebase -i upstream/main

# En el editor, cambia "pick" por "squash" excepto el primero:
pick abc1234 Add type hints
squash def5678 Fix typo
squash ghi9012 Address review comments
# Guarda y edita el mensaje de commit combinado

# 2. Force push (SOLO en tu fork)
git push --force origin feature/professional-refactor
```

---

## 10. Buenas Prácticas de Colaboración

### 10.1 Comunicación Efectiva

**DO:**
✅ Sé específico y claro
✅ Proporciona contexto
✅ Muestra ejemplos
✅ Sé respetuoso y profesional
✅ Agradece el feedback
✅ Explica tus decisiones

**DON'T:**
❌ Asumas que todos entienden tu contexto
❌ Uses jerga sin explicación
❌ Seas defensivo con el feedback
❌ Hagas cambios sin explicación
❌ Ignores comentarios

### 10.2 Gestión de Tiempo

```markdown
## Mi Cronograma de Trabajo

| Semana | Tareas | Horas Estimadas |
|--------|--------|-----------------|
| 1 | Setup + Type hints | 12h |
| 2 | Tests + Logging | 15h |
| 3 | Docs + CI/CD | 10h |
| 4 | Review + Polish | 8h |

Total: ~45 horas (1 mes a tiempo parcial)

Disponibilidad para reviews:
- Lunes-Viernes: 18:00-21:00 (GMT-5)
- Fines de semana: Flexible

Objetivo: PR abierto para 2024-02-01
```

### 10.3 Trabajo Incremental

**Estrategia de múltiples PRs:**

```markdown
## Roadmap de PRs

PR #1: Setup and Tooling (MERGED ✅)
- .gitignore
- pyproject.toml
- requirements-dev.txt
- pre-commit config

PR #2: Type Hints (EN REVIEW 👀)
- Add type hints to all modules
- Configure MyPy
Status: Waiting for review

PR #3: Testing Suite (DRAFT 📝)
- Create test structure
- Add core tests
- Setup coverage
Status: WIP, 60% complete

PR #4: Documentation (PLANNED 📅)
- README improvements
- CONTRIBUTING.md
- CHANGELOG.md
Target: After PR #2 merged

PR #5: CI/CD (PLANNED 📅)
- GitHub Actions
- Automated testing
Target: After PR #3 merged
```

**Ventajas:**
- Reviews más fáciles y rápidas
- Menor riesgo de conflictos
- Progreso visible
- Más fácil revertir si algo falla

### 10.4 Manejo de Conflictos

**Cuando hay desacuerdos técnicos:**

```markdown
## Desacuerdo: ¿Usar Black o mantener estilo actual?

### Mi Propuesta: Usar Black
Pros:
- Elimina debates sobre formato
- Auto-formateo = menos trabajo manual
- Estándar de la industria
- Fácil integración con CI

Cons:
- Cambiará mucho código existente
- Line length de 88 vs 79 actual

### Alternativa: Mantener estilo actual
Pros:
- Sin disruption
- Familiaridad para contributors actuales

Cons:
- Inconsistencia eventual
- Más trabajo en code reviews
- Dificulta automatización

### Mi Recomendación
Usar Black pero:
1. En PR separado (fácil de revertir)
2. Con line-length=100 (compromiso)
3. Solo en archivos que estoy modificando

¿Qué opinas @matgille?
```

**Cuando hay bloqueos:**

```markdown
Hi @matgille,

I haven't heard back on PR #123 for 2 weeks. I understand you're busy!

Options to move forward:
1. I can split it into smaller PRs if that helps
2. I can address any concerns you have
3. If it's not a priority now, I can shelf it and revisit later

No pressure - just want to make sure I'm not blocking anything.

Thanks!
```

### 10.5 Documentar Decisiones

**Para decisiones importantes, crea un ADR (Architecture Decision Record):**

```markdown
# ADR 001: Use Black for Code Formatting

## Status
Accepted

## Context
We need consistent code formatting across the project. Currently there's
inconsistency in:
- Line lengths (ranging from 70-120)
- Indentation (mixed 2 and 4 spaces)
- Quote styles (mixed single and double)

## Decision
We will use Black for automatic code formatting with these settings:
- Line length: 100 characters
- Python versions: 3.9+

## Consequences

Positive:
- Zero debate on formatting
- Automatic enforcement via pre-commit
- Consistent codebase
- Reduced code review time

Negative:
- One-time large diff when applying
- Some developers prefer manual control
- 100 chars longer than PEP 8's 79

## Alternatives Considered

1. Manual PEP 8 enforcement
   - Rejected: Too time-consuming, inconsistent results

2. autopep8
   - Rejected: Less opinionated, still allows variations

3. YAPF
   - Rejected: More configuration needed, less standard

## Implementation
- Add black to requirements-dev.txt
- Configure in pyproject.toml
- Add to pre-commit hooks
- Run on all files in separate commit for easy revert
```

### 10.6 Celebrar Éxitos

```markdown
🎉 Milestone: PR Merged!

Big thanks to @matgille for:
- Detailed code review
- Great suggestions on error handling
- Patience with my questions

What we accomplished:
✅ 100% type hints
✅ 85% test coverage
✅ Professional documentation
✅ CI/CD pipeline

Next steps:
- Monitor for any issues
- Plan v0.2.0 features
- Update PyPI package

Thanks to everyone who contributed feedback!
```

---

## 11. Checklist Final

### Antes de Abrir PR

```markdown
## Pre-PR Checklist

### Código
- [ ] Todo el código tiene type hints
- [ ] Todos los docstrings están completos
- [ ] No hay print statements (solo logging)
- [ ] Sin código comentado
- [ ] Sin TODOs sin issue asociado

### Tests
- [ ] Todos los tests pasan localmente
- [ ] Coverage ≥ 80%
- [ ] Tests added for new features
- [ ] Edge cases covered

### Calidad
- [ ] Black formatting applied
- [ ] Ruff linting passed
- [ ] MyPy type checking passed
- [ ] Pre-commit hooks pass

### Documentación
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] API docs complete
- [ ] Examples work

### Git
- [ ] Commits are logical and atomic
- [ ] Commit messages are clear
- [ ] Branch is up to date with main
- [ ] No merge conflicts

### CI/CD
- [ ] GitHub Actions configured
- [ ] All CI checks pass
- [ ] Coverage reports upload
```

### Después de Merge

```markdown
## Post-Merge Tasks

- [ ] Cerrar issues relacionados
- [ ] Actualizar project board
- [ ] Notificar a stakeholders
- [ ] Actualizar documentación externa
- [ ] Planificar próximos pasos
- [ ] Escribir blog post (opcional)
- [ ] Agradecer a reviewers
```

---

## 12. Recursos Adicionales

### Documentación Oficial

- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [Python Packaging Guide](https://packaging.python.org/)

### Herramientas

- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pre-commit](https://pre-commit.com/)

### Lecturas Recomendadas

- "Effective Python" by Brett Slatkin
- "Python Testing with pytest" by Brian Okken
- "Clean Code" by Robert C. Martin
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

### Cursos

- [Real Python - Testing](https://realpython.com/pytest-python-testing/)
- [Real Python - Type Checking](https://realpython.com/python-type-checking/)
- [GitHub Skills - CI/CD](https://skills.github.com/)

---

## Conclusión

Mejorar una librería de Python a estándares profesionales es un proceso que requiere:

1. **Comunicación clara** con mantenedores
2. **Planificación cuidadosa** del trabajo
3. **Ejecución incremental** con PRs pequeños
4. **Testing exhaustivo** de todos los cambios
5. **Documentación completa** para usuarios y desarrolladores
6. **Automatización** de calidad y testing
7. **Paciencia y profesionalismo** durante code review

Recuerda: **El objetivo no es solo mejorar el código, sino hacerlo de manera que beneficie a toda la comunidad y sea sostenible a largo plazo.**

¡Buena suerte con tus contribuciones! 🚀

---

**Autor**: Claude Code
**Fecha**: 2025-01-16
**Versión**: 1.0
**Licencia**: CC-BY-SA-4.0
