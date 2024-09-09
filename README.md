# 💊医療機関、薬剤検索アプリ

### **TEAM B  :  haruka, kumin, meme**
## 開発サービス概要

以下の機能を備えたLINEのチャットbotを開発
- 症状や位置情報からの受診可能な医療機関の提案
- 処方された薬に関する対話形式（薬の説明や副作用）での疑問解消

📍全体
https://github.com/user-attachments/assets/75e7c21e-37ac-4978-a8e8-653ac431aab9

📍期待しないメッセージがきた時の挙動
https://github.com/ms-engineer-bc24-06/sec8-b/issues/18#issue-2512703982

### **開発理由**
- 薬に関する情報について、使い方や副作用が気軽に検索できたらいいな
- 位置情報と対話形式を活用したLINEチャットボットを開発し、ユーザーに適切な医療機関の情報提供と薬に関する疑問解消をサポートするアプリにチャレンジしてみたい

### **実装済みの機能**
- LINEボットと各種実装機能（医療機関or薬剤情報）を疎通
- 医療機関及び薬剤情報について、外部知識参照(RAG)の要素を取り入れ、自然言語に落とし込んで回答を生成
- 特定の話題以外は回答できない制限（ADVANCE課題）
- 裏側
    - 会話履歴のデータベースへの保存
    - ログ

### **実装予定の機能**
- ユーザの過去の対話内容をふまえた回答（DBまわり）
- DBをNosqlへチェンジしてみる（トライ案件、できれば）
- テストの実装（トライ案件、できれば）


## 使用技術

**フロントエンド: LINE Messaging API**

**バックエンド: Python / FastAPI**

**データベース: PostgreSQL**

**開発環境: Docker**

**バージョン管理: GitHub**

**外部API:  OpenAI AI ( GPT-4) , Google Maps Places API**

**その他: PmdaホームページURL**


### **各種ドキュメント**
- 開発概要、経過

<details>
<summary>開発時のメモ</summary>

### 医療機関検索機能に使用するもの（候補）

