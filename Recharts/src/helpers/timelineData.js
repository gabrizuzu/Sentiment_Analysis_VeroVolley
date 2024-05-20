import getProcessedPosts from "./formatData";

const monthLabels = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

const seasonStart = 8;

// - Comments
export function countSentimentComments(platforms, keywords) {
  const posts = getProcessedPosts();
  const count = {
    "2020/2021": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    "2021/2022": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    "2022/2023": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    "2023/2024": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
  };

  for (const post of posts) {
    if (
      !platforms.includes(post.platform) ||
      !keywords.some((keyword) => post.keywords.includes(keyword))
    ) {
      continue;
    }
    const comments = post.comments || [];

    for (const comment of comments) {
      if (!comment.author.includes("verovolley")) {
        const season = comment.season;
        const mese = comment.mese - 1;
        const sentiment = comment.sentiment_comment;

        if (count[season]) {
          if (sentiment === "positive")
            count[season].positive[(mese + 12 - seasonStart) % 12] += 1;
          else if (sentiment === "negative")
            count[season].negative[(mese + 12 - seasonStart) % 12] += 1;
          else if (sentiment === "neutral")
            count[season].neutral[(mese + 12 - seasonStart) % 12] += 1;
        }
      }
    }
  }

  return count;
}

// - Posts
export function countSentimentPosts(platforms, keywords) {
  const posts = getProcessedPosts();
  const count = {
    "2020/2021": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    "2021/2022": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    "2022/2023": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    "2023/2024": {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
  };

  for (const post of posts) {
    if (
      !platforms.includes(post.platform) ||
      !keywords.some((keyword) => post.keywords.includes(keyword))
    ) {
      continue;
    }
    const season = post.season;
    const mese = post.mese - 1;
    const sentiment = post.sentiment_post;

    if (count[season]) {
      if (sentiment === "positive")
        count[season].positive[(mese + 12 - seasonStart) % 12] += 1;
      else if (sentiment === "negative")
        count[season].negative[(mese + 12 - seasonStart) % 12] += 1;
      else if (sentiment === "neutral")
        count[season].neutral[(mese + 12 - seasonStart) % 12] += 1;
    }
  }

  return count;
}

export function getTimelineData(
  season,
  platforms,
  keywords,
  usePosts = true,
  usePercentage = false
) {
  let count;
  if (usePosts) {
    count = countSentimentPosts(platforms, keywords);
  } else {
    count = countSentimentComments(platforms, keywords);
  }

  const data = [];

  for (const index of [...Array(12).keys()]) {
    let positive = count[season].positive[index];
    let negative = count[season].negative[index];
    let neutral = count[season].neutral[index];

    if (usePercentage) {
      const total = positive + negative + neutral;
      positive = Math.round((positive * 100) / total) || 0;
      negative = Math.round((negative * 100) / total) || 0;
      neutral = total > 0 ? 100 - positive - negative : 0;
    }

    data.push({
      month: monthLabels[(index + seasonStart) % 12],
      positive,
      negative,
      neutral,
    });
  }

  return data;
}
