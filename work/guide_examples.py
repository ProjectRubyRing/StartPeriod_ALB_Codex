"""Concrete examples shared by the workbook and Markdown."""
import json
import guide_content as g

g.SOURCES.extend([
    ("S38", "AWS ELB TargetGroupAttribute API", "https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_TargetGroupAttribute.html", "slow start 30–900秒、登録解除遅延0–3600秒、ルーティング閾値"),
    ("S39", "AWS CloudFormation ECS ContainerDefinition", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-ecs-taskdefinition-containerdefinition.html", "CloudFormationのプロパティ名とコンテナ依存の位置"),
])

def containers(pattern):
    values=[]
    images={"adot":"REPLACE_WITH_ADOT_IMAGE_DIGEST", "backend":"REPLACE_WITH_BACKEND_UBI_EAP_IMAGE_DIGEST", "frontend":"REPLACE_WITH_FRONTEND_UBI_EAP_IMAGE_DIGEST", "cwagent":"REPLACE_WITH_CWAGENT_IMAGE_WITH_PROC_HEALTHCHECK"}
    commands={"adot":["CMD","/healthcheck"],"backend":["CMD-SHELL",g.BACK_CMD],"frontend":["CMD-SHELL",g.FRONT_CMD],"cwagent":["CMD","/usr/local/bin/proc-healthcheck","/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent"]}
    for row in [r for r in g.CONFIG_ROWS if r[0]==pattern["id"]]:
        _,name,essential,sp,interval,timeout,retries,st,dep=row
        c={"name":name,"image":images[name],"essential":essential=="true","stopTimeout":30 if name=="cwagent" else 60,
           "healthCheck":{"command":commands[name],"interval":interval,"timeout":timeout,"retries":retries,"startPeriod":sp}}
        if isinstance(st,int): c['startTimeout']=st
        if dep!='なし':
            target,condition=dep.split(' : ')
            c['dependsOn']=[{"containerName":target,"condition":condition}]
        if name=='frontend': c['portMappings']=[{"name":"frontend-http","containerPort":8080,"protocol":"tcp"}]
        if name=='adot': c['command']=['--config=/etc/ecs/otel-config.yaml']
        values.append(c)
    return values

P4=next(z for z in g.PATTERNS if z['id']=='P4')
TASK={"family":"eap-healthcheck-example", "requiresCompatibilities":["FARGATE"],"networkMode":"awsvpc",
      "cpu":"2048","memory":"8192","runtimePlatform":{"operatingSystemFamily":"LINUX","cpuArchitecture":"X86_64"},
      "executionRoleArn":"REPLACE_WITH_EXECUTION_ROLE_ARN","taskRoleArn":"REPLACE_WITH_TASK_ROLE_ARN",
      "containerDefinitions":containers(P4)}
SERVICE_FRAGMENT={"healthCheckGracePeriodSeconds":300,"desiredCount":2,
    "deploymentConfiguration":{"minimumHealthyPercent":100,"maximumPercent":200,"deploymentCircuitBreaker":{"enable":True,"rollback":True}},
    "loadBalancers":[{"targetGroupArn":"REPLACE_WITH_TARGET_GROUP_ARN","containerName":"frontend","containerPort":8080}]}
TARGET_FRAGMENT={"Protocol":"HTTP","Port":8080,"TargetType":"ip","HealthCheckProtocol":"HTTP","HealthCheckPort":"traffic-port",
    "HealthCheckPath":"/app/health/ready","HealthCheckIntervalSeconds":10,"HealthCheckTimeoutSeconds":5,"HealthyThresholdCount":2,"UnhealthyThresholdCount":3,"Matcher":{"HttpCode":"200"}}

s=g.section('12_JSON設定例','ECS JSONへ落とし込む','テンプレート。REPLACE_WITH_*を置換し、既存のログ・Secrets・CPU/メモリ・起動引数等へ統合して使用します。')
g.p(s,'このJSONの前提','P4を主例にします。タスク2 vCPU / 8 GiBは4コンテナを置く形式例であり、2つのEAPに十分なサイズだと検証したものではありません。Javaヒープだけでなくメタスペース・直接メモリ・スレッド・Java Agent・サイドカーを含むメモリと、並列起動時のCPUを計測します。ARM64を使う場合はruntimePlatformと全イメージのアーキテクチャを合わせます。')
g.p(s,'イメージ側で完了しておくこと','バックEAPにport-offset=100、フロントのHTTP待受にALBからの到達性、管理インターフェイスに適切な制限を設定します。各/app/health/*を実装し、curl・シェルを確認します。ADOTには後述の設定ファイル、CW Agentには実用途の設定とproc-healthcheckを同梱します。既存のentrypointやJAVA_OPTSをこの資料の例で無条件に上書きしないでください。')
g.code(s,'P4：タスク定義の全体例',json.dumps(TASK,ensure_ascii=False,indent=2),'json')
g.p(s,'運用設定の補完','上の例はヘルスチェックと依存の配置が分かるように、logConfiguration・secrets・各コンテナの細かな資源配分を省いています。採用環境の設定を維持して統合してください。executionRoleArnはイメージ取得・ログ・Secrets等、taskRoleArnはアプリやCollector等のAWS API利用に使い、用途に必要な権限を与えます。外部に公開しない13133や管理ポートはALBへ登録しません。')
g.code(s,'ECSサービスへ統合する断片（単独のcreate-service入力ではない）',json.dumps(SERVICE_FRAGMENT,ensure_ascii=False,indent=2),'json','S05 S23 S24')
g.code(s,'ALBターゲットグループへ統合する断片',json.dumps(TARGET_FRAGMENT,ensure_ascii=False,indent=2),'json','S08 S10')
g.table(s,'他パターンへ変更するときの全差分',['案','依存・タイムアウト','startPeriod変更と追加条件','サービスG'],[
    ['P0','両アプリのdependsOnとADOTのstartTimeoutを削除','ADOT30 / バック210 / フロント210 / CW30。SDKの起動時再試行が必要。',300],
    ['P1','バックにstartTimeout=120、フロントのdependsOnをbackend:HEALTHYへ','ADOT30 / バック90 / フロント60 / CW30。実際の初回HEALTHYが期限内。',150],
    ['P2','バックにstartTimeout=120、フロントのdependsOnをbackend:HEALTHYへ','ADOT30 / バック100 / フロント210 / CW30。バック初回HEALTHY95秒の仮定。',300],
    ['P3','P2と同じ依存。反例として扱い採用しない','バック210 / フロント210。実準備200秒のバックでは期限超過。',600],
    ['P4','このJSONどおり','両アプリはADOT:HEALTHYを待ち、互いには依存しない。',300],
    ['P5','フロントのdependsOnをbackend:STARTへ','startPeriodはP4と同じ。フロントの再接続が必須。',300],
    ['P6','依存はP4と同じ','バック300 / フロント270。他は同じ。起動分布を測定して採用。',420],
    ['P7','依存はP4と同じ。フロントentrypointに準備待ちラッパー','フロントS=300 / I=15 / T=5 / R=6。他はP4と同じ。コンテナ開始順の保証ではない。',450],
],[10,65,92,17])
g.code(s,'ADOT設定：既存設定へ統合する最小断片',r'''
# 既存のexportersやprocessorsを維持して統合する。
# この断片だけでは送信先や完全なpipelineは定義していない。
extensions:
  health_check:
    endpoint: 127.0.0.1:13133
    path: /
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 127.0.0.1:4317
      http:
        endpoint: 127.0.0.1:4318
service:
  extensions: [health_check]
# service.pipelines.traces等に上記otlpと既存のexporterを組み込む。
''','yaml','S16 S17 S18')
g.p(s,'ADOT断片の統合方法','既存のservice.extensionsへhealth_checkを追加し、認証・file_storage等の他の拡張を消さないようにします。receiverの宣言だけではトレース経路にならないため、既存のtraces pipelineにもotlpを指定します。アプリがhttp/protobufを使うなら4318、gRPCなら4317というようにprotocolと送信先を一致させます。Exporterの種類と認証は利用中の保存先に合わせるため、この資料で架空の本番設定を埋めません。')

TERRAFORM=r'''
# 設定の位置を示す例。既存のprovider・変数・ログ・IAMへ統合する。
# P4_container_definitions.jsonは本資料のP4のcontainerDefinitions配列。
resource "aws_ecs_task_definition" "app" {
  family                   = "eap-healthcheck-example"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "2048"
  memory                   = "8192"
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn
  container_definitions    = file("${path.module}/P4_container_definitions.json")
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
}

resource "aws_lb_target_group" "frontend" {
  name        = "eap-frontend-example"
  vpc_id      = var.vpc_id
  target_type = "ip"
  protocol    = "HTTP"
  port        = 8080
  health_check {
    enabled             = true
    protocol            = "HTTP"
    port                = "traffic-port"
    path                = "/app/health/ready"
    matcher             = "200"
    interval            = 10
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}

resource "aws_ecs_service" "app" {
  name                               = "eap-healthcheck-example"
  cluster                            = var.cluster_arn
  task_definition                    = aws_ecs_task_definition.app.arn
  launch_type                        = "FARGATE"
  desired_count                      = 2
  health_check_grace_period_seconds  = 300
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = var.task_security_group_ids
    assign_public_ip = false
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.frontend.arn
    container_name   = "frontend"
    container_port   = 8080
  }
  # ALB listener / ruleで対象TGを関連付ける。
  # 同時作成する場合は、そのリソースへのdepends_onも既存構成に合わせる。
}
'''
s=g.section('13_Terraformと補助','Terraformとコンテナ内の補助実装','Terraformのリソースdepends_onはインフラの作成順です。ECSのコンテナ起動順はcontainer_definitions内のdependsOnで設定します。')
g.code(s,'Terraformの設定位置',TERRAFORM,'hcl','S35 S36')
g.p(s,'Terraform例の位置付け','この断片には変数宣言・provider版・既存ALBのlistener/rule・ネットワーク・IAM作成を含めていません。したがって単独でapplyする完成モジュールではありません。既存リポジトリの固定provider版へ統合し、fmt / validate / planで差分を確認します。Fargate依存が必要なLinux platformは1.3.0以降とし、採用中のプラットフォームで検証します。', 'S03')

GO_PROBE=r'''
// proc-healthcheck: inspect an exact executable path in this container's /proc.
package main

import (
    "fmt"
    "os"
    "path/filepath"
    "strconv"
)

func main() {
    if len(os.Args) != 2 || !filepath.IsAbs(os.Args[1]) {
        fmt.Fprintln(os.Stderr, "usage: proc-healthcheck /absolute/executable")
        os.Exit(2)
    }
    entries, err := os.ReadDir("/proc")
    if err != nil {
        fmt.Fprintln(os.Stderr, "cannot inspect /proc")
        os.Exit(1)
    }
    for _, entry := range entries {
        if !entry.IsDir() {
            continue
        }
        if _, err := strconv.Atoi(entry.Name()); err != nil {
            continue
        }
        exe, err := os.Readlink(filepath.Join("/proc", entry.Name(), "exe"))
        if err == nil && exe == os.Args[1] {
            os.Exit(0)
        }
    }
    fmt.Fprintln(os.Stderr, "expected process not found or not inspectable")
    os.Exit(1)
}
'''
g.code(s,'CloudWatch Agent用：追加する静的プローブの実装例',GO_PROBE,'go')
g.p(s,'プローブの権限と失敗','読み取り権限がない、Agentの実ファイルパスが違う、プロセスが終了している場合は成功を返しません。プロセスが見つかることしか判定しないため、送信先疎通や設定妥当性の代わりにはなりません。このコードは公式同梱機能ではなく追加実装例で、採用イメージ・UID・アーキテクチャでの検証が必要です。')
g.code(s,'派生イメージを作るためのDockerfile例',r'''
# 2つのイメージは承認済みの固定タグまたはdigestで指定する。
ARG GO_BUILDER_IMAGE
ARG CWAGENT_IMAGE
FROM ${GO_BUILDER_IMAGE} AS probe-build
ARG TARGETARCH
WORKDIR /src
COPY proc-healthcheck.go .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} \
    go build -trimpath -o /out/proc-healthcheck proc-healthcheck.go

FROM ${CWAGENT_IMAGE}
COPY --from=probe-build --chmod=0555 /out/proc-healthcheck /usr/local/bin/proc-healthcheck
# ベースイメージのENTRYPOINT・CMD・USERを引き継ぐ。
''','dockerfile')
g.p(s,'P7の起動待ちの設計例','フロントのコンテナが開始したら、バックの/app/health/readyを接続1秒・全体2秒のHTTP検査で確認します。失敗時は5秒の間隔に小さなジッターを加えて再確認し、総経過300秒を越えたら理由をstderrへ記録して終了します。成功後はexecで既存のEAP起動コマンドへ引き継ぎます。待機中のSIGTERMを扱い、起動時の秘密をログへ出さないようにします。固定sleep 210秒では準備の早い回を無駄に待ち、遅い回にも対応できません。')
g.p(s,'P7が必要になる理由と限界','本当に必要なのが『バックAPIが使えてからフロントのJVM初期化を行う』なら、120秒を超える待ちをこのようなアプリ制御に移せます。ただしコンテナ自体は先に開始しており、ECSの厳密なコンテナ直列起動を満たす代替ではありません。最大待ち300秒とEAP起動150秒が常に合計450秒まで伸びるなら、表のstartPeriod=300 / retries=6の想定を超えるため再設計します。表はバック200秒の仮定に対する値です。')

# Place added chapters in their intended order.
g.SECTIONS.sort(key=lambda item:item['sheet'])

s=g.section('18_出典と適用範囲','出典・確認範囲','確認日2026-10-07。公開一次資料の現行記述を確認しました。main / latestは将来変更されるため、導入時は採用版を固定して照合します。')
g.table(s,'一次情報一覧',['ID','資料名','確認した事項','URL'],[[a,b,d,c] for a,b,c,d in g.SOURCES],[10,49,65,80])
g.p(s,'公式仕様と設計例の区別','許容範囲・パラメータの意味・発表日は出典を伴う仕様または事実です。A=20秒、B=200秒、G=300秒などの組み合わせ、マージン、提案URL、プローブ、資源サイズ、P0〜P8の選び方は本資料の設計例です。AWSやRed Hatがこのアプリに推奨した値・動作を実測した値ではありません。')
g.p(s,'基盤ごとの差','Fargate Linuxを主対象にしています。EC2はAgentの版・設定も利用者が管理し、ECS_CONTAINER_START_TIMEOUTはタスク定義のstartTimeoutと独立した設定です。EC2やECS Managed Instancesに別の上限・既定値がある資料を見ても、Fargateの上限120秒を置き換える根拠にはしません。Fargate Windows、Classic Load Balancer、Kubernetesの仕様をこのまま適用しないでください。', 'S03 S12')
g.p(s,'調査上の限界','実AWSアカウント・既存タスク定義・アプリのソース・コンテナ実体を確認していません。JBoss EAPのRed Hatサポート構成の説明は、カスタムUBIイメージをFargateで動かす構成全体の認定・サポート可否を証明するものではありません。本資料は起動・健康判定の設計に対象を絞っています。', 'S28')

s=g.section('01b_用語をやさしく','途中で困らないための用語集','短い意味を先に読み、必要なら詳細章へ戻れるようにしています。')
g.table(s,'言葉と意味',['用語','やさしい意味','今回の例'],[
    ['コンテナ','アプリと動作に必要なものをひとまとめにした実行単位','フロント、バック、ADOT、CloudWatch Agentの4つ。'],
    ['タスク','一緒に実行するコンテナを束ねた1組','今回は同じネットワークを共有する1組。'],
    ['Fargate','コンテナを動かす機械の管理をAWSに任せる実行方法','利用者がEC2のAgent設定を直接変更する構成とは異なる。'],
    ['サイドカー','本体の横で働く補助役のコンテナ','ADOTとCloudWatch Agent。'],
    ['API','別のプログラムに仕事を頼むための窓口','フロントがバックへ業務処理を頼む。'],
    ['HTTP 200 / 503','Webの返事の番号。200は成功、503は現在利用できない','健康確認では準備できるまで503、準備後200とする例。'],
    ['ポート','同じ住所の中で窓口を区別する番号','フロント8080、バック8180。'],
    ['localhost / 127.0.0.1','自分のネットワーク空間の中の宛先','同一Fargateタスク内のコンテナ間で通信できる。'],
    ['healthCheck','元気か・準備できたかを定期的に調べる検査','コンテナ内部でコマンドを実行する。'],
    ['interval','検査と検査の間隔','10秒ごとに確認する目安。'],
    ['timeout','1回の処理を待つ限度','HTTP応答を5秒まで待つ。'],
    ['retries / threshold','何回続けて失敗・成功したら状態を変えるか','一瞬の遅れだけで故障と決めないための回数。'],
    ['essential','そのコンテナをタスクに必須とする指定','trueのADOTが終了すると、通常はタスク全体の停止へつながる。'],
    ['readiness','今、お客さんの依頼を受けてよいか','バックのAPIが使えるまでフロントのALB用検査は成功させない。'],
    ['liveness','処理を続けられる状態で生きているか','一時的な外部DB障害と、自分の停止・ハングを分けて考える。'],
    ['JVM / EAP / WAR','Javaを実行する仕組み / アプリサーバー / 配置するアプリのまとまり','JVMがあるだけでWARが正しく配置できたとは限らない。'],
    ['CPU / メモリ / OOM','計算する力 / 作業場所 / 作業場所の不足による異常','2つのEAPを同時に起こすと資源の取り合いが起こり得る。'],
    ['JIT / ウォームアップ','実行しながら速くする仕組み / 本調子までの準備','健康になった直後に大量アクセスを受ける場合も負荷試験する。'],
    ['トレース / SDK / Collector','処理の足跡 / アプリ内の送信部品 / 足跡の収集係','SDK→ADOT→保存先の各段階で失敗を扱う。'],
    ['キュー / flush','送信を待つデータの列 / 残りを送り出す処理','終了直前のトレースを残さないためにも設計する。'],
    ['digest','イメージ内容を特定する値','同じタグでも中身が変わる問題を避け、検証した版を使う。'],
    ['P99','遅い側まで見る統計の目安','最大時間の保証ではない。実際の遅い起動を追加で測る。'],
],[34,69,76])
g.SECTIONS.sort(key=lambda item:item['sheet'])

patterns_section=next(item for item in g.SECTIONS if item['sheet']=='04_パターン比較')
g.p(patterns_section,'ADOT自身が120秒を超える場合','バックだけでなくADOTも、初回HEALTHYまで120秒以上なら明示したstartTimeout=120の依存設計に収まりません。設定読込みやリモート処理を軽くする、受信準備と外部送信先の確認を分ける、SDK側でCollector未準備を扱う構成へ変える、などを検討します。startPeriodを短くするだけではADOTの処理時間は変わりません。')
g.p(patterns_section,'P8の設定値をそろえる場合','各サービスのアプリ：S=210 / I=10 / T=5 / R=3、essential=true、dependsOn=自分のADOT:HEALTHY。各ADOT：S=30 / I=5 / T=2 / R=3、essential=true、startTimeout=120。各CW Agent：S=30 / I=30 / T=5 / R=3、essential=false、依存なし。ALBを使うサービスのG=300、ALBは共通の10 / 5 / 成功2 / 失敗3 / HTTP200を候補にします。既存バックサービスが準備済みという前提でフロントを更新する例です。')

for item in g.SECTIONS:
    if item['sheet']=='02_設定値の範囲':
        for block in item['blocks']:
            if block['heading']=='ECSサービスとALBターゲットグループ':block['refs']+=' S38'
            if block['heading']=='同じ意味でも設定ファイルによって綴りが違う':block['refs']+=' S39'

verification=next(item for item in g.SECTIONS if item['sheet']=='18_出典と適用範囲')
g.table(verification,'成果物の検証と未実施の検証',['項目','結果','範囲・理由'],[
    ['XLSX構造・文字・書式','検証済み','21シート。全ての文字入りセルをMeiryo UIで統一。色はグレースケール。改行・折返し・行高・列幅・固定枠・印刷範囲を設定。'],
    ['計算表','検証済み','14計算セルの保存値と数式を照合。8パターンと120秒境界・猶予不足など4ケースを独立した式評価で確認。'],
    ['JSONの構文と設定値','検証済み','9つの内部テンプレートとMarkdown内7つのJSONブロックを解析。健康検査の値域・依存先・循環の有無・essentialを確認。AWS登録の成功を示すものではない。'],
    ['Terraformの書式','terraform fmt -check 成功','説明用断片の書式を確認。fmt -diffはdiffコマンドがないため使わず、Pythonで変更差分を確認した。'],
    ['空白・差分','空白エラーなし','作業フォルダーはGitリポジトリではないため通常のgit diff --checkは利用不可。空の基準フォルダーに対しgit diff --no-index --checkで確認。no-indexの差分ありは終了コード1となる。'],
    ['表示の検証','セル情報からのプレビューで確認','6つの代表範囲をローカル描画して確認。Excel本体のCOM起動はサーバー実行エラーで利用できず、Excelネイティブの表示・印刷確認は未実施。'],
    ['出典URL','39件の応答確認','Red Hatの4件はHEADが403だったためGETで再確認して200。他はHEADで応答を確認。各出典の内容確認とは分けて記録。'],
    ['AWS実環境試験','未実施','AWSアカウント・実タスク・アプリのイメージは未提示。起動時間、ALB配信、トレース受信、停止・再起動動作は実機で確認が必要。'],
    ['terraform validate / plan','未実施','既存provider版・変数・ネットワーク・IAMが未提示の説明用断片。実リポジトリへ統合後に実施する。'],
    ['Goプローブのビルド・実コンテナ試験','未実施','Goツールチェーンと採用イメージが未提示。ソース例を静的に確認。Linux向けビルド、UIDとプロセスパスの試験は導入側で実施する。'],
],[47,44,94])

measurement=next(item for item in g.SECTIONS if item['sheet']=='15_測定と検証')
g.p(measurement,'検査履歴の残し方','DescribeTasksのhealthStatusだけでは、すべての検査実行時刻とコマンド出力の履歴を取得できません。Fargateでホストのdocker inspectが自由に使えるとも考えないでください。検証用プローブやアプリのreadiness状態変化をUTC時刻付きで記録し、ALBの状態・サービスイベントと突き合わせます。healthCheckコマンドの出力が通常のアプリログへ自動的に出るとは仮定せず、ログの取得方法を事前に確かめます。')
