document.addEventListener('DOMContentLoaded', () => {
    const uploadSection = document.getElementById('uploadSection');
    const resultsSection = document.getElementById('resultsSection');
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const fileNameDisplay = document.getElementById('fileName');
    const jobDescription = document.getElementById('jobDescription');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const newAnalysisBtn = document.getElementById('newAnalysisBtn');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');

    let selectedFile = null;

    // --- Drag and Drop Handlers ---
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('active'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('active'), false);
    });

    dropZone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    }

    // --- File Input Handlers ---
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        const allowedTypes = ['.pdf', '.docx', '.txt', '.doc'];
        const extension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(extension)) {
            alert('Invalid file type. Please upload a PDF, DOCX, or TXT file.');
            return;
        }

        selectedFile = file;
        fileNameDisplay.textContent = `Selected: ${file.name}`;
        validateForm();
    }

    // --- Form Validation ---
    function validateForm() {
        const hasFile = selectedFile !== null;
        const hasJD = jobDescription.value.trim().length > 50;
        analyzeBtn.disabled = !(hasFile && hasJD);
    }

    jobDescription.addEventListener('input', validateForm);

    // --- Analysis ---
    analyzeBtn.addEventListener('click', async () => {
        if (!selectedFile || !jobDescription.value.trim()) return;

        showLoading('Uploading and processing resume...');

        try {
            // 1. Upload Resume
            const formData = new FormData();
            formData.append('file', selectedFile);

            const uploadResponse = await fetch('/api/upload-resume', {
                method: 'POST',
                body: formData
            });

            if (!uploadResponse.ok) {
                const error = await uploadResponse.json();
                throw new Error(error.error || 'Upload failed');
            }

            const uploadData = await uploadResponse.json();
            const resumeId = uploadData.resume_id;

            // 2. Engaging Loading Sequence
            const genericMessages = [
                'Decoding resume structure...',
                'Mapping technical competencies...',
                'Synthesizing career insights...',
                'Matching with job requirements...'
            ];

            let msgIndex = 0;
            const msgInterval = setInterval(() => {
                updateLoadingStatus(genericMessages[msgIndex % genericMessages.length]);
                msgIndex++;
            }, 2500);

            // Wait 10 seconds for vector index synchronization
            await new Promise(resolve => setTimeout(resolve, 30000));
            clearInterval(msgInterval);
            
            updateLoadingStatus('Finalizing AI-powered evaluation...');
            
            const analyzeResponse = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    resume_id: resumeId,
                    job_description: jobDescription.value.trim()
                })
            });

            if (!analyzeResponse.ok) {
                const error = await analyzeResponse.json();
                throw new Error(error.error || 'Analysis failed');
            }

            const analysisData = await analyzeResponse.json();
            displayResults(analysisData.analysis);

        } catch (error) {
            console.error(error);
            alert(`Error: ${error.message}`);
            hideLoading();
        }
    });

    // --- Results Display ---
    function displayResults(data) {
        // Switch sections
        uploadSection.classList.remove('active');
        resultsSection.classList.add('active');
        window.scrollTo(0, 0);
        hideLoading();

        // Animate Scores
        animateScore('matchScore', 'matchScoreRing', data.match_score);
        animateScore('atsScore', 'atsScoreRing', data.ats_score);

        // Skills
        const matchedSkillsContainer = document.getElementById('matchedSkills');
        const missingSkillsContainer = document.getElementById('missingSkills');
        
        matchedSkillsContainer.innerHTML = data.matched_skills.map(skill => 
            `<span class="skill-badge matched">${skill}</span>`
        ).join('');
        
        missingSkillsContainer.innerHTML = data.missing_skills.length > 0 
            ? data.missing_skills.map(skill => `<span class="skill-badge missing">${skill}</span>`).join('')
            : '<p class="no-data">No major skills missing!</p>';

        // Lists
        renderList('strengths', data.strengths);
        renderList('weaknesses', data.weaknesses);
        renderList('improvements', data.improvements);

        // Reasoning
        document.getElementById('reasoning').textContent = data.reasoning;
    }

    function animateScore(valueId, ringId, targetValue) {
        const element = document.getElementById(valueId);
        const ring = document.getElementById(ringId);
        const circumference = 2 * Math.PI * 45; // r=45

        let current = 0;
        const duration = 1500;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing
            const easedProgress = 1 - Math.pow(1 - progress, 3);
            current = Math.floor(easedProgress * targetValue);
            
            element.textContent = current;
            
            const offset = circumference - (easedProgress * targetValue / 100) * circumference;
            ring.style.strokeDashoffset = offset;

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        
        // Dynamic color
        if (targetValue >= 80) ring.style.stroke = 'var(--success)';
        else if (targetValue >= 60) ring.style.stroke = 'var(--warning)';
        else ring.style.stroke = 'var(--danger)';

        requestAnimationFrame(update);
    }

    function renderList(id, items) {
        const container = document.getElementById(id);
        if (!items || items.length === 0) {
            container.innerHTML = '<li>None identified</li>';
            return;
        }
        container.innerHTML = items.map(item => `<li>${item}</li>`).join('');
    }

    // --- Helpers ---
    function showLoading(text) {
        loadingText.textContent = text;
        loadingOverlay.classList.add('active');
    }

    function updateLoadingStatus(text) {
        loadingText.textContent = text;
    }

    function hideLoading() {
        loadingOverlay.classList.remove('active');
    }

    newAnalysisBtn.addEventListener('click', () => {
        resultsSection.classList.remove('active');
        uploadSection.classList.add('active');
        resetForm();
    });

    function resetForm() {
        selectedFile = null;
        fileInput.value = '';
        fileNameDisplay.textContent = '';
        jobDescription.value = '';
        validateForm();
    }
});
