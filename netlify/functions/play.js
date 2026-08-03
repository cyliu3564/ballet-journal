exports.handler = async (event, context) => {
  const songId = event.queryStringParameters?.id;
  if (!songId || !/^\d+$/.test(songId)) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Invalid song ID' }) };
  }

  try {
    // Get the redirect URL from NetEase
    const res = await fetch(`https://music.163.com/song/media/outer/url?id=${songId}.mp3`, {
      redirect: 'manual',
    });

    let audioUrl = res.headers.get('location');
    if (!audioUrl) {
      return { statusCode: 404, body: JSON.stringify({ error: 'Song not found' }) };
    }

    // Force HTTPS on the CDN URL
    audioUrl = audioUrl.replace(/^http:\/\//, 'https://');

    // Stream the audio back with CORS headers
    const audioRes = await fetch(audioUrl, {
      headers: {
        'Range': event.headers?.range || '',
      },
    });

    const headers = {
      'Content-Type': 'audio/mpeg',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'public, max-age=3600',
    };

    if (audioRes.headers.get('content-length')) {
      headers['Content-Length'] = audioRes.headers.get('content-length');
    }
    if (audioRes.headers.get('accept-ranges')) {
      headers['Accept-Ranges'] = 'bytes';
    }
    if (audioRes.headers.get('content-range')) {
      headers['Content-Range'] = audioRes.headers.get('content-range');
    }

    return {
      statusCode: audioRes.status,
      headers,
      body: await audioRes.text(),
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