- Google Maps Places API- 位置情報から検索した近くの医療機関の情報をLLMに渡し、自然言語に組み込んで出力する
- ~~[医療保険情報取得API 取得情報一覧｜マイナポータル (myna.go.jp)](https://myna.go.jp/html/api/medicalexaminfo/infolist.html)~~
- ~~[医療機関情報販売 | まろん医療機関情報2024 (iryokikan.info)](https://www.iryokikan.info/api.html)~~  

### 薬剤検索機能

- 公開された無料APIがないため、~~スクレイピングしてきたデータを~~ PMDA（[医療用医薬品 添付文書等情報検索 | 独立行政法人 医薬品医療機器総合機構 (pmda.go.jp)](https://www.pmda.go.jp/PmdaSearch/iyakuSearch/)）を検索先として指定し、LLMに読み込ませたうえで検索させる ⇒ 出力させる
- スクレイピング禁止: [PMDA スクレイピング禁止](https://www.pmda.go.jp/searchhelp_005.html)

### 医薬品情報検索API

日本国内に限定して医療用医薬品の情報を検索できる無料のAPIは少ないですが、以下のリソースがあります：

#### 1. **厚生労働省「医薬品医療機器情報提供ホームページ」**

- **概要**: 日本の医薬品に関する情報を提供する厚生労働省の公式サイトです。APIとしては公開されていませんが、データをWebスクレイピングで取得することが可能です。
- **特徴**: 医薬品の承認情報、副作用、用法・用量など。
- **URL**: [厚生労働省 医薬品医療機器情報提供ホームページ](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000064845.html)

#### 2. **薬事日報**

- **概要**: 日本の医薬品や医療機器に関する情報を提供する薬事日報のサイトです。公式なAPIは公開されていないため、情報取得には手動でのデータ収集やスクレイピングが必要です。
- **URL**: [薬事日報](https://www.yakuji.co.jp/)

#### 3. **日本薬剤師会**

- **概要**: 日本薬剤師会が提供する医薬品に関する情報源ですが、APIは公開されていません。医薬品情報の参照はサイトを通じて行う必要があります。
- **URL**: [日本薬剤師会](https://www.nichiyaku.or.jp/)

#### 4. **医薬品情報提供サイト（例: くすりのしおり）**

- **概要**: 一部の日本の医薬品情報提供サイトでは、医薬品の詳細情報を提供しており、これらのサイトから情報を取得するための非公式なAPIが存在するかもしれません。
- **URL**: [くすりのしおり](https://www.kusuri-no-shiori.jp/)

#### 5. **日本薬局方**

- **概要**: 日本薬局方に関する情報が提供されています。公式なAPIはないものの、医薬品に関する詳細な情報を掲載している場合があります。
- **URL**: [日本薬局方](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000188410.html)

### APIの使用
これらのリソースは、公式なAPIが提供されていないため、情報を取得するためには以下の方法が考えられます：
- **スクレイピング**: サイトからデータを抽出するためのスクレイピング手法を用いる（注意点：利用規約を確認し、スクレイピングの許可があるか確認すること）。
- **手動データ収集**: APIが公開されていない場合、データを手動で収集し、自分のデータベースを作成する方法もあります。
        
### まとめ
日本国内で利用できる無料の医薬品情報APIは少なく、主に公式なサイトからデータを取得する必要あり。APIの有無や利用方法については、各公式サイトや関連機関に問い合わせることも有効。また、APIが提供されていない場合には、スクレイピングや手動収集の方法を検討。
</details>


<details>
<summary>API設計書</summary>

```jsx
{
  "openapi": "3.1.0",
  "info": {
    "title": "FastAPI",
    "version": "0.1.0"
  },
  "paths": {
    "/": {
      "get": {
        "summary": "Index",
        "operationId": "index__get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          }
        }
      }
    },
    "/callback/": {
      "post": {
        "summary": "Callback",
        "operationId": "callback_callback__post",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          }
        }
      }
    },
    "/api/conversation/": {
      "post": {
        "summary": "Create Conversation",
        "operationId": "create_conversation_api_conversation__post",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/Body_create_conversation_api_conversation__post"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/conversation/{user_id}": {
      "get": {
        "summary": "Read Conversation",
        "operationId": "read_conversation_api_conversation__user_id__get",
        "parameters": [
          {
            "name": "user_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "title": "User Id"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Body_create_conversation_api_conversation__post": {
        "properties": {
          "user_id": {
            "type": "string",
            "title": "User Id"
          },
          "user_message": {
            "type": "string",
            "title": "User Message"
          },
          "bot_response": {
            "type": "string",
            "title": "Bot Response"
          }
        },
        "type": "object",
        "required": ["user_id", "user_message", "bot_response"],
        "title": "Body_create_conversation_api_conversation__post"
      },
      "HTTPValidationError": {
        "properties": {
          "detail": {
            "items": {
              "$ref": "#/components/schemas/ValidationError"
            },
            "type": "array",
            "title": "Detail"
          }
        },
        "type": "object",
        "title": "HTTPValidationError"
      },
      "ValidationError": {
        "properties": {
          "loc": {
            "items": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "integer"
                }
              ]
            },
            "type": "array",
            "title": "Location"
          },
          "msg": {
            "type": "string",
            "title": "Message"
          },
          "type": {
            "type": "string",
            "title": "Error Type"
          }
        },
        "type": "object",
        "required": ["loc", "msg", "type"],
        "title": "ValidationError"
      }
    }
  }
}

```

</details>

<details>
<summary>RAG要素の取り込みについての考え方</summary>

### 1. 症状や位置情報からの医療機関の提案

### 1.1 現在のアプローチ

現在のアプローチでは、ユーザーの位置情報や症状に基づいて、Google Maps APIなどの外部サービスから医療機関の情報を取得し、提案することができます。これには以下のステップが含まれます：

- **位置情報の取得**: ユーザーからの位置情報を取得する。
- **医療機関の検索**: Google Maps Places APIなどを使用して、位置情報に基づいて医療機関を検索する。
- **結果の提示**: 検索結果をユーザーに提示する。

### 1.2 RAGの要素を取り入れる方法

RAGを取り入れるためには、生成モデルと情報検索の組み合わせを利用します。以下の手順で実装できます：

1. **情報検索**: Google Maps APIなどで医療機関の情報を取得します。
2. **生成モデル**: 取得した情報を元に、生成モデル（例えば、GPT-4）で自然言語での提案を生成します。
3. **対話の強化**: ユーザーの質問や追加のリクエストに応じて、生成モデルが適切な回答を生成します。

### 2. 処方された薬に関する疑問解消

### 2.1 現在のアプローチ

現在のアプローチでは、ユーザーが処方された薬について質問し、それに対する一般的な回答や情報を提供することができます。これには以下のステップが含まれます：

- **薬の情報収集**: 薬に関する一般的な情報やFAQを提供する。
- **ユーザーからの質問に対応**: 薬に関する具体的な質問に答える。

### 2.2 RAGの要素を取り入れる方法

処方された薬に関する疑問解消にRAGの要素を取り入れるには、以下の手順で実装できます：

1. **情報検索**: 薬に関するデータベースや情報源から詳細な情報を検索します（例：医薬品データベース、公開された研究論文、信頼できるウェブサイト）。
2. **生成モデル**: 検索結果を基に生成モデルがユーザーの質問に対して自然言語で回答を生成します。
3. **対話の強化**: 薬に関する追加の質問や具体的なケースに対して、生成モデルが応答を提供します。
</details>

<details>
<summary>Google Maps APIメソッドの一覧</summary>

| №  | メソッド名 | メソッド内容                                | 例                     | その他の情報                                | 今回の実装使用中かどうか                       |
|----|------------|--------------------------------------------|------------------------|---------------------------------------------|-------------------------------------------------|
| 1  | location   | 検索の中心となる位置（緯度と経度のタプル）を指定 | (35.6895, 139.6917)    | 必須パラメータ                                | 第１の対話の回答結果として使用                   |
| 2  | radius     | 検索範囲の半径をメートル単位で指定          | 1000                   | rankbyがdistanceでない場合に必須                | 第１の対話の回答結果として使用                   |
| 3  | keyword    | 任意の検索キーワードを指定                  | "hospital"             | 施設の名前やカテゴリに基づいて検索               | 第１の対話の回答結果として使用                   |
| 4  | language   | 検索結果の言語を指定                        | "ja"                   | 結果の言語設定                                  | 回答内容を日本語にするかどうかなので、毎回使用       |
| 5  | min_price  | 価格レベルの下限を指定                      | 0                      | 価格レベルは0（無料）から4（非常に高価）まで       | 対話：価格０～４を指定したら表示可能               |
| 6  | max_price  | 価格レベルの上限を指定                      | 4                      | 価格レベルは0（無料）から4（非常に高価）まで       | 対話：価格０～４を指定したら表示可能               |
| 7  | name       | 場所の名前を指定して検索                    | "General Hospital"     | 施設の名前に基づいて検索                          | 対話：具体的な施設名を指定したら表示可能           |
| 8  | open_now   | 現在営業中の施設のみを検索するかどうかを指定 | True                   | 現在営業中の施設のみを検索                         | 対話：営業中を指定したら表示可能                 |
| 9  | rankby     | 結果の並び順を指定                          | "prominence"または"distance" | distanceに設定するとradiusは指定できない        | 対話：近い順に表示させる？                        |
| 10 | type       | 検索する施設の種類を指定                    | "hospital"             | 施設の種類（例：restaurant, cafe, hospital）  | hospitalとして、結果表示を毎回使用                |

</summary>
</details>
