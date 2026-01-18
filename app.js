// ===================================
// Resume Analysis & Job Matching System
// ===================================

console.log('CareerMatch AI: App.js Loaded Successfully');

// Sample Resume Data
const sampleResume = `Full Stack Developer with 3+ years of experience in web development.

Technical Skills:
- Programming Languages: JavaScript, Python, Java, TypeScript
- Frontend: React, Vue.js, HTML5, CSS3, Tailwind CSS
- Backend: Node.js, Express, Django, REST APIs
- Databases: MongoDB, PostgreSQL, MySQL
- Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD
- Tools: Git, VS Code, Jira, Figma

Education:
Bachelor of Technology in Computer Science

Projects:
- Built e-commerce platform using MERN stack
- Developed ML-powered recommendation system
- Created data visualization dashboard with React and D3.js

Experience:
Software Engineer at Tech Company (2021-2024)
- Developed microservices architecture
- Optimized database performance
- Led team of 3 developers`;

// Job Role Database with Required Skills
const jobRoles = {
  "Full Stack Developer": {
    requiredSkills: ["javascript", "react", "node.js", "html", "css", "git", "rest api", "sql", "mongodb"],
    category: "Software Development",
    weight: {
      "javascript": 3,
      "react": 2,
      "node.js": 2,
      "html": 1,
      "css": 1
    }
  },
  "Data Scientist": {
    requiredSkills: ["python", "machine learning", "statistics", "pandas", "numpy", "data visualization", "sql", "tensorflow", "scikit-learn"],
    category: "Data Science",
    weight: {
      "python": 3,
      "machine learning": 3,
      "statistics": 2,
      "pandas": 2
    }
  },
  "Machine Learning Engineer": {
    requiredSkills: ["python", "tensorflow", "pytorch", "machine learning", "deep learning", "nlp", "computer vision", "aws", "docker"],
    category: "AI/ML",
    weight: {
      "python": 3,
      "machine learning": 3,
      "tensorflow": 2,
      "deep learning": 2
    }
  },
  "DevOps Engineer": {
    requiredSkills: ["docker", "kubernetes", "ci/cd", "aws", "azure", "linux", "terraform", "jenkins", "git", "shell scripting"],
    category: "DevOps",
    weight: {
      "docker": 3,
      "kubernetes": 3,
      "aws": 2,
      "ci/cd": 2
    }
  },
  "Frontend Developer": {
    requiredSkills: ["javascript", "react", "vue.js", "html", "css", "typescript", "webpack", "responsive design", "git"],
    category: "Software Development",
    weight: {
      "javascript": 3,
      "react": 2,
      "html": 2,
      "css": 2
    }
  },
  "Backend Developer": {
    requiredSkills: ["java", "python", "node.js", "sql", "rest api", "microservices", "docker", "mongodb", "postgresql"],
    category: "Software Development",
    weight: {
      "java": 2,
      "python": 2,
      "node.js": 2,
      "sql": 2,
      "rest api": 2
    }
  },
  "Data Engineer": {
    requiredSkills: ["python", "sql", "spark", "hadoop", "etl", "data warehousing", "kafka", "airflow", "aws", "azure"],
    category: "Data Engineering",
    weight: {
      "python": 3,
      "sql": 3,
      "spark": 2,
      "etl": 2
    }
  },
  "Mobile App Developer": {
    requiredSkills: ["react native", "flutter", "swift", "kotlin", "android", "ios", "firebase", "rest api", "git"],
    category: "Mobile Development",
    weight: {
      "react native": 3,
      "flutter": 3,
      "swift": 2,
      "kotlin": 2
    }
  },
  "Cloud Architect": {
    requiredSkills: ["aws", "azure", "gcp", "cloud architecture", "terraform", "kubernetes", "security", "networking", "devops"],
    category: "Cloud",
    weight: {
      "aws": 3,
      "azure": 2,
      "cloud architecture": 3,
      "terraform": 2
    }
  },
  "QA Engineer": {
    requiredSkills: ["selenium", "testing", "automation", "java", "python", "jira", "test cases", "api testing", "ci/cd"],
    category: "Quality Assurance",
    weight: {
      "selenium": 2,
      "automation": 3,
      "testing": 3,
      "api testing": 2
    }
  }
};

