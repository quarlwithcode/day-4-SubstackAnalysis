// Load influencers and transcripts on page load
document.addEventListener('DOMContentLoaded', () => {
    loadInfluencers();
    loadTranscripts();
});

// Handle form submission
document.getElementById('transcriptForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const spinner = document.getElementById('spinner');
    const messageDiv = document.getElementById('message');
    
    // Get form data
    const formData = {
        url: document.getElementById('url').value,
        influencer: document.getElementById('influencer').value,
        title: document.getElementById('title').value
    };
    
    // Show loading state
    submitBtn.disabled = true;
    btnText.textContent = 'Downloading...';
    spinner.classList.remove('hidden');
    messageDiv.classList.add('hidden');
    
    try {
        const response = await fetch('/download_transcript', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Show success message
            showMessage(`✅ ${data.message} (${data.word_count} words)`, 'success');
            
            // Clear form
            document.getElementById('transcriptForm').reset();
            
            // Reload transcripts list
            loadTranscripts();
            
            // Reload influencers (in case new one was added)
            loadInfluencers();
        } else {
            // Show error message
            showMessage(`❌ Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showMessage(`❌ Error: ${error.message}`, 'error');
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        btnText.textContent = 'Download Transcript';
        spinner.classList.add('hidden');
    }
});

// Handle refresh button
document.getElementById('refreshBtn').addEventListener('click', () => {
    loadTranscripts();
});

// Load influencers for datalist
async function loadInfluencers() {
    try {
        const response = await fetch('/get_influencers');
        const influencers = await response.json();
        
        const datalist = document.getElementById('influencersList');
        datalist.innerHTML = '';
        
        influencers.forEach(influencer => {
            const option = document.createElement('option');
            // Convert slug format to proper name
            const properName = influencer.split('-').map(word => 
                word.charAt(0).toUpperCase() + word.slice(1)
            ).join(' ');
            option.value = properName;
            datalist.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading influencers:', error);
    }
}

// Load transcripts list
async function loadTranscripts() {
    const listDiv = document.getElementById('transcriptsList');
    listDiv.innerHTML = '<div class="loading">Loading transcripts...</div>';
    
    try {
        const response = await fetch('/list_transcripts');
        const transcripts = await response.json();
        
        if (transcripts.length === 0) {
            listDiv.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📄</div>
                    <p>No transcripts downloaded yet</p>
                </div>
            `;
        } else {
            listDiv.innerHTML = transcripts.map(transcript => `
                <div class="transcript-item">
                    <div class="transcript-name">${transcript.name}</div>
                    <div class="transcript-meta">
                        <span>📦 ${transcript.size}</span>
                        <span>📅 ${transcript.modified}</span>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        listDiv.innerHTML = '<div class="error">Error loading transcripts</div>';
        console.error('Error loading transcripts:', error);
    }
}

// Show message
function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.classList.remove('hidden');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        messageDiv.classList.add('hidden');
    }, 5000);
}

// Auto-refresh transcripts list every 30 seconds
setInterval(loadTranscripts, 30000);