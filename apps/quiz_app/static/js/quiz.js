// Quiz Taking Logic

let currentQuestionIndex = 0;
let questions = [];
let userAnswers = {};
let timerInterval;
let timeRemaining = 0;

// Initialize Quiz
document.addEventListener('DOMContentLoaded', function() {
    // Load session data first
    if (sessionStorage.getItem("userAnswers")) {
        userAnswers = JSON.parse(sessionStorage.getItem("userAnswers"));
    }
    if (sessionStorage.getItem("currentQuestionIndex")) {
        currentQuestionIndex = parseInt(sessionStorage.getItem("currentQuestionIndex"));
    }
    if (sessionStorage.getItem("timeRemaining")) {
        timeRemaining = parseInt(sessionStorage.getItem("timeRemaining"));
    }

    // Load quiz data from backend (this should be populated by Django)
    loadQuizData();

    // Setup event listeners
    setupEventListeners();

    // Start timer
    startTimer();

    // Display current question (respects session data)
    displayQuestion(currentQuestionIndex);

    // Create question navigator
    createQuestionNavigator();
});

// Load Quiz Data (should be populated by Django template)
function loadQuizData() {
    // This would typically be loaded from Django context
    // For now, using sample data
    questions = window.quizData || getSampleQuestions();
    timeRemaining = parseInt(document.getElementById('timer').textContent) * 60;
    document.getElementById('totalQuestions').textContent = questions.length;
}

// Sample Questions (for testing)
function getSampleQuestions() {
    return [
        {
            id: 1,
            text: 'ما هي لغة البرمجة المستخدمة في Django؟',
            code: null,
            options: [
                { id: 'a', text: 'JavaScript' },
                { id: 'b', text: 'Python' },
                { id: 'c', text: 'Java' },
                { id: 'd', text: 'PHP' }
            ],
            correctAnswer: 'b'
        },
        {
            id: 2,
            text: 'ما هو ناتج الكود التالي؟',
            code: 'x = 5\ny = 3\nprint(x + y)',
            options: [
                { id: 'a', text: '8' },
                { id: 'b', text: '53' },
                { id: 'c', text: 'Error' },
                { id: 'd', text: '15' }
            ],
            correctAnswer: 'a'
        }
    ];
}

// Setup Event Listeners
function setupEventListeners() {
    document.getElementById('nextBtn').addEventListener('click', nextQuestion);
    document.getElementById('prevBtn').addEventListener('click', previousQuestion);
    document.getElementById('submitBtn').addEventListener('click', showSubmitModal);
    document.getElementById('confirmSubmit').addEventListener('click', submitQuiz);
}

// Display Question
function displayQuestion(index) {
    if (index < 0 || index >= questions.length) return;
    
    currentQuestionIndex = index;
    const question = questions[index];
    
    // Update question text
    document.getElementById('questionText').textContent = question.text;
    
    // Display code if exists
    const codeBlock = document.getElementById('codeBlock');
    if (question.code) {
        document.getElementById('codeContent').textContent = question.code;
        codeBlock.style.display = 'block';
        // Highlight code syntax
        if (typeof Prism !== 'undefined') {
            Prism.highlightAll();
        }
    } else {
        codeBlock.style.display = 'none';
    }
    
    // Display answer options
    const optionsContainer = document.getElementById('answerOptions');
    optionsContainer.innerHTML = '';
    
    question.options.forEach(option => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'col-md-6';
        
        const isSelected = userAnswers[question.id] === option.id;
        
        optionDiv.innerHTML = `
            <div class="answer-option ${isSelected ? 'selected' : ''}" data-option-id="${option.id}">
                <h6 class="mb-0">${option.id.toUpperCase()}. ${option.text}</h6>
            </div>
        `;
        
        optionDiv.querySelector('.answer-option').addEventListener('click', function() {
            selectAnswer(question.id, option.id);
        });
        
        optionsContainer.appendChild(optionDiv);
    });
    
    // Update UI
    updateUI();
}

// Select Answer
function selectAnswer(questionId, optionId) {
    userAnswers[questionId] = optionId;
    
    // Update visual feedback
    document.querySelectorAll('.answer-option').forEach(opt => {
        opt.classList.remove('selected');
    });
    document.querySelector(`[data-option-id="${optionId}"]`).classList.add('selected');
    
    // Update question navigator
    updateQuestionNavigator();
    
    // Play selection sound (optional)
    playSound('select');
}

// Next Question
function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        displayQuestion(currentQuestionIndex + 1);
    }
}

// Previous Question
function previousQuestion() {
    if (currentQuestionIndex > 0) {
        displayQuestion(currentQuestionIndex - 1);
    }
}

// Update UI
function updateUI() {
    // Update current question number
    document.getElementById('currentQuestion').textContent = currentQuestionIndex + 1;
    
    // Update progress bar
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
    document.getElementById('progressBar').style.width = progress + '%';
    
    // Update navigation buttons
    document.getElementById('prevBtn').disabled = currentQuestionIndex === 0;
    
    if (currentQuestionIndex === questions.length - 1) {
        document.getElementById('nextBtn').style.display = 'none';
        document.getElementById('submitBtn').style.display = 'inline-block';
    } else {
        document.getElementById('nextBtn').style.display = 'inline-block';
        document.getElementById('submitBtn').style.display = 'none';
    }
    
    // Update question navigator
    updateQuestionNavigator();
}

