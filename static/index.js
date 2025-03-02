document.addEventListener('DOMContentLoaded', function() {
    // the form in which the question are placed
    const questionContainer = document.querySelector(".questionContainer")
    
    // form to take enquiries for asking questions
    let questionForm = document.querySelector(".ask_question")

    // the main div in which the question are placed
    let questionToSubmit_div = document.querySelector(".question_to_submit")
    questionToSubmit_div.style.display = "none"
    
    
    questionForm.addEventListener('submit', function (event) {
        event.preventDefault()
        let numOfquestion = document.querySelector(".numberOfquestion").value
        let numOfoption = document.querySelector(".numOfoption").value
        let allQuestions = document.createElement("div")
        localStorage.setItem("numOfquestion", numOfquestion)
        localStorage.setItem("numOfoption", numOfoption)
        let stage = document.querySelector(".stage").value
        localStorage.setItem("stage", stage)
        let subject = document.querySelector(".subject").value
        localStorage.setItem("subject", subject)

        for (let i = 0; i < numOfquestion; i++) {
            // each question is wrapped in a the div
            let questionNum = document.createElement("div")
            questionNum.style.padding = "15px 0";
            let questionlabel = document.createElement("label")
            questionlabel.textContent = `${i + 1}-`
            questionNum.appendChild(questionlabel)
            questionNum.classList.add("col-12")
            // an input to store the question 
            let question = document.createElement("input")
            let j = 0
            question.setAttribute("type", "text")
            question.classList.add("form-contol")
            question.classList.add("question")
            questionNum.appendChild(question)
            let div = document.createElement("div")
            div.style.padding = "14px 0 7px 0";
            let optionLable = document.createElement("label")
            optionLable.textContent = (String.fromCharCode(97 + j) + "-")
            let answer = document.createElement("input")
            let answer_explain = document.createElement("input")
            answer.style.padding = "7px 0"
            answer.setAttribute("type", "radio")
            answer.setAttribute("name", `option${j + 1}`)
            answer.classList.add("oui")
            let label = document.createElement("input")
            label.setAttribute("type", "text")
            label.setAttribute("placeholder", "The answer here")
            label.classList.add("correct_answer")
            // answer_explain.setAttribute("type", "text")
            answer_explain.setAttribute("placeholder", "Explain the answer here")
            answer_explain.classList.add("answer_explain")
            answer_explain.style.margin = "7px 0 7px 50px";
            div.appendChild(optionLable)
            div.appendChild(answer)
            div.appendChild(label)
            questionNum.appendChild(div)
            questionNum.appendChild(answer_explain)
    
            for (j = 1; j < numOfoption; j++) {
                let div = document.createElement("div")
                let option = document.createElement("input")
                let optionLable = document.createElement("label")
                optionLable.textContent = (String.fromCharCode(97 + j) + "-")
                div.style.padding = "7px 0";
                option.setAttribute("type", "radio")
                option.setAttribute("name", `option${j + 1}`)
                option.classList.add("option")
                
                let label = document.createElement("input")
                label.setAttribute("placeholder", "Option here")
                label.classList.add("incorrect_option")
                div.appendChild(optionLable)
                div.appendChild(option)
                div.appendChild(label)
                questionNum.appendChild(div)
                
                questionForm.style.display = "none"
                allQuestions.appendChild(questionNum)
                questionToSubmit_div.style.display = ""
            }
            console.log('Yes')
            questionContainer.style.display = "block"
            questionContainer.appendChild(allQuestions)
        }
    })
   
    const allquestionset = document.querySelector("#allQuestions")
    console.log(allquestionset)
   
    allquestionset.addEventListener('submit', function (event) {
        event.preventDefault()
        console.log(allquestionset)
        
        // let all_questions = document.querySelectorAll('[class^="question"]')
        numOfoption = localStorage.getItem("numOfoption")
        localStorage.removeItem("allQuestions ")
        let allQuestions = localStorage.getItem("numOfquestion")
      
        
        let allAnswers = document.querySelectorAll('.correct_answer')
        console.log(allAnswers)
        
        let all_questions = document.querySelectorAll('.question')
        const allQuestionSet = []
        all_questions.forEach(question => {
            allQuestionSet.push(question.value)
        })

        let allOptions = []
        let tempOptions = []
        let all_options = document.querySelectorAll('[class^="incorrect"]')
        console.log(all_options)
        all_options.forEach(option => {
            tempOptions.push(option.value)
        })

        // console.log(tempOptions)

        for (let i = 0; i < tempOptions.length; i++) {
            let option = []
            
            for (let j = 0; j < numOfoption - 1; j++) {
                if (i * (numOfoption - 1) + j < tempOptions.length) {
                
                    option.push(tempOptions[i * (numOfoption - 1) + j])
                }
            }
            if (option.length > 0) {
                allOptions.push(option)
            }
        }

       

        let answers = []
        allAnswers.forEach(answer => {
            answers.push(answer.value)
        })


        let answer_explain = document.querySelectorAll(".answer_explain")
        let allanswers_explain = []
        answer_explain.forEach(answer => {
            allanswers_explain.push(answer.value)
        })
        let questions = document.querySelectorAll(".question")
        let allquestions = []
        questions.forEach(question => {
            allquestions.push(question.value)
        })
        stage = localStorage.getItem("stage")
        subject = localStorage.getItem("subject")

        const questionRequest = {
            stage: stage,
            subject: subject
        }
        fetch('http://127.0.0.1:5000/userIdSubjetId',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(questionRequest)
            })
            .then(response => {
                if (!response.ok) {
                    event.preventDefault()
                    throw new Error(`HTTP error! status: ${response.status}`)
                }
                return response.json()
            })
            .then((data) => {
                console.log(data)
                localStorage.setItem("subjectId", data.subjectId)
                localStorage.setItem("stageId", data.stageId)
                
            })
            .catch((error) => {
                console.log('Error', error)
            });
        
        
        stageId = localStorage.getItem("stageId")
        subjectId = localStorage.getItem("subjectId")
        console.log(stageId)
        console.log(subjectId)
            

            
        const dataTosend = {
            answers: answers,
            questions: allquestions,
            options: allOptions,
            stageId: stageId,
            answerExplain: allanswers_explain,
            subjectId: subjectId
        }

       



        fetch('http://127.0.0.1:5000/new-question', {
            method: 'POST',
            headers: {
                'content-Type': 'application/json',
            },
            body: JSON.stringify(dataTosend),
        })
            .then(response => response.json())
            .then(() => {
                localStorage.removeItem("stage")
                localStorage.removeItem("numOfquestion")
                localStorage.removeItem("numOfoption")
                localStorage.removeItem("subjectId")
                localStorage.removeItem("stageId")
                window.location.href = "/"
            }).catch((error) => {
                console.log('Error:', error)
            });
        
        console.log(answers)
        console.log(allquestions)
        console.log(allanswers_explain)
        console.log(allOptions)
        
    })
})