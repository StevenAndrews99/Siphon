function detectPlatform(url) {
    const infoDiv = document.getElementById('platform-info');
    const metadataDiv = document.getElementById('video-metadata');
    const loading = document.getElementById('loading');
    const lower = url.toLowerCase();

    // Detect platform
    if (lower.includes("youtube.com") || lower.includes("youtu.be")) {
        infoDiv.innerText = "Platform Detected: YouTube";
    } else if (lower.includes("tiktok.com")) {
        infoDiv.innerText = "Platform Detected: TikTok";
    } else if (lower.includes("instagram.com")) {
        infoDiv.innerText = "Platform Detected: Instagram";
    } else {
        infoDiv.innerText = "Platform: Unknown";
    }

    // If input is valid, fetch metadata
    if (url.trim() !== "") {
        loading.style.display = 'block';
        metadataDiv.style.display = 'none';

        fetch('/fetch_metadata', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        })
        .then(res => res.json())
        .then(data => {
            loading.style.display = 'none';

            if (data.error) {
                metadataDiv.style.display = 'none';
            } else {
                document.getElementById('video-thumbnail').src = data.thumbnail;
                document.getElementById('video-title').innerText = data.title;
                document.getElementById('video-duration').innerText = data.duration;
                metadataDiv.style.display = 'block';
            }
        })
        .catch(() => {
            loading.style.display = 'none';
            metadataDiv.style.display = 'none';
        });
    } else {
        loading.style.display = 'none';
        metadataDiv.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const loadingIndicator = document.getElementById('download-loading');
    const submitButton = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function () {
        loadingIndicator.style.display = 'block';
        submitButton.disabled = true;
        submitButton.innerText = 'Downloading...';
    });
});

