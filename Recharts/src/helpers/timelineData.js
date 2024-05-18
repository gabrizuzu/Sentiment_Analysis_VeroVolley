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
// - Comments
export function countSentimentComments(platforms) {
  const posts = getProcessedPosts();
  const count = {
    2021: {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    2022: {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    2023: {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    2024: {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
  };

  for (const post of posts) {
    if (!platforms.includes(post.platform)) {
      continue;
    }
    const comments = post.comments || [];

    for (const comment of comments) {
      if (!comment.author.includes("verovolley")) {
        const anno = comment.anno;
        const mese = comment.mese;
        const sentiment = comment.sentiment_comment;

        if (count[anno]) {
          if (sentiment === "positive") count[anno].positive[mese - 1] += 1;
          else if (sentiment === "negative")
            count[anno].negative[mese - 1] += 1;
          else if (sentiment === "neutral") count[anno].neutral[mese - 1] += 1;
        }
      }
    }
  }

  return count;
}

// - Posts
export function countSentimentPosts(platforms) {
  const posts = getProcessedPosts();
  const count = {
    2021: {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    2022: {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    2023: {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
    2024: {
      positive: new Array(12).fill(0),
      negative: new Array(12).fill(0),
      neutral: new Array(12).fill(0),
    },
  };

  for (const post of posts) {
    if (!platforms.includes(post.platform)) {
      continue;
    }
    const anno = post.anno;
    const mese = post.mese;
    const sentiment = post.sentiment_post;

    if (count[anno]) {
      if (sentiment === "positive") count[anno].positive[mese - 1] += 1;
      else if (sentiment === "negative") count[anno].negative[mese - 1] += 1;
      else if (sentiment === "neutral") count[anno].neutral[mese - 1] += 1;
    }
  }

  return count;
}

export function getTimelineData(year, platforms, isComments = false) {
  let count;
  if (isComments) {
    count = countSentimentComments(platforms);
  } else {
    count = countSentimentPosts(platforms);
  }

  const data = [];

  for (const month of [...Array(12).keys()]) {
    data.push({
      month: monthLabels[month],
      positive: count[year].positive[month],
      negative: count[year].negative[month],
      neutral: count[year].neutral[month],
    });
  }

  return data;
}
