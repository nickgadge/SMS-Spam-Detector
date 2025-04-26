document.addEventListener('DOMContentLoaded', function() {
    const textInput = document.getElementById('textInput');
    const convertBtn = document.getElementById('convertBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const statusDiv = document.getElementById('status');
    const audioContainer = document.getElementById('audioContainer');
    const audioPlayer = document.getElementById('audioPlayer');
    const audioSource = document.getElementById('audioSource');

    convertBtn.addEventListener('click', async function() {
        const text = textInput.value.trim();

        if (!text) {
            statusDiv.textContent = "Please enter some text first!";
            statusDiv.style.color = 'red';
            return;
        }

        // Reset UI
        statusDiv.textContent = "Converting text to speech...";
        statusDiv.style.color = 'blue';
        convertBtn.disabled = true;
        downloadBtn.style.display = 'none';
        audioContainer.style.display = 'none';
        audioPlayer.pause();

        try {
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `text=${encodeURIComponent(text)}`
            });

            const result = await response.json();

            if (result.status === 'success') {
                statusDiv.textContent = "Conversion successful!";
                statusDiv.style.color = 'green';

                // Set up download button
                downloadBtn.href = result.download_url;
                downloadBtn.style.display = 'inline-block';

                // Set up audio player
                audioSource.src = result.play_url;
                audioPlayer.load();
                audioContainer.style.display = 'block';

                // Optional: Auto-play (may be blocked by browser policies)
                audioPlayer.play().catch(e => {
                    console.log("Auto-play prevented:", e);
                });
            } else {
                statusDiv.textContent = "Error: " + (result.message || "Conversion failed");
                statusDiv.style.color = 'red';
            }
        } catch (error) {
            statusDiv.textContent = "Network error: " + error.message;
            statusDiv.style.color = 'red';
        } finally {
            convertBtn.disabled = false;
        }
    });
});