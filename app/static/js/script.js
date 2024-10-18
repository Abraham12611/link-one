document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent form submission
  
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
  
    if (!file) {
      document.getElementById('message').textContent = 'Please select a file.';
      return;
    }
  
    const formData = new FormData();
    formData.append('file', file);
  
    // Send file to the backend using Fetch API
    fetch('/upload', { // Replace '/upload' with your actual backend API endpoint
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          document.getElementById('message').textContent = 'File uploaded successfully!';
        } else {
          document.getElementById('message').textContent = 'File upload failed. Please try again.';
        }
      })
      .catch(error => {
        document.getElementById('message').textContent = 'An error occurred. Please try again.';
        console.error('Error:', error);
      });
  });
  