// Skill Categories for Classification
const skillCategories = {
  "Programming Languages": ["javascript", "python", "java", "c++", "c#", "go", "rust", "ruby", "php", "typescript", "kotlin", "swift", "r"],
  "Frontend Technologies": ["react", "vue.js", "angular", "html", "css", "sass", "tailwind", "bootstrap", "webpack", "next.js"],
  "Backend Technologies": ["node.js", "express", "django", "flask", "spring boot", "asp.net", "ruby on rails"],
  "Databases": ["sql", "mysql", "postgresql", "mongodb", "redis", "cassandra", "elasticsearch", "oracle"],
  "ML/AI": ["machine learning", "deep learning", "tensorflow", "pytorch", "keras", "nlp", "computer vision", "scikit-learn"],
  "Cloud & DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "jenkins", "terraform", "ansible"],
  "Data Science": ["pandas", "numpy", "matplotlib", "data visualization", "statistics", "spark", "hadoop", "etl"],
  "Mobile Development": ["react native", "flutter", "android", "ios", "swift", "kotlin"],
  "Tools & Others": ["git", "jira", "figma", "postman", "vs code", "linux", "agile", "rest api", "graphql", "microservices"]
};

// Comprehensive Skills Dictionary
const allKnownSkills = Object.values(skillCategories).flat();

