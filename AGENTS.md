# AGENTS.md

## プロジェクト概要

このリポジトリは、Ryohei Tanaka による ComfyUI 向けカスタムノード集です。

## 開発ガイドライン

- ノードは小さく、目的を絞って実装する。
- 失敗を黙って無視せず、分かりやすいエラーメッセージを出す。
- ComfyUI カスタムノードの慣例に従う。
  - `INPUT_TYPES`
  - `RETURN_TYPES`
  - `RETURN_NAMES`
  - `FUNCTION`
  - `CATEGORY`
- ノード登録は `NODE_CLASS_MAPPINGS` と `NODE_DISPLAY_NAME_MAPPINGS` で行う。
- 絶対パスをハードコードしない。
- ファイル保存時は ComfyUI の出力ディレクトリを `folder_paths.get_output_directory()` で取得する。
- 新しいノードを追加した場合は README を更新する。

## テストチェックリスト

- ComfyUI 起動時に import error が出ないこと。
- ノードが正しいカテゴリに表示されること。
- WAV 書き出しが動作すること。
- OGG 書き出しが動作する、または ffmpeg 不足時に分かりやすいエラーが出ること。
- MP3 書き出しが動作する、または ffmpeg 不足時に分かりやすいエラーが出ること。
- すべての保存形式を無効にした場合、分かりやすいバリデーションエラーが出ること。
