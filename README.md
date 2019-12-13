動画反転システムの冗長構成サンプルシステム
===

目次
===
* [動画反転システムの冗長構成サンプルシステム](#%E5%8B%95%E7%94%BB%E5%8F%8D%E8%BB%A2%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0%E3%81%AE%E5%86%97%E9%95%B7%E6%A7%8B%E6%88%90%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0)
* [構成](#%E6%A7%8B%E6%88%90)
* [事前確認](#%E4%BA%8B%E5%89%8D%E7%A2%BA%E8%AA%8D)
* [構築](#%E6%A7%8B%E7%AF%89)
* [動作確認](#%E5%8B%95%E4%BD%9C%E7%A2%BA%E8%AA%8D)
* [改定履歴](#%E6%94%B9%E5%AE%9A%E5%B1%A5%E6%AD%B4)

# システム構成

## 必要なもの

 - Kubernetes マスター用 PC 1台 (Raspberry PI 可)
 - Kubernetes ワーカー用 PC 2台 (Raspberry PI 可)
 - ロボット用 PC 1台

## 静的構造

![system](https://user-images.githubusercontent.com/45954537/70786986-21c2b400-1dd1-11ea-98da-6e0161343203.png)

## ソフトウェアのインストール

各PCに必要なソフトウェアの一覧を下表に示します。

| | Kubernetes | Docker | OpenRTM-aist |異常検出＆切り替えアプリ|jqコマンド
:----:|:----:|:----:|:----:|:----:|:----:|
| マスター用PC | ○ | ○ | - | ○ | ○ |
| ワーカー用PC | ○ | ○ | - | - | - |
| ロボット用PC | - | - | ○ | - | - |

### kuberntest と Docker のインストール

Kubernetes のインストールは、下記のURLを参照ください。

https://github.com/r-kurose/rtm_k8s/blob/master/index.md#インストール手順

### OpenRTM-aist のインストール

- Windows の場合

  下記のURLの手順に従ってインストールしてください。
  https://www.openrtm.org/openrtm/ja/doc/installation/install_1_2/cpp_1_2/install_windows_1_2

- Ubuntu の場合

  下記のURLの手順に従ってインストールしてください。
  https://www.openrtm.org/openrtm/ja/doc/installation/install_1_2/cpp_1_2/install_ubuntu_1_2


### 異常検知とRTCの切り替えスクリプトをダウンロード
下記コマンドで必要なスクリプトをマスター用 PC で取得してください。

これらは、異常の検出や多重化の RTC 切り替えに使うスクリプトで動作確認で使用します。

  `wget https://raw.githubusercontent.com/r-kurose/rtm_k8s_redundancy/master/app.sh`
  `wget https://raw.githubusercontent.com/r-kurose/rtm_k8s_redundancy/master/man_ctl.py`

### JSON形式の情報をパースする jq コマンドのインストール
app.sh は kubernetes から得られるJSON形式の情報をパースして切り替えを判断しているため、

JSON形式の情報をパースできる jq コマンドを同じくマスター用PCへインストールします。

- Windows の場合

  下記のURLからダウンロード、インストールしてください。
  
  https://stedolan.github.io/jq/

- Ubuntu の場合

  `sudo apt -y install jq`
  
### OpenCVCamera と CameraViewer のインストール

- Windows の場合

  OpenRTM-aist がインストールされていれば、追加のインストールは不要です。
  
  OpenRTM-aist をインストールしたフォルダ配下に OpenCVCameraComp と CameraViewer というRTCがあるので起動してください。
  
  - 詳細なインストール場所を知りたい方は以下を参照してください
    https://www.openrtm.org/openrtm/ja/doc/installation/install_1_2/cpp_1_2/install_windows_1_2

- Ubuntu の場合

　下記のgithubからソースコードを取得してください。

# 事前確認

まずは、カメラとカメラビューワーの RTC の動作確認を行います。

これは、カメラが使える環境であるかを事前に確認する項目なので、不要であれば実施は不要です。

詳細な確認手順は下記のURLを参照してください。

https://www.openrtm.org/openrtm/ja/doc/installation/sample_components/opencvcameracomp


# 構築

## クラスター構築手順

まずマスターノードを初期化し、その後にワーカーノードをマスターノードに登録します。
具体的なやり方を下記に示します。

### マスター用PCで初期化
　下記の初期化手順をおまじないとして実行してください。これでマスターノードとして動作します。
```
kubeadm init --pod-network-cidr=10.244.0.0/16
```

### ワーカー用PCでワーカーノードとしてマスターへ登録
```
kubeadm join <マスターノードの kubeadm init 実行で表示されるパラメーター>
```
確認方法: マスターノードで `kubectl get nodes` を実行するとノードが見えます。

### クラスタのネットワーク構築
　マスター用PCでKubernetes のネットワークを構築するために以下のおまじないを実行してください。
```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```
### ワーカーにラベルを設定
　マスターPC からワーカーにラベルを設定します。
このラベルは、ソフトウェア（Docker イメージ）を動かすワーカーノードを指定するのに使用されます。

`kubectl label node <ノード名> flip-1=true`
`kubectl label node <ノード名> flip-2=true`


# 動作確認



# 改定履歴

  - 2019-12-13: 初版
