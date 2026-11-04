# Modifying and relinking the LGPL / GPL components

日本語の要約：AI DevEnv Bench の配布物に入っている LGPL／GPL の部品は、利用者が自分で改変・再ビルドし、
差し替えて使えます。共有ライブラリー（`.so`／`.dll`）は同じ名前の互換ファイルに置き換えます。静的に結合された
LGPL（Chromium 内の Blink・FFmpeg、Bun 内の JavaScriptCore・TinyCC、cmake-gui 内の Qt）は、このリポジトリの
対応ソースからプログラム全体を再ビルドして置き換えます。改変した実行環境は、公式スコアの整合性確認に通りません
（ハッシュで固定しているため）。これは採点上の扱いであり、改変・再リンクして個人で使う権利を制限するものではありません。
macOS では、差し替えたファイルに ad-hoc 署名（`codesign --force --sign -`）を付け直してください（Apple Silicon は署名のないコードを実行しません）。

All paths below are as they appear after extracting the AI DevEnv Bench 1.0.0 ZIP (Windows: the
launcher restores `Data.bin` into `app/`; the runtime is `app/runtime/`. macOS: the runtime is
`AIDevBench.app/Contents/Resources/app/runtime/`, written `<mac>/` below). The benchmark pins every runtime
file by SHA-256, so a modified runtime is reported as not eligible for an official score. That is a rule of
the scoring service only: AI DevEnv Bench's license (section 5) keeps every right the third-party licenses
give you, including modification, reverse engineering for debugging such modifications, and relinking.

## Shared libraries (replace the file)

These components are separate shared libraries or separate programs. Build a modified version from the
source in this repository with a compatible ABI and replace the file of the same name.

