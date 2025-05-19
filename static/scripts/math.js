let currentAnswer = "";
        let currentIndex = 0;
        let correctCount = 0;
        let retryQueue = [];

        const questions = [
            { q: "2 + 2 = ?", a: ["4","four"] },
            { q: "1 + 3 = ?", a: ["4","four"] },
            { q: "3 + 2 = ?", a:  ["5","five"] },
            { q: "0 + 5 = ?", a: ["5","five"] },
            { q: "6 + 1 = ?", a: ["7","seven"] }
        ];

        function setMode(mode) {
            const micBtn = document.getElementById("micBtn");
            const keypadBtn = document.getElementById("keypadBtn");
            const micMode = document.getElementById("mic-mode");
            const keypadMode = document.getElementById("keypad-mode");

            if (mode === "mic") {
                micBtn.classList.add("active");
                keypadBtn.classList.remove("active");
                micMode.style.display = "flex";
                keypadMode.style.display = "none";
            } else {
                keypadBtn.classList.add("active");
                micBtn.classList.remove("active");
                keypadMode.style.display = "flex";
                micMode.style.display = "none";
            }
        }
        
        function startListening() {
            const feedback = document.getElementById("speech-feedback");
            const answerBox = document.getElementById("answer-box");

            if (!('webkitSpeechRecognition' in window)) {
                alert("Speech recognition not supported in this browser.");
                return;
            }

            const recognition = new webkitSpeechRecognition(); // or SpeechRecognition
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            feedback.innerText = "🎙️ Listening...";

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript.trim();
                feedback.innerText = `You said: "${transcript}"`;
                currentAnswer = transcript;
                answerBox.value = transcript;
                //submitAnswer();
            };

            recognition.onerror = (event) => {
                feedback.innerText = `❌ Error: ${event.error}`;
            };

            recognition.onend = () => {
                if (!currentAnswer) {
                    feedback.innerText = "No speech detected.";
                }
            };

            recognition.start();
        }

        function loadQuestion() {
            if (currentIndex < questions.length) {
                document.getElementById("question-display").innerHTML = `Question ${correctCount + 1}<br>${questions[currentIndex].q}`;
            } else if (retryQueue.length > 0) {
                questions.length = 0; // Clear old set
                questions.splice(0, questions.length, ...retryQueue);
                retryQueue = [];
                currentIndex = 0;
                loadQuestion();
            } else {
                document.getElementById("question-display").innerText = "🎉 Lesson Complete!";
            }
        }


        function appendAnswer(num) {
            currentAnswer += num;
            document.getElementById("answer-box").value = currentAnswer;
        }

        function clearAnswer() {
            currentAnswer = "";
            document.getElementById("answer-box").value = "";
            document.getElementById("feedback").innerText = "";
        }

        function updateProgressBar() {
            const percent = (correctCount / questions.length) * 100;
            document.getElementById("progress-bar").style.width = percent + "%";
        }

        function submitAnswer() {
            const feedback = document.getElementById("feedback");
            let userAnswer = currentAnswer.trim().toLowerCase();
        
            // Convert spoken number words to digits
            const numberMap = {
                "zero": "0", "one": "1", "two": "2", "three": "3",
                "four": "4", "five": "5", "six": "6",
                "seven": "7", "eight": "8", "nine": "9"
            };
        
            if (numberMap[userAnswer]) {
                userAnswer = numberMap[userAnswer];  // convert if it's a word
            }
        
            const correctAnswers = questions[currentIndex].a.map(ans => ans.toLowerCase());
        
            if (correctAnswers.includes(userAnswer)) {
                feedback.innerText = "✅ Correct!";
                feedback.style.color = "green";
                correctCount++;
                updateProgressBar();
            } else {
                feedback.innerText = "❌ Try Again Later!";
                feedback.style.color = "red";
                questions.splice(currentIndex, 1);
            }
        
            currentAnswer = "";
            document.getElementById("answer-box").value = "";
        
            setTimeout(() => {
                feedback.innerText = "";
                currentIndex++;
                loadQuestion();
            }, 1000);
        }
        

        function exitLesson() {
            window.location.href = "/subjects";
        }

        window.onload = () => {
            setMode("keypad");
            loadQuestion();
        };