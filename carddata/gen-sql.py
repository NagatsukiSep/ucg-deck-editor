import json
import os


# JSONデータの読み込み
data_json = """
{
  "data": [
    {
      "id": 183,
      "section": "BP",
      "bundle_version": "01",
      "serial": "101",
      "branch": "APS",
      "number": "AP-S BP01-101",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": "2",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1543,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "石の神話",
        "ruby": "-",
        "character_name": "-",
        "effect": "[起動](ターンに1回)自分の手札にあるレベル3の 『ティガ』 1枚を公開する→DOUBLEかTRIPLEのレベル3の自分の 『ティガ』 1体の1番上のカード1枚を手札に戻し、その上に公開した 『ティガ』 1枚を登場させる。",
        "flavor_text": "-",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "NAKANO RYO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/e76484d75f97c889c10adaeaa87d4c358af295d0",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/a0ca6e273c9eb7b320896421b6ce52c4b2682b0f"
      }
    },
    {
      "id": 182,
      "section": "BP",
      "bundle_version": "01",
      "serial": "085",
      "branch": "AP20",
      "number": "AP(20/20) BP01-085",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2021,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1542,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマントリガー",
        "ruby": "-",
        "character_name": "トリガー",
        "effect": "[DBL]《このキャラの登場時》ラウンド3以下のシーン1つを捨て札にすることができる。",
        "flavor_text": "信じよう。人は誰でも、優しさひとつで生きられることを。",
        "participating_works": "ウルトラマントリガー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/1cf2e937da3c1c1b34f4388d2a1f9cdb350af8ef",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/e10af92266f5c18aec49106fa157f64b7baa1bde"
      }
    },
    {
      "id": 181,
      "section": "BP",
      "bundle_version": "01",
      "serial": "082",
      "branch": "AP19",
      "number": "AP(19/20) BP01-082",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2021,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1541,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマントリガー",
        "ruby": "-",
        "character_name": "トリガー",
        "effect": "[SIN]《このキャラの登場時》自分のデッキの上のカード3枚を公開することで、その中のウルトラヒーローカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "未来を築く希望の光。勇者の心に満ちる時──！",
        "participating_works": "ウルトラマントリガー",
        "participating_works_url": null,
        "type_name": "マルチタイプ",
        "illustrator_name": "SENNSU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/5069dc4b3db090094c7cad1e0421ee0bb4e79d3b",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/8af562a0f463277e34c99193adb26e55df7b0825"
      }
    },
    {
      "id": 180,
      "section": "BP",
      "bundle_version": "01",
      "serial": "076",
      "branch": "AP18",
      "number": "AP(18/20) BP01-076",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 9000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1540,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "[SIN][DBL]《このキャラの登場時》自分のデッキの上のカード5枚を公開することで、その中のシーンカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "心震わす仲間がいる。光の乱舞に絆が閃く。",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/a809a31919fb79c36d201a2de853880a2b7e16a0",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/b74c6421a9871be87fc0f042c1de9ce854be3732"
      }
    },
    {
      "id": 179,
      "section": "BP",
      "bundle_version": "01",
      "serial": "073",
      "branch": "AP17",
      "number": "AP(17/20) BP01-073",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1539,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "[SIN]《このキャラの登場時》自分は2枚ドローできる。この効果でドローした時、自分の手札1枚をデッキの下に戻す。",
        "flavor_text": "勇者の魂が受け継ぐ、宇宙拳法の心・技・体。",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "アルファエッジ",
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/a23c4adaf16e9fcf5037b491814af1733d51258f",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/b25dddf42a28eb6947a4b1ff93d2540533b9f240"
      }
    },
    {
      "id": 178,
      "section": "BP",
      "bundle_version": "01",
      "serial": "067",
      "branch": "AP16",
      "number": "AP(16/20) BP01-067",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 10000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1538,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "[DBL]《このキャラの登場時》バトル相手のキャラがDOUBLEなら、このターンのこのキャラのバトルを引き分けにすることができる。",
        "flavor_text": "明日を生きていく勇気──この一撃にこめて！",
        "participating_works": "ウルトラマンジード",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/8d1aab02e7ff30c72439be0cd06c8f6479db8cd6",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/f79fc9955790ccb911cb26845b1640602756e8d1"
      }
    },
    {
      "id": 177,
      "section": "BP",
      "bundle_version": "01",
      "serial": "064",
      "branch": "AP15",
      "number": "AP(15/20) BP01-064",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1537,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "[SIN]《このキャラの登場時》自分のデッキの上のカード3枚を公開することで、その中のウルトラヒーローカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "力が正義なのか？正義が力なのか？この命すべてを懸けて、見届けてみせる！",
        "participating_works": "ウルトラマンジード",
        "participating_works_url": null,
        "type_name": "プリミティブ",
        "illustrator_name": "Kazumasa Yasukuni",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/5e6e062aff715f8fdbe209420fd5db3016318735",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/c09f666b5850c9f7ec111068ccfed08c54964a73"
      }
    },
    {
      "id": 176,
      "section": "BP",
      "bundle_version": "01",
      "serial": "061",
      "branch": "AP14",
      "number": "AP(14/20) BP01-061",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 13000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1536,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【剛力】 か 【武装】 の間、BPが1グレードアップする。",
        "flavor_text": "自らの過ちを全身に受け止め、過酷な特訓に耐え抜き──そして、今！",
        "participating_works": "大怪獣バトル ウルトラ銀河伝説 THE MOVIE",
        "participating_works_url": null,
        "type_name": "ゼロスラッガー",
        "illustrator_name": "JUN YAMAGUCHI",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/24212f01d13e19f105f7f8b4d2dfc49ae676f848",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/85aefb89f6a6e07865ac5a4e8d27b89fbb339541"
      }
    },
    {
      "id": 175,
      "section": "BP",
      "bundle_version": "01",
      "serial": "055",
      "branch": "AP13",
      "number": "AP(13/20) BP01-055",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1535,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "[SIN]《このキャラの登場時》自分は2枚ドローできる。この効果でドローした時、自分の手札1枚をデッキの下に戻す。",
        "flavor_text": "宇宙拳法が俺を強くする。砕くは平和を乱す者！",
        "participating_works": "大怪獣バトル ウルトラ銀河伝説 THE MOVIE",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/79cb9356702865e15e00c4dc3cfd6b5cfab6abe6",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/54592c40acfa1caad4c3d8694459f94cc7d1f4b2"
      }
    },
    {
      "id": 174,
      "section": "BP",
      "bundle_version": "01",
      "serial": "049",
      "branch": "AP12",
      "number": "AP(12/20) BP01-049",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 10000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1534,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "[DBL]《このキャラの登場時》このキャラ以外のDOUBLEかTRIPLEの自分のウルトラヒーロー1体の1番上のカード1枚を手札に戻すことで、自分のウルトラヒーロー1体を、このターンの間、BP+1000できる。",
        "flavor_text": "地球の大地よ空よ、永遠に。",
        "participating_works": "ウルトラマンガイア",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "F.M.U",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/0a4a9f142331d8061d884dad68641ecd5ce82345",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/a37ce488d2ef3a4902f24aa1c988d56e654b635d"
      }
    },
    {
      "id": 173,
      "section": "BP",
      "bundle_version": "01",
      "serial": "046",
      "branch": "AP11",
      "number": "AP(11/20) BP01-046",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1533,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "[SIN]《このキャラの登場時》自分のデッキの上のカード3枚を公開することで、その中のウルトラヒーローカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "追い続けよう、地球の光が託した使命。",
        "participating_works": "ウルトラマンガイア",
        "participating_works_url": null,
        "type_name": "V1",
        "illustrator_name": "KISUKE",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/e35aaace466391b4fb85ffd5d048bf66241112dc",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/4158081a3d99b484bbc09a03d35c7c61dffd7cba"
      }
    },
    {
      "id": 172,
      "section": "BP",
      "bundle_version": "01",
      "serial": "040",
      "branch": "AP10",
      "number": "AP(10/20) BP01-040",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": 15000,
      "battle_power_ex": null,
      "publication_year": 2023,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1532,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンブレーザー",
        "ruby": "-",
        "character_name": "ブレーザー",
        "effect": "[DBL]《このキャラの登場時》バトル相手のキャラ1体を、このターンの間、BP-2000できる。(※BPは0未満にはならない)",
        "flavor_text": "昨日を積み重ねてきた者だけに訪れる秘めた確信。──勝負は一瞬に決まる。",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "toriyufu",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/a1ab8c54fa1f0c75b4016c8547a0b858a819d775",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/511cfeee33339cf6f3098a59deffb264c10eaaa1"
      }
    },
    {
      "id": 171,
      "section": "BP",
      "bundle_version": "01",
      "serial": "037",
      "branch": "AP09",
      "number": "AP(09/20) BP01-037",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2023,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1531,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンブレーザー",
        "ruby": "-",
        "character_name": "ブレーザー",
        "effect": "[SIN]《このキャラの登場時》自分は2枚ドローできる。この効果でドローした時、自分の手札1枚をデッキの下に戻す。",
        "flavor_text": "掴め、その手を。繋げ、絆を。未来へ続く光に終わりは無い。",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "Kazumasa Yasukuni",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/1d6b1af19ad8fb89d2e2698fdd818991bf91b3b2",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/5779be9d464331877b2496177663868fcff2270d"
      }
    },
    {
      "id": 170,
      "section": "BP",
      "bundle_version": "01",
      "serial": "031",
      "branch": "AP08",
      "number": "AP(08/20) BP01-031",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2022,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1530,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンデッカー",
        "ruby": "-",
        "character_name": "デッカー",
        "effect": "[DBL]《このキャラの登場時》このキャラと、このキャラの左隣か右隣にいるウルトラヒーロー1体の場所を入れ替えることができる。",
        "flavor_text": "──それでも進む道は自分が決める。",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "SENNSU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/47ccb1fa290ddcddda30245c18bacec83e87a82a",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/3e79205cc120d7c8be6f9e27f56a0e12158af2ba"
      }
    },
    {
      "id": 169,
      "section": "BP",
      "bundle_version": "01",
      "serial": "028",
      "branch": "AP07",
      "number": "AP(07/20) BP01-028",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2022,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1529,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンデッカー",
        "ruby": "-",
        "character_name": "デッカー",
        "effect": "[SIN]《このキャラの登場時》自分は2枚ドローできる。この効果でドローした時、自分の手札1枚をデッキの下に戻す。",
        "flavor_text": "明日がまだ見えなくても精一杯生きよう。僕は君の手を離さない。",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "フラッシュタイプ",
        "illustrator_name": "HUJIWARA HISASHI",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/84c5d8937f2f3cb456cd1f329e3f27994d675c1c",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/6b686b8c8fa6751df85ac8fcb8d29c5521ed3cef"
      }
    },
    {
      "id": 168,
      "section": "BP",
      "bundle_version": "01",
      "serial": "022",
      "branch": "AP06",
      "number": "AP(06/20) BP01-022",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 9000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2006,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1528,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンメビウス",
        "ruby": "-",
        "character_name": "メビウス",
        "effect": "[DBL]《このキャラの登場時》自分のデッキの上のカード2枚を捨て札にすることで、自分の捨て札エリアにあるシーンカードか、 『メビウス』 1枚を手札に戻すことができる。",
        "flavor_text": "本当に大切なものは、何なのか。仲間たちと探そう、日々の未来に向かって。",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "Kazumasa Yasukuni",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/fe71246a35ed622a6ffc40d0573cb427c6e539b3",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/2cd323770f7b69b154e0f9713bf119547f1cb9c8"
      }
    },
    {
      "id": 167,
      "section": "BP",
      "bundle_version": "01",
      "serial": "019",
      "branch": "AP05",
      "number": "AP(05/20) BP01-019",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2006,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1527,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンメビウス",
        "ruby": "-",
        "character_name": "メビウス",
        "effect": "[SIN]《このキャラの登場時》自分のデッキの上のカード3枚を公開することで、その中のウルトラヒーローカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "炎のエンブレムは絆の証。心に熱を通わせ、光に希望を溢れさせていく。",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/5ff955ed5ab286da9dc74a8940a0dbe9370fd5b7",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/b3351ed365150e4d06abc2b7449647de24728031"
      }
    },
    {
      "id": 166,
      "section": "BP",
      "bundle_version": "01",
      "serial": "016",
      "branch": "SSSP02",
      "number": "SSSP(02/02) BP01-016",
      "rarity": {
        "value": "200_sssp",
        "description": "SSSP"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": 18000,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1526,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "[DBL][TRP]《このキャラの登場時》自分の手札にあるラウンド1以下のシーンカード1枚を公開することで、シーン1つを捨て札にし、公開したシーンカード1枚をシーンエリアに出すことができる。",
        "flavor_text": "君を照らす巨人の光。君が目指す、新たな未来を照らし出す希望の光。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "Masayuki Gotoh",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/4ef89eb6c03ec4ad5fd29b6fa0e452425a3350e6",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/0467ccbb09232c79d94b4a9e86625345270d408e"
      }
    },
    {
      "id": 165,
      "section": "BP",
      "bundle_version": "01",
      "serial": "016",
      "branch": "UR02",
      "number": "UR(02/02) BP01-016",
      "rarity": {
        "value": "100_ur",
        "description": "UR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": 18000,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1525,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "[DBL][TRP]《このキャラの登場時》自分の手札にあるラウンド1以下のシーンカード1枚を公開することで、シーン1つを捨て札にし、公開したシーンカード1枚をシーンエリアに出すことができる。",
        "flavor_text": "あの巨人も君と同じ。大切なものを見つめている。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "Masayuki Gotoh",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/e096358a862acd3759b0cc1d111f109648a78cfd",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/0ff29533f472648a6f499c56392a0a7871eed236"
      }
    },
    {
      "id": 164,
      "section": "BP",
      "bundle_version": "01",
      "serial": "013",
      "branch": "AP04",
      "number": "AP(04/20) BP01-013",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 9000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1524,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "[SIN][DBL]《このキャラの登場時》自分のデッキの上のカード5枚を公開することで、その中のシーンカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "吹き荒れる嵐の中でも、心ひとつで感じ取れるさ。明日へと進む足音だけは。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "toriyufu",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/0314d19dee40c4daa7a1fbae83bb756332849c66",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/7ee3b7d9342eb352f7c608d1a7c050c82df20152"
      }
    },
    {
      "id": 163,
      "section": "BP",
      "bundle_version": "01",
      "serial": "010",
      "branch": "AP03",
      "number": "AP(03/20) BP01-010",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1523,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "[SIN]《このキャラの登場時》自分は2枚ドローできる。この効果でドローした時、自分の手札1枚をデッキの下に戻す。",
        "flavor_text": "君の夢は育っていく。昨日から今日へ。今日から明日へと続く架け橋になる。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "Akihiro MIYANO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/c5c159cfc8b9670f0ce78fa6ab037b031a0f0fd8",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/e9f667fbcbc3970b80f38c7669a02b73ae939e2e"
      }
    },
    {
      "id": 162,
      "section": "BP",
      "bundle_version": "01",
      "serial": "007",
      "branch": "SSSP01",
      "number": "SSSP(01/02) BP01-007",
      "rarity": {
        "value": "200_sssp",
        "description": "SSSP"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 13000,
      "battle_power_3": 18000,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1522,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "[TRP]《このキャラの登場時》このキャラと、他の自分のウルトラヒーロー1体の場所を入れ替えることができる。",
        "flavor_text": "覆せ悪魔の審判。闇と邪心を切り裂く時、僕らが信じる未来はそこに。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": "ゼペリオン光線",
        "illustrator_name": "Hiroshi Maruyama",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/3a8a3dc0bdc6f849c5002eb19415e68d5ddfb781",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/379913d828330fd2c1a7e291f09cace318d8b2a7"
      }
    },
    {
      "id": 161,
      "section": "BP",
      "bundle_version": "01",
      "serial": "007",
      "branch": "UR01",
      "number": "UR(01/02) BP01-007",
      "rarity": {
        "value": "100_ur",
        "description": "UR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 13000,
      "battle_power_3": 18000,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1521,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "[TRP]《このキャラの登場時》このキャラと、他の自分のウルトラヒーロー1体の場所を入れ替えることができる。",
        "flavor_text": "君は見たか、眩い光を。君は聞いたか、凄まじい光が駆け抜ける音を。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": "ゼペリオン光線",
        "illustrator_name": "Hiroshi Maruyama",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/f887e60828537a0ba94746ddd226ba05ba91d28c",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/82d8d9712048f5d308be97e0f35cc07a091194bd"
      }
    },
    {
      "id": 160,
      "section": "BP",
      "bundle_version": "01",
      "serial": "004",
      "branch": "AP02",
      "number": "AP(02/20) BP01-004",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 9000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1520,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "[SIN][DBL]《このキャラの登場時》自分のデッキの上のカード5枚を公開することで、その中のシーンカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "夢よりも鮮やかな光。希望よりも眩しい光。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "YAMAGUCHI BIRU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/38283865c179eefbc535a6e7101f44e7a6c91b6a",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/aa9d1588a03a18a04aed88c2cfa27889251ba6f0"
      }
    },
    {
      "id": 159,
      "section": "BP",
      "bundle_version": "01",
      "serial": "001",
      "branch": "AP01",
      "number": "AP(01/20) BP01-001",
      "rarity": {
        "value": "350_ap",
        "description": "AP"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 1519,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "[SIN]《このキャラの登場時》自分のデッキの上のカード3枚を公開することで、その中のウルトラヒーローカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "光が見えるか。君を呼ぶ声が聞こえるか。大切なものはすべてそこにある。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "JUN YAMAGUCHI",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/1f0b3d51883af924e6a1d22e32dc852d8652f3dd",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/1db5f512a712cafd310a61af3ebd37940d8f2fcf"
      }
    },
    {
      "id": 40,
      "section": "BP",
      "bundle_version": "01",
      "serial": "043",
      "branch": "SP05",
      "number": "SP(05/05)BP01-043",
      "rarity": {
        "value": "300_sp",
        "description": "SP"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 12000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2023,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 334,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンブレーザー",
        "ruby": "-",
        "character_name": "ブレーザー",
        "effect": "[TRP]《このキャラの登場時》自分のデッキの上のカード3枚を公開し、好きな順番でデッキの上に戻すことで、バトル相手のキャラ1体を、このターンの間、BP-3000できる。(※BPは0未満にはならない)",
        "flavor_text": "光を構えろ。大地の鼓動を感じろ。君が戦うべき時は、この瞬間に迫っている。",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": "スパイラルバレード",
        "illustrator_name": "As'Maria",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/3a9ae84c0064fe5de40db3314ee6d4ef6a05480f",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/d78314cb465e49538fc3345747e9c347df2ae4c2"
      }
    },
    {
      "id": 32,
      "section": "BP",
      "bundle_version": "01",
      "serial": "034",
      "branch": "SP04",
      "number": "SP(04/05)BP01-034",
      "rarity": {
        "value": "300_sp",
        "description": "SP"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 12000,
      "battle_power_3": 18000,
      "battle_power_ex": null,
      "publication_year": 2022,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 326,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンデッカー",
        "ruby": "-",
        "character_name": "デッカー",
        "effect": "[DBL][TRP]SINGLEの自分の 『デッカー』 と 『トリガー』 すべては、 このキャラ以外のTRIPLEの自分のウルトラヒーローがいる間、BPが1グレードアップする。この効果は重複しない。",
        "flavor_text": "たったひとつの小さな出逢い。それが明日への宝物。",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "フラッシュタイプ",
        "illustrator_name": "As'Maria",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/9310c4fe9d2152480d71e9a212b5baffc2b4eaae",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/f66e2b2bc063b0c718dbc4085e659cc672ede1d5"
      }
    },
    {
      "id": 29,
      "section": "BP",
      "bundle_version": "01",
      "serial": "025",
      "branch": "SP03",
      "number": "SP(03/05)BP01-025",
      "rarity": {
        "value": "300_sp",
        "description": "SP"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 12000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2006,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 323,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンメビウス",
        "ruby": "-",
        "character_name": "メビウス",
        "effect": "[DBL][TRP][起動](ターンに1回)自分の手札1枚を捨て札にする→自分の 『メビウス』 1体は、このターンの間、BPが1グレードアップする。",
        "flavor_text": "この力で誰かを救おう。君の残した思いは、今も僕に勇気をくれる。",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": "メビュームナイトブレード",
        "illustrator_name": "As'Maria",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/7867eae4c5f28bf50a60c5e957c0f55d296e385e",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/8194a908c0b6910e4d38c2adbdebf8f727ae1b53"
      }
    },
    {
      "id": 26,
      "section": "BP",
      "bundle_version": "01",
      "serial": "016",
      "branch": "SP02",
      "number": "SP(02/05)BP01-016",
      "rarity": {
        "value": "300_sp",
        "description": "SP"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": 18000,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 320,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "[DBL][TRP]《このキャラの登場時》自分の手札にあるラウンド1以下のシーンカード1枚を公開することで、シーン1つを捨て札にし、公開したシーンカード1枚をシーンエリアに出すことができる。",
        "flavor_text": "君にかわってウルトラマンが闇を断つ。だから全てを諦めるな。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "As'Maria",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/574491b9ff04b18e336abf3b41ce8f17aa5edc13",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/b1aa8d9f60005245d79e88bc3519436e4fa0f1d7"
      }
    },
    {
      "id": 21,
      "section": "BP",
      "bundle_version": "01",
      "serial": "007",
      "branch": "SP01",
      "number": "SP(01/05)BP01-007",
      "rarity": {
        "value": "300_sp",
        "description": "SP"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 13000,
      "battle_power_3": 18000,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 315,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "[TRP]《このキャラの登場時》このキャラと、他の自分のウルトラヒーロー1体の場所を入れ替えることができる。",
        "flavor_text": "聞こえるか、闇を切り裂く光の轟き。聞こえるだろう、僕らの声が。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": "ゼペリオン光線",
        "illustrator_name": "As'Maria",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/980ea17eca85b47211564800e9cc90db8fff0bc6",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/ca76d4249cd2ee9a17fa9b299a81de5d20c69a8f"
      }
    },
    {
      "id": 158,
      "section": "BP",
      "bundle_version": "01",
      "serial": "110",
      "branch": null,
      "number": "BP01-110",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "2",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 940,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "笑顔のために",
        "ruby": "-",
        "character_name": "-",
        "effect": "《このシーンが出た時》自分の 『トリガー』 がいるなら、自分は1枚ドローできる。この効果でドローした時、自分の手札1枚を捨て札にする。",
        "flavor_text": "-",
        "participating_works": "ウルトラマントリガー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/67ba3561a89bce0b32951d77e2863dca47578486",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/1e28ecfd17a811a5f9772cb3195b974843f3acc6"
      }
    },
    {
      "id": 157,
      "section": "BP",
      "bundle_version": "01",
      "serial": "109",
      "branch": null,
      "number": "BP01-109",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "1",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 939,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ご唱和ください、我の名を!",
        "ruby": "-",
        "character_name": "-",
        "effect": "《このシーンが出た時》自分の 『ゼット』 がいるなら、自分の捨て札エリアにある「ご唱和ください、我の名を!」以外のシーンカード2枚までを手札に戻すことができる。",
        "flavor_text": "-",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/a7ec96c8f92590aa4de0742b71b7e978e4cfb6c6",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/7020b724587a63921a58a450952afedfaddacbba"
      }
    },
    {
      "id": 156,
      "section": "BP",
      "bundle_version": "01",
      "serial": "108",
      "branch": null,
      "number": "BP01-108",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "4",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 938,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "僕が僕であること",
        "ruby": "-",
        "character_name": "-",
        "effect": "[起動](ターンに1回)このシーンを捨て札にする→自分の 『ジード』 すべては、このターンの間、BPが1グレードアップする。",
        "flavor_text": "-",
        "participating_works": "ウルトラマンジード",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/ac904851a2a9ffec7115884e0a2034c6a2693db3",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/b7c8fb40106612d7d4a123ca56ee881a42ce0fb4"
      }
    },
    {
      "id": 155,
      "section": "BP",
      "bundle_version": "01",
      "serial": "104",
      "branch": null,
      "number": "BP01-104",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": "3",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 937,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "光と闇、ふたたび",
        "ruby": "-",
        "character_name": "-",
        "effect": "[起動](ターンに1回)自分の手札1枚を捨て札にする→自分の 『デッカー』 すべてを、このターンの間、BP+1000する。",
        "flavor_text": "-",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/58b967e4c3aa5300fe7b90a441bdbb62a162228c",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/859b6c4edac9ce39725db43175949104992229f1"
      }
    },
    {
      "id": 154,
      "section": "BP",
      "bundle_version": "01",
      "serial": "103",
      "branch": null,
      "number": "BP01-103",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": "2",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 936,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "激闘の覇者",
        "ruby": "-",
        "character_name": "-",
        "effect": "[起動](ターンに1回)自分の捨て札エリアにあるレベル1と2と3の 『メビウス』 を、それぞれ1枚ずつ選択する→DOUBLEかTRIPLEの自分の 『メビウス』 1体をゲームから取り除き、その 『メビウス』 がいた場所に、選択したそれぞれの 『メビウス』 をTRIPLEの状態で登場させる。",
        "flavor_text": "-",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/f6d4fd2887f78d78a9308f63aa54b30ab7d287b2",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/97bbf2caa7f423532341052b5be10aa9209f0b7b"
      }
    },
    {
      "id": 153,
      "section": "BP",
      "bundle_version": "01",
      "serial": "101",
      "branch": null,
      "number": "BP01-101",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": "2",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 935,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "石の神話",
        "ruby": "-",
        "character_name": "-",
        "effect": "[起動](ターンに1回)自分の手札にあるレベル3の 『ティガ』 1枚を公開する→DOUBLEかTRIPLEのレベル3の自分の 『ティガ』 1体の1番上のカード1枚を手札に戻し、その上に公開した 『ティガ』 1枚を登場させる。",
        "flavor_text": "-",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/210ede5ce60006b2b18cd3552e61ecf22c42de03",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/1a47a9ceb0c1cd4fbd41b45fab075abad1a995e1"
      }
    },
    {
      "id": 152,
      "section": "BP",
      "bundle_version": "01",
      "serial": "100",
      "branch": null,
      "number": "BP01-100",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 10000,
      "battle_power_2": 17000,
      "battle_power_3": null,
      "battle_power_ex": 8000,
      "publication_year": 2021,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 934,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "超古代闇怪獣",
        "ruby": "ちょうこだいやみかいじゅう",
        "character_name": "ゴルバー",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【敏速】 の間、EXTRAのBPになる。",
        "flavor_text": "“大地を揺るがす怪獣” と、“空を切り裂く怪獣” が融合されているのだろうか－－－。",
        "participating_works": "ウルトラマントリガー",
        "participating_works_url": null,
        "type_name": "ゴルバー",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/aaf55883de9a6f35ff66078fa86422e64bcb5b7f",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/12446e3e37c4110ec2bb2a0992930f4896dda6cd"
      }
    },
    {
      "id": 151,
      "section": "BP",
      "bundle_version": "01",
      "serial": "099",
      "branch": null,
      "number": "BP01-099",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 10000,
      "battle_power_2": 17000,
      "battle_power_3": null,
      "battle_power_ex": 8000,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 933,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "凶暴宇宙鮫",
        "ruby": "きょうぼううちゅうざめ",
        "character_name": "ゲネガーグ",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【剛力】 の間、EXTRAのBPになる。",
        "flavor_text": "正も邪も根刮ぎ喰らう。宇宙の未曾有の大悪食。",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ゲネガーグ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/ec330932cf82dadeec298cb80b54d2a294d63289",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/41a9bdb8997dfaa458e42da106f04419315af3f6"
      }
    },
    {
      "id": 150,
      "section": "BP",
      "bundle_version": "01",
      "serial": "098",
      "branch": null,
      "number": "BP01-098",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 10000,
      "battle_power_2": 16000,
      "battle_power_3": null,
      "battle_power_ex": 8000,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 932,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ベリアル融合獣",
        "ruby": "ゆうごうじゅう",
        "character_name": "サンダーキラー",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【武装】 の間、EXTRAのBPになる。",
        "flavor_text": "それはエースキラーの鎧を纏ったエレキングか？怪獣カプセルの融合が生んだ驚異の難敵。",
        "participating_works": "ウルトラマンジード",
        "participating_works_url": null,
        "type_name": "サンダーキラー",
        "illustrator_name": "gozz",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/39a6666aaf77be3e6180c43d41d3d5be113f0e79",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/ba09448df56979fec549506e2f37ed65346ecab2"
      }
    },
    {
      "id": 149,
      "section": "BP",
      "bundle_version": "01",
      "serial": "097",
      "branch": null,
      "number": "BP01-097",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 9000,
      "battle_power_2": 15000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2010,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 931,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ダークロプスゼロ",
        "ruby": "-",
        "character_name": "ダークロプスゼロ",
        "effect": "[SIN]《このキャラの登場時》ラウンド2以下の相手のシーン1つを捨て札にすることができる。",
        "flavor_text": "不敵なモノ・アイが、ただひとつの標的を映し出す。",
        "participating_works": "ウルトラ銀河伝説外伝 ウルトラマンゼロVSダークロプスゼロ",
        "participating_works_url": null,
        "type_name": "ダークロプスゼロ",
        "illustrator_name": "gozz",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/9900adfb29f124c51179a77461aa3b817976dca9",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/7219b5872ebe5d43b3c68c2a05a5ef6a0f6f6d53"
      }
    },
    {
      "id": 148,
      "section": "BP",
      "bundle_version": "01",
      "serial": "096",
      "branch": null,
      "number": "BP01-096",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 10000,
      "battle_power_2": 17000,
      "battle_power_3": null,
      "battle_power_ex": 8000,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 930,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "宇宙戦闘獣",
        "ruby": "うちゅうせんとうじゅう",
        "character_name": "コッヴ",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【基本】 の間、EXTRAのBPになる。",
        "flavor_text": "いつの日かと怖れていた破滅の災い、降臨す。",
        "participating_works": "ウルトラマンガイア",
        "participating_works_url": null,
        "type_name": "コッヴ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/99a6eca98c42ef497b5789de0cc32f5e2347785d",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/16c8dfc13798dcb64dc3852ddebc8f3bad6576b1"
      }
    },
    {
      "id": 147,
      "section": "BP",
      "bundle_version": "01",
      "serial": "095",
      "branch": null,
      "number": "BP01-095",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 11000,
      "battle_power_2": 16000,
      "battle_power_3": null,
      "battle_power_ex": 8000,
      "publication_year": 2023,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 929,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "宇宙甲殻怪獣",
        "ruby": "うちゅうこうかくかいじゅう",
        "character_name": "バザンガ",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【基本】 の間、EXTRAのBPになる。",
        "flavor_text": "宇宙からの謎多き破壊者・飛来！夜の街に咆哮を轟かす。",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": "バザンガ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/3e9a286c449629eddb89c1b8e5e536d3af4dff1c",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/ee192b8a1c6a577f3f5c2cb7156a892666987cf2"
      }
    },
    {
      "id": 146,
      "section": "BP",
      "bundle_version": "01",
      "serial": "093",
      "branch": null,
      "number": "BP01-093",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 10000,
      "battle_power_2": 15000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2006,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 928,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "宇宙斬鉄怪獣",
        "ruby": "うちゅうざんてつかいじゅう",
        "character_name": "ディノゾール",
        "effect": "[SIN]このキャラは、バトル相手のキャラのTYPEが 【武装】 の間、BPが1グレードアップする。",
        "flavor_text": "斬る！超高速の舌が走るとき、すべては微塵と消える！",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": "ディノゾール",
        "illustrator_name": "gozz",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/41d67abf6b861a1b980dd103efabcd27703052af",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/2dbc770564f86bf712de9c7881edd70c50b96811"
      }
    },
    {
      "id": 145,
      "section": "BP",
      "bundle_version": "01",
      "serial": "092",
      "branch": null,
      "number": "BP01-092",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 11000,
      "battle_power_2": 16000,
      "battle_power_3": null,
      "battle_power_ex": 7000,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 927,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "鎧甲殻獣",
        "ruby": "よろいこうかくじゅう",
        "character_name": "シャゴン",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【基本】 の間、EXTRAのBPになる。",
        "flavor_text": "閃光・電撃・強酸──脅威の武器に堅牢な防御をあわせ持つ。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": "シャゴン",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/faf542636e651f6a919f78e7ebe3064da6b89b7d",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/f8710299249fa86a34d95895346c7cebf4064a10"
      }
    },
    {
      "id": 144,
      "section": "BP",
      "bundle_version": "01",
      "serial": "090",
      "branch": null,
      "number": "BP01-090",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 14000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 2021,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 926,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマントリガー",
        "ruby": "-",
        "character_name": "トリガー",
        "effect": "-",
        "flavor_text": "天空を駆ける高速の光！熱き思いをこの一閃に懸ける！",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "ウルトラデュアルソード",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/c95c62ee9c7592a652031e4f6154162eebe9ede5",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/d62d0135fde624c75d7c8d9dca55659c24e83a0b"
      }
    },
    {
      "id": 143,
      "section": "BP",
      "bundle_version": "01",
      "serial": "089",
      "branch": null,
      "number": "BP01-089",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 12000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2021,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 925,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマントリガー",
        "ruby": "-",
        "character_name": "トリガー",
        "effect": "[DBL][TRP]《このキャラの登場時》このキャラの左隣か右隣のキャラ1体を、このターンの間、BP+1000できる。",
        "flavor_text": "勝利を掴む剛力の光！届け宇宙へ。遥かな願いを乗せて。",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "ウルトラデュアルソード",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/e47dde34c9ee74f33ef063187f1ed0f77a21f445",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/05ce3785ca50a7c57e465bd8bfb942a4e8cf22fd"
      }
    },
    {
      "id": 142,
      "section": "BP",
      "bundle_version": "01",
      "serial": "088",
      "branch": null,
      "number": "BP01-088",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 13000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 2021,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 924,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマントリガー",
        "ruby": "-",
        "character_name": "トリガー",
        "effect": "[TRP]《このキャラの登場時》自分のデッキの上のカード5枚を公開することで、その中のカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "一緒に歩もう。すべてが笑顔になれる、世界を信じて。",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "ウルトラデュアルソード",
        "illustrator_name": "Kazumasa Yasukuni",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/50093ce9f33b5dea48bc3351adb250e4b830569f",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/bcdcb5f2744ca7cec7887654d2bdeda9468cfe1c"
      }
    },
    {
      "id": 141,
      "section": "BP",
      "bundle_version": "01",
      "serial": "087",
      "branch": null,
      "number": "BP01-087",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 10000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2021,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 923,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマントリガー",
        "ruby": "-",
        "character_name": "トリガー",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【武装】 の間、BPが1グレードアップする。",
        "flavor_text": "どこまでも続く空を突き抜け、どこまでも願いは届くと信じて。",
        "participating_works": "ウルトラマントリガー",
        "participating_works_url": null,
        "type_name": "スカイタイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/3edbe239e0668783113ed19aacb0f40300b67379",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/5fc46198111f2f5c6a7aba122c7454199f5a5e28"
      }
    },
    {
      "id": 140,
      "section": "BP",
      "bundle_version": "01",
      "serial": "086",
      "branch": null,
      "number": "BP01-086",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2021,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 922,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマントリガー",
        "ruby": "-",
        "character_name": "トリガー",
        "effect": "-",
        "flavor_text": "燃える闘志。目覚める心。自分の殻をうち破れ！",
        "participating_works": "ウルトラマントリガー",
        "participating_works_url": null,
        "type_name": "パワータイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/8f3910df20b5ddc46066fe3b5a5489cc64b56a56",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/8247e8672b521885c6e9574bf8add45a64aa2ed5"
      }
    },
    {
      "id": 139,
      "section": "BP",
      "bundle_version": "01",
      "serial": "084",
      "branch": null,
      "number": "BP01-084",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2021,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 921,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマントリガー",
        "ruby": "-",
        "character_name": "トリガー",
        "effect": "-",
        "flavor_text": "大きくてもいい。小さくてもいい。心から愛する花を咲かせよう。",
        "participating_works": "ウルトラマントリガー",
        "participating_works_url": null,
        "type_name": "サークルアームズ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/f40a88af2538080f3082f39f688a3b06891c5a81",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/6e6a98ca758dcc8353cceee20e0ab8185fede113"
      }
    },
    {
      "id": 138,
      "section": "BP",
      "bundle_version": "01",
      "serial": "083",
      "branch": null,
      "number": "BP01-083",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2021,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 920,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマントリガー",
        "ruby": "-",
        "character_name": "トリガー",
        "effect": "-",
        "flavor_text": "苦しい時、悲しい時の辛さに勝るもの──答えを出すのは自分自身。",
        "participating_works": "ウルトラマントリガー",
        "participating_works_url": null,
        "type_name": "マルチタイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/76bdb090e9b806669e2db07dbffbfba8c1136c32",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/f1aa22eadb277759abc1eea6b20f1d1957b36baa"
      }
    },
    {
      "id": 137,
      "section": "BP",
      "bundle_version": "01",
      "serial": "081",
      "branch": null,
      "number": "BP01-081",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 14000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 919,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "-",
        "flavor_text": "輝けるウルトラマンティガ・ダイナ・ガイアの力をひとつに。ウルトラフュージョン！",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ガンマフューチャー",
        "illustrator_name": "Kazumasa Yasukuni",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/4f17adf732d67787f77878cd07e118fe5c06dcd2",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/c06f6b88788774974a628794c602af8426979dda"
      }
    },
    {
      "id": 136,
      "section": "BP",
      "bundle_version": "01",
      "serial": "080",
      "branch": null,
      "number": "BP01-080",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 9000,
      "battle_power_2": 13000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 918,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "-",
        "flavor_text": "真っ赤に燃える、勇気の力。ウルトラマン・A・タロウの力を得て、熱き拳が唸りをあげる！",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ベータスマッシュ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/d47614a51b7028678aa7dbd8f49b991dd66ddba3",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/83948cdede9dfd4213c8b7d0709021f1848835ed"
      }
    },
    {
      "id": 135,
      "section": "BP",
      "bundle_version": "01",
      "serial": "079",
      "branch": null,
      "number": "BP01-079",
      "rarity": {
        "value": "500_rr",
        "description": "RR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": 15000,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 917,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "[SIN][DBL][TRP]《このキャラの登場時》自分の手札にあるシーンカード1枚を捨て札にすることで、このキャラがSINGLEなら1枚、DOUBLEなら2枚、TRIPLEなら3枚、自分はドローできる。",
        "flavor_text": "放て斬撃！ウルトラマンジャック、ゾフィー、ウルトラの父の力をひとつに合わせて！",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "M78流・竜巻閃光斬",
        "illustrator_name": "YAMAGUCHI BIRU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/82515f451368aea20bb75a34114676423dc01404",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/9eca59fac1c0787e2595f83b00d6383e57266cff"
      }
    },
    {
      "id": 134,
      "section": "BP",
      "bundle_version": "01",
      "serial": "078",
      "branch": null,
      "number": "BP01-078",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 10000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 916,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "-",
        "flavor_text": "全力集中せよ、五感を研ぎ澄ませ。狙うはひとつ、邪神の邪心！",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ゼットランスアロー",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/19ab4d7960b1af6a66337181a848470206a5a4d4",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/3aee7cdd789ace41f3b3f154696735e4c35fce72"
      }
    },
    {
      "id": 133,
      "section": "BP",
      "bundle_version": "01",
      "serial": "077",
      "branch": null,
      "number": "BP01-077",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 915,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "-",
        "flavor_text": "この手に響く、数えきれない星の彼方からのエールが、最大最強の糧になる！",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ウルトラゼットライザー",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/e7713c3faa41f3e0130232381937c9eadce8b54b",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/f0fe62dd33669b8ee5cee632b9e5d24008550d06"
      }
    },
    {
      "id": 132,
      "section": "BP",
      "bundle_version": "01",
      "serial": "075",
      "branch": null,
      "number": "BP01-075",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 914,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "-",
        "flavor_text": "対話って難しい。けれども対話がある限り、いつでも君と繋がれる。",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "オリジナル",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/de171dee2be19c878150243413c083b209771d75",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/20f4ca8e1ad9d47ed8a163206ef50fecc0aa0351"
      }
    },
    {
      "id": 131,
      "section": "BP",
      "bundle_version": "01",
      "serial": "074",
      "branch": null,
      "number": "BP01-074",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 8000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 913,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "[SIN]このキャラは、バトル相手のキャラのTYPEが 【剛力】 の間、BPが1グレードアップする。",
        "flavor_text": "ご唱和ください、我の名を！宇宙に響く友情の叫び！",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "オリジナル",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/ef2351ed6bd3133d53f21215c2d4a694ffeb22be",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/75b30e99f0daf3d302088f97ecfdc6046e80f7fe"
      }
    },
    {
      "id": 130,
      "section": "BP",
      "bundle_version": "01",
      "serial": "073",
      "branch": null,
      "number": "BP01-073",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 912,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "[SIN]《このキャラの登場時》自分は2枚ドローできる。この効果でドローした時、自分の手札1枚をデッキの下に戻す。",
        "flavor_text": "宇宙拳法・秘伝の神業が、悪を討つ！",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "アルファエッジ",
        "illustrator_name": "JUN YAMAGUCHI",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/d7cb04144266084e262e7d6540c1b885489922a6",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/23f930f0a3ae65cd3901e3470e45f680666090ec"
      }
    },
    {
      "id": 129,
      "section": "BP",
      "bundle_version": "01",
      "serial": "072",
      "branch": null,
      "number": "BP01-072",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 14000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 911,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "-",
        "flavor_text": "絶対自分に嘘はつけない。見せるぜ！衝撃！",
        "participating_works": "ウルトラマンジード",
        "participating_works_url": null,
        "type_name": "アトモスインパクト",
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/0aa0664dccbc57f677d2bde4dde94680779b3ace",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/fe6e78b803539c49230e69f48d7f8a429ad5ac06"
      }
    },
    {
      "id": 128,
      "section": "BP",
      "bundle_version": "01",
      "serial": "071",
      "branch": null,
      "number": "BP01-071",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 9000,
      "battle_power_2": 13000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 910,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "-",
        "flavor_text": "燃やすぜ！勇気！今日の不可能を明日の可能に変える！",
        "participating_works": "ウルトラマンジード",
        "participating_works_url": null,
        "type_name": "ストライクブースト",
        "illustrator_name": "Murakami Hisashi",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/0ba7fe5d48c09aa6d0693b13ab17a06400f8febb",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/0b0921f1f9c109c64754d4d1ae114b2797a078b4"
      }
    },
    {
      "id": 127,
      "section": "BP",
      "bundle_version": "01",
      "serial": "070",
      "branch": null,
      "number": "BP01-070",
      "rarity": {
        "value": "500_rr",
        "description": "RR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 14000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 909,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "[TRP][起動](ターンに1回)コストなし→自分のウルトラヒーロー1体を、このターンの間、BP+1000する。",
        "flavor_text": "もっと強く！もっと激しく！夢を抱け！この腕はみんなの明日を掴むためにある！",
        "participating_works": "ウルトラマンジード",
        "participating_works_url": null,
        "type_name": "ジードクロー",
        "illustrator_name": "KISUKE",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/d9c175f743dfd55b7eefb44f545c72ba5b036ef9",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/e5c12cc6cc8ccf8fee1f25107227859b54225f13"
      }
    },
    {
      "id": 126,
      "section": "BP",
      "bundle_version": "01",
      "serial": "069",
      "branch": null,
      "number": "BP01-069",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 10000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 908,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "-",
        "flavor_text": "いま、心の中に慈愛の勇者がいる。命を慈しむ学究のひとがいる。",
        "participating_works": "ウルトラマンジード",
        "participating_works_url": null,
        "type_name": "アクロスマッシャー",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/0895db2e70f4420349c571c604e5279fab0a3b7e",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/9144c61a66e4e0bd93ec96c8bdf5ba33b98b0128"
      }
    },
    {
      "id": 125,
      "section": "BP",
      "bundle_version": "01",
      "serial": "068",
      "branch": null,
      "number": "BP01-068",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 907,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "-",
        "flavor_text": "ウルトラセブンとレオの力と融合！優れた防御とパワーを宿す！",
        "participating_works": "ウルトラマンジード",
        "participating_works_url": null,
        "type_name": "ソリッドバーニング",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/af2b413f027542d9e4c7f321524dd3f39e5c8389",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/996abdcaa1cce5036c80d3e92473398367c5bfb3"
      }
    },
    {
      "id": 124,
      "section": "BP",
      "bundle_version": "01",
      "serial": "067",
      "branch": null,
      "number": "BP01-067",
      "rarity": {
        "value": "500_rr",
        "description": "RR"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 10000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 906,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "[DBL]《このキャラの登場時》バトル相手のキャラがDOUBLEなら、このターンのこのキャラのバトルを引き分けにすることができる。",
        "flavor_text": "困難だからこそ、立ち向かう価値がある、意味がある。",
        "participating_works": "ウルトラマンジード",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "Kazumasa Yasukuni",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/b72f632b8f87a5b0bf0f23c57cd41454bc3dade1",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/158dd2e405dc8a020471b2ef2c3c1359cabee4e7"
      }
    },
    {
      "id": 123,
      "section": "BP",
      "bundle_version": "01",
      "serial": "066",
      "branch": null,
      "number": "BP01-066",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 905,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "-",
        "flavor_text": "生まれた時に与えられたもの、それは勇気。",
        "participating_works": "ウルトラマンジード",
        "participating_works_url": null,
        "type_name": "プリミティブ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/b30d0a91633d196a9a3db2cc262a708581825730",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/f8b1233f5fcf5ad1eb52ef9c4a2fbc6716ff8ca6"
      }
    },
    {
      "id": 122,
      "section": "BP",
      "bundle_version": "01",
      "serial": "061",
      "branch": null,
      "number": "BP01-061",
      "rarity": {
        "value": "500_rr",
        "description": "RR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 13000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 904,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【剛力】 か 【武装】 の間、BPが1グレードアップする。",
        "flavor_text": "守れ宇宙の幸せを。傷つくことなど、恐れはしない。",
        "participating_works": "大怪獣バトル ウルトラ銀河伝説 THE MOVIE",
        "participating_works_url": null,
        "type_name": "ゼロスラッガー",
        "illustrator_name": "KISUKE",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/e13052f85e88dc3fa738a2652a6ed047cbf00ccb",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/c2fcdc2e65a63b749531e24d1b2e69a4ade64f61"
      }
    },
    {
      "id": 121,
      "section": "BP",
      "bundle_version": "01",
      "serial": "053",
      "branch": null,
      "number": "BP01-053",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 13000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 903,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "[TRP]《このキャラの登場時》自分がこのターンの先手プレイヤーなら、自分は1枚ドローできる。",
        "flavor_text": "海の光と大地の光が、ひとつになって新たな勇姿が奮い立つ！",
        "participating_works": "ウルトラマンガイア",
        "participating_works_url": null,
        "type_name": "V2",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/7ceacd752b472dc488b8bae53d16d743cc5193ad",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/dd13ba1d1ed312791948c574a7b146ee09a391f4"
      }
    },
    {
      "id": 120,
      "section": "BP",
      "bundle_version": "01",
      "serial": "052",
      "branch": null,
      "number": "BP01-052",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 12000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 902,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "[TRP]《このキャラの登場時》相手のシーン1つを手札に戻すことができる。",
        "flavor_text": "この地球に生きている限り、君を変える誰かが待っている。",
        "participating_works": "ウルトラマンガイア",
        "participating_works_url": null,
        "type_name": "フォトンエッジ",
        "illustrator_name": "Kazumasa Yasukuni",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/a421d64d11cab5c23779f7e0372c6d0e12c75894",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/03b2b328cd2fb7146dd638a64d46013a7aec19ce"
      }
    },
    {
      "id": 119,
      "section": "BP",
      "bundle_version": "01",
      "serial": "051",
      "branch": null,
      "number": "BP01-051",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 10000,
      "battle_power_3": 15000,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 901,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【剛力】 の間、BPが1グレードアップする。",
        "flavor_text": "君が歩いてきた道のどこかにきっと、君が気付けなかった光がある。",
        "participating_works": "ウルトラマンガイア",
        "participating_works_url": null,
        "type_name": "V2",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/bae377335052b4825769d6ce4b69c501c9927a15",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/ea4bf5bccc4a4ff047ef4d38e5ada0a734ff450f"
      }
    },
    {
      "id": 118,
      "section": "BP",
      "bundle_version": "01",
      "serial": "050",
      "branch": null,
      "number": "BP01-050",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 10000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 900,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "-",
        "flavor_text": "勇者は立つ。絶体絶命の時、本当の君が試される。",
        "participating_works": "ウルトラマンガイア",
        "participating_works_url": null,
        "type_name": "V1",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/df5212f953cb5c6d5de5fa577fb3d513651f4f0d",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/18748c24cd30524be1dc6633335d180bea7564a0"
      }
    },
    {
      "id": 117,
      "section": "BP",
      "bundle_version": "01",
      "serial": "049",
      "branch": null,
      "number": "BP01-049",
      "rarity": {
        "value": "500_rr",
        "description": "RR"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 10000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 899,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "[DBL]《このキャラの登場時》このキャラ以外のDOUBLEかTRIPLEの自分のウルトラヒーロー1体の1番上のカード1枚を手札に戻すことで、自分のウルトラヒーロー1体を、このターンの間、BP+1000できる。",
        "flavor_text": "君の心を受け止めたい。迷いも苦しみも悲しみもすべて。",
        "participating_works": "ウルトラマンガイア",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "F.M.U",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/55aedb5f798e95178833e0f86c9af709d0f2ab12",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/95570f0073c641f1d6726388d38543278a407ad8"
      }
    },
    {
      "id": 116,
      "section": "BP",
      "bundle_version": "01",
      "serial": "048",
      "branch": null,
      "number": "BP01-048",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 898,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "-",
        "flavor_text": "心と体の全てを賭けて平和を望む時、光はそれに応える。",
        "participating_works": "ウルトラマンガイア",
        "participating_works_url": null,
        "type_name": "V1",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/d4893ac62b710b5925991f631d1e97ea818cd816",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/ca7a763a38bf19534954f021a844c16446026128"
      }
    },
    {
      "id": 115,
      "section": "BP",
      "bundle_version": "01",
      "serial": "039",
      "branch": null,
      "number": "BP01-039",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2023,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 897,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンブレーザー",
        "ruby": "-",
        "character_name": "ブレーザー",
        "effect": "-",
        "flavor_text": "君は知るだろう。どんな困難にも怯まない天空を翔ぶ巨人を。",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/b635ae7d437d5b0b50f131130e8525b07c9d45a8",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/d999f2bbce7ed92baba6195faff96d1a036909c2"
      }
    },
    {
      "id": 114,
      "section": "BP",
      "bundle_version": "01",
      "serial": "037",
      "branch": null,
      "number": "BP01-037",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2023,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 896,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンブレーザー",
        "ruby": "-",
        "character_name": "ブレーザー",
        "effect": "[SIN]《このキャラの登場時》自分は2枚ドローできる。この効果でドローした時、自分の手札1枚をデッキの下に戻す。",
        "flavor_text": "俺が行く。君の願いの全てを抱き締めて。",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "JUN YAMAGUCHI",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/cfea823c92040c25c384e4c75caa255b4ef1a434",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/108bace3b27b5f42bbcbe20f6dd6f327606391dc"
      }
    },
    {
      "id": 113,
      "section": "BP",
      "bundle_version": "01",
      "serial": "033",
      "branch": null,
      "number": "BP01-033",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2022,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 895,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンデッカー",
        "ruby": "-",
        "character_name": "デッカー",
        "effect": "-",
        "flavor_text": "眠っていた心を呼び覚ませ。未知なる力を解き放つのは今。",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "ミラクルタイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/905af71f932343b8404d8c29f8bfa779f6028f2a",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/4d7fcb48b20c268e49bc9091545cc34ca9436ee0"
      }
    },
    {
      "id": 112,
      "section": "BP",
      "bundle_version": "01",
      "serial": "032",
      "branch": null,
      "number": "BP01-032",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 10000,
      "battle_power_3": 15000,
      "battle_power_ex": null,
      "publication_year": 2022,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 894,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンデッカー",
        "ruby": "-",
        "character_name": "デッカー",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【敏速】 の間、BPが1グレードアップする。",
        "flavor_text": "変わりたいと願うなら、もっともっと、強く強く。変わりたいと願い抜く！",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "ストロングタイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/c4b180466fd9f7a0cf659ac063f729ca73fb0584",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/6eea212aefd3367992ebafc5c1fd0c2206841c21"
      }
    },
    {
      "id": 111,
      "section": "BP",
      "bundle_version": "01",
      "serial": "031",
      "branch": null,
      "number": "BP01-031",
      "rarity": {
        "value": "500_rr",
        "description": "RR"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2022,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 893,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンデッカー",
        "ruby": "-",
        "character_name": "デッカー",
        "effect": "[DBL]《このキャラの登場時》このキャラと、このキャラの左隣か右隣にいるウルトラヒーロー1体の場所を入れ替えることができる。",
        "flavor_text": "希望の地図に書き足そう。色褪せない夢が進む、新しい道を。",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "F.M.U",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/e1c3ddacbdc2da3307c230b3c9c2548a43659ffc",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/4f6669344689d241aaf00e897bfceb47a75505eb"
      }
    },
    {
      "id": 110,
      "section": "BP",
      "bundle_version": "01",
      "serial": "030",
      "branch": null,
      "number": "BP01-030",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2022,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 892,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンデッカー",
        "ruby": "-",
        "character_name": "デッカー",
        "effect": "-",
        "flavor_text": "信じ続けて初めて分かることがある。到達出来る場所がある。",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "フラッシュタイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/0bb9f0946e2ab80d84b63798a6fa5a4da1caefb9",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/70fe63e07dc70dd09c6b74cfd6802fb8f0fa1887"
      }
    },
    {
      "id": 109,
      "section": "BP",
      "bundle_version": "01",
      "serial": "029",
      "branch": null,
      "number": "BP01-029",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": 9000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2022,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 891,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンデッカー",
        "ruby": "-",
        "character_name": "デッカー",
        "effect": "[SIN]このキャラは、バトル相手のキャラのTYPEが 【武装】 の間、BPが1グレードアップする。",
        "flavor_text": "希望が果てることはない。立ち止まることをやめた時、君の未来は変わる。",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "フラッシュタイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/f7caa507a771db75194677f3402117870aee16b7",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/505cb40bdb8c526e42955d56c52e5e8f6cfdaf86"
      }
    },
    {
      "id": 108,
      "section": "BP",
      "bundle_version": "01",
      "serial": "027",
      "branch": null,
      "number": "BP01-027",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 9000,
      "battle_power_2": 13000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2006,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 890,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンメビウス",
        "ruby": "-",
        "character_name": "メビウス",
        "effect": "-",
        "flavor_text": "最初にみんなとの夢を叶えた日。それは無限に続く未来の始まりの日。",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": "ブレードオーバーロード",
        "illustrator_name": "KISUKE",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/36dd282852e494e6b173b2b80c70fbd8dedf65ec",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/0328ed588ac9d1e3ba6fe8dd7cd810c660a9f115"
      }
    },
    {
      "id": 107,
      "section": "BP",
      "bundle_version": "01",
      "serial": "026",
      "branch": null,
      "number": "BP01-026",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 12000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 2006,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 889,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンメビウス",
        "ruby": "-",
        "character_name": "メビウス",
        "effect": "[TRP]《このキャラの登場時》自分のデッキの上のカード3枚を捨て札にすることで、自分のウルトラヒーロー1体を、このターンの間、BP+2000できる。",
        "flavor_text": "いつも信じよう、絆を夢を。いつだって僕はここにいる。",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": "メビュームナイトブレード",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/6c15edcc190f95b135a70d863f8a2b78ca110504",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/0d9b0c3ac6bdd0fb13eee72fe0d800b34a5a0de8"
      }
    },
    {
      "id": 106,
      "section": "BP",
      "bundle_version": "01",
      "serial": "025",
      "branch": null,
      "number": "BP01-025",
      "rarity": {
        "value": "400_rrr",
        "description": "RRR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 12000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2006,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 888,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンメビウス",
        "ruby": "-",
        "character_name": "メビウス",
        "effect": "[DBL][TRP][起動](ターンに1回)自分の手札1枚を捨て札にする→自分の 『メビウス』 1体は、このターンの間、BPが1グレードアップする。",
        "flavor_text": "託された思いが、託された光が、希望を宿した剣になる。",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": "メビュームナイトブレード",
        "illustrator_name": "SENNSU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/d7532d98d4e1adfc2e426330ac4dee8b02b6d83a",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/a3f20a2c39ea3da8b29d5016b2f92aae9053d953"
      }
    },
    {
      "id": 105,
      "section": "BP",
      "bundle_version": "01",
      "serial": "024",
      "branch": null,
      "number": "BP01-024",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2006,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 887,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンメビウス",
        "ruby": "-",
        "character_name": "メビウス",
        "effect": "-",
        "flavor_text": "誰かと戦うためじゃない。誰かと出会うために。",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/8fd6c7efe01903858b5e156f5b6b153a64ff871f",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/d6a25d8b3422043d34eae1b7952203fa34ac1c3c"
      }
    },
    {
      "id": 104,
      "section": "BP",
      "bundle_version": "01",
      "serial": "022",
      "branch": null,
      "number": "BP01-022",
      "rarity": {
        "value": "500_rr",
        "description": "RR"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 9000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2006,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 886,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンメビウス",
        "ruby": "-",
        "character_name": "メビウス",
        "effect": "[DBL]《このキャラの登場時》自分のデッキの上のカード2枚を捨て札にすることで、自分の捨て札エリアにあるシーンカードか、 『メビウス』 1枚を手札に戻すことができる。",
        "flavor_text": "十字を組んで輝く光。仲間たちとの思いをひとつに重ね、いま放たれる。",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "Kazumasa Yasukuni",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/5ed52971125e372ac3fb7f55f93061f34c1c201a",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/846f1c1650ce4c367407ffc001138c8fb259eac8"
      }
    },
    {
      "id": 103,
      "section": "BP",
      "bundle_version": "01",
      "serial": "021",
      "branch": null,
      "number": "BP01-021",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2006,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 885,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンメビウス",
        "ruby": "-",
        "character_name": "メビウス",
        "effect": "-",
        "flavor_text": "光の神殿で授けられたそれは、仲間と共に生きるための炎の徴。",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/4d39d457a24d33a5e212dbb6911c38ed71625ad6",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/f6466663b49abbf72a380a64536dab2cbeb2c639"
      }
    },
    {
      "id": 102,
      "section": "BP",
      "bundle_version": "01",
      "serial": "020",
      "branch": null,
      "number": "BP01-020",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 8000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2006,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 884,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンメビウス",
        "ruby": "-",
        "character_name": "メビウス",
        "effect": "[SIN]このキャラは、バトル相手のキャラのTYPEが 【敏速】 の間、BPが1グレードアップする。",
        "flavor_text": "光の国の若者は立つ。誰もが多くを学んだ地球という名の星に。",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/86066f92162ec05149647298c19add956d1635ca",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/dc41ae789edd620af2d2b1969e0b641e7a12a77e"
      }
    },
    {
      "id": 101,
      "section": "BP",
      "bundle_version": "01",
      "serial": "019",
      "branch": null,
      "number": "BP01-019",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2006,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 883,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンメビウス",
        "ruby": "-",
        "character_name": "メビウス",
        "effect": "[SIN]《このキャラの登場時》自分のデッキの上のカード3枚を公開することで、その中のウルトラヒーローカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "どんな時も、勇気を胸に。それが僕だ！",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/b80b04020a5064378731bfc8d577d6d0cf834284",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/cd66882cbc462d25e1338f53c8d17c7e339a7123"
      }
    },
    {
      "id": 100,
      "section": "BP",
      "bundle_version": "01",
      "serial": "017",
      "branch": null,
      "number": "BP01-017",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 13000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 882,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "[DBL][TRP]《このキャラの登場時》自分のウルトラヒーロー1体を、このターンの間、BP+1000できる。",
        "flavor_text": "纏う鎧が勇気を宿す。悲しみも憎しみも、この一撃が変える。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": "ソリスアーマー",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/b46ae1a289326889d5bd117f1adb861c5ae014a3",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/b34f77bc1a316fdf2490ccded3d8642f4cbe20b2"
      }
    },
    {
      "id": 99,
      "section": "BP",
      "bundle_version": "01",
      "serial": "015",
      "branch": null,
      "number": "BP01-015",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 881,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "-",
        "flavor_text": "大地を汚すものを打ち砕く。鎧拳にこめた思いを増幅する瞬間を見届けろ。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": "ソリスアーマー",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/37aa89649eaaa42beb2b652e5ea142c3c5d7e46e",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/be007b444c0d880ee4324ae29f61a316763bdd25"
      }
    },
    {
      "id": 98,
      "section": "BP",
      "bundle_version": "01",
      "serial": "014",
      "branch": null,
      "number": "BP01-014",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 10000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 880,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【武装】 の間、BPが1グレードアップする。",
        "flavor_text": "月の力を鎧に変えて、双肩に満ち渡る戦いの勇気。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": "ルーナアーマー",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/10a58de0300e69966a0e4f2493df0cc5356dac09",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/2fb14fa30caa957aa2bf3f7e14a14d833ed32b8b"
      }
    },
    {
      "id": 97,
      "section": "BP",
      "bundle_version": "01",
      "serial": "013",
      "branch": null,
      "number": "BP01-013",
      "rarity": {
        "value": "500_rr",
        "description": "RR"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 9000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 879,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "[SIN][DBL]《このキャラの登場時》自分のデッキの上のカード5枚を公開することで、その中のシーンカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "聖剣を手にする者。孤独に耐え、揺らめく影を断つ。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "HUJIWARA HISASHI",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/00996da66bdd884e3d42a158ba35143990016b3f",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/3fd6334a3672603b7449bd42146affe108e9e7f4"
      }
    },
    {
      "id": 96,
      "section": "BP",
      "bundle_version": "01",
      "serial": "012",
      "branch": null,
      "number": "BP01-012",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 878,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "-",
        "flavor_text": "想像の力で未来のために──支え、守り、そして戦う！",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/28a23d5f5831ccb3883e8aa2fba435f7f67f51b1",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/acc0d5fb0057845219438e3c12a4745ee6939c9a"
      }
    },
    {
      "id": 95,
      "section": "BP",
      "bundle_version": "01",
      "serial": "011",
      "branch": null,
      "number": "BP01-011",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 8000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 877,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "[SIN]このキャラは、バトル相手のキャラのTYPEが 【剛力】 の間、BPが1グレードアップする。",
        "flavor_text": "信じよう。君の瞳に映るものは、僕の瞳に映るものと同じ。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/0e61b1a1e3ed330062f4e99e9f189058f5b37c68",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/ae994341b1293f4f1b2004568fea2ce93d623f10"
      }
    },
    {
      "id": 94,
      "section": "BP",
      "bundle_version": "01",
      "serial": "007",
      "branch": null,
      "number": "BP01-007",
      "rarity": {
        "value": "400_rrr",
        "description": "RRR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 13000,
      "battle_power_3": 18000,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 876,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "[TRP]《このキャラの登場時》このキャラと、他の自分のウルトラヒーロー1体の場所を入れ替えることができる。",
        "flavor_text": "思い出そう。あの時君に勇気をくれたものは何だったのか。今度は君の番だ。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": "ゼペリオン光線",
        "illustrator_name": "Kenji Watanabe",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/bf1d342b29f35913433b21eaef5a5a8cbb5143ac",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/0237226abe5a6f1047fab9ce24222d5830cbc923"
      }
    },
    {
      "id": 93,
      "section": "BP",
      "bundle_version": "01",
      "serial": "004",
      "branch": null,
      "number": "BP01-004",
      "rarity": {
        "value": "500_rr",
        "description": "RR"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 9000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 875,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "[SIN][DBL]《このキャラの登場時》自分のデッキの上のカード5枚を公開することで、その中のシーンカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "腕をのばせ。心を研ぎ澄ませ。あれが闇を切り裂く光だ。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "F.M.U",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/e75fe05bc802be4956379b9110d37a123da3532d",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/a4bc1330205301f693ee8bdc9f3e8ea8048dfc57"
      }
    },
    {
      "id": 36,
      "section": "BP",
      "bundle_version": "01",
      "serial": "040",
      "branch": null,
      "number": "BP01-040",
      "rarity": {
        "value": "500_rr",
        "description": "RR"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": 15000,
      "battle_power_ex": null,
      "publication_year": 2023,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 330,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンブレーザー",
        "ruby": "-",
        "character_name": "ブレーザー",
        "effect": "[DBL]《このキャラの登場時》バトル相手のキャラ1体を、このターンの間、BP-2000できる。(※BPは0未満にはならない)",
        "flavor_text": "二重の螺旋が形成する光の槍。撃ち抜くのは巨悪の願いか傾く心か。",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "Kazumasa Yasukuni",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/332574476042915fcb60b655a447b700c7586560",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/8901437ee8e80f5b2c141ac694e6c95c5c577bda"
      }
    },
    {
      "id": 92,
      "section": "SD",
      "bundle_version": "02",
      "serial": "013",
      "branch": null,
      "number": "SD02-013",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 9000,
      "battle_power_2": 15000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 770,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ベリアル融合獣",
        "ruby": "ゆうごうじゅう",
        "character_name": "ペダニウムゼットン",
        "effect": "[SIN]《このキャラの登場時》ラウンド1の相手のシーン1つを捨て札にすることができる。",
        "flavor_text": "謎の寄生生物セレブロが宇宙の超強豪・キングジョーとゼットン、ウルトラマンベリアルの力を宿す。",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ペダニウムゼットン",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/d4d0b431ad3153c7c101cc62d9c4dba2d5bde223",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/49224a3913b5d45887eb2e5da93dbd9a365a741a"
      }
    },
    {
      "id": 91,
      "section": "SD",
      "bundle_version": "02",
      "serial": "010",
      "branch": null,
      "number": "SD02-010",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 769,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "-",
        "flavor_text": "誰かの歩んだ道と、誰かが目指す道とがめぐりあい、新たな道が続いていく。",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ゼットスラッガー",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/0eb306d60524f1233a2c7c4833328c146046707c",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/13af5c6025b06cb570d289c0417239088eb94d11"
      }
    },
    {
      "id": 90,
      "section": "SD",
      "bundle_version": "02",
      "serial": "008",
      "branch": null,
      "number": "SD02-008",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 10000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 768,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【武装】 の間、BPが1グレードアップする。",
        "flavor_text": "この宇宙に生まれた誇りに懸けて、その手に実りを結ぶ。",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ギャラクシーバースト",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/3a76a60e0636753047da025d772790fb98bde392",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/a3a69401339fff93ff62464273e6cb6c147517ba"
      }
    },
    {
      "id": 89,
      "section": "SD",
      "bundle_version": "02",
      "serial": "007",
      "branch": null,
      "number": "SD02-007",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 767,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "-",
        "flavor_text": "たとえ傷つき倒れても、この心は傷つかない！",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ギャラクシーライジング",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/c80b0ad46fe8cc846e5eabf7aa68e4b57d2e6c52",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/ed4a6c9d8361d98452644636c2fdc868f5c485b3"
      }
    },
    {
      "id": 88,
      "section": "SD",
      "bundle_version": "02",
      "serial": "006",
      "branch": null,
      "number": "SD02-006",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 766,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "-",
        "flavor_text": "苦しみでも悲しみでも、何度でもかかってこい！",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ワイドゼロショット",
        "illustrator_name": "HUJIWARA HISASHI",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/1bc06c2911a7014492bf427fe9f75053dbeb05bf",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/7e0f70f0fcdf6a27a7d3d510f05264e85478b82a"
      }
    },
    {
      "id": 87,
      "section": "SD",
      "bundle_version": "02",
      "serial": "005",
      "branch": null,
      "number": "SD02-005",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 10000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 765,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【武装】 の間、BPが1グレードアップする。",
        "flavor_text": "宇宙の平和を乱す奴は、この俺が許さない！",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "エメリウムスラッシュ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/714fcb3f01536a2e5f11c074e70585cde8b8825b",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/a3547c94052fdd27b91d551db24465b74444dbb1"
      }
    },
    {
      "id": 86,
      "section": "SD",
      "bundle_version": "01",
      "serial": "013",
      "branch": null,
      "number": "SD01-013",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 9000,
      "battle_power_2": 15000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1999,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 764,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "最強合体獣",
        "ruby": "さいきょうがったいじゅう",
        "character_name": "キングオブモンス",
        "effect": "[SIN]《このキャラの登場時》ラウンド0の相手のシーン1つを捨て札にすることができる。",
        "flavor_text": "邪心の深淵は果てない。満身創痍となろうとも、光の巨人に牙を剥く。",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": "キングオブモンス",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/6bb16f6166240e6783582db295ae2616ec8abef2",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/525bf4137f0eb28eb432dd7a7e2bb9f6ff13b53c"
      }
    },
    {
      "id": 85,
      "section": "SD",
      "bundle_version": "01",
      "serial": "011",
      "branch": null,
      "number": "SD01-011",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 11000,
      "battle_power_3": 13000,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 763,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【敏速】 の間、BPが1グレードアップする。",
        "flavor_text": "君が世界に存在する意味は、君が生き続けることで分かるもの。決められた道なんて無い。",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": "フォトンエッジ",
        "illustrator_name": "YAMAGUCHI BIRU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/8e56512595137e7e3335ff6aa54483f91247d58e",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/6711a29a5cc0808478cadb1c7b085ade7512c3bd"
      }
    },
    {
      "id": 84,
      "section": "SD",
      "bundle_version": "01",
      "serial": "008",
      "branch": null,
      "number": "SD01-008",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 10000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 1997,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 762,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンダイナ",
        "ruby": "-",
        "character_name": "ダイナ",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【武装】 の間、BPが1グレードアップする。",
        "flavor_text": "戦いの時は来た。君の街を守るため、君の思いを守るため、俺は来た！",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": "フラッシュタイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/6de20d819fd7151fa6530c43e8e8b41f70203845",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/f5e413cf27148073fc18a7bcbbeb30f1a6671065"
      }
    },
    {
      "id": 83,
      "section": "SD",
      "bundle_version": "01",
      "serial": "007",
      "branch": null,
      "number": "SD01-007",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1997,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 761,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンダイナ",
        "ruby": "-",
        "character_name": "ダイナ",
        "effect": "-",
        "flavor_text": "彼はまだ旅の途中。この宇宙の悲しみも喜びも、共に受けとめる旅の途中。",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": "フラッシュタイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/931694b6c8c6f931b542ac0d48b566ec1cb71bfc",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/f88340bb6c52fe23f193a5b30392cab660f202c9"
      }
    },
    {
      "id": 82,
      "section": "SD",
      "bundle_version": "01",
      "serial": "006",
      "branch": null,
      "number": "SD01-006",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 10000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 760,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "-",
        "flavor_text": "闇深き海底を照らす一条の光。邪気をまとった海獣を打ち砕く。",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": "ゼペリオン光線",
        "illustrator_name": "HUJIWARA HISASHI",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/0bde37d23edf04614029ee994a89e1ecaf6f4409",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/1e63feebd1232207a606ba48cca748c431ac9ad3"
      }
    },
    {
      "id": 81,
      "section": "SD",
      "bundle_version": "01",
      "serial": "005",
      "branch": null,
      "number": "SD01-005",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 10000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 759,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【剛力】 の間、BPが1グレードアップする。",
        "flavor_text": "そこに可能性がある限り、光は必ず現れる。",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": "マルチタイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/786165b140f09aa5e5d2c88df14409d4390527ad",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/109cea74d2ed940c1bd2cce3e871af9689ad9350"
      }
    },
    {
      "id": 80,
      "section": "SD",
      "bundle_version": "01",
      "serial": "004",
      "branch": null,
      "number": "SD01-004",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 758,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "-",
        "flavor_text": "自分に出来ること。それは多分、小さなことかもしれないけれど──",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": "マルチタイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/0f55bb60abff80d1bd647318fd5cf59bb5411b3d",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/406c852be8e27904c4e75fd9fd830327983478c9"
      }
    },
    {
      "id": 79,
      "section": "SD",
      "bundle_version": "02",
      "serial": "014",
      "branch": null,
      "number": "SD02-014",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "0",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 373,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "陛下のメダル",
        "ruby": "-",
        "character_name": "-",
        "effect": "[起動](ターンに1回)コストなし→自分の 『ゼロ』 か、 『ジード』 か、 『ゼット』 のバトル相手のキャラ1体に、このターンの間 、 【武装】 を与える。",
        "flavor_text": "-",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/c3e0ae60931bf637b4e647c0ce9f2a30b9997757",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/4953e23e6e3c82750f4b2aa2ee7e8cb6fa400f06"
      }
    },
    {
      "id": 78,
      "section": "SD",
      "bundle_version": "02",
      "serial": "012",
      "branch": null,
      "number": "SD02-012",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 10000,
      "battle_power_2": 16000,
      "battle_power_3": null,
      "battle_power_ex": 8000,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 372,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ベリアル融合獣",
        "ruby": "ゆうごうじゅう",
        "character_name": "スカルゴモラ",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【基本】 の間、EXTRAのBPになる。",
        "flavor_text": "ベリアル・ゴモラ・レッドキング──三つのメダルがセレブロを巨獣に変える！",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "スカルゴモラ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/5d44ed3381e5c66a02e2b9d1a48feb82a6698e49",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/42979583801f187a259fb8df0b27e75631b22db3"
      }
    },
    {
      "id": 77,
      "section": "SD",
      "bundle_version": "02",
      "serial": "011",
      "branch": null,
      "number": "SD02-011",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 10000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 371,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【武装】 の間、BPが1グレードアップする。",
        "flavor_text": "もう一度前を向く勇気が溢れた時、最強の魂がこの槍に宿る。",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ゼットランスアロー",
        "illustrator_name": "YAMAGUCHI BIRU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/564e3bdd62ae749eee61501af94cf7214cb7875c",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/5ad41e5268396eb96b61e6664eda5a8cd261f341"
      }
    },
    {
      "id": 76,
      "section": "SD",
      "bundle_version": "02",
      "serial": "009",
      "branch": null,
      "number": "SD02-009",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": 11000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 370,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "-",
        "flavor_text": "自分の運命を受け止め、運命と戦い抜く。そこに自分だけの未来が待っている。",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "レッキングフェニックス",
        "illustrator_name": "SENNSU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/24da40e6bbe97469f0269556695818e4347ad29f",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/7fd9dd02b263e8dfad597c207b64868c1e4fae68"
      }
    },
    {
      "id": 75,
      "section": "SD",
      "bundle_version": "02",
      "serial": "004",
      "branch": null,
      "number": "SD02-004",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 369,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "-",
        "flavor_text": "心の準備はいいか？君が漕ぎ出す戦いの海。俺も支える、全力で。",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ウルトラゼロマント",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/95573bded05ea6c50fb2c0788cb6c7572e8d4359",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/987eb43ae1e35efe6a8fed30f92ecb21553c6553"
      }
    },
    {
      "id": 74,
      "section": "SD",
      "bundle_version": "02",
      "serial": "003",
      "branch": null,
      "number": "SD02-003",
      "rarity": {
        "value": "400_rrr",
        "description": "RRR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 368,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "[SIN][DBL]《このキャラの登場時》DOUBLEの自分の 『ジード』 1体を、このターンの間、BPを1グレードアップできる。",
        "flavor_text": "宇宙には、君だけが歩む唯一の道がある。",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ギャラクシーライジング",
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/ebecd9f4a1c325c1e69cacc780efbcb63d31b41e",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/d19ae18b25e8019ed9620f56fe9fb8f2912f1237"
      }
    },
    {
      "id": 73,
      "section": "SD",
      "bundle_version": "02",
      "serial": "002",
      "branch": null,
      "number": "SD02-002",
      "rarity": {
        "value": "400_rrr",
        "description": "RRR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 13000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 367,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【基本】 か 【武装】 の間、BPが1グレードアップする。",
        "flavor_text": "真実とは、自分の心で確かめるもの。",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "ウルトラゼロマント",
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/12c69fc01a5aa803344c2a63e969f92d139ed00c",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/e95dc60a48f13e4ccab678d2f312d3a537af8787"
      }
    },
    {
      "id": 72,
      "section": "SD",
      "bundle_version": "02",
      "serial": "001",
      "branch": null,
      "number": "SD02-001",
      "rarity": {
        "value": "400_rrr",
        "description": "RRR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 13000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第2弾】デッキ 零のキズナ"],
      "detail": {
        "id": 366,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【敏速】 か 【武装】 の間、BPが1グレードアップする。",
        "flavor_text": "この星に降りかかる悲しみを打ち払う、勇気の光。",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": "アルファエッジ",
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/acd006ecb2717ab45f3368f74daaf8d1a874ab2b",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/cc807cabc13dea093ceb2d749a623e4d66f12061"
      }
    },
    {
      "id": 71,
      "section": "SD",
      "bundle_version": "01",
      "serial": "014",
      "branch": null,
      "number": "SD01-014",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "1",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 365,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ・ウルトラマンダイナ＆ウルトラマンガイア 超時空の大決戦",
        "ruby": "-",
        "character_name": "-",
        "effect": "[起動](ターンに1回)コストなし→自分の 『ティガ』 か、 『ダイナ』 か、 『ガイア』 1体を、このターンの間、BP+1000する。",
        "flavor_text": "-",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/57754bbb0ffdfedff9f3eb557ab363e5a4f6a0b8",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/295d918145a843eccdc64004259cd759ec1aff5c"
      }
    },
    {
      "id": 70,
      "section": "SD",
      "bundle_version": "01",
      "serial": "012",
      "branch": null,
      "number": "SD01-012",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 10000,
      "battle_power_2": 16000,
      "battle_power_3": null,
      "battle_power_ex": 8000,
      "publication_year": 1999,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 364,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "巨大異形獣",
        "ruby": "きょだいいぎょうじゅう",
        "character_name": "サタンビゾー",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【基本】 の間、EXTRAのBPになる。",
        "flavor_text": " “この世界は滅びる” ──「悪魔の接吻」の物語は、人々に絶望を叩きつける！",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": "サタンビゾー",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/7fa3e0a44231cce86e011e4098264436cdabaf34",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/9d1d2838bba6598fce3c2069183e73b473adc2f2"
      }
    },
    {
      "id": 69,
      "section": "SD",
      "bundle_version": "01",
      "serial": "010",
      "branch": null,
      "number": "SD01-010",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 363,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "-",
        "flavor_text": "約束しよう。悲しみに染まる時間はここまでだ！",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": "V2",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/830acbd8e371310f03c4b9637252ea15b106c8ff",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/71a219920aa4d97109810295ef21dda8da6111d1"
      }
    },
    {
      "id": 68,
      "section": "SD",
      "bundle_version": "01",
      "serial": "009",
      "branch": null,
      "number": "SD01-009",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 10000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1997,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 362,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンダイナ",
        "ruby": "-",
        "character_name": "ダイナ",
        "effect": "-",
        "flavor_text": "宇宙のドッグファイトを制する者は、骨翼の威容を放つ超獣か？彗星のごとき光の戦士か？",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": "ソルジェント光線",
        "illustrator_name": "JUN YAMAGUCHI",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/182fc39e9ec2f7a02b019e2969fe4574baaa36d6",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/d179c3cae5ca5f82e5bcbb4727757957be29aeb9"
      }
    },
    {
      "id": 67,
      "section": "SD",
      "bundle_version": "01",
      "serial": "003",
      "branch": null,
      "number": "SD01-003",
      "rarity": {
        "value": "400_rrr",
        "description": "RRR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 9000,
      "battle_power_2": 11000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 361,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "[DBL][TRP]《このキャラの登場時》自分のデッキの上のカード3枚を公開することで、その中の「ウルトラマンティガ・ウルトラマンダイナ＆ウルトラマンガイア 超時空の大決戦」か、 『ティガ』 か、 『ダイナ』 1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "不安に追われて忘れかけていることはないかい？本当の友だちがそれを教えてくれる。",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": "V2",
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/f8e35ad499f14c83b5a6823eb772f891f8382080",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/f7a43262236ee5837f0872dab11568118d4f9821"
      }
    },
    {
      "id": 66,
      "section": "SD",
      "bundle_version": "01",
      "serial": "002",
      "branch": null,
      "number": "SD01-002",
      "rarity": {
        "value": "400_rrr",
        "description": "RRR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 9000,
      "battle_power_2": 12000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 360,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "[TRP][起動](ターンに1回)自分の手札1枚を捨て札にする→バトル相手のキャラ1体は、このターンの間、BPが1グレードダウンする。",
        "flavor_text": "正義に絶対は無い。だが、誰かを思いやる心は、どんなに時を超えても永久不変。",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": "マルチタイプ",
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/d6224cae8d6570f3f7cb1e598ffcdbce56bb7f33",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/8be2289113f03eaa39f67a5867fff99f4c3f5823"
      }
    },
    {
      "id": 65,
      "section": "SD",
      "bundle_version": "01",
      "serial": "001",
      "branch": null,
      "number": "SD01-001",
      "rarity": {
        "value": "400_rrr",
        "description": "RRR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 9000,
      "battle_power_2": 11000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 1997,
      "display_card_bundle_names": ["【第1弾】デッキ 超時空の英雄たち"],
      "detail": {
        "id": 359,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンダイナ",
        "ruby": "-",
        "character_name": "ダイナ",
        "effect": "[DBL][TRP]《このキャラの登場時》自分のデッキの上のカード3枚を公開することで、その中の「ウルトラマンティガ・ウルトラマンダイナ＆ウルトラマンガイア 超時空の大決戦」か、 『ティガ』 か、 『ガイア』 1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "最高の時は一度限りじゃない。空を見ろ、チャンスは何度でも降ってくる。",
        "participating_works": "ウルトラマンティガ・ウルトラマンダイナ&ウルトラマンガイア 超時空の大決戦",
        "participating_works_url": null,
        "type_name": "フラッシュタイプ",
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/8f0a33cfe1e2a3b130d107293b37fbcb5d97c5c2",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/631b2626469f72354e6c402c034e982332546836"
      }
    },
    {
      "id": 64,
      "section": "BP",
      "bundle_version": "01",
      "serial": "107",
      "branch": null,
      "number": "BP01-107",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "1",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 358,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "大怪獣バトル ウルトラ銀河伝説 THE MOVIE THE MOVIE",
        "ruby": "-",
        "character_name": "-",
        "effect": "[起動](ターンに1回)コストなし→自分の 『ゼロ』 のバトル相手のキャラ1体に、このターンの間、 【剛力】 か 【敏速】 を与える。",
        "flavor_text": "-",
        "participating_works": "大怪獣バトル ウルトラ銀河伝説 THE MOVIE",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/64d291e58af9fe5a9b7f9473017c515f96a2858c",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/ad0d61a4a9fb8626a9c0a66de7cef3de50762948"
      }
    },
    {
      "id": 63,
      "section": "BP",
      "bundle_version": "01",
      "serial": "106",
      "branch": null,
      "number": "BP01-106",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "4",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 357,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "決着の日",
        "ruby": "-",
        "character_name": "-",
        "effect": "TRIPLEの自分の 『ガイア』 すべてをBP+1000する。",
        "flavor_text": "-",
        "participating_works": "ウルトラマンガイア",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/9d558b1f140c18720dcac1a58f74bebee125d87c",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/d4e2565219cedb53cc5605621f9043742a82688c"
      }
    },
    {
      "id": 62,
      "section": "BP",
      "bundle_version": "01",
      "serial": "105",
      "branch": null,
      "number": "BP01-105",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": "2",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 356,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "SKaRDを作った男",
        "ruby": "-",
        "character_name": "-",
        "effect": "[起動](ターンに1回)自分の 『ブレーザー』 がいるなら、自分のデッキの上のカード5枚を公開する→公開したカードの中にあるウルトラヒーローカード1枚を、レベルアップが可能な自分のウルトラヒーロー1体の上に登場させる。登場させなかったカードは捨て札にし、ターン終了時に、この効果で登場させたカードを捨て札にする。",
        "flavor_text": "-",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/42d8195d1e8890f6b966bf19a1263f31b5b64b93",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/2afac04a04432d8825747a3d81b4682557203a2a"
      }
    },
    {
      "id": 61,
      "section": "BP",
      "bundle_version": "01",
      "serial": "102",
      "branch": null,
      "number": "BP01-102",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": "1",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 355,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "未来へ駆ける円弧(アーク)",
        "ruby": "-",
        "character_name": "-",
        "effect": "[起動](ターンに1回)自分の手札にある 『アーク』 1枚を捨て札にする→自分のウルトラヒーロー1体を、このターンの間、BP+2000する。",
        "flavor_text": "-",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/83d74254c99079e4c3d6cb6f88b00516e6d97035",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/71352f90c760a3ad99e455ffd222f1a839f06531"
      }
    },
    {
      "id": 60,
      "section": "BP",
      "bundle_version": "01",
      "serial": "094",
      "branch": null,
      "number": "BP01-094",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 9000,
      "battle_power_2": 15000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2022,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 354,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "精強融合獣",
        "ruby": "せいきょうゆうごうじゅう",
        "character_name": "スフィアザウルス",
        "effect": "[SIN]このキャラは、バトル相手のキャラのTYPEが 【基本】 の間、BPが1グレードアップする。",
        "flavor_text": "禍々しき巨大な腕を大地に突き立て、星の命を喰らう！",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "スフィアザウルス",
        "illustrator_name": "Murakami Hisashi",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/19c303b66e641fdf45b688071adcb726bc8a0a6d",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/e81861d69b9c3bc173267498fc1d157e0b1df0c8"
      }
    },
    {
      "id": 59,
      "section": "BP",
      "bundle_version": "01",
      "serial": "091",
      "branch": null,
      "number": "BP01-091",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "6",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 9000,
      "battle_power_2": 16000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 353,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "超古代怪獣",
        "ruby": "ちょうこだいかいじゅう",
        "character_name": "ゴルザ",
        "effect": "[SIN]《このキャラの登場時》ラウンド3以上の相手のシーン1つを捨て札にすることができる。",
        "flavor_text": "大地を揺るがす怪獣──それは、太古の予言が伝えた闇の支配者の尖兵。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": "ゴルザ",
        "illustrator_name": "gozz",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/c962e3ed15e295cdbb112cb2f1e65c78f414d2c5",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/b9dbeeee99fbb93a281d0251cae9d218129c19aa"
      }
    },
    {
      "id": 58,
      "section": "BP",
      "bundle_version": "01",
      "serial": "085",
      "branch": null,
      "number": "BP01-085",
      "rarity": {
        "value": "500_rr",
        "description": "RR"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2021,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 352,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマントリガー",
        "ruby": "-",
        "character_name": "トリガー",
        "effect": "[DBL]《このキャラの登場時》ラウンド3以下のシーン1つを捨て札にすることができる。",
        "flavor_text": "仲間のために、未来のために、君は今の時代に生まれてきた。",
        "participating_works": "ウルトラマントリガー NEW GENERATION TIGA",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "JUN YAMAGUCHI",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/6b8cd5fd197c4173a0d70d636cf5f3d05d2807f5",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/8c8615a187321a5c2e305f9a55d7425a1b686dca"
      }
    },
    {
      "id": 57,
      "section": "BP",
      "bundle_version": "01",
      "serial": "082",
      "branch": null,
      "number": "BP01-082",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2021,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 351,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマントリガー",
        "ruby": "-",
        "character_name": "トリガー",
        "effect": "[SIN]《このキャラの登場時》自分のデッキの上のカード3枚を公開することで、その中のウルトラヒーローカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "時の大河を越える時、見えてくる光。護るべきものを指し示す光。",
        "participating_works": "ウルトラマントリガー NEW GENERATION TIGA",
        "participating_works_url": null,
        "type_name": "マルチタイプ",
        "illustrator_name": "TSUYOSHI NONAKA",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/51f1b70023f65f0fca593cf7740099b59e43a93c",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/5c5f8cf3f8416b84f6d9b15b95f471e68c054b85"
      }
    },
    {
      "id": 56,
      "section": "BP",
      "bundle_version": "01",
      "serial": "076",
      "branch": null,
      "number": "BP01-076",
      "rarity": {
        "value": "500_rr",
        "description": "RR"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 9000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2020,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 350,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼット",
        "ruby": "-",
        "character_name": "ゼット",
        "effect": "[SIN][DBL]《このキャラの登場時》自分のデッキの上のカード5枚を公開することで、その中のシーンカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "奇跡は待ってたって来やしない。どこまでもどこまでも、自分の思いで引き寄せる！",
        "participating_works": "ウルトラマンZ",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "HUJIWARA HISASHI",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/1ad6ac384bf8144b679168bfada0a153a4849920",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/0230c4a46ad5866112a493c8d72181d386def4ad"
      }
    },
    {
      "id": 55,
      "section": "BP",
      "bundle_version": "01",
      "serial": "065",
      "branch": null,
      "number": "BP01-065",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 8000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 349,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "[SIN]このキャラは、バトル相手のキャラのTYPEが 【剛力】 の間、BPが1グレードアップする。",
        "flavor_text": "夢を汚す者は誰？愛を知らぬ者は誰？",
        "participating_works": "ウルトラマンジード",
        "participating_works_url": null,
        "type_name": "プリミティブ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/4aac2f8e2625e5d19ab8375f922db309dd2a0b3d",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/c225d3aebf976cb71f4f6fb7b9c4991e16629033"
      }
    },
    {
      "id": 54,
      "section": "BP",
      "bundle_version": "01",
      "serial": "064",
      "branch": null,
      "number": "BP01-064",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2017,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 348,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンジード",
        "ruby": "-",
        "character_name": "ジード",
        "effect": "[SIN]《このキャラの登場時》自分のデッキの上のカード3枚を公開することで、その中のウルトラヒーローカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "このぬくもり、いつまでも分かち合いたい。決めるぜ！覚悟！",
        "participating_works": "ウルトラマンジード",
        "participating_works_url": null,
        "type_name": "プリミティブ",
        "illustrator_name": "YAMAGUCHI BIRU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/c92e5c88722cd6753c8952b6b75ca84f22f8546b",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/f2fbfed2ddbeb943eba4cee41383f394a082de30"
      }
    },
    {
      "id": 53,
      "section": "BP",
      "bundle_version": "01",
      "serial": "063",
      "branch": null,
      "number": "BP01-063",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 14000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 347,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "-",
        "flavor_text": "不可能は可能への入り口。勇気ひとつが、突破口を開く。",
        "participating_works": "大怪獣バトル ウルトラ銀河伝説 THE MOVIE",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/6bac34599b19cc4b9e9f494534fc3a8b77ecc51b",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/b60dc111fe1d9bb16a34db33ce9acbbb6842d3d7"
      }
    },
    {
      "id": 52,
      "section": "BP",
      "bundle_version": "01",
      "serial": "062",
      "branch": null,
      "number": "BP01-062",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 12000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 346,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "[DBL]《このキャラの登場時》自分の 『ゼロ』 1体を、このターンの間、BP+2000できる。",
        "flavor_text": "可能性はゼロではない。だが、可能性を無限大にするのは、自分の力以外に無い。",
        "participating_works": "大怪獣バトル ウルトラ銀河伝説 THE MOVIE",
        "participating_works_url": null,
        "type_name": "プラズマスパークスラッシュ",
        "illustrator_name": "SENNSU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/6ebfa17e613667ed3b15edd6369edf2e959507cb",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/31f06a3b05445c7c1a209a831ec4f92995d8ec11"
      }
    },
    {
      "id": 51,
      "section": "BP",
      "bundle_version": "01",
      "serial": "060",
      "branch": null,
      "number": "BP01-060",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 10000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 345,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "-",
        "flavor_text": "君の命も、星の命も、変わりはない。必ず守り抜く同じ命。",
        "participating_works": "大怪獣バトル ウルトラ銀河伝説 THE MOVIE",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/311799d87c38fe50f459845e7ec8d8d2984344ad",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/cf3e865fe6ff07b4d34e72de2adac8f4f3a053d0"
      }
    },
    {
      "id": 50,
      "section": "BP",
      "bundle_version": "01",
      "serial": "059",
      "branch": null,
      "number": "BP01-059",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 11000,
      "battle_power_3": 13000,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 344,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【敏速】 の間、BPが1グレードアップする。",
        "flavor_text": "命を懸けて、誇りを懸けて、俺は行く。宇宙を駆ける光になる。",
        "participating_works": "大怪獣バトル ウルトラ銀河伝説 THE MOVIE",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/a99828784b15549dccd8fd6192a6674761a6e60a",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/1fc5f0e0cb839dcef953a156785a2434ceb64fb9"
      }
    },
    {
      "id": 49,
      "section": "BP",
      "bundle_version": "01",
      "serial": "058",
      "branch": null,
      "number": "BP01-058",
      "rarity": {
        "value": "500_rr",
        "description": "RR"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 11000,
      "battle_power_3": 14000,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 343,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "[SIN][DBL]《このキャラの登場時》自分は 【剛力】 か 【敏速】 を選ぶことで、相手のキャラすべてに、このターンの間、選んだTYPEを与えることができる。",
        "flavor_text": "見よ！宇宙も照らすこの輝き。魂で受け継ぐウルトラマンのフルパワー！",
        "participating_works": "大怪獣バトル ウルトラ銀河伝説 THE MOVIE",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "JUN YAMAGUCHI",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/6c5aa15b89458553adb46999ba6d80b6c59ee996",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/7d14ee700d71d3836f7d0ad0cd6129b6f9f7775c"
      }
    },
    {
      "id": 48,
      "section": "BP",
      "bundle_version": "01",
      "serial": "057",
      "branch": null,
      "number": "BP01-057",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 342,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "テクターギア・ゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "-",
        "flavor_text": "鎧の重さは俺のさだめ。耐えぬき培ったものこそ、俺の未来への礎。",
        "participating_works": "大怪獣バトル ウルトラ銀河伝説 THE MOVIE",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "Kazumasa Yasukuni",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/ffddfb5342ed8a275b506de2f229fea38727c15e",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/3328908176972a59c0b11bd510eee0afa0c28943"
      }
    },
    {
      "id": 47,
      "section": "BP",
      "bundle_version": "01",
      "serial": "056",
      "branch": null,
      "number": "BP01-056",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 341,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "テクターギア・ゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "-",
        "flavor_text": "鍛え抜いた体に魂をこめて、全てに追いつき、全てを抜き去る！",
        "participating_works": "大怪獣バトル ウルトラ銀河伝説 THE MOVIE",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/2f12e1b14aa8bc815c6cac7e8facd8ebd2082b22",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/e1b1ecf5e4618473795f19de7738f6c62de0e673"
      }
    },
    {
      "id": 46,
      "section": "BP",
      "bundle_version": "01",
      "serial": "055",
      "branch": null,
      "number": "BP01-055",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 340,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "[SIN]《このキャラの登場時》自分は2枚ドローできる。この効果でドローした時、自分の手札1枚をデッキの下に戻す。",
        "flavor_text": "父・ウルトラセブンの想いを胸に、行くぞ新時代へ！立つぞ新世界の大地に！",
        "participating_works": "大怪獣バトル ウルトラ銀河伝説 THE MOVIE",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "YAMAGUCHI BIRU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/b08ee6c9a147a9e096e2749ffd90213558e2a9f1",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/2d9377221e8758a092bfc27de02a9a907d402be1"
      }
    },
    {
      "id": 45,
      "section": "BP",
      "bundle_version": "01",
      "serial": "054",
      "branch": null,
      "number": "BP01-054",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 9000,
      "battle_power_2": 13000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 339,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "-",
        "flavor_text": "この星に生まれた奇跡、奇跡を生む大地の光。その円環の中に巨人は立つ。",
        "participating_works": "ウルトラマンガイア",
        "participating_works_url": null,
        "type_name": "V2",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/1cd332a774c74e8f6ca2a4a46a88ec1b4ad45283",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/f283b97ee66d5c4d0d048f14ccad373d4e6b465a"
      }
    },
    {
      "id": 44,
      "section": "BP",
      "bundle_version": "01",
      "serial": "047",
      "branch": null,
      "number": "BP01-047",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 338,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "-",
        "flavor_text": "ひとりじゃない。君の声が届いたら、星も時空も超えてみせる。",
        "participating_works": "ウルトラマンガイア",
        "participating_works_url": null,
        "type_name": "V1",
        "illustrator_name": "YAMAGUCHI BIRU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/57d5abb80d9f5f09505d8287b45364611f02cb57",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/7e65097aafb330ec5339b0495ced1fd612e1f7e0"
      }
    },
    {
      "id": 43,
      "section": "BP",
      "bundle_version": "01",
      "serial": "046",
      "branch": null,
      "number": "BP01-046",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1998,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 337,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンガイア",
        "ruby": "-",
        "character_name": "ガイア",
        "effect": "[SIN]《このキャラの登場時》自分のデッキの上のカード3枚を公開することで、その中のウルトラヒーローカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "君が教えてくれた。護るものに気付いた今が、本当の幸せだと。",
        "participating_works": "ウルトラマンガイア",
        "participating_works_url": null,
        "type_name": "V1",
        "illustrator_name": "KISUKE",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/646886186dd5c5556bd1f0431861d4a955865740",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/180f9834fc5476bc6c09d6b469ede5a57e415c57"
      }
    },
    {
      "id": 42,
      "section": "BP",
      "bundle_version": "01",
      "serial": "045",
      "branch": null,
      "number": "BP01-045",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 9000,
      "battle_power_2": 13000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2023,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 336,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンブレーザー",
        "ruby": "-",
        "character_name": "ブレーザー",
        "effect": "-",
        "flavor_text": "誰もが明日の平和を夢見ている。その願いを一身に受け、勇者は戦う。",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/73df1091916b1508f387777b580569daf7c70879",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/8db5c6d9684cd4ecadde5df3390b4af71dad001b"
      }
    },
    {
      "id": 41,
      "section": "BP",
      "bundle_version": "01",
      "serial": "044",
      "branch": null,
      "number": "BP01-044",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 12000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 2023,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 335,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンブレーザー",
        "ruby": "-",
        "character_name": "ブレーザー",
        "effect": "[DBL][TRP]《このキャラの登場時》自分は1枚ドローできる。この効果でドローした時、自分の手札1枚をデッキの上か下に戻す。",
        "flavor_text": "澱む闇夜に怖じ気づく者たちよ。見よ。巨人の光が明日を照らす道標となる。",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": "サプレッシブ・スプライト",
        "illustrator_name": "TSUYOSHI NONAKA",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/a65c64411af72a15acdc948b4afed7337b5dd4c1",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/15e93ff144fa7d946b3608353acaeb8fae9eac37"
      }
    },
    {
      "id": 39,
      "section": "BP",
      "bundle_version": "01",
      "serial": "043",
      "branch": null,
      "number": "BP01-043",
      "rarity": {
        "value": "400_rrr",
        "description": "RRR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 12000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2023,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 333,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンブレーザー",
        "ruby": "-",
        "character_name": "ブレーザー",
        "effect": "[TRP]《このキャラの登場時》自分のデッキの上のカード3枚を公開し、好きな順番でデッキの上に戻すことで、バトル相手のキャラ1体を、このターンの間、BP-3000できる。(※BPは0未満にはならない)",
        "flavor_text": "守れその力で！この星の人々との奇跡の絆を‼",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": "スパイラルバレード",
        "illustrator_name": "YAMAGUCHI BIRU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/1fe604610f76e21f5ca4229ea084bc552c339bfa",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/de813dfe17ea3cd6cb7529fbc56481d154338940"
      }
    },
    {
      "id": 38,
      "section": "BP",
      "bundle_version": "01",
      "serial": "042",
      "branch": null,
      "number": "BP01-042",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2023,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 332,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンブレーザー",
        "ruby": "-",
        "character_name": "ブレーザー",
        "effect": "-",
        "flavor_text": "明日へ飛べ。光の速さで、君の思いと心を重ねて。",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/4c66d0fda0c231d7fbd2689b9eb7e08c094f779e",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/3ede62d0a0fc6dff153a0a285d9024c6c457f4a9"
      }
    },
    {
      "id": 37,
      "section": "BP",
      "bundle_version": "01",
      "serial": "041",
      "branch": null,
      "number": "BP01-041",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": 13000,
      "battle_power_ex": null,
      "publication_year": 2023,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 331,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンブレーザー",
        "ruby": "-",
        "character_name": "ブレーザー",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【剛力】 の間、BPが1グレードアップする。",
        "flavor_text": "拳が感じとる。光の脈動が全身に伝わり、心を震わせていく。",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "SENNSU",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/d8172326b978b31725ce3da9819edc4e2bd907f6",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/3c8e71a0a48c0cf62ab1399beb341999069b8fae"
      }
    },
    {
      "id": 35,
      "section": "BP",
      "bundle_version": "01",
      "serial": "038",
      "branch": null,
      "number": "BP01-038",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": 9000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2023,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 329,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンブレーザー",
        "ruby": "-",
        "character_name": "ブレーザー",
        "effect": "[SIN]このキャラは、バトル相手のキャラのTYPEが 【武装】 の間、BPが1グレードアップする。",
        "flavor_text": "地球を離れること、4億4100万光年の彼方、天体M421から希望は来たれり。",
        "participating_works": "ウルトラマンブレーザー",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/ca6bccb92fefc6862257de3918f9d2034fc02ef2",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/75dece56548c145a4dc398a6410cea47b5adf696"
      }
    },
    {
      "id": 34,
      "section": "BP",
      "bundle_version": "01",
      "serial": "036",
      "branch": null,
      "number": "BP01-036",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 9000,
      "battle_power_2": 13000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2022,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 328,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンデッカー",
        "ruby": "-",
        "character_name": "デッカー",
        "effect": "-",
        "flavor_text": "飛び出せ！ミラクル！夢を曇らせるな。この光は、明日の在処を照らし出す。",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "レアリュートウェーブ",
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/12fc6f0131f2babc4a6def4d1b44fa44bc3486b9",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/7e4bf3e6291a1a376bd7566ba95368be952a3c83"
      }
    },
    {
      "id": 33,
      "section": "BP",
      "bundle_version": "01",
      "serial": "035",
      "branch": null,
      "number": "BP01-035",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 13000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 2022,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 327,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンデッカー",
        "ruby": "-",
        "character_name": "デッカー",
        "effect": "[TRP]《このキャラの登場時》このキャラの両隣にいるウルトラヒーローを、このターンの間、BP+1000できる。",
        "flavor_text": "弾けろ！ストロング！その姿には、限りない希望と強さが宿る。",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "ドルネイドブレイカー",
        "illustrator_name": "TSUYOSHI NONAKA",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/9bfffce32d489cff2b8d40b68c2df60dc1251ab8",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/d0a1172436a32847098e67615097680d51971236"
      }
    },
    {
      "id": 31,
      "section": "BP",
      "bundle_version": "01",
      "serial": "034",
      "branch": null,
      "number": "BP01-034",
      "rarity": {
        "value": "400_rrr",
        "description": "RRR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "armed",
        "description": "武装"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 12000,
      "battle_power_3": 18000,
      "battle_power_ex": null,
      "publication_year": 2022,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 325,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンデッカー",
        "ruby": "-",
        "character_name": "デッカー",
        "effect": "[DBL][TRP]SINGLEの自分の 『デッカー』 と 『トリガー』 すべては、 このキャラ以外のTRIPLEの自分のウルトラヒーローがいる間、BPが1グレードアップする。この効果は重複しない。",
        "flavor_text": "どんな困難の渦にも、きっと光が見えるはず──みんなの思いを重ねれば。",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "フラッシュタイプ",
        "illustrator_name": "Kazumasa Yasukuni",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/99972f5922215dfab3e26e805d618d99bf6cf176",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/ce4ba4c136c34ced2dc339ed35cb618eecbc4f1d"
      }
    },
    {
      "id": 30,
      "section": "BP",
      "bundle_version": "01",
      "serial": "028",
      "branch": null,
      "number": "BP01-028",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2022,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 324,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンデッカー",
        "ruby": "-",
        "character_name": "デッカー",
        "effect": "[SIN]《このキャラの登場時》自分は2枚ドローできる。この効果でドローした時、自分の手札1枚をデッキの下に戻す。",
        "flavor_text": "星の彼方に届く夢のつづきを、今日も絆で紡いでいく。",
        "participating_works": "ウルトラマンデッカー",
        "participating_works_url": null,
        "type_name": "フラッシュタイプ",
        "illustrator_name": "KISUKE",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/33e108258b321d60ea07445974c92f676877fbbe",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/dcfa9f524b980ff556f06acc97f578df96dae32d"
      }
    },
    {
      "id": 28,
      "section": "BP",
      "bundle_version": "01",
      "serial": "023",
      "branch": null,
      "number": "BP01-023",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 10000,
      "battle_power_3": 15000,
      "battle_power_ex": null,
      "publication_year": 2006,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 322,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンメビウス",
        "ruby": "-",
        "character_name": "メビウス",
        "effect": "[SIN][DBL]このキャラは、バトル相手のキャラのTYPEが 【剛力】 の間、BPが1グレードアップする。",
        "flavor_text": "いまその腕に未来への希望が輝き、闇を撃ち抜く熱気は高まる。",
        "participating_works": "ウルトラマンメビウス",
        "participating_works_url": null,
        "type_name": "メビュームブレード",
        "illustrator_name": "Akihiro MIYANO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/a02ececca9a6e349c300bdd542791858a0b4aaed",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/72336823849caf8b730dfd519207ce897fc7c4ea"
      }
    },
    {
      "id": 27,
      "section": "BP",
      "bundle_version": "01",
      "serial": "018",
      "branch": null,
      "number": "BP01-018",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 9000,
      "battle_power_2": 13000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 321,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "-",
        "flavor_text": "纏う鎧は勇者の証。心を研ぎ澄まし、明日への物語を紡ぐ。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": "ルーナアーマー",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/406eac5d6fb04d35bb6ae77dba5c69f93a4022d7",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/a12b5edf21ca12fd548e562e0b651b53b6274d1e"
      }
    },
    {
      "id": 25,
      "section": "BP",
      "bundle_version": "01",
      "serial": "016",
      "branch": null,
      "number": "BP01-016",
      "rarity": {
        "value": "400_rrr",
        "description": "RRR"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": 18000,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 319,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "[DBL][TRP]《このキャラの登場時》自分の手札にあるラウンド1以下のシーンカード1枚を公開することで、シーン1つを捨て札にし、公開したシーンカード1枚をシーンエリアに出すことができる。",
        "flavor_text": "誰もがいま巨人の力を目撃する。空と大地を震わせて奇跡のパワーが発動する。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "TSUYOSHI NONAKA",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/901180e1cf4edd230500cd4be07f60b4a800219d",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/4cc8af986d35deb61b216461c5b2e46f99dd64e2"
      }
    },
    {
      "id": 24,
      "section": "BP",
      "bundle_version": "01",
      "serial": "010",
      "branch": null,
      "number": "BP01-010",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 318,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "[SIN]《このキャラの登場時》自分は2枚ドローできる。この効果でドローした時、自分の手札1枚をデッキの下に戻す。",
        "flavor_text": "君にもあるこの力。君にもあるこの勇気。立ち上がれ、ウルトラマンのように。",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/06f3233660416b899446fef8fc53af1fe0a93d56",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/3d952884dd4d4b59f3078bf94f2a573dfc036df6"
      }
    },
    {
      "id": 23,
      "section": "BP",
      "bundle_version": "01",
      "serial": "009",
      "branch": null,
      "number": "BP01-009",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 9000,
      "battle_power_2": 13000,
      "battle_power_3": 17000,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 317,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "-",
        "flavor_text": "悪鬼漂う空も貫く一陣の光弾。俊敏の巨人が悲しみに終止符を打つ。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": "ランバルト光弾",
        "illustrator_name": "Akihiro MIYANO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/2478d1545bf77e6d6a4eacd9a34ab486b96751e6",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/62e5d36b2baa4526e5169f81d3db541bb41e49f9"
      }
    },
    {
      "id": 22,
      "section": "BP",
      "bundle_version": "01",
      "serial": "008",
      "branch": null,
      "number": "BP01-008",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "3",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 13000,
      "battle_power_3": 16000,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 316,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "[DBL][TRP]《このキャラの登場時》相手のキャラ1体を、このターンの間、BP-1000できる。(※BPは0未満にはならない)",
        "flavor_text": "この手の中に集まりゆく光。この胸に高められていく大切なものすべて。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": "デラシウム光流",
        "illustrator_name": "F.M.U",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/565cf8a1946de32433decd8f044e75273ddaff39",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/683362e1591d4269e3a5d3ae0d8c515581f1573b"
      }
    },
    {
      "id": 20,
      "section": "BP",
      "bundle_version": "01",
      "serial": "006",
      "branch": null,
      "number": "BP01-006",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "speed",
        "description": "敏速"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 10000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 314,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "-",
        "flavor_text": "伝説の彼方にも空があった。巨人がいた。そして今も、それは君の目の前にある。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": "スカイタイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/809b90d8970e201d40517b4a4e3dcc7ffc2c395c",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/1005de2da2f7acd3a1a4e6cb874ea9ca40817f56"
      }
    },
    {
      "id": 19,
      "section": "BP",
      "bundle_version": "01",
      "serial": "005",
      "branch": null,
      "number": "BP01-005",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "power",
        "description": "剛力"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 7000,
      "battle_power_2": 11000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 313,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "-",
        "flavor_text": "はるか遠い時の彼方で掴み取った光。それはいまを輝かせる力になる。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": "パワータイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/d9fc32cad132601b2d03b39867cc57da7b436882",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/43f11ab50b4c55d4972a48f2ee1f8a19180f21f3"
      }
    },
    {
      "id": 18,
      "section": "BP",
      "bundle_version": "01",
      "serial": "003",
      "branch": null,
      "number": "BP01-003",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 312,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "-",
        "flavor_text": "何のために戦うのか、分からなければ光を探せ。きっと見えてくるものがある。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": "マルチタイプ",
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/b837eda7e08762feddbec32c7455e3e989a633df",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/14e0e1689ef4f1e85c711cddc7cd3b99cfc7efa4"
      }
    },
    {
      "id": 17,
      "section": "BP",
      "bundle_version": "01",
      "serial": "002",
      "branch": null,
      "number": "BP01-002",
      "rarity": {
        "value": "800_u",
        "description": "U"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 6000,
      "battle_power_2": 8000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 311,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "[SIN]このキャラは、バトル相手のキャラのTYPEが 【剛力】 の間、BPが1グレードアップする。",
        "flavor_text": "3000万年の時を超え、立ち上がる伝説の巨人。君はいま光の奇跡を目撃する。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": "マルチタイプ",
        "illustrator_name": "HUJIWARA HISASHI",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/0d2141ddf963106cd3e71b9864e7e6def1f44566",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/f32bf6dba82ea93c63cbc04d80b3f5e3bef31267"
      }
    },
    {
      "id": 16,
      "section": "BP",
      "bundle_version": "01",
      "serial": "001",
      "branch": null,
      "number": "BP01-001",
      "rarity": {
        "value": "600_r",
        "description": "R"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 1000,
      "battle_power_2": 7000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1996,
      "display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"],
      "detail": {
        "id": 310,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンティガ",
        "ruby": "-",
        "character_name": "ティガ",
        "effect": "[SIN]《このキャラの登場時》自分のデッキの上のカード3枚を公開することで、その中のウルトラヒーローカード1枚を手札に加えることができる。加えなかったカードは捨て札にする。",
        "flavor_text": "僕がティガだ。君がティガさ。消えない希望に気付けたら、君もウルトラマンだ。",
        "participating_works": "ウルトラマンティガ",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "toriyufu",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/28c2bbc9125e2b1eb6e6fb2ccfe2a18b2e2c0198",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/1b6867b52a8ef70f5ddf0d0c3c9ede38e5fe4a08"
      }
    },
    {
      "id": 15,
      "section": "BP",
      "bundle_version": "01",
      "serial": "060",
      "branch": "(PR-011)",
      "number": "(PR-011)BP01-060",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "2",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 8000,
      "battle_power_2": 10000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2009,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 15,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンゼロ",
        "ruby": "-",
        "character_name": "ゼロ",
        "effect": "-",
        "flavor_text": "君の命も、星の命も、変わりはない。必ず守り抜く同じ命。",
        "participating_works": "映画『大怪獣バトル ウルトラ銀河伝説 THE MOVIE』",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/ecd10a894811b5d3f60f7d530191c4ae15a2341d",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/3d635a8fec9fccb9a0802687ef0ea780cad03df9"
      }
    },
    {
      "id": 14,
      "section": "BP",
      "bundle_version": "01",
      "serial": "012",
      "branch": "(PR-010)(02)",
      "number": "(PR-010)(02)BP01-012",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 14,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "-",
        "flavor_text": "想像の力で未来のために──支え、守り、そして戦う！",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/b08a4ff0177aff2aade2309680f705ee111e7ce1",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/1be8ccd31d58a3c5ca713c5169dd213e2f3ebeaa"
      }
    },
    {
      "id": 13,
      "section": "BP",
      "bundle_version": "01",
      "serial": "012",
      "branch": "(PR-010)(01)",
      "number": "(PR-010)(01)BP01-012",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": null,
      "level": "1",
      "type": {
        "value": "basic",
        "description": "基本"
      },
      "feature": {
        "value": "ultra_hero",
        "description": "ウルトラヒーロー"
      },
      "battle_power_1": 5000,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 2024,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 13,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "ウルトラマンアーク",
        "ruby": "-",
        "character_name": "アーク",
        "effect": "-",
        "flavor_text": "想像の力で未来のために──支え、守り、そして戦う！",
        "participating_works": "ウルトラマンアーク",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "TONJI MATSUNO",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/84f1b210f0f0a3813ce78eed58a4d30a43e5c88f",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/57b6c6c0aa8de6d00ad545b9e4f3e873c016987d"
      }
    },
    {
      "id": 12,
      "section": "PR",
      "bundle_version": "",
      "serial": "004",
      "branch": "",
      "number": "PR-004",
      "rarity": {
        "value": "400_rrr",
        "description": "RRR"
      },
      "round": null,
      "level": "5",
      "type": {
        "value": "disaster",
        "description": "災禍"
      },
      "feature": {
        "value": "kaiju",
        "description": "ウルトラ怪獣"
      },
      "battle_power_1": 9000,
      "battle_power_2": 12000,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": 1966,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 12,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "古代怪獣ゴモラ",
        "ruby": "こだいかいじゅう",
        "character_name": "ゴモラ",
        "effect": "[SIN]《このキャラの登場時》このキャラを、このターンの間、BPを1グレードアップできる。",
        "flavor_text": "その剛腕の前に、巨人は崩れ落ちる。しかし、巨人には、“怪獣殿下”がついていた。",
        "participating_works": "ウルトラマン",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": "Kenji Watanabe",
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/e72fdde471a8b321f6e9ef6aa2984a0de5da1244",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/7e234c16a187452d6681bd1cd73037ad5758ef44"
      }
    },
    {
      "id": 11,
      "section": "PR",
      "bundle_version": "",
      "serial": "001",
      "branch": "(11)",
      "number": "(11)PR-001",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "0",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 11,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "Ultraman: Rising",
        "ruby": "-",
        "character_name": "-",
        "effect": "-",
        "flavor_text": "-",
        "participating_works": "Ultraman: Rising",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/650dbe3c2f8acc41b17ea5d5bbd8ea1c6994008a",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/0d44cad2ac4c0a579e58732d04307acedd98b418"
      }
    },
    {
      "id": 10,
      "section": "PR",
      "bundle_version": "",
      "serial": "001",
      "branch": "(10)",
      "number": "(10)PR-001",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "0",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 10,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "Ultraman: Rising",
        "ruby": "-",
        "character_name": "-",
        "effect": "-",
        "flavor_text": "-",
        "participating_works": "Ultraman: Rising",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/11bc4013959f7d66f8965dc94c52d97798a1b555",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/739351d5bea819cefab3e8889e0d4886da71b1c6"
      }
    },
    {
      "id": 9,
      "section": "PR",
      "bundle_version": "",
      "serial": "001",
      "branch": "(09)",
      "number": "(09)PR-001",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "0",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 9,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "Ultraman: Rising",
        "ruby": "-",
        "character_name": "-",
        "effect": "-",
        "flavor_text": "-",
        "participating_works": "Ultraman: Rising",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/4111289dc6d69a7ea439ba35b1c998ef62022d08",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/b01cf14db75223f513da8c20ee492060b5eb2c13"
      }
    },
    {
      "id": 8,
      "section": "PR",
      "bundle_version": "",
      "serial": "001",
      "branch": "(08)",
      "number": "(08)PR-001",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "0",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 8,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "Ultraman: Rising",
        "ruby": "-",
        "character_name": "-",
        "effect": "-",
        "flavor_text": "-",
        "participating_works": "Ultraman: Rising",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/fbc8db41dac848563581bf2be7a7f9e3bf652268",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/566a838be05db835fef86aa3bca42f5722ac9836"
      }
    },
    {
      "id": 7,
      "section": "PR",
      "bundle_version": "",
      "serial": "001",
      "branch": "(07)",
      "number": "(07)PR-001",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "0",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 7,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "Ultraman: Rising",
        "ruby": "-",
        "character_name": "-",
        "effect": "-",
        "flavor_text": "-",
        "participating_works": "Ultraman: Rising",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/74dc78940656326666346b39f5ee9a16f1563757",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/59cbb27816a284b799a5e3cb3cb3c0b6552bb899"
      }
    },
    {
      "id": 6,
      "section": "PR",
      "bundle_version": "",
      "serial": "001",
      "branch": "(06)",
      "number": "(06)PR-001",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "0",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 6,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "Ultraman: Rising",
        "ruby": "-",
        "character_name": "-",
        "effect": "-",
        "flavor_text": "-",
        "participating_works": "Ultraman: Rising",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/14953de796cb3b2111a8de79d3f7d33ba5e45511",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/1d32dfac63ee07272408f48c2c59ac1c0258f55a"
      }
    },
    {
      "id": 5,
      "section": "PR",
      "bundle_version": "",
      "serial": "001",
      "branch": "(05)",
      "number": "(05)PR-001",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "0",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 5,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "Ultraman: Rising",
        "ruby": "-",
        "character_name": "-",
        "effect": "-",
        "flavor_text": "-",
        "participating_works": "Ultraman: Rising",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/dc489bc2e080408a4d662c88d12e8e0920d41013",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/46a03b2dd876c6836441f7fb103c2e69dbc9763a"
      }
    },
    {
      "id": 4,
      "section": "PR",
      "bundle_version": "",
      "serial": "001",
      "branch": "(04)",
      "number": "(04)PR-001",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "0",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 4,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "Ultraman: Rising",
        "ruby": "-",
        "character_name": "-",
        "effect": "-",
        "flavor_text": "-",
        "participating_works": "Ultraman: Rising",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/bd4e2e1c4b6327c9c44dad10e89951f0e484f70d",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/8fd2ac2735f7a2e36ee473c3594119a4cce7cd40"
      }
    },
    {
      "id": 3,
      "section": "PR",
      "bundle_version": "",
      "serial": "001",
      "branch": "(03)",
      "number": "(03)PR-001",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "0",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 3,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "Ultraman: Rising",
        "ruby": "-",
        "character_name": "-",
        "effect": "-",
        "flavor_text": "-",
        "participating_works": "Ultraman: Rising",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/98637e7a94d39196c9082ee05b58c9eada7595f7",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/29428add75e95320d91e178bc0781ca0db3b2dd0"
      }
    },
    {
      "id": 2,
      "section": "PR",
      "bundle_version": "",
      "serial": "001",
      "branch": "(02)",
      "number": "(02)PR-001",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "0",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 2,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "Ultraman: Rising",
        "ruby": "-",
        "character_name": "-",
        "effect": "-",
        "flavor_text": "-",
        "participating_works": "Ultraman: Rising",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/89a392f2788b02a061bee3ff2a1b6808df81c575",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/7ea8a446bea0320eee6aba88ad4934729e60bc69"
      }
    },
    {
      "id": 1,
      "section": "PR",
      "bundle_version": "",
      "serial": "001",
      "branch": "(01)",
      "number": "(01)PR-001",
      "rarity": {
        "value": "900_c",
        "description": "C"
      },
      "round": "0",
      "level": null,
      "type": null,
      "feature": {
        "value": "scene",
        "description": "シーン"
      },
      "battle_power_1": null,
      "battle_power_2": null,
      "battle_power_3": null,
      "battle_power_ex": null,
      "publication_year": null,
      "display_card_bundle_names": ["PRカード"],
      "detail": {
        "id": 1,
        "product_language": {
          "value": "ja",
          "description": "日本語"
        },
        "name": "Ultraman: Rising",
        "ruby": "-",
        "character_name": "-",
        "effect": "-",
        "flavor_text": "-",
        "participating_works": "Ultraman: Rising",
        "participating_works_url": null,
        "type_name": null,
        "illustrator_name": null,
        "image_url": "https://api.ultraman-cardgame.com/api/v1/media/ac1e9d26d1c382227459c600984562b84cb6549d",
        "thumbnail_image_url": "https://api.ultraman-cardgame.com/api/v1/media/0b8a72a6d1402a15a4f5d0eb41fe41a84ca7ddc8"
      }
    }
  ]
}

"""


