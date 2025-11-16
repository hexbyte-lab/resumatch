let selectedFile = null;

function handleFileSelect(event) {
    selectedFile = event.target.files[0];
    const fileNameDiv = document.getElementById('fileName');
    const resumeTextarea = document.getElementById('resume');
    
    if (selectedFile) {
        fileNameDiv.textContent = `Selected: ${selectedFile.name}`;
        // Clear and disable the text area when file is selected
        resumeTextarea.value = '';
        resumeTextarea.disabled = true;
        resumeTextarea.placeholder = 'File upload selected. Remove file to use text input.';
        resumeTextarea.style.backgroundColor = '#f0f0f0';
        resumeTextarea.style.cursor = 'not-allowed';
    } else {
        fileNameDiv.textContent = '';
        // Re-enable textarea if no file
        resumeTextarea.disabled = false;
        resumeTextarea.placeholder = 'Paste your resume text here...';
        resumeTextarea.style.backgroundColor = '';
        resumeTextarea.style.cursor = '';
    }
}

function clearForm() {
    // Clear file upload
    const fileInput = document.getElementById('resumeFile');
    fileInput.value = '';
    selectedFile = null;
    document.getElementById('fileName').textContent = '';
    
    // Re-enable and clear resume textarea
    const resumeTextarea = document.getElementById('resume');
    resumeTextarea.value = '';
    resumeTextarea.disabled = false;
    resumeTextarea.placeholder = 'Paste your resume text here...';
    resumeTextarea.style.backgroundColor = '';
    resumeTextarea.style.cursor = '';
    
    // Clear job description
    document.getElementById('jobDesc').value = '';
}

async function analyzeResume() {
    const resumeText = document.getElementById('resume').value.trim();
    const jobDesc = document.getElementById('jobDesc').value.trim();
    
    // Reset UI
    document.getElementById('results').classList.remove('show');
    document.getElementById('error').classList.remove('show');
    document.getElementById('resumePreview').style.display = 'none';
    
    // Validation
    if (!selectedFile && !resumeText) {
        showError('Please upload a resume file or paste resume text');
        return;
    }
    
    if (!jobDesc) {
        showError('Please enter a job description');
        return;
    }
    
    // Show loading
    document.getElementById('loading').classList.add('show');
    document.getElementById('analyzeBtn').disabled = true;
    
    try {
        let response;
        
        // If file is uploaded, use file upload endpoint
        if (selectedFile) {
            const formData = new FormData();
            formData.append('resume_file', selectedFile);
            formData.append('job_description', jobDesc);
            
            response = await fetch('http://localhost:5000/api/analyze-file', {
                method: 'POST',
                body: formData
            });
        } else {
            // Otherwise use text endpoint
            response = await fetch('http://localhost:5000/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    resume: resumeText,
                    job_description: jobDesc
                })
            });
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.data, data.resume_preview);
            // Clear form after successful analysis
            clearForm();
        } else {
            showError(data.error || 'An error occurred');
        }
    } catch (error) {
        showError('Failed to connect to API. Make sure the server is running.');
        console.error(error);
    } finally {
        document.getElementById('loading').classList.remove('show');
        document.getElementById('analyzeBtn').disabled = false;
    }
}

function displayResults(data, resumePreview) {
    document.getElementById('score').textContent = data.match_score + '%';
    document.getElementById('missingCount').textContent = data.total_missing;
    
    const keywordsList = document.getElementById('keywordsList');
    keywordsList.innerHTML = '';
    
    if (data.missing_keywords.length === 0) {
        keywordsList.innerHTML = '<p>No missing keywords! Great match!</p>';
    } else {
        data.missing_keywords.forEach(keyword => {
            const tag = document.createElement('span');
            tag.className = 'keyword-tag';
            tag.textContent = keyword;
            keywordsList.appendChild(tag);
        });
    }
    
    // Show resume preview if available (from file upload)
    if (resumePreview) {
        document.getElementById('previewText').textContent = resumePreview;
        document.getElementById('resumePreview').style.display = 'block';
    }
    
    document.getElementById('results').classList.add('show');
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.add('show');
}