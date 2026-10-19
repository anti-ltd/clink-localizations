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

## Brazilian Portuguese draft — 19 October 2026

Added `pt-BR` to all 5,476 translatable keys in the shared catalog, including
the nine pluralized keys (5,485 string units). European Portuguese (`pt`) and
all other existing locale values are unchanged. The 38 entries marked
`shouldTranslate: false` continue to use their original names or symbols.

This is an AI-assisted draft adapted from the existing Portuguese catalog,
with sentence-level revisions for Brazilian usage. It uses `você`, `arquivo`,
`tela`, `salvar`, `compartilhar` and `assinatura`; platform-specific instructions
distinguish iOS Ajustes from Android Configurações. The draft includes current
and historical app copy, keyboard panels, accessibility text, and Android-only
permissions, downloads and purchases. Format arguments, plural structures,
code examples and links are retained.

Every new string unit is `needs_review`. No native-speaking reviewer or release
approval has been recorded. Coverage and format checks are technical evidence,
not editorial approval. The 5 October acceptance applies to the earlier release
locales and does not approve this translation. `pt-BR` stays out of
`release-locales.txt`, downloadable releases, and both apps' supported UI lists.

Before enabling or publishing:

1. Have a Brazilian Portuguese native-speaking editor review the full locale,
   including grammar, consistent feature names, permission paths, plurals,
   accessibility labels, purchase terms and longer help text. Record the
   reviewer, date and approved revision here, then update the reviewed states.
2. Follow the app repository's `docs/19-adding-a-language.md` UI checklist:
   add the locale, `Português (Brasil)` name and Brazilian flag on both platforms;
   preserve regional matching so `pt-BR` does not resolve to European `pt`;
   translate the iOS permission-purpose catalog; and add locale-resolution tests.
3. Add `pt-BR` to the release allowlist, regenerate the release packs, Apple
   runtime catalogs and Android resources, and run `make check-localization`.
   Exercise the downloaded iOS app translation, offline extension resources,
   and Android picker/system-language paths with real screens before release.
   Update ANTI's app-language usage guide when the language becomes available.

The iOS keyboard-sound instruction uses Apple's Brazilian terminology from
[Alterar os sons ou a resposta tátil do teclado do iPhone](https://support.apple.com/pt-br/102463).
The editor should confirm labels against the OS versions supported at release.
