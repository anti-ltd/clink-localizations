#!/usr/bin/env python3
"""Regression cases for release hazards that source-key coverage misses."""
import copy
import hashlib
import importlib.util
import json
import pathlib
import plistlib
import tempfile
import unittest

TOOLS = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("validator", TOOLS / "validate-localization.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
catalog_spec = importlib.util.spec_from_file_location("catalog_validator", TOOLS / "validate-catalog.py")
catalog_validator = importlib.util.module_from_spec(catalog_spec)
catalog_spec.loader.exec_module(catalog_validator)
release_spec = importlib.util.spec_from_file_location("release_validator", TOOLS / "validate-release.py")
release_validator = importlib.util.module_from_spec(release_spec)
release_spec.loader.exec_module(release_validator)


class CompiledValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.pack = pathlib.Path(self.temporary.name) / "fr.lproj"
        self.pack.mkdir()
        self.catalog = {"strings": {
            "Copy color": {"localizations": {"fr": {"stringUnit": {"state": "translated", "value": "Copier la couleur"}}}},
            "%lld word": {"localizations": {"fr": {"variations": {"plural": {
                "one": {"stringUnit": {"state": "translated", "value": "%lld mot"}},
                "other": {"stringUnit": {"state": "translated", "value": "%lld mots"}},
            }}}}},
        }}
        self.strings = {"Copy color": "Copier la couleur"}
        self.plurals = {"%lld word": {
            "NSStringLocalizedFormatKey": "%#@value@",
            "value": {"NSStringFormatSpecTypeKey": "NSStringPluralRuleType",
                      "NSStringFormatValueTypeKey": "lld", "one": "%lld mot", "other": "%lld mots"},
        }}

    def check(self):
        (self.pack / "Localizable.strings").write_bytes(plistlib.dumps(self.strings))
        (self.pack / "Localizable.stringsdict").write_bytes(plistlib.dumps(self.plurals))
        return validator.validate(self.pack, self.catalog)

    def test_complete_pack(self):
        self.assertEqual(self.check(), [])

    def test_stale_missing_key(self):
        self.catalog["strings"]["Paste color"] = copy.deepcopy(self.catalog["strings"]["Copy color"])
        self.assertTrue(any("missing translated" in error for error in self.check()))

    def test_same_keys_edited_translation(self):
        self.strings["Copy color"] = "Copy color"
        self.assertTrue(any("compiled value differs" in error for error in self.check()))

    def test_missing_plural_form(self):
        del self.plurals["%lld word"]["value"]["other"]
        self.assertTrue(any("compiled plural values differ" in error for error in self.check()))

    def test_wrong_plural_argument_type(self):
        self.plurals["%lld word"]["value"]["NSStringFormatValueTypeKey"] = "f"
        self.assertTrue(any("argument type differs" in error for error in self.check()))

    def test_tampered_plural_placeholder(self):
        self.plurals["%lld word"]["value"]["one"] = "%@ mot"
        self.assertTrue(any("compiled plural values differ" in error for error in self.check()))

    def test_unknown_key(self):
        self.strings["Old removed copy"] = "Ancien texte"
        self.assertTrue(any("unknown catalog" in error for error in self.check()))

    def test_duplicate_table_key(self):
        self.strings["%lld word"] = "%lld mot"
        self.assertTrue(any("duplicated" in error for error in self.check()))


class CatalogValidationTests(unittest.TestCase):
    def test_reordered_types_need_positions(self):
        self.assertNotEqual(catalog_validator.signature("%@: %lld"),
                            catalog_validator.signature("%lld: %@"))
        self.assertEqual(catalog_validator.signature("%@: %lld"),
                         catalog_validator.signature("%2$lld: %1$@"))

    def test_nested_incomplete_plural_branch_is_visible(self):
        units = catalog_validator.units({"variations": {"device": {"iphone": {
            "variations": {"plural": {
                "one": {"stringUnit": {"state": "translated", "value": "%lld mot"}},
                "other": {},
            }},
        }}}})
        self.assertEqual(len(units), 2)
        self.assertIn({}, units)


class ReleaseValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = pathlib.Path(self.temporary.name)
        (self.root / "Catalog").mkdir()
        self.pack = self.root / "Localizations/en.lproj"
        self.pack.mkdir(parents=True)
        self.catalog = self.root / "Catalog/Localizable.xcstrings"
        self.catalog.write_text(json.dumps({"sourceLanguage": "en", "strings": {"Copy color": {}}}))
        (self.pack / "Localizable.strings").write_bytes(plistlib.dumps({"Copy color": "Copy color"}))
        (self.root / "release-locales.txt").write_text("en\n")
        self.fingerprint = self.root / "Localizations/.catalog-sha256"
        self.fingerprint.write_text(hashlib.sha256(self.catalog.read_bytes()).hexdigest() + "\n")
        self.assertEqual(release_validator.validate_release(self.root), [])

    def test_catalog_drift_rejects_stale_pack(self):
        self.catalog.write_text(self.catalog.read_text() + "\n")
        self.assertTrue(any("stale" in error for error in release_validator.validate_release(self.root)))

    def test_missing_stamp(self):
        self.fingerprint.unlink()
        self.assertTrue(any("stale" in error for error in release_validator.validate_release(self.root)))

    def test_missing_release_locale(self):
        (self.root / "release-locales.txt").write_text("en\nfr\n")
        self.assertTrue(any("exactly match" in error for error in release_validator.validate_release(self.root)))

    def test_matching_stamp_does_not_hide_edited_compiled_value(self):
        (self.pack / "Localizable.strings").write_bytes(plistlib.dumps({"Copy color": "Different text"}))
        self.assertTrue(any("compiled value differs" in error for error in release_validator.validate_release(self.root)))


if __name__ == "__main__":
    unittest.main()
