# untranslated_items_tool

## インストール方法

1. Select_api.phpが/var/www/tripnscan/controllers/にあると確認
2. /var/www/tripnscan/config/routes.phpには、
 *      $route['select_api/find_changes'] = 'select_api/find_changes'があると確認
1. 上の点が反映してない場合は、kevin_api_shuuseiのブランチからマージ
2. このレポジトリを対象のサーバでclone
3. ファイルの設定を変更
 *      google_login.py:
 *          ８行目　gsheet = gs.open_by_key('1c5bIqiIz8A_bT595kr_vI9fN7U1dkFDnk6Q3uwl3Tb0')　のキーを "1mRU-3NgPgayN17x-sMnWRix3-C7NiiKjaMyDIgBtO40" に変更 (PRDの場合。新たなサーバの場合は空のファイルを用意してそのキーを取っても良い）
 *      slack_post.sh:
 *          １５行目　channel="G8G0U13UK" を投稿したいチャネル名及び、チャネルidに変更
 *      ２５行目　text1='The list of untranslated items for the STG environment has been updated.'の'STG'を正しいサーバ名に変更
 *          ２７行目　linkのキーをgoogle_login.pyの８行目で使った同じキーを入れ替え
1. サーバ上でcrontab -e でcron一覧を開いて
 *   '59 23 * * * /home/ec2-user/untranslated_items_tool/update_untranslated_log.sh' を追記
 *      毎日 23:59にこのuntranslated items toolを実行して、と言う意味。

## テスト方法

1. /home/ec2-user/untranslated_items_tool/update_untranslated_log.shを実行
2. /var/www/tripnscan/batch_logs/untranslated_items.jsonが制作されたと確認
3. 利用したキーのgoogle spreadsheetファイルを開いて、埋まったと確認
4. このレポジトリの「get_untranslated_items」クエリをDBで実装
 *   ３、４の結果の内容が完全一致してると確認
