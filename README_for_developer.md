# Usage for Developer
開発者用のドキュメントです。

# Release
GitHubのReleasesからリリースしてください。バージョンはSemantic Versioningに従います。
リリースすると、以下の状態になります。

* パッケージのバージョン情報は、https://github.com/ninoseki/uv-dynamic-versioning でGitHubのバージョンタグから生成されます。
* 自動でPyPIに公開されます。

## シークレット検査

`make gitleaks` で現在のブランチの Git 履歴を検査します。gitleaks をインストール済みならそのコマンドを使い、未インストールなら Docker で v8.30.1 を実行します。検出値はログでマスクします。CI でも同じ検査を実行します。

コミット前の差分検査には pre-commit フックを利用できます。

```sh
uv sync --locked
uv run pre-commit install
```