# JSONデータをPythonの辞書に変換
data = json.loads(data_json)

# 特殊文字をエスケープする関数
def escape_sql(value):
    if value is None:
        return "NULL"
    return f"'{str(value).replace('\'', '\'\'')}'"  # シングルクォートを2つに置換

# INSERT文を生成する関数
def generate_sql(data):
    inserts = []

    for card in data['data']:
        # 安全に取得する関数
        def get_value(obj, key, default="NULL"):
            return escape_sql(obj[key]) if obj and obj.get(key) is not None else default

        # メインテーブル(cards)のINSERT文
        inserts.append(f"""
        INSERT INTO cards (
            id, section, bundle_version, serial, branch, number, 
            rarity_value, rarity_description, round, level, 
            type_value, type_description, feature_value, feature_description, 
            battle_power_1, battle_power_2, battle_power_3, battle_power_ex, 
            publication_year, display_card_bundle_names, detail_id,
            product_language_value, product_language_description, detail_name, 
            ruby, character_name, effect, flavor_text, participating_works, 
            participating_works_url, type_name, illustrator_name, 
            image_url, thumbnail_image_url
        ) VALUES (
            {card['id']},
            {escape_sql(card['section'])},
            {escape_sql(card['bundle_version'])},
            {escape_sql(card['serial'])},
            {escape_sql(card['branch'])},
            {escape_sql(card['number'])},
            {escape_sql(card['rarity']['value'])},
            {escape_sql(card['rarity']['description'])},
            {card['round'] if card['round'] is not None else "NULL"},
            {escape_sql(card['level']) if card['level'] else "NULL"},
            {get_value(card.get('type'), 'value')},
            {get_value(card.get('type'), 'description')},
            {escape_sql(card['feature']['value'])},
            {escape_sql(card['feature']['description'])},
            {card['battle_power_1'] if card['battle_power_1'] is not None else "NULL"},
            {card['battle_power_2'] if card['battle_power_2'] is not None else "NULL"},
            {card['battle_power_3'] if card['battle_power_3'] is not None else "NULL"},
            {card['battle_power_ex'] if card['battle_power_ex'] is not None else "NULL"},
            {card['publication_year'] if card['publication_year'] is not None else "NULL"},
            {escape_sql(json.dumps(card['display_card_bundle_names']))},
            {card['detail']['id']},
            {escape_sql(card['detail']['product_language']['value'])},
            {escape_sql(card['detail']['product_language']['description'])},
            {escape_sql(card['detail']['name'])},
            {escape_sql(card['detail']['ruby'])},
            {escape_sql(card['detail']['character_name'])},
            {escape_sql(card['detail']['effect'])},
            {escape_sql(card['detail']['flavor_text'])},
            {escape_sql(card['detail']['participating_works'])},
            {escape_sql(card['detail']['participating_works_url']) if card['detail']['participating_works_url'] else "NULL"},
            {escape_sql(card['detail']['type_name']) if card['detail']['type_name'] else "NULL"},
            {escape_sql(card['detail']['illustrator_name'])},
            {escape_sql(card['detail']['image_url'])},
            {escape_sql(card['detail']['thumbnail_image_url'])}
        );
        """)

    return inserts

# SQL分割してファイル出力
def split_and_save_sql(inserts, chunk_size=50, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    for i in range(0, len(inserts), chunk_size):
        part_number = i // chunk_size + 1
        chunk = inserts[i:i + chunk_size]
        file_name = os.path.join(output_dir, f"insert_cards_part_{part_number}.sql")

        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(chunk))

        print(f"File {file_name} created with {len(chunk)} statements.")

# メイン処理
inserts = generate_sql(data)
split_and_save_sql(inserts, chunk_size=50)