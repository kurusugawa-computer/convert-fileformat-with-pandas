# Usage for Developer
開発者用のドキュメントです。

# Release
GitHubのReleasesからリリースしてください。バージョンはSemantic Versioningに従います。
リリースすると、以下の状態になります。

* パッケージのバージョン情報は、https://github.com/ninoseki/uv-dynamic-versioning でGitHubのバージョンタグから生成されます。
* 自動でPyPIに公開されます。

## シークレット検査

`make gitleaks` で現在のブランチの Git 履歴（マージ時の変更を含む）を検査します。gitleaks をインストール済みならそのコマンドを使い、未インストールなら Docker で v8.30.1 を実行します。検出値はログでマスクします。CI でも同じ検査を実行します。

DevContainer には gitleaks v8.30.1 を同梱しています。既存のコンテナは再ビルドしてください。

コミット前の差分検査には pre-commit フックを利用できます。

```sh
uv sync --locked
uv run pre-commit install
```

Docker の接続先・認証設定は、通常利用している設定を引き継ぎます。設定ディレクトリを明示的に切り替える場合のみ、`GITLEAKS_DOCKER_CONFIG=/tmp/gitleaks-docker-config make gitleaks` のように指定してください。
