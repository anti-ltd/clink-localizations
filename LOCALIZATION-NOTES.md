# Localization expansion — 28 September 2026

The expansion adds Romanian (`ro`), Dutch (`nl`), Afrikaans (`af`),
Polish (`pl`), Ukrainian (`uk`), Turkish (`tr`), Czech (`cs`), Slovak (`sk`),
Greek (`el`), Swedish (`sv`), Danish (`da`), Norwegian Bokmål (`nb`),
Finnish (`fi`), Indonesian (`id`), Vietnamese (`vi`), and Traditional Chinese
(`zh-Hant`) as working localizations.

They use the normal supported-language list, `release-locales.txt`, and compiled
`Localizations/` packs. Catalog entries use `translated`, as requested for the
TestFlight branch. There is no separate draft-pack distribution path.

Each locale covers all required keys, including nine pluralized strings. The
app language lists, flags, bundled extension resources, and permission purpose
strings include the additions. “From Photo” and “Surprise Me” are translated
across all active UI languages.

The initial translations use Google Translate, with some Afrikaans passages
from Bing Translator, protected placeholders and links, and subsequent edits
to plurals, common controls, formatting, and permission instructions. Existing
Afrikaans and Turkish translations are retained. Traditional Chinese starts
from the Simplified Chinese catalog, converted with OpenCC's Taiwan vocabulary
configuration and adjusted for selected platform terminology.

On 30 September 2026, the maintainer confirmed that these translations have
been reviewed and accepted for publication. The initial TestFlight review is
complete. Structural validation checks coverage and resource integrity, not
translation quality.

Hindi and Nepali retain incomplete initial catalog entries and are not included
in the supported UI list or release allowlist.
