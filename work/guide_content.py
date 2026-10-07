"""Source content for the Japanese ECS/Fargate health-check design guide."""
from __future__ import annotations

DATE = "2026-10-07"
TITLE = "ECS Fargate ヘルスチェック・起動依存関係 設計ガイド"
SUBTITLE = "UBI / OpenJDK 21 / JBoss EAP 8.1 · フロント / バック / ADOT / CloudWatch Agent"

SOURCES = [
    ("S01", "AWS ECS HealthCheck API", "https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_HealthCheck.html", "startPeriod・interval・timeout・retriesの範囲、早期成功、終了コード"),
    ("S02", "AWS ECS コンテナヘルスチェック", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/healthcheck.html", "essentialとタスク健康状態、イメージ内コマンドの要件"),
    ("S03", "AWS ECS ContainerDefinition API", "https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerDefinition.html", "startTimeoutの指定先、Fargate 2–120秒、essential、stopTimeout"),
    ("S04", "AWS ECS ContainerDependency API", "https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerDependency.html", "START / HEALTHY / COMPLETE / SUCCESS、起動時のみの判定"),
    ("S05", "AWS ECS UpdateService API", "https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_UpdateService.html", "サービス猶予の意味、0–2147483647秒、更新時の挙動・例外"),
    ("S06", "AWS ECS Task API", "https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Task.html", "task.startedAtはRUNNINGへの遷移時刻"),
    ("S07", "AWS ECS タスクのライフサイクル", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-lifecycle-explanation.html", "PROVISIONING / PENDING / ACTIVATING / RUNNING"),
    ("S08", "AWS ALB ターゲットのヘルスチェック", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html", "ALBの検査・各設定範囲・HTTP成功コード・状態"),
    ("S09", "AWS ECS ロードバランサーヘルスチェックの最適化", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-healthcheck.html", "初回登録は成功1回、異常からの復帰はHealthyThresholdCount"),
    ("S10", "AWS ELB CreateTargetGroup API", "https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_CreateTargetGroup.html", "ALBターゲットグループのAPI定義・IPターゲット"),
    ("S11", "AWS ALB ターゲットグループ属性", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html", "slow start・登録解除遅延・fail open"),
    ("S12", "AWS Fargate タスク定義パラメータ", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html", "Fargate制約・コンテナ依存・タイムアウト"),
    ("S13", "AWS Fargate タスクネットワーク", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html", "同一タスクのlocalhost通信・ENI・target type ip"),
    ("S14", "AWS ECS タスクメタデータV4", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-metadata-endpoint-v4-response.html", "各コンテナのStartedAtを取得する方法"),
    ("S15", "ADOT 公式Dockerfile", "https://github.com/aws-observability/aws-otel-collector/blob/main/cmd/awscollector/Dockerfile", "scratchベース・/healthcheck同梱の確認"),
    ("S16", "ADOT 公式healthcheck実装", "https://github.com/aws-observability/aws-otel-collector/blob/main/cmd/healthcheck/main.go", "127.0.0.1:13133/へのHTTP検査、200判定、-port"),
    ("S17", "OpenTelemetry Health Check Extension", "https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/extension/healthcheckextension/README.md", "health_checkの有効化・既定エンドポイント・パイプライン検査の制約"),
    ("S18", "OpenTelemetry Collector resiliency", "https://opentelemetry.io/docs/collector/resiliency/", "送信キュー・再試行・永続化・データ欠損条件"),
    ("S19", "CloudWatch Agent 公式Dockerfile", "https://github.com/aws/amazon-cloudwatch-agent/blob/main/amazon-cloudwatch-container-insights/cloudwatch-agent-dockerfile/Dockerfile", "scratchベース・シェルとpgrepを当然視できない"),
    ("S20", "AWS CloudWatch Application Signals ECS sidecar", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Signals-ECS-Sidecar.html", "CloudWatch Agentの用途別構成、4316の送信先例"),
    ("S21", "AWS ECS コンテナ再起動ポリシー", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-restart-policy.html", "essential / non-essentialの再起動、既定は無効"),
    ("S22", "AWS ECS ContainerRestartPolicy API", "https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerRestartPolicy.html", "restartAttemptPeriod 60–1800秒・既定300秒"),
    ("S23", "AWS ECS デプロイサーキットブレーカー", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html", "起動失敗と健康状態によるデプロイ失敗検出"),
    ("S24", "AWS ECS サービス定義パラメータ", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service_definition_parameters.html", "健康なタスクの数え方・minimumHealthyPercent / maximumPercent"),
    ("S25", "Red Hat EAP 8.1 ソケットバインディング", "https://docs.redhat.com/ja/documentation/red_hat_jboss_enterprise_application_platform/8.1/html/configuration_guide/assembly-about-socket-bindings_default", "port-offsetとHTTP / 管理ポートの分離"),
    ("S26", "Red Hat EAP 8.1 / XP 6.0 MicroProfile Health", "https://docs.redhat.com/en/documentation/red_hat_jboss_enterprise_application_platform/8.1/html-single/using_jboss_eap_xp_6.0/using_jboss_eap_xp_6.0", "SmallRye Health・standalone・管理HTTP・readiness"),
    ("S27", "Red Hat EAP 8.1 OpenShift image health", "https://docs.redhat.com/en/documentation/red_hat_jboss_enterprise_application_platform/8.1/html/using_jboss_eap_on_openshift_container_platform/assembly_reference-information-for-openshift-container-platform_default", "サーバー状態・ブートエラー・デプロイ状態と健康判定"),
    ("S28", "Red Hat EAP 8.1 サポート構成", "https://docs.redhat.com/en/documentation/red_hat_jboss_enterprise_application_platform/8.1/html/release_notes_for_red_hat_jboss_enterprise_application_platform_8.1/supported-configurations-rn_assembly-release-notes", "OpenJDK 21 / RHEL 9のイメージ構成。利用環境の認定とは区別"),
    ("S29", "AWS 2017年 ELB health check grace period", "https://aws.amazon.com/jp/about-aws/whats-new/2017/12/amazon-ecs-adds-elb-health-check-grace-period/", "2017-12-27、起動途中の早すぎる停止を抑える背景"),
    ("S30", "AWS 2018年 container health checks", "https://aws.amazon.com/pt/about-aws/whats-new/2018/03/amazon-ecs-supports-container-health-checks-and-task-health-mana/", "2018-03-08、コンテナ内部の健康監視を追加"),
    ("S31", "AWS Fargate platform 1.1.0", "https://aws.amazon.com/about-aws/whats-new/2018/03/aws-fargate-platform-version-1-1/", "2018-03-26、Fargateでコンテナヘルスチェック対応"),
    ("S32", "AWS 2019年 enhanced container dependency", "https://aws.amazon.com/about-aws/whats-new/2019/03/amazon-ecs-introduces-enhanced-container-dependency-management/", "2019-03-07、テレメトリサイドカー・初期化コンテナの順序制御"),
    ("S33", "AWS ECS ドキュメント履歴", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/document_history.html", "2019-03-27 Fargate依存制御、2024-08-15 restart policy"),
    ("S34", "Dockerfile HEALTHCHECK reference", "https://docs.docker.com/reference/dockerfile/#healthcheck", "start-periodとstart-interval、DockerとECS APIの違い"),
    ("S35", "HashiCorp AWS ECS service resource", "https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/ecs_service.html.markdown", "health_check_grace_period_secondsなどTerraform名"),
    ("S36", "HashiCorp AWS LB target group resource", "https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/lb_target_group.html.markdown", "health_checkブロック・閾値・属性"),
    ("S37", "AWS ECS Agent dependency graph（参考実装）", "https://github.com/aws/amazon-ecs-agent/blob/master/agent/engine/dependencygraph/graph.go", "依存先StartedAtとstartTimeoutの関係。Fargate内部実装の保証ではない"),
]

SECTIONS = []

def section(sheet, title, intro=""):
    item = {"sheet": sheet, "title": title, "intro": intro, "blocks": []}
    SECTIONS.append(item)
    return item

def p(s, heading, text, refs=""):
    s["blocks"].append({"type": "prose", "heading": heading, "text": text, "refs": refs})

def table(s, heading, headers, rows, widths=None, refs=""):
    s["blocks"].append({"type": "table", "heading": heading, "headers": headers, "rows": rows, "widths": widths, "refs": refs})

def code(s, heading, text, language="text", refs=""):
    s["blocks"].append({"type": "code", "heading": heading, "text": text.strip(), "language": language, "refs": refs})

s = section("00_結論と読み方", "最初に押さえる結論", "確認日：2026-10-07。AWS・Red Hat・OpenTelemetry等の一次情報を確認。数値例は測定値ではなく設計用の仮定です。")
p(s, "今回の条件", "実行環境はECS Fargate（Linux）。フロントとバックはUBI上のOpenJDK 21 / JBoss EAP 8.1として説明します。タスクにはADOT Collector（essential=true）とCloudWatch Agent（essential=false）も置きます。実際の起動時間・アプリの健康判定URL・イメージのタグ・CPU/メモリ量は未提示です。以下の秒数はAWS推奨の固定値ではなく、仮定に対して計算した候補です。")
table(s, "誤解しやすい点と正しい読み替え", ["論点", "正しい考え方", "実務上の結論"], [
    ["startPeriod=210", "そのコンテナの起動直後に失敗を数えない猶予。検査は実行され、途中の成功でHEALTHYになれる。", "210秒そのものを起動時間として足し算しない。"],
    ["ELB / ALBの猶予300秒", "実体はECSサービスのhealthCheckGracePeriodSeconds。ALBの検査開始を遅らせない。", "ALBが異常を報告しても、ECSの健康判定に基づく置換を猶予する。"],
    ["HEALTHY依存", "依存先の最初の健康判定成功を待つ。起動順序を制御する。", "依存先の実際の準備時間＋検査・通知の遅れを測る。"],
    ["Fargateの待機上限", "明示できるstartTimeoutは2–120秒。依存先側へ設定する。", "初回HEALTHYまで210秒かかるバックを120秒の依存待ちで待つ設計は成立しない。"],
    ["300秒の起点", "タスクの作成時刻、最初のコンテナ開始、task.startedAt、各コンテナStartedAtは別。", "task.startedAtを基準に残りの準備時間を評価し、実イベントでも突き合わせる。"],
    ["13133番が200", "Collectorのヘルスエンドポイントが成功したこと。全トレースの永続保存を証明しない。", "起動順に加え、SDK・Collectorの再試行、キュー、保存先での受信を確認する。"],
], [25, 68, 59], "S01 S03 S04 S05 S06 S16 S18")
p(s, "未計測の現時点での選び方", "まずはP4を検証候補とします。ADOTのHEALTHYを待って両方のEAPを並列に開始し、フロントとバックの間にはHEALTHY依存を置きません。startPeriodはADOT 30秒、CloudWatch Agent 30秒、バック210秒、フロント210秒、ECSサービス猶予300秒とする例です。ALBにはフロントからバックまで最低限使えることを判定するreadinessを設定します。バックがいない間もフロントが起動し続け、再接続できる実装が前提です。")
p(s, "希望どおり直列にする場合", "バックの『コンテナ開始→初回HEALTHY』が負荷の高い時も十分に120秒未満ならP1 / P2が候補です。例えばバックが95秒でHEALTHY、フロントの準備が200秒なら、フロントのstartPeriod=210とサービス猶予300を維持できる時間例を示します。バック自身が200秒以上かかるなら、サービス猶予を600へ変更するだけでは120秒の依存待ちの問題を解消できません。", "S03 S12")
p(s, "210秒を短くする効果", "210を60へ変更しても、アプリの初期化処理は速くなりません。変わるのは失敗を数え始める時刻です。準備完了を早く検知したい場合は、準備完了条件を正しく実装したうえでintervalを30秒から10秒などへ調整します。十分な余裕を持つ実測結果が出てからstartPeriodを縮めます。", "S01")
p(s, "読み進め方", "仕組みと時計→設定範囲→依存関係→パターン比較→起動時系列の順で読めます。Excelの『08_時間計算』は白い入力セルを書き換えると見積もりが変わります。JSON・Terraformは設定の位置を示すテンプレートです。AWSへの適用や実機負荷試験は行っていません。")

s = section("01_仕組みと時計", "お店の開店にたとえて理解する", "『動いている』『準備ができた』『お客さんを入れてよい』を分けると、各設定の役割が見えます。")
table(s, "登場人物", ["登場するもの", "小学生向けのたとえ", "実際の仕事"], [
    ["ECSサービス", "お店を決まった数だけ営業させる店長", "必要タスク数を保ち、起動失敗や健康状態に応じてタスクを入れ替える。"],
    ["Fargateタスク", "同じ建物で働く1チーム", "今回の4コンテナをひとまとめに実行する。"],
    ["フロントエンド", "注文を受ける受付", "利用者のHTTPリクエストを受け、必要に応じバックのAPIを呼ぶ。"],
    ["バックエンド", "注文どおりに調理する台所", "APIや業務処理を実行する。Javaプロセスが起動しただけでは調理可能とは限らない。"],
    ["ADOT Collector", "仕事の記録を受け取る係", "OTLPなどでトレースを受け取り、加工して保存先へ送る。"],
    ["CloudWatch Agent", "別の測定・記録係", "構成されたメトリクスやログ等を収集・送信する。ADOTと役割を決めて重複を防ぐ。"],
    ["ALB", "開いているお店へお客さんを案内する係", "ターゲットへHTTP健康確認を行い、状態に基づいてリクエストを振り分ける。"],
], [27, 46, 79])
table(s, "混同してはいけない4つの時計", ["時計", "起点・対象", "時間内でも行われること", "延ばしても解決しないこと"], [
    ["startPeriod", "各コンテナが開始してから。そのコンテナの失敗回数。", "ヘルスチェック、成功の判定、HEALTHYによる依存解除。", "初期化処理の遅さ、依存待ちの期限、プロセス終了。"],
    ["startTimeout", "依存先が条件を満たすまでの待ち。依存先コンテナへ指定。", "依存先の起動・検査。待つ側は未起動でよい。", "ALBの猶予、起動後の通信リトライ。Fargateに210や300は指定できない。"],
    ["healthCheckGracePeriodSeconds", "タスクが最初に開始した後のECSサービスの猶予。", "ALB・コンテナの健康確認、健康なターゲットへの配信。", "HEALTHY依存の失敗、OOM、必須コンテナ終了、誤ったURL。"],
    ["ALB interval / timeout / thresholds", "登録済みターゲットに対する周期的なHTTP検査。", "HTTP GETと成功・失敗の判定。猶予中も続く。", "ECSがコンテナを開始する順番、Javaの初期化時間。"],
], [30, 48, 43, 56], "S01 S03 S05 S08")
p(s, "startPeriodの動作イメージ", "startPeriod=210、interval=10、retries=3とします。仮に10・20・30秒の検査が失敗しても、初回成功前の猶予内なので失敗回数には入れません。40秒で成功すれば、その時点でHEALTHYです。以後50・60・70秒に連続して失敗すると、210秒を待たずUNHEALTHYになり得ます。この例の検査時刻は説明用です。実際は検査実行時間・ランタイム・通知の遅れがあります。", "S01 S34")
p(s, "失敗し続けた場合", "初回成功がないまま210秒を過ぎれば、その後の失敗が回数に入ります。仮に220・230・240秒で失敗したら240秒付近でUNHEALTHYです。『必ず210＋10×3=240秒で停止』ではありません。コンテナの状態変化と、ECSサービスが置換を判断する時刻と、停止完了時刻は別です。サービスの猶予中なら健康異常による置換が抑えられる場合があります。", "S01 S05")
p(s, "ECSの猶予中もALBは働く", "ALBが50秒で失敗し、180秒で成功を確認することもあります。ECSの猶予が300秒でも、正常と判定されれば300秒を待たず配信できます。猶予終了時に失敗回数がゼロへ戻るわけでもありません。300秒時点ですでにUNHEALTHYなら、その状態に対してサービスが置換を判断できます。", "S05 S08 S09")
p(s, "タスク開始時刻の落とし穴", "起動要求を出した時刻やcreatedAtから、機械的に300秒を引かないでください。APIのtask.startedAtはRUNNINGに遷移した時刻です。依存先を待っている間はタスクが起動処理中であり、その時間がstartedAtより前に位置することがあります。資料の時系列は『最初のコンテナ開始をt=0』として、task.startedAtの仮定を別列に示します。猶予の期限はtask.startedAt＋Gを基準にイベントと照合します。", "S05 S06 S07 S14")
code(s, "起動の概念図", """
起動要求 → リソース準備・イメージ取得 → コンテナ作成・依存待ち → RUNNING
                               ADOT開始 → HEALTHY
                                            バック開始 → HEALTHY
                                                           フロント開始 → 準備完了
                                                           ↑ startedAtは実測で確認
ALB: ターゲット登録と必要条件成立後、独立して周期検査 ───────────→
ECS: task.startedAtからG秒、健康異常による早期置換を猶予 ─────────→
""", refs="S06 S07 S08")

s = section("02_設定値の範囲", "どこに何を指定できるか", "単位は特記しない限り秒。以下の範囲はECS Fargate LinuxとALBのHTTPターゲットを中心に整理しています。")
table(s, "ECSタスク定義のコンテナ項目", ["JSON名 / 指定場所", "実際に指定できる値", "省略時", "今回の候補・意味"], [
    ["healthCheck.command", '配列の先頭CMDまたはCMD-SHELL。終了0が成功、非0が失敗。', "健康チェックを定義しない場合は監視対象外", "HTTP検査や専用バイナリ。ツールをイメージへ同梱する。"],
    ["healthCheck.interval", "整数5–300", "30", "ADOT 5、EAP 10、CloudWatch Agent 30。成功を拾う速さと負荷の交換条件。"],
    ["healthCheck.timeout", "整数2–60", "5", "ADOT 2、EAP 5、CloudWatch Agent 5。1回の実行上限。"],
    ["healthCheck.retries", "整数1–10", "3", "通常3。P7のフロントは6とするが、稼働中の検知も遅くなる。"],
    ["healthCheck.startPeriod", "整数0–300", "無効（0相当）", "ADOT 30、CloudWatch Agent 30、EAP 60 / 90 / 100 / 210 / 270 / 300など。"],
    ["dependsOn", "同一タスク内のcontainerNameとconditionの配列", "明示的な依存なし", "APIではdependsOn。循環依存を作らない。複数条件はすべて満たす必要がある。"],
    ["dependsOn[].condition", "START / COMPLETE / SUCCESS / HEALTHY", "依存を作る場合は必須", "APIの綴りは大文字。HEALTHYはタスク定義のコンテナhealthCheckを使う。"],
    ["essential", "true / false", "true", "ADOT・バック・フロント=true、CloudWatch Agent=false。少なくとも1つtrueが必要。"],
    ["startTimeout", "Fargate：整数2–120", "参照APIに一律の既定秒数の明記なし", "待たれるADOT / バックに120を明示。省略を120秒超の保証として利用しない。"],
    ["stopTimeout", "Fargate：整数2–120", "30", "EAP 60、ADOT 60、CloudWatch Agent 30を検証例にする。起動猶予ではない。"],
    ["restartPolicy.enabled", "true / false", "再起動ポリシーは無効", "本例の必須コンテナは無効。CloudWatch Agentの再起動は別途選択する。"],
    ["restartPolicy.restartAttemptPeriod", "整数60–1800", "300", "任意例60。毎回60秒待てば必ず再起動するという意味ではない。"],
], [43, 48, 35, 68], "S01 S03 S04 S12 S21 S22")
table(s, "ECSサービスとALBターゲットグループ", ["場所 / JSON・API名", "許容値 / 省略時", "設定例", "読み方"], [
    ["ECS service: healthCheckGracePeriodSeconds", "0–2147483647 / 0", "150 / 300 / 420 / 450", "健康異常による早期置換の猶予。ALBを止める値ではない。"],
    ["ALB: HealthCheckProtocol", "HTTP / HTTPS / HTTP", "HTTP", "主例はALBでHTTPS終端、ターゲットへHTTP。暗号化要件によってHTTPSを選ぶ。"],
    ["ALB: HealthCheckPort", "traffic-portまたはポート1–65535", "traffic-port（8080）", "実トラフィックと同じフロントポートを確認する。"],
    ["ALB: HealthCheckPath", "HTTPパス / /", "/app/health/ready", "この資料のアプリ実装例。EAP既定URLではない。"],
    ["ALB: HealthCheckIntervalSeconds", "整数5–300 / IPターゲットは30", "10", "間隔。長くすると開始を遅らせるのではなく、成功も故障も検知しにくくなる。"],
    ["ALB: HealthCheckTimeoutSeconds", "整数2–120 / IPターゲットは5", "5", "1回のHTTP応答待ち。intervalより小さくする設計例。"],
    ["ALB: HealthyThresholdCount", "整数2–10 / 5", "2", "一度異常になったターゲットが正常へ戻るための連続成功回数。"],
    ["ALB: UnhealthyThresholdCount", "整数2–10 / 2", "3", "連続失敗による異常判定。通常の故障検知の遅れも評価する。"],
    ["ALB: Matcher.HttpCode", "HTTPでは200–499のコード・集合・範囲 / 200", "200", "認証画面・404・リダイレクトを誤って成功扱いしない。"],
    ["TargetType", "Fargate awsvpcではip", "ip", "instanceは今回の構成に使わない。"],
    ["slow_start.duration_seconds", "0（無効）または30–900 / 0", "0。必要なら60を負荷試験", "正常になった後にトラフィック割合を徐々に増やす機能。検査開始猶予ではない。"],
    ["deregistration_delay.timeout_seconds", "0–3600 / 300", "初期は300を維持", "停止時の接続処理。長いリクエストを確認してから短縮する。"],
], [48, 48, 30, 67], "S05 S08 S10 S11 S13")
p(s, "他のシステムからコピーしない項目", "KubernetesのinitialDelaySeconds / startupProbe / readinessProbe / livenessProbeは、ECSタスク定義の項目ではありません。ECSにはコンテナごとに1つのhealthCheckがあり、ALBの検査と組み合わせます。Dockerのstart_interval / --start-intervalも、この確認時点のECS HealthCheck APIには公開されていません。Dockerのtimeout既定値をECSへ持ち込まないでください。", "S01 S34")
table(s, "同じ意味でも設定ファイルによって綴りが違う", ["意味", "ECS API / JSON", "CloudFormation", "Terraform"], [
    ["起動失敗の猶予", "healthCheck.startPeriod", "HealthCheck.StartPeriod", "container_definitions内はstartPeriod"],
    ["起動順の依存", "dependsOn", "ContainerDefinitions内のDependsOn", "container_definitions内はdependsOn"],
    ["サービスの猶予", "healthCheckGracePeriodSeconds", "HealthCheckGracePeriodSeconds", "health_check_grace_period_seconds"],
    ["ALBの検査間隔", "HealthCheckIntervalSeconds", "HealthCheckIntervalSeconds", "health_check { interval = 10 }"],
    ["リソースを作る順番", "コンテナ依存とは別", "リソース直下のDependsOn", "リソースのdepends_on"],
], [28, 48, 48, 51], "S01 S03 S05 S35 S36")

s = section("03_依存とessential", "dependsOnとessentialの正確な役割", "バックがADOTを待ち、フロントがバックを待つという希望の構成は、各依存先の準備時間が期限内なら利用できます。")
code(s, "希望の構成と停止順", """
起動：ADOT ──HEALTHY──> バック ──HEALTHY──> フロント
      CloudWatch Agent ─────────────────────> 独立して起動

停止：フロント → バック → ADOT（依存関係の逆向き）
      CloudWatch Agentの順序は明示していない

backend.dependsOn = [{containerName: "adot", condition: "HEALTHY"}]
frontend.dependsOn = [{containerName: "backend", condition: "HEALTHY"}]
adot.startTimeout = 120
backend.startTimeout = 120
""", refs="S03 S04")
table(s, "conditionの使い分け", ["値", "待つ状態", "適した用途", "今回の注意"], [
    ["START", "依存先のコンテナが開始した", "順番だけを決め、アプリ側が接続失敗を再試行できる場合", "JVM開始・EAPデプロイ完了・API準備完了は別。"],
    ["HEALTHY", "依存先のコンテナヘルスチェックが成功した", "Collector受信準備や、短時間で準備できるAPIを待つ", "起動時のみ評価。後から不健康になっても起動済みフロントを順番待ちへ戻さない。"],
    ["COMPLETE", "依存先が終了した。終了コードは問わない", "終了する初期化処理", "待たれるコンテナはnon-essential。常駐ADOTやEAPには不適切。"],
    ["SUCCESS", "依存先が終了コード0で終了した", "設定ファイル生成などの成功を待つ", "待たれるコンテナはnon-essential。常駐サービスの準備待ちと混同しない。"],
], [20, 44, 54, 66], "S04")
p(s, "startTimeoutは待たれる側へ", "frontendがbackendのHEALTHYを待つときは、backend側のstartTimeout=120が関係します。frontendにだけ120を置いても、backendに210秒の準備時間を与えることにはなりません。公式APIのcontainerA / containerB例に合わせた説明です。ADOTの準備時間とバックの準備時間にはそれぞれの期限があり、2段だから1つの120秒を合計で分け合うという説明も適切ではありません。", "S03 S12")
p(s, "120秒ぎりぎりを目標にしない", "準備完了ログが115秒でも、次の検査が10秒後なら初回HEALTHYの通知は120秒を超え得ます。依存先の起動から実際にHEALTHYが観測されるまでを測り、例えば最大側の実測95秒＋25秒の余裕として120を設計します。省略時の内部挙動や公開Agentの実装から、Fargateで無期限に待てると断定しません。", "S03 S37")
table(s, "essentialと停止・健康状態", ["条件", "本資料の前提で起こること", "設計判断"], [
    ["ADOT=trueが終了", "再起動ポリシー無効の例では、タスクの他コンテナも停止対象になる。", "観測基盤の停止をアプリ継続より重く扱う、という可用性上の選択。"],
    ["バック / フロント=trueが終了", "同じくタスク全体の停止につながる。サービスが必要数を補充する。", "startPeriodやサービス猶予で終了そのものを無効にはできない。"],
    ["必須コンテナのhealthCheckがUNHEALTHY", "タスク健康状態はUNHEALTHY。サービスの猶予等を踏まえ置換が判断される。", "プロセス終了とhealthCheck失敗は別経路。"],
    ["CloudWatch Agent=falseが終了", "その終了だけでは他コンテナを止めない。", "監視が止まった状態でアプリが動き続けるので、送信途絶の検知を別途持つ。"],
    ["CloudWatch Agent=falseがUNHEALTHY", "そのhealthCheckはタスク全体のhealthStatus集計に含まれない。", "非必須だから自動復旧する、とは限らない。"],
    ["必須・検査ありコンテナにUNKNOWNが残る", "UNHEALTHYがなければ、タスク健康状態はUNKNOWNになる。", "検査なしコンテナを含めて全員HEALTHYが必要と誤解しない。"],
], [44, 72, 62], "S02 S03 S21")
p(s, "起動後の故障は別に設計する", "HEALTHY依存は『最初に開店する順番』です。バックが後で止まったとき、フロントの既存接続の再接続、失敗したHTTP呼出しの扱い、ALBのready判定を代わりに実装してくれる機能ではありません。ADOTのhealthCheckを通過しても、その直後の障害・キューあふれ・保存先エラーは起こり得ます。", "S04 S18")

# Timing inputs are deliberately explicit. Detection allowances are illustrative.
PATTERNS = [
    dict(id="P0", name="現在形・全コンテナ並列", mode="parallel_all", a=20, b=200, f=200, da=5, db=10, df=10, sp=(30,210,210,30), grace=300, margin=60, task=0, native_b=False, status="条件付き成立", graph="依存なし", note="起動時トレースの送信先未準備と、フロントのバック未接続をアプリ側で扱う必要があります。"),
    dict(id="P1", name="希望の直列・短い起動", mode="serial", a=15, b=70, f=50, da=5, db=10, df=10, sp=(30,90,60,30), grace=150, margin=45, task=100, native_b=True, status="成立例", graph="ADOT HEALTHY → バック HEALTHY → フロント", note="バック初回HEALTHY=80秒で120秒以内。サービス猶予300の維持も可能ですが、150まで短くする候補を示します。"),
    dict(id="P2", name="希望の直列・フロントだけ遅い", mode="serial", a=20, b=85, f=200, da=5, db=10, df=10, sp=(30,100,210,30), grace=300, margin=60, task=120, native_b=True, status="成立例", graph="ADOT HEALTHY → バック HEALTHY → フロント", note="バックは95秒で依存条件成立。フロント自身は200秒かかっても、誰もフロントのHEALTHYを依存待ちしないので同じ120秒制約はかかりません。"),
    dict(id="P3", name="反例・バックの準備が200秒", mode="serial", a=20, b=200, f=200, da=5, db=10, df=10, sp=(30,210,210,30), grace=600, margin=60, task=None, native_b=True, status="依存期限超過", graph="ADOT HEALTHY → バック HEALTHY → フロント", note="バックstartTimeout=120では、バック開始の約120秒後に依存解決失敗。600秒の猶予を設定してもフロント起動を救済できません。"),
    dict(id="P4", name="推奨候補・ADOTの後にEAP並列", mode="parallel_adot", a=20, b=200, f=200, da=5, db=10, df=10, sp=(30,210,210,30), grace=300, margin=60, task=25, native_b=False, status="未計測時の検証候補", graph="ADOT HEALTHY → バック / フロント並列", note="バックとフロントの間にHEALTHY依存を置かず、ALBのフロントreadinessでバック利用可能性を確認します。"),
    dict(id="P5", name="STARTだけで順番を付ける", mode="start", a=20, b=200, f=200, da=5, db=10, df=10, sp=(30,210,210,30), grace=300, margin=60, task=30, native_b=False, status="アプリの再試行が前提", graph="ADOT HEALTHY → バック START → フロント", note="STARTの解除からフロント開始まで5秒と仮定。API準備を待たないため、起動中の接続拒否を許容しないアプリには使えません。"),
    dict(id="P6", name="遅い起動の裾・並列で猶予拡張", mode="parallel_adot", a=20, b=290, f=250, da=5, db=10, df=10, sp=(30,300,270,30), grace=420, margin=90, task=25, native_b=False, status="長い起動を実測した場合", graph="ADOT HEALTHY → バック / フロント並列", note="バックのstartPeriodは上限300。初回HEALTHYが300秒を超える裾がある場合はさらにアプリ起動処理・故障検出方針を見直します。"),
    dict(id="P7", name="長いバック待ちをアプリ起動制御へ", mode="wrapper", a=20, b=200, f=150, da=5, db=10, df=15, sp=(30,210,300,30), grace=450, margin=60, task=25, native_b=False, status="特別な実装が必要", graph="ADOT HEALTHY → 両コンテナ開始 / フロントJVMはバックを待つ", note="フロントのコンテナは先にRUNNING。内部ラッパーが5秒周期で最大300秒バックを待ってからJVMを開始します。ネイティブのコンテナ起動順とは別です。"),
]

def timing(z):
    ha=z["a"]+z["da"]; hb=z["b"]+z["db"]; hf=z["f"]+z["df"]
    bs=0 if z["mode"]=="parallel_all" else ha
    fs=(bs+hb if z["mode"]=="serial" else bs+5 if z["mode"]=="start" else bs)
    jvm=bs+z["b"]+5 if z["mode"]=="wrapper" else fs
    ah=ha; bh=bs+hb; fh=jvm+hf
    app=max(bs+z["b"],jvm+z["f"])
    alb=app+10*2+2  # Recovery example: 2 successes, 10s interval, 2s response allowance.
    end=max(ah,bh,fh,alb)
    need=None if z["task"] is None else max(0,end-z["task"])+z["margin"]
    return dict(ha=ha,hb=hb,hf=hf,bs=bs,fs=fs,jvm=jvm,ah=ah,bh=bh,fh=fh,app=app,alb=alb,end=end,need=need)

s = section("04_パターン比較", "時間パターン別の具体案", "全例でCloudWatch Agentは依存なし・essential=false、他3コンテナはessential=true。起動秒数は負荷試験で置き換える仮定です。")
table(s, "まず選ぶための比較", ["ID / 構成", "仮定の実準備時間\nADOT / バック / フロント", "startPeriod\n同順＋CW Agent", "サービス猶予G", "採用判断"], [
    [f'{z["id"]} {z["name"]}', f'{z["a"]} / {z["b"]} / {z["f"]} 秒', ' / '.join(map(str,z['sp']))+' 秒', z['grace'], z['status']] for z in PATTERNS
], [48, 32, 34, 22, 43])
p(s, "全パターン共通のALB設定例", "HTTP、traffic-port=8080、path=/app/health/ready、成功200、interval=10、timeout=5、HealthyThresholdCount=2、UnhealthyThresholdCount=3とします。P3は比較用の失敗例で、この設定を付けても依存の問題は直りません。現在のALB値が不明なため、既存値からの無条件な変更指示ではありません。検査負荷と障害時の切り離し速度を評価するための具体的な出発点です。", "S08 S09")
for z in PATTERNS:
    t=timing(z)
    p(s, f'{z["id"]}：{z["name"]}', z['graph']+'。'+z['note'])
    if z['id']=='P3':
        p(s, "P3で起こること", "ADOTはt=25でHEALTHY、バックはt=25で開始。バックの初回HEALTHYは仮にt=235ですが、明示した120秒の依存期限はt=145付近です。したがってフロントは開始できません。『t=300でバックが健康になり、そこからフロント開始』という時系列を、このタイムアウト構成の正常動作として描くことはできません。停止の実時刻には検知・制御の遅れがあります。")
    else:
        p(s, f'{z["id"]}の見積もり', f'最初のコンテナ開始をt=0とすると、バック開始t={t["bs"]}、フロントコンテナ開始t={t["fs"]}、フロントJVM開始t={t["jvm"]}です。全体準備完了はt={t["end"]}を見込み、task.startedAtをt={z["task"]}と仮定すると、残り{t["end"]-z["task"]}秒＋余裕{z["margin"]}秒={t["need"]}秒。候補G={z["grace"]}秒はこの見積もりを上回ります。実際のstartedAtが異なる場合は再計算します。')
p(s, "P1のstartPeriodを210のまま残す選択", "P1のバック90・フロント60を両方210にしても、最初の成功時刻が同じなら依存解除は同じです。短縮は必須ではありません。起動の裾をまだ十分に測っていない段階では210を維持し、誤検知防止と恒久故障の検出遅延を確認する進め方も取れます。")
p(s, "P2が示す大事な点", "最初のコンテナ開始から300秒を過ぎても、フロントが準備中だから直ちに猶予超過とは限りません。本例ではフロントコンテナ開始とtask.startedAtをt=120と仮定するので、G=300の期限はt=420です。t=342のALB復帰見積もりは間に合います。これを実環境でも成立と判断するには、startedAtとALBのイベントを測定します。")
p(s, "P7を採る場合の追加責任", "ラッパーは固定sleepではなく、バックの準備完了を短いタイムアウト付きで確認し、上限を超えたら明確な理由で終了します。シグナルを扱い、最後はexecでEAP起動へ引き継ぎます。フロントのstartPeriodはコンテナ開始から数えるので、待機200秒＋EAP初期化150秒という合計を評価します。例ではstartPeriod=300、interval=15、retries=6で残りの失敗を許容します。稼働後の故障検知も約90秒規模へ遅くなる代償があります。")
p(s, "P8：独立サービスへ分ける比較案", "さらに起動時間が長い、独立して拡縮したい、バック故障でフロントまで巻き込みたくない場合は、サービスを分ける設計もあります。各サービスに自分のADOT等を付け、アプリstartPeriod=210、ADOT/CW Agent=30、各サービスG=300を検証例とします。これは同じ4コンテナタスクではなく構成変更です。タスク間にはdependsOnを置けず、バックのサービス探索・再接続・認可・ネットワーク・先行デプロイを設計します。今回の第一選択として強制する案ではありません。")

s = section("05_コンテナ設定", "4コンテナに入れる具体値", "S=startPeriod、I=interval、T=timeout、R=retries。startTimeoutは待たれる側に明示。P3は依存期限超過の反例で、採用しない設定です。")
CONFIG_ROWS=[]
for z in PATTERNS:
    for idx,name in enumerate(['adot','backend','frontend','cwagent']):
        dep='なし'; st='省略'; interval=5 if idx==0 else 30 if idx==3 else 10
        retries=6 if z['id']=='P7' and idx==2 else 3
        if z['id']=='P7' and idx==2: interval=15
        if z['mode']!='parallel_all':
            if idx==0: st=120
            if idx==1: dep='adot : HEALTHY'
            if idx==2:
                dep='backend : HEALTHY' if z['mode']=='serial' else 'backend : START' if z['mode']=='start' else 'adot : HEALTHY'
            if idx==1 and z['native_b']: st=120
        CONFIG_ROWS.append([z['id'],name,'false' if idx==3 else 'true',z['sp'][idx],interval,2 if idx==0 else 5,retries,st,dep])
table(s, "パターン別・コンテナ別一覧", ['案','コンテナ','essential','S 秒','I 秒','T 秒','R 回','startTimeout 秒','dependsOn'], CONFIG_ROWS, [8,20,14,10,10,10,10,23,33])
p(s, "検査先の前提", "ADOTはhttp://127.0.0.1:13133/。バックはhttp://127.0.0.1:8180/app/health/ready。フロントのコンテナ検査はhttp://127.0.0.1:8080/app/health/ready-localとし、フロント自体の初期化完了を調べます。ALBの/app/health/readyはバックも利用可能かを調べます。/app/health/*はこの資料で提案するアプリ用URLであり、現状のアプリに存在すると確認したものではありません。")
p(s, "stopTimeoutとrestartPolicy", "停止順がある構成では、フロント・バック・ADOTのstopTimeout=60、CloudWatch Agent=30を例にします。ADOTにflush時間を確保する目的ですが、トレース損失ゼロを保証するものではありません。比較の基準を一定にするため、必須コンテナのrestartPolicyは省略（無効）とします。CloudWatch Agentの任意の再起動設定は別章で説明します。", "S03 S21")

s = section("06_ALBとサービス", "ALBの判定とECSの猶予を組み合わせる", "ALBは交通整理、ECSはタスクを維持する管理役です。同じヘルスチェック結果でも使い道が違います。")
table(s, "サービス側の候補", ["案", "G 秒", "startedAt仮定", "猶予期限の例", "補足"], [
    [z['id'],z['grace'],'未到達' if z['task'] is None else f't={z["task"]}', '依存失敗のため評価不可' if z['task'] is None else f't={z["task"]+z["grace"]}', z['status']] for z in PATTERNS
], [12,14,28,43,65])
p(s, "最初の1回と復帰時の2回", "新しく登録されたターゲットは、初回の正常化に成功1回でよいという例外があります。一度UNHEALTHYとなった後はHealthyThresholdCount分の連続成功が必要です。本資料は起動中に失敗して異常判定された状況も見込み、10秒間隔・2回成功の約20秒に応答の余裕2秒を加えた22秒を計算例に使います。必ず22秒で反映されるというAWSの時間保証ではありません。", "S09")
p(s, "300秒経過した瞬間の説明", "猶予終了時にALBが初めて検査を始めるわけではありません。ALBがすでに異常と判定していれば、その健康状態をECSが置換判断に使えるようになります。停止はスケジューラの処理を経るため、必ず300.000秒で起きるわけではありません。また猶予はdesiredCountを超えるタスクの整理など、すべての停止理由を防ぐ保証ではありません。", "S05")
p(s, "readinessを正しくしても配信を絶対に防ぐものではない", "通常は正常ターゲットへ送りますが、ALBには健康なターゲット不足時のfail openがあります。全ターゲット異常などの条件では異常ターゲットにも配信され得ます。古い正常タスクを残すローリング更新、必要台数、アプリが準備前に503を返す動作も合わせて考えます。startPeriodやGはエンドユーザーへの配信遮断スイッチではありません。", "S11")
p(s, "Javaのウォームアップとslow start", "『リクエストに正しく答えられる』と『大量のリクエストを速く処理できる』は別です。JITやキャッシュの準備が必要なら、正常判定後の負荷を段階的に増やすslow start=60秒などを試験できます。ただし既存の正常ターゲットがない場合など適用条件があり、slow start自体を起動中のヘルスチェック失敗の回避策にはしません。", "S11")
p(s, "猶予を長くする費用", "Gを300から600へ変えると、正常に起動する遅いタスクを救える場合がある一方、起動できない新タスクの失敗確定が遅れます。必要な余裕は確保し、いつまでも起動しない不具合を隠さない長さにします。intervalを長くする方法は、配信開始と稼働中の異常検知を同時に遅くするので、猶予の代用にしません。")

s = section("07_起動時系列", "時刻を並べて動きを見る", "t=0は最初のコンテナ開始。イメージ取得・ENI準備の所要時間は別です。実測ではない説明用の時系列です。")
TIMELINE_ROWS=[]
for z in PATTERNS:
    t=timing(z)
    if z['id']=='P3':
        events=[(0,'ADOT / CW Agent開始','バック・フロントはまだ開始しない'),(25,'ADOT HEALTHY、バック開始','バックの依存期限は開始から120秒'),(145,'バックの依存期限超過付近','フロントは開始できず、タスク停止へ。検知遅延は別'),(235,'バックHEALTHYの想定時刻','実際には停止により到達しない可能性。正常系の続きではない')]
    else:
        events=[(0,'ADOT / CW Agent開始','P0では両EAPも並列開始'),(t['ah'],'ADOT HEALTHY','依存があればEAPを開始可能'),(t['bs'],'バック開始',f'実準備{z["b"]}秒＋検知余裕{z["db"]}秒'),(t['fs'],'フロントコンテナ開始', 'P7は内部でバックを待つ' if z['mode']=='wrapper' else 'EAP/JVM開始の仮定'),(z['task'],'task.startedAtの仮定',f'G={z["grace"]}の時計の起点'),(t['bh'],'バックHEALTHY','startPeriod終了を待たず成功可'),(t['jvm'],'フロントJVM開始','P7以外はコンテナ開始時と同じ仮定'),(t['fh'],'フロントのローカル検査成功','バック連動のALB検査とは分ける'),(t['app'],'フロント経由で必要APIが利用可能','ALBの次の成功判定を待つ'),(t['alb'],'ALB復帰の見積もり','10秒×2回＋応答余裕2秒を上乗せ'),(z['task']+z['grace'],'ECSサービス猶予終了の例','終了前にもALBの検査と配信は行われる')]
    for time,event,meaning in sorted(events,key=lambda e:e[0]): TIMELINE_ROWS.append([z['id'],time,event,meaning])
table(s,'全パターンのイベント一覧',['案','相対時刻 秒','イベント','そのときの意味'],TIMELINE_ROWS,[10,20,59,84])
p(s, "ユーザーの想定を読み替える", "『300秒時点でバックOK→フロント開始→ALBが初検査して失敗』ではなく、①バックのHEALTHYが依存期限内か、②フロント開始とtask.startedAtはいつか、③ALBがすでに検査してどの状態か、④task.startedAt＋Gより前に全体が準備完了できるか、の順に確認します。特にバック200秒の直列例は①で成立しないため、③④の延長だけでは解決しません。")

s = section("08_時間計算", "値を選ぶための計算方法", "Excel版ではこの章の末尾に入力可能な計算表を付けています。計算値は時間保証ではなく、設計の不足を見つけるための見積もりです。")
table(s,'記号の意味',['記号','意味','今回の扱い'],[
    ['A / B / F','それぞれADOT・バック・フロントの実準備時間','コンテナ開始からサービス提供可能になるまで。P7のFはJVM開始から。'],
    ['dA / dB / dF','準備完了から最初のHEALTHY観測までの余裕','検査待ち・実行・通知の遅れ。例では5 / 10 / 10秒など。'],
    ['HA / HB / HF','A+dA / B+dB / F+dF','startPeriodの値ではない。実測で置き換える。'],
    ['I / H / τ','ALB検査間隔・復帰成功回数・応答等の余裕','主例は10 / 2 / 2。管理系の反映遅れは別途余裕へ。'],
    ['Ts','task.startedAtをt=0からの相対時刻にした値','最初のコンテナ開始時刻と一致するとは限らない。'],
    ['M','ばらつきに対する設計余裕','45 / 60 / 90秒の仮定。測定で調整する。'],
    ['G','healthCheckGracePeriodSeconds','必要残時間＋M以上を候補にする。'],
],[25,62,85])
code(s,'基本式',r'''
バック初回HEALTHY：バック開始 + HB
フロント初回HEALTHY：フロントJVM開始 + HF
フロント経由のreadiness成立：max(バック開始 + B, フロントJVM開始 + F)
ALB復帰見積もり：readiness成立 + I × H + τ
全体の健康確認：max(必須コンテナの初回HEALTHY時刻, ALB復帰見積もり)
必要な猶予 G_needed：max(0, 全体の健康確認 - Ts) + M

直列の成立条件：HA < ADOT.startTimeout かつ HB < backend.startTimeout
Fargateで明示可能なstartTimeout：最大120秒
（等号ぎりぎりは検知の揺れがあるため採用しない）
''')
p(s,'依存関係で変わる式', '直列ならバック開始=HA、フロント開始=HA+HBです。ADOTの後に両EAPを並列にするなら、両者の開始=HAです。後者はB+Fではなくmax(B,F)が中心になります。CloudWatch Agentは依存なし・非必須なので、自動的にこの直列和へ加えません。ただし同じCPU・メモリ・ネットワークを使うため、その競合を含む起動時間を測定します。')
p(s,'startPeriodの決め方', '各コンテナの開始から初回成功までの分布を取り、通常の遅い側でも起動途中の失敗を数えすぎない値を選びます。例えばバック200秒＋検知余裕10秒なら210を試す、290秒＋10秒なら上限300を試す、という選び方です。必ずその秒数で起動完了するという意味ではありません。早期の誤った成功があると猶予が終わるため、プローブが本当の準備完了条件を見ていることが先です。')
p(s,'P99と最悪値', '多数回の起動からP50・P95・P99・最大を求めます。P99とは100回中およそ99回がその時間以内という分位の目安で、最大値の保証ではありません。各段階のP99を足しても全体のP99と等しいとは限りません。同時起動、CPU制約、イメージ取得、DB混雑を含む実際の1本の起動チェーンも測ります。')
p(s,'故障検出時間の式の限界', 'おおまかな検知速度はinterval×retriesで比較できますが、次の検査までの位相、コマンド実行時間、通知遅延があります。ALBもinterval×UnhealthyThresholdCountは規模感であり、厳密な停止時刻ではありません。timeoutの長い外部コマンドを重ねるとさらに遅くなるので、HTTPクライアントの上限もECS timeoutより短くします。')

s = section("09_EAPと健康判定", "UBI / Java / EAPで何を確かめるか", "JVMプロセスがあることと、WARのデプロイが完了しAPIを使えることは別です。")
table(s,'準備完了までの段階',['段階','見える状態の例','この段階だけでは不足する理由'],[
    ['コンテナ開始','コンテナのlastStatus=RUNNING','entrypointが動き始めただけかもしれない。'],
    ['JVM開始','javaプロセスが存在','クラス読み込み、モジュール初期化、Java Agent初期化が残る。'],
    ['EAPのポート待受','8080や8180へTCP接続可能','目的のWARが未デプロイ、デプロイ失敗、必要資源未初期化の場合がある。'],
    ['EAPのサーバー準備','server-state=running、boot / deploymentにエラーなし','アプリ独自の初期データや必須APIの準備は別に確認する。'],
    ['アプリのreadiness','必要なハンドラ・初期化・最小限の依存が利用可能','実トラフィック量での遅延・JIT性能は負荷試験で確認する。'],
],[29,53,88], 'S26 S27')
table(s,'同一タスク内のポート例',['コンテナ','HTTP / 管理 / 受信','指定・用途'],[
    ['frontend','8080 / 9990','HTTPはALBから到達可能なアドレスで待受。管理は127.0.0.1へ制限する例。'],
    ['backend','8180 / 10090','標準ソケット構成ならport-offset=100。フロントは127.0.0.1:8180へアクセス。'],
    ['adot','13133 / OTLP 4317・4318','health_checkとOTLPは別。タスク内専用なら127.0.0.1を明示。'],
    ['cwagent','用途で決定。Application Signals例は4316','ADOTと4317 / 4318などを二重にバインドしない。'],
],[24,46,100],'S13 S20 S25')
p(s,'EAPのポートオフセット', 'バックのstandalone起動に-Djboss.socket.binding.port-offset=100を加える例では、標準の8080は8180、9990は10090になります。既存のsocket-binding-groupやfixed-port等で上書きされていれば結果は変わるため、管理API・起動ログ・待受を確認します。HTTPだけでなく管理、HTTPS、トランザクション、必要なクラスタ用ポートも確認します。コンテナが別でもネットワーク空間が共通なので衝突を避けられません。', 'S13 S25')
p(s,'EAP標準healthとアプリ用healthを区別', 'Red HatのEAP 8.1 / XP 6.0資料にはSmallRye Health、standaloneでの利用、管理インターフェイスの/healthが記載されています。ただし今回のカスタムUBIイメージに、どのプロファイル・Galleon layer・拡張が入っているかは未確認です。/health/readyや/health/liveを使う場合は実際のsubsystemとHTTP応答を確認します。EAPのバージョン名だけから、アプリポート8080に/healthが必ず存在すると決めません。', 'S26 S27')
p(s,'アプリ用エンドポイントの契約', 'バックの/app/health/readyは、目的のアプリが初期化を終え、必要な処理を受けられるときだけ200、それ以外は503を返す設計例です。フロントの/app/health/ready-localはフロント自体、/app/health/readyはフロント自体＋バックの利用可能性を判定します。認証画面へ転送したり、まだ準備していないのに固定200を返したりしないようにします。実URLはアプリ実装に合わせて変更します。')
p(s,'readinessとlivenessを一緒にするときの注意', 'livenessは『自分が生きていて処理を続けられるか』、readinessは『今リクエストを受けてよいか』です。ECSの1つのコンテナhealthCheckをHEALTHY依存に使うと、起動後も同じ条件で監視します。共通DBや外部APIの短い障害を毎回UNHEALTHYへ結び付けると、再起動しても直らないタスクを大量に置換することがあります。起動完了条件と継続的なローカル健全性を設計し、外部サービスの可用性はALB readinessや別監視との役割を決めます。', 'S01 S04')
p(s,'軽い検査を作る', '健康確認で毎回重い業務処理や大量SELECTを実行しません。バックへの小さな確認に1秒の上限、確認結果を2秒程度だけキャッシュする、といった具体案をアプリ要件に合わせて評価できます。ALBの各ノードとコンテナの両方から呼ばれるので、1つのタスクに10秒ごと1回しか来ないと決めつけません。', 'S08')

s = section("10_ADOTとCWAgent", "サイドカーの開始・検査・欠損対策", "サイドカーは軽いことが多くても、起動0秒とは扱いません。設定読み込みやCPU競合を含めて測ります。")
p(s,'ADOT 13133の正体', '13133はhealth_check拡張のHTTPポートです。OTLPを受け取る4317 / 4318とは役割が違います。設定ファイルのextensionsにhealth_checkを書くだけでなく、service.extensionsで有効化します。参照した公式ADOTイメージ実装には/healthcheckがあり、標準では127.0.0.1:13133/のHTTP 200を確認します。実際の採用タグ / digestでも同じバイナリ・設定を確かめます。', 'S15 S16 S17')
p(s,'ADOTの健康＝トレース欠損ゼロではない', 'この依存関係はバックがCollectorの準備前に送ってしまう競合を減らします。一方、受信後の送信失敗、IAM不足、保存先障害、SDKのサンプリング、メモリキュー満杯、Collector終了時の未送信データは別問題です。アプリ起動直後に識別できるテストトレースを送り、保存先で観測する試験が必要です。HEALTHYを待つだけで『確実な受信・保存』と断定しません。', 'S17 S18')
p(s,'キューと再試行をどこへ置くか', 'SDKからCollectorに到達できない時間にはSDK側のバッファと再試行が必要です。Collectorが受け取った後の保存先障害には、対応exporterのsending_queue / retry_on_failureが関係します。Collectorのメモリキューはタスク置換で失われ得ます。永続キューもFargateの一時ストレージに置くだけでは、タスクをまたぐ耐久性の保証にはなりません。永続化・順序・重複・容量は別に設計します。', 'S18')
p(s,'health_checkのバージョン差', '参照したOpenTelemetryのmain文書には、従来のパイプライン検査機能の制約と、コンポーネント状態を使う新しい方式への移行が記載されています。upstreamの最新オプションが、そのまま選択したADOT配布版に含まれるとは限りません。今回の設定例は基本のhealth_checkを用い、バージョンを固定して検証する前提です。', 'S17')
p(s,'CloudWatch Agentのプロセス検査', 'プロセスの存在を確認することは、設定の読み込み成功やCloudWatchへの送信成功までは検査しません。startPeriod=30、interval=30、timeout=5、retries=3という例で軽い生存確認を行い、メトリクス・ログの送信途絶を別に監視します。非必須のため、これが不健康でもタスク全体の健康判定へ自動的には反映しません。', 'S02 S19')
p(s,'公式イメージにshやpgrepがあるとは限らない', '参照したCloudWatch Agent公式Dockerfileは最終段がscratchです。CMD-SHELLでpgrepを実行する例を、そのまま公式イメージへ入れるとコマンド自体が存在せず失敗する可能性があります。専用の静的プローブを派生イメージへ同梱してCMDで実行する方法、またはシェル・procpsを備えた管理下のイメージを使う方法を示します。', 'S19')
p(s,'ADOTとCloudWatch Agentの担当', '例えばトレースはADOT、特定メトリクスはCloudWatch Agent、と送信経路を決めます。Application Signalsを有効にしたCloudWatch Agentがトレースも受ける場合は、ADOTとの重複送信、受信ポートの衝突、Java Agentの二重導入がないかを確認します。今回の『CloudWatch Agentは依存なし』は、アプリの起動やトレース開始がそのAgentの準備に依存しないという業務上の前提です。', 'S20')

s = section("11_検査コマンド", "コンテナ内で動く検査の具体例", "以下の/app/health/*は提案する契約です。実装済みのURLへ合わせ、成功・失敗の両方を実イメージで試験してください。")
BACK_CMD = r'''code=$(curl --noproxy '*' --silent --show-error --output /dev/null --write-out '%{http_code}' --connect-timeout 1 --max-time 3 http://127.0.0.1:8180/app/health/ready) && [ "$code" = "200" ]'''
FRONT_CMD = BACK_CMD.replace('8180/app/health/ready','8080/app/health/ready-local')
code(s,'バック：HTTPが正確に200か確認',BACK_CMD,'sh')
code(s,'フロント：ローカル準備完了だけを確認',FRONT_CMD,'sh')
p(s,'このコマンドにした理由', 'curlの-fだけでは3xxを失敗扱いしないため、明示的に200を比較します。リダイレクトを追跡する-Lは付けません。接続待ち1秒・全体3秒に制限し、ECS timeout=5の内側で終わるようにします。--noproxyでlocalhost検査がHTTPプロキシへ出ないようにします。UBIの種類によりcurlや/bin/shの同梱状況が違うので、イメージビルド時に確認します。')
code(s,'ADOT：公式同梱バイナリを使うECSコマンド', '["CMD", "/healthcheck"]', 'json', 'S15 S16')
p(s,'ADOTコマンドの調整範囲', '参照した実装は-portでポートを変更できますが、パスは/です。health_checkのパスを変えたのに、このバイナリが同じパスを検査すると決めないでください。例ではendpoint=127.0.0.1:13133、path=/を明示します。コマンド自体のHTTP待ち時間はECS timeout=2で上限を持たせる例です。', 'S16')
code(s,'CloudWatch Agent：プローブ同梱済み派生イメージの例', '["CMD", "/usr/local/bin/proc-healthcheck", "/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent"]','json')
p(s,'proc-healthcheckはこの資料の追加実装', '上記パスは公式CloudWatch Agentに元からあるコマンドではありません。付録のGo実装をLinux向けに静的ビルドしてCOPYした派生イメージでのみ使います。/proc内の実行ファイルの絶対パスを確認するため、pgrepの短いプロセス名制約や検索コマンド自身への一致を避けられます。コンテナのPID名前空間を標準のまま使う前提です。')
code(s,'シェルとprocpsが存在すると確認したイメージだけの代替', r'''["CMD-SHELL", "pgrep -f '^/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent([[:space:]]|$)' >/dev/null"]''','json')
p(s,'プロセス確認の限界', '代替pgrep例は起動コマンドのargv[0]が上記絶対パスである前提です。pgrep -x amazon-cloudwatch-agentのような長い名前は、環境のプロセス名の長さ制限で一致しないことがあります。kill -0 1も、PID 1がランチャーならAgent自身の存在を証明しません。プロセス検査だけではハングや送信エラーを見つけられないことを運用監視で補います。')

s = section("14_障害と運用", "稼働中・停止中も同じ構成を点検する", "起動順を決めたら、起動後の故障と終了順も合わせて評価します。")
table(s,'症状からの切り分け',['見える症状','先に確認すること','値変更だけで直るか'],[
    ['フロントがPENDINGのまま起動しない','dependsOnの向き、依存先HEALTHYの有無、startTimeout、循環、stoppedReason','バック準備が120秒を超えるならG延長では直らない。'],
    ['コンテナ検査が毎回失敗','URL、port-offset、バイナリの有無、CMD/CMD-SHELL、終了コード、認証','存在しないcurlや健康URLはstartPeriod延長で直らない。'],
    ['ローカルは成功、ALBはTarget.Timeout','フロントがENIから到達可能なアドレスにbindしているか、SG、NACL、ポート','Gは到達不能を直さない。'],
    ['ALBでResponseCodeMismatch','パス、Hostヘッダー、認証リダイレクト、context root、準備中503','200–499を全部成功にして隠さない。'],
    ['ADOT healthyなのにトレースなし','SDK送信先・protocol・sampling、receiver/pipeline、IAM、exporter・送信先','13133成功だけでは送信経路の検証にならない。'],
    ['CW Agent停止後もアプリは動く','essential=false、restartPolicy、送信途絶アラーム','意図した可用性分離。必要なら個別再起動を検討。'],
    ['新タスクが繰り返し置換される','first HEALTHY、task.startedAt、ALB状態、exitCode、OOM、起動CPU/メモリ','原因が起動遅延かプロセス異常かを区別して調整する。'],
    ['全台のreadinessが一斉に失敗','共通DB/API障害、プローブ負荷、fail open、再試行の集中','全台再起動では復旧しないケースがある。'],
], [38,75,65])
p(s,'任意のCloudWatch Agent再起動', 'restartPolicy.enabled=true、restartAttemptPeriod=60を例にできます。これは『最低60秒動けたコンテナについて再起動を認める』という条件を含み、起動直後10秒で失敗するコンテナが必ず再起動される設定ではありません。また対象はコンテナの終了であり、プロセスが生きたままhealthCheckが失敗しているだけで自動的に同じコンテナを再起動する仕組みではありません。', 'S21 S22')
code(s,'任意設定の断片', '{"restartPolicy": {"enabled": true, "restartAttemptPeriod": 60}}','json')
p(s,'更新時の例', 'ECSローリング更新でdesiredCount=2、minimumHealthyPercent=100、maximumPercent=200、deploymentCircuitBreaker={enable:true,rollback:true}を検証例にできます。古い正常タスクを維持しつつ新しいタスクの健康を確認します。必要な一時リソース、IP、クォータ、実行費用を見込んでください。ロールバックには戻れる正常なデプロイが必要です。値だけで初回構築や全台障害の配信を保証するものではありません。', 'S23 S24')
p(s,'健康に数える条件', 'ALBを使い、必須コンテナにもhealthCheckがあるサービスでは、新タスクを正常台数として扱うにはターゲットの正常と必須コンテナの正常を考慮します。プロセスRUNNINGだけを成功と数えないでください。Gが長いと失敗の確定が遅れ、デプロイが長く継続する場合があります。', 'S24')
p(s,'設定更新の違い', 'startPeriodやdependsOnなどタスク定義の変更は新リビジョンを作り、サービスへ反映して新しいタスクで検証します。healthCheckGracePeriodSecondsの更新自体は新規デプロイを開始しないとAPIに記載されています。変更しただけで、既存コンテナの起動時猶予が初期化されると考えないでください。', 'S05')
p(s,'停止とトレースの最後の処理', '直列依存を付けると停止順は逆向きになり、フロント→バック→ADOTの順序を表現できます。ただし異常終了・OOM・強制停止ではすべてのflushが完了するとは限りません。EAPの終了処理、HTTPのdraining、SDKのshutdown/flush、ADOTのstopTimeoutを試験します。CloudWatch Agentに依存がなければ、最後まで必ず残る順序は指定していません。', 'S03 S18')

s = section("15_測定と検証", "実環境へ当てはめる手順", "この資料作成ではAWSへ接続しておらず、既存サービスへの変更も行っていません。次の確認は利用者の検証環境で行うための手順です。")
table(s,'収集したい時刻',['記録','取得場所','使い道'],[
    ['起動要求 / createdAt / pullStartedAt / pullStoppedAt','ECS DescribeTasks、デプロイ記録','起動要求からの総時間と、健康猶予の対象時間を混同しない。'],
    ['task.startedAt','ECS DescribeTasks','サービス猶予の基準時刻を整理する。'],
    ['各コンテナStartedAt','タスク内のメタデータV4 /task、アプリログ','startPeriodと依存先の待ちの時間を分ける。'],
    ['ADOT初回ready / API listen / EAP deployment完了','UTCミリ秒付き起動ログ、専用プローブログ','実準備時間A / B / Fを測る。'],
    ['初回コンテナHEALTHY','状態変化イベントと時刻付きポーリング','検査周期と通知の遅れdA / dB / dFを含めて測る。'],
    ['ターゲットinitial / unhealthy / healthy','DescribeTargetHealthを時刻と一緒に保存、ALBヘルスチェックログ等','初回成功か異常からの復帰かを分ける。'],
    ['stoppedReason / stopCode / container exitCode・reason','停止タスクのDescribeTasks、サービスevents','依存タイムアウト、OOM、プロセス終了、ALB異常を分ける。'],
],[45,64,63], 'S06 S08 S14')
code(s,'Windows PowerShellからの参照コマンド例',r'''
# 例示名を実環境の名前に置き換える。読み取りのみ。
aws ecs describe-task-definition --task-definition YOUR_TASK_FAMILY
aws ecs describe-services --cluster YOUR_CLUSTER --services YOUR_SERVICE
aws ecs describe-tasks --cluster YOUR_CLUSTER --tasks YOUR_TASK_ARN
aws elbv2 describe-target-groups --target-group-arns YOUR_TARGET_GROUP_ARN
aws elbv2 describe-target-health --target-group-arn YOUR_TARGET_GROUP_ARN
aws elbv2 describe-target-group-attributes --target-group-arn YOUR_TARGET_GROUP_ARN
''','powershell')
code(s,'タスク内Linuxコンテナからのメタデータ参照例',r'''
# curlがある診断用コンテナで実行。ホストのPowerShellコマンドではない。
curl --silent --show-error --max-time 3 "${ECS_CONTAINER_METADATA_URI_V4}/task"
''','sh','S14')
p(s,'検証順序', '最初に健康コマンド単体で200成功、503失敗、接続拒否、応答停止、コマンド不存在を確かめます。次に通常起動、コールド起動、最大同時デプロイ、CPUを圧迫した状態で起動を繰り返します。依存先をわざと遅らせ、100秒付近では成功し130秒超では依存期限の問題が見えることを検証します。起動後はバック停止・ADOT停止・CW Agent停止をそれぞれ分けて試験します。')
table(s,'検証ケースと合格条件',['ケース','合格とする観測','関連する案'],[
    ['startPeriod途中で正常化','210を待たずにHEALTHYになり、依存側が開始できる','P1 / P2'],
    ['初回成功の後に連続失敗','210秒以内でもR回の失敗でUNHEALTHYになる','全案'],
    ['バックの健康成功が120秒超','Gを600にしても依存待ちに失敗する理由が記録される','P3'],
    ['フロントがバックより先に準備完了','ローカルreadyは成功可。ALB readyはバック利用まで503','P4 / P5 / P6'],
    ['ALB猶予中','ALBから検査が届く。正常化すれば猶予終了前でも配信する','全成立案'],
    ['同一タスクのEAPを2つ起動','8080/8180、9990/10090等が競合せず、正しい相手を検査する','全案'],
    ['Collector保存先への接続を遮断','13133と送信失敗を区別し、キュー・再試行・欠損を観測する','全案'],
    ['CW Agentを終了','アプリの継続と監視途絶の検出を確認。任意restartPolicyの条件を確認','全案'],
    ['フロントを停止 / タスクを更新','通信のdraining、停止順、SDK / ADOT flushを確認','依存を持つ案'],
    ['サービスを0台から起動','古い正常タスクがない条件で503 / fail openと復旧時間を確認','全案'],
],[46,81,24])
p(s,'初期サンプル数と記録', 'まず各主要条件で20〜30回程度の起動を取り、裾があると分かった条件を追加測定する方法が考えられます。この数でP99を精密に確定したとは言えません。CPU・メモリ、イメージdigest、EAP設定、Java Agent、デプロイ数、AZ、DB状態も記録します。重い初期データ処理やDBスキーマ変更があるなら、アプリ起動のたびに行う必要性から見直します。')

s = section("16_歴史と背景", "なぜ複数の仕組みができたのか", "似た名前が増えた理由は、解決している問題が違うからです。")
table(s,'主な歩み',['時期','追加・変化したこと','当時解決したかった問題','今回との関係'],[
    ['2017-12-27','ECSにELB health check grace period','起動に時間がかかるタスクが、準備できる前に異常として止められる。','現在のサービス猶予300秒の系譜。'],
    ['2018-03-08','ECSのコンテナhealthCheck / task health管理','ロードバランサーだけでは、各コンテナ内部の状態やHTTP以外の確認が難しい。','サイドカーを含む内部監視とstartPeriodの役割。'],
    ['2018-03-26','Fargate platform 1.1.0でコンテナhealthCheck対応','サーバー管理をしないFargateでもコンテナ単位で確認したい。','FargateでのhealthCheck利用の前提が整う。'],
    ['2019-03-07','ECSの起動・停止依存とコンテナ別タイムアウト','記録係を先に起こし、最後に止める。初期化処理の完了を待つ。','ADOT→バック→フロントのような構成を表現できる。'],
    ['2019-03-27','Fargate 1.3.0で依存などの追加設定を利用可能','Fargateにも同じ順序制御を持ち込む。','Linux platform 1.3.0以降という要件。'],
    ['2024-08-15','ECSのコンテナ別restart policy','一時的なコンテナ終了から、タスク全部を置換せず回復したい。','CW Agentなどの個別復旧を検討できる。ただし条件がある。'],
    ['2026-10-07 確認','現在のAPI・公式資料で役割と値を照合','古い記事の用語や、Docker / Kubernetesの設定を混同しない。','healthCheckGracePeriodSecondsは現行APIでELB等とコンテナ検査の異常を対象にする。'],
],[24,43,67,54],'S29 S30 S31 S32 S33 S05')
p(s,'1つの待ち時間では足りない理由', '受付・台所・記録係それぞれの準備が違うので、まず各担当の準備を見ます。さらに記録係の後に台所を始める順序が必要になり、最後に店長が早すぎる閉店判断をしない仕組みが必要になります。startPeriodは各担当の起動中の失敗数、dependsOnは開始順、startTimeoutは待ちの期限、サービス猶予は店長の置換判断、と分けて考えれば矛盾しません。')
p(s,'歴史的な名称への注意', '昔の発表では『ELBヘルスチェックの猶予』と説明されていました。現在の公式APIではコンテナヘルスチェックなども記載されています。古い名称だけでALBにタイマーがあると解釈したり、今もELBの失敗だけが対象だと判断したりしないことが重要です。', 'S05 S29')

s = section("17_よくある疑問", "設定を決める前の最終確認", "ここは各章の判断を短く参照するための一覧です。")
table(s,'よくある疑問',['疑問','答え'],[
    ['startPeriod=210は210秒間チェックしない？','いいえ。チェックし、成功すればその時点でHEALTHY。初回成功前の猶予中の失敗を数えない。'],
    ['210+210+300を足す？','足しません。startPeriodは実起動時間ではなく、Gの起点も各コンテナ開始とは別。実測のクリティカルパスで計算する。'],
    ['G=300はALBの初回検査を300秒後へずらす？','いいえ。ALBは独立して検査。ECS側の健康異常による置換を猶予する。'],
    ['backend.startPeriod=210とstartTimeout=120は同時に指定可能？','値の組み合わせ自体は可能。初回HEALTHYが120秒未満なら使える。初回成功が210秒になる設計は間に合わない。'],
    ['frontend.startTimeout=120ならバックを120秒待つ？','この依存の待ちに関係するのは待たれるbackendのstartTimeout。待つ側の値だけでは代わりにならない。'],
    ['フロントが200秒で準備完了するのも120秒制約に違反？','他コンテナがフロントのHEALTHY等を待っていなければ、その依存期限とは別。サービス猶予・コンテナ健康検査で評価する。'],
    ['STARTならバックのAPIが使える？','コンテナ開始しか確認しない。APIがまだ使えない間の再試行・ready判定が必要。'],
    ['ADOT healthyで全トレースを確実に保存できる？','できません。受信・SDK・exporter・IAM・保存先・キュー・終了時flushを別に検証する。'],
    ['CW Agentの起動時間も必ず直列に足す？','依存なし・非必須なら直列に加算しない。ただしCPU等の競合を含めて各時間を測る。'],
    ['essential=falseなら不健康なCW Agentは再起動する？','その指定だけでは再起動を保証しない。終了時restartPolicyと、送信途絶の監視を別に検討する。'],
    ['DockerfileのHEALTHCHECKだけでECSのHEALTHY依存になる？','ECSが監視・報告するにはタスク定義のhealthCheckを明示する。'],
    ['ALBのHealthyThresholdCount=2なら新規登録でも必ず2回？','初回正常化は成功1回。いったん異常になってからの復帰は設定回数が必要。'],
    ['フロントとバックを別コンテナにすれば同じ8080でもよい？','同じFargateタスクの共有ネットワークでは衝突する。HTTPと管理を含めて分離する。'],
    ['EAPだから/actuator/healthを使える？','それはEAPが一律に提供するURLではない。アプリの実装・拡張・管理エンドポイントを確認する。'],
    ['Gを延ばせばOOMや必須コンテナ終了も待ってくれる？','そのような保護ではない。メモリ・終了コード・起動設定の原因を修正する。'],
    ['Terraformのdepends_onにコンテナ名を並べればよい？','Terraformのリソース依存とECS JSONのdependsOnは別。container_definitions内へ正しいJSON構造を入れる。'],
    ['最終的にどの案？','未計測ならP4を検証。バックの初回HEALTHYが余裕を持って120秒未満なら希望のP1 / P2を選べる。'],
],[62,108])
p(s,'この資料で未確定のこと', '実際の起動分布、採用イメージの中身、プローブURLの実装、EAPのプロファイル、既存ALB設定、タスクCPU/メモリ、Java AgentとCollectorの版、アプリの接続リトライは実機未確認です。したがってP4=300秒やP2=300秒を本番で必ず成立する保証値とはしていません。Excelの値を実測で置き換え、各依存の期限とサービス猶予の両方を検証することが完了条件です。')
