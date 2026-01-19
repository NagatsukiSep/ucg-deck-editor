type OptionEntry = {
  value: string;
  labelKey: string;
};

export const ultraCharacter: OptionEntry[] = [
  { value: "アーク", labelKey: "character.ultra.arc" },
  { value: "アグル", labelKey: "character.ultra.agul" },
  { value: "エックス", labelKey: "character.ultra.x" },
  { value: "オーブ", labelKey: "character.ultra.orb" },
  { value: "オメガ", labelKey: "character.ultra.omega" },
  { value: "ガイア", labelKey: "character.ultra.gaia" },
  { value: "ギンガ", labelKey: "character.ultra.ginga" },
  { value: "サトウ ケン", labelKey: "character.ultra.satoKen" },
  { value: "サトウ ハヤオ", labelKey: "character.ultra.satoHayao" },
  { value: "ジード", labelKey: "character.ultra.geed" },
  { value: "ゼット", labelKey: "character.ultra.z" },
  { value: "ゼロ", labelKey: "character.ultra.zero" },
  { value: "ダイナ", labelKey: "character.ultra.dyna" },
  { value: "ティガ", labelKey: "character.ultra.tiga" },
  { value: "デッカー", labelKey: "character.ultra.decker" },
  { value: "トリガー", labelKey: "character.ultra.trigger" },
  { value: "ネクサス", labelKey: "character.ultra.nexus" },
  { value: "ヒカリ", labelKey: "character.ultra.hikari" },
  { value: "ビクトリー", labelKey: "character.ultra.victory" },
  { value: "ブル", labelKey: "character.ultra.blu" },
  { value: "ブレーザー", labelKey: "character.ultra.blazar" },
  { value: "マックス", labelKey: "character.ultra.max" },
  { value: "メビウス", labelKey: "character.ultra.mebius" },
  { value: "ロッソ", labelKey: "character.ultra.rosso" },
];

export const ultraMechaCharacter: OptionEntry[] = [
  { value: "アースガロン", labelKey: "character.mecha.earthGaron" },
  { value: "セブンガー", labelKey: "character.mecha.sevenger" },
];

export const kaijuCharacter: OptionEntry[] = [
  { value: "ギルアーク", labelKey: "character.kaiju.gilArc" },
  { value: "ジャグラス ジャグラー", labelKey: "character.kaiju.jugglusJuggler" },
  { value: "ベリアル", labelKey: "character.kaiju.belial" },
];

export const cardTypes: Array<{ value: string; labelKey: string }> = [
  { value: "basic", labelKey: "cardType.basic" },
  { value: "power", labelKey: "cardType.power" },
  { value: "armed", labelKey: "cardType.armed" },
  { value: "speed", labelKey: "cardType.speed" },
  { value: "disaster", labelKey: "cardType.disaster" },
  { value: "devastation", labelKey: "cardType.devastation" },
  { value: "invasion", labelKey: "cardType.invasion" },
  { value: "meteo", labelKey: "cardType.meteo" },
];
