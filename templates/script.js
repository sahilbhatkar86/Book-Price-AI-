document.getElementById('analyzeBtn').addEventListener('click', async function() {
    // Get the selected file
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select an image.');
        return;
    }

    // Show loading spinner
    document.getElementById('loading').style.display = 'block';

    // Hide result section initially
    document.getElementById('result').style.display = 'none';

    // Prepare FormData to send with the image
    const formData = new FormData();
    formData.append('image', file);

    try {
        // Send the image to the API
        const response = await fetch('https://book-price-ai.onrender.com/predict', {
            method: 'POST',
            body: formData
        });

        // Hide loading spinner after the request completes
        document.getElementById('loading').style.display = 'none';

        // Check if the request was successful
        if (response.ok) {
            const data = await response.json();
            // Update result section with the API response
            document.getElementById('stage').textContent = data.stage;
            document.getElementById('activity').textContent = data.activity;
            document.getElementById('components').textContent = data.components;
            document.getElementById('subStageProgress').textContent = JSON.stringify(data.sub_stage_progress);
            document.getElementById('overallProgress').textContent = data.overall_progress;

            // Show the result section
            document.getElementById('result').style.display = 'block';
        } else {
            alert('Error: ' + response.statusText);
        }
    } catch (error) {
        // Hide the spinner if error occurs
        document.getElementById('loading').style.display = 'none';
        alert('Error during the analysis: ' + error.message);
    }
});
