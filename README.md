# AI DevEnv Bench — 第三者ソフトウェアの対応ソース

このリポジトリは、[AI DevEnv Bench](https://devbench.yuhalab.net) 1.0.0 の配布ZIPに同梱している第三者ソフトウェアのうち、GPL・LGPL・MPL 等の条件によりソースの提供が必要な部品の対応ソースを公開するためのものです。同じ取得元から揃えられる許諾型の部品のソースも、確認しやすいように一緒に置いています。

- 対応ソースの本体は、GitHub Releases の [`v1.0.0-sources`](https://github.com/ylab-aidev/aidevbench-gpl/releases/tag/v1.0.0-sources) に置いています（1ファイル2 GiB未満に分割）。
- どのファイルがどの部品・版・ソースに当たるかは [SOURCES.md](SOURCES.md) と `manifest/` にあります。
- 改変・再ビルド・再リンクの方法は [RELINK.md](RELINK.md) にあります。
- 各ライセンスの原文は、ソースの中と `licenses/` にあります。配布ZIPの `License` フォルダー（`THIRD_PARTY_LICENSES.txt`、`Chromium/credits.html`）にも著作権表示とライセンス原文を入れています。その対応表は `manifest/third-party-licenses.manifest.json` です。

AI DevEnv Bench 本体（権利者 Yuha @ Yuhalab が作成した部分）はクローズドソースで、このリポジトリには含みません。本体の利用条件は配布ZIPの `License/LICENSE.txt` にあります。このリポジトリの第三者ソースには、それぞれの元のライセンスが適用されます。本体の利用条件は、第三者のライセンスが利用者に与える権利（改変、デバッグのための解析、再リンクを含みます）を制限しません。

## 対象の配布物

1.0.0 の配布ZIPは、次の実行環境をそのまま収録します。ZIPを展開した後の `app/runtime/ADMISSION.json`（macOS は `AIDevBench.app/Contents/Resources/app/runtime/ADMISSION.json`）の SHA-256 で、同じ実行環境か確認できます。

| 実行環境 | 版 | `app/runtime/ADMISSION.json` の SHA-256 |
|---|---|---|
| Windows x64 | r15 | `215d38be1ea9ff8e960a6353d7e7e4238ff4f888323b7bda657dc85dd37745b4` |
| Windows ARM64 | r4 | `11bd88ac4b1e5d68b5f6930571455df63f5852b69c697d61e018450f0d748124` |
| Linux x86_64 | r14 | `06a7e091d682e01902efbaefc20d563e864222d3fea3d0255e7992571463fe59` |
| Linux aarch64 | r7 | `8fc8b6c5c23128f73cee75dad7875e962f1e1e9294e05df0343beb402dd5fb6b` |
| macOS arm64 | r4 | `2f00e4f5c2b16fa44794d64b06f344ea91d2c9b00845fd5f8ac911889968be17` |

Windows版は x64／ARM64 共通のZIP（`Data.bin` から実行するCPU用だけを `app/` に復元）、Linux版は x86_64 と aarch64 の別ZIP、macOS版は Apple Silicon 用のZIP（`AIDevBench.app`）です。

## Release の資産

| 資産 | 内容 | サイズ | ファイル数 |
|---|---|---:|---:|
| `aidevbench-1.0.0-src-windows-git-for-windows.tar` | Git for Windows 2.56.0.windows.4 の同梱分（git、Bash、GNU coreutils/grep/sed、MSYS2 runtime、libiconv、gettext、libidn2、libunistring、docx2txt-rs ほか）の source パッケージ | 355.5 MB | 1 |
| `aidevbench-1.0.0-src-mingw-w64-sdk.tar` | Windows 用 SDK（llvm-mingw 20250709 / mingw-w64 a0e69f7） | 15.4 MB | 1 |
| `aidevbench-1.0.0-src-cmake-4.4.5-qt.tar` | CMake 4.4.5 と cmake-gui が静的結合する Qt（Windows: qtbase 6.10.1、Linux: 5.12.0） | 573.8 MB | 1 |
| `aidevbench-1.0.0-src-linux-ubuntu-24.04.tar` | Linux 版に同梱する Ubuntu 24.04 由来ファイルの source パッケージ（.dsc／orig／debian） | 701.8 MB | 1 |
| `aidevbench-1.0.0-src-linux-debian-12-libs.tar` | Linux 版 Chromium が使う Debian 12 ライブラリーの source パッケージ | 63.2 MB | 1 |
| `aidevbench-1.0.0-src-linux-debian-12-chromium-156.0.8078.73.tar` | Linux 版 Chromium（Debian 12、156.0.8078.73-1~deb12u1）の source パッケージ | 819.9 MB | 1 |
| `aidevbench-1.0.0-src-linux-git-2.56.0.tar` | Linux 版 git 2.56.0 の元 tarball とビルド手順・記録 | 8.5 MB | 1 |
| `aidevbench-1.0.0-src-linux-bun-1.4.4.tar` | Bun 1.4.4（Linux・macOS 共通）のソース、固定 commit の WebKit（JavaScriptCore 部分）、TinyCC | 109.6 MB | 1 |
| `aidevbench-1.0.0-src-macos-gnu-tools.tar` | macOS 版でソースから作る GNU Bash 5.2.21（パッチ001〜021）、coreutils 9.4（posixtm.c の修正つき）、sed 4.9、git 2.56.0、liblzma（xz 5.8.1）と、ビルド手順・記録 | 33.7 MB | 1 |
| `aidevbench-1.0.0-src-chromium-156.0.8076.0-r1705623.tar.xz` | Chromium スナップショット r1705623 のソース一式（分割）。Windows x64／ARM64 と macOS（Mac_Arm）は同じ revision | 2.56 GB | 2 |

SHA-256 は [SHA256SUMS](SHA256SUMS) と `manifest/release-assets.json`（各 tar の中のファイルごとの SHA-256 も記録）にあります。分割した資産は、番号順に連結すると元のファイルになります。

```sh
python3 scripts/verify_assets.py <ダウンロードしたフォルダー> --join --members
```

## 書面による申出 / Written offer

Yuha @ Yuhalab は、AI DevEnv Bench 1.0.0 を最後に配布した日から少なくとも3年間、これらの部品の完全な対応ソースを、求めに応じて、媒体と送付の実費を超えない費用で提供します。このリポジトリから取得できない場合は、[お問い合わせ](https://devbench.yuhalab.net/ja/contact)からご連絡ください。

## English

This repository publishes the corresponding source code of the third-party components that are redistributed in the AI DevEnv Bench 1.0.0 distribution ZIPs and whose licenses (GPL, LGPL, MPL and others) require the source to be made available. Sources of permissive components that come from the same origin are included for convenience. The archives are attached to the GitHub release `v1.0.0-sources`; [SOURCES.md](SOURCES.md) and `manifest/` map every redistributed file (path and SHA-256) to its component, version and source archive, and [RELINK.md](RELINK.md) explains how to modify, rebuild and relink. AI DevEnv Bench itself (the parts written by Yuha @ Yuhalab) is closed source and is not part of this repository; its license never restricts the rights the third-party licenses give you.

Written offer: for at least three years after the last distribution of AI DevEnv Bench 1.0.0, Yuha @ Yuhalab will give anyone who asks a complete machine-readable copy of the corresponding source listed here, for a charge no more than the cost of physically performing the distribution. Contact: https://devbench.yuhalab.net/en/contact