// Create Question Navigator
function createQuestionNavigator() {
    const navigator = document.getElementById('questionNavigator');
    navigator.innerHTML = '';
    
    questions.forEach((question, index) => {
        const btn = document.createElement('div');
        btn.className = 'question-nav-btn';
        btn.textContent = index + 1;
        btn.dataset.index = index;
        
        btn.addEventListener('click', function() {
            displayQuestion(index);
        });
        
        navigator.appendChild(btn);
    });
}

// Update Question Navigator
function updateQuestionNavigator() {
    const navBtns = document.querySelectorAll('.question-nav-btn');
    
    navBtns.forEach((btn, index) => {
        btn.classList.remove('active', 'answered');
        
        if (index === currentQuestionIndex) {
            btn.classList.add('active');
        } else if (userAnswers[questions[index].id]) {
            btn.classList.add('answered');
        }
    });
}

// Start Timer
function startTimer() {
    updateTimerDisplay();
    
    timerInterval = setInterval(function() {
        timeRemaining--;
        updateTimerDisplay();
        
        // Warning at 5 minutes
        if (timeRemaining === 300) {
            document.getElementById('timer').classList.add('warning');
            window.quizApp.showToast('تبقى 5 دقائق فقط!', 'warning');
        }
        
        // Danger at 1 minute
        if (timeRemaining === 60) {
            document.getElementById('timer').classList.remove('warning');
            document.getElementById('timer').classList.add('danger');
            window.quizApp.showToast('تبقى دقيقة واحدة فقط!', 'danger');
        }
        
        // Time's up
        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            window.quizApp.showToast('انتهى الوقت!', 'danger');
            submitQuiz();
        }
    }, 1000);
}

// Update Timer Display
function updateTimerDisplay() {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    document.getElementById('timer').textContent = 
        `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

// Show Submit Modal
function showSubmitModal() {
    const answeredCount = Object.keys(userAnswers).length;
    const totalCount = questions.length;
    
    document.getElementById('answeredCount').textContent = answeredCount;
    document.getElementById('totalCount').textContent = totalCount;
    
    const modal = new bootstrap.Modal(document.getElementById('submitModal'));
    modal.show();
}

// Submit Quiz
function submitQuiz() {
    clearInterval(timerInterval);
    
    window.quizApp.showSpinner();
    
    // Prepare submission data
    const submissionData = {
        answers: userAnswers,
        timeSpent: parseInt(document.getElementById('timer').getAttribute('data-initial-time')) - timeRemaining
    };
    
    // Submit to backend
    // This should be an AJAX call to Django view
    console.log('Submitting quiz:', submissionData);
    
    // Simulate API call
    setTimeout(function() {
        window.quizApp.hideSpinner();
        
        // Redirect to results page
        // window.location.href = '/quiz/results/';
        
        // For demo, show success message
        window.quizApp.showToast('تم إرسال الاختبار بنجاح!', 'success');
    }, 2000);
}

// Play Sound
function playSound(type) {
    // Optional: Add sound effects
    // const audio = new Audio(`/static/sounds/${type}.mp3`);
    // audio.play();
}

// Handle Page Unload
window.addEventListener('beforeunload', function(e) {
    if (Object.keys(userAnswers).length > 0 && timeRemaining > 0) {
        e.preventDefault();
        e.returnValue = 'لديك اختبار قيد التقدم. هل أنت متأكد أنك تريد المغادرة؟';
        return e.returnValue;
    }
});

// Keyboard Shortcuts
document.addEventListener('keydown', function(e) {
    // Arrow keys for navigation
    if (e.key === 'ArrowRight' && currentQuestionIndex > 0) {
        previousQuestion();
    } else if (e.key === 'ArrowLeft' && currentQuestionIndex < questions.length - 1) {
        nextQuestion();
    }
    
    // Number keys for answers (1-4)
    if (e.key >= '1' && e.key <= '4') {
        const options = questions[currentQuestionIndex].options;
        if (options[parseInt(e.key) - 1]) {
            selectAnswer(
                questions[currentQuestionIndex].id,
                options[parseInt(e.key) - 1].id
            );
        }
    }
});

// ====== SESSION STORAGE LOGIC ======

// استرجاع البيانات المخزنة لما الصفحة تفتح
window.addEventListener("DOMContentLoaded", function() {
    if (sessionStorage.getItem("userAnswers")) {
        userAnswers = JSON.parse(sessionStorage.getItem("userAnswers"));
    }
    if (sessionStorage.getItem("currentQuestionIndex")) {
        currentQuestionIndex = parseInt(sessionStorage.getItem("currentQuestionIndex"));
    }
    if (sessionStorage.getItem("timeRemaining")) {
        timeRemaining = parseInt(sessionStorage.getItem("timeRemaining"));
    }
});

// Update sessionStorage after selecting an answer
document.addEventListener("click", function(e) {
    if (e.target.closest(".answer-option")) {
        sessionStorage.setItem("userAnswers", JSON.stringify(userAnswers));
    }
});

// Save time and current question every second
setInterval(function() {
    sessionStorage.setItem("timeRemaining", timeRemaining);
    sessionStorage.setItem("currentQuestionIndex", currentQuestionIndex);
}, 1000);
// Clear storage when the user submits the quiz
document.addEventListener("click", function(e) {
    if (e.target && e.target.id === "confirmSubmit") {
        sessionStorage.clear();
    }
});


