import posts from "../data/sentiment_output";

export const AVAILABLE_KEYWORDS = {
  VeroVolley: ["monza", "verovolley", "vero volley", "allianz milano"],
  egonu: null,
  orro: null,
  danesi: null,
  larson: null,
  sylla: null,
  cazaute: null,
  malual: null,
  heyrman: null,
  folie: null,
  prandi: null,
  pusic: null,
  rettke: null,
  bajema: null,
  daalderop: null,
  candi: null,
  castillo: null,
};

export const AVAILABLE_PLATFORMS = [
  { name: "Facebook", key: "FB" },
  { name: "Instagram", key: "IG" },
  { name: "Web", key: "Web" },
];

export default function getProcessedPosts() {
  return posts;
}
