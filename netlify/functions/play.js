exports.handler = async (event, context) => {
  const songId = event.queryStringParameters?.id;
  if (!songId || !/^\d+$/.test(songId)) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Invalid song ID' }) };
  }

  try {
    const res = await fetch(`https://music.163.com/song/media/outer/url?id=${songId}.mp3`, {
      redirect: 'manual',
    });

    let audioUrl = res.headers.get('location');
    if (!audioUrl) {
      return { statusCode: 404, body: JSON.stringify({ error: 'Song not found' }) };
    }

    // Force HTTPS on CDN URL
    audioUrl = audioUrl.replace(/^http:\/\//, 'https://');

    // Redirect browser directly to HTTPS CDN
    return {
      statusCode: 302,
      headers: {
        'Location': audioUrl,
        'Cache-Control': 'public, max-age=3600',
      },
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
