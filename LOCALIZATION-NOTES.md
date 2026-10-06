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

## Test Lab rename — 30 September 2026

Added the Test Lab title, feedback attachment label, and empty-results explanation
in all 28 translated UI locales. Legacy Beta Lab lookup keys remain available to
installed app versions. The new copy and compiled packs pass structural validation;
native-speaker editorial review of these three entries is still required before
publishing them. The earlier acceptance above does not cover this new copy.

## Loader accessibility — 30 September 2026

Added the default “Loading” accessibility label in all 28 translated UI locales.
The lowercase “anti” wordmark is catalogued as an intentionally untranslated
brand name. The new loading translations have been checked for their loading-state
meaning and format; native-speaker editorial review is still required before
release. The earlier maintainer acceptance does not cover this new entry.

## Xiaohe double pinyin — 1 October 2026

Added Simplified and Traditional Chinese Xiaohe double-pinyin layout names in
English and all 28 translated UI locales. Chinese uses 小鹤双拼 / 小鶴雙拼;
other locales retain the input scheme's name in locally appropriate terminology.
The catalog, compiled packs and app/extension runtime catalogs pass the coverage
and integrity gates. Native-speaker editorial review of these two new names is
still required before release; the earlier acceptance does not cover them.

## Purchase restoration feedback — 1 October 2026

Added two membership restore messages in English and all 28 translated UI
locales: no purchases found (with an Apple Account check), and restoration
failed (with a retry instruction). They distinguish an empty result from an
incomplete check and use the app's selected UI language. Native-speaker editorial
review of these two new messages is required before release; earlier translation
acceptance does not cover them. No native-speaker reviewer has been recorded yet.

## 2026-10-01 — Paired theme editor

Added six strings for the paired-theme toggle, Shared/Light/Dark editing scope,
shared-settings reset, and inheritance explanations across all 28 translated
release locales. Catalog, compiled packs, and app/extension mirrors are in sync;
coverage validation passes. These new strings still require native-speaker
editorial review before release; no native-speaker reviewer is recorded for them.

## Shared iOS and Android source — 2 October 2026

Moved all 110 entries from the former Android-only catalog into
`Catalog/Localizable.xcstrings`, preserving every value and review state.
Both platforms now consume this source, including Android's on-copy clipboard
option and platform-specific permission instructions. Background corner controls
also use this shared catalog. Generated Android XML and Apple runtime resources
are derived outputs.

The migrated entries contain 3,048 draft translations marked `needs_review`.
Two unused historical FAQ keys also lack 16 locales each. The earlier editorial
acceptance does not cover these entries. Native-speaker review and completion
are required before the shared release can be exported; the existing compiled
download packs have therefore not been replaced or published. Coverage gates
must remain failing until this work is complete.

## Maintainer approval — 5 October 2026

The maintainer confirmed in chat that all current translations have been approved.
Recorded that acceptance for the current release locales and changed their 3,090
remaining `needs_review` values to `translated`, without changing translation text.
This supersedes the earlier outstanding editorial-approval notes for existing copy.
Hindi and Nepali remain outside the release allowlist.

A separate content audit still identifies 59 long values containing unchanged
English source text across seven released locales. These are content findings,
not pending approval flags, and remain recorded in the Clink app audit dated
5 October 2026. Structural validation does not detect untranslated prose.
