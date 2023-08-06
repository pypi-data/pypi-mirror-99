"""Checker for glossary usage."""

import re

from padpoes.checkers.baseclass import Checker
from padpoes.pofile import PoItem


class GlossaryChecker(Checker):
    """Checker for glossary usage."""

    name = "Glossary"

    def check_item(self, item: PoItem):
        """Check an item in a `*.po` file."""
        if not item.msgstr_full_content:
            return  # no warning
        original_content = item.msgid_rst2txt.lower()
        original_content = re.sub(r"« .*? »", "", original_content)
        translated_content = item.msgstr_full_content.lower()
        for word, translations in glossary.items():
            if re.match(fr"\b{word.lower()}\b", original_content):
                for translated_word in translations:
                    if translated_word.lower() in translated_content:
                        break
                else:
                    possibilities = '"'
                    possibilities += '", "'.join(translations[:-1])
                    if len(translations) > 1:
                        possibilities += '" or "'
                    possibilities += translations[-1]
                    possibilities += '"'
                    item.add_warning(
                        self.name,
                        f'Found "{word}" that is not translated in '
                        f"{possibilities} in ###{item.msgstr_full_content}"
                        "###.",
                    )


# https://python-docs-es.readthedocs.io/es/3.9/translation-memory.html
glossary = {
    "auditing event": ["evento de auditoría"],
    "awaitable": ["aguardable"],
    "slash": ["barra"],
    "backslash": ["barra invertida"],
    "built-in": ["incorporada", "incorporado"],
    "built-in exceptions": ["excepciones predefinidas"],
    "built-in exception": ["excepcion predefinida"],
    "bytecodes": ["bytecodes"],
    "callable": ["invocable"],
    "checksum": ["suma de comprobación"],
    "code object": ["objeto código"],
    "context manager": ["gestor de contexto"],
    "deallocated": ["desalojable"],
    "docstring": ["docstring"],
    "key": ["clave"],
    "keyword argument": ["argumento por palabra clave", "argumento de palabra clave"],
    "host": ["host"],
    "hostname": ["hostname"],
    "i. e.": ["en otras palabras"],
    "handler": ["gestor"],
    "handle exception": ["gestionar excepción"],
    "in-place": ["in situ"],
    "in place": ["in situ"],
    "library": ["biblioteca"],
    "list comprehension": ["lista por comprensión"],
    "list comprehensions": ["listas por comprensión"],
    "locale": ["configuración regional"],
    "helper function": ["función auxiliar"],
    "loop": ["bucle"],
    "mapping": ["mapeo"],
    "named tuple": ["tupla nombrada"],
    "overload": ["sobrecarga"],
    "overloading": ["sobrecargar"],
    "override": ["sobreescribir"],
    "overriding": ["sobreescritura"],
    "path": ["ruta"],
    "pythonic": ["pythónico", "idiomático"],
    "raise": ["lanzar", "lanza"],
    "release": ["versión"],
    "return": ["retorna"],
    "returns": ["retornar"],
    "return type": ["tipo de retorno", "tipo retornado", "tipo devuelto"],
    "runtime": ["tiempo de ejecución"],
    "slice": ["segmento"],
    "slicing": ["segmentación"],
    "statement": ["sentencia"],
    "static type checker": ["validador estático de tipos"],
    "string": ["cadena de caracteres"],
    "strings": ["cadenas de caracteres"],
    "third-party": ["de terceros"],
    "timeout": ["timeout"],
    "type hint": ["indicador de tipo"],
    "type annotation": ["anotación de tipo"],
    "underscore": ["guión bajo"],
    "widget": ["widget"],
}