| Platform | Files | Component (see SOURCES.md) |
|---|---|---|
| Linux | `app/runtime/application/native-cross/host/lib/libc.so.6`, `libm.so.6`, `ld-linux-*.so.*`, `libgcc_s.so.1`, `libstdc++.so.6` | Ubuntu glibc, gcc-14 |
| Linux | `app/runtime/application/runtime/tools/lib/*`, `app/runtime/application/runtime/portable/lib/*` | Ubuntu acl, gcc-14, binutils (libctf, libsframe), ... |
| Linux | `app/runtime/application/runtime/web/browser/chromium-debian-156.0.8078.73/lib*.so*` | Ubuntu and Debian library packages |
| Linux | `app/runtime/application/runtime/tools/prefix/bin/{bash,head,ls,nl,sed,tr}`, `.../portable/prefix/bin/readelf` | Ubuntu bash, coreutils, sed, binutils |
| Windows | `app/runtime/route-runtime/git/usr/bin/*.dll`, `app/runtime/bundle/tools/git/usr/bin/*.dll` | MSYS2 runtime, libiconv, gettext |
| Windows | `app/runtime/route-runtime/git/ucrt64/bin/*.dll`, `.../git-native/clangarm64/bin/*.dll` | mingw-w64 libiconv, gettext, libidn2, libunistring |
| Windows | Git, Bash and GNU tools under `.../git/`, `.../git-native/` | Git for Windows, MSYS2 packages |
| macOS | `<mac>/application/runtime/tools/prefix/bin/{bash,git,head,ls,nl,sed,tr}` (with Git's `libexec/git-core/`), `<mac>/application/runtime/portable/bin/touch` | GNU Bash, coreutils, sed and Git built from source: `macos/gnu-tools/BUILD.md` in `aidevbench-1.0.0-src-macos-gnu-tools.tar` |

Ubuntu and Debian source packages build with `dpkg-source -x <name>.dsc` and `dpkg-buildpackage -b`
on the matching distribution release (Ubuntu 24.04 "noble" for `ubuntu/`, Debian 12 "bookworm" for
`debian/`). MSYS2 / Git for Windows source packages (`*.src.tar.zst`, `*.src.tar.gz`) contain the PKGBUILD,
patches and upstream archives; build them with `makepkg` in an MSYS2 / Git for Windows SDK environment.

## Chromium for Windows (snapshot r1705623)

`app/runtime/bundle/browsers/chromium-1705623/` is the unmodified Chromium snapshot build 156.0.8076.0
(`chromium/src@3e4b22a1d5ad1c1e101c90668f7015e361de5c79`) for x64 and ARM64. Blink (LGPL-2.0/2.1 parts) and
FFmpeg (built as LGPL-2.1: `CONFIG_GPL 0`, `CONFIG_NONFREE 0`, see
`src/third_party/ffmpeg/chromium/config/Chrome/win/*/config.h`) are linked into `chrome.dll`.

1. Join and unpack `aidevbench-1.0.0-src-chromium-156.0.8076.0-r1705623.tar.xz.NN`
   (`python3 scripts/verify_assets.py <folder> --join`, then `tar -xJf ...`).
   The tree is what `gclient sync` produces for `target_os = ["win"]` at that commit:
   `src/` plus every git dependency of `src/DEPS` at its pinned revision.
   `AIDEVBENCH-CHROMIUM-SOURCE-FETCH.json` lists each dependency (URL, commit, tree id). Test-data,
   benchmark and documentation repositories that are not used to build the browser are listed there
   under `excluded` with URL and commit instead of being included. Prebuilt toolchains and test data
   that `gclient runhooks` downloads (CIPD/GCS objects, e.g. clang, Rust, Node.js) are listed under
   `non_git`; the `node_modules` archive used to build the browser's WebUI is included in `gcs-objects/`.
2. Build as described in `src/docs/windows_build_instructions.md`. The snapshot builders use
   `src/infra/config/generated/builders/ci/Win x64 Builder/gn-args.json` (x64) and
   `.../ci/win-arm64-rel/gn-args.json` (ARM64): `is_debug=false`, `is_component_build=false`,
   `proprietary_codecs=true`, `ffmpeg_branding="Chrome"`, `symbol_level=1`, `dcheck_always_on=false`.
3. Replace the files of `chromium-1705623/` with your build.

## Chromium for macOS (snapshot Mac_Arm r1705623)

`<mac>/application/runtime/web/browser/chromium-1705623/Chromium.app` is the Chromium snapshot build
156.0.8076.0 for macOS arm64, built from the same `chromium/src` commit as the Windows snapshot above; the
benchmark only re-signs it ad hoc. Blink and FFmpeg (LGPL-2.1 build, see
`src/third_party/ffmpeg/chromium/config/Chrome/mac/arm64/config.h`) are linked into `Chromium Framework`.
Use the same source archive; its `gclient` tree was synced for Windows, so add the macOS-only dependencies
with `target_os = ["mac"]` in `.gclient` and `gclient sync` at the same commit. Then build as described in
`src/docs/mac_build_instructions.md` with the gn arguments of the Mac arm64 CI builder under
`src/infra/config/generated/builders/ci/`, replace `Chromium.app` and sign it again ad hoc.

## Chromium for Linux (Debian 156.0.8078.73-1~deb12u1)

`app/runtime/application/runtime/web/browser/chromium-debian-156.0.8078.73/` holds the files of the Debian 12
packages `chromium` and `chromium-common` (the main executable is renamed `headless_shell.real`) and their
shared libraries. Rebuild with the Debian source package in
`aidevbench-1.0.0-src-linux-debian-12-chromium-156.0.8078.73.tar` (`dpkg-source -x chromium_*.dsc`,
`dpkg-buildpackage -b`) on Debian 12, then replace the files.

## Bun 1.4.4 (Linux and macOS)

`app/runtime/application/runtime/bun/bun` (Linux) and `<mac>/application/runtime/bun/bun` (macOS) are the
official Bun 1.4.4 release binaries. On macOS, Bun uses the system ICU (`libicucore`). Each binary statically links
JavaScriptCore/WebKit (LGPL-2.0 and BSD) and TinyCC (LGPL-2.1). `aidevbench-1.0.0-src-linux-bun-1.4.4.tar` has:

- `bun-v1.4.4.tar.gz` — the Bun source at tag `bun-v1.4.4`, including Bun's JavaScriptCore bindings
  (the object files that use JavaScriptCore) and `scripts/build/deps/*.ts`, which pin every bundled library;
- `oven-sh-webkit-d6375c72affe0f70222cdcb45012b10f0bf3a9d5-jsc.tar.xz` — `oven-sh/WebKit` at the pinned
  `WEBKIT_VERSION`, with the parts used for Bun's JavaScriptCore build (PORT=JSCOnly);
- `oven-sh-tinycc-05f0fafaa3be31e31d7b4b5c17dc60f62c991171.tar.gz` — TinyCC at the pinned commit.

Bun's own `LICENSE.md` gives the relink procedure: put WebKit at `vendor/WebKit`, run
`bun sync-webkit-source` if needed, then `bun run build:local`. This compiles JavaScriptCore and Bun's
bindings and links a new `bun` binary.

## cmake-gui (Windows and Linux)

`cmake-gui` in the official CMake 4.4.5 binaries statically links Qt (LGPL-3.0):
Windows `app/runtime/bundle/tools/signed-native/cmake/bin/cmake-gui.exe` uses qtbase 6.10.1, Linux
`app/runtime/application/runtime/portable/prefix/bin/cmake-gui` uses Qt 5.12.0. `cmake-4.4.5.tar.gz`
contains Kitware's exact Qt build scripts (`Utilities/Release/win/qtbase-6.10.1-win-msvc.cmake`,
`Utilities/Release/linux/*/deps/Dockerfile` and `qt-install.patch`); the Qt archives are included with the
hashes those scripts check. Build Qt with those scripts, build CMake against it with
`-DBUILD_QtDialog=ON`, and replace `cmake-gui`. cmake-gui is not used by the benchmark itself.

## Git (Linux) and the GNU tools of macOS

See `linux/git/BUILD.md` in `aidevbench-1.0.0-src-linux-git-2.56.0.tar` and `macos/gnu-tools/BUILD.md` in
`aidevbench-1.0.0-src-macos-gnu-tools.tar`.

## Windows target SDK (mingw-w64)

`app/runtime/bundle/tools/signed-native/sdk/` (Windows), `app/runtime/application/native-cross/sdk/` (Linux) and
`<mac>/application/native-cross/sdk/` (macOS, the same bytes as Linux) are the x86_64 sysroot of llvm-mingw 20250709 (LLVM 20.1.8, mingw-w64 commit a0e69f7). Headers derived from
Wine are LGPL-2.1-or-later and are themselves source. The CRT and libraries are rebuilt from
`mingw-w64-a0e69f7.tar.gz` with the scripts in `llvm-mingw-20250709.tar.gz` (`build-mingw-w64.sh`,
`build-mingw-w64-libraries.sh`).
