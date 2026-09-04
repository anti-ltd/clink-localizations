<p align="center">
  <img src="https://raw.githubusercontent.com/anti-ltd/clink-language-packs/main/icon-1024.png" width="96" alt="Clink app icon">
</p>

<h1 align="center">Clink localizations</h1>

<p align="center">Open UI-language packs for Clink.</p>

Downloadable, verified UI-language packs for Clink. This repository is for the
language users **read the app in**: settings, accessibility text, onboarding,
alerts, and controlled display labels. It is not for typing dictionaries,
emoji aliases, or keyboard layouts; those belong in the other Clink content
repositories.

## Official Clink repositories

[Language packs](https://github.com/anti-ltd/clink-language-packs) · [Localizations](https://github.com/anti-ltd/clink-localizations) · [Layouts](https://github.com/anti-ltd/clink-layouts) · [Profiles](https://github.com/anti-ltd/clink-profiles) · [Themes](https://github.com/anti-ltd/clink-themes) · [Panels](https://github.com/anti-ltd/clink-panels) · [Actions](https://github.com/anti-ltd/clink-actions) · [Fonts](https://github.com/anti-ltd/clink-fonts) · [Sounds](https://github.com/anti-ltd/clink-sounds)

Clone the official repository with:

```sh
git clone git@github.com:anti-ltd/clink-localizations.git
```

## Current status

`Catalog/Localizable.xcstrings` is the editable source catalog and
`release-locales.txt` is the reviewed release allowlist. Run
`./tools/export-localizations.sh` on a Mac after editing it; it compiles the
catalog into the release-ready resources in `Localizations/`.

Do not publish an incomplete locale. A localization is a product surface, not
a collection of strings: every key must be translated and editorially reviewed
by a native speaker before release.

## Included localizations

The release contains every locale listed in `release-locales.txt`. Work-in-progress
translations may remain in the source catalog, but are neither offered in Clink
nor published until every key is translated and editorially reviewed. English
remains bundled as the offline fallback; installed locale resources replace it
at runtime.

## Pack format

Each release asset lives at:

```text
Localizations/<locale>.lproj/Localizable.strings
```

`Localizable.strings` and, where required, `Localizable.stringsdict` are the
compiled Apple resources used by the app. Keeping the native format preserves
format placeholders, plurals, morphology, accessibility text, and every
existing `String(localized:)` call without a fragile source rewrite.

The published release also contains a generated `manifest.json`. Never edit it
by hand: it records each asset's URL, SHA-256 digest, and byte count.

## Make your first localization

1. Edit `Catalog/Localizable.xcstrings` in Xcode.
2. Translate every required key naturally for the locale and platform context.
   Preserve placeholders, plural categories, Markdown, URLs, official iOS
   setting names, and the Clink brand.
3. Have a native-speaking editor review the complete locale.
4. Run `./tools/export-localizations.sh`.
5. Run `python3 tools/validate-localization.py Localizations/<locale>.lproj`.
6. Push to `main`. GitHub Actions validates every pack, builds the manifest,
   and refreshes the `latest` release.

The validator verifies structure. It cannot prove a translation is idiomatic;
native-speaker review is a release gate.

## Use a localization repository in Clink

Clink fetches this official repository's `latest` release automatically during
onboarding and whenever the app returns to the foreground. A selected locale is
downloaded before it is applied; later releases update it automatically while
the bundled English catalog remains the safe fallback.

Anyone can publish a compatible public GitHub repository. In Clink, open
**Repositories**, choose **Add repository**, and enter `owner/repository` (or
its HTTPS GitHub URL). Its verified locale codes then appear in both the
onboarding and App language pickers. Official Clink locales take precedence
when the same locale exists in more than one source.

## Release security

Clink will accept only the canonical GitHub `latest` release for the official
repository or a repository the user explicitly added. Every downloaded file is
size-checked and SHA-256 verified in a staging directory before it becomes
active. The prior verified localization remains active if an update fails.

## Publishing is automatic

Keep `Catalog/`, `Localizations/`, `tools/`, and `.github/workflows/` in your
clone. Add or update a reviewed locale and push to `main`. GitHub Actions
validates each pack, builds the manifest, calculates each asset's hash and size,
and refreshes the `latest` release.
