document.getElementById('imageUpload').addEventListener('change', function() {
    // Get the selected file
    const file = this.files[0];
    
    // Check if a file is selected
    if (file) {
        // Create a URL for the image file
        const imgURL = URL.createObjectURL(file);

        // Get the image element for preview
        const imagePreview = document.getElementById('imagePreview');
        
        // Set the image source to the created URL
        imagePreview.src = imgURL;

        // Display the preview image section
        document.getElementById('previewContainer').style.display = 'block';
    }
});

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
            const data = await response.json();  // Get response as JSON
            
            // Extract the relevant part of the response
            const bookDescription = data.result;  // Assuming 'result' contains the description you need

            // Display the book description in the result section
            document.getElementById('result').innerHTML = `<p>${bookDescription}</p>`;
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