// ===================================
// Skill Extraction Engine
// ===================================
function extractSkills(resumeText) {
  const text = resumeText.toLowerCase();
  const extractedSkills = [];

  // Extract known skills
  allKnownSkills.forEach(skill => {
    const skillRegex = new RegExp(`\\b${skill.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'gi');
    if (skillRegex.test(text)) {
      extractedSkills.push(skill);
    }
  });

  // Remove duplicates
  return [...new Set(extractedSkills)];
}

// Categorize Extracted Skills
function categorizeSkills(skills) {
  const categorized = {};

  Object.keys(skillCategories).forEach(category => {
    const categorySkills = skills.filter(skill =>
      skillCategories[category].includes(skill.toLowerCase())
    );
    if (categorySkills.length > 0) {
      categorized[category] = categorySkills;
    }
  });

  return categorized;
}

// ===================================
// Education Extraction
// ===================================
function extractEducation(resumeText) {
  const text = resumeText.toLowerCase();
  const educationKeywords = [
    'bachelor', 'master', 'phd', 'doctorate', 'degree',
    'computer science', 'engineering', 'mba', 'b.tech', 'm.tech',
    'university', 'college', 'institute'
  ];

  const educationInfo = [];
  const lines = resumeText.split('\n');

  lines.forEach(line => {
    educationKeywords.forEach(keyword => {
      if (line.toLowerCase().includes(keyword) && line.length < 150) {
        educationInfo.push(line.trim());
      }
    });
  });

  return educationInfo.length > 0
    ? [...new Set(educationInfo)].slice(0, 3).join('<br>')
    : 'Education information not clearly specified';
}

// ===================================
// Job Matching Algorithm
// ===================================
function calculateJobMatches(extractedSkills) {
  const matches = [];

  Object.keys(jobRoles).forEach(jobTitle => {
    const role = jobRoles[jobTitle];
    const requiredSkills = role.requiredSkills;
    const weights = role.weight || {};

    // Calculate matched and missing skills
    const matchedSkills = extractedSkills.filter(skill =>
      requiredSkills.some(req => req.toLowerCase() === skill.toLowerCase())
    );

    const missingSkills = requiredSkills.filter(req =>
      !extractedSkills.some(skill => skill.toLowerCase() === req.toLowerCase())
    );

    // Calculate weighted score
    let weightedScore = 0;
    let totalWeight = 0;

    requiredSkills.forEach(skill => {
      const weight = weights[skill.toLowerCase()] || 1;
      totalWeight += weight;
      if (matchedSkills.some(s => s.toLowerCase() === skill.toLowerCase())) {
        weightedScore += weight;
      }
    });

    // Calculate percentage (70% Jaccard + 30% Weighted)
    const jaccardSimilarity = matchedSkills.length / requiredSkills.length;
    const weightedSimilarity = weightedScore / totalWeight;
    const matchPercentage = Math.round((jaccardSimilarity * 0.7 + weightedSimilarity * 0.3) * 100);

    matches.push({
      jobTitle,
      matchPercentage,
      matchedSkills,
      missingSkills,
      category: role.category
    });
  });

  // Sort by match percentage and return top 3
  return matches.sort((a, b) => b.matchPercentage - a.matchPercentage).slice(0, 3);
}

// ===================================
// Recommendation Engine
// ===================================
function generateRecommendations(topMatches, extractedSkills) {
  const recommendations = [];
  const allMissingSkills = new Set();

  // Collect all missing skills from top 3 matches
  topMatches.forEach(match => {
    match.missingSkills.forEach(skill => allMissingSkills.add(skill));
  });

  const missingArray = Array.from(allMissingSkills);

  // Skill recommendations
  if (missingArray.length > 0) {
    const topMissing = missingArray.slice(0, 5);
    recommendations.push(`Focus on learning: ${topMissing.join(', ')} to improve your job match`);
  }

  // Certification recommendations
  const certifications = {
    "aws": "Get AWS Certified Solutions Architect certification",
    "azure": "Consider Microsoft Azure Fundamentals certification",
    "machine learning": "Pursue Google ML Engineer or AWS ML Specialty certification",
    "kubernetes": "Earn Certified Kubernetes Administrator (CKA) certification",
    "python": "Get Python Institute PCEP or PCAP certification"
  };

  missingArray.forEach(skill => {
    if (certifications[skill.toLowerCase()]) {
      recommendations.push(certifications[skill.toLowerCase()]);
    }
  });

  // General recommendations
  if (extractedSkills.length < 10) {
    recommendations.push("Expand your technical skillset - aim for 12-15 diverse skills");
  }

  if (!extractedSkills.some(s => s.includes('git'))) {
    recommendations.push("Add version control (Git/GitHub) to your resume");
  }

  if (!extractedSkills.some(s => ['docker', 'kubernetes', 'ci/cd'].includes(s.toLowerCase()))) {
    recommendations.push("Learn DevOps fundamentals (Docker, CI/CD) for better opportunities");
  }

  recommendations.push("Include quantifiable achievements in your projects");
  recommendations.push("Keep your resume updated with latest projects and technologies");

  return recommendations.slice(0, 7);
}

// ===================================
// Summary Generator
// ===================================
function generateSummary(extractedSkills, topMatches) {
  const skillCount = extractedSkills.length;
  const topMatch = topMatches[0];
  const avgMatch = Math.round(topMatches.reduce((sum, m) => sum + m.matchPercentage, 0) / topMatches.length);

  const categories = Object.keys(categorizeSkills(extractedSkills));

  return `Your resume demonstrates strong technical expertise with ${skillCount} identified skills across ${categories.length} domains (${categories.join(', ')}). You are an excellent match for ${topMatch.jobTitle} roles with a ${topMatch.matchPercentage}% compatibility score. Your diverse skillset positions you well for ${topMatches.length} different career paths with an average match rate of ${avgMatch}%. ${skillCount >= 12 ? 'Your comprehensive skill portfolio is a significant strength.' : 'Consider expanding your skillset for broader opportunities.'}`;
}

// ===================================
// Visualization - Pie Chart Renderer
// ===================================
function drawPieChart(canvasId, data, colors) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = Math.min(centerX, centerY) - 20;

  // Clear canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Calculate total
  const total = data.reduce((sum, item) => sum + item.value, 0);

  let currentAngle = -Math.PI / 2; // Start from top

  data.forEach((item, index) => {
    const sliceAngle = (item.value / total) * 2 * Math.PI;

    // Draw slice
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
    ctx.closePath();
    ctx.fillStyle = colors[index % colors.length];
    ctx.fill();

    // Add border
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Add percentage label
    const labelAngle = currentAngle + sliceAngle / 2;
    const labelX = centerX + (radius * 0.7) * Math.cos(labelAngle);
    const labelY = centerY + (radius * 0.7) * Math.sin(labelAngle);

    const percentage = ((item.value / total) * 100).toFixed(1) + '%';
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 14px Inter';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(percentage, labelX, labelY);

    currentAngle += sliceAngle;
  });
}

function createLegend(legendId, data, colors) {
  const legendContainer = document.getElementById(legendId);
  if (!legendContainer) return; // Guard for missing legend elements in new UI

  legendContainer.innerHTML = '';

  data.forEach((item, index) => {
    const legendItem = document.createElement('div');
    legendItem.className = 'legend-item';

    const colorBox = document.createElement('div');
    colorBox.className = 'legend-color';
    colorBox.style.backgroundColor = colors[index % colors.length];

    const label = document.createElement('span');
    label.textContent = item.label;

    legendItem.appendChild(colorBox);
    legendItem.appendChild(label);
    legendContainer.appendChild(legendItem);
  });
}

// ===================================
// UI Update Functions
// ===================================
function displaySkills(skills) {
  const container = document.getElementById('skillsContainer');
  container.innerHTML = '';

  skills.forEach((skill, index) => {
    const tag = document.createElement('span');
    tag.className = 'skill-tag skill-match'; // Use new class
    tag.textContent = skill;
    // tag.style.animationDelay = `${index * 0.05}s`;
    container.appendChild(tag);
  });
}

function displayJobMatches(matches) {
  // Legacy client-side display function, mostly superseded by displayJobMatchesFromAPI
  displayJobMatchesFromAPI(matches);
}

function displayRecommendations(recommendations) {
  const list = document.getElementById('recommendationsList');
  list.innerHTML = '';

  recommendations.forEach((rec, index) => {
    const item = document.createElement('li');
    item.className = 'recommendation-item';
    item.textContent = rec;
    item.style.marginBottom = '0.5rem';
    list.appendChild(item);
  });
}

function displayJobMatchesFromAPI(matches) {
  const container = document.getElementById('jobMatchList');

  if (!container) return;
  container.innerHTML = '';

  matches.forEach((match, index) => {
    const item = document.createElement('div');
    item.className = `job-match-item rank-${index + 1}`;

    // Minimal display for hidden list or future use
    item.innerHTML = `<strong>${match.job_title || match.jobTitle}</strong>: ${Math.round(match.score || match.matchPercentage)}%`;
    container.appendChild(item);
  });
}

// Global Application State
// currentAnalysisContext is already defined globally
let currentChartIndex = 0;
let chartDataCache = {}; // Start caching chart data

// ... (displayChartsFromAPI logic)

// ===================================
// Visualization - Advanced Chart.js Renderer
// ===================================
let matchChartInstance = null;
let categoryChartInstance = null;

function renderAdvancedCharts(skills, topMatches, categorizedSkills) {
  // 1. Prepare Match Data
  let matchedCount = 0;
  let missingCount = 0;

  if (topMatches && topMatches.length > 0) {
    const topMatch = topMatches[0];
    matchedCount = topMatch.matched_skills ? topMatch.matched_skills.length : (topMatch.matchedSkills ? topMatch.matchedSkills.length : 0);
    missingCount = topMatch.missing_skills ? topMatch.missing_skills.length : (topMatch.missingSkills ? topMatch.missingSkills.length : 0);
  } else {
    // Fallback if no matches
    matchedCount = skills.length;
    missingCount = 0;
  }

  // 2. Prepare Category Data
  let categoryLabels = [];
  let categoryValues = [];

  if (Object.keys(categorizedSkills).length > 0) {
    categoryLabels = Object.keys(categorizedSkills);
    categoryValues = categoryLabels.map(cat => categorizedSkills[cat].length);
  } else {
    const cat = categorizeSkills(skills);
    categoryLabels = Object.keys(cat);
    categoryValues = categoryLabels.map(c => cat[c].length);
  }

  // --- Chart 1: Skill Match (Doughnut) ---
  const matchCtx = document.getElementById('matchChart');
  if (matchCtx) {
    if (matchChartInstance) {
      matchChartInstance.destroy();
    }

    matchChartInstance = new Chart(matchCtx, {
      type: 'doughnut',
      data: {
        labels: ['Matched Skills', 'Missing Skills'],
        datasets: [{
          data: [matchedCount, missingCount],
          backgroundColor: [
            '#10b981', // Green-500
            '#334155'  // Slate-700
          ],
          borderWidth: 0,
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%', // Thinner ring
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: '#94a3b8', font: { family: 'Inter' } }
          },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.9)',
            padding: 12,
            bodyFont: { family: 'Inter' }
          }
        }
      }
    });
  }

  // --- Chart 2: Category Distribution (Doughnut) ---
  const catCtx = document.getElementById('categoryChart');
  if (catCtx) {
    if (categoryChartInstance) {
      categoryChartInstance.destroy();
    }

    // Neon Palette
    const neonColors = [
      '#f472b6', '#c084fc', '#818cf8', '#60a5fa', '#34d399', '#facc15'
    ];

    categoryChartInstance = new Chart(catCtx, {
      type: 'doughnut',
      data: {
        labels: categoryLabels,
        datasets: [{
          data: categoryValues,
          backgroundColor: neonColors.slice(0, categoryLabels.length),
          borderWidth: 0,
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '60%',
        plugins: {
          legend: {
            display: false // Hide legend if too many items
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                return ` ${context.label}: ${context.raw}`;
              }
            },
            backgroundColor: 'rgba(15, 23, 42, 0.9)',
            padding: 10
          }
        }
      }
    });
  }
}

// ===================================
// Project Analysis Display
// ===================================
function displayProjectAnalysis(analysis) {
  const card = document.getElementById('projectAnalysisCard');
  const container = document.getElementById('projectAnalysisContent');

  if (!card || !container) return;

  if (!analysis || analysis.length === 0) {
    card.style.display = 'none';
    return;
  }

  card.style.display = 'block';

  container.innerHTML = '';

  analysis.forEach((item, index) => {
    const itemDiv = document.createElement('div');
    itemDiv.className = 'project-analysis-item';

    // Tech Stack Tags
    const techTags = item.tech_stack && item.tech_stack.length > 0
      ? item.tech_stack.map(t =>
        `<span style="background:rgba(99, 102, 241, 0.1); color:var(--color-primary); padding:2px 8px; border-radius:12px; font-size:0.85rem; margin-right:5px;">${t}</span>`
      ).join('')
      : '<span style="color:#666; font-size:0.85rem;">No specific tech detected</span>';

    // Advantages List
    const advantagesHtml = item.advantages && item.advantages.length > 0
      ? `<div style="margin-top:0.8rem;">
             <strong style="color:#10b981; display:block; font-size:0.9rem; margin-bottom:0.2rem;">Detailed Advantages:</strong>
             <ul style="color:var(--text-secondary); margin:0; padding-left:1.2rem; font-size:0.9rem;">
                ${item.advantages.map(adv => `<li>${adv}</li>`).join('')}
             </ul>
           </div>`
      : '';

    // Disadvantages List
    const disadvantagesHtml = item.disadvantages && item.disadvantages.length > 0
      ? `<div style="margin-top:0.8rem;">
             <strong style="color:#ef4444; display:block; font-size:0.9rem; margin-bottom:0.2rem;">Areas for Improvement:</strong>
             <ul style="color:var(--text-secondary); margin:0; padding-left:1.2rem; font-size:0.9rem;">
                ${item.disadvantages.map(dis => `<li>${dis}</li>`).join('')}
             </ul>
           </div>`
      : '';

    // Relevance Badges
    const relevanceHtml = item.relevance && item.relevance.length > 0
      ? `<div style="margin-top:0.8rem; border-top:1px solid var(--border-color); padding-top:0.5rem;">
             <span style="font-size:0.85rem; color:var(--text-secondary); margin-right:0.5rem;">Relevant for:</span>
             ${item.relevance.map(role =>
        `<span style="background:rgba(255,255,255,0.1); color:var(--text-primary); padding:2px 8px; border-radius:4px; font-size:0.8rem; margin-right:4px;">${role}</span>`
      ).join('')}
           </div>`
      : '';

    // Tier Color Logic
    let tierColor = '#64748b'; // Default gray
    if (item.tier === 'S') tierColor = '#8b5cf6'; // Violet
    else if (item.tier === 'A') tierColor = '#10b981'; // Green
    else if (item.tier === 'B') tierColor = '#3b82f6'; // Blue
    else if (item.tier === 'C') tierColor = '#f59e0b'; // Amber

    itemDiv.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:0.5rem;">
          <div>
            <h4 style="color:var(--text-primary); margin:0; font-size:1.1rem;">${item.name}</h4>
          </div>
          <div style="text-align:right;">
             <div style="background:${tierColor}; color:white; padding:4px 12px; border-radius:12px; font-weight:bold; font-size:0.9rem; display:inline-block; box-shadow:0 2px 10px rgba(0,0,0,0.2);">
                Tier ${item.tier || 'B'}
             </div>
             <div style="color:var(--text-secondary); font-size:0.8rem; margin-top:2px;">Score: ${item.score || 60}/100</div>
          </div>
      </div>
      
      <p style="color:var(--color-primary); font-weight:500; font-size:0.9rem; margin-bottom:0.5rem;">
         ${item.summary || "Project Overview"}
      </p>

      <p style="color:var(--text-secondary); margin-bottom:0.8rem; font-style:italic; font-size:0.95rem;">
         "${item.description}"
      </p>

      <div style="margin-bottom:1rem;">${techTags}</div>
      
      <div style="background:rgba(255,255,255,0.03); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
        ${advantagesHtml}
        ${disadvantagesHtml}
        ${relevanceHtml}
      </div>
    `;

    container.appendChild(itemDiv);
  });
}

// ===================================
// Internship Analysis Display
// ===================================
// ===================================
// Internship & Training Display
// ===================================
function displayInternships(analysis) {
  const internshipCard = document.getElementById('internshipCard');
  const internshipContainer = document.getElementById('internshipContent');
  const trainingCard = document.getElementById('trainingCard');
  const trainingContainer = document.getElementById('trainingContent');

  if (!internshipCard || !trainingCard) return;

  // Reset
  internshipCard.style.display = 'none';
  trainingCard.style.display = 'none';
  internshipContainer.innerHTML = '';
  trainingContainer.innerHTML = '';

  if (!analysis || analysis.length === 0) {
    return;
  }

  // Split Data
  const internships = analysis.filter(item => item.type === 'Internship');
  const trainings = analysis.filter(item => item.type === 'Training');

  // Render Internships
  if (internships.length > 0) {
    internshipCard.style.display = 'block';
    renderItems(internships, internshipContainer);
  }

  // Render Trainings
  if (trainings.length > 0) {
    trainingCard.style.display = 'block';
    renderItems(trainings, trainingContainer);
  }
}

function renderItems(items, container) {
  items.forEach((item) => {
    const itemDiv = document.createElement('div');
    itemDiv.className = 'project-analysis-item'; // Reuse styles

    // Skills Used
    const techTags = item.skills_used && item.skills_used.length > 0
      ? item.skills_used.map(t =>
        `<span style="background:rgba(16, 185, 129, 0.1); color:var(--success); padding:2px 8px; border-radius:12px; font-size:0.85rem; margin-right:5px;">${t}</span>`
      ).join('')
      : '';

    itemDiv.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:0.5rem;">
          <div>
            <h4 style="color:var(--text-primary); margin:0; font-size:1.1rem;">${item.role}</h4>
            <div style="color:var(--color-primary); font-size:0.95rem; font-weight:500;">${item.company}</div>
          </div>
      </div>
      
      <p style="color:var(--text-secondary); margin-bottom:0.8rem; font-size:0.95rem; line-height:1.5;">
         ${item.summary}
      </p>

      <div style="margin-bottom:1rem;">${techTags}</div>
    `;

    container.appendChild(itemDiv);
  });
}

// ===================================
// Main Analysis Function (Updated)
// ===================================
async function analyzeResume() {
  const resumeText = document.getElementById('resumeText').value.trim();
  const targetRole = document.getElementById('jobRole') ? document.getElementById('jobRole').value.trim() : '';

  // Basic validation - check if text or file provided
  if (!resumeText) {
    showToast('Please enter your resume text or upload a file.', 'info');
    return;
  }

  if (resumeText.length < 50) {
    showToast('Please provide a more detailed resume (at least 50 characters)', 'warning');
    return;
  }

  // Show loading state
  const btn = document.getElementById('analyzeBtn');
  const loadingDiv = document.getElementById('loading');
  const resultsSection = document.getElementById('resultsSection');

  if (loadingDiv) {
    loadingDiv.style.display = 'block';
    loadingDiv.scrollIntoView({ behavior: 'smooth' });
  }

  if (resultsSection) {
    resultsSection.style.display = 'none';
    resultsSection.classList.remove('active');
  }

  const originalBtnContent = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = '<span>Analyzing...</span>'; // Removed emoji

  try {
    // Call Flask API
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        resumeText,
        target_role: targetRole
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Analysis failed');
    }

    const data = await response.json();

    // 1. Update Stats Cards (New UI Support)
    const scoreBase = data.jobMatches && data.jobMatches.length > 0 ? data.jobMatches[0].score || data.jobMatches[0].matchPercentage : 60;
    const atsScore = Math.min(98, Math.max(40, scoreBase + (data.skills.length > 10 ? 10 : 0)));
    const finalAtsScore = Math.round(atsScore);

    // Skill Counts
    const topMatch = data.jobMatches && data.jobMatches.length > 0 ? data.jobMatches[0] : null;
    const matchedCount = topMatch ? (topMatch.matched_skills ? topMatch.matched_skills.length : (topMatch.matchedSkills ? topMatch.matchedSkills.length : 0)) : 0;
    const missingCount = topMatch ? (topMatch.missing_skills ? topMatch.missing_skills.length : (topMatch.missingSkills ? topMatch.missingSkills.length : 0)) : 0;

    // Update DOM Elements
    if (document.getElementById('atsScore')) document.getElementById('atsScore').textContent = finalAtsScore;
    if (document.getElementById('skillMatchCount')) document.getElementById('skillMatchCount').textContent = matchedCount;
    if (document.getElementById('missingSkillsCount')) document.getElementById('missingSkillsCount').textContent = missingCount;

    // Update Score Circle in Match Score Card
    const mainScore = topMatch ? Math.round(topMatch.score || topMatch.matchPercentage || 0) : 0;

    const circle = document.querySelector('.progress-ring__circle');
    const valueText = document.querySelector('.stat-value');

    if (circle && valueText) {
      const radius = circle.r.baseVal.value;
      const circumference = radius * 2 * Math.PI;

      circle.style.strokeDasharray = `${circumference} ${circumference}`;
      const offset = circumference - (mainScore / 100) * circumference;
      circle.style.strokeDashoffset = offset;

      valueText.textContent = `${mainScore}%`;

      // Dynamic Color based on score
      if (mainScore >= 80) circle.style.stroke = 'var(--color-primary)'; // Green
      else if (mainScore >= 60) circle.style.stroke = '#3b82f6'; // Blue
      else if (mainScore >= 40) circle.style.stroke = '#facc15'; // Yellow
      else circle.style.stroke = '#ef4444'; // Red
    }

    // Update Best Match / Target Match Text
    const matchText = document.querySelector('.score-circle-container + p');
    if (matchText && topMatch) {
      if (targetRole && topMatch.is_target) {
        matchText.innerHTML = `Target Match: <strong>${topMatch.job_title || topMatch.jobTitle}</strong>`;
      } else {
        matchText.innerHTML = `Best Match: <strong>${topMatch.job_title || topMatch.jobTitle}</strong>`;
      }
    }


    // 2. Display Standard Results
    if (document.getElementById('summaryText')) document.getElementById('summaryText').textContent = data.summary;
    if (document.getElementById('educationText')) document.getElementById('educationText').innerHTML = data.education;

    // Display Skills
    displaySkills(data.skills);

    // Matched vs Missing Containers (New UI)
    // Populate the "Missing Skills" container specifically from the top job match
    if (topMatch && document.getElementById('missingSkillsContainer')) {
      const missingContainer = document.getElementById('missingSkillsContainer');
      missingContainer.innerHTML = '';
      const missing = topMatch.missing_skills || topMatch.missingSkills || [];
      missing.forEach(skill => {
        const tag = document.createElement('span');
        tag.className = 'skill-tag skill-missing';
        tag.textContent = skill;
        missingContainer.appendChild(tag);
      });
    }

    displayJobMatchesFromAPI(data.jobMatches);
    displayRecommendations(data.recommendations);
    renderAdvancedCharts(data.skills, data.jobMatches, data.categorizedSkills);
    displayProjectAnalysis(data.projectAnalysis);
    displayInternships(data.internshipAnalysis);

    // [New] Display Top 5 Recommended Roles
    const rolesContainer = document.getElementById('recommendedRolesContainer');
    if (rolesContainer && data.jobMatches) {
      rolesContainer.innerHTML = data.jobMatches.map(role => `
          <div class="role-card" style="padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; border: 1px solid var(--border-color); transition: transform 0.2s;">
              <h4 style="color: var(--color-primary); margin-bottom: 0.5rem; font-size: 1rem;">${role.job_title}</h4>
              <div class="match-bar">
                  <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
                      <span class="text-secondary" style="font-size: 0.85rem;">Match</span>
                      <span class="font-bold" style="color: var(--text-primary); font-size: 0.9rem;">${Math.round(role.score || role.matchPercentage || 0)}%</span>
                  </div>
                  <div style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px;">
                      <div style="width: ${Math.round(role.score || role.matchPercentage || 0)}%; height: 100%; background: var(--color-primary); border-radius: 3px;"></div>
                  </div>
              </div>
          </div>
        `).join('');
    }

    // [New] Save context for AI Coach
    currentAnalysisContext = {
      skills: data.skills || [],
      jobMatches: data.jobMatches || [],
      projectAnalysis: data.projectAnalysis || [],
      summary: data.summary || ""
    };

    // Hide loading, show results
    if (loadingDiv) loadingDiv.style.display = 'none';
    if (resultsSection) {
      resultsSection.style.display = 'block';
      resultsSection.classList.add('active');
      resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Re-enable button
    btn.disabled = false;
    btn.innerHTML = originalBtnContent;

  } catch (error) {
    console.error('Analysis error:', error);
    showToast('Error analyzing resume: ' + error.message, 'error');

    if (loadingDiv) loadingDiv.style.display = 'none';
    btn.disabled = false;
    btn.innerHTML = originalBtnContent;
  }
}


// ===================================
// File Upload Handler
// ===================================
async function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const uploadHint = document.querySelector('.upload-hint');
  // Should check if exists before using textContent, but removed in new UI anyway

  // Try server-side extraction first (preferred method)
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      const data = await response.json();
      document.getElementById('resumeText').value = data.text;
      showToast("File uploaded and text extracted!", "success");
      return;
    } else {
      console.log('Server extraction failed, falling back to client-side');
    }
  } catch (error) {
    console.log('Server extraction error, falling back to client-side:', error);
  }

  showToast("Using client-side fallback...", "info");
}


// Success feedback
function showUploadSuccess(element, originalText) {
  if (element) {
    element.textContent = 'File loaded successfully!';
    element.style.color = '#10b981';

    setTimeout(() => {
      element.textContent = originalText;
      element.style.color = '';
    }, 3000);
  }

  // Scroll to textarea
  setTimeout(() => {
    document.getElementById('resumeText').scrollIntoView({
      behavior: 'smooth',
      block: 'center'
    });
  }, 300);
}

// Error feedback
function showUploadError(element, originalText, message) {
  if (element) {
    element.textContent = message;
    element.style.color = '#ef4444';

    setTimeout(() => {
      element.textContent = originalText;
      element.style.color = '';
    }, 5000);
  }
  showToast(message + '. Please use PDF, TXT, or DOCX files.', 'error');
}

// Load Sample Resume
function loadSampleResume() {
  document.getElementById('resumeText').value = sampleResume;

  // Scroll to textarea
  document.getElementById('resumeText').scrollIntoView({
    behavior: 'smooth',
    block: 'center'
  });
}

// ===================================
// Event Listeners
// ===================================
document.addEventListener('DOMContentLoaded', () => {
  const analyzeBtn = document.getElementById('analyzeBtn');
  const fileUpload = document.getElementById('fileUpload');
  const sampleBtn = document.getElementById('sampleBtn');

  if (analyzeBtn) analyzeBtn.addEventListener('click', analyzeResume);
  if (fileUpload) fileUpload.addEventListener('change', handleFileUpload);
  if (sampleBtn) sampleBtn.addEventListener('click', loadSampleResume);

  // Allow Enter key in textarea (Ctrl+Enter to analyze)
  const txt = document.getElementById('resumeText');
  if (txt) {
    txt.addEventListener('keydown', (e) => {
      if (e.ctrlKey && e.key === 'Enter') {
        analyzeResume();
      }
    });
  }

  // Chat Widget Init
  chatWidget.init();
});

// ===================================
// Initialization
// ===================================
document.addEventListener('DOMContentLoaded', () => {
  // initializeChat(); // Chat removed

  // File Upload Listeners
  const fileUpload = document.getElementById('fileUpload');
  const dropZone = document.getElementById('dropZone');

  if (fileUpload && dropZone) {
    // Drag & Drop
    dropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropZone.style.borderColor = 'var(--color-primary)';
      dropZone.style.background = 'rgba(99, 102, 241, 0.1)';
    });

    dropZone.addEventListener('dragleave', (e) => {
      e.preventDefault();
      dropZone.style.borderColor = 'var(--border-color)';
      dropZone.style.background = 'rgba(255, 255, 255, 0.05)';
    });

    dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropZone.style.borderColor = 'var(--border-color)';
      dropZone.style.background = 'rgba(255, 255, 255, 0.05)';

      if (e.dataTransfer.files.length > 0) {
        fileUpload.files = e.dataTransfer.files;
        handleFileUpload(e.dataTransfer.files[0]);
      }
    });

    // Click Upload
    fileUpload.addEventListener('change', (e) => {
      if (e.target.files.length > 0) {
        handleFileUpload(e.target.files[0]);
      }
    });
  }

  // Initialize Analyze Button
  const analyzeBtn = document.getElementById('analyzeBtn');
  if (analyzeBtn) {
    analyzeBtn.addEventListener('click', analyzeResume);
  }

  // Initialize Sample Resume Button
  const sampleBtn = document.getElementById('sampleBtn');
  if (sampleBtn) {
    sampleBtn.addEventListener('click', () => {
      const textarea = document.getElementById('resumeText');
      if (textarea) {
        textarea.value = sampleResume;
        textarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  }

  console.log("CareerMatch AI: Initialized");
});

// ===================================
// AI Coach Chat Logic
// ===================================
// Global State
let currentAnalysisContext = {};

const chatWidget = {
  collapsed: true,

  init() {
    this.cacheDOM();
    if (this.header) this.bindEvents();
  },

  cacheDOM() {
    this.widget = document.getElementById('chatWidget');
    this.header = document.getElementById('chatHeader');
    this.toggleBtn = document.getElementById('toggleChatBtn');
    this.input = document.getElementById('chatInput');
    this.sendBtn = document.getElementById('sendMessageBtn');
    this.messagesContainer = document.getElementById('chatMessages');
  },

  bindEvents() {
    // Toggle chat
    this.header.addEventListener('click', (e) => {
      if (this.collapsed || (e.target !== this.toggleBtn && !this.toggleBtn.contains(e.target))) {
        this.toggleChat();
      }
    });

    this.toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleChat();
    });

    // Send message
    this.sendBtn.addEventListener('click', () => this.sendMessage());
    this.input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.sendMessage();
    });
  },

  toggleChat() {
    this.collapsed = !this.collapsed;
    if (this.collapsed) {
      this.widget.classList.add('collapsed');
    } else {
      this.widget.classList.remove('collapsed');
      setTimeout(() => this.input.focus(), 300);
      this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
  },

  addMessage(text, isUser = false) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${isUser ? 'user-message' : 'system-message'}`;
    // Removed avatar icons logic or emojis in string

    const formattedText = text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');

    msgDiv.innerHTML = formattedText;

    this.messagesContainer.appendChild(msgDiv);
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  },

  async sendMessage() {
    const text = this.input.value.trim();
    if (!text) return;
    this.input.value = '';
    // Add user message
    this.addMessage(text, true);

    // Add Thinking Indicator
    const thinkingId = 'thinking-' + Date.now();
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'message system-message typing-indicator';
    thinkingDiv.id = thinkingId;
    thinkingDiv.innerHTML = '<em>Thinking...</em>';
    this.messagesContainer.appendChild(thinkingDiv);
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;

    const context = currentAnalysisContext || {};

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          context: context
        })
      });

      const data = await response.json();

      // Remove thinking indicator
      const thinkingEl = document.getElementById(thinkingId);
      if (thinkingEl) thinkingEl.remove();

      if (data.error) {
        this.addMessage("Sorry, I encountered an error. Please try again.");
      } else {
        this.addMessage(data.reply);
      }

    } catch (error) {
      console.error('Chat error:', error);
      this.addMessage("Sorry, I'm having trouble connecting to the server.");
    }
  }
};

// =================================== 
// Toast Notification Logic
// ===================================
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  // Icon based on type
  let icon = 'ℹ️';
  if (type === 'success') icon = '✅';
  if (type === 'error') icon = '❌';

  toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;

  container.appendChild(toast);

  // Remove after 3 seconds
  setTimeout(() => {
    toast.style.animation = 'fadeOut 0.3s ease-out forwards';
    toast.addEventListener('animationend', () => {
      toast.remove();
    });
  }, 3000);
}

// End of file